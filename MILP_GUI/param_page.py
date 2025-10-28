from PySide6.QtWidgets import (
    QWidget,
    QSizePolicy
)
from PySide6.QtGui import QResizeEvent, QFont, QShowEvent
from PySide6.QtCore import Qt
from MILP_GUI.ParamWidget import Ui_ParamWidget
from PySide6.QtCore import QDateTime, QTime
from PySide6.QtGui import QPixmap, Qt
from PySide6.QtSvgWidgets import QSvgWidget
from MILP_GUI import resources_rc


class ParamPage(QWidget, Ui_ParamWidget):
    def __init__(self):
        
        
        super().__init__()
        self.setupUi(self)
        

        # POSTAVLJANJE DEFAULT VRIJEDNOSTI QSLIDERA I QLINEEDITA
        self.status_msg = ""
        self.scenarij1 = str()
        self.scenarij2 = str()
        self.heater = ""
        self.lineEdit_9.setText(str(self.horizontalSlider_2.value())) #Water tank capacity (L)
        self.lineEdit.setText(str(self.horizontalSlider.value())) #Battery capacity (Wh)
        self.lineEdit_2.setText(str(self.horizontalSlider_3.value())) #Inverter power (W)
        self.lineEdit_3.setText(str(self.horizontalSlider_4.value())) #Water heater power (W)
        self.lineEdit_4.setText(str(self.horizontalSlider_5.value())) #Number of solar panels
        self.lineEdit_12.setText(str(self.horizontalSlider_6.value())) #Solar panel power (Wp)
        self.lineEdit_7.setText(str(self.horizontalSlider_7.value())) #Water temperature setpoint (°C)
        self.comboBox.setCurrentText(str(12))  # Q
        self.radioButton.setChecked(True)
        self.radioButton_6.setChecked(True)
        self.lineEdit_13.setText(str(0.1))  # cr+
        self.lineEdit_14.setText(str(90))  # alfa+
        self.lineEdit_5.setText(str(0.1))  # cr-
        self.lineEdit_6.setText(str(80))  # alfa-
        self.radioButton_3.setChecked(True)
        self.comboBox_2.setCurrentIndex(0)
        self.comboBox_3.setCurrentIndex(0)
        self.comboBox_4.setCurrentIndex(2)

        # UPDATEANJE VRIJEDNOSTI QSLIDERA I QLINEEDITA
        self.flexibilityParams()
        self.spinBox_2.valueChanged.connect(self.flexibilityParams)
        self.spinBox.valueChanged.connect(self.flexibilityParams)
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
        self.horizontalSlider_6.valueChanged.connect(
            lambda value: self.update_slider_value(value, self.lineEdit_12)
        )
        self.horizontalSlider_7.valueChanged.connect(
            lambda value: self.update_slider_value(value, self.lineEdit_7)
        )
        # RADI LI SE O USPOREDBI ILI POKRETANJU SAMO JEDNOG MODELA
        if self.radioButton_2.isChecked():
            self.comboBox_3.setEnabled(False)
            self.comboBox_3.setVisible(False)

        self.radioButton.toggled.connect(self.changeComboBox)
        self.radioButton_2.toggled.connect(self.changeComboBox)
        self.comboBox_2.currentIndexChanged.connect(self.changeComboBox)
        self.radioButton_3.toggled.connect(self.setHeater)
        self.radioButton_4.toggled.connect(self.setHeater)
        self.setHeater()
        self.radioButton.toggled.connect(self.noOfModels)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # self.timeEdit_2.timeChanged.connect(self.checkFlexTime)
        # self.timeEdit.timeChanged.connect(self.checkFlexTime)
        self.ferLogo = QSvgWidget(":/icons/FER_logo_2.svg")
        self.laresLogo = QSvgWidget(":/icons/LARES_2_transparent_white.svg")



    # def checkFlexTime(self):
    #      if (self.timeEdit_2.time().hour()*60 + self.timeEdit_2.time().minute() >=  self.timeEdit.time().hour()*60 + self.timeEdit.time().minute()):
    #           if(self.timeEdit.time().hour() == self.timeEdit_2.time().hour() and self.timeEdit.time().minute() == 0):
    #             self.timeEdit_2.setTime(QTime(self.timeEdit.time().hour()-1, (self.timeEdit.time().minute()-15)%60, 0))
    #           else:
    #             self.timeEdit_2.setTime(QTime(self.timeEdit.time().hour(), (self.timeEdit.time().minute()-15)%60, 0))
                   
                   

    def loop_through_widgets(self, font):
        for widget in self.findChildren(QWidget):
            widget.setFont(font)


        buttonfont = self.pushButton.font()
        buttonfont.setPointSize(font.pointSize()*1.2)
        self.pushButton.setFont(buttonfont)
        self.pushButton_2.setFont(buttonfont)
        

        font = self.title1.font()
        font.setPointSize(font.pointSize()*1.2)
        font.setBold(True)
        self.title1.setFont(font)
        self.title4.setFont(font)
        font2 = self.groupBox.font()
        font2.setBold(True)
        self.groupBox.setFont(font2)
        self.groupBox_2.setFont(font2)
        self.groupBox_3.setFont(font2)

   

    def resizeEvent(self, event: QResizeEvent):
                super().resizeEvent(event)
                #self.update_logos()
                # Heuristic: base size on window height
                h = self.height()
                new_pt = max(9, h / 60)  # adjust divisor as needed
                font = self.font()
                font.setPointSizeF(new_pt)
                self.loop_through_widgets(font)


    def showEvent(self, event: QShowEvent):
                super().showEvent(event)
                
                # Heuristic: base size on window height
                h = self.height()
                new_pt = max(9, h / 60)  # adjust divisor as needed
                font = self.font()
                font.setPointSizeF(new_pt)
                self.loop_through_widgets(font)
                


    def setHeater(self):
        if self.radioButton_3.isChecked():
            self.heater = "C"
        elif self.radioButton_4.isChecked():
            self.heater = "I"

    def noOfModels(self):
        self.twoModels = self.radioButton.isChecked()

    def update_slider_value(self, value, lineEdit):
        lineEdit.setText(str(value))

    def changeComboBox(self):
        if self.radioButton.isChecked():
            self.comboBox_3.setEnabled(True)
            self.comboBox_3.setVisible(True)
            self.widget_4.setEnabled(True)
           
        else:
            self.comboBox_3.setEnabled(False)
            self.comboBox_3.setVisible(False)

        if self.comboBox_2.currentIndex() == 1:  # bez odziva potrošnje
            self.widget_4.setEnabled(False)
            
        elif self.comboBox_2.currentIndex() == 0:  # s odzivom potrošnje
            self.widget_4.setEnabled(True)
           
    def flexibilityParams(self):
        hours_beg = self.timeEdit_2.time().hour()
        minutes_beg = self.timeEdit_2.time().minute()
        time_beg = hours_beg + minutes_beg / 60

        hours_end = self.timeEdit.time().hour()
        minutes_end = self.timeEdit.time().minute()
        time_end = hours_end + minutes_end / 60

        self.spinBox_2.setMaximum(int(self.comboBox.currentText()) - 1)
        self.spinBox.setMaximum(
            int(self.comboBox.currentText()) - self.spinBox_2.value()
        )

    def getParams(self):
        params = []
        try:
            params.append(self.horizontalSlider_4.value())  # heater power
            params.append(self.horizontalSlider.value())  # Ebatmax
            params.append(self.horizontalSlider_3.value())  # converter power
            params.append(self.horizontalSlider_2.value())  # tank volume
            params.append(self.horizontalSlider_6.value())  # PV power
            params.append(self.horizontalSlider_5.value())  # numberofPV
            params.append(self.dateEdit.date().month())  # month
            params.append(self.dateEdit.date().day())  # day
            params.append(int(self.comboBox.currentText()))  # Q
            params.append(self.spinBox_2.value())  # F
            params.append(self.spinBox.value())  # R

            hours_beg = self.timeEdit_2.time().hour()
            minutes_beg = self.timeEdit_2.time().minute()
            time_beg = hours_beg + minutes_beg / 60

            hours_end = self.timeEdit.time().hour()
            minutes_end = self.timeEdit.time().minute()
            time_end = hours_end + minutes_end / 60

            if hours_end == 23 and minutes_end == 59:
                time_end = 24

            params.append(time_beg)  # beginning_flex_ready
            params.append(time_end)  # end_flex_ready
            if (time_end - time_beg < 0.25):
                 raise ParameterTooSmallError(f"Please enter a larger end time!")

            params.append(float(self.lineEdit_14.text()))  # alfa+
            params.append(float(self.lineEdit_6.text()))  # alfa-
            params.append(float(self.lineEdit_13.text()))  # cr
            params.append(float(self.lineEdit_5.text()))  # cr

            
            params.append(self.comboBox_4.currentText())
            params.append(self.horizontalSlider_7.value()) 
            
        except ValueError:
            raise TypeError("Only integers and floats are allowed!")
      
        return params


class ParameterTooSmallError(Exception):
    
    pass