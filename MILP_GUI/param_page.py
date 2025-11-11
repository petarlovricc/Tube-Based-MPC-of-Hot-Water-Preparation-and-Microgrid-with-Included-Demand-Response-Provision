from PySide6.QtWidgets import (
    QWidget,
    QSizePolicy,
    QLabel
)
from PySide6.QtGui import QResizeEvent, QFont, QShowEvent
from PySide6.QtCore import Qt
from MILP_GUI.ParamWidget import Ui_ParamWidget
from PySide6.QtCore import QDateTime, QTime, QDate
from PySide6.QtGui import QPixmap, Qt
from PySide6.QtSvgWidgets import QSvgWidget
from MILP_GUI import resources_rc
from Parameters.getData_flex import getData as DataGetter


class ParamPage(QWidget, Ui_ParamWidget):
    def __init__(self):
        
        
        super().__init__()
        self.setupUi(self)
        

        # POSTAVLJANJE DEFAULT VRIJEDNOSTI QSLIDERA I QLINEEDITA
        self.status_msg = ""
        self.scenarij1 = str()
        self.scenarij2 = str()
        self.heater = ""
        self.hub_name = None
        self.radioButton.setChecked(True)
        self.radioButton_9.setChecked(True)
        self.lineEdit_13.setText(str(0.7))  # cr+
        self.lineEdit_14.setText(str(90))  # alfa+
        self.lineEdit_5.setText(str(0.7))  # cr-
        self.lineEdit_6.setText(str(80))  # alfa-
        self.radioButton_3.setChecked(True)
        self.comboBox_2.setCurrentIndex(0)
        self.comboBox_3.setCurrentIndex(0)
        self.comboBox_4.setCurrentIndex(2)
        self.timeEdit.setTime(QTime(23, 59))
        self.timeEdit_2.setTime(QTime(0, 0))
        self.label_11.setText("Water tank capacity (m<sup>3</sup>)")
        self.label_12.setText("Annual tempered water consumption (m<sup>3</sup>)")

        # UPDATEANJE VRIJEDNOSTI QSLIDERA I QLINEEDITA
        self.flexibilityParams()
        self.spinBox_2.valueChanged.connect(self.flexibilityParams)
        self.spinBox.valueChanged.connect(self.flexibilityParams)
        self.comboBox.currentTextChanged.connect(self.flexibilityParams)
        
        # RADI LI SE O USPOREDBI ILI POKRETANJU SAMO JEDNOG MODELA
        if self.radioButton_2.isChecked():
            self.comboBox_3.setEnabled(False)
            self.comboBox_3.setVisible(False)

        self.radioButton.toggled.connect(self.changeComboBox)
        self.radioButton_2.toggled.connect(self.changeComboBox)
        self.comboBox_2.currentIndexChanged.connect(self.changeComboBox)
        self.radioButton_3.toggled.connect(self.setHeater)
        self.radioButton_4.toggled.connect(self.setHeater)
        self.radioButton_7.toggled.connect(self._get_hubname)
        self.radioButton_8.toggled.connect(self._get_hubname)
        self.radioButton_9.toggled.connect(self._get_hubname)
        self.radioButton_10.toggled.connect(self._get_hubname)
        self.setHeater()
        self._get_hubname()
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
            if(widget.objectName() == "label_11" or widget.objectName() == "label_12"):
                self.label_11.setTextFormat(Qt.RichText)
                self.label_11.setText(f'<span style="font-size:{int(font.pointSize())}pt">Water tank capacity (m<sup>3</sup>)</span>')

                self.label_12.setTextFormat(Qt.RichText)
                self.label_12.setText(f'<span style="font-size:{int(font.pointSize())}pt">Annual tempered water consumption (m<sup>3</sup>)</span>')
            else:      
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
        self.groupBox_4.setFont(font2)
        

    def _get_hubname(self):
        # Household hub
        if self.radioButton_9.isChecked():
            self.hub_name = "Household"
            # System parameters
            self.lineEdit_9.setText("0.2")     # Water tank capacity (m3)
            self.lineEdit.setText("10")       # Battery capacity (kWh)
            self.lineEdit_2.setText("2.5")      # Inverter power (kW)
            self.lineEdit_3.setText("2.5")    # Water heater power (kW)
            self.lineEdit_4.setText("10")     # Number of solar panels
            self.lineEdit_12.setText("400")   # Solar panel power (Wp)
            # Annual consumptions
            self.lineEdit_7.setText("5")    # Annual electricity consumption (MWh)
            self.lineEdit_8.setText("50")     # Annual water consumption (m3)

            self.timeEdit.setTime(QTime(12,0)) #endTime
            self.comboBox.setCurrentIndex(4) #Q = 12
            self.dateEdit.setDate(QDate(2024,2,25))

        # Industry hub
        elif self.radioButton_7.isChecked():
            self.hub_name = "Industry"
            # System parameters
            self.lineEdit_9.setText("5")       # Water tank capacity (m3)
            self.lineEdit.setText("500")      # Battery capacity (kWh)
            self.lineEdit_2.setText("250")    # Inverter power (kW)
            self.lineEdit_3.setText("50")    # Water heater power (kW)
            self.lineEdit_4.setText("2000")   # Number of solar panels
            self.lineEdit_12.setText("400")   # Solar panel power (Wp)
            # Annual consumptions
            self.lineEdit_7.setText("4000")   # Annual electricity consumption (MWh)
            self.lineEdit_8.setText("3000")  # Annual water consumption (m3)
            self.timeEdit.setTime(QTime(12,0)) #endTime
            self.comboBox.setCurrentIndex(4) #Q = 12
            self.dateEdit.setDate(QDate(2024,2,25))
            self.lineEdit_13.setText(str(0.7))  # cr+
            self.lineEdit_5.setText(str(0.7))  # cr-



        # Commercial hub (shopping mall)
        elif self.radioButton_10.isChecked():
            self.hub_name = "Commercial"
            # System parameters
            self.lineEdit_9.setText("100")      # Water tank capacity (m3)
            self.lineEdit.setText("500")      # Battery capacity (kWh)
            self.lineEdit_2.setText("300")   # Inverter power (kW)
            self.lineEdit_3.setText("500")    # Water heater power (kW)
            self.lineEdit_4.setText("2000")   # Number of solar panels
            self.lineEdit_12.setText("400")   # Solar panel power (Wp)
            # Annual consumptions
            self.lineEdit_7.setText("8750")   # Annual electricity consumption (MWh)
            self.lineEdit_8.setText("10000")  # Annual water consumption (m3)

            self.timeEdit.setTime(QTime(12,0)) #endTime
            self.comboBox.setCurrentIndex(4) #Q = 12
            self.dateEdit.setDate(QDate(2024,2,25))

        # Power-2-X hub
        elif self.radioButton_8.isChecked():
            self.hub_name = "Power-2-X"
            # System parameters
            self.lineEdit_9.setText("1")      # Water tank capacity (m3)
            self.lineEdit.setText("8000")     # Battery capacity (kWh)
            self.lineEdit_2.setText("2500")   # Inverter power (kW)
            self.lineEdit_3.setText("100")    # Water heater power (kW)
            self.lineEdit_4.setText("27500")  # Number of solar panels
            self.lineEdit_12.setText("400")   # Solar panel power (Wp)
            # Annual consumptions
            self.lineEdit_7.setText("80000")  # Annual electricity consumption (MWh)
            self.lineEdit_8.setText("1000")   # Annual water consumption (m3)

            self.timeEdit.setTime(QTime(12,0)) #endTime
            self.comboBox.setCurrentIndex(4) #Q = 12
            self.dateEdit.setDate(QDate(2024,2,25))

            self.lineEdit_13.setText(str(0.7))  # cr+
            self.lineEdit_5.setText(str(0.7))  # cr-
            
        


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
            params.append(float(self.lineEdit_3.text()))  # heater power
            params.append(float(self.lineEdit.text()))  # Ebatmax
            params.append(float(self.lineEdit_2.text()))  # converter power
            params.append(float(self.lineEdit_9.text()))  # tank volume
            params.append(float(self.lineEdit_12.text()))  # PV power
            params.append(float(self.lineEdit_4.text()))  # numberofPV
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
            params.append(self.hub_name)
            params.append(float(self.lineEdit_7.text()))
            params.append(float(self.lineEdit_8.text()))
           
            
        except ValueError:
            raise TypeError("Only integers and floats are allowed!")
      
        return params


class ParameterTooSmallError(Exception):
    
    pass