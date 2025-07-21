import numpy as np
from scipy.sparse import csr_matrix
import cplex
import matplotlib.pyplot as plt
from MILP_formulation.extrasprojekt import *
import math
import sys
import os

from collections import defaultdict
from cplex.exceptions import CplexSolverError, error_codes


from Profiles_Readers.PV_reader import PVreader
from Profiles_Readers.Disturbances_Reader import CSV_disturbances_reader
from Parameters.getData_flex import getData
import MILP_formulation.MILP_peak_power as noflex
#from Result_Processing.result_processing_noflex import result_processing
import MILP_formulation.MILP_flex as flex
import pyqtgraph as pg

from PySide6 import QtWidgets

def solve_cplex(data, f, Aeq, beq, Aineq, bineq, lb, ub, heater):
    c = cplex.Cplex()
    c.parameters.mip.tolerances.mipgap.set(0.02)
    c.parameters.preprocessing.reduce.set(0)
    
    c.objective.set_sense(c.objective.sense.minimize)

    #print(c.parameters._get_info())
    types = (data.n_x * "C" + data.N * f"{heater}CC" + data.n_a*data.n_z*(data.N_F+data.N_R)*f"{heater}CC"
             +data.n_a*data.n_z*data.N_R*"C" + data.N*"C" + "C"*(data.n_a+1) + "C" + "C")


    #for i in range(f.shape[0]):
    #    c.variables.add(obj=[f.ravel()[i]], ub=[ub.ravel()[i]], lb=[lb.ravel()[i]], types=types[i])

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



    for i in range(Aeq.shape[0]):
        cols = Aeq[[i], :].indices.tolist() 
        vals = Aeq[[i], :].data.tolist()
        pair = cplex.SparsePair(ind=cols, val=vals)
        c.linear_constraints.add(lin_expr=[pair], senses=['E'], rhs=[beq.flatten()[i]], names=[f"eq_{i}"])

    for i in range(Aineq.shape[0]):
        cols = Aineq[[i], :].indices.tolist() 
        vals = Aineq[[i], :].data.tolist() 
        pair = cplex.SparsePair(ind=cols, val=vals)
        c.linear_constraints.add(lin_expr=[pair], senses=['L'], rhs=[bineq.flatten()[i]], names=[f"ineq_{i}"])


    
    start_time = c.get_time()
    c.solve()


    c.conflict.refine(c.conflict.all_constraints())
    print("Solution status: {0} ({1})".format(c.solution.get_status_string(),
                                              c.solution.get_status()))

    # Get the conflict status for the conflict group that was specified
    # (e.g., the all constraints group was used above).
    try:
        confstatus = c.conflict.get()
    except CplexSolverError as err:
        # If the conflict refiner was unable to identify a conflict then
        # exit early.
        if err.args[2] == error_codes.CPXERR_NO_CONFLICT:
            print("A conflict was not identified.")
            print("Exiting....")
            return
        else:
            raise

    groups = c.conflict.get_groups()

    # For the purposes of this example, we only care about the constraint
    # types as they align with the conflict statuses.
    conftypes = []
    for pref, subgroup in groups:
        for grptype, index in subgroup:
            conftypes.append(grptype)

    # Count the number of conflicts found for each constraint group and
    # print the results.
    grpdict = defaultdict(int)
    for grptype, grpstat in zip(conftypes, confstatus):
        if grpstat in (c.conflict.group_status.possible_member,
                       c.conflict.group_status.member):
            grpdict[grptype] += 1

    for grptype in grpdict:
        print("{0}(s): {1}".format(c.conflict.constraint_type[grptype],
                                   grpdict[grptype]))
        
    conffile = "conflictex1.py.lp"
    print("Writing conflict file to '{0}'....".format(conffile))
    c.conflict.write(conffile)

    # Display the entire conflict subproblem.
    with open(conffile, "r") as conf_file:
        for line in conf_file:
            print(line.strip())


    end_time = c.get_time()
    time_to_solve = end_time - start_time
    #c.conflict.get

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
    if(heater == "I"):
        c.parameters.mip.tolerances.mipgap.set(0.21)
    elif(heater == "C"):
        c.parameters.mip.tolerances.mipgap.set(0.001)

    types = (data.n_x * "C" + data.N * f"{heater}CC" + data.n_a*data.n_z*(data.N_F+data.N_R)*f"{heater}CC"
             +data.n_a*data.n_z*data.N_R*"C" + data.N*"C" + "C"*(data.n_a+1) + "C" + "C")
    
   

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
    c.solve()

    
    # c.conflict.refine()
    # conflicts = c.conflict.get()
    # c.conflict.write("conflict.lp")

    # fill solution Structure
    sol = Structure()
    sol.status_string = c.solution.get_status_string()
    print(sol.status_string)
    if c.solution.get_status() in (1, 5, 6, 101, 102):
        sol.status = 1
        sol.x = np.array(c.solution.get_values())
    else:
        sol.status = 0
        sol.x = np.array([])

    return sol

if __name__ == "__main__":
    heater_power=2500
    bat_cap=9400
    converter_power=2500
    tank_volume=190
    PV_power=410
    numberofPV=10
    buyPriceHigh=0.18
    buyPriceLow=0.09
    month=7
    day=4
    cpp=1
    Q = 12
    F = 1
    R = 2
    beginning_flex_ready = 15
    end_flex_ready = 16
    alfa = 0.811
    cr = 0.7
    sgn_Pr = 1
    cid = 0.6
    data = getData(
            heater_power,
            bat_cap,
            converter_power,
            tank_volume,
            PV_power,
            numberofPV,
            buyPriceHigh,
            buyPriceLow,
            month,
            day,
            Q,
            F,
            R,
            beginning_flex_ready,
            end_flex_ready,
            cpp,
            alfa,
            cr,
            sgn_Pr,
            cid
        )

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
    solution = _solve_cplex(f, Aeq, beq, Aineq, bineq, lb, ub,data)

    solution = solution.x

    
   
 
    