import numpy as np
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QLabel,
    QWidget,
    QLineEdit,
    QSlider,
    QVBoxLayout,
    QComboBox,
    QPushButton,
    QHBoxLayout,
    QGridLayout
)

import pyqtgraph as pg
from Profiles_Readers.PV_reader import PVreader
from Profiles_Readers.Disturbances_Reader import CSV_disturbances_reader
from MILP_formulation.MILP_peak_power import getData
from MILP_formulation.extrasprojekt import Structure


class ResultPage(QWidget):
    def __init__(self,paramPage):
        super().__init__()
        
        self.paramPage = paramPage

        month = self.paramPage.dateEdit.date().month()
        day = self.paramPage.dateEdit.date().day()
        PV_power = int(self.paramPage.lineEdit_12.text())
        numberofPV = self.paramPage.horizontalSlider_5.value()
        

        self.result1 = None
        self.result2 = None

        self.legend1 = None
        self.legend2 = None

        self.profiles = getData(
                        heater_power=2500,
                        bat_cap = 9400,
                        converter_power=2500,
                        tank_volume=190,
                        PV_power=PV_power,
                        numberofPV=numberofPV,
                        buyPriceHigh=0.07,
                        buyPriceLow=0.035,
                        month=month,
                        day=day,
                        cpp=3.05
                    )

        layout = QVBoxLayout()
        
        self.comboBox = QComboBox()
        self.comboBox.addItems(["Temperatura vode u spremniku tijekom dana",
                           "SOE baterije",
                           "Stanje uključenosti grijača vode",
                           "Energija punjenja baterije",
                           "Energija pražnjenja baterije",
                           "Potrošnja tople vode tijekom dana",
                           "Proizvodnja fotonaponskih panela",
                           "Neupravljiva potrošnja",
                           "Željena temperatura vode",
                           "Temperatura okoline",
                           "Energija mreže"])
        

        
        self.comboBox.currentIndexChanged.connect(self.setGraph)

        self.graphWidget = pg.PlotWidget()
        self.graphWidget.setBackground('w')


        buttonLayout = QHBoxLayout()
        self.retButton = QPushButton("Povratak na postavljanje parametara")
        self.infoButton = QPushButton("Podatci optimizacije")

        self.label1 = QLabel()
        self.label2 = QLabel()
        self.label3 = QLabel()
        self.label4 = QLabel()


        labelLayout = QGridLayout()
        
        labelLayout.addWidget(self.label1,0,0)
        labelLayout.addWidget(self.label2,0,1)
        labelLayout.addWidget(self.label3,1,0)
        labelLayout.addWidget(self.label4,1,1)


        layout.addWidget(self.comboBox)
        layout.addWidget(self.graphWidget)

        buttonLayout.addWidget(self.retButton)
        #buttonLayout.addWidget(self.infoButton)

        layout.addLayout(labelLayout)
        layout.addLayout(buttonLayout)
        self.setLayout(layout)

        #postavi graf pri prvom pokretanju
        #self.setGraph()

    def setGraph(self):

        self.getParamsAfterChange()
        
        self.label1.clear()
        self.label2.clear()
        self.label3.clear()
        self.label4.clear()

        self.graphWidget.clear()

        pen = pg.mkPen(color = "black")
        pen_graph = pg.mkPen(color = "orange", width = 2)
        pen_graph2 = pg.mkPen(color = "blue", width = 2)
        
        styles = {'color':'k', 'font-size':'12pt'}
        self.graphWidget.setLabel("bottom", "Vrijeme [h]", **styles)
        self.graphWidget.getAxis("bottom").setTextPen(pen)
        self.graphWidget.getAxis("left").setTextPen(pen)
        self.graphWidget.getAxis("bottom").setTickPen(pen)
        self.graphWidget.getAxis("left").setTickPen(pen)

        hour_labels = [(i*4, f"{i}:00") for i in range(0,25)]

        self.graphWidget.getAxis("bottom").setTicks([hour_labels])
        self.graphWidget.setXRange(0, 95)
        self.graphWidget.setTitle(bold=True)

        self.graphWidget.addLegend(labelTextColor = "black")
        if(self.paramPage.radioButton_2.isChecked()):
            if self.comboBox.currentIndex() == 0:
                self.graphWidget.setXRange(0, 96)
                self.graphWidget.setTitle("Temperatura vode u spremniku tijekom dana", size = "15pt", color = "k", bold=True)
                self.graphWidget.plot(np.arange(0,97,1), self.result1.tempC.flatten(), pen = pen_graph, stepMode="left",name = self.legend1)
                self.graphWidget.setLabel("left", "Temperatura [°C]", **styles)
                
        
            if self.comboBox.currentIndex() == 1:
                self.graphWidget.setXRange(0, 96)
                self.graphWidget.setTitle("SOE baterije", size = "15pt", color = "k", bold=True)
                self.graphWidget.plot(np.arange(0,97,1), self.result1.SOE.flatten(), pen = pen_graph, stepMode="left",name = self.legend1)
                self.graphWidget.setLabel("left", "SOE [Wh]", **styles)
                

            if self.comboBox.currentIndex() == 2:
                self.graphWidget.setTitle("Stanje uključenosti grijača vode", size = "15pt", color = "k", bold=True)
                self.graphWidget.plot(np.arange(0,96,1), self.result1.delte.flatten(), pen = pen_graph, stepMode="left",name = self.legend1)
                self.graphWidget.setLabel("left", "", **styles)
                

            if self.comboBox.currentIndex() == 3:
                self.graphWidget.setTitle("Energija punjenja baterije", size = "15pt", color = "k", bold=True)
                self.graphWidget.plot(np.arange(0,96,1), self.result1.Ech.flatten(), pen = pen_graph, stepMode="left",name = self.legend1)            
                self.graphWidget.setLabel("left", "Energija punjenja [Wh]", **styles)
            
            if self.comboBox.currentIndex() == 4:
                self.graphWidget.setTitle("Energija pražnjenja baterije", size = "15pt", color = "k", bold=True)
                self.graphWidget.plot(np.arange(0,96,1), self.result1.Edch.flatten(), pen = pen_graph, stepMode="left",name = self.legend1)
                self.graphWidget.setLabel("left", "Energija pražnjenja [Wh]", **styles)

            if self.comboBox.currentIndex() == 5:
                self.graphWidget.setTitle("Željeni protok miješane tople vode tijekom dana", size = "15pt", color = "k", bold=True)
                self.graphWidget.setLabel("left", "Maseni protok [L/h]", **styles)
                self.graphWidget.plot(np.arange(0,96,1), self.profiles.water_demand.flatten(), pen = pen_graph, stepMode="left")
                

            
            if self.comboBox.currentIndex() == 6:
                self.graphWidget.setTitle("Proizvodnja fotonaponskih panela", size = "15pt", color = "k", bold=True)
                self.graphWidget.setLabel("left", "Snaga proizvodnje [W]", **styles)
                self.graphWidget.plot(np.arange(0,96,1), self.profiles.pv_power.flatten(), pen = pen_graph, stepMode="left")
                print("Proizvodnja fotonaponskih panela "+str(self.profiles.pv_energy_sum))


            if self.comboBox.currentIndex() == 7:
                self.graphWidget.setTitle("Neupravljiva potrošnja", size = "15pt", color = "k", bold=True)
                self.graphWidget.setLabel("left", "Snaga [W]", **styles)
                self.graphWidget.plot(np.arange(0,96,1), self.profiles.nc_load_power.flatten(), pen = pen_graph, stepMode="left")
                print("Neupravljiva potrošnja "+str(self.profiles.sum_nc_load_energy))

            if self.comboBox.currentIndex() == 8:
                self.graphWidget.setTitle("Željena temperatura vode", size = "15pt", color = "k", bold=True)
                self.graphWidget.setLabel("left", "Temperatura [°C]", **styles)
                self.graphWidget.plot(np.arange(0,96,1), self.profiles.set_water_temp_C.flatten(), pen = pen_graph, stepMode="left")

            if self.comboBox.currentIndex() == 9:
                self.graphWidget.setTitle("Temperatura okoline", size = "15pt", color = "k", bold=True)
                self.graphWidget.setLabel("left", "Temperatura [°C]", **styles)
                self.graphWidget.plot(np.arange(0,96,1), self.profiles.env_temp_C, pen = pen_graph, stepMode="left")

            
            if self.comboBox.currentIndex() == 10:
                self.graphWidget.setTitle("Energija mreže", size = "15pt", color = "k", bold=True)
                self.graphWidget.setLabel("left", "Energija [Wh]", **styles)
                self.graphWidget.plot(np.arange(0,96,1), self.result1.grid_energy.flatten(), pen = pen_graph, stepMode="left",name = self.legend1)
                self.label1.setText(f"Trošak električne energije (€): {(sum(self.result1.eps)+self.result1.eps_peak*self.profiles.cpp):.3f}")
                self.label3.setText(f"Trošak električne energije, bez vršne snage (€): {sum(self.result2.eps):.3f}")


        if(self.paramPage.radioButton.isChecked()):
            if self.comboBox.currentIndex() == 0:
                self.graphWidget.setXRange(0, 96)
                self.graphWidget.setTitle("Temperatura vode u spremniku tijekom dana", size = "15pt", color = "k", bold=True)
                self.graphWidget.plot(np.arange(0,97,1), self.result1.tempC.flatten(), pen = pen_graph, stepMode="left",name = self.legend1)
                self.graphWidget.plot(np.arange(0,97,1), self.result2.tempC.flatten(), pen = pen_graph2, stepMode="left",name = self.legend2)
                self.graphWidget.setLabel("left", "Temperatura [°C]", **styles)


            if self.comboBox.currentIndex() == 1:
                self.graphWidget.setXRange(0, 96)
                self.graphWidget.setTitle("SOE baterije", size = "15pt", color = "k", bold=True)
                self.graphWidget.plot(np.arange(0,97,1), self.result1.SOE.flatten(), pen = pen_graph, stepMode="left",name = self.legend1)
                self.graphWidget.plot(np.arange(0,97,1), self.result2.SOE.flatten(), pen = pen_graph2, stepMode="left",name = self.legend2)
                self.graphWidget.setLabel("left", "SOE [Wh]", **styles)
                

            if self.comboBox.currentIndex() == 2:
                self.graphWidget.setTitle("Stanje uključenosti grijača vode", size = "15pt", color = "k", bold=True)
                self.graphWidget.plot(np.arange(0,96,1), self.result1.delte.flatten(), pen = pen_graph, stepMode="left",name = self.legend1)
                self.graphWidget.plot(np.arange(0,96,1), self.result2.delte.flatten(), pen = pen_graph2, stepMode="left",name = self.legend2)
                self.graphWidget.setLabel("left", "", **styles)
                

            if self.comboBox.currentIndex() == 3:
                self.graphWidget.setTitle("Energija punjenja baterije", size = "15pt", color = "k", bold=True)
                self.graphWidget.plot(np.arange(0,96,1), self.result1.Ech.flatten(), pen = pen_graph, stepMode="left",name = self.legend1)
                self.graphWidget.plot(np.arange(0,96,1), self.result2.Ech.flatten(), pen = pen_graph2, stepMode="left",name = self.legend2)            
                self.graphWidget.setLabel("left", "Energija punjenja [Wh]", **styles)
            
            if self.comboBox.currentIndex() == 4:
                self.graphWidget.setTitle("Energija pražnjenja baterije", size = "15pt", color = "k", bold=True)
                self.graphWidget.plot(np.arange(0,96,1), self.result1.Edch.flatten(), pen = pen_graph, stepMode="left",name = self.legend1)
                self.graphWidget.plot(np.arange(0,96,1), self.result2.Edch.flatten(), pen = pen_graph2, stepMode="left",name = self.legend2)
                self.graphWidget.setLabel("left", "Energija pražnjenja [Wh]", **styles)

            if self.comboBox.currentIndex() == 5:
                self.graphWidget.setTitle("Željeni protok miješane tople vode tijekom dana", size = "15pt", color = "k", bold=True)
                self.graphWidget.setLabel("left", "Maseni protok [L/h]", **styles)
                self.graphWidget.plot(np.arange(0,96,1), self.profiles.water_demand.flatten(), pen = pen_graph, stepMode="left")
                

            
            if self.comboBox.currentIndex() == 6:
                self.graphWidget.setTitle("Proizvodnja fotonaponskih panela", size = "15pt", color = "k", bold=True)
                self.graphWidget.setLabel("left", "Snaga proizvodnje [W]", **styles)
                self.graphWidget.plot(np.arange(0,96,1), self.profiles.pv_power.flatten(), pen = pen_graph, stepMode="left")
                print("Proizvodnja fotonaponskih panela "+str(self.profiles.pv_energy_sum))


            if self.comboBox.currentIndex() == 7:
                self.graphWidget.setTitle("Neupravljiva potrošnja", size = "15pt", color = "k", bold=True)
                self.graphWidget.setLabel("left", "Snaga [W]", **styles)
                self.graphWidget.plot(np.arange(0,96,1), self.profiles.nc_load_power.flatten(), pen = pen_graph, stepMode="left")
                print("Neupravljiva potrošnja "+str(self.profiles.sum_nc_load_energy))

            if self.comboBox.currentIndex() == 8:
                self.graphWidget.setTitle("Željena temperatura vode", size = "15pt", color = "k", bold=True)
                self.graphWidget.setLabel("left", "Temperatura [°C]", **styles)
                self.graphWidget.plot(np.arange(0,96,1), self.profiles.set_water_temp_C.flatten(), pen = pen_graph, stepMode="left")

            if self.comboBox.currentIndex() == 9:
                self.graphWidget.setTitle("Temperatura okoline", size = "15pt", color = "k", bold=True)
                self.graphWidget.setLabel("left", "Temperatura [°C]", **styles)
                self.graphWidget.plot(np.arange(0,96,1), self.profiles.env_temp_C, pen = pen_graph, stepMode="left")

            
            if self.comboBox.currentIndex() == 10:
                self.graphWidget.setTitle("Energija mreže", size = "15pt", color = "k", bold=True)
                self.graphWidget.setLabel("left", "Energija [Wh]", **styles)
                self.graphWidget.plot(np.arange(0,96,1), self.result1.grid_energy.flatten(), pen = pen_graph, stepMode="left",name = self.legend1)
                self.graphWidget.plot(np.arange(0,96,1), self.result2.grid_energy.flatten(), pen = pen_graph2, stepMode="left",name = self.legend2)
                self.label1.setText(f"Trošak električne energije (€): {(sum(self.result1.eps)+self.result1.eps_peak*self.profiles.cpp):.3f}")
                self.label3.setText(f"Trošak električne energije, bez vršne snage (€): {sum(self.result2.eps):.3f}")
                self.label2.setText(f"Korištena energija iz mreže (Wh): {sum(self.result1.grid_energy):.3f}")
                self.label4.setText(f"Korištena energija iz mreže, bez vršne snage (Wh): {sum(self.result2.grid_energy):.3f}")
                                    
    def getParamsAfterChange(self):
        month = self.paramPage.dateEdit.date().month()
        day = self.paramPage.dateEdit.date().day()
        PV_power = int(self.paramPage.lineEdit_12.text())
        numberofPV = self.paramPage.horizontalSlider_5.value()
       
        params = self.paramPage.getParams()
        
        self.profiles = getData(
                        heater_power=params[0],
                        bat_cap = params[1],
                        converter_power=params[2],
                        tank_volume=params[3],
                        PV_power=params[4],
                        numberofPV=params[5],
                        buyPriceHigh=params[6],
                        buyPriceLow=params[7],
                        month=params[8],
                        day=params[9],
                        cpp=params[10]
                    )


