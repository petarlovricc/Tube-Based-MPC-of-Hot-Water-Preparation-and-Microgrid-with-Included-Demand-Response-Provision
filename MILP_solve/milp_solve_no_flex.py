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
from Parameters.getData_noflex import getData
import MILP_formulation.MILP_peak_power as noflex
from Result_Processing.result_processing_noflex import result_processing
import pyqtgraph as pg

from PySide6 import QtWidgets

def solve_cplex(data, f, Aeq, beq, Aineq, bineq, lb, ub, heater):
    c = cplex.Cplex()
    if(heater == "I"):
        c.parameters.mip.tolerances.mipgap.set(0.07)
    elif(heater == "C"):
        c.parameters.mip.tolerances.mipgap.set(0.001)
        
    c.objective.set_sense(c.objective.sense.minimize)

    #print(c.parameters._get_info())
    types = data.n_x * "C" + data.N * f"{heater}CC" + data.len_eps_da * "C" + data.len_epp_noflex * "C"


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


# if __name__ == "__main__": 
#     data = getData(
#         heater_power=2500,
#         bat_cap = 9400,
#         converter_power=2500,
#         tank_volume=190,
#         PV_power=410,
#         numberofPV=20,
#         buyPriceHigh=0.07,
#         buyPriceLow=0.035,
#         month=7,
#         day=4,
#         cpp=3.05
#     )
#     model = noflex.getModel(data)
#     matrices = noflex.get_Matrices(data, model)

#     lb = noflex.getLb(data,matrices)
#     ub = noflex.getUb(data,matrices)
#     Aineq = noflex.getAineq(data, matrices)
#     bineq = noflex.getbineq(data,matrices)
#     Aeq = noflex.getAeq(data,matrices,model)
#     beq = noflex.getbeq(data,matrices,model)
#     f = noflex.getF(data)

#     solution = solve_cplex(data,f,Aeq,beq,Aineq,bineq,lb,ub)
#     r = result_processing(data,matrices,solution.x)


#     data = getData(
#         heater_power=2500,
#         bat_cap = 9400,
#         converter_power=2500,
#         tank_volume=190,
#         PV_power=410,
#         numberofPV=20,
#         buyPriceHigh=0.07,
#         buyPriceLow=0.035,
#         month=7,
#         day=4,
#         cpp=0
#     )
#     model = noflex.getModel(data)
#     matrices = noflex.get_Matrices(data, model)

#     lb = noflex.getLb(data,matrices)
#     ub = noflex.getUb(data,matrices)
#     Aineq = noflex.getAineq(data, matrices)
#     bineq = noflex.getbineq(data,matrices)
#     Aeq = noflex.getAeq(data,matrices,model)
#     beq = noflex.getbeq(data,matrices,model)
#     f = noflex.getF(data)

#     solution2 = solve_cplex(data,f,Aeq,beq,Aineq,bineq,lb,ub)
#     r2 = result_processing(data,matrices,solution2.x)



#     class MainWindow(QtWidgets.QMainWindow):
#         def __init__(self):
#             super().__init__()
#             self.graphWidget = pg.PlotWidget()
#             self.graphWidget.plot(np.arange(1, 97),r.delte, stepmode = "left")
#             self.graphWidget.setBackground("w")
#             pen = pg.mkPen(color=(255, 0, 0))
#             self.graphWidget.plot(np.arange(1, 97),r.delte, stepmode = "left")
#             app = QtWidgets.QApplication(sys.argv)
#             main = MainWindow()
#             main.show()
#             app.exec()
            
#     plt.step(np.arange(1, 97),r.delte)
#     plt.show()
#     plt.step(np.arange(1, 97),r.Ech)
#     plt.show()
#     plt.step(np.arange(1, 97),r.grid_energy)
#     plt.step(np.arange(1, 97),r2.grid_energy)
#     plt.show()


#     plt.step(np.arange(1, 97),r.temp[1:]-273.15)
#     plt.step(np.arange(1, 97),data.Tmin_interval_before-273.15)
#     plt.show()


# PySide6 GUI klasa
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, r):
        super().__init__()
        self.setWindowTitle("PyQtGraph - Delte")
        self.graphWidget = pg.PlotWidget()
        self.setCentralWidget(self.graphWidget)
        self.graphWidget.setBackground("w")
        pen = pg.mkPen(color=(255, 0, 0), width=2)
        self.graphWidget.plot(np.arange(0, 97), r.delte, stepMode=True, pen=pen)

if __name__ == "__main__":
    # --- Prvo rješenje (s cpp) ---
    data = getData(
        heater_power=2500,
        bat_cap=9400,
        converter_power=2500,
        tank_volume=190,
        PV_power=410,
        numberofPV=20,
        buyPriceHigh=0.18,
        buyPriceLow=0.09,
        month=7,
        day=4,
        cpp=3.64,
    )
    heater = "C"
    model = noflex.getModel(data)
    matrices = noflex.get_Matrices(data, model)
    lb = noflex.getLb(data, matrices)
    ub = noflex.getUb(data, matrices)
    Aineq = noflex.getAineq(data, matrices)
    bineq = noflex.getbineq(data, matrices)
    Aeq = noflex.getAeq(data, matrices, model)
    beq = noflex.getbeq(data, matrices, model)
    f = noflex.getF(data)
    solution = solve_cplex(data, f, Aeq, beq, Aineq, bineq, lb, ub, heater)
    res = result_processing(data, matrices, solution.x)

   