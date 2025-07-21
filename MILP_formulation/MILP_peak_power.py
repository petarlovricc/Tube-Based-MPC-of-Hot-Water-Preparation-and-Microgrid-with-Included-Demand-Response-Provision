import numpy as np
from scipy.sparse import csr_matrix
import cplex
import matplotlib.pyplot as plt
from MILP_formulation.extrasprojekt import *
import math
import sys
import os

from Profiles_Readers.PV_reader import PVreader
from Profiles_Readers.Disturbances_Reader import CSV_disturbances_reader


def getModel(data):
    model = Structure()
    model.kapa1 = -1/(data.R*data.m_w_tank*data.c_water)
    model.kapa2 = data.P_heater/(data.m_w_tank*data.c_water)
    
    model.a11 = np.exp(model.kapa1*data.ts)
    model.A = np.array([[model.a11, 0],
                       [0, 1]],dtype="float64")
    
    model.b11 = (np.exp(model.kapa1*data.ts)-1)*model.kapa1**-1*model.kapa2
    model.B = np.array([[model.b11, 0, 0],
                       [0, data.nCh, -1/data.nDch]])
    
    model.c11 = (np.exp(model.kapa1*data.ts)-1)*model.kapa1**-1/(data.R*data.m_w_tank*data.c_water)

    model.C = np.array([[model.c11],
                        [0]])
    
    model.d11 = -(np.exp(model.kapa1*data.ts)-1)*model.kapa1**-1/(data.m_w_tank)
    model.D = np.array([[model.d11],
                        [0]])
    
    model.e11 = (np.exp(model.kapa1*data.ts)-1)*model.kapa1**-1*(data.cold_water_temp/data.m_w_tank)
    model.E = np.array([[model.e11],
                        [0]])


    return model

def get_Matrices(data,model):
    matrices = Structure()

    matrices.u_min = np.zeros((3,1))
    matrices.u_max = np.array([1, data.P_PC*data.ts,data.P_PC*data.ts]).reshape(-1,1)

    
    #Ogranicenje temperature Thot(k) vezano za Qmix(k-1) i Tmix(k-1)
    matrices.Tmin_interval_before = ((data.water_demand)/data.Qmax*
                                (data.set_water_temp_K-data.cold_water_temp)+data.cold_water_temp).reshape(-1,1)

    #Ogranicenje temperature Thot(k) vezano za Qmix(k) i Tmix(k), s time da je isto ogr. za Qmix(N-1)
    matrices.Tmin_interval_after = np.r_[matrices.Tmin_interval_before[1:].ravel(),matrices.Tmin_interval_before[-1]].reshape(-1,1)

    matrices.x0_min = np.array([matrices.Tmin_interval_before[0][0],0.2*data.E_bat_max]).reshape(-1,1)
    matrices.x0_max = np.array([data.Tmax,0.8*data.E_bat_max]).reshape(-1,1)

    matrices.X_max = np.tile(matrices.x0_max, (data.N,1))


    matrices.X_min_1 = np.zeros((data.N*2,1))
    matrices.X_min_1[::2] =  matrices.Tmin_interval_before
    matrices.X_min_1[1::2]= 0.2*data.E_bat_max

    matrices.X_min_2 = np.zeros((data.N*2,1))
    matrices.X_min_2[::2] = matrices.Tmin_interval_after
    matrices.X_min_2[1::2]= 0.2*data.E_bat_max

    matrices.lower_triang_AB = np.zeros((data.N*2,data.N*3))
    for i in range(data.N):
        for j in range(i+1):
             matrices.lower_triang_AB[2*i:2*(i+1),3*j:3*(j+1)] = np.linalg.matrix_power(model.A, i-j)@model.B

    matrices.lower_triang_AC = np.zeros((data.N*2,data.N))
    for i in range(data.N):
        for j in range(i+1):
             matrices.lower_triang_AC[2*i:2*(i+1),j:(j+1)] = np.linalg.matrix_power(model.A, i-j)@model.C
    
    matrices.lower_triang_AD = np.zeros((data.N*2,data.N))
    for i in range(data.N):
        for j in range(i+1):
             matrices.lower_triang_AD[2*i:2*(i+1),j:(j+1)] = np.linalg.matrix_power(model.A, i-j)@model.D

    matrices.lower_triang_AE = np.zeros((data.N*2,data.N))
    for i in range(data.N):
        for j in range(i+1):
             matrices.lower_triang_AE[2*i:2*(i+1),j:(j+1)] = np.linalg.matrix_power(model.A, i-j)@model.E

    matrices.matrix_A_x0 = np.zeros((data.N*2,2))
    for i in range(data.N):
        matrices.matrix_A_x0[2*i: 2*(i+1),:] = np.linalg.matrix_power(model.A, i+1)

    return matrices

def getLb(data,matrices):
    lb = np.zeros((data.len_chi,1))
    U_min = np.tile(matrices.u_min, (data.N ,1))
    lb = np.vstack((matrices.x0_min, U_min, np.tile(-np.inf,(data.len_eps_da ,1)), 0))
    
    return lb

def getUb(data,matrices):
    ub = np.zeros((data.len_chi,1))
    U_max = np.tile(matrices.u_max, (data.N,1))
    ub = np.vstack((matrices.x0_max, U_max, np.tile(np.inf,(data.len_eps_da ,1)), np.inf))

    return ub


def getThetax(data,matrices):
    Theta = np.zeros((data.N*2, data.len_chi))
    Trailing_zeros = np.zeros((data.N*2, data.len_eps_da + data.len_epp_noflex))
    Theta = np.hstack((matrices.matrix_A_x0, matrices.lower_triang_AB, Trailing_zeros))

    return Theta

def getPsix(data, matrices):
    Psi = (matrices.lower_triang_AC@data.env_temp_K.reshape(-1,1) + 
            matrices.lower_triang_AD@data.mul_TQ.reshape(-1,1) +
            matrices.lower_triang_AE@data.water_demand.reshape(-1,1)
            )
    return Psi

def getThetaPPC(data):
    ThetaPPC = np.zeros((data.N, data.len_chi))
    mat_x0_zeros = np.zeros((data.N, data.n_x))
    mat_Un = np.zeros((data.N, data.len_U_noflex))
    for i in range(mat_Un.shape[0]):
        mat_Un[i,3*i:3*i+3] = np.array([0,1,1])

    mat_da_eps_zeros = np.zeros((data.N,data.len_eps_da + data.len_epp_noflex))

    ThetaPPC = np.hstack((mat_x0_zeros,mat_Un,mat_da_eps_zeros))

    return ThetaPPC

def getPsiPPC(data):
    PsiPPC = np.zeros((data.N,1))
    PsiPPC = np.tile(data.P_PC*data.ts, (PsiPPC.shape[0],1))

    return PsiPPC

def getThetasell(data):
    Thetasell = np.zeros((data.N,data.len_chi))
    mat_x0_zeros = np.zeros((data.N, data.n_x))
    mat_Un = np.zeros((data.N,data.len_U_noflex))
    for i in range(mat_Un.shape[0]):
        mat_Un[i,3*i:3*i+3] = np.array([data.c_sell[i]*data.P_heater*data.ts,data.c_sell[i],-data.c_sell[i]])
    mat_da = np.eye(data.len_eps_da)
    mat_eps_zeros = np.zeros((data.N, data.len_epp_noflex))

    Thetasell = np.hstack((mat_x0_zeros,mat_Un, -mat_da, mat_eps_zeros))

    return Thetasell

def getPsiSell(data):
    PsiSell = np.zeros((data.N,1))
    PsiSell = data.c_sell*(data.pv_energy-data.nc_load_energy)
    return PsiSell.reshape(-1,1)

def getThetabuy(data):
    Thetabuy = np.zeros((data.N, data.len_chi))
    mat_x0_zeros = np.zeros((data.N, data.n_x))
    mat_Un = np.zeros((data.N, data.len_U_noflex ))
    for i in range(mat_Un.shape[0]):
        mat_Un[i, 3*i:3*i+3] = np.array([data.c_buy[i]*data.P_heater*data.ts, data.c_buy[i], -data.c_buy[i]])
    mat_da = np.eye(data.len_eps_da)
    mat_eps_zeros = np.zeros((data.N, data.len_epp_noflex))

    Thetabuy = np.hstack((mat_x0_zeros, mat_Un, -mat_da, mat_eps_zeros))

    return Thetabuy

def getPsiBuy(data):
    PsiBuy = np.zeros((data.N, 1))
    PsiBuy = data.c_buy * (data.pv_energy - data.nc_load_energy)
    return PsiBuy.reshape(-1, 1)

def getThetaPP(data):
    ThetaPP = np.zeros((data.N, data.len_chi))
    mat_x0_zeros = np.zeros((data.N, data.n_x))
    mat_Un = np.zeros((data.N, data.len_U_noflex ))
    for i in range(mat_Un.shape[0]):
        mat_Un[i, 3*i:3*i+3] = np.array([data.P_heater, 1/data.ts, -1/data.ts])
    mat_da = np.zeros((data.len_eps_da, data.len_eps_da ))
    mat_eps = -np.ones((data.N, data.len_epp_noflex ))

    ThetaPP = np.hstack((mat_x0_zeros,mat_Un,mat_da,mat_eps))

    return ThetaPP

def getPsiPP(data):
    PsiBuy = np.zeros((data.N, 1))
    PsiBuy = (1/data.ts) * (data.pv_energy - data.nc_load_energy)
    return PsiBuy.reshape(-1, 1)


def getAineq(data,matrices):
    Aineq = np.vstack((
        getThetax(data,matrices),
        getThetax(data,matrices),
        -getThetax(data,matrices),
        -getThetax(data,matrices),
        getThetaPPC(data),
        getThetasell(data),
        getThetabuy(data),
        getThetaPP(data)
    ))
    return csr_matrix(Aineq)

def getbineq(data,matrices):
    bineq = np.vstack((
        matrices.X_max - getPsix(data,matrices),
        matrices.X_max - getPsix(data,matrices),
        getPsix(data,matrices) - matrices.X_min_1,
        getPsix(data,matrices) - matrices.X_min_2,
        getPsiPPC(data),
        getPsiSell(data),
        getPsiBuy(data),
        getPsiPP(data)
    ))
    return bineq

def getAeq(data,matrices,model):
    Aeq = np.zeros((2,data.len_chi))
    Aeq_x0 = np.linalg.matrix_power(model.A,data.N)-np.eye(2)
    Aeq_Un = matrices.lower_triang_AB[-2:,:]
    Aeq_da = np.zeros((2,data.len_eps_da))
    Aeq_eps = np.zeros((2,data.len_epp_noflex))

    Aeq = np.hstack((Aeq_x0,Aeq_Un,Aeq_da,Aeq_eps))

    return csr_matrix(Aeq)

def getbeq(data,matrices,model):
    beq = -(matrices.lower_triang_AC[-2:, :] @ data.env_temp_K.reshape(-1, 1) + 
        matrices.lower_triang_AD[-2:, :] @ data.mul_TQ.reshape(-1, 1) + 
        matrices.lower_triang_AE[-2:, :] @ data.water_demand.reshape(-1, 1))

    return beq



def getF(data):
    f = np.r_[np.zeros((data.n_x)),np.zeros((data.len_U_noflex)),
             np.ones((data.len_eps_da)), data.cpp]
    return f.reshape(-1,1)






