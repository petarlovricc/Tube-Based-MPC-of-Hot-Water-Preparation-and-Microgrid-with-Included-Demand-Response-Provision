import numpy as np
import os
import sys
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
import re
import pandas as pd
import pyqtgraph as pg
from Profiles_Readers.PV_reader import PVreader
from Profiles_Readers.Disturbances_Reader import CSV_disturbances_reader
from Parameters.getData_noflex import getData as data_noflex
from Parameters.getData_flex import getData as data_flex
from MILP_formulation.extrasprojekt import Structure

import matplotlib
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure

from matplotlib.backends.backend_qtagg import (
NavigationToolbar2QT as NavigationToolbar,
)
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QSizePolicy



matplotlib.use("QtAgg")

class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=3.47, height=2.5, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        super().__init__(self.fig)


class ResultPage(QWidget):
    def __init__(self,paramPage):
        super().__init__()
        
        self.paramPage = paramPage

        self.data = Structure()
        self.data_flex = Structure()

        self.getParamsNoFlex()
        self.getParamsFlex()
        

        self.result1 = None
        self.result2 = None

        self.legend1 = None
        self.legend2 = None

        self.alt_combo = QComboBox()

        self.reslayout = QVBoxLayout()



        
        self.hlayout = QHBoxLayout()

        self.comboBox = QComboBox()


        self.comboBox.addItems(["Temperatura vode u spremniku",
                           "SOE baterije",
                           "Stanje uključenosti grijača vode",
                           "Energija punjenja baterije",
                           "Energija pražnjenja baterije",
                           "Potrošnja tople vode",
                           "Proizvodnja fotonaponskih panela",
                           "Neupravljiva potrošnja",
                           "Željena temperatura vode",
                           "Temperatura okoline",
                           "Energija mreže"])
        


        
        

        self.hlayout.addWidget(self.comboBox)
        self.hlayout.addWidget(self.alt_combo)


        self.canvas = MplCanvas(self, width=3.47, height=2.5, dpi=100)         #self.canvas.axes.xticks(pd.date_range(start="2023-01-01", end="2023-12-31", freq="M"))

        toolbar = NavigationToolbar(self.canvas, self)
       
        self.buttonLayout = QHBoxLayout()
        self.retButton = QPushButton("Povratak na postavljanje parametara")
        self.infoButton = QPushButton("Podatci optimizacije")

        self.label1 = QLabel()
        self.label2 = QLabel()
        self.label3 = QLabel()
        self.label4 = QLabel()


        self.labelLayout = QGridLayout()



        self.buttonLayout.addWidget(self.retButton)

        self.labelLayout.addWidget(self.label1,0,0)
        self.labelLayout.addWidget(self.label2,0,1)
        self.labelLayout.addWidget(self.label3,1,0)
        self.labelLayout.addWidget(self.label4,1,1)

        self.buttonLayout.addWidget(self.infoButton)

        self.toolbarlayout = QHBoxLayout()
        self.toolbarlayout.addWidget(toolbar)
        self.label_graph = QLabel()
        font = QFont("Segoe UI", 15, QFont.Bold)  
        self.label_graph.setFont(font)

        self.label_graph.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.toolbarlayout.addWidget(self.label_graph)
        self.toolbarlayout.addStretch() 
        self.canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)


        self.reslayout.addLayout(self.hlayout, stretch=0)
        self.reslayout.addLayout(self.toolbarlayout, stretch=0)
        self.reslayout.addWidget(self.canvas, stretch=3)
        self.reslayout.addLayout(self.labelLayout, stretch=0)
        self.reslayout.addLayout(self.buttonLayout, stretch=0)
        self.setLayout(self.reslayout)

        
        

       
        #signali i slotovi
        self.comboBox.currentIndexChanged.connect(self.setGraph)
        self.alt_combo.currentIndexChanged.connect(self.setGraph)

       
        self.update_alt_combo()

    def clearGraph(self):
         self.canvas.axes.cla()

    def update_alt_combo(self):
        flex = self.paramPage.comboBox_2.currentIndex() == 0 
        self.alt_combo.blockSignals(True)
        if flex == True:
            self.alt_combo.setEnabled(True)
            self.alt_combo.clear()
            for i in range(self.data_flex.n_a):
                if(self.result1 and self.result1.worst_ind == i):
                    self.alt_combo.addItem(f"Alternativni profil {i+1} (WORST)")
                else:
                     self.alt_combo.addItem(f"Alternativni profil {i+1}")
        else:   
            self.alt_combo.setEnabled(False)

            self.alt_combo.clear()
        self.alt_combo.blockSignals(False)

        
        



    def getYlabel(self, index):
        if index in [0, 8, 9]:
            label = "Temperatura [°C]"
        elif index in [1,3,4]:
            label = "Energija [Wh]"
        elif index in [5]:
            label = "Volumen [L]"
        elif index in [6, 7, 10]:
             label = "Snaga [W]"
        else:
            label = ""

        return label



    def setGraph(self):
        # Očisti prethodni graf i labele
        self.canvas.axes.cla()
        for lbl in (self.label1, self.label2, self.label3, self.label4):
            lbl.clear()

        # Crtanje na temelju odabira korisnika
        if self.paramPage.radioButton_2.isChecked():
            if self.result1 and self.result1.case == "flex":
                self.label1.setText(f"Iznos rezervirane snage (W): {self.result1.Pr:.0f}")
                self.label3.setText(f"Promjena potrošnje (Wh): {self.result1.Pr * self.data_flex.ts:.1f}")
                self.plot_alternative_profiles()
            elif self.result1 and self.result1.case == "noflex":
                self.plot_noflex()

        elif self.paramPage.radioButton.isChecked():
            if self.result2 and self.result1.case == "flex":
                self.plot_comparison_alt_nom()
            elif self.result2 and self.result1.case == "noflex":
                self.plot_comparison_noflex()

        # Profil potrošnje i proizvodnje
        self.plot_profiles_demand_production()

        # Postavke osi
        ax = self.canvas.axes
        ax.set_xlabel("Vrijeme [h]", fontsize=10, fontfamily="serif")
        ax.set_ylabel(self.getYlabel(self.comboBox.currentIndex()), fontsize=10, fontfamily="serif")

        # Vrijeme na X osi
        timestamps = pd.date_range(start="00:00:00", periods=97, freq="15min")
        labels = [ts.strftime("%H:%M") for ts in timestamps]
        tick_positions = list(range(0, 97, 4))  # svaka 1h
        tick_labels = [labels[i] for i in tick_positions]

        ax.set_xticks(tick_positions)
        ax.set_xticklabels(tick_labels, rotation=45, ha="right", fontsize=9, fontfamily="serif")

        # Opcionalno: male oznake svakih 15 min
        ax.set_xticks(range(97), minor=True)
        ax.tick_params(axis="x", which="minor", length=2)

        # Mreža i legenda
        ax.grid(True, linestyle="--", linewidth=0.4, alpha=0.6)
        ax.set_axisbelow(True)
        ax.legend(frameon=False, fontsize=9)

        # Estetsko podešavanje
        for label in (ax.get_yticklabels() + ax.get_xticklabels()):
            label.set_fontsize(9)
            label.set_fontfamily("serif")

        self.canvas.fig.subplots_adjust(
            left=0.08,    # lijeva margina
            right=0.98,   # desna margina
            bottom=0.15,  # donja margina (za vrijeme)
            top=0.95,     # gornja margina
        )   
        #self.canvas.fig.tight_layout()
        self.canvas.draw()
        self.save_ieee_pdf()



    def resource_path(relative_path):
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, relative_path)
        return os.path.join(os.path.abspath("."), relative_path)

    def save_ieee_pdf(self):
        old_size = self.canvas.fig.get_size_inches()
        self.canvas.fig.set_size_inches(7.16, 3.5)
        filename = re.sub(r' ', '_', self.comboBox.currentText())
        output_dir = os.path.join(os.path.dirname(sys.executable if getattr(sys, 'frozen', False) else __file__), "grafovi")
        os.makedirs(output_dir, exist_ok=True)
        path = os.path.join(output_dir, f"{filename}.pdf")
        self.canvas.fig.savefig(path, dpi=600, bbox_inches='tight')
        print(f"Spremljeno kao {path}")
        self.canvas.fig.set_size_inches(old_size)
        self.canvas.draw()
            

    def plot_comparison_noflex(self):
        if self.comboBox.currentIndex() == 0:
                    self.label_graph.setText(self.comboBox.itemText(0))
                    self.plot_noflex_states(self.data, self.result1, "heater")
                    self.plot_noflex_states(self.data, self.result2, "heater")

        if self.comboBox.currentIndex() == 1:
                    self.label_graph.setText(self.comboBox.itemText(1))
                    self.plot_noflex_states(self.data, self.result1, "batt")
                    self.plot_noflex_states(self.data, self.result2, "batt")

        if self.comboBox.currentIndex() == 2:
                    self.label_graph.setText(self.comboBox.itemText(2))
                    self.plot_input_output_noflex(self.data, self.result1, "delte")
                    self.plot_input_output_noflex(self.data, self.result2, "delte")
                
        if self.comboBox.currentIndex() == 3:
                    self.label_graph.setText(self.comboBox.itemText(3))
                    self.plot_input_output_noflex(self.data, self.result1, "Ech")
                    self.plot_input_output_noflex(self.data, self.result2, "Ech")

        if self.comboBox.currentIndex() == 4:
                    self.label_graph.setText(self.comboBox.itemText(4))
                    self.plot_input_output_noflex(self.data, self.result1, "Edch")
                    self.plot_input_output_noflex(self.data, self.result2, "Edch")

        if self.comboBox.currentIndex() == 10:
                    self.label_graph.setText(self.comboBox.itemText(10))
                    self.plot_input_output_noflex(self.data, self.result1, "grid")                
                    self.plot_input_output_noflex(self.data, self.result2, "grid")

         
            
    def plot_comparison_alt_nom(self):
        if self.comboBox.currentIndex() == 0:
                    self.label_graph.setText(self.comboBox.itemText(0))
                    self.plot_state_matplotlib(self.data_flex, self.result1, self.alt_combo.currentIndex(), "heater")
                    self.plot_noflex_states(self.data, self.result2, "heater")

        if self.comboBox.currentIndex() == 1:
                    self.label_graph.setText(self.comboBox.itemText(1))
                    self.plot_state_matplotlib(self.data_flex, self.result1, self.alt_combo.currentIndex(), "batt")
                    self.plot_noflex_states(self.data, self.result2, "batt")

        if self.comboBox.currentIndex() == 2:
                    self.label_graph.setText(self.comboBox.itemText(2))
                    self.plot_input_output_matplotlib(self.data_flex, self.result1, self.alt_combo.currentIndex(), "delte" )
                    self.plot_input_output_noflex(self.data, self.result2, "delte")
                
        if self.comboBox.currentIndex() == 3:
                    self.label_graph.setText(self.comboBox.itemText(3))
                    self.plot_input_output_matplotlib(self.data_flex, self.result1, self.alt_combo.currentIndex(), "Ech" )
                    self.plot_input_output_noflex(self.data, self.result2, "Ech")

        if self.comboBox.currentIndex() == 4:
                    self.label_graph.setText(self.comboBox.itemText(4))
                    self.plot_input_output_matplotlib(self.data_flex, self.result1, self.alt_combo.currentIndex(), "Edch" )
                    self.plot_input_output_noflex(self.data, self.result2, "Edch")

        if self.comboBox.currentIndex() == 10:
                    self.label_graph.setText(self.comboBox.itemText(10))
                    self.plot_input_output_matplotlib(self.data_flex, self.result1, self.alt_combo.currentIndex(), "grid" )                
                    self.plot_input_output_noflex(self.data, self.result2, "grid")



    def plot_profiles_demand_production(self):
                self.getParamsNoFlex()

                if self.comboBox.currentIndex() == 5:
                    self.label_graph.setText(self.comboBox.itemText(5))
                    self.plot_profiles(self.data, "flow")
                
                if self.comboBox.currentIndex() == 6:
                    self.label_graph.setText(self.comboBox.itemText(6))
                    self.plot_profiles(self.data, "pv")

                if self.comboBox.currentIndex() == 7:
                    self.label_graph.setText(self.comboBox.itemText(7))
                    self.plot_profiles(self.data, "nc_load")

                if self.comboBox.currentIndex() == 8:
                    self.label_graph.setText(self.comboBox.itemText(8))
                    self.plot_profiles(self.data, "setTemp")

                if self.comboBox.currentIndex() == 9:
                    self.label_graph.setText(self.comboBox.itemText(8))
                    self.plot_profiles(self.data, "envtemp")


                
                    
    def plot_noflex(self):
                if self.comboBox.currentIndex() == 0:
                    self.label_graph.setText(self.comboBox.itemText(0))
                    self.plot_noflex_states(self.data, self.result1, "heater")

                if self.comboBox.currentIndex() == 1:
                    self.label_graph.setText(self.comboBox.itemText(1))
                    self.plot_noflex_states(self.data, self.result1, "batt")

                if self.comboBox.currentIndex() == 2:
                    self.label_graph.setText(self.comboBox.itemText(2))
                    self.plot_input_output_noflex(self.data, self.result1, "delte")
                
                if self.comboBox.currentIndex() == 3:
                    self.label_graph.setText(self.comboBox.itemText(3))
                    self.plot_input_output_noflex(self.data, self.result1, "Ech")

                if self.comboBox.currentIndex() == 4:
                    self.label_graph.setText(self.comboBox.itemText(4))
                    self.plot_input_output_noflex(self.data, self.result1, "Edch")


                if self.comboBox.currentIndex() == 10:
                    self.label_graph.setText(self.comboBox.itemText(10))
                    self.plot_input_output_noflex(self.data, self.result1, "grid")
                

           


    def plot_alternative_profiles(self):
                if self.comboBox.currentIndex() == 0:
                    self.label_graph.setText(self.comboBox.itemText(0))
                    print("alternativni indeks" + str(self.alt_combo.currentIndex()))
                    self.plot_state_matplotlib(self.data_flex, self.result1, self.alt_combo.currentIndex(), "heater")

                if self.comboBox.currentIndex() == 1:
                    self.label_graph.setText(self.comboBox.itemText(1))
                    self.plot_state_matplotlib(self.data_flex, self.result1, self.alt_combo.currentIndex(), "batt")

                if self.comboBox.currentIndex() == 2:
                    self.label_graph.setText(self.comboBox.itemText(2))
                    self.plot_input_output_matplotlib(self.data_flex, self.result1, self.alt_combo.currentIndex(), "delte" )
                
                if self.comboBox.currentIndex() == 3:
                    self.label_graph.setText(self.comboBox.itemText(3))
                    self.plot_input_output_matplotlib(self.data_flex, self.result1, self.alt_combo.currentIndex(), "Ech" )

                if self.comboBox.currentIndex() == 4:
                    self.label_graph.setText(self.comboBox.itemText(4))
                    self.plot_input_output_matplotlib(self.data_flex, self.result1, self.alt_combo.currentIndex(), "Edch" )

                if self.comboBox.currentIndex() == 10:
                    self.label_graph.setText(self.comboBox.itemText(10))
                    self.plot_input_output_matplotlib(self.data_flex, self.result1, self.alt_combo.currentIndex(), "grid" )                

                

    def getParamsNoFlex(self):
        params = self.paramPage.getParams()               
        self.data = data_noflex(
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
        

    def getParamsFlex(self):
        params = self.paramPage.get_flexParams()                
        self.data_flex = data_flex(
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
                        cpp=params[10],
                        Q = params[11],
                        F = params[12],
                        R = params[13],
                        beginning_flex_ready = params[14],
                        end_flex_ready = params[15],
                        alfa = params[16],
                        cr = params[17],
                        sgn_Pr = params[18],
                        cid = params[19]
                    )
        
    def plot_state_matplotlib(self, data, res, scen, var):
        labelSet = False
        if var == "heater":
            alt = res.tempC_alt
            nom = res.tempC_nom
            self.canvas.axes.set_ylim(0, 110)

        elif var == "batt":
            alt = res.SOE_alt.ravel()
            nom = res.SOE_nom
            self.canvas.axes.set_ylim(0, 10000)

        alt_indices = res.K_i_x[scen]
        act_indices = np.zeros((data.n_z, data.N_F + data.N_R + 1))
        for z in range(data.n_z):
            act_indices[z] = alt_indices[z * (data.N_F + data.N_R + 1):(z + 1) * (data.N_F + data.N_R + 1)]

        alt_values = alt[scen * data.n_z * (data.N_F + data.N_R + 1):(scen + 1) * data.n_z * (data.N_F + data.N_R + 1)]
        act_values = np.zeros((data.n_z, data.N_F + data.N_R + 1))
        print(alt_values)
        for z in range(data.n_z):
            act_values[z] = alt_values[z * (data.N_F + data.N_R + 1):(z + 1) * (data.N_F + data.N_R + 1)]

        # Nominirano stanje
        self.canvas.axes.plot(np.arange(data.N + 1), nom , linestyle='--', color = "blue", label = "Nominalni profil")

        for z in range(data.n_z):
            act_ind = act_indices[z]
            act_val = act_values[z]

            if 0 in act_ind:
                index = np.where(act_ind == 0)[0][0]
                self.canvas.axes.plot(np.append(act_ind[:index], data.N), act_val[:index + 1], linestyle='--', color = "orange")
                if not labelSet:
                    self.canvas.axes.plot(act_ind[index:], act_val[index:], linestyle='--', color = "orange",  label = self.alt_combo.currentText())
                    labelSet = True
                else:
                     self.canvas.axes.plot(act_ind[index:], act_val[index:], linestyle='--', color = "orange")
                     
            else:
                if not labelSet:
                    self.canvas.axes.plot(act_ind, act_val, linestyle='--', color = "orange",  label = self.alt_combo.currentText())
                    labelSet = True
                else:
                     self.canvas.axes.plot(act_ind, act_val, linestyle='--', color = "orange")

        

        
    def plot_input_output_matplotlib(self, data, res, scen, var):
        labelSet = False
        if var == "Ech":
            alt = res.Ech_alt
            nom = res.Ech_nom
            self.canvas.axes.set_ylim(0, 825)
        elif var == "Edch":
            alt = res.Edch_alt
            nom = res.Edch_nom
            self.canvas.axes.set_ylim(0, 825)
        elif var == "delte":
            self.canvas.axes.set_ylim(0, 1.4)
            alt = res.delte_alt
            nom = res.delte
        elif var == "grid":
            alt = res.grid_power_alt.ravel()
            nom = res.grid_power_nom

        alt_indices = res.K_i[scen]
        act_indices = np.zeros((data.n_z, data.N_F + data.N_R))
        for z in range(data.n_z):
            act_indices[z] = alt_indices[z * (data.N_F + data.N_R):(z + 1) * (data.N_F + data.N_R)]

        alt_values = alt[scen * data.n_z * (data.N_F + data.N_R):(scen + 1) * data.n_z * (data.N_F + data.N_R)]
        act_values = np.zeros((data.n_z, data.N_F + data.N_R))
        for z in range(data.n_z):
            act_values[z] = alt_values[z * (data.N_F + data.N_R):(z + 1) * (data.N_F + data.N_R)]

        # Nominalna vrijednost (dashed)
        self.canvas.axes.step(np.arange(data.N+1), np.append(nom,nom[-1]), linestyle='--', color = "blue", where="post", label = "Nominalni profil")

        for z in range(data.n_z):
            act_ind = act_indices[z]
            act_ind = np.append(act_ind, (act_ind[-1]+1)%data.N)
            act_val = act_values[z]
            act_val = np.append(act_val, act_val[-1])

            print(self.alt_combo.currentText())
          
            if 0 in act_ind and act_ind[0] != 0:
                index = np.where(act_ind == 0)[0][0]
                changed_ind = np.concatenate((act_ind[:index], [act_ind[index-1]+1], act_ind[index:]))
                changed_val = np.concatenate((act_val[:index], [act_val[index-1]], act_val[index:]))
                
                self.canvas.axes.step(changed_ind[:index+1], changed_val[:index+1], linestyle='--', color='orange', where="post")
                if not labelSet:
                    self.canvas.axes.step(changed_ind[index+1:], changed_val[index+1:], linestyle='--', color='orange', where="post",  label = self.alt_combo.currentText())
                    labelSet = True
                else:
                     self.canvas.axes.step(changed_ind[index+1:], changed_val[index+1:], linestyle='--', color='orange', where="post")
                     
                

            else:
                print(labelSet)
                if not labelSet:
                    self.canvas.axes.step(act_ind, act_val, linestyle='--', color='orange', where="post",  label = self.alt_combo.currentText())
                    labelSet = True
                else:
                     self.canvas.axes.step(act_ind, act_val, linestyle='--', color='orange', where="post")
            if int(act_ind[0]) > 0 and nom[int(act_ind[0]) - 1] != act_val[0]:
                self.canvas.axes.step([act_ind[0], act_ind[0]], [act_val[0], nom[int(act_ind[0])]], color='orange', linestyle=':', where="post")

            if int(act_ind[-1]) + 1 < len(nom) and nom[int(act_ind[-1]) + 1] != act_val[-1]:
                self.canvas.axes.step([act_ind[-1], act_ind[-1]], [act_val[-1], nom[int(act_ind[-1])]], color='orange', linestyle=':', where="post"
                                )

       
       

    def plot_noflex_states(self, data, res, var):

        if var == "heater":
            graph = res.tempC
            self.canvas.axes.set_ylim(0, 110)
        elif var == "batt":
            graph = res.SOE
            self.canvas.axes.set_ylim(0, 10000)

        if(res.case == "noflexcpp"):
            self.canvas.axes.plot(np.arange(data.N + 1), graph , linestyle='--', color = "purple", label = "Bez pružanja fleksibilnosti, cpp = 0")
        elif (res.case == "hist"):
            self.canvas.axes.plot(np.arange(data.N + 1), graph , linestyle='--', color = "brown", label = "Jednostavno upravljanje")
        else:
            self.canvas.axes.plot(np.arange(data.N + 1), graph , linestyle='--', color = "green", label = "Bez pružanja fleksibilnosti")
                 


    def plot_input_output_noflex(self, data, res, var):

        if var == "Ech":
            graph = res.Ech
           
        elif var == "Edch":
            graph = res.Edch
           
        elif var == "delte":
            self.canvas.axes.set_ylim(0, 1.4)
            graph = res.delte
            
        elif var == "grid":
            graph = res.grid_power


        if (res.case == "noflexcpp"):
            self.canvas.axes.step(np.arange(data.N+1), np.append(graph, graph[-1]), linestyle='--', color = "purple", where="post", label = "Bez pružanja fleksibilnosti, cpp = 0")
        elif (res.case == "hist"):
            self.canvas.axes.step(np.arange(data.N+1), np.append(graph, graph[-1]), linestyle='--', color = "brown", where="post", label = "Jednostavno upravljanje")
        else:
            self.canvas.axes.step(np.arange(data.N+1), np.append(graph, graph[-1]), linestyle='--', color = "green", where="post", label = "Bez pružanja fleksibilnosti")



    def plot_profiles(self,data, var):
        if var == "envtemp":
            graph = data.env_temp_C
           
        elif var == "flow":
            graph = data.water_demand
           
        elif var == "setTemp":
            graph = data.set_water_temp_C

        elif var == "nc_load":
            graph = data.nc_load_power

        elif var == "pv":
            graph = data.pv_power

        self.canvas.axes.step(np.arange(data.N+1), np.append(graph, graph[-1]) , linestyle='--', color = "red", where="post", label = f"{self.comboBox.currentText()} ({data.day}.{data.month}.)")




