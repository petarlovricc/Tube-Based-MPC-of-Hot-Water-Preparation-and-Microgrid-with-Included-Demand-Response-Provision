import sys
from PySide6.QtCore import  QThreadPool
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QStackedLayout
)
from PySide6.QtGui import QFont
from PySide6.QtCore import QTimer
import numpy as np
from MILP_GUI.utils import InfeasibleException

from MILP_GUI.param_page import ParamPage
from MILP_GUI.error_page import ErrorPage
from MILP_GUI.loading_page import LoadingPage
from MILP_GUI.result_page import ResultPage 
from Multithreading.worker import Worker
from MILP_GUI.table_page import TablePage
import MILP_formulation.MILP_peak_power as noflex_matrix
import MILP_formulation.MILP_flex as flex_matrix
import Parameters.getData_flex as DataGetter
import Result_Processing.result_processing_noflex as noflex_results
import Result_Processing.result_processing_flex as flex_results
import MILP_solve.milp_solve_no_flex as noflex_solve
import MILP_solve.milp_solve_flex as flex_solve
from MILP_formulation.MILP_comparison import MILP_comparison
from Multithreading.worker_comparison import WorkerComparison
from MILP_GUI.utils import check_cplex_full_version
from MILP_GUI.utils import invert_svg
import subprocess
import os

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(invert_svg(":/icons/smart_HOUSE", size=256))
        self.setWindowTitle("Optimal Water Heater, Battery, and PV Operation Scheduler")
        self.threadpool = QThreadPool()
        self.paramPage = ParamPage()
        self.loadingPage = LoadingPage(self.paramPage)
        self.resultPage = ResultPage(self.paramPage)
        self.tablePage = TablePage(self.resultPage, self.paramPage) 
        self.errorPage = ErrorPage() 
        self.layout = QStackedLayout()
        self.layout.addWidget(self.paramPage)
        self.layout.addWidget(self.loadingPage)
        self.layout.addWidget(self.resultPage)
        self.layout.addWidget(self.tablePage)
        self.layout.addWidget(self.errorPage)
        self.layout.setCurrentIndex(0)
        self.widget = QWidget()
        self.widget.setObjectName("MainWidget")
        self.widget.setStyleSheet("""
            QWidget#MainWidget {
                background: qlineargradient(
                    spread: pad,
                    x1: 0, y1: 0,
                    x2: 1, y2: 0,
                    stop: 0 #0C0C31,
                    stop: 0.5 #06032E,
                    stop: 1 #0C0C31
                );
            }
        """)
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)
        self.flex = self.paramPage.comboBox_2.currentText() == "With DR"
        self.solved = False
        self.time_to_solve = None
        #Povezivanje slotova i connectiona 
        self.paramPage.pushButton.pressed.connect(self.beginCalculation)
        self.paramPage.pushButton_2.pressed.connect(self.toResults)
        self.resultPage.retButton.pressed.connect(self.returnToParam)
        self.tablePage.graphButton.pressed.connect(self.tableToGraph)
        self.tablePage.graphButton_2.pressed.connect(self.tableToGraph)
        self.resultPage.infoButton.pressed.connect(self.toTable)
        self.errorPage.pushButton.pressed.connect(self.returnToParam)
    

    def tableToGraph(self):
        if self.solved == False:
            self.resultPage.comboBox.setCurrentIndex(11)
        else:
            self.resultPage.comboBox.setCurrentIndex(10)
        self.layout.setCurrentIndex(2)
        

    def update_flex(self):
        self.flex = self.paramPage.comboBox_2.currentText() == "With DR"
    

    def toTable(self):
        self.layout.setCurrentIndex(3)
   
    def show_error(self, err):
        # err je tuple (exctype, value, traceback) jer tako emitiraš
        exctype, value, tb_str = err
        self.errorPage.label.setText(f"{exctype.__name__}: {value}")
        print(tb_str)  # ili log u file
        self.layout.setCurrentIndex(4)

    def beginCalculation(self):
            self.loadingPage.label.clear()
            self.layout.setCurrentIndex(1)
            self.update_flex()
            self.resultPage.result1 = None
            self.resultPage.result2 = None
            self.tablePage.result1 = None
            self.tablePage.result2 = None
            self.tablePage.firstRun = True
            try:
                args = self.paramPage.getParams()
            except Exception as e:
                # ovdje ulaze ValueError, ParameterTooSmallError, ...
                self.errorPage.label.setText(f"{type(e).__name__}:\n {e}")
                self.layout.setCurrentIndex(4)
                return
            if(self.paramPage.radioButton.isChecked()):
                kwargs = {"scenarij1": self.paramPage.comboBox_2.currentText(),"scenarij2": self.paramPage.comboBox_3.currentText()}
                self.resultPage.legend1 = kwargs["scenarij1"]
                self.resultPage.legend2 = kwargs["scenarij2"]
                print("Napravio sam Comparison Workera!")
                worker = WorkerComparison(self.optimization_comparison, *args,**kwargs)
                self.threadpool.start(worker)
                worker.signals.result.connect(self.comparisonResult)
                worker.signals.error.connect(self.show_error)
                #worker.signals.finished.connect(self.toResults)    
            else:
                kwargs = {"scenarij1": self.paramPage.comboBox_2.currentText()}
                self.resultPage.legend1 = kwargs["scenarij1"]
                worker = Worker(self.optimization_function,*args,**kwargs)
                self.threadpool.start(worker)
                worker.signals.result.connect(self.show_result)
                worker.signals.error.connect(self.show_error)
                #worker.signals.finished.connect(self.toResults)
                
        



    def show_result(self, result1):
        currtext = self.loadingPage.label.text()
        currtext = self.loadingPage.label.text()
        #if(not "\nProblem solved!" in currtext):
            #self.loadingPage.label.setText(currtext + f"\nProblem solved!\nTime to solve: {result1.time} s")
        self.update_flex()
        if(not self.flex):
            args = self.paramPage.getParams()
            data = DataGetter.getData(*args)
            model = noflex_matrix.getModel(data)
            matrices = noflex_matrix.get_Matrices(data,model) 
            self.resultPage.result1 = noflex_results.result_processing(data, matrices,result1)
        elif(self.flex):
            args = self.paramPage.getParams()
            data = DataGetter.getData(*args)
            model = flex_matrix.getModel(data)
            matrices = flex_matrix.get_Matrices_nom(data,model) 
            matrices_alt = flex_matrix.getMatrices_alt(data, model)
            self.resultPage.result1 = flex_results.result_processing(data, model, matrices, matrices_alt, result1)
        self.resultPage.getParamsRes()
        self.resultPage.update_alt_combo()
        self.solved = True
        print("SOLVED " + str(self.solved))
        self.toResults()
        

    def comparisonResult(self,result):
        self.update_flex()
        self.resultPage.result1 = result[0]
        self.resultPage.result2 = result[1]
        self.resultPage.getParamsRes()
        self.resultPage.update_alt_combo()
        self.solved = True
        print("SOLVED " + str(self.solved))
        currtext = self.loadingPage.label.text()
        if(not "\nProblem solved!" in currtext):
            self.loadingPage.label.setText(currtext + "\nProblem solved!")
        self.toResults()



    def returnToParam(self):
        self.layout.setCurrentIndex(0)


    def toResults(self):
        try:
            self.update_flex()
            self.resultPage.resultDate.setDate(self.paramPage.dateEdit.date())
            if self.solved == False:
                self.resultPage.comboBox.setCurrentIndex(11)
            else:
                self.resultPage.comboBox.setCurrentIndex(10)
                
            self.resultPage.setGraph()   
            #QTimer.singleShot(500, lambda: self.layout.setCurrentIndex(2))
            self.layout.setCurrentIndex(2)
        except Exception as e:
                # ovdje ulaze ValueError, ParameterTooSmallError, ...
                self.errorPage.label.setText(f"{type(e).__name__}:\n {e}")
                self.layout.setCurrentIndex(4)
                return
        

    

    def optimization_function(self, *args, **kwargs):
        try:
            if(not self.flex):
                data = DataGetter.getData(*args)
                model = noflex_matrix.getModel(data)
                matrices = noflex_matrix.get_Matrices(data, model)
                currtext = self.loadingPage.label.text()
                if(not "\nMathematical problem formulated." in currtext):
                    self.loadingPage.label.setText(currtext + "\nMathematical problem formulated.")
                currtext = self.loadingPage.label.text()
                if(not "\nSolving problem..." in currtext):
                    self.loadingPage.label.setText(currtext + "\nSolving problem...")
                print("POKRECEM OPTIMIZACIJU")
                
                result = noflex_solve._solve_highs(data,
                                    f = noflex_matrix.getF(data),
                                    Aeq = noflex_matrix.getAeq(data,matrices,model),
                                    beq = noflex_matrix.getbeq(data,matrices,model),
                                    Aineq = noflex_matrix.getAineq(data,matrices),
                                    bineq = noflex_matrix.getbineq(data,matrices),
                                    lb = noflex_matrix.getLb(data,matrices),
                                    ub = noflex_matrix.getUb(data,matrices),
                                    heater = self.paramPage.heater)
                
            elif(self.flex):
                data = DataGetter.getData(*args)
                model = flex_matrix.getModel(data)
                matrices = flex_matrix.get_Matrices_nom(data, model)
                matrices_alt = flex_matrix.getMatrices_alt(data, model)
                print("POKRECEM OPTIMIZACIJU")
                currtext = self.loadingPage.label.text()
                if(not "\nMathematical problem formulated." in currtext):
                    self.loadingPage.label.setText(currtext + "\nMathematical problem formulated.")
                currtext = self.loadingPage.label.text()
                if(not "\nSolving problem..." in currtext):
                    self.loadingPage.label.setText(currtext + "\nSolving problem...")
                    
                result = flex_solve._solve_highs(
                                    f = flex_matrix.getF(data),
                                    Aeq= flex_matrix.getAeq(data,model,matrices, matrices_alt),
                                    beq = flex_matrix.getbeq(data,matrices),
                                    Aineq = flex_matrix.getAineq(data,matrices, model, matrices_alt),
                                    bineq = flex_matrix.getbineq(data,matrices, matrices_alt, model),
                                    lb = flex_matrix.getLb(data,matrices, matrices_alt),
                                    ub = flex_matrix.getUb(data,matrices, matrices_alt),
                                    data = data,
                                    heater = self.paramPage.heater)
                if(result.status_string == "HighsModelStatus.kInfeasible"):
                    raise InfeasibleException("Solution infeasible!")
                
        except (MemoryError, np.core._exceptions._ArrayMemoryError):
            raise MemoryError("RAM used up!")
        
        return result
    

    def optimization_comparison(self,*args,**kwargs):
        self.update_flex()
        comparer = MILP_comparison(self.paramPage, self.loadingPage, self.flex, self.paramPage.comboBox_2.currentIndex(),
                                   self.paramPage.comboBox_3.currentIndex(), self.paramPage.heater,
                                    *args)
        result1 = comparer.result1 
        result2 = comparer.result2
        return (result1, result2)
    

class InfeasibleException(Exception):
    pass

def main():
    app = QApplication(sys.argv)  
    app.setStyle("windows11")
    app.setFont(QFont("Segoe UI"))

    window = MainWindow()
    window.show()

    app.exec()



