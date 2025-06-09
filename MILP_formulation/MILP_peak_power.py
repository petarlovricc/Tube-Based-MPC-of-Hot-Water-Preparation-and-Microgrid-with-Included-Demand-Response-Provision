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

#funkcija koja sluzi stvaranju strukture
def getData(heater_power, bat_cap, converter_power, tank_volume,PV_power, numberofPV, buyPriceHigh, buyPriceLow, month, day, cpp):
    data = Structure()

    PV_reader = PVreader(day=day, month=month, PV_power=PV_power, numberofPV=numberofPV) #klasa koja postavlja dan 
    disturbance_reader = CSV_disturbances_reader()
    
    #Podatci o dimenzijama matrica
    data.N =  96 #broj 15min intervala u jednom danu
    data.len_x0 = 2 #[T(k) SOE(k)]
    data.len_U_noflex = 3*data.N #duljina upravljackog ulaza nominalnog profila
    data.len_eps_da = data.N #duljina vektora epsilona day ahead energije
    data.len_epp_noflex = 1 #epsilon za peak power bez fleksibilnosti
    
    #duljina optimizacijskog vektora
    data.len_chi = (data.len_x0 + data.len_U_noflex + data.len_eps_da + data.len_epp_noflex)


    data.P_heater = heater_power #snaga grijača u W
    data.ts = 0.25 #duljina perioda diskretizacije u satima
    data.E_bat_max = bat_cap #kapacitet baterije u Wh
    data.P_PC = converter_power #snaga pretvarača snage
    data.tank_volume = tank_volume/1000 #volumen vode u spremniku(m3)
    data.tank_radius = (data.tank_volume / (4 * math.pi))**(1/3)  #promjer spremnika vode
    data.tank_area = 10 * math.pi * data.tank_radius**2  #vanjska povrsina spremnika vode
    data.Lambda = 0.0245 #koeficijent toplinske vodljivosti
    data.thickness = 0.05 #debljina spremnika vode u m
    data.R = data.thickness/(data.Lambda*data.tank_area) 
    data.ro_water = 1000 #kg/m3
    data.c_water = 4200/3600 #Wh(kg^-1)(K-1)
    data.nCh = 0.9 #efikasnost punjenja baterije
    data.nDch = 0.9 #efikasnost pražnjenja baterije



    data.m_w_tank = data.tank_volume*data.ro_water
    data.cold_water_temp = 7+273.15 #temperatura hladne vode (°C -> K) 
    data.boiling_temp = 100+273.15 # maksimalna željena temperatura vode u grijaču

    #Podatci o proizvodnji i potrošnji
    data.pv_power, data.pv_energy, data.pv_energy_sum = PV_reader.csvreader()
    data.env_temp_K, data.env_temp_C = disturbance_reader.environment_Temperature()
    data.set_water_temp_K, data.set_water_temp_C = disturbance_reader.setWaterTemparray()
    data.water_demand = disturbance_reader.csvreaderWater() #kg/h
    data.nc_load_power, data.nc_load_energy, data.sum_nc_load_energy = disturbance_reader.csvreaderElectricity()
    data.mul_TQ = data.set_water_temp_K*data.water_demand
    #Cijene davanja i preuzimanja te cijena vršne snage
    data.cpp = cpp/1000  #cijena vrsne snage €/kWh --> €/Wh
    data.c_buy = np.r_[np.repeat(buyPriceLow,28), np.repeat(buyPriceHigh,56)
                       ,np.repeat(buyPriceLow,12)] /1000 #€/kWh --> €/Wh
    data.c_sell = data.c_buy*0.8

    #################################################################################

    #Gornje i donje granice protoka i temperature
    data.Qmax = data.water_demand.max() #maksimalni protok vode u danu

    #Ogranicenje temperature Thot(k) vezano za Qmix(k-1) i Tmix(k-1)
    data.Tmin_interval_before = ((data.water_demand)/data.Qmax*
                                (data.set_water_temp_K-data.cold_water_temp)+data.cold_water_temp).reshape(-1,1)

    #Ogranicenje temperature Thot(k) vezano za Qmix(k) i Tmix(k), s time da je isto ogr. za Qmix(N-1)
    data.Tmin_interval_after = np.r_[data.Tmin_interval_before[1:].ravel(),data.Tmin_interval_before[-1]].reshape(-1,1)
    data.Tmax = data.boiling_temp

    return data


def getModel(data):
    model = Structure()
    model.kapa1 = -1/(data.R*data.m_w_tank*data.c_water)
    model.kapa2 = data.P_heater/(data.m_w_tank*data.c_water)
    
    a11 = np.exp(model.kapa1*data.ts)
    model.A = np.array([[a11, 0],
                       [0, 1]],dtype="float64")
    
    b11 = (np.exp(model.kapa1*data.ts)-1)*model.kapa1**-1*model.kapa2
    model.B = np.array([[b11, 0, 0],
                       [0, data.nCh, -1/data.nDch]])
    
    c11 = (np.exp(model.kapa1*data.ts)-1)*model.kapa1**-1/(data.R*data.m_w_tank*data.c_water)

    model.C = np.array([[c11],
                        [0]])
    
    d11 = -(np.exp(model.kapa1*data.ts)-1)*model.kapa1**-1/(data.m_w_tank)
    model.D = np.array([[d11],
                        [0]])
    
    e11 = (np.exp(model.kapa1*data.ts)-1)*model.kapa1**-1*(data.cold_water_temp/data.m_w_tank)
    model.E = np.array([[e11],
                        [0]])


    return model

def get_Matrices(data,model):
    matrices = Structure()

    matrices.u_min = np.zeros((3,1))
    matrices.u_max = np.array([1, data.P_PC*data.ts,data.P_PC*data.ts]).reshape(-1,1)

    matrices.x0_min = np.array([data.Tmin_interval_before[0][0],0.2*data.E_bat_max]).reshape(-1,1)
    matrices.x0_max = np.array([data.Tmax,0.8*data.E_bat_max]).reshape(-1,1)

    matrices.X_max = np.tile(matrices.x0_max, (data.N,1))

    matrices.X_min_1 = np.zeros((data.N*2,1))
    matrices.X_min_1[::2] = data.Tmin_interval_before
    matrices.X_min_1[1::2]= 0.2*data.E_bat_max

    matrices.X_min_2 = np.zeros((data.N*2,1))
    matrices.X_min_2[::2] = data.Tmin_interval_after
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
    lb = np.vstack((matrices.x0_min, U_min, np.tile(0,(data.len_eps_da ,1)), -np.inf))
    
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
    mat_x0_zeros = np.zeros((data.N, data.len_x0))
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
    mat_x0_zeros = np.zeros((data.N, data.len_x0))
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
    mat_x0_zeros = np.zeros((data.N, data.len_x0))
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
    mat_x0_zeros = np.zeros((data.N, data.len_x0))
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
    f = np.r_[np.zeros((data.len_x0)),np.zeros((data.len_U_noflex)),
             np.ones((data.len_eps_da)), data.cpp]
    return f.reshape(-1,1)

def solve_cplex(data, f, Aeq, beq, Aineq, bineq, lb, ub):
    c = cplex.Cplex()
    c.parameters.mip.tolerances.mipgap.set(0.02)
    c.parameters.preprocessing.reduce.set(0)
    
    c.objective.set_sense(c.objective.sense.minimize)

    #print(c.parameters._get_info())
    types = data.len_x0 * "C" + data.N * "ICC" + data.len_eps_da * "C" + data.len_epp_noflex * "C"


    for i in range(f.shape[0]):
        c.variables.add(obj=[f.ravel()[i]], ub=[ub.ravel()[i]], lb=[lb.ravel()[i]], types=types[i])

    for i in range(Aeq.shape[0]):
        cols = Aeq[[i], :].indices.tolist() 
        vals = Aeq[[i], :].data.tolist()
        pair = cplex.SparsePair(ind=cols, val=vals)
        c.linear_constraints.add(lin_expr=[pair], senses=['E'], rhs=[beq.flatten()[i]])

    for i in range(Aineq.shape[0]):
        cols = Aineq[[i], :].indices.tolist() 
        vals = Aineq[[i], :].data.tolist() 
        pair = cplex.SparsePair(ind=cols, val=vals)
        c.linear_constraints.add(lin_expr=[pair], senses=['L'], rhs=[bineq.flatten()[i]])

    
    start_time = c.get_time()
    c.solve()
    end_time = c.get_time()
    time_to_solve = end_time - start_time
    c.conflict.get

    sol = Structure()
    sol.status_string = c.solution.get_status_string()
    if c.solution.get_status() in (101, 1, 5, 6, 102):
        sol.status = 1
        sol.x = np.array(c.solution.get_values())
    else:
        sol.status = 0
        sol.x = np.array([])
    
    sol.time = time_to_solve
    return sol

def result_processing(data,matrices, solution):
    res = Structure()
    res.delte = solution[data.len_x0:data.len_x0+data.len_U_noflex:3]
    res.Ech = solution[data.len_x0+1:data.len_x0+data.len_U_noflex:3]
    res.Edch = solution[data.len_x0+2:data.len_x0+data.len_U_noflex:3]
    res.x_0 = solution[0:data.len_x0]
    res.eps = solution[data.len_x0+data.len_U_noflex : data.len_x0+data.len_U_noflex+data.len_eps_da]
    res.eps_peak = solution[-1]
    res.Theta = getThetax(data,matrices)
    res.Psi = getPsix(data,matrices)
    if(len(solution) > 0):
        res.x = res.Theta@solution.reshape(-1,1)+res.Psi
    else:
        return None
    res.temp = np.append(res.x_0[0], res.x[0::2])
    res.tempC = res.temp - 273.15
    res.SOE = np.append(res.x_0[1], res.x[1::2])
    res.grid_energy = data.nc_load_energy - data.pv_energy + data.P_heater*data.ts*res.delte + res.Ech - res.Edch
    
    res.grid_energy_cost = sum(res.eps)

    return res

if __name__ == "__main__": 
    data = getData(
        heater_power=2500,
        bat_cap = 9400,
        converter_power=2500,
        tank_volume=190,
        PV_power=410,
        numberofPV=20,
        buyPriceHigh=0.07,
        buyPriceLow=0.035,
        month=7,
        day=4,
        cpp=3.05
    )
    model = getModel(data)
    matrices = get_Matrices(data, model)

    lb = getLb(data,matrices)
    ub = getUb(data,matrices)
    Aineq = getAineq(data, matrices)
    bineq = getbineq(data,matrices)
    Aeq = getAeq(data,matrices,model)
    beq = getbeq(data,matrices,model)
    f = getF(data)

    solution = solve_cplex(data,f,Aeq,beq,Aineq,bineq,lb,ub)
    r = result_processing(data,matrices,solution.x)


    data = getData(
        heater_power=2500,
        bat_cap = 9400,
        converter_power=2500,
        tank_volume=190,
        PV_power=410,
        numberofPV=20,
        buyPriceHigh=0.07,
        buyPriceLow=0.035,
        month=7,
        day=4,
        cpp=0
    )
    model = getModel(data)
    matrices = get_Matrices(data, model)

    lb = getLb(data,matrices)
    ub = getUb(data,matrices)
    Aineq = getAineq(data, matrices)
    bineq = getbineq(data,matrices)
    Aeq = getAeq(data,matrices,model)
    beq = getbeq(data,matrices,model)
    f = getF(data)

    solution2 = solve_cplex(data,f,Aeq,beq,Aineq,bineq,lb,ub)
    r2 = result_processing(data,matrices,solution2.x)

    plt.step(np.arange(1, 97),r.delte)
    plt.show()
    plt.step(np.arange(1, 97),r.Ech)
    plt.show()
    plt.step(np.arange(1, 97),r.grid_energy)
    plt.step(np.arange(1, 97),r2.grid_energy)
    plt.show()


    plt.step(np.arange(1, 97),r.temp[1:]-273.15)
    plt.step(np.arange(1, 97),data.Tmin_interval_before-273.15)
    plt.show()

