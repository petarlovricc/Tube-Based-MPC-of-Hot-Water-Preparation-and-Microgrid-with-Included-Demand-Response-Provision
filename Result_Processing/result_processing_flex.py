from MILP_formulation.extrasprojekt import *
from MILP_formulation.MILP_peak_power import getThetax
from MILP_formulation.MILP_peak_power import getPsix
import pandas as pd
import numpy as np
from Parameters.getData_flex import get_Ki
from Parameters.getData_flex import get_Kzx
import matplotlib.pyplot as plt
import MILP_formulation.MILP_flex as flex
from Parameters.getData_flex import getData
from MILP_solve.milp_solve_flex import _solve_cplex
import sys
from MILP_formulation.MILP_flex import getF
print("Python koji se koristi:", sys.executable)


def result_processing(data, model, matrices, matrices_alt, solution):
    if(solution.status_string == "HighsModelStatus.kInfeasible"):
        return
    res = Structure()
    res.case = "flex"
    
    res.time = solution.time
    res.solution = solution.x
    res.delte = res.solution[data.n_x:data.n_x+data.n_u*data.N:data.n_u]
    res.Ech_nom = res.solution[data.n_x+1:data.n_x+data.n_u*data.N:data.n_u]
    res.Edch_nom = res.solution[data.n_x+2:data.n_x+data.n_u*data.N:data.n_u]
    res.EPV_nom = res.solution[data.n_x+3:data.n_x+data.n_u*data.N:data.n_u]
    res.x_0 = res.solution[0:data.n_x]

    U_alt_plus_beg = data.n_x+data.n_u*data.N
    U_alt_plus_end = U_alt_plus_beg + data.n_u*data.n_a*data.n_z*(data.N_F+data.N_R)
    res.delte_alt_plus = res.solution[U_alt_plus_beg:U_alt_plus_end:data.n_u]
    res.Ech_alt_plus = res.solution[U_alt_plus_beg+1:U_alt_plus_end:data.n_u]
    res.Edch_alt_plus = res.solution[U_alt_plus_beg+2:U_alt_plus_end:data.n_u]
    res.EPV_alt_plus = res.solution[U_alt_plus_beg+3:U_alt_plus_end:data.n_u]

    U_alt_minus_beg = U_alt_plus_end
    U_alt_minus_end = U_alt_minus_beg + data.n_u*data.n_a*data.n_z*(data.N_F+data.N_R)
    res.delte_alt_minus = res.solution[U_alt_minus_beg:U_alt_minus_end:data.n_u]
    res.Ech_alt_minus = res.solution[U_alt_minus_beg+1:U_alt_minus_end:data.n_u]
    res.Edch_alt_minus = res.solution[U_alt_minus_beg+2:U_alt_minus_end:data.n_u]
    res.EPV_alt_minus = res.solution[U_alt_minus_beg+3:U_alt_minus_end:data.n_u]
    

    Eps_abs_plus_beg = U_alt_minus_end
    Eps_abs_plus_end = Eps_abs_plus_beg + data.N_R*data.n_a*data.n_z
    res.eps_abs_plus_alt = res.solution[Eps_abs_plus_beg:Eps_abs_plus_end]

    Eps_abs_minus_beg = Eps_abs_plus_end
    Eps_abs_minus_end = Eps_abs_minus_beg + data.N_R*data.n_a*data.n_z
    res.eps_abs_minus_alt = res.solution[Eps_abs_minus_beg:Eps_abs_minus_end]

    da_beg = Eps_abs_minus_end
    da_end = da_beg + data.N
    res.da = res.solution[da_beg: da_end]
    epp_beg = da_end
    epp_end = da_end + 1 + data.n_a
    res.epp = res.solution[epp_beg:epp_end]
    res.epp_nom = res.epp[0]
    res.epp_alt_plus = res.epp[1:]
    res.epp_alt_minus  = res.solution[epp_end: epp_end + data.n_a]
    res.Pr_plus = res.solution[-5]
    res.Pr_minus = res.solution[-4]
    res.emax_plus = res.solution[-3]
    res.emax_minus = res.solution[-2]
    res.emax_plus_minus = res.solution[-1]

    res.PPV_nom = res.EPV_nom*4
    res.PPV_alt_plus = res.EPV_alt_plus*4
    res.PPV_alt_minus = res.EPV_alt_minus*4

    res.grid_energy_nom = data.nc_load_energy - res.EPV_nom + data.P_heater*data.ts*res.delte + res.Ech_nom - res.Edch_nom
    res.K_i = get_Ki(data)
    K_zx = get_Kzx(data)
    res.K_i_x = np.zeros((res.K_i.shape[0],res.K_i.shape[1]+1*data.n_z))
    for i in range(res.K_i.shape[0]):
        for j in range(data.n_z):
            res.K_i_x[i][j*(data.act_len+1):(j+1)*(data.act_len+1)] = np.append(res.K_i[i][j*data.act_len:(j+1)*data.act_len], int(K_zx[i][j]))


    theta_alt = flex.getTheta_a(data, matrices_alt, model)
    psi_alt = flex.get_Psi_x_alt_two_reservations(data, model)

    res.x_alt = theta_alt@res.solution.reshape(-1,1)+psi_alt

    res.x_alt_plus = res.x_alt[:data.n_x*data.n_a*data.n_z*(data.N_F+data.N_R+1)]
    res.x_alt_minus = res.x_alt[data.n_x*data.n_a*data.n_z*(data.N_F+data.N_R+1):]

    res.temp_alt_plus = res.x_alt_plus[0::2].ravel()
    res.SOE_alt_plus = res.x_alt_plus[1::2].ravel()
    res.tempC_alt_plus = res.temp_alt_plus - 273.15
    res.SOE_alt_plus = res.x_alt_plus[1::2]

    res.temp_alt_minus = res.x_alt_minus[0::2].ravel()
    res.SOE_alt_minus = res.x_alt_minus[1::2].ravel()
    res.tempC_alt_minus = res.temp_alt_minus - 273.15
    res.SOE_alt_minus = res.x_alt_minus[1::2]




    theta_nom = flex.getTheta_n(data, matrices)
    psi_nom = flex.getPsix_nom(data, matrices)

    res.x_nom = theta_nom@res.solution.reshape(-1,1)+psi_nom

    res.temp_nom = np.append(res.x_0[0], res.x_nom[0::2])
    res.SOE_nom = np.append(res.x_0[1], res.x_nom[1::2])
    res.tempC_nom = res.temp_nom - 273.15

    #Izdvajanje proizvodnje i potrošnje za vrijeme alternativnih profila
    res.nc_load_energy_alt = np.zeros((data.n_a,data.n_z*(data.N_F+data.N_R)))

    for i in range(data.n_a):
        for j in range(data.n_z*(data.N_F+data.N_R)):
            res.nc_load_energy_alt[i][j] = data.nc_load_energy[int(res.K_i[i][j])]


    res.pv_energy_alt = np.zeros((data.n_a,data.n_z*(data.N_F+data.N_R)))

    for i in range(data.n_a):
        for j in range(data.n_z*(data.N_F+data.N_R)):
            res.pv_energy_alt[i][j] = data.pv_energy[int(res.K_i[i][j])]


    #RAZDVAJANJE VEKTORA ALTERNATIVNIH PROFILA NA POJEDINE ALTERNATIVNE PROFILE

    #alternativni profili za pozitivnu rezervaciju
    res.delte_profili_plus = np.zeros((data.n_a, data.n_z*(data.N_F+data.N_R)))

    for i in range(data.n_a):
        res.delte_profili_plus[i] = res.delte_alt_plus[i*data.n_z*(data.N_F+data.N_R):(i+1)*data.n_z*(data.N_F+data.N_R)]

    Ech_profili_plus = np.zeros((data.n_a, data.n_z*(data.N_F+data.N_R)))

    for i in range(data.n_a):
        Ech_profili_plus[i] = res.Ech_alt_plus[i*data.n_z*(data.N_F+data.N_R):(i+1)*data.n_z*(data.N_F+data.N_R)]

    Edch_profili_plus = np.zeros((data.n_a, data.n_z*(data.N_F+data.N_R)))

    for i in range(data.n_a):
        Edch_profili_plus[i] = res.Edch_alt_plus[i*data.n_z*(data.N_F+data.N_R):(i+1)*data.n_z*(data.N_F+data.N_R)]

    
    res.EPV_profili_plus = np.zeros((data.n_a, data.n_z*(data.N_F+data.N_R)))
    for i in range(data.n_a):
        res.EPV_profili_plus[i] = res.EPV_alt_plus[i*data.n_z*(data.N_F+data.N_R):(i+1)*data.n_z*(data.N_F+data.N_R)]

    res.grid_energy_alt_plus = np.zeros((data.n_a, data.n_z*(data.N_F+data.N_R)))

    for i in range(data.n_a):
        res.grid_energy_alt_plus[i] = (
            res.nc_load_energy_alt[i]
            - res.EPV_profili_plus[i]
            + data.P_heater*data.ts*res.delte_profili_plus[i]
            + Ech_profili_plus[i]
            - Edch_profili_plus[i]
        )

    #alternativni profili za negativnu rezervaciju
    res.delte_profili_minus = np.zeros((data.n_a, data.n_z*(data.N_F+data.N_R)))

    for i in range(data.n_a):
        res.delte_profili_minus[i] = res.delte_alt_minus[i*data.n_z*(data.N_F+data.N_R):(i+1)*data.n_z*(data.N_F+data.N_R)]

    Ech_profili_minus = np.zeros((data.n_a, data.n_z*(data.N_F+data.N_R)))

    for i in range(data.n_a):
        Ech_profili_minus[i] = res.Ech_alt_minus[i*data.n_z*(data.N_F+data.N_R):(i+1)*data.n_z*(data.N_F+data.N_R)]

    Edch_profili_minus = np.zeros((data.n_a, data.n_z*(data.N_F+data.N_R)))

    for i in range(data.n_a):
        Edch_profili_minus[i] = res.Edch_alt_minus[i*data.n_z*(data.N_F+data.N_R):(i+1)*data.n_z*(data.N_F+data.N_R)]

    res.EPV_profili_minus = np.zeros((data.n_a, data.n_z*(data.N_F+data.N_R)))
    for i in range(data.n_a):
        res.EPV_profili_minus[i] = res.EPV_alt_minus[i*data.n_z*(data.N_F+data.N_R):(i+1)*data.n_z*(data.N_F+data.N_R)]

    res.grid_energy_alt_minus = np.zeros((data.n_a, data.n_z*(data.N_F+data.N_R)))

    for i in range(data.n_a):
        res.grid_energy_alt_minus[i] = (
            res.nc_load_energy_alt[i]
            - res.EPV_profili_minus[i]
            + data.P_heater*data.ts*res.delte_profili_minus[i]
            + Ech_profili_minus[i]
            - Edch_profili_minus[i]
        )


    grid_nom_alt_power = np.zeros((data.n_a,data.n_z*(data.N_F+data.N_R)))

    for i in range(data.n_a):
        for j in range(data.n_z*(data.N_F+data.N_R)):
            grid_nom_alt_power[i][j] = res.grid_energy_nom[int(res.K_i[i][j])]*4

    res.Jn = get_Jn(data, res)
    maxInd_plus, Jai_plus  = calculateJai_plus(data, res)
    res.maxJai_plus = Jai_plus[maxInd_plus]

    maxInd_minus, Jai_minus  = calculateJai_minus(data, res)
    res.maxJai_minus = Jai_minus[maxInd_minus]

    res.grid_power_nom = res.grid_energy_nom*4
    res.grid_power_alt_plus = res.grid_energy_alt_plus*4
    res.grid_power_alt_minus = res.grid_energy_alt_minus*4


    res.JDR = getJDR(data, res)
    
    ####################################
    res.table_nom, res.table_plus, res.table_minus, res.worst_ind_plus, res.worst_ind_minus = getTable(data, res)

    if (res.maxJai_plus >= res.maxJai_minus):
        res.worst_ind = res.worst_ind_plus
    else:
        res.worst_ind = res.worst_ind_minus


    res.table2_nom, res.table2_plus, res.table2_minus = getTable_flow(data,res)

    return res

def getTable(data, res):
    ROWS = 6
    resultlist  = np.zeros((ROWS, data.n_a))  # Nominal
    resultlist2 = np.zeros((ROWS, data.n_a))  # Positive DR
    resultlist3 = np.zeros((ROWS, data.n_a))  # Negative DR

    if res is None:
        for i in range(data.n_a):
            for r in range(ROWS):
                resultlist[r][i]  = -1
                resultlist2[r][i] = -1
                resultlist3[r][i] = -1

        maxJai_plus = None
        maxJai_minus = None

    else:
        maxJai_plus, Jai_plus   = calculateJai_plus(data, res)
        maxJai_minus, Jai_minus = calculateJai_minus(data, res)

        intraday_plus  = get_intraday_plus(data, res)
        intraday_minus = get_intraday_minus(data, res)
        Jn              = get_Jn(data, res)

        for i in range(data.n_a):

            # 0) Reserved power [kW]
            resultlist[0][i]  = -1                      # nominal
            resultlist2[0][i] =  res.Pr_plus  / 1000    # positive DR
            resultlist3[0][i] =  res.Pr_minus / 1000    # negative DR

            # 1) Day-ahead cost
            resultlist[1][i]  = sum(res.da)
            resultlist2[1][i] = -1
            resultlist3[1][i] = -1

            # 2) Peak power cost
            resultlist[2][i]  = res.epp_nom          * data.cpp
            resultlist2[2][i] = res.epp_alt_plus[i]  * data.cpp
            resultlist3[2][i] = res.epp_alt_minus[i] * data.cpp

            # 3) Intraday cost
            resultlist[3][i]  = -1
            resultlist2[3][i] = intraday_plus[i]
            resultlist3[3][i] = intraday_minus[i]

            # 4) Energy cost
            resultlist[4][i]  = Jn
            resultlist2[4][i] = -1
            resultlist3[4][i] = -1

            # 5) Operational cost (updated)
            resultlist[5][i]  = get_J_no_act(data, res, "nominal",i)
            resultlist2[5][i] = get_J_no_act(data, res, "positive", i)
            resultlist3[5][i] = get_J_no_act(data, res, "negative", i)

    return resultlist, resultlist2, resultlist3, maxJai_plus, maxJai_minus


def getTable_flow(data, res):
    ROWS = 3
    resultlist = np.zeros((ROWS,data.n_a))
    resultlist2 = np.zeros((ROWS,data.n_a))
    resultlist3 = np.zeros((ROWS,data.n_a))

    for i in range(data.n_a):
        resultlist[0][i] = sum(res.delte*data.P_heater)*0.25/1000
        resultlist[1][i] = sum(res.grid_energy_nom)/1000
        resultlist[2][i] = sum(res.EPV_nom)/1000

        resultlist2[0][i] = (sum(res.delte*data.P_heater)*0.25 -
                             getNomSumAltInd(res,res.delte, i)*data.P_heater*0.25 + sum(res.delte_profili_plus[i]*data.P_heater)*0.25)/1000
        resultlist2[1][i] = (sum(res.grid_energy_nom) - getNomSumAltInd(res,res.grid_energy_nom, i) + sum(res.grid_energy_alt_plus[i]))/1000
        resultlist2[2][i] = (sum(res.EPV_nom) - getNomSumAltInd(res,res.EPV_nom, i) + sum(res.EPV_profili_plus[i]))/1000


        resultlist3[0][i] = (sum(res.delte*data.P_heater)*0.25 - getNomSumAltInd(res,res.delte, i)*data.P_heater*0.25
                              + sum(res.delte_profili_minus[i]*data.P_heater)*0.25)/1000
        resultlist3[1][i] = (sum(res.grid_energy_nom) - getNomSumAltInd(res,res.grid_energy_nom, i) + sum(res.grid_energy_alt_minus[i]))/1000
        resultlist3[2][i] = (sum(res.EPV_nom) - getNomSumAltInd(res,res.EPV_nom, i) + sum(res.EPV_profili_minus[i]))/1000
       
    return resultlist, resultlist2, resultlist3

def getNomSumAltInd(res,value, alt_scen):
    suma = 0
    for i in res.K_i[alt_scen]:
        suma+= value[int(i)]
    return suma


def calculateJai_plus(data,res):
    Jai = np.zeros(data.n_a)
    for i in range(data.n_a):
        Jai[i] = data.cpp*res.epp_alt_plus[i]+sum(res.da)+sum(res.eps_abs_plus_alt[i*data.N_R*data.n_z:(i+1)*data.N_R*data.n_z])*data.cid

    maxJai = np.where(Jai == max(Jai))[0][0]

    return maxJai, Jai

def calculateJai_minus(data,res):
    Jai = np.zeros(data.n_a)
    for i in range(data.n_a):
        Jai[i] = data.cpp*res.epp_alt_minus[i]+sum(res.da)+sum(res.eps_abs_minus_alt[i*data.N_R*data.n_z:(i+1)*data.N_R*data.n_z])*data.cid

    maxJai = np.where(Jai == max(Jai))[0][0]

    return maxJai, Jai

def get_intraday_minus(data, res):
    id = np.zeros(data.n_a)
    for i in range(data.n_a):
        id[i] = sum(res.eps_abs_minus_alt[i*data.N_R*data.n_z:(i+1)*data.N_R*data.n_z])*data.cid
    return id

def get_intraday_plus(data, res):
    id = np.zeros(data.n_a)
    for i in range(data.n_a):
        id[i] = sum(res.eps_abs_plus_alt[i*data.N_R*data.n_z:(i+1)*data.N_R*data.n_z])*data.cid
    return id

def getJDR(data, res):
    return getF(data).T@res.solution

def get_Jn(data,res):
    Jn =  data.cpp*res.epp_nom + sum(res.da)
    return Jn

def get_J_no_act(data,res, profile, ind):
    Jn = 0

    if(profile == "nominal"):
        Jn =  data.cpp*res.epp_nom + sum(res.da) - data.cr_plus*abs(res.Pr_plus) - data.cr_minus*abs(res.Pr_minus)
    elif(profile == "positive"):
        Jn =  (data.cpp*res.epp_alt_plus[ind] + sum(res.da) 
               - data.cr_plus*abs(res.Pr_plus) - data.cr_minus*abs(res.Pr_minus) + get_intraday_plus(data, res)[ind])
    elif(profile == "negative"):
        Jn =  (data.cpp*res.epp_alt_minus[ind] + sum(res.da) 
               - data.cr_minus*abs(res.Pr_minus) - data.cr_plus*abs(res.Pr_plus) + get_intraday_minus(data, res)[ind])
    return Jn 

   