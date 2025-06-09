from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QLabel,
    QWidget,
    QLineEdit,
    QSlider,
    QVBoxLayout
)
from MILP_GUI.ParamWidget import Ui_ParamWidget

class ParamPage(QWidget, Ui_ParamWidget):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


        #POSTAVLJANJE DEFAULT VRIJEDNOSTI QSLIDERA I QLINEEDITA
        self.scenarij1 = str()
        self.scenarij2 = str()

        self.lineEdit_9.setText(str(self.horizontalSlider_2.value()))
        self.lineEdit.setText(str(self.horizontalSlider.value()))
        self.lineEdit_2.setText(str(self.horizontalSlider_3.value()))
        self.lineEdit_3.setText(str(self.horizontalSlider_4.value()))
        self.lineEdit_4.setText(str(self.horizontalSlider_5.value()))
        self.lineEdit_10.setText(str(self.horizontalSlider_7.value()))
        self.lineEdit_11.setText(str(self.horizontalSlider_8.value()))

        self.lineEdit_6.setText(str(0.07)) #kupovna cijena elektricne energije
        self.lineEdit_7.setText(str(0.035))#prodajna cijena elektricne energije
        self.lineEdit_8.setText(str(3.05)) #cijena vrsne snage
        self.lineEdit_12.setText(str(410)) #snaga solarnog panela (Wp)
        self.comboBox.setCurrentText(str(24))

        self.radioButton.setChecked(True)
        self.comboBox_2.setCurrentIndex(1)
        self.comboBox_3.setCurrentIndex(3)

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
        print(self.comboBox_2.isEnabled())
        print(self.comboBox_3.isEnabled())
        if self.radioButton_2.isChecked():
            self.comboBox_3.setEnabled(False)
            self.comboBox_3.setVisible(False)
            self.label_10.setVisible(False)
            self.label_9.setText("Odaberite model")
            try:
                self.comboBox_2.removeItem(2)
            except:
                print("Greška s micanjem histereze")
            
        self.radioButton.toggled.connect(self.changeComboBox)
        self.radioButton_2.toggled.connect(self.changeComboBox)
        self.comboBox_2.currentIndexChanged.connect(self.changeComboBox)


    
    def update_slider_value(self, value, lineEdit):
        lineEdit.setText(str(value))

    def changeComboBox(self):
        print(self.comboBox_2.currentIndex())
        print(self.comboBox_2.isEnabled())
        print(self.comboBox_3.isEnabled())
        if self.radioButton.isChecked():
            self.comboBox_3.setEnabled(True)
            self.comboBox_3.setVisible(True)
            self.label_10.setVisible(True)
            self.label_9.setText("Prvi model")
            self.widget_4.setEnabled(True)
            self.widget_5.setEnabled(True)
            
        else:
            self.comboBox_3.setEnabled(False)
            self.comboBox_3.setVisible(False)
            self.label_10.setVisible(False)
            self.label_9.setText("Odaberite model")
            if self.comboBox_2.currentIndex() == 1: 
                self.widget_4.setEnabled(False)
                self.widget_5.setEnabled(False)
            elif self.comboBox_2.currentIndex() == 0:
                self.widget_4.setEnabled(True)
                self.widget_5.setEnabled(True)

           

    def flexibilityParams(self):
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