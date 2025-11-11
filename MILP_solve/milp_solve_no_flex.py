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
from Parameters.getData_flex import getData
import MILP_formulation.MILP_peak_power as noflex
from Result_Processing.result_processing_noflex import result_processing
import highspy



def solve_cplex(data, f, Aeq, beq, Aineq, bineq, lb, ub, heater):
    c = cplex.Cplex()
    if(heater == "I"):
        c.parameters.mip.tolerances.mipgap.set(0.07)
    elif(heater == "C"):
        c.parameters.mip.tolerances.mipgap.set(0.001)
        
    c.objective.set_sense(c.objective.sense.minimize)

    #print(c.parameters._get_info())
    types = data.n_x * "C" + data.N * f"{heater}CCC" + data.len_eps_da * "C" + data.len_epp_nom * "C"


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
    sol.time = round(end_time - start_time,3)
    sol.status_string = c.solution.get_status_string()
    if c.solution.get_status() in (101, 1, 5, 6, 102):
        sol.status = 1
        sol.x = np.array(c.solution.get_values())
    else:
        sol.status = 0
        sol.x = np.array([])
    
    sol.time = time_to_solve
    return sol

def _solve_highs(data, f, Aeq, beq, Aineq, bineq, lb, ub, heater):
    # define problem
    highs = highspy.Highs()
    highs.changeObjectiveSense(highspy.ObjSense.kMinimize)

    types = (data.n_x * "C" + data.N * f"{heater}CCC" + 2*data.n_a*data.n_z*(data.N_F+data.N_R)*f"{heater}CCC"
             +2*data.n_a*data.n_z*data.N_R*"C" + data.N*"C" + "C" + 2*"C"*(data.n_a) + "CC" + "CC")
    
    map_type = {"C":0, "I": 1, "B": 2}
    integrality = [map_type[t] for t in types]

    lb = lb.flatten()
    ub = ub.flatten()
    obj = f.flatten()
    n_var = f.shape[0]

    
    highs.addVars(n_var, lb, ub)
    highs.changeColsCost(f.shape[0],np.arange(f.shape[0]), obj)

    highs.changeColsIntegrality(f.shape[0],np.arange(f.shape[0]) , integrality)

    for i in range(Aeq.shape[0]):
        cols = Aeq[[i], :].indices.tolist()
        vals = Aeq[[i], :].data.tolist()
        rhs = beq[i, 0]
        highs.addRow(rhs, rhs,len(cols), cols, vals)

    for i in range(Aineq.shape[0]):
        cols = Aineq[[i], :].indices.tolist()
        vals = Aineq[[i], :].data.tolist()
        rhs = bineq[i, 0]
        highs.addRow(-highs.inf, rhs,len(cols), cols, vals)
    
    highs.run()

    sol = Structure()
    status = highs.getModelStatus()
    sol.status_string = str(status)
    print(sol.status_string)

    solution = highs.getSolution()

    if status == highspy.HighsModelStatus.kOptimal:
        sol.status = 1
        sol.x = np.array(solution.col_value)   # vrijednosti varijabli
    else:
        sol.status = 0
        sol.x = np.array([])

    return sol


if __name__ == "__main__":
    # --- Prvo rješenje (s cpp) ---
    heater_power=2.5
    bat_cap=10
    converter_power=2.5
    tank_volume=0.2
    PV_power=400
    numberofPV=10
    month=6
    day=15
    cpp=11
    Q = 12
    F = 1
    R = 2
    beginning_flex_ready = 11
    end_flex_ready = 13
    alfa_plus = 80
    alfa_minus = 0.811
    cr_plus = 0.7
    cr_minus = 0.7
    sgn_Pr = "positive and negative"
    cid = 0.6
    setwatertemp = 40
    hub_name = "Household"
    annual_load = 5
    annual_water = 50

    data = getData(heater_power, bat_cap, converter_power, tank_volume,PV_power, numberofPV, month,
                    day, Q, F, R, beginning_flex_ready, end_flex_ready, alfa_plus, alfa_minus, cr_plus,
                      cr_minus, sgn_Pr,hub_name, annual_load, annual_water)
    model = noflex.getModel(data)
    matrices = noflex.get_Matrices(data, model)
    lb = noflex.getLb(data, matrices)
    ub = noflex.getUb(data, matrices)
    Aineq = noflex.getAineq(data, matrices)
    bineq = noflex.getbineq(data, matrices)
    Aeq = noflex.getAeq(data, matrices, model)
    beq = noflex.getbeq(data, matrices, model)
    f = noflex.getF(data)
    solution = _solve_highs(data, f, Aeq, beq, Aineq, bineq, lb, ub, "C")
    res = result_processing(data, matrices, solution)

   