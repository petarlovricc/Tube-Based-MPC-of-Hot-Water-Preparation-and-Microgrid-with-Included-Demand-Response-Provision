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
import MILP_formulation.extrasprojekt
import MILP_formulation.MILP_peak_power as optim
from MILP_formulation.MILP_comparison import MILP_comparison
from Multithreading.worker_comparison import WorkerComparison

import pyqtgraph 

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("OPTIMIZATION GUI")

        self.threadpool = QThreadPool()

        self.paramPage = ParamPage()
        loadingPage = LoadingPage()
        self.resultPage = ResultPage(self.paramPage)

        self.layout = QStackedLayout()
        self.layout.addWidget(self.paramPage)
        self.layout.addWidget(loadingPage)
        self.layout.addWidget(self.resultPage)

        self.layout.setCurrentIndex(0)

        widget = QWidget()
        widget.setLayout(self.layout)
        self.setCentralWidget(widget)


        #Povezivanje slotova i connectiona 
        
        #Izmjena stranica
        self.paramPage.pushButton.pressed.connect(self.beginCalculation)
        self.paramPage.pushButton_2.pressed.connect(self.toResults)
        self.resultPage.retButton.pressed.connect(self.returnToParam)

        #Promjena grafa proizvodnje i potrošnje
        self.paramPage.pushButton_2.pressed.connect(self.resultPage.setGraph)
        self.paramPage.pushButton.pressed.connect(self.beginCalculation)
        


    def beginCalculation(self):
        self.layout.setCurrentIndex(1)
        args = self.paramPage.getParams()
        if(self.paramPage.radioButton.isChecked()):
            kwargs = {"scenarij1": self.paramPage.comboBox_2.currentText(),"scenarij2": self.paramPage.comboBox_3.currentText()}
            self.resultPage.legend1 = kwargs["scenarij1"]
            self.resultPage.legend2 = kwargs["scenarij2"]
            worker = WorkerComparison(self.optimization_comparison,*args,**kwargs)
            worker.signals.result.connect(self.comparisonResult)
            worker.signals.finished.connect(self.toResults)
            self.threadpool.start(worker)

            
        else:
            kwargs = {"scenarij1": self.paramPage.comboBox_2.currentText()}
            self.resultPage.legend1 = kwargs["scenarij1"]
            worker = Worker(self.optimization_function,*args,**kwargs)
            worker.signals.result.connect(self.result1)
            self.threadpool.start(worker)
            worker.signals.finished.connect(self.toResults)


    def result1(self, result1):
        args = self.paramPage.getParams()
        data = optim.getData(*args)
        model = optim.getModel(data)
        matrices = optim.get_Matrices(data,model) 
        self.resultPage.result1 = optim.result_processing(data, matrices,result1.x)

    def comparisonResult(self,result):
        self.resultPage.result1 = result[0]
        self.resultPage.result2 = result[1]

    def returnToParam(self):
        self.layout.setCurrentIndex(0)

    def toResults(self):
        self.layout.setCurrentIndex(2)
        self.resultPage.setGraph()

    def optimization_function(self,*args,**kwargs):
        print(args)
        print(kwargs)
        data = optim.getData(*args)
        model = optim.getModel(data)
        matrices = optim.get_Matrices(data, model)
        
        print("data.cpp " + str(data.cpp))
        print("POKRECEM OPTIMIZACIJU")
        result = optim.solve_cplex(data,
                          f = optim.getF(data),
                          Aeq=optim.getAeq(data,matrices,model),
                          beq = optim.getbeq(data,matrices,model),
                          Aineq = optim.getAineq(data,matrices),
                          bineq = optim.getbineq(data,matrices),
                          lb = optim.getLb(data,matrices),
                          ub = optim.getUb(data,matrices))

        return result
    
    def optimization_comparison(self,*args,**kwargs):
        print(args)
        print(self.paramPage.comboBox_2.currentIndex())
        print(self.paramPage.comboBox_3.currentIndex())
        comparer = MILP_comparison(self.paramPage.comboBox_2.currentIndex(),
                                   self.paramPage.comboBox_3.currentIndex(),
                                    *args)
        result1 = comparer.result1
        result2 = comparer.result2

        

        return (result1, result2)

os.environ['QT_QUICK_BACKEND'] = 'software'

app = QApplication(sys.argv)
window = MainWindow()
window.show()

app.exec()



