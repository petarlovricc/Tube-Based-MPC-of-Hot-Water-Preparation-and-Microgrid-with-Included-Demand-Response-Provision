from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QLabel,
    QWidget,
    QLineEdit,
    QSlider,
    QVBoxLayout,
    QMainWindow
)
 
from MILP_GUI.ParamWidget import Ui_ParamWidget

class ParamPage(QWidget, Ui_ParamWidget):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        #POSTAVLJANJE DEFAULT VRIJEDNOSTI QSLIDERA I QLINEEDITA
        self.scenarij1 = str()
        self.scenarij2 = str()

        self.heater = ""

        self.lineEdit_9.setText(str(self.horizontalSlider_2.value()))
        self.lineEdit.setText(str(self.horizontalSlider.value()))
        self.lineEdit_2.setText(str(self.horizontalSlider_3.value()))
        self.lineEdit_3.setText(str(self.horizontalSlider_4.value()))
        self.lineEdit_4.setText(str(self.horizontalSlider_5.value()))
        self.lineEdit_10.setText(str(self.horizontalSlider_7.value()))
        self.lineEdit_11.setText(str(self.horizontalSlider_8.value()))

        self.lineEdit_6.setText(str(0.18)) #kupovna cijena elektricne energije
        self.lineEdit_7.setText(str(0.09))#prodajna cijena elektricne energije
        self.lineEdit_8.setText(str(3.64)) #cijena vrsne snage
        self.lineEdit_12.setText(str(410)) #snaga solarnog panela (Wp)
        self.comboBox.setCurrentText(str(24)) #Q
        self.radioButton.setChecked(True)

        self.lineEdit_13.setText(str(0.7)) #cr
        self.lineEdit_15.setText(str(float(self.lineEdit_6.text())*1.2)) #cid
        self.lineEdit_14.setText(str(0.8)) #alfa



        self.radioButton_3.setChecked(True)
        

        #UPDATEANJE VRIJEDNOSTI QSLIDERA I QLINEEDITA
        self.flexibilityParams()
        self.horizontalSlider_7.valueChanged.connect(self.flexibilityParams)
        self.horizontalSlider_8.valueChanged.connect(self.flexibilityParams)
        self.comboBox.currentTextChanged.connect(self.flexibilityParams)

        self.horizontalSlider_2.valueChanged.connect(
            lambda value: self.update_slider_value(value, self.lineEdit_9)
        )
        self.horizontalSlider.valueChanged.connect(
            lambda value: self.update_slider_value(value, self.lineEdit)
        )
        self.horizontalSlider_3.valueChanged.connect(
            lambda value: self.update_slider_value(value, self.lineEdit_2)
        )
        self.horizontalSlider_4.valueChanged.connect(
            lambda value: self.update_slider_value(value, self.lineEdit_3)
        ) 
        self.horizontalSlider_5.valueChanged.connect(
            lambda value: self.update_slider_value(value, self.lineEdit_4)
        )
        self.horizontalSlider_7.valueChanged.connect(
            lambda value: self.update_slider_value(value, self.lineEdit_10)
        )
        self.horizontalSlider_8.valueChanged.connect(
            lambda value: self.update_slider_value(value, self.lineEdit_11)
        )        

        #RADI LI SE O USPOREDBI ILI POKRETANJU SAMO JEDNOG MODELA
        if self.radioButton_2.isChecked():
            self.comboBox_3.setEnabled(False)
            self.comboBox_3.setVisible(False)
            self.label_10.setVisible(False)
            self.label_9.setText("Odaberite model")
            
        self.radioButton.toggled.connect(self.changeComboBox)

        self.radioButton_2.toggled.connect(self.changeComboBox)
        self.comboBox_2.currentIndexChanged.connect(self.changeComboBox)

        self.radioButton_3.toggled.connect(self.setHeater)
        self.radioButton_4.toggled.connect(self.setHeater)

        self.setHeater()

        self.radioButton.toggled.connect(self.noOfModels)

    def setHeater(self):
        print(self.heater)
        if(self.radioButton_3.isChecked()):
            self.heater = "C"
        elif(self.radioButton_4.isChecked()):
            self.heater = "I"
        

    def noOfModels(self):
        if (self.radioButton.isChecked()):
            self.twoModels = True
        else:
            self.twoModels = False
        print(self.twoModels)
        
    
    def update_slider_value(self, value, lineEdit):
        lineEdit.setText(str(value))

    def changeComboBox(self):
        if self.radioButton.isChecked():
            self.comboBox_3.setEnabled(True)
            self.comboBox_3.setVisible(True)
            self.label_10.setVisible(True)
            self.label_9.setText("Prvi model")
            self.widget_4.setEnabled(True)
            self.widget_5.setEnabled(True)
            self.widget_6.setEnabled(True)
            self.label_8.setText("Dani u godini (Model 1 i Model 2)")
            
        else:
            self.comboBox_3.setEnabled(False)
            self.comboBox_3.setVisible(False)
            self.label_10.setVisible(False)
            self.label_9.setText("Odaberite model")
            self.label_8.setText("Dan u godini")

        if self.comboBox_2.currentIndex() == 1:  #bez odziva potrošnje, disableaj widgete za odabir parametara flex
            self.widget_4.setEnabled(False)
            self.widget_5.setEnabled(False)
            self.widget_6.setEnabled(False)

        elif self.comboBox_2.currentIndex() == 0: #s odzivom potrošnje, enableaj widgete za odabir parametara flex
            self.widget_4.setEnabled(True)
            self.widget_5.setEnabled(True)
            self.widget_6.setEnabled(True)

           

    def flexibilityParams(self):
        hours_beg = self.timeEdit_2.time().hour()
        minutes_beg = self.timeEdit_2.time().minute()
        time_beg = hours_beg + minutes_beg/60  
        #beginning_flex_ready

        hours_end = self.timeEdit.time().hour()
        minutes_end = self.timeEdit.time().minute()
        time_end = hours_end + minutes_end/60 
        #end_flex_ready

        self.horizontalSlider_7.setMaximum(int(self.comboBox.currentText())-1)
        self.horizontalSlider_8.setMaximum(int(self.comboBox.currentText())-self.horizontalSlider_7.value())

    def getParams(self):
        params = []
        params.append(self.horizontalSlider_4.value()) #heater power
        params.append(self.horizontalSlider.value()) #Ebatmax
        params.append(self.horizontalSlider_3.value()) #converter power
        params.append(self.horizontalSlider_2.value()) #tank volume
        params.append(int(self.lineEdit_12.text())) #PV power
        params.append(self.horizontalSlider_5.value()) #numberofPV
        params.append(float(self.lineEdit_6.text())) #buyPriceHigh
        params.append(float(self.lineEdit_7.text())) #buyPriceLow
        params.append(self.dateEdit.date().month()) #month
        params.append(self.dateEdit.date().day()) #day
        params.append(float(self.lineEdit_8.text())) #peak power
        

        return params
    

     


    #def setOptimTypes(self):
    #    if()

    def get_flexParams(self):
        params = []
        params.append(self.horizontalSlider_4.value()) #heater power
        params.append(self.horizontalSlider.value()) #Ebatmax
        params.append(self.horizontalSlider_3.value()) #converter power
        params.append(self.horizontalSlider_2.value()) #tank volume
        params.append(int(self.lineEdit_12.text())) #PV power
        params.append(self.horizontalSlider_5.value()) #numberofPV
        params.append(float(self.lineEdit_6.text())) #buyPriceHigh
        params.append(float(self.lineEdit_7.text())) #buyPriceLow
        params.append(self.dateEdit.date().month()) #month
        params.append(self.dateEdit.date().day()) #day

        params.append(float(self.lineEdit_8.text())) #peak power
        params.append(int(self.comboBox.currentText())) #Q
        params.append(self.horizontalSlider_7.value()) #F
        params.append(self.horizontalSlider_8.value()) #R
        
        hours_beg = self.timeEdit_2.time().hour()
        minutes_beg = self.timeEdit_2.time().minute()
        time_beg = hours_beg + minutes_beg/60  
        

        hours_end = self.timeEdit.time().hour()
        minutes_end = self.timeEdit.time().minute()
        time_end = hours_end + minutes_end/60 
        
        if(hours_end == 23 and minutes_end == 59):
            time_end = 24
            
        params.append(time_beg) #beginning_flex_ready
        params.append(time_end) #end_flex_ready


        
        params.append(float(self.lineEdit_14.text())) #alfa
        params.append(float(self.lineEdit_13.text())) #cr

        
        if (self.comboBox_4.currentIndex() == 0):
            params.append(1) #sgnPr

        elif(self.comboBox_4.currentIndex() == 1):
            params.append(-1) #sgnPr

        else:
            params.append(None) #sgnPr

        
        params.append(float(self.lineEdit_15.text())) #cid

       
        return params



        