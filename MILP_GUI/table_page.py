from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QLabel,
    QWidget,
    QLineEdit,
    QSlider,
    QVBoxLayout
)
from MILP_GUI.TableWidget import Ui_TableWidget
from PySide6.QtWidgets import QTableWidgetItem, QHeaderView


from Parameters.getData_noflex import getData as data_noflex
from Parameters.getData_flex import getData as data_flex

import numpy as np

class TablePage(QWidget, Ui_TableWidget):
    def __init__(self, resultPage, paramPage):
        super().__init__()
        self.setupUi(self)
        self.resultPage = resultPage
        self.paramPage = paramPage

        self.rownames = [
            '<span style="font-size:12pt; font-weight:bold">Dan unaprijed trošak [€]</span>',
            '<span style="font-size:12pt; font-weight:bold">Trošak vršne snage (bez fleksibilnosti) [€]</span>',
            '<span style="font-size:12pt; font-weight:bold">Trošak vršne snage (nominalni) [€]</span>',
            '<span style="font-size:12pt; font-weight:bold">Trošak vršne snage (alternativni) [€]</span>',
            '<span style="font-size:12pt; font-weight:bold">Trošak uravnoteženja sustava [€]</span>',
            '<span style="font-size:12pt; font-weight:bold">Rezervirana snaga [W]</span>',
            '<span style="font-size:12pt; font-weight:bold">Optimizacijski kriterij J<sub>ai</sub> [€]</span>',
            '<span style="font-size:12pt; font-weight:bold">Optimizacijski kriterij J<sub>n</sub> [€]</span>',
            '<span style="font-size:12pt; font-weight:bold">Optimizacijski kriterij J<sub>no-flex</sub> [€]</span>',
            '<span style="font-size:12pt; font-weight:bold">Optimizacijski kriterij J<sub>DR</sub> [€]</span>'
        ]



        self.result1 = None
        self.result2 = None
        self.data_flex = None
        self.data_noflex = None

        self.flex = False

        self.firstRun = True

                
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.tableWidget.verticalHeader().setStretchLastSection(True)
        self.tableWidget.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.horizontalHeader().setVisible(False)

        
        self.resultPage.infoButton.pressed.connect(self.updateTablePage)
        self.comboBox.currentIndexChanged.connect(self.update_Table)
        

    
    def update_table_flex(self):
        self.flex = self.result1 and self.result1.case == "flex"

    
    def update_Table(self):
        self.update_table_flex()
        alt_scen = self.comboBox.currentIndex()
        if(self.result1):
            if(self.flex):
                print(self.result1.table)
                for i in range(self.result1.table.shape[0]):
                    if(self.result1.table[i][0] != -1):
                        self.tableWidget.setItem(i+1, 1, QTableWidgetItem(str(round(self.result1.table[i][alt_scen],2))))
                    else:
                        self.tableWidget.setItem(i+1, 1, QTableWidgetItem("/"))
                    item = self.tableWidget.item(i+1, 1)
                    font = item.font()
                    font.setPointSize(12)
                    item.setTextAlignment(Qt.AlignCenter)
                    item.setFont(font)


            else:
                for i in range(self.result1.table.shape[0]):
                    if(self.result1.table[i][0] != -1):
                        self.tableWidget.setItem(i+1, 1, QTableWidgetItem(str(round(self.result1.table[i][0],2))))
                    else:
                        self.tableWidget.setItem(i+1, 1, QTableWidgetItem("/"))
                    item = self.tableWidget.item(i+1, 1)
                    font = item.font()
                    font.setPointSize(12)
                    item.setTextAlignment(Qt.AlignCenter)
                    item.setFont(font)



        if(self.result2):
            for i in range(self.result2.table.shape[0]):
                if(self.result2.table[i][0] != -1):
                    self.tableWidget.setItem(i+1, 2, QTableWidgetItem(str(round(self.result2.table[i][0],2))))
                else:
                    self.tableWidget.setItem(i+1, 2, QTableWidgetItem("/"))
                item = self.tableWidget.item(i+1, 2)
                font = item.font()
                font.setPointSize(12)
                item.setTextAlignment(Qt.AlignCenter)
                item.setFont(font)



    def getResults(self):
        self.result1 = self.resultPage.result1

        self.getParamsFlexTable()

        self.getParamsNoFlexTable()

    
        if(self.resultPage.result2):
            self.result2 = self.resultPage.result2
        

    def updateTablePage(self):
        if(self.firstRun):        
            self.getResults()
            self.update_combo_table()

            if(self.paramPage.radioButton_2.isChecked()):
                self.tableWidget.setRowCount(1+len(self.rownames))
                self.tableWidget.setColumnCount(2)
                self.tableWidget.setItem(0, 1, QTableWidgetItem(self.paramPage.comboBox_2.currentText()))
                
            
            if(self.paramPage.radioButton.isChecked()):
                self.tableWidget.setRowCount(1+len(self.rownames))
                self.tableWidget.setColumnCount(3)
                self.tableWidget.setItem(0, 1, QTableWidgetItem(self.paramPage.comboBox_2.currentText()))
                self.tableWidget.setItem(0, 2, QTableWidgetItem(self.paramPage.comboBox_3.currentText()))
          

            self.tableWidget.setItem(0, 0, QTableWidgetItem("Parametri"))

            for i in range(len(self.rownames)):
                label = QLabel(self.rownames[i], self.tableWidget)
                label.setTextFormat(Qt.RichText)          
                label.setAlignment(Qt.AlignCenter)        
                self.tableWidget.setCellWidget(i + 1, 0, label)
                            
            for i in range(self.tableWidget.rowCount()):
                for j in range(self.tableWidget.columnCount()):
                    item = self.tableWidget.item(i, j)
                    if item:
                        font = item.font()
                        if i == 0:
                            # Prvi red (zaglavlje) – bold + 15
                            font.setBold(True)
                            font.setPointSize(15)
                        elif j == 0:
                            # Prvi stupac – bold + 12
                            font.setBold(True)
                            font.setPointSize(12)
                        else:
                            # Ostale ćelije – normalno + 12
                            font.setBold(False)
                            font.setPointSize(12)

                        item.setFont(font)
                        item.setTextAlignment(Qt.AlignCenter)



       
        self.firstRun = False
        self.update_Table()



    def update_combo_table(self):
        self.update_table_flex()
        if self.flex == True:
            self.comboBox.setEnabled(True)
            self.comboBox.clear()
            self.comboBox.blockSignals(True)
            for i in range(self.data_flex.n_a):
                if(self.result1 and i == self.result1.worst_ind):
                    self.comboBox.addItem(f"Alternativni scenarij {i+1} (WORST)")
                else:
                    self.comboBox.addItem(f"Alternativni scenarij {i+1}")

        else:   
            self.comboBox.setEnabled(False)

            self.comboBox.clear()

        self.comboBox.blockSignals(False)
        
        



                    

    def getParamsNoFlexTable(self):
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
        

    def getParamsFlexTable(self):
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



