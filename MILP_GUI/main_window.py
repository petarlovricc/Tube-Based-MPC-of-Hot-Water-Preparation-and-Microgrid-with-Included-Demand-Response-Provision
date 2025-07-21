import sys
import os
from PySide6.QtCore import Qt, QRunnable, QThreadPool, QThread
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QWidget,
    QStackedLayout
)
from MILP_GUI.param_page import ParamPage
from MILP_GUI.loading_page import LoadingPage
from MILP_GUI.result_page import ResultPage 
from Multithreading.worker import Worker
from MILP_GUI.table_page import TablePage
import MILP_formulation.extrasprojekt
import MILP_formulation.MILP_peak_power as noflex_matrix
import Parameters.getData_noflex as noflex_data
import MILP_formulation.MILP_flex as flex_matrix
import Parameters.getData_flex as flex_data
import Result_Processing.result_processing_noflex as noflex_results
import Result_Processing.result_processing_flex as flex_results
import MILP_solve.milp_solve_no_flex as noflex_solve
import MILP_solve.milp_solve_flex as flex_solve
from MILP_formulation.MILP_comparison import MILP_comparison
from Multithreading.worker_comparison import WorkerComparison
from MILP_formulation.extrasprojekt import Structure
import pyqtgraph 

import numpy as np

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("OPTIMIZATION GUI")

        self.threadpool = QThreadPool()

        self.paramPage = ParamPage()
        loadingPage = LoadingPage()
        self.resultPage = ResultPage(self.paramPage)
        self.tablePage = TablePage(self.resultPage, self.paramPage) 

        self.layout = QStackedLayout()
        self.layout.addWidget(self.paramPage)
        self.layout.addWidget(loadingPage)
        self.layout.addWidget(self.resultPage)
        self.layout.addWidget(self.tablePage)

        self.layout.setCurrentIndex(0)

        widget = QWidget()
        widget.setLayout(self.layout)
        self.setCentralWidget(widget)


        self.flex = self.paramPage.comboBox_2.currentText() == "S odzivom potrošnje"
        self.solved = False
        #Povezivanje slotova i connectiona 
        
        #Izmjena stranica
        self.paramPage.pushButton.pressed.connect(self.beginCalculation)
        self.paramPage.pushButton_2.pressed.connect(self.toResults)
        self.resultPage.retButton.pressed.connect(self.returnToParam)
        self.tablePage.graphButton.pressed.connect(self.tableToGraph)
        self.resultPage.infoButton.pressed.connect(self.toTable)
        #Promjena grafa proizvodnje i potrošnje

    def tableToGraph(self):
        self.layout.setCurrentIndex(2)
        
    def update_flex(self):
        self.flex = self.paramPage.comboBox_2.currentText() == "S odzivom potrošnje"
    
    def toTable(self):
        self.layout.setCurrentIndex(3)
   

    def beginCalculation(self):
        self.layout.setCurrentIndex(1)
        self.update_flex()
        self.resultPage.clearGraph()

        self.resultPage.result1 = None
        self.resultPage.result2 = None
        self.tablePage.result1 = None
        self.tablePage.result2 = None
        self.tablePage.firstRun = True

        if(self.flex):
            args = self.paramPage.get_flexParams()
        else:
            args = self.paramPage.getParams()

        if(self.paramPage.radioButton.isChecked()):
            kwargs = {"scenarij1": self.paramPage.comboBox_2.currentText(),"scenarij2": self.paramPage.comboBox_3.currentText()}
            self.resultPage.legend1 = kwargs["scenarij1"]
            self.resultPage.legend2 = kwargs["scenarij2"]
            print("Napravio sam Comparison Workera!")
            worker = WorkerComparison(self.optimization_comparison, *args,**kwargs)
            self.threadpool.start(worker)
            worker.signals.result.connect(self.comparisonResult)
            worker.signals.finished.connect(self.toResults)

            
        else:
            kwargs = {"scenarij1": self.paramPage.comboBox_2.currentText()}
            self.resultPage.legend1 = kwargs["scenarij1"]
            worker = Worker(self.optimization_function,*args,**kwargs)
            self.threadpool.start(worker)
            worker.signals.result.connect(self.show_result)
            worker.signals.finished.connect(self.toResults)


    def show_result(self, result1):
        self.update_flex()
        if(not self.flex):
            args = self.paramPage.getParams()
            data = noflex_data.getData(*args)
            model = noflex_matrix.getModel(data)
            matrices = noflex_matrix.get_Matrices(data,model) 
            self.resultPage.result1 = noflex_results.result_processing(data, matrices,result1.x)
        elif(self.flex):
            args = self.paramPage.get_flexParams()
            data = flex_data.getData(*args)
            model = flex_matrix.getModel(data)
            matrices = flex_matrix.get_Matrices_nom(data,model) 
            matrices_alt = flex_matrix.getMatrices_alt(data, model)
           
            rezultat = flex_results.result_processing(data, model, matrices, matrices_alt, result1.x)
            self.resultPage.result1 = flex_results.result_processing(data, model, matrices, matrices_alt, result1.x)

        if self.flex:
            self.resultPage.getParamsFlex()
        elif not self.flex:
            self.resultPage.getParamsNoFlex()

        self.resultPage.update_alt_combo()
        self.solved = True
        print("SOLVED " + str(self.solved))



    def comparisonResult(self,result):
        self.update_flex()
        self.resultPage.result1 = result[0]
        self.resultPage.result2 = result[1]

        if self.flex:
            self.resultPage.getParamsFlex()
        elif not self.flex:
            self.resultPage.getParamsNoFlex()

        self.resultPage.update_alt_combo()
        self.solved = True
        print("SOLVED " + str(self.solved))
       

    def returnToParam(self):
        self.layout.setCurrentIndex(0)


    def toResults(self):
        self.update_flex()
        self.resultPage.setGraph()   
        self.layout.setCurrentIndex(2)

    def optimization_function(self, *args, **kwargs):
       

        if(not self.flex):
            data = noflex_data.getData(*args)
            model = noflex_matrix.getModel(data)
            matrices = noflex_matrix.get_Matrices(data, model)
            

            print("POKRECEM OPTIMIZACIJU")
            result = noflex_solve.solve_cplex(data,
                            f = noflex_matrix.getF(data),
                            Aeq = noflex_matrix.getAeq(data,matrices,model),
                            beq = noflex_matrix.getbeq(data,matrices,model),
                            Aineq = noflex_matrix.getAineq(data,matrices),
                            bineq = noflex_matrix.getbineq(data,matrices),
                            lb = noflex_matrix.getLb(data,matrices),
                            ub = noflex_matrix.getUb(data,matrices),
                            heater = self.paramPage.heater)
        

        elif(self.flex):
            data = flex_data.getData(*args)
            model = flex_matrix.getModel(data)
            matrices = flex_matrix.get_Matrices_nom(data, model)
            matrices_alt = flex_matrix.getMatrices_alt(data, model)
            

            print("POKRECEM OPTIMIZACIJU")
            result = flex_solve._solve_cplex(
                            f = flex_matrix.getF(data),
                            Aeq= flex_matrix.getAeq(data,model,matrices, matrices_alt),
                            beq = flex_matrix.getbeq(data,matrices),
                            Aineq = flex_matrix.getAineq(data,matrices, model, matrices_alt),
                            bineq = flex_matrix.getbineq(data,matrices, matrices_alt, model),
                            lb = flex_matrix.getLb(data,matrices, matrices_alt),
                            ub = flex_matrix.getUb(data,matrices, matrices_alt),
                            data = data,
                            heater = self.paramPage.heater)

             

        return result
    
    def optimization_comparison(self,*args,**kwargs):
        self.update_flex()
        comparer = MILP_comparison(self.flex, self.paramPage.comboBox_2.currentIndex(),
                                   self.paramPage.comboBox_3.currentIndex(), self.paramPage.heater,
                                    *args)
        result1 = comparer.result1 
        result2 = comparer.result2

        

        return (result1, result2)


app = QApplication(sys.argv)    
window = MainWindow()
window.show()

app.exec()



