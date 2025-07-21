# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'paramwidget.ui'
##
## Created by: Qt User Interface Compiler version 6.9.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QDateEdit, QGridLayout,
    QGroupBox, QLabel, QLayout, QLineEdit,
    QPushButton, QRadioButton, QSizePolicy, QSlider,
    QTimeEdit, QWidget)

class Ui_ParamWidget(object):
    def setupUi(self, ParamWidget):
        if not ParamWidget.objectName():
            ParamWidget.setObjectName(u"ParamWidget")
        ParamWidget.resize(1723, 650)
        ParamWidget.setMinimumSize(QSize(1000, 600))
        ParamWidget.setAutoFillBackground(False)
        ParamWidget.setStyleSheet(u"#ParamWidget{\n"
"background-color: white;\n"
"}\n"
"")
        self.gridLayout_8 = QGridLayout(ParamWidget)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.widget_4 = QWidget(ParamWidget)
        self.widget_4.setObjectName(u"widget_4")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_4.sizePolicy().hasHeightForWidth())
        self.widget_4.setSizePolicy(sizePolicy)
        self.widget_4.setStyleSheet(u"QWidget #widget_4 {\n"
"	background-color: rgba(245, 245, 245, 0.9);\n"
"	border-radius: 8px;\n"
"	border-style:dotted;\n"
"}\n"
"")
        self.gridLayout_6 = QGridLayout(self.widget_4)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.label_13 = QLabel(self.widget_4)
        self.label_13.setObjectName(u"label_13")
        font = QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.label_13.setFont(font)
        self.label_13.setAlignment(Qt.AlignCenter)

        self.gridLayout_6.addWidget(self.label_13, 0, 0, 1, 1)

        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setVerticalSpacing(25)
        self.label_14 = QLabel(self.widget_4)
        self.label_14.setObjectName(u"label_14")

        self.gridLayout_3.addWidget(self.label_14, 0, 0, 1, 1)

        self.label_15 = QLabel(self.widget_4)
        self.label_15.setObjectName(u"label_15")

        self.gridLayout_3.addWidget(self.label_15, 1, 0, 1, 1)

        self.timeEdit_2 = QTimeEdit(self.widget_4)
        self.timeEdit_2.setObjectName(u"timeEdit_2")
        self.timeEdit_2.setTime(QTime(11, 0, 0))

        self.gridLayout_3.addWidget(self.timeEdit_2, 0, 1, 1, 1)

        self.timeEdit = QTimeEdit(self.widget_4)
        self.timeEdit.setObjectName(u"timeEdit")
        self.timeEdit.setTime(QTime(12, 0, 0))

        self.gridLayout_3.addWidget(self.timeEdit, 1, 1, 1, 1)


        self.gridLayout_6.addLayout(self.gridLayout_3, 1, 0, 1, 1)


        self.gridLayout_8.addWidget(self.widget_4, 2, 1, 2, 1)

        self.widget_6 = QWidget(ParamWidget)
        self.widget_6.setObjectName(u"widget_6")
        self.widget_6.setStyleSheet(u"QWidget #widget_6 {\n"
"	background-color: rgba(245, 245, 245, 0.9);\n"
"	border-radius: 8px;\n"
"	border-style:dotted;\n"
"}\n"
"")
        self.gridLayout_7 = QGridLayout(self.widget_6)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.gridLayout_7.setVerticalSpacing(10)
        self.comboBox_4 = QComboBox(self.widget_6)
        self.comboBox_4.addItem("")
        self.comboBox_4.addItem("")
        self.comboBox_4.setObjectName(u"comboBox_4")

        self.gridLayout_7.addWidget(self.comboBox_4, 2, 1, 1, 1)

        self.label_21 = QLabel(self.widget_6)
        self.label_21.setObjectName(u"label_21")

        self.gridLayout_7.addWidget(self.label_21, 3, 0, 1, 1)

        self.lineEdit_13 = QLineEdit(self.widget_6)
        self.lineEdit_13.setObjectName(u"lineEdit_13")
        self.lineEdit_13.setAlignment(Qt.AlignCenter)

        self.gridLayout_7.addWidget(self.lineEdit_13, 3, 1, 1, 1)

        self.label_23 = QLabel(self.widget_6)
        self.label_23.setObjectName(u"label_23")

        self.gridLayout_7.addWidget(self.label_23, 4, 0, 1, 1)

        self.label_22 = QLabel(self.widget_6)
        self.label_22.setObjectName(u"label_22")

        self.gridLayout_7.addWidget(self.label_22, 5, 0, 1, 1)

        self.lineEdit_14 = QLineEdit(self.widget_6)
        self.lineEdit_14.setObjectName(u"lineEdit_14")
        self.lineEdit_14.setAlignment(Qt.AlignCenter)

        self.gridLayout_7.addWidget(self.lineEdit_14, 4, 1, 1, 1)

        self.lineEdit_15 = QLineEdit(self.widget_6)
        self.lineEdit_15.setObjectName(u"lineEdit_15")
        self.lineEdit_15.setAlignment(Qt.AlignCenter)

        self.gridLayout_7.addWidget(self.lineEdit_15, 5, 1, 1, 1)

        self.label_5 = QLabel(self.widget_6)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout_7.addWidget(self.label_5, 2, 0, 1, 1)

        self.label_25 = QLabel(self.widget_6)
        self.label_25.setObjectName(u"label_25")
        self.label_25.setFont(font)
        self.label_25.setAlignment(Qt.AlignCenter)

        self.gridLayout_7.addWidget(self.label_25, 1, 0, 1, 2)


        self.gridLayout_8.addWidget(self.widget_6, 4, 1, 2, 1)

        self.widget_3 = QWidget(ParamWidget)
        self.widget_3.setObjectName(u"widget_3")
        self.widget_3.setStyleSheet(u"QWidget #widget_3 {\n"
"	background-color: rgba(245, 245, 245, 0.9);\n"
"	border-radius: 8px;\n"
"}\n"
"")
        self.gridLayout = QGridLayout(self.widget_3)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setVerticalSpacing(10)
        self.lineEdit_3 = QLineEdit(self.widget_3)
        self.lineEdit_3.setObjectName(u"lineEdit_3")
        self.lineEdit_3.setAlignment(Qt.AlignCenter)
        self.lineEdit_3.setReadOnly(True)

        self.gridLayout.addWidget(self.lineEdit_3, 4, 2, 1, 1)

        self.label_4 = QLabel(self.widget_3)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout.addWidget(self.label_4, 5, 0, 1, 1)

        self.label_2 = QLabel(self.widget_3)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 3, 0, 1, 1)

        self.horizontalSlider_4 = QSlider(self.widget_3)
        self.horizontalSlider_4.setObjectName(u"horizontalSlider_4")
        self.horizontalSlider_4.setMinimum(1000)
        self.horizontalSlider_4.setMaximum(10000)
        self.horizontalSlider_4.setValue(2500)
        self.horizontalSlider_4.setOrientation(Qt.Horizontal)

        self.gridLayout.addWidget(self.horizontalSlider_4, 4, 1, 1, 1)

        self.lineEdit_12 = QLineEdit(self.widget_3)
        self.lineEdit_12.setObjectName(u"lineEdit_12")
        self.lineEdit_12.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit_12, 6, 1, 1, 1)

        self.lineEdit_9 = QLineEdit(self.widget_3)
        self.lineEdit_9.setObjectName(u"lineEdit_9")
        self.lineEdit_9.setAlignment(Qt.AlignCenter)
        self.lineEdit_9.setReadOnly(True)

        self.gridLayout.addWidget(self.lineEdit_9, 1, 2, 1, 1)

        self.label = QLabel(self.widget_3)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 2, 0, 1, 1)

        self.label_6 = QLabel(self.widget_3)
        self.label_6.setObjectName(u"label_6")
        font1 = QFont()
        self.label_6.setFont(font1)

        self.gridLayout.addWidget(self.label_6, 7, 0, 1, 1)

        self.lineEdit_8 = QLineEdit(self.widget_3)
        self.lineEdit_8.setObjectName(u"lineEdit_8")
        self.lineEdit_8.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit_8, 9, 1, 1, 1)

        self.horizontalSlider_5 = QSlider(self.widget_3)
        self.horizontalSlider_5.setObjectName(u"horizontalSlider_5")
        self.horizontalSlider_5.setMaximum(80)
        self.horizontalSlider_5.setValue(15)
        self.horizontalSlider_5.setOrientation(Qt.Horizontal)

        self.gridLayout.addWidget(self.horizontalSlider_5, 5, 1, 1, 1)

        self.horizontalSlider_3 = QSlider(self.widget_3)
        self.horizontalSlider_3.setObjectName(u"horizontalSlider_3")
        self.horizontalSlider_3.setMaximum(5000)
        self.horizontalSlider_3.setValue(2500)
        self.horizontalSlider_3.setOrientation(Qt.Horizontal)

        self.gridLayout.addWidget(self.horizontalSlider_3, 3, 1, 1, 1)

        self.lineEdit_4 = QLineEdit(self.widget_3)
        self.lineEdit_4.setObjectName(u"lineEdit_4")
        self.lineEdit_4.setAlignment(Qt.AlignCenter)
        self.lineEdit_4.setReadOnly(True)

        self.gridLayout.addWidget(self.lineEdit_4, 5, 2, 1, 1)

        self.label_12 = QLabel(self.widget_3)
        self.label_12.setObjectName(u"label_12")

        self.gridLayout.addWidget(self.label_12, 9, 0, 1, 1)

        self.horizontalSlider_2 = QSlider(self.widget_3)
        self.horizontalSlider_2.setObjectName(u"horizontalSlider_2")
        self.horizontalSlider_2.setMinimum(50)
        self.horizontalSlider_2.setMaximum(300)
        self.horizontalSlider_2.setValue(190)
        self.horizontalSlider_2.setOrientation(Qt.Horizontal)

        self.gridLayout.addWidget(self.horizontalSlider_2, 1, 1, 1, 1)

        self.label_8 = QLabel(self.widget_3)
        self.label_8.setObjectName(u"label_8")

        self.gridLayout.addWidget(self.label_8, 10, 0, 1, 1)

        self.lineEdit_2 = QLineEdit(self.widget_3)
        self.lineEdit_2.setObjectName(u"lineEdit_2")
        self.lineEdit_2.setAlignment(Qt.AlignCenter)
        self.lineEdit_2.setReadOnly(True)

        self.gridLayout.addWidget(self.lineEdit_2, 3, 2, 1, 1)

        self.label_7 = QLabel(self.widget_3)
        self.label_7.setObjectName(u"label_7")

        self.gridLayout.addWidget(self.label_7, 8, 0, 1, 1)

        self.lineEdit = QLineEdit(self.widget_3)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setAlignment(Qt.AlignCenter)
        self.lineEdit.setReadOnly(True)

        self.gridLayout.addWidget(self.lineEdit, 2, 2, 1, 1)

        self.dateEdit = QDateEdit(self.widget_3)
        self.dateEdit.setObjectName(u"dateEdit")
        self.dateEdit.setDateTime(QDateTime(QDate(2025, 6, 25), QTime(0, 0, 0)))
        self.dateEdit.setDate(QDate(2025, 6, 25))

        self.gridLayout.addWidget(self.dateEdit, 10, 1, 1, 1)

        self.label_20 = QLabel(self.widget_3)
        self.label_20.setObjectName(u"label_20")

        self.gridLayout.addWidget(self.label_20, 6, 0, 1, 1)

        self.label_24 = QLabel(self.widget_3)
        self.label_24.setObjectName(u"label_24")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label_24.sizePolicy().hasHeightForWidth())
        self.label_24.setSizePolicy(sizePolicy1)
        self.label_24.setFont(font)
        self.label_24.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_24, 0, 0, 1, 3)

        self.label_11 = QLabel(self.widget_3)
        self.label_11.setObjectName(u"label_11")

        self.gridLayout.addWidget(self.label_11, 1, 0, 1, 1)

        self.horizontalSlider = QSlider(self.widget_3)
        self.horizontalSlider.setObjectName(u"horizontalSlider")
        self.horizontalSlider.setMaximum(20000)
        self.horizontalSlider.setValue(9400)
        self.horizontalSlider.setOrientation(Qt.Horizontal)

        self.gridLayout.addWidget(self.horizontalSlider, 2, 1, 1, 1)

        self.lineEdit_6 = QLineEdit(self.widget_3)
        self.lineEdit_6.setObjectName(u"lineEdit_6")
        self.lineEdit_6.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit_6, 7, 1, 1, 1)

        self.label_3 = QLabel(self.widget_3)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 4, 0, 1, 1)

        self.lineEdit_7 = QLineEdit(self.widget_3)
        self.lineEdit_7.setObjectName(u"lineEdit_7")
        self.lineEdit_7.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit_7, 8, 1, 1, 1)


        self.gridLayout_8.addWidget(self.widget_3, 0, 0, 5, 1)

        self.pushButton = QPushButton(ParamWidget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setEnabled(True)
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())
        self.pushButton.setSizePolicy(sizePolicy2)
        self.pushButton.setStyleSheet(u"")

        self.gridLayout_8.addWidget(self.pushButton, 6, 1, 1, 1)

        self.widget_2 = QWidget(ParamWidget)
        self.widget_2.setObjectName(u"widget_2")
        self.widget_2.setStyleSheet(u"QWidget #widget_2 {\n"
"	background-color: rgba(245, 245, 245, 0.9);\n"
"	border-radius: 8px;\n"
"}\n"
"")
        self.gridLayout_2 = QGridLayout(self.widget_2)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.groupBox_2 = QGroupBox(self.widget_2)
        self.groupBox_2.setObjectName(u"groupBox_2")
        sizePolicy1.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy1)
        font2 = QFont()
        font2.setBold(True)
        self.groupBox_2.setFont(font2)
        self.radioButton_3 = QRadioButton(self.groupBox_2)
        self.radioButton_3.setObjectName(u"radioButton_3")
        self.radioButton_3.setGeometry(QRect(11, 31, 91, 20))
        self.radioButton_4 = QRadioButton(self.groupBox_2)
        self.radioButton_4.setObjectName(u"radioButton_4")
        self.radioButton_4.setGeometry(QRect(120, 30, 111, 20))

        self.gridLayout_2.addWidget(self.groupBox_2, 1, 1, 1, 1)

        self.comboBox_2 = QComboBox(self.widget_2)
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.setObjectName(u"comboBox_2")

        self.gridLayout_2.addWidget(self.comboBox_2, 4, 0, 1, 1)

        self.groupBox = QGroupBox(self.widget_2)
        self.groupBox.setObjectName(u"groupBox")
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setFont(font2)
        self.radioButton = QRadioButton(self.groupBox)
        self.radioButton.setObjectName(u"radioButton")
        self.radioButton.setGeometry(QRect(11, 31, 38, 20))
        self.radioButton_2 = QRadioButton(self.groupBox)
        self.radioButton_2.setObjectName(u"radioButton_2")
        self.radioButton_2.setGeometry(QRect(55, 31, 39, 20))

        self.gridLayout_2.addWidget(self.groupBox, 1, 0, 1, 1)

        self.label_9 = QLabel(self.widget_2)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setFont(font2)
        self.label_9.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.label_9, 2, 0, 1, 1)

        self.comboBox_3 = QComboBox(self.widget_2)
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.setObjectName(u"comboBox_3")

        self.gridLayout_2.addWidget(self.comboBox_3, 4, 1, 1, 1)

        self.label_10 = QLabel(self.widget_2)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setFont(font2)
        self.label_10.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.label_10, 2, 1, 1, 1)


        self.gridLayout_8.addWidget(self.widget_2, 5, 0, 3, 1)

        self.pushButton_2 = QPushButton(ParamWidget)
        self.pushButton_2.setObjectName(u"pushButton_2")
        sizePolicy2.setHeightForWidth(self.pushButton_2.sizePolicy().hasHeightForWidth())
        self.pushButton_2.setSizePolicy(sizePolicy2)
        self.pushButton_2.setStyleSheet(u"")

        self.gridLayout_8.addWidget(self.pushButton_2, 7, 1, 1, 1)

        self.widget_5 = QWidget(ParamWidget)
        self.widget_5.setObjectName(u"widget_5")
        self.widget_5.setStyleSheet(u"QWidget #widget_5 {\n"
"	background-color: rgba(245, 245, 245, 0.9);\n"
"	border-radius: 8px;\n"
"	border-style:dotted;\n"
"}\n"
"")
        self.gridLayout_5 = QGridLayout(self.widget_5)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setVerticalSpacing(10)
        self.gridLayout_4 = QGridLayout()
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setSizeConstraint(QLayout.SetNoConstraint)
        self.gridLayout_4.setHorizontalSpacing(30)
        self.gridLayout_4.setVerticalSpacing(10)
        self.lineEdit_10 = QLineEdit(self.widget_5)
        self.lineEdit_10.setObjectName(u"lineEdit_10")
        self.lineEdit_10.setAlignment(Qt.AlignCenter)
        self.lineEdit_10.setReadOnly(True)

        self.gridLayout_4.addWidget(self.lineEdit_10, 0, 2, 1, 1)

        self.label_18 = QLabel(self.widget_5)
        self.label_18.setObjectName(u"label_18")
        self.label_18.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_4.addWidget(self.label_18, 1, 0, 1, 1)

        self.label_19 = QLabel(self.widget_5)
        self.label_19.setObjectName(u"label_19")
        self.label_19.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_4.addWidget(self.label_19, 2, 0, 1, 1)

        self.horizontalSlider_7 = QSlider(self.widget_5)
        self.horizontalSlider_7.setObjectName(u"horizontalSlider_7")
        self.horizontalSlider_7.setMaximum(24)
        self.horizontalSlider_7.setValue(1)
        self.horizontalSlider_7.setOrientation(Qt.Horizontal)

        self.gridLayout_4.addWidget(self.horizontalSlider_7, 0, 1, 1, 1)

        self.label_17 = QLabel(self.widget_5)
        self.label_17.setObjectName(u"label_17")
        self.label_17.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_4.addWidget(self.label_17, 0, 0, 1, 1)

        self.lineEdit_11 = QLineEdit(self.widget_5)
        self.lineEdit_11.setObjectName(u"lineEdit_11")
        self.lineEdit_11.setAlignment(Qt.AlignCenter)
        self.lineEdit_11.setReadOnly(True)

        self.gridLayout_4.addWidget(self.lineEdit_11, 1, 2, 1, 1)

        self.horizontalSlider_8 = QSlider(self.widget_5)
        self.horizontalSlider_8.setObjectName(u"horizontalSlider_8")
        self.horizontalSlider_8.setMaximum(24)
        self.horizontalSlider_8.setValue(2)
        self.horizontalSlider_8.setOrientation(Qt.Horizontal)

        self.gridLayout_4.addWidget(self.horizontalSlider_8, 1, 1, 1, 1)

        self.comboBox = QComboBox(self.widget_5)
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.setObjectName(u"comboBox")
        self.comboBox.setLayoutDirection(Qt.LeftToRight)

        self.gridLayout_4.addWidget(self.comboBox, 2, 2, 1, 1)


        self.gridLayout_5.addLayout(self.gridLayout_4, 1, 0, 1, 1)

        self.label_16 = QLabel(self.widget_5)
        self.label_16.setObjectName(u"label_16")
        sizePolicy1.setHeightForWidth(self.label_16.sizePolicy().hasHeightForWidth())
        self.label_16.setSizePolicy(sizePolicy1)
        font3 = QFont()
        font3.setPointSize(12)
        font3.setBold(True)
        font3.setUnderline(False)
        self.label_16.setFont(font3)
        self.label_16.setLayoutDirection(Qt.LeftToRight)
        self.label_16.setAlignment(Qt.AlignCenter)

        self.gridLayout_5.addWidget(self.label_16, 0, 0, 1, 1)


        self.gridLayout_8.addWidget(self.widget_5, 0, 1, 2, 1)


        self.retranslateUi(ParamWidget)

        self.comboBox_3.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(ParamWidget)
    # setupUi

    def retranslateUi(self, ParamWidget):
        ParamWidget.setWindowTitle(QCoreApplication.translate("ParamWidget", u"Form", None))
        self.label_13.setText(QCoreApplication.translate("ParamWidget", u"Period spremnosti za pru\u017eanje usluge fleksibilnosti", None))
        self.label_14.setText(QCoreApplication.translate("ParamWidget", u"Po\u010detak", None))
        self.label_15.setText(QCoreApplication.translate("ParamWidget", u"Zavr\u0161etak", None))
        self.comboBox_4.setItemText(0, QCoreApplication.translate("ParamWidget", u"pozitivan", None))
        self.comboBox_4.setItemText(1, QCoreApplication.translate("ParamWidget", u"negativan", None))

        self.comboBox_4.setCurrentText(QCoreApplication.translate("ParamWidget", u"pozitivan", None))
        self.label_21.setText(QCoreApplication.translate("ParamWidget", u"Naknada za fleksibilnost [EUR/kW]", None))
        self.label_23.setText(QCoreApplication.translate("ParamWidget", u"Vjerojatnost prolaska ponude fleksibilnosti", None))
        self.label_22.setText(QCoreApplication.translate("ParamWidget", u"Cijena odstupanja potro\u0161nje [EUR/kWh]", None))
        self.label_5.setText(QCoreApplication.translate("ParamWidget", u"Predznak usluge fleksibilnosti", None))
        self.label_25.setText(QCoreApplication.translate("ParamWidget", u"Parametri fleksibilnosti", None))
        self.label_4.setText(QCoreApplication.translate("ParamWidget", u"Broj solarnih panela", None))
        self.label_2.setText(QCoreApplication.translate("ParamWidget", u"Snaga pretvara\u010da (W)", None))
        self.label.setText(QCoreApplication.translate("ParamWidget", u"Kapacitet baterije (Wh)", None))
        self.label_6.setText(QCoreApplication.translate("ParamWidget", u"Radna energija VT [EUR/kWh]", None))
        self.label_12.setText(QCoreApplication.translate("ParamWidget", u"Vr\u0161na snaga[EUR/kW]", None))
        self.label_8.setText(QCoreApplication.translate("ParamWidget", u"Dan u godini ", None))
        self.label_7.setText(QCoreApplication.translate("ParamWidget", u"Radna energija NT [EUR/kWh]", None))
        self.dateEdit.setDisplayFormat(QCoreApplication.translate("ParamWidget", u"d.M.", None))
        self.label_20.setText(QCoreApplication.translate("ParamWidget", u"Snaga solarnog panela (Wp)", None))
        self.label_24.setText(QCoreApplication.translate("ParamWidget", u"Parametri sustava", None))
        self.label_11.setText(QCoreApplication.translate("ParamWidget", u"Kapacitet spremnika vode (L)", None))
        self.lineEdit_6.setText("")
        self.label_3.setText(QCoreApplication.translate("ParamWidget", u"Snaga grija\u010da vode (W)", None))
        self.pushButton.setText(QCoreApplication.translate("ParamWidget", u"Pokretanje optimizacije", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("ParamWidget", u"Postavke grija\u010da", None))
        self.radioButton_3.setText(QCoreApplication.translate("ParamWidget", u"Kontinuiran", None))
        self.radioButton_4.setText(QCoreApplication.translate("ParamWidget", u"Diskretan", None))
        self.comboBox_2.setItemText(0, QCoreApplication.translate("ParamWidget", u"S odzivom potro\u0161nje", None))
        self.comboBox_2.setItemText(1, QCoreApplication.translate("ParamWidget", u"Bez odziva potro\u0161nje", None))

        self.groupBox.setTitle(QCoreApplication.translate("ParamWidget", u"Usporedba dvaju modela", None))
        self.radioButton.setText(QCoreApplication.translate("ParamWidget", u"Da", None))
        self.radioButton_2.setText(QCoreApplication.translate("ParamWidget", u"Ne", None))
        self.label_9.setText(QCoreApplication.translate("ParamWidget", u"Prvi model", None))
        self.comboBox_3.setItemText(0, QCoreApplication.translate("ParamWidget", u"Bez odziva potro\u0161nje", None))
        self.comboBox_3.setItemText(1, QCoreApplication.translate("ParamWidget", u"Jednostavno upravljanje", None))
        self.comboBox_3.setItemText(2, QCoreApplication.translate("ParamWidget", u"Bez odziva potro\u0161nje i vr\u0161ne snage", None))

        self.label_10.setText(QCoreApplication.translate("ParamWidget", u"Drugi model", None))
        self.pushButton_2.setText(QCoreApplication.translate("ParamWidget", u"Grafovi optimizacije", None))
        self.label_18.setText(QCoreApplication.translate("ParamWidget", u"Trajanje oporavka (R)", None))
        self.label_19.setText(QCoreApplication.translate("ParamWidget", u"Period izme\u0111u aktivacija (Q)", None))
        self.label_17.setText(QCoreApplication.translate("ParamWidget", u"Trajanje pru\u017eanja fleksibilnosti (F)", None))
        self.comboBox.setItemText(0, QCoreApplication.translate("ParamWidget", u"2", None))
        self.comboBox.setItemText(1, QCoreApplication.translate("ParamWidget", u"4", None))
        self.comboBox.setItemText(2, QCoreApplication.translate("ParamWidget", u"6", None))
        self.comboBox.setItemText(3, QCoreApplication.translate("ParamWidget", u"8", None))
        self.comboBox.setItemText(4, QCoreApplication.translate("ParamWidget", u"12", None))
        self.comboBox.setItemText(5, QCoreApplication.translate("ParamWidget", u"24", None))

        self.comboBox.setCurrentText(QCoreApplication.translate("ParamWidget", u"2", None))
        self.label_16.setText(QCoreApplication.translate("ParamWidget", u"Duljine perioda pru\u017eanja fleksibilnosti", None))
    # retranslateUi

