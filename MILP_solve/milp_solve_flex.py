import numpy as np
from scipy.sparse import csr_matrix
import cplex
import matplotlib.pyplot as plt
from MILP_formulation.extrasprojekt import *
import math
import sys
import os
import highspy
from Parameters.getData_flex import getData
import MILP_formulation.MILP_flex as flex
import time


def _solve_cplex(f, Aeq, beq, Aineq, bineq, lb, ub,data, heater):
    
    '''
    Solves LP by using CPLEX solver.
    Argument prob has these objects:
        f: np.array or np.matrix, cost function,
           column vector where second dimension is 1 or None
        lb: np.array or np.matrix, lower bounds,
            column vector where second dimension is 1 or None
        ub: np.array or np.matrix, upper bounds,
            column vector where second dimension is 1 or None
        Aeq: scipy.sparse.csr_matrix, matrix of linear equalities
        beq: np.array or np.matrix, vector of linear equalities,
             column vector where second dimension is 1 or None
        Aineq: scipy.sparse.csr_matrix, matrix of linear equalities
        bineq: np.array or np.matrix, vector of linear inequalities,
               column vector where second dimension is 1 or None
    Returns Structure containing:
        status: int
        status_string: string
        x: np.array
    '''

    # define problem
    c = cplex.Cplex()
    c.objective.set_sense(c.objective.sense.minimize)
    # if(heater == "I"):
    #     c.parameters.mip.tolerances.mipgap.set(0.21)
    # elif(heater == "C"):
    #     c.parameters.mip.tolerances.mipgap.set(0.001)

    types = (data.n_x * "C" + data.N * f"{heater}CCC" + 2*data.n_a*data.n_z*(data.N_F+data.N_R)*f"{heater}CCC"
             +2*data.n_a*data.n_z*data.N_R*"C" + data.N*"C" + "C" + 2*"C"*(data.n_a) + "CC" + "CCC")
    
   

    # define variables
    for i in range(f.shape[0]):
        if lb[i, 0] == -np.inf:
            lb_temp = -cplex.infinity
        else:
            lb_temp = lb[i, 0]
        if ub[i, 0] == np.inf:
            ub_temp = cplex.infinity
        else:
            ub_temp = ub[i, 0]
        c.variables.add(obj=[f[i, 0]], ub=[ub_temp], lb=[lb_temp], types=types[i])
        #print(f"Variable {i}: obj={f[i, 0]}, lb={lb_temp}, ub={ub_temp}")
        if lb_temp > ub_temp:
            print(f"Variable {i} has infeasible bounds: lb={lb_temp}, ub={ub_temp}")
            continue  # or raise an error

    # equalities - row by row
    for i in range(Aeq.shape[0]):
        cols = Aeq[[i], :].indices.tolist() #column indices
        vals = Aeq[[i], :].data.tolist() #values
        pair = cplex.SparsePair(ind=cols, val=vals)
        c.linear_constraints.add(lin_expr=[pair], senses=['E'], rhs=[beq[i, 0]])

    # inequalities - row by row
    for i in range(Aineq.shape[0]):
        cols = Aineq[[i], :].indices.tolist() #column indices
        vals = Aineq[[i], :].data.tolist() #values
        pair = cplex.SparsePair(ind=cols, val=vals)
        c.linear_constraints.add(lin_expr=[pair], senses=['L'], rhs=[bineq[i, 0]])

    #c.parameters.read.datacheck.set(1)
    #c.parameters.preprocessing.presolve.set(0)
    c.parameters.conflict.display.set(2) 
    c.set_log_stream(sys.stdout)
    c.set_error_stream(sys.stderr)
    c.set_warning_stream(sys.stdout)
    c.set_results_stream(sys.stdout)

    # Use only dual simplex method
    #c.parameters.lpmethod.set(c.parameters.lpmethod.values.dual)

    # solve
    start_time = time.time()
    c.solve()
    end_time = time.time()

    print(f"Solving time: {end_time - start_time}")
    
    # c.conflict.refine()
    # conflicts = c.conflict.get()
    # c.conflict.write("conflict.lp")

    # fill solution Structure
    sol = Structure()
    sol.status_string = c.solution.get_status_string()
    sol.time = round(end_time - start_time,3)
    print(sol.status_string)
    if c.solution.get_status() in (1, 5, 6, 101, 102):
        sol.status = 1
        sol.x = np.array(c.solution.get_values())
    else:
        sol.status = 0
        sol.x = np.array([])

    return sol

def _solve_highs(f, Aeq, beq, Aineq, bineq, lb, ub, data, heater):

    # define problem
    highs = highspy.Highs()
    highs.changeObjectiveSense(highspy.ObjSense.kMinimize)

    types = (data.n_x * "C" + data.N * f"{heater}CCC" + 2*data.n_a*data.n_z*(data.N_F+data.N_R)*f"{heater}CCC"
             +2*data.n_a*data.n_z*data.N_R*"C" + data.N*"C" + "C" + 2*"C"*(data.n_a) + "CC" + "CCC")
    
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
    
    
    start_time = time.time()
    highs.run()
    end_time = time.time()
    print(f"Solving time: {end_time - start_time}")

    sol = Structure()
    sol.time = round(end_time - start_time,3)
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
    heater_power = 50                 # Water heater power (kW)
    bat_cap = 500                     # Battery capacity (kWh)
    converter_power = 250             # Inverter power (kW)
    tank_volume = 5                   # Water tank capacity (m^3)
    PV_power = 400                    # Solar panel power (Wp)
    numberofPV = 2000                 # Number of PV panels

    # Date
    month = 2                         # from screenshot: 25.2.
    day = 25

    
    Q = 12                            # Period between activations
    F = 1                             # Activation duration
    R = 1                             # Recovery duration

    beginning_flex_ready = 0          # 0:00
    end_flex_ready = 12               # 12:00

    alfa_plus = 90                    # Acceptance probability +
    alfa_minus = 80                   # Acceptance probability -

    cr_plus = 0.7                     # Incentive + (€/kW)
    cr_minus = 0.7                    # Incentive - (€/kW)

    sgn_Pr = "positive and negative"  # Direction of flexibility service

    

    

    hub_name = "Industry"             # Renewable energy hub

    annual_load = 4000                # Annual electricity consumption (MWh)
    annual_water = 3000               # Annual tempered water consumption (m^3)


    data = getData(heater_power, bat_cap, converter_power, tank_volume,PV_power, numberofPV, month,
                    day, Q, F, R, beginning_flex_ready, end_flex_ready, alfa_plus, alfa_minus, cr_plus,
                      cr_minus, sgn_Pr,hub_name, annual_load, annual_water, neg_prices_on_off=True)

    model = flex.getModel(data)
    matrices = flex.get_Matrices_nom(data, model)
    matrices_alt = flex.getMatrices_alt(data, model)
    lb = flex.getLb(data, matrices, matrices_alt)
    ub = flex.getUb(data, matrices, matrices_alt)
    Aineq = flex.getAineq(data, matrices, model, matrices_alt)
    bineq = flex.getbineq(data, matrices, matrices_alt, model)
    Aeq = flex.getAeq(data,model, matrices, matrices_alt)
    beq = flex.getbeq(data, matrices)
    f = flex.getF(data)
    heater = "C"
    solution = _solve_highs(f, Aeq, beq, Aineq, bineq, lb, ub,data, heater)

    

    
   
 
    
    