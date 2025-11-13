from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QLabel,
    QWidget
)
from PySide6.QtGui import QFont, QResizeEvent, QShowEvent
from MILP_GUI.TableWidget import Ui_TableWidget
from PySide6.QtWidgets import QTableWidgetItem, QHeaderView
from Parameters.getData_flex import getData as data

class TablePage(QWidget, Ui_TableWidget):
    def __init__(self, resultPage, paramPage):
        super().__init__()
        self.setupUi(self)
        self.resultPage = resultPage
        self.paramPage = paramPage
        
        self.texts_en = [
            "Reserved power P<sub>res</sub> [kW]",
            "Day-ahead cost J<sub>DA</sub> [€]",
            "Peak power cost J<sub>PP</sub> [€]",
            "Intra-day cost J<sub>ID</sub> [€]",
            "Energy cost [€]",
            "Operational cost [€]"
        ]

        self.texts_en_table2 = [
            "Heater energy [kWh]",
            "Grid energy [kWh]",
            "PV energy [kWh]",
            "PV generation [kWh]",
            "Non-controllable load [kWh]"
        ]


        self.result1 = None
        self.result2 = None
        self.data = None
        self.data_noflex = None
        self.flex = False
        self.firstRun = True    
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.verticalHeader().setStretchLastSection(True)
        self.tableWidget.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.horizontalHeader().setVisible(False)
        self.tableWidget_2.horizontalHeader().setStretchLastSection(True)
        self.tableWidget_2.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget_2.verticalHeader().setStretchLastSection(True)
        self.tableWidget_2.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget_2.verticalHeader().setVisible(False)
        self.tableWidget_2.horizontalHeader().setVisible(False)
        self.comboBox.currentIndexChanged.connect(self.update_Table)
        self.tabWidget.setCurrentIndex(0)  

    def loop_through_widgets(self, font):
            for widget in self.findChildren(QWidget):
                widget.setFont(font)

            font = self.label.font()
            font.setPointSize(font.pointSize()*1.5)
            font.setBold(True)
            self.label.setFont(font)

    def resizeEvent(self, event: QResizeEvent):
                super().resizeEvent(event)
                
                # Heuristic: base size on window height
                h = self.height()
                new_pt = max(9, h / 60)  # adjust divisor as needed
                font = self.font()
                font.setPointSizeF(new_pt)
                self.loop_through_widgets(font)
                
                for i in range(self.tableWidget.rowCount()):
                    for j in range(self.tableWidget.columnCount()):
                        item = self.tableWidget.item(i, j)
                        if item:
                            font = item.font()
                            if i == 0:
                                font.setBold(True)
                            item.setFont(font)
                            item.setTextAlignment(Qt.AlignCenter)
                        elif i != 0 and j == 0:
                                    label = QLabel(f'<span style="font-size:{int(new_pt)}pt; font-weight:bold">{self.texts_en[i-1]}</span>', self.tableWidget)
                                    label.setTextFormat(Qt.RichText)          
                                    label.setAlignment(Qt.AlignCenter)        
                                    self.tableWidget.setCellWidget(i, 0, label) 

                for i in range(self.tableWidget_2.rowCount()):
                    for j in range(self.tableWidget_2.columnCount()):
                        item = self.tableWidget_2.item(i, j)
                        if item:
                            font = item.font()
                            if i == 0:
                                font.setBold(True)
                            item.setFont(font)
                            item.setTextAlignment(Qt.AlignCenter)
                        elif i != 0 and j == 0:
                                    label = QLabel(f'<span style="font-size:{int(new_pt)}pt; font-weight:bold">{self.texts_en_table2[i-1]}</span>', self.tableWidget_2)
                                    label.setTextFormat(Qt.RichText)          
                                    label.setAlignment(Qt.AlignCenter)        
                                    self.tableWidget_2.setCellWidget(i, 0, label) 
    

    def _span_first_two_rows_table2(self):
        if self.tableWidget_2.columnCount() >=3:       
            self.tableWidget_2.setSpan(4, 1, 1, 4)
            self.tableWidget_2.setSpan(5, 1, 1, 4)
        


      


    def showEvent(self, event: QShowEvent):
                super().showEvent(event)
                print("SHOW EVENT")
                self.getResults()
                self.update_combo_table()
                # Heuristic: base size on window height
                h = self.height()
                new_pt = max(9, h / 60)  # adjust divisor as needed
                font = self.font()
                font.setPointSizeF(new_pt)
                self.loop_through_widgets(font)

                if(self.paramPage.radioButton_2.isChecked()):
                                    self.tableWidget.setRowCount(1+len(self.texts_en))
                                    self.tableWidget.setColumnCount(2)
                                    self.tableWidget.setItem(0, 1, QTableWidgetItem(self.paramPage.comboBox_2.currentText()))
                                    if (self.paramPage.comboBox_2.currentText() == "With DR"):
                                        if (self.paramPage.comboBox_4.currentText() == "positive and negative"):
                                            self.tableWidget.setColumnCount(4)
                                            self.tableWidget.setItem(0, 1, QTableWidgetItem("EDR Nominal"))
                                            self.tableWidget.setItem(0, 2, QTableWidgetItem("Positive EDR"))
                                            self.tableWidget.setItem(0, 3, QTableWidgetItem("Negative EDR"))
                                        else:
                                            self.tableWidget.setColumnCount(2)
                                            self.tableWidget.setItem(0, 1, QTableWidgetItem(f"{self.paramPage.comboBox_4.currentText()} EDR"))        
                                    else:       
                                        self.tableWidget.setColumnCount(2)
                                        self.tableWidget.setItem(0, 1, QTableWidgetItem(self.paramPage.comboBox_2.currentText()))
                                        

                if(self.paramPage.radioButton.isChecked()):
                                    self.tableWidget.setRowCount(1 + len(self.texts_en))
                                    if (self.paramPage.comboBox_2.currentText() == "With DR"):
                                        if (self.paramPage.comboBox_4.currentText() == "positive and negative"):
                                            self.tableWidget.setColumnCount(5)
                                            self.tableWidget.setItem(0, 1, QTableWidgetItem("EDR Nominal"))
                                            self.tableWidget.setItem(0, 2, QTableWidgetItem("Positive EDR"))
                                            self.tableWidget.setItem(0, 3, QTableWidgetItem("Negative EDR"))
                                            self.tableWidget.setItem(0, 4, QTableWidgetItem(self.paramPage.comboBox_3.currentText()))
                                        else:
                                            self.tableWidget.setColumnCount(4)
                                            self.tableWidget.setItem(0, 1, QTableWidgetItem("EDR Nominal"))
                                            self.tableWidget.setItem(0, 2, QTableWidgetItem(f"{self.paramPage.comboBox_4.currentText()} EDR"))
                                            self.tableWidget.setItem(0, 3, QTableWidgetItem(self.paramPage.comboBox_3.currentText()))           
                                    else:       
                                        self.tableWidget.setColumnCount(3)
                                        self.tableWidget.setItem(0, 1, QTableWidgetItem(self.paramPage.comboBox_2.currentText()))
                                        self.tableWidget.setItem(0, 2, QTableWidgetItem(self.paramPage.comboBox_3.currentText()))

                
                if(self.paramPage.radioButton_2.isChecked()):
                                    self.tableWidget_2.setRowCount(1+len(self.texts_en_table2))
                                    if (self.paramPage.comboBox_2.currentText() == "With DR"):
                                        if (self.paramPage.comboBox_4.currentText() == "positive and negative"):
                                            self.tableWidget.setColumnCount(4)
                                            self.tableWidget.setItem(0, 1, QTableWidgetItem("EDR Nominal"))
                                            self.tableWidget.setItem(0, 2, QTableWidgetItem("Positive EDR"))
                                            self.tableWidget.setItem(0, 3, QTableWidgetItem("Negative EDR"))
                                        else:
                                            self.tableWidget_2.setColumnCount(3)
                                            self.tableWidget_2.setItem(0, 1, QTableWidgetItem("EDR Nominal")) 
                                            self.tableWidget_2.setItem(0, 2, QTableWidgetItem(f"{self.paramPage.comboBox_4.currentText()} EDR"))          
                                    else:       
                                        self.tableWidget_2.setColumnCount(2)
                                        self.tableWidget_2.setItem(0, 1, QTableWidgetItem(self.paramPage.comboBox_2.currentText()))

                
                if(self.paramPage.radioButton.isChecked()):
                                    self.tableWidget_2.setRowCount(1+len(self.texts_en_table2))
                                    if (self.paramPage.comboBox_2.currentText() == "With DR"):
                                        if (self.paramPage.comboBox_4.currentText() == "positive and negative"):
                                            self.tableWidget_2.setColumnCount(5)
                                            self.tableWidget_2.setItem(0,1, QTableWidgetItem("Nominal EDR"))
                                            self.tableWidget_2.setItem(0, 2, QTableWidgetItem("Positive EDR"))
                                            self.tableWidget_2.setItem(0, 3, QTableWidgetItem("Negative EDR"))
                                            self.tableWidget_2.setItem(0, 4, QTableWidgetItem(self.paramPage.comboBox_3.currentText()))
                                        else:
                                            self.tableWidget_2.setColumnCount(4)
                                            self.tableWidget_2.setItem(0,1, QTableWidgetItem("Nominal EDR"))
                                            self.tableWidget_2.setItem(0, 2, QTableWidgetItem(f"{self.paramPage.comboBox_4.currentText()} EDR"))
                                            self.tableWidget_2.setItem(0, 3, QTableWidgetItem(self.paramPage.comboBox_3.currentText()))           
                                    else:       
                                        self.tableWidget_2.setColumnCount(3)
                                        self.tableWidget_2.setItem(0, 1, QTableWidgetItem(self.paramPage.comboBox_2.currentText()))
                                        self.tableWidget_2.setItem(0, 2, QTableWidgetItem(self.paramPage.comboBox_3.currentText()))
                
                self._span_first_two_rows_table2()
                
               
                
                
                for i in range(self.tableWidget.rowCount()):
                    for j in range(self.tableWidget.columnCount()):
                        item = self.tableWidget.item(i, j)
                        if item:
                            font = item.font()
                            if i == 0:
                                font.setBold(True)
                            item.setFont(font)
                            item.setTextAlignment(Qt.AlignCenter)
                        elif i != 0 and j == 0:
                                    label = QLabel(f'<span style="font-size:{int(new_pt)}pt; font-weight:bold">{self.texts_en[i-1]}</span>', self.tableWidget)
                                    label.setTextFormat(Qt.RichText)          
                                    label.setAlignment(Qt.AlignCenter)        
                                    self.tableWidget.setCellWidget(i, 0, label) 

                for i in range(self.tableWidget_2.rowCount()):
                    for j in range(self.tableWidget_2.columnCount()):
                        item = self.tableWidget_2.item(i, j)
                        if item:
                            font = item.font()
                            if i == 0:
                                font.setBold(True)
                            item.setFont(font)
                            item.setTextAlignment(Qt.AlignCenter)
                        elif i != 0 and j == 0:
                                    label = QLabel(f'<span style="font-size:{int(new_pt)}pt; font-weight:bold">{self.texts_en_table2[i-1]}</span>', self.tableWidget_2)
                                    label.setTextFormat(Qt.RichText)          
                                    label.setAlignment(Qt.AlignCenter)        
                                    self.tableWidget_2.setCellWidget(i, 0, label) 

                print("Napravio tablicu")
                self.update_Table()

    def update_table_flex(self):
        self.flex = self.result1 and self.result1.case == "flex"

    
    def update_Table(self):
        self.update_table_flex()
        alt_scen = self.comboBox.currentIndex()

        self.getParams()

        table2 = [sum(self.data.pv_energy)/1000, sum(self.data.nc_load_energy)/1000] #Wh -> kWh
        for i in range(3,5):
            self.tableWidget_2.setItem(i+1, 1, QTableWidgetItem(str(round(table2[i-3],2))))
            item = self.tableWidget_2.item(i+1, 1)
            item.setTextAlignment(Qt.AlignCenter)

        if(self.result1):
            if(self.flex):
                #Tablica costova
                if(self.paramPage.comboBox_4.currentText() == "positive and negative"):
                    for i in range(self.result1.table_plus.shape[0]):
                        if(self.result1.table_nom[i][0] != -1):
                            self.tableWidget.setItem(i+1, 1, QTableWidgetItem(str(round(self.result1.table_nom[i][alt_scen],2))))        
                        else:
                            self.tableWidget.setItem(i+1, 1, QTableWidgetItem("-"))
                        if(self.result1.table_plus[i][0] != -1):
                            if(i == 0): #Pr na 3 decimale
                                self.tableWidget.setItem(i+1, 2, QTableWidgetItem(str(round(self.result1.table_plus[i][alt_scen],3))))
                            else:
                                self.tableWidget.setItem(i+1, 2, QTableWidgetItem(str(round(self.result1.table_plus[i][alt_scen],2))))        
                        else:
                            self.tableWidget.setItem(i+1, 2, QTableWidgetItem("-"))
                        if(self.result1.table_minus[i][0] != -1):
                            if(i == 0): #Pr na 3 decimale
                                self.tableWidget.setItem(i+1, 3, QTableWidgetItem(str(round(self.result1.table_minus[i][alt_scen],3))))
                            else:
                                self.tableWidget.setItem(i+1, 3, QTableWidgetItem(str(round(self.result1.table_minus[i][alt_scen],2))))    
                        else:
                            self.tableWidget.setItem(i+1, 3, QTableWidgetItem("-"))
                        
                        item = self.tableWidget.item(i+1, 1)
                        item.setTextAlignment(Qt.AlignCenter)
                        item = self.tableWidget.item(i+1, 2)
                        item.setTextAlignment(Qt.AlignCenter)
                        item = self.tableWidget.item(i+1, 3)
                        item.setTextAlignment(Qt.AlignCenter)


                elif(self.paramPage.comboBox_4.currentText() == "positive"):
                        for i in range(self.result1.table_plus.shape[0]):
                            if(self.result1.table_nom[i][0] != -1):
                                self.tableWidget.setItem(i+1, 1, QTableWidgetItem(str(round(self.result1.table_nom[i][alt_scen],2))))        
                            else:
                                self.tableWidget.setItem(i+1, 1, QTableWidgetItem("-"))
                            if(self.result1.table_plus[i][0] != -1):
                                if(i == 0): #Pr na 3 decimale
                                    self.tableWidget.setItem(i+1, 2, QTableWidgetItem(str(round(self.result1.table_plus[i][alt_scen],3))))
                                else:
                                    self.tableWidget.setItem(i+1, 2, QTableWidgetItem(str(round(self.result1.table_plus[i][alt_scen],2))))        
                            else:
                                self.tableWidget.setItem(i+1, 2, QTableWidgetItem("-"))
                        
                        item = self.tableWidget.item(i+1, 1)
                        item.setTextAlignment(Qt.AlignCenter)
                        item = self.tableWidget.item(i+1, 2)
                        item.setTextAlignment(Qt.AlignCenter)


                elif(self.paramPage.comboBox_4.currentText() == "negative"):
                        for i in range(self.result1.table_plus.shape[0]):
                            if(self.result1.table_nom[i][0] != -1):
                                self.tableWidget.setItem(i+1, 1, QTableWidgetItem(str(round(self.result1.table_nom[i][alt_scen],2))))        
                            else:
                                self.tableWidget.setItem(i+1, 1, QTableWidgetItem("-"))
                            
                            if(self.result1.table_minus[i][0] != -1):
                                if(i == 0): #Pr na 3 decimale
                                    self.tableWidget.setItem(i+1, 2, QTableWidgetItem(str(round(self.result1.table_minus[i][alt_scen],3))))
                                else:
                                    self.tableWidget.setItem(i+1, 2, QTableWidgetItem(str(round(self.result1.table_minus[i][alt_scen],2))))    
                            else:
                                self.tableWidget.setItem(i+1, 2, QTableWidgetItem("-"))
                            
                            item = self.tableWidget.item(i+1, 1)
                            item.setTextAlignment(Qt.AlignCenter)
                            item = self.tableWidget.item(i+1, 2)
                            item.setTextAlignment(Qt.AlignCenter)
                else:
                 pass

                #Tablica energija
                if(self.paramPage.comboBox_4.currentText() == "positive and negative"):
                    for i in range(self.result1.table2_plus.shape[0]):
                        if(self.result1.table2_nom[i][0] != -1):
                            self.tableWidget_2.setItem(i+1, 1, QTableWidgetItem(str(round(self.result1.table2_nom[i][alt_scen],2))))
                        else:
                            self.tableWidget_2.setItem(i+1, 1, QTableWidgetItem("-"))
                        if(self.result1.table2_plus[i][0] != -1):
                            self.tableWidget_2.setItem(i+1, 2, QTableWidgetItem(str(round(self.result1.table2_plus[i][alt_scen],2))))
                        else:
                            self.tableWidget_2.setItem(i+1, 2, QTableWidgetItem("-"))

                        if(self.result1.table2_minus[i][0] != -1):
                            self.tableWidget_2.setItem(i+1, 3, QTableWidgetItem(str(round(self.result1.table2_minus[i][alt_scen],2))))
                        else:
                            self.tableWidget_2.setItem(i+1, 3, QTableWidgetItem("-"))

                        item = self.tableWidget_2.item(i+1, 1)
                        item.setTextAlignment(Qt.AlignCenter)
                        item = self.tableWidget_2.item(i+1, 2)
                        item.setTextAlignment(Qt.AlignCenter)
                        item = self.tableWidget_2.item(i+1, 3)
                        item.setTextAlignment(Qt.AlignCenter)
                
                elif(self.paramPage.comboBox_4.currentText() == "positive"):
                     for i in range(self.result1.table2_plus.shape[0]):
                        if(self.result1.table2_nom[i][0] != -1):
                            self.tableWidget_2.setItem(i+1, 1, QTableWidgetItem(str(round(self.result1.table2_nom[i][alt_scen],2))))
                        else:
                            self.tableWidget_2.setItem(i+1, 1, QTableWidgetItem("-"))
                        if(self.result1.table2_plus[i][0] != -1):
                            self.tableWidget_2.setItem(i+1, 2, QTableWidgetItem(str(round(self.result1.table2_plus[i][alt_scen],2))))
                        else:
                            self.tableWidget_2.setItem(i+1, 2, QTableWidgetItem("-"))
                        item = self.tableWidget_2.item(i+1, 1)
                        item.setTextAlignment(Qt.AlignCenter)
                        item = self.tableWidget_2.item(i+1, 2)
                        item.setTextAlignment(Qt.AlignCenter)

                elif(self.paramPage.comboBox_4.currentText() == "negative"):
                     for i in range(self.result1.table2_minus.shape[0]):
                        if(self.result1.table2_nom[i][0] != -1):
                            self.tableWidget_2.setItem(i+1, 1, QTableWidgetItem(str(round(self.result1.table2_nom[i][alt_scen],2))))
                        else:
                            self.tableWidget_2.setItem(i+1, 1, QTableWidgetItem("-"))
                        if(self.result1.table2_minus[i][0] != -1):
                            self.tableWidget_2.setItem(i+1, 2, QTableWidgetItem(str(round(self.result1.table2_minus[i][alt_scen],2))))
                        else:
                            self.tableWidget_2.setItem(i+1, 2, QTableWidgetItem("-"))
                        item = self.tableWidget_2.item(i+1, 1)
                        item.setTextAlignment(Qt.AlignCenter)
                        item = self.tableWidget_2.item(i+1, 2)
                        item.setTextAlignment(Qt.AlignCenter)
                else:
                 pass

                

                


            else:
                #Tablica costova
                for i in range(self.result1.table.shape[0]):
                    if(self.result1.table[i][0] != -1):
                        self.tableWidget.setItem(i+1, 1, QTableWidgetItem(str(round(self.result1.table[i][0],2))))
                    else:
                        self.tableWidget.setItem(i+1, 1, QTableWidgetItem("-"))
                    item = self.tableWidget.item(i+1, 1)
                    item.setTextAlignment(Qt.AlignCenter)

                #Tablica energija
                for i in range(self.result1.table2.shape[0]):
                    if(self.result1.table2[i][0] != -1):
                        self.tableWidget_2.setItem(i+1, 1, QTableWidgetItem(str(round(self.result1.table2[i][0],2))))
                    else:
                        self.tableWidget_2.setItem(i+1, 1, QTableWidgetItem("-"))
                    item = self.tableWidget_2.item(i+1, 1)
                    item.setTextAlignment(Qt.AlignCenter)

                
                
                    
        if(self.result2):
            #Tablica costova
            if self.tableWidget.columnCount() == 5:       
                for i in range(self.result2.table.shape[0]):
                    if(self.result2.table[i][0] != -1):
                        self.tableWidget.setItem(i+1, 4, QTableWidgetItem(str(round(self.result2.table[i][0],2))))
                    else:
                        self.tableWidget.setItem(i+1, 4, QTableWidgetItem("-"))
                    item = self.tableWidget.item(i+1, 4)
                    item.setTextAlignment(Qt.AlignCenter)

            elif self.tableWidget.columnCount() == 3:
                 for i in range(self.result2.table.shape[0]):
                    if(self.result2.table[i][0] != -1):
                        self.tableWidget.setItem(i+1, 2, QTableWidgetItem(str(round(self.result2.table[i][0],2))))
                    else:
                        self.tableWidget.setItem(i+1, 2, QTableWidgetItem("-"))
                    item = self.tableWidget.item(i+1, 2)
                    item.setTextAlignment(Qt.AlignCenter)
            else:
                 pass

            


            #Tablica energija
            if self.tableWidget_2.columnCount() == 5:       
                for i in range(self.result2.table2.shape[0]):
                    if(self.result2.table2[i][0] != -1):
                        self.tableWidget_2.setItem(i+1, 4, QTableWidgetItem(str(round(self.result2.table2[i][0],2))))
                    else:
                        self.tableWidget_2.setItem(i+1, 4, QTableWidgetItem("-"))
                    item = self.tableWidget_2.item(i+1, 4)
                    item.setTextAlignment(Qt.AlignCenter)

            elif self.tableWidget_2.columnCount() == 3:
                 for i in range(self.result2.table2.shape[0]):
                    if(self.result2.table2[i][0] != -1):
                        self.tableWidget_2.setItem(i+1, 2, QTableWidgetItem(str(round(self.result2.table2[i][0],2))))
                    else:
                        self.tableWidget_2.setItem(i+1, 2, QTableWidgetItem("-"))
                    item = self.tableWidget_2.item(i+1, 2)
                    item.setTextAlignment(Qt.AlignCenter)
            else:
                 pass

            

        
        
    def getResults(self):
        self.result1 = self.resultPage.result1
        self.getParams()
        if(self.resultPage.result2):
            self.result2 = self.resultPage.result2
        
    def update_combo_table(self):
        self.update_table_flex()
        if self.flex == True:
            self.comboBox.setEnabled(True)
            self.comboBox.clear()
            self.comboBox.blockSignals(True)
            for i in range(self.data.n_a):
                if(self.result1 and i == self.result1.worst_ind):
                    self.comboBox.addItem(f"Alternative profile {i+1} (WORST)")
                else:
                    self.comboBox.addItem(f"Alternative profile {i+1}")
        else:   
            self.comboBox.setEnabled(False)
            self.comboBox.clear()
        self.comboBox.blockSignals(False)
        print("Table update...")
        
    def getParams(self):
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
            sgn_Pr=params[17],
            hub_name = params[18],
            annual_load = params[19],
            annual_water = params[20]
        )

