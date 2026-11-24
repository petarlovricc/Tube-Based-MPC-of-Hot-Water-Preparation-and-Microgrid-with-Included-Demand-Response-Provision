import numpy as np
from scipy.sparse import csr_matrix
import matplotlib.pyplot as plt
from MILP_formulation_accelerated.extrasprojekt import *
import math
import sys
import os
import highspy
from Parameters.getData_flex import getData
import MILP_formulation_accelerated.MILP_peak_power as flex
import time
from scipy.sparse import csr_array, vstack as sp_vstack

def _solve_highs(f, Aeq, beq, Aineq, bineq, lb, ub, data, heater):

    # define problem
    highs = highspy.Highs()
    highs.changeObjectiveSense(highspy.ObjSense.kMinimize)

    types = data.n_x*"C" + data.N*f"{heater}CCC" + data.N*"C" + "C"

    integrality = np.array([0 if t == "C" else 1 for t in types], dtype=int)

    lb = lb.flatten()
    ub = ub.flatten()
    obj = f.flatten()
    n_var = f.shape[0]

    
    highs.addVars(n_var, lb, ub)
    highs.changeColsCost(f.shape[0],np.arange(f.shape[0]), obj)

    highs.changeColsIntegrality(f.shape[0],np.arange(f.shape[0]) , integrality)

    A = sp_vstack((csr_array(Aeq), csr_array(Aineq)), format='csr')
    lower = np.r_[beq.ravel(), np.full(Aineq.shape[0], -highspy.kHighsInf)]
    upper = np.r_[beq.ravel(), bineq.ravel()]
    highs.addRows(A.shape[0], lower, upper, A.nnz, A.indptr[:-1], A.indices, A.data)
    
    
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


   
 
    
    