import numpy as np
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QLabel,
    QWidget,
    QVBoxLayout,
    QComboBox,
    QPushButton,
    QHBoxLayout,
    QGridLayout,
    QDateEdit
)
import re
import sys
import pandas as pd
from Parameters.getData_flex import getData as data
from MILP_formulation.extrasprojekt import Structure
import matplotlib
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import (
NavigationToolbar2QT as NavigationToolbar,
)
from PySide6.QtGui import QFont, QResizeEvent, QShowEvent
from PySide6.QtWidgets import QSizePolicy
from PySide6.QtCore import QTimer
from MILP_GUI.utils import resource_path
import os


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

        with open(resource_path("MILP_GUI/stylesheet.qss"), "r") as f:
            self.setStyleSheet(f.read())

        self.data = Structure()
        self.data = Structure()
        self.getParamsRes()
        self.result1 = None
        self.result2 = None
        self.legend1 = None
        self.legend2 = None
        self.alt_combo = QComboBox()
        self.reslayout = QVBoxLayout()
        self.hlayout = QHBoxLayout()
        self.comboBox = QComboBox()
        self.comboBox.addItems([
            "Water tank temperature",
            "Battery state of energy",
            "Water heater on-off state",
            "Battery charging power",
            "Battery discharging power",
            "Hot water consumption",
            "PV generation",
            "Uncontrollable load",
            "Target water temperature",
            "Ambient temperature",
            "Grid power",
            "Day-ahead electricity prices"
        ])

        self.hlayout.addWidget(self.comboBox)
        self.hlayout.addWidget(self.alt_combo)
        self.canvas = MplCanvas(self, width=3.47, height=2.5, dpi=100)         #self.canvas.axes.xticks(pd.date_range(start="2023-01-01", end="2023-12-31", freq="M"))
        toolbar = NavigationToolbar(self.canvas, self)
        toolbar.setStyleSheet("""
            QToolBar {
                 background: qlineargradient(
                    spread: pad,
                    x1: 0, y1: 0,
                    x2: 1, y2: 0,
                    stop: 0 #51FCBB,
                    stop: 0.5 #4EE5D9
                    stop: 1 #0C0C31
                );
            }
        """)
        self.buttonLayout = QHBoxLayout()
        self.retButton = QPushButton("Back to parameters")
        self.infoButton = QPushButton("Optimization results")
        self.resultDate = QDateEdit()
        self.saveButton = QPushButton("Save")
        self.resultDate.setDisplayFormat("d.M.")
        self.hlayout.addWidget(self.resultDate)
        
        self.labelLayout = QGridLayout()
        self.buttonLayout.addWidget(self.retButton)
        self.buttonLayout.addWidget(self.infoButton)
        self.toolbarlayout = QHBoxLayout()
        self.toolbarlayout.addWidget(toolbar)
        self.label_graph = QLabel()
        font = QFont("Segoe UI", 15, QFont.Bold)  
        self.label_graph.setFont(font)
        self.label_graph.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.toolbarlayout.addWidget(self.label_graph)
        self.toolbarlayout.addStretch()
        self.toolbarlayout.addWidget(self.saveButton)
        
        
        self.canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.reslayout.addLayout(self.hlayout, stretch=0)
        self.reslayout.addLayout(self.toolbarlayout, stretch=0)
        self.reslayout.addWidget(self.canvas, stretch=3)
        self.reslayout.addLayout(self.buttonLayout, stretch=1)
        self.setLayout(self.reslayout) 
        #signali i slotovi
        self.comboBox.currentIndexChanged.connect(self.setGraph)
        self.alt_combo.currentIndexChanged.connect(self.setGraph)
        self.comboBox.currentIndexChanged.connect(self.changeGraphFont)
        self.alt_combo.currentIndexChanged.connect(self.changeGraphFont)
        self.update_alt_combo()
        self.resultDate.dateChanged.connect(self.changePlot)
        self.saveButton.pressed.connect(self.save_ieee_pdf)
        
       

        self.pointSize = self.font().pointSize()

  

    
    def changePlot(self):
        self.paramPage.dateEdit.setDate(self.resultDate.date())
        self.setGraph()
        
         


    def loop_through_widgets(self, font):
        for widget in self.findChildren(QWidget):
            widget.setFont(font)

        buttonfont = self.retButton.font()
        buttonfont.setPointSize(font.pointSize()*1.2)
        self.retButton.setFont(buttonfont)
        self.infoButton.setFont(buttonfont)

        font = self.label_graph.font()
        font.setPointSize(font.pointSize()*1.5)
        font.setBold(True)
        self.label_graph.setFont(font)
    
    def changeGraphFont(self):
        pointSize = self.pointSize

        ax = self.canvas.axes
        ax.set_xlabel("Time [h]", fontsize=pointSize, fontfamily="serif", labelpad=pointSize*0.5)
        ax.set_ylabel(self.getYlabel(self.comboBox.currentIndex()), fontsize=pointSize, fontfamily="serif", labelpad=pointSize*0.5)

        ax.tick_params(axis='both', which='major', labelsize=pointSize)

        ax.legend(frameon=False, fontsize=pointSize)

    
    def resizeEvent(self, event: QResizeEvent):
                super().resizeEvent(event)
                
                # Heuristic: base size on window height
                h = self.height()
                new_pt = max(9, h / 60)  # adjust divisor as needed
                font = self.font()
                font.setPointSizeF(new_pt)
                self.loop_through_widgets(font)
                self.pointSize = new_pt
                self.changeGraphFont()
                self.canvas.fig.tight_layout()

    def showEvent(self, event: QShowEvent):
                super().showEvent(event)
                # Heuristic: base size on window height
                h = self.height()
                new_pt = max(9, h / 60)  # adjust divisor as needed
                font = self.font()
                font.setPointSizeF(new_pt)
                self.loop_through_widgets(font)
                self.pointSize = new_pt
                self.changeGraphFont()
                self.canvas.fig.tight_layout()

                 
               


    def clearGraph(self):
         self.canvas.axes.cla()


    def update_alt_combo(self):
        flex = self.paramPage.comboBox_2.currentIndex() == 0 
        self.alt_combo.blockSignals(True)
        if flex == True:
            self.alt_combo.setEnabled(True)
            self.alt_combo.clear()
            for i in range(self.data.n_a):
                if(self.result1 and self.result1.worst_ind == i):
                    self.alt_combo.addItem(f"Alternative profile {i+1} (WORST)")
                else:
                     self.alt_combo.addItem(f"Alternative profile {i+1}")
        else:   
            self.alt_combo.setEnabled(False)

            self.alt_combo.clear()
        self.alt_combo.blockSignals(False)

        
    def getYlabel(self, index):
        if index in [0, 8, 9]:
            label = "Temperature [°C]"
        elif index in [1,3,4]:
            label = "Energy [Wh]"
        elif index in [5]:
            label = "Volume [L]"
        elif index in [6, 7, 10]:
             label = "Power [W]"
        elif index in [11]:
             label = "Price [€/kW]"
        else:
            label = ""
        return label


    def setGraph(self):
        # Očisti prethodni graf i labele
        self.canvas.axes.cla()
        
        
        # Crtanje na temelju odabira korisnika
        if self.paramPage.radioButton_2.isChecked():
            if self.result1 and self.result1.case == "flex":
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
        ax.set_xlabel("Time [h]", fontsize=10, fontfamily="serif")
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
        self.changeGraphFont()
        self.canvas.fig.tight_layout()
        self.canvas.draw()
        #self.save_ieee_pdf()


    def save_ieee_pdf(self):
        # 1. Spremi staru veličinu
        old_size = self.canvas.fig.get_size_inches()

        # 2. Namjesti IEEE dimenzije (npr. 7.16 x 3.5 inča)
        self.canvas.fig.set_size_inches(7.16, 3.5)

        for ax in self.canvas.fig.axes:
            ax.set_xlabel(ax.get_xlabel(), fontsize=9)   # labela osi x
            ax.set_ylabel(ax.get_ylabel(), fontsize=9)   # labela osi y
            ax.tick_params(axis="both", labelsize=9)     # oznake osi

            leg = ax.get_legend()
            if leg:
                for text in leg.get_texts():
                    text.set_fontsize(9)                 # legenda

        # 3. Bazni direktorij → pored exe-a ili .py datoteke
        base_dir = os.path.dirname(sys.argv[0])

        # 4. Provjeri / napravi folder "grafovi"
        folder = os.path.join(base_dir, "grafovi")
        os.makedirs(folder, exist_ok=True)

        # 5. Ime datoteke (čisti naziv iz ComboBoxa)
        filename = re.sub(r'\s+', '_', self.comboBox.currentText())
        path = os.path.join(folder, f"{filename}.pdf")

        # 6. Spremi PDF s 600 DPI
        try:
            self.canvas.fig.savefig(path, dpi=600, bbox_inches='tight')
            print(f"Spremljeno kao {path}")
        except Exception as e:
            print(f"Greška pri spremanju PDF-a: {e}")

        # 7. Vrati staru veličinu (za GUI prikaz)
        self.canvas.fig.set_size_inches(old_size)
        self.changeGraphFont()
        self.canvas.fig.tight_layout()
        self.canvas.draw()

        # 8. Vizualna potvrda
        self.saveButton.setText("Saved!")
        self.saveButton.setDisabled(True)
        QTimer.singleShot(1000, lambda: (
            self.saveButton.setText("Save"),
            self.saveButton.setDisabled(False)
        ))
            

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
                    self.plot_state_matplotlib(self.data, self.result1, self.alt_combo.currentIndex(), "heater", self.paramPage.comboBox_4.currentText())
                    self.plot_noflex_states(self.data, self.result2, "heater")
        if self.comboBox.currentIndex() == 1:
                    self.label_graph.setText(self.comboBox.itemText(1))
                    self.plot_state_matplotlib(self.data, self.result1, self.alt_combo.currentIndex(), "batt", self.paramPage.comboBox_4.currentText())
                    self.plot_noflex_states(self.data, self.result2, "batt")
        if self.comboBox.currentIndex() == 2:
                    self.label_graph.setText(self.comboBox.itemText(2))
                    self.plot_input_output_matplotlib(self.data, self.result1, self.alt_combo.currentIndex(), "delte", self.paramPage.comboBox_4.currentText())
                    self.plot_input_output_noflex(self.data, self.result2, "delte")               
        if self.comboBox.currentIndex() == 3:
                    self.label_graph.setText(self.comboBox.itemText(3))
                    self.plot_input_output_matplotlib(self.data, self.result1, self.alt_combo.currentIndex(), "Ech" , self.paramPage.comboBox_4.currentText())
                    self.plot_input_output_noflex(self.data, self.result2, "Ech")
        if self.comboBox.currentIndex() == 4:
                    self.label_graph.setText(self.comboBox.itemText(4))
                    self.plot_input_output_matplotlib(self.data, self.result1, self.alt_combo.currentIndex(), "Edch", self.paramPage.comboBox_4.currentText() )
                    self.plot_input_output_noflex(self.data, self.result2, "Edch")
        if self.comboBox.currentIndex() == 10:
                    self.label_graph.setText(self.comboBox.itemText(10))
                    self.plot_input_output_matplotlib(self.data, self.result1, self.alt_combo.currentIndex(), "grid" , self.paramPage.comboBox_4.currentText())                
                    self.plot_input_output_noflex(self.data, self.result2, "grid")


    def plot_profiles_demand_production(self):
                self.getParamsRes()
                if self.comboBox.currentIndex() == 5:
                    self.label_graph.setText(self.comboBox.itemText(5))
                    self.plot_profiles(self.data, "flow")              
                if self.comboBox.currentIndex() == 6:
                    self.label_graph.setText(self.comboBox.itemText(6))
                    self.plot_profiles(self.data, "pv")
                    if self.result1 and self.result1.case == "flex":
                        self.plot_input_output_matplotlib(self.data, self.result1, self.alt_combo.currentIndex(), "epvused", self.paramPage.comboBox_4.currentText())
                    if self.result1 and self.result1.case == "noflex":
                        self.plot_input_output_noflex(self.data,self.result1, "epvused")
                    if(self.result2):
                         self.plot_input_output_noflex(self.data,self.result2, "epvused")
                         
                if self.comboBox.currentIndex() == 7:
                    self.label_graph.setText(self.comboBox.itemText(7))
                    self.plot_profiles(self.data, "nc_load")
                if self.comboBox.currentIndex() == 8:
                    self.label_graph.setText(self.comboBox.itemText(8))
                    self.plot_profiles(self.data, "setTemp")
                if self.comboBox.currentIndex() == 9:
                    self.label_graph.setText(self.comboBox.itemText(9))
                    self.plot_profiles(self.data, "envtemp")
                if self.comboBox.currentIndex() == 11:
                    self.label_graph.setText(self.comboBox.itemText(11))
                    self.plot_profiles(self.data, "daprice")

                    
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
                    
                    self.plot_state_matplotlib(self.data, self.result1, self.alt_combo.currentIndex(), "heater", self.paramPage.comboBox_4.currentText())
                if self.comboBox.currentIndex() == 1:
                    self.label_graph.setText(self.comboBox.itemText(1))
                    self.plot_state_matplotlib(self.data, self.result1, self.alt_combo.currentIndex(), "batt", self.paramPage.comboBox_4.currentText())
                if self.comboBox.currentIndex() == 2:
                    self.label_graph.setText(self.comboBox.itemText(2))
                    self.plot_input_output_matplotlib(self.data, self.result1, self.alt_combo.currentIndex(), "delte", self.paramPage.comboBox_4.currentText() )                
                if self.comboBox.currentIndex() == 3:
                    self.label_graph.setText(self.comboBox.itemText(3))
                    self.plot_input_output_matplotlib(self.data, self.result1, self.alt_combo.currentIndex(), "Ech", self.paramPage.comboBox_4.currentText() )
                if self.comboBox.currentIndex() == 4:
                    self.label_graph.setText(self.comboBox.itemText(4))
                    self.plot_input_output_matplotlib(self.data, self.result1, self.alt_combo.currentIndex(), "Edch", self.paramPage.comboBox_4.currentText() )
                if self.comboBox.currentIndex() == 10:
                    self.label_graph.setText(self.comboBox.itemText(10))
                    self.plot_input_output_matplotlib(self.data, self.result1, self.alt_combo.currentIndex(), "grid", self.paramPage.comboBox_4.currentText() )                


    def getParamsRes(self):
        params = self.paramPage.getParams()                
        self.data = data(
            heater_power=params[0],
            bat_cap=params[1],
            converter_power=params[2],
            tank_volume=params[3],
            PV_power=params[4],
            numberofPV=params[5],
            month=params[6],
            day=params[7],
            Q=params[8],
            F=params[9],
            R=params[10],
            beginning_flex_ready=params[11],
            end_flex_ready=params[12],
            alfa_plus=params[13],
            alfa_minus=params[14],
            cr_plus=params[15],
            cr_minus=params[16],
            sgn_Pr=params[17]
        )

    
    def plot_alt_state(self, data, alt, Pr_direction, res, scen, color):
        labelSet = False
        alt_indices = res.K_i_x[scen]
        act_indices = np.zeros((data.n_z, data.N_F + data.N_R + 1))
        for z in range(data.n_z):
            act_indices[z] = alt_indices[z * (data.N_F + data.N_R + 1):(z + 1) * (data.N_F + data.N_R + 1)]
        alt_values = alt[scen * data.n_z * (data.N_F + data.N_R + 1):(scen + 1) * data.n_z * (data.N_F + data.N_R + 1)]
        act_values = np.zeros((data.n_z, data.N_F + data.N_R + 1))
        
        for z in range(data.n_z):
            act_values[z] = alt_values[z * (data.N_F + data.N_R + 1):(z + 1) * (data.N_F + data.N_R + 1)]
       
        for z in range(data.n_z):
            act_ind = act_indices[z]
            act_val = act_values[z]

            if 0 in act_ind:
                index = np.where(act_ind == 0)[0][0]
                self.canvas.axes.plot(np.append(act_ind[:index], data.N), act_val[:index + 1], linestyle="--", linewidth=2, color = color)
                if not labelSet:
                    self.canvas.axes.plot(act_ind[index:], act_val[index:], linestyle="--", linewidth=2, color = color,  label = self.alt_combo.currentText() + " " + Pr_direction)
                    labelSet = True
                else:
                     self.canvas.axes.plot(act_ind[index:], act_val[index:], linestyle="--", linewidth=2, color = color)        
            else:
                if not labelSet:
                    self.canvas.axes.plot(act_ind, act_val, linestyle="--", linewidth=2, color = color,  label = self.alt_combo.currentText() + " " + Pr_direction)
                    labelSet = True
                else:
                     self.canvas.axes.plot(act_ind, act_val, linestyle="--", linewidth=2, color = color)
         
        

    def plot_state_matplotlib(self, data, res, scen, var,  Pr_direction):
        if var == "heater":
            alt_plus = res.tempC_alt_plus
            alt_minus = res.tempC_alt_minus
            nom = res.tempC_nom
            ymax = max(alt_plus.max(), alt_minus.max(), nom.max())
            self.canvas.axes.set_ylim(0, 1.6 * ymax)
        elif var == "batt":
            alt_plus = res.SOE_alt_plus.ravel()
            alt_minus = res.SOE_alt_minus.ravel()
            nom = res.SOE_nom
            ymax = max(alt_plus.max(), alt_minus.max(), nom.max())
            self.canvas.axes.set_ylim(0, 1.6 * ymax)
        # Nominalno stanje
        self.canvas.axes.plot(np.arange(data.N + 1), nom , linestyle="--", linewidth=2.5, color = "red", label = "Nominal profile")

        if (Pr_direction == "positive"):
            alt_minus = None
        elif (Pr_direction == "negative"):
            alt_plus = None

        if alt_plus is not None:
            self.plot_alt_state(data, alt_plus, "positive", res, scen, "orange")

        if alt_minus is not None:
            self.plot_alt_state(data, alt_minus, "negative", res, scen, "green")

        
    def plot_alt_input_output(self, data, res, scen, color, Pr_direction, nom, alt):
        labelSet = False

        alt_indices = res.K_i[scen]
        act_indices = np.zeros((data.n_z, data.N_F + data.N_R))
        for z in range(data.n_z):
            act_indices[z] = alt_indices[z * (data.N_F + data.N_R):(z + 1) * (data.N_F + data.N_R)]

        alt_values = alt[scen * data.n_z * (data.N_F + data.N_R):(scen + 1) * data.n_z * (data.N_F + data.N_R)]
        act_values = np.zeros((data.n_z, data.N_F + data.N_R))
        for z in range(data.n_z):
            act_values[z] = alt_values[z * (data.N_F + data.N_R):(z + 1) * (data.N_F + data.N_R)]
        
        for z in range(data.n_z):
            act_ind = act_indices[z]
            act_ind = np.append(act_ind, (act_ind[-1]+1)%data.N)
            act_val = act_values[z]
            act_val = np.append(act_val, act_val[-1])

            
          
            if 0 in act_ind and act_ind[0] != 0:
                index = np.where(act_ind == 0)[0][0]
                changed_ind = np.concatenate((act_ind[:index], [act_ind[index-1]+1], act_ind[index:]))
                changed_val = np.concatenate((act_val[:index], [act_val[index-1]], act_val[index:]))
                
                self.canvas.axes.step(changed_ind[:index+1], changed_val[:index+1], linestyle="--", linewidth=2, color=color, where="post")
                if not labelSet:
                    self.canvas.axes.step(changed_ind[index+1:], changed_val[index+1:], linestyle="--", linewidth=2, color=color, where="post",  label = self.alt_combo.currentText() + " " + Pr_direction)
                    labelSet = True
                else:
                     self.canvas.axes.step(changed_ind[index+1:], changed_val[index+1:], linestyle="--", linewidth=2, color=color, where="post")
            else:
               
                if not labelSet:
                    self.canvas.axes.step(act_ind, act_val, linestyle="--", linewidth=2, color=color, where="post",  label = self.alt_combo.currentText() + " " + Pr_direction)
                    labelSet = True
                else:
                     self.canvas.axes.step(act_ind, act_val, linestyle="--", linewidth=2, color=color, where="post")
            if int(act_ind[0]) > 0 and nom[int(act_ind[0]) - 1] != act_val[0]:
                self.canvas.axes.step([act_ind[0], act_ind[0]], [act_val[0], nom[int(act_ind[0])]], color=color, linestyle=':', linewidth=2, where="post")

            if int(act_ind[-1]) + 1 < len(nom) and nom[int(act_ind[-1]) + 1] != act_val[-1]:
                self.canvas.axes.step([act_ind[-1], act_ind[-1]], [act_val[-1], nom[int(act_ind[-1])]], color=color, linestyle=':', linewidth=2, where="post"
                                )


    def plot_input_output_matplotlib(self, data, res, scen, var, Pr_direction):
        if var == "Ech":
            alt_plus = res.Ech_alt_plus
            alt_minus = res.Ech_alt_minus
            nom = res.Ech_nom
            ymax = max(alt_plus.max(), alt_minus.max(), nom.max())
            self.canvas.axes.set_ylim(0, 1.6 * ymax)
        elif var == "Edch":
            alt_plus = res.Edch_alt_plus
            alt_minus = res.Edch_alt_minus
            nom = res.Edch_nom
            ymax = max(alt_plus.max(), alt_minus.max(), nom.max())
            self.canvas.axes.set_ylim(0, 1.6 * ymax)
        elif var == "delte":
            alt_plus = res.delte_alt_plus
            alt_minus = res.delte_alt_minus
            nom = res.delte
            ymax = max(alt_plus.max(), alt_minus.max(), nom.max())
            self.canvas.axes.set_ylim(0, 1.7 * ymax)
        elif var == "grid":
            alt_plus = res.grid_power_alt_plus.ravel()
            alt_minus = res.grid_power_alt_minus.ravel()
            nom = res.grid_power_nom
            ymax = max(alt_plus.max(), alt_minus.max(), nom.max())
            ymin = min(alt_plus.min(), alt_minus.min(), nom.min())
            self.canvas.axes.set_ylim(min(-1000,-1.6*abs(ymin)), max(1000,1.6 * ymax))
        elif var == "epvused":
            alt_plus = res.PPV_alt_plus
            alt_minus =  res.PPV_alt_minus
            nom = res.PPV_nom
            ymax = max(alt_plus.max(), alt_minus.max(), nom.max())
            self.canvas.axes.set_ylim(0, 1.6 * ymax)

        # Nominalna vrijednost (dashed)
        self.canvas.axes.step(np.arange(data.N+1), np.append(nom,nom[-1]), linestyle="--", linewidth=2.5, color = "red", where="post", label = "Nominal profile")
        
        if (Pr_direction == "positive"):
             alt_minus = None
        elif (Pr_direction == "negative"):
             alt_plus = None

        if alt_plus is not None:
            self.plot_alt_input_output(data, res, scen, "orange", "positive", nom, alt_plus)
        if alt_minus is not None:
            self.plot_alt_input_output(data, res, scen, "green", "negative", nom, alt_minus)
       


    def plot_noflex_states(self, data, res, var):
        if var == "heater":
            graph = res.tempC
            if not self.result1.case == "flex":
                self.canvas.axes.set_ylim(0, max(1.6*max(self.result1.tempC), 1.6*max(graph)))
            else:
                 self.canvas.axes.set_ylim(0, max(1.6*max(self.result1.tempC_nom),max(1.6*max(self.result1.tempC_alt_plus),1.6*max(self.result1.tempC_alt_minus), 1.6*max(graph))))
        elif var == "batt":
            graph = res.SOE
            if not self.result1.case == "flex":
                self.canvas.axes.set_ylim(0, 1.6*max(graph))
        if(res.case == "noflexcpp"):
            self.canvas.axes.plot(np.arange(data.N + 1), graph , linestyle="--", linewidth=1.6, color = "magenta", label = "Without DR and peak power")
        elif (res.case == "hist"):
            self.canvas.axes.plot(np.arange(data.N + 1), graph , linestyle="--", linewidth=1.6, color = "brown", label = "Hysteresis control")
        else:
            self.canvas.axes.plot(np.arange(data.N + 1), graph , linestyle="--", linewidth=1.6, color = "blue", label = "Without DR")
                 

    def plot_input_output_noflex(self, data, res, var):
        if var == "Ech":
            graph = res.Ech
            if not self.result1.case == "flex":
                self.canvas.axes.set_ylim(0, max(1.6*max(self.result1.Ech),1.6*max(graph)))     
            else:
                 self.canvas.axes.set_ylim(0, max(1.6*max(self.result1.Ech_nom),1.6*max(self.result1.Ech_alt_plus),1.6*max(self.result1.Ech_alt_minus),1.6*max(graph)))     
        elif var == "Edch":
            graph = res.Edch  
            if not self.result1.case == "flex":
                self.canvas.axes.set_ylim(0, max(1.6*max(self.result1.Edch),1.6*max(graph))) 
            else:
                 self.canvas.axes.set_ylim(0, max(1.6*max(self.result1.Edch_nom),1.6*max(self.result1.Edch_alt_plus),1.6*max(self.result1.Edch_alt_minus),1.6*max(graph)))       
        elif var == "delte":
            graph = res.delte
            if not self.result1.case == "flex":
                self.canvas.axes.set_ylim(0, max(1.7*max(self.result1.delte),1.7*max(graph)))
            else:
                 self.canvas.axes.set_ylim(0, max(1.7*max(self.result1.delte),1.7*max(self.result1.delte_alt_plus),1.7*max(self.result1.delte_alt_minus),1.7*max(graph)))
        elif var == "epvused":
            graph = res.PPV_used
            if not self.result1.case == "flex":
                self.canvas.axes.set_ylim(0, max(1.6*max(self.result1.PPV_used),1.6*max(graph)))    
            else:
                 self.canvas.axes.set_ylim(0, max(1.6*max(self.result1.PPV_nom),1.6*max(self.result1.PPV_alt_plus),1.6*max(self.result1.PPV_alt_minus),1.6*max(graph)))        
        elif var == "grid":
            graph = res.grid_power
            if not self.result1.case == "flex":
                self.canvas.axes.set_ylim(min(-1000,-1.6*abs(graph.min())), max(1000,1.6*max(graph)))
            else:
                self.canvas.axes.set_ylim(min(-1.6*abs(self.result1.grid_power_nom.min()),-1.6*abs(self.result1.grid_power_alt_plus.min()),-1.6*abs(self.result1.grid_power_alt_minus.min()),-1000,-1.6*abs(graph.min())),
                                           max(1000,1.6*max(graph),1.6*self.result1.grid_power_nom.max(),1.6*self.result1.grid_power_alt_plus.max(),1.6*self.result1.grid_power_alt_minus.max()))
        if (res.case == "noflexcpp"):
            if(var == "epvused"):
                self.canvas.axes.step(np.arange(data.N+1), np.append(graph, graph[-1]), linestyle="--", linewidth=1.6, color = "magenta", where="post", label = "Without DR and PP)")
            else:
                self.canvas.axes.step(np.arange(data.N+1), np.append(graph, graph[-1]), linestyle="--", linewidth=1.6, color = "magenta", where="post", label = "Without DR and peak power")
        elif (res.case == "hist" and var != "epvused"):
            self.canvas.axes.step(np.arange(data.N+1), np.append(graph, graph[-1]), linestyle="--", linewidth=1.6, color = "brown", where="post", label = "Hysteresis control")
        elif (res.case == "hist" and var == "epvused"):
            self.canvas.axes.step(np.arange(data.N+1), np.append(graph, graph[-1]), linestyle="--", linewidth=1.6, color = "brown", where="post", label = "Hysteresis control")
        else:
            if(var == "epvused"):
                self.canvas.axes.step(np.arange(data.N+1), np.append(graph, graph[-1]), linestyle="--", linewidth=1.6, color = "blue", where="post", label = "Without DR")
            else:
                 self.canvas.axes.step(np.arange(data.N+1), np.append(graph, graph[-1]), linestyle="--", linewidth=1.6, color = "blue", where="post", label = "Without DR")
                 


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
        elif var == "daprice":
            graph = data.da_prices*(10**3)
        self.canvas.axes.step(np.arange(data.N+1), np.append(graph, graph[-1]) , linestyle="--", linewidth=1, color = "purple", where="post", label = f"{self.comboBox.currentText()} ({data.day}.{data.month}.)")




