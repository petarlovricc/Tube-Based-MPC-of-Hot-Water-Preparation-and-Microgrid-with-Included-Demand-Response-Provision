from MILP_formulation.extrasprojekt import *
from MILP_formulation.MILP_peak_power import getThetax
from MILP_formulation.MILP_peak_power import getPsix
import numpy as np

def result_processing(data,matrices, solution):
    res = Structure()
    res.case = "noflex"
    
    res.solution = solution.x
    res.delte = res.solution[data.n_x:data.n_x+data.len_U_nom:data.n_u]
    res.Ech = res.solution[data.n_x+1:data.n_x+data.len_U_nom:data.n_u]
    res.Edch = res.solution[data.n_x+2:data.n_x+data.len_U_nom:data.n_u]
    res.EPV_used = res.solution[data.n_x+3:data.n_x+data.len_U_nom:data.n_u]
    res.PPV_used = res.EPV_used/data.ts
    res.x_0 = res.solution[0:data.n_x]
    res.eps = res.solution[data.n_x+data.len_U_nom : data.n_x+data.len_U_nom+data.len_eps_da]
    res.eps_peak = res.solution[-1]
    res.Theta = getThetax(data,matrices)
    res.Psi = getPsix(data,matrices)
    if(len(res.solution) > 0):
        res.x = res.Theta @ res.solution.reshape(-1,1)+res.Psi
    else:
        return None
    res.temp = np.append(res.x_0[0], res.x[0::2])
    res.tempC = res.temp - 273.15
    res.SOE = np.append(res.x_0[1], res.x[1::2])
    res.grid_energy = data.nc_load_energy - res.EPV_used + data.P_heater*data.ts*res.delte + res.Ech - res.Edch
    
    res.grid_energy_cost = sum(res.eps)

    res.table = getTable(data, res)

    res.table2 = getTable_flow(data, res)


    res.grid_power = res.grid_energy*4

    return res

def getTable(data,res):
    Jn = get_Jn(data, res)
    resultlist = np.zeros((11,1))
    resultlist[0][0] = sum(res.eps)
    resultlist[1][0] = res.eps_peak * data.cpp
    resultlist[2][0] = -1
    resultlist[3][0] = -1
    resultlist[4][0] = -1
    resultlist[5][0] = -1
    resultlist[6][0] = -1
    resultlist[7][0] = -1
    resultlist[8][0] = Jn
    resultlist[9][0] = -1
    resultlist[10][0] = -1
    return resultlist

def getTable_flow(data,res):
    resultlist = np.zeros((7,1))
    resultlist[0][0] = -1
    resultlist[1][0] = -1
    resultlist[2][0] = sum(res.delte*data.P_heater)*0.25/1000
    resultlist[3][0] = -1
    resultlist[4][0] = -1
    resultlist[5][0] = sum(res.grid_energy)/1000
    resultlist[6][0] = sum(res.EPV_used)/1000
    return resultlist


def get_Jn(data,res):
    Jn =  data.cpp*res.eps_peak + sum(res.eps)
    return Jn