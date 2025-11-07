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
    QGroupBox, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QRadioButton, QSizePolicy, QSpinBox,
    QTimeEdit, QWidget)
from MILP_GUI import resources_rc

class Ui_ParamWidget(object):
    def setupUi(self, ParamWidget):
        if not ParamWidget.objectName():
            ParamWidget.setObjectName(u"ParamWidget")
        ParamWidget.resize(2095, 976)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(ParamWidget.sizePolicy().hasHeightForWidth())
        ParamWidget.setSizePolicy(sizePolicy)
        ParamWidget.setMinimumSize(QSize(1200, 645))
        ParamWidget.setAutoFillBackground(False)
        ParamWidget.setStyleSheet(u"QWidget {\n"
"    color: #ffffff;\n"
"}\n"
".QWidget {\n"
"	margin: 5px;\n"
"}\n"
"QWidget#ParamWidget{\n"
"background: qlineargradient(\n"
"        spread:pad,\n"
"        x1:0, y1:0,\n"
"        x2:1, y2:0,\n"
"        stop:0   #0C0C31,     \n"
"        stop:0.5 #06032E,     \n"
"        stop:1   #0C0C31     \n"
"    );	\n"
"}\n"
"QMainWindow {\n"
"background-color: #0C0C31;\n"
"}\n"
".QWidget {\n"
"	background-color: #091539;\n"
"}\n"
"\n"
"QLineEdit {\n"
"    background-color: #041c3d;\n"
"    color: #ffffff;\n"
"    border: 1px solid #2a628f;\n"
"    padding: 4px 4px;\n"
"    border-radius: 4px;\n"
"}\n"
"QGroupBox {\n"
"    background-color: #041c3d;\n"
"    color: #ffffff;\n"
"    border: 1px solid #2a628f;\n"
"    padding: 0px 4px;\n"
"    border-radius: 4px;\n"
"}\n"
"QPushButton {\n"
"    background: qlineargradient(\n"
"        spread:pad,\n"
"        x1:0, y1:0,\n"
"        x2:1, y2:0,\n"
"        stop:0 #51FCBB,\n"
"        stop:1 #4EE5D9\n"
"    );\n"
"    color: #000000;\n"
"    font-weight: bol"
                        "d;\n"
"    border: none;\n"
"    border-radius: 5px;\n"
"    padding: 5px 15px;\n"
"	margin: 5px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #CBFEEF\n"
"}\n"
"\n"
"QSlider::handle{\n"
" background-color: #45CACB;\n"
"}\n"
"\n"
"QSlider::handle:hover{\n"
" background-color: #51FDBA;\n"
"}\n"
"\n"
"\n"
"/* Popup lista */\n"
"QComboBox QAbstractItemView {\n"
"    background-color: #002949;\n"
"    color: #ffffff;\n"
"    border: 1px solid #2a628f;\n"
"    border-radius: 4px;\n"
"    padding: 4px;\n"
"    outline: none;   /* makni bijeli obrub */\n"
"}\n"
"\n"
"/* Hover efekt na item */\n"
"QComboBox QAbstractItemView::item:hover {\n"
"    background-color: #15415A;\n"
"    color: #51FDBA;\n"
"    outline: none;\n"
"    border: none;\n"
"}\n"
"\n"
"/* Selektirani item */\n"
"QComboBox QAbstractItemView::item:selected {\n"
"    background-color: #15415A;\n"
"    color: #51FDBA;\n"
"    outline: none;\n"
"    border: none;\n"
"}\n"
"\n"
"QRadioButton::hover {\n"
"color: #51FDBA;\n"
"}\n"
"QRadioBut"
                        "ton{\n"
"margin: 8px 0px;\n"
"}\n"
"\n"
"QLabel#title1 {\n"
"	padding: 8px 16px\n"
"}\n"
"QLabel#title4 {\n"
"	margin: 8px 16px\n"
"}\n"
"QLabel#title3 {\n"
"	margin: 8px 16px\n"
"}\n"
"\n"
"\n"
"QSpinBox, QDateEdit, QTimeEdit, QComboBox{\n"
"    background-color: #002949;\n"
"    color: #ffffff;\n"
"    padding: 4px 15px;\n"
"}\n"
"QComboBox{\n"
"	padding: 2px 15px;\n"
"}\n"
"\n"
"QSpinBox:hover,\n"
"QDateEdit:hover,\n"
"QTimeEdit:hover,\n"
"QComboBox:hover {\n"
"    color: #51FDBA;\n"
"}\n"
"")
        self.gridLayout_7 = QGridLayout(ParamWidget)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.widget_5 = QWidget(ParamWidget)
        self.widget_5.setObjectName(u"widget_5")
        sizePolicy.setHeightForWidth(self.widget_5.sizePolicy().hasHeightForWidth())
        self.widget_5.setSizePolicy(sizePolicy)
        self.widget_5.setMinimumSize(QSize(0, 80))
        self.widget_5.setMaximumSize(QSize(16777215, 80))
        self.horizontalLayout = QHBoxLayout(self.widget_5)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_6 = QLabel(self.widget_5)
        self.label_6.setObjectName(u"label_6")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy1)
        self.label_6.setMinimumSize(QSize(104, 65))
        self.label_6.setMaximumSize(QSize(104, 65))
        self.label_6.setPixmap(QPixmap(u":/icons/FER_logo_2.svg"))
        self.label_6.setScaledContents(True)

        self.horizontalLayout.addWidget(self.label_6)

        self.label_7 = QLabel(self.widget_5)
        self.label_7.setObjectName(u"label_7")
        sizePolicy1.setHeightForWidth(self.label_7.sizePolicy().hasHeightForWidth())
        self.label_7.setSizePolicy(sizePolicy1)
        self.label_7.setMinimumSize(QSize(198, 65))
        self.label_7.setMaximumSize(QSize(198, 65))
        self.label_7.setPixmap(QPixmap(u":/icons/LARES_2_transparent_white.svg"))
        self.label_7.setScaledContents(True)

        self.horizontalLayout.addWidget(self.label_7)

        self.label_9 = QLabel(self.widget_5)
        self.label_9.setObjectName(u"label_9")
        sizePolicy1.setHeightForWidth(self.label_9.sizePolicy().hasHeightForWidth())
        self.label_9.setSizePolicy(sizePolicy1)

        self.horizontalLayout.addWidget(self.label_9)


        self.gridLayout_7.addWidget(self.widget_5, 0, 0, 1, 1)

        self.widget = QWidget(ParamWidget)
        self.widget.setObjectName(u"widget")
        self.widget.setMinimumSize(QSize(0, 80))
        self.widget.setMaximumSize(QSize(16777215, 80))
        self.horizontalLayout_2 = QHBoxLayout(self.widget)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_8 = QLabel(self.widget)
        self.label_8.setObjectName(u"label_8")
        sizePolicy.setHeightForWidth(self.label_8.sizePolicy().hasHeightForWidth())
        self.label_8.setSizePolicy(sizePolicy)
        self.label_8.setMinimumSize(QSize(0, 65))
        self.label_8.setMaximumSize(QSize(16777215, 65))
        font = QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.label_8.setFont(font)
        self.label_8.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.label_8.setMargin(10)
        self.label_8.setIndent(-1)

        self.horizontalLayout_2.addWidget(self.label_8)

        self.dateEdit = QDateEdit(self.widget)
        self.dateEdit.setObjectName(u"dateEdit")
        sizePolicy.setHeightForWidth(self.dateEdit.sizePolicy().hasHeightForWidth())
        self.dateEdit.setSizePolicy(sizePolicy)
        self.dateEdit.setMinimumSize(QSize(0, 30))
        self.dateEdit.setMaximumSize(QSize(500, 70))
        self.dateEdit.setFont(font)
        self.dateEdit.setDateTime(QDateTime(QDate(2025, 6, 25), QTime(0, 0, 0)))
        self.dateEdit.setDate(QDate(2025, 6, 25))

        self.horizontalLayout_2.addWidget(self.dateEdit)


        self.gridLayout_7.addWidget(self.widget, 0, 1, 1, 1)

        self.widget_3 = QWidget(ParamWidget)
        self.widget_3.setObjectName(u"widget_3")
        sizePolicy.setHeightForWidth(self.widget_3.sizePolicy().hasHeightForWidth())
        self.widget_3.setSizePolicy(sizePolicy)
        self.widget_3.setMinimumSize(QSize(0, 0))
        self.widget_3.setMaximumSize(QSize(16777215, 16777215))
        self.widget_3.setStyleSheet(u"")
        self.gridLayout = QGridLayout(self.widget_3)
        self.gridLayout.setObjectName(u"gridLayout")
        self.lineEdit_7 = QLineEdit(self.widget_3)
        self.lineEdit_7.setObjectName(u"lineEdit_7")
        sizePolicy.setHeightForWidth(self.lineEdit_7.sizePolicy().hasHeightForWidth())
        self.lineEdit_7.setSizePolicy(sizePolicy)
        self.lineEdit_7.setMinimumSize(QSize(0, 30))
        self.lineEdit_7.setMaximumSize(QSize(1000, 70))
        self.lineEdit_7.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit_7, 8, 1, 1, 1)

        self.groupBox_4 = QGroupBox(self.widget_3)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.groupBox_4.setMinimumSize(QSize(300, 0))
        self.groupBox_4.setFont(font)
        self.horizontalLayout_3 = QHBoxLayout(self.groupBox_4)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(-1, 30, -1, 20)
        self.radioButton_9 = QRadioButton(self.groupBox_4)
        self.radioButton_9.setObjectName(u"radioButton_9")
        font1 = QFont()
        font1.setPointSize(12)
        self.radioButton_9.setFont(font1)

        self.horizontalLayout_3.addWidget(self.radioButton_9)

        self.radioButton_7 = QRadioButton(self.groupBox_4)
        self.radioButton_7.setObjectName(u"radioButton_7")
        self.radioButton_7.setFont(font1)

        self.horizontalLayout_3.addWidget(self.radioButton_7)

        self.radioButton_10 = QRadioButton(self.groupBox_4)
        self.radioButton_10.setObjectName(u"radioButton_10")
        self.radioButton_10.setFont(font1)

        self.horizontalLayout_3.addWidget(self.radioButton_10)

        self.radioButton_8 = QRadioButton(self.groupBox_4)
        self.radioButton_8.setObjectName(u"radioButton_8")
        self.radioButton_8.setFont(font1)

        self.horizontalLayout_3.addWidget(self.radioButton_8)


        self.gridLayout.addWidget(self.groupBox_4, 1, 0, 1, 2)

        self.label_4 = QLabel(self.widget_3)
        self.label_4.setObjectName(u"label_4")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy2)
        font2 = QFont()
        font2.setPointSize(12)
        font2.setBold(False)
        self.label_4.setFont(font2)

        self.gridLayout.addWidget(self.label_4, 6, 0, 1, 1)

        self.title1 = QLabel(self.widget_3)
        self.title1.setObjectName(u"title1")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.title1.sizePolicy().hasHeightForWidth())
        self.title1.setSizePolicy(sizePolicy3)
        self.title1.setMaximumSize(QSize(16777215, 70))
        font3 = QFont()
        font3.setPointSize(14)
        font3.setBold(True)
        self.title1.setFont(font3)
        self.title1.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.title1, 0, 0, 1, 2)

        self.label_2 = QLabel(self.widget_3)
        self.label_2.setObjectName(u"label_2")
        sizePolicy2.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy2)
        self.label_2.setFont(font2)

        self.gridLayout.addWidget(self.label_2, 4, 0, 1, 1)

        self.label_12 = QLabel(self.widget_3)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setFont(font1)

        self.gridLayout.addWidget(self.label_12, 9, 0, 1, 1)

        self.label_11 = QLabel(self.widget_3)
        self.label_11.setObjectName(u"label_11")
        sizePolicy2.setHeightForWidth(self.label_11.sizePolicy().hasHeightForWidth())
        self.label_11.setSizePolicy(sizePolicy2)
        self.label_11.setFont(font2)

        self.gridLayout.addWidget(self.label_11, 2, 0, 1, 1)

        self.lineEdit_2 = QLineEdit(self.widget_3)
        self.lineEdit_2.setObjectName(u"lineEdit_2")
        sizePolicy.setHeightForWidth(self.lineEdit_2.sizePolicy().hasHeightForWidth())
        self.lineEdit_2.setSizePolicy(sizePolicy)
        self.lineEdit_2.setMinimumSize(QSize(0, 30))
        self.lineEdit_2.setMaximumSize(QSize(1000, 70))
        self.lineEdit_2.setFont(font1)
        self.lineEdit_2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineEdit_2.setReadOnly(False)

        self.gridLayout.addWidget(self.lineEdit_2, 4, 1, 1, 1)

        self.label_3 = QLabel(self.widget_3)
        self.label_3.setObjectName(u"label_3")
        sizePolicy2.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy2)
        self.label_3.setFont(font2)

        self.gridLayout.addWidget(self.label_3, 5, 0, 1, 1)

        self.label_20 = QLabel(self.widget_3)
        self.label_20.setObjectName(u"label_20")
        sizePolicy2.setHeightForWidth(self.label_20.sizePolicy().hasHeightForWidth())
        self.label_20.setSizePolicy(sizePolicy2)
        self.label_20.setFont(font2)

        self.gridLayout.addWidget(self.label_20, 7, 0, 1, 1)

        self.label = QLabel(self.widget_3)
        self.label.setObjectName(u"label")
        sizePolicy2.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy2)
        self.label.setFont(font2)

        self.gridLayout.addWidget(self.label, 3, 0, 1, 1)

        self.lineEdit_4 = QLineEdit(self.widget_3)
        self.lineEdit_4.setObjectName(u"lineEdit_4")
        sizePolicy.setHeightForWidth(self.lineEdit_4.sizePolicy().hasHeightForWidth())
        self.lineEdit_4.setSizePolicy(sizePolicy)
        self.lineEdit_4.setMinimumSize(QSize(0, 30))
        self.lineEdit_4.setMaximumSize(QSize(1000, 70))
        self.lineEdit_4.setFont(font1)
        self.lineEdit_4.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineEdit_4.setReadOnly(False)

        self.gridLayout.addWidget(self.lineEdit_4, 6, 1, 1, 1)

        self.lineEdit = QLineEdit(self.widget_3)
        self.lineEdit.setObjectName(u"lineEdit")
        sizePolicy.setHeightForWidth(self.lineEdit.sizePolicy().hasHeightForWidth())
        self.lineEdit.setSizePolicy(sizePolicy)
        self.lineEdit.setMinimumSize(QSize(0, 30))
        self.lineEdit.setMaximumSize(QSize(1000, 70))
        self.lineEdit.setFont(font1)
        self.lineEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineEdit.setReadOnly(False)

        self.gridLayout.addWidget(self.lineEdit, 3, 1, 1, 1)

        self.lineEdit_3 = QLineEdit(self.widget_3)
        self.lineEdit_3.setObjectName(u"lineEdit_3")
        sizePolicy.setHeightForWidth(self.lineEdit_3.sizePolicy().hasHeightForWidth())
        self.lineEdit_3.setSizePolicy(sizePolicy)
        self.lineEdit_3.setMinimumSize(QSize(0, 30))
        self.lineEdit_3.setMaximumSize(QSize(1000, 70))
        self.lineEdit_3.setFont(font1)
        self.lineEdit_3.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineEdit_3.setReadOnly(False)

        self.gridLayout.addWidget(self.lineEdit_3, 5, 1, 1, 1)

        self.lineEdit_12 = QLineEdit(self.widget_3)
        self.lineEdit_12.setObjectName(u"lineEdit_12")
        sizePolicy.setHeightForWidth(self.lineEdit_12.sizePolicy().hasHeightForWidth())
        self.lineEdit_12.setSizePolicy(sizePolicy)
        self.lineEdit_12.setMinimumSize(QSize(0, 30))
        self.lineEdit_12.setMaximumSize(QSize(1000, 70))
        self.lineEdit_12.setFont(font1)
        self.lineEdit_12.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineEdit_12.setReadOnly(False)

        self.gridLayout.addWidget(self.lineEdit_12, 7, 1, 1, 1)

        self.label_10 = QLabel(self.widget_3)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setFont(font1)

        self.gridLayout.addWidget(self.label_10, 8, 0, 1, 1)

        self.lineEdit_8 = QLineEdit(self.widget_3)
        self.lineEdit_8.setObjectName(u"lineEdit_8")
        sizePolicy.setHeightForWidth(self.lineEdit_8.sizePolicy().hasHeightForWidth())
        self.lineEdit_8.setSizePolicy(sizePolicy)
        self.lineEdit_8.setMinimumSize(QSize(0, 30))
        self.lineEdit_8.setMaximumSize(QSize(1000, 70))
        self.lineEdit_8.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit_8, 9, 1, 1, 1)

        self.lineEdit_9 = QLineEdit(self.widget_3)
        self.lineEdit_9.setObjectName(u"lineEdit_9")
        self.lineEdit_9.setEnabled(True)
        sizePolicy.setHeightForWidth(self.lineEdit_9.sizePolicy().hasHeightForWidth())
        self.lineEdit_9.setSizePolicy(sizePolicy)
        self.lineEdit_9.setMinimumSize(QSize(0, 30))
        self.lineEdit_9.setMaximumSize(QSize(1000, 70))
        self.lineEdit_9.setFont(font1)
        self.lineEdit_9.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineEdit_9.setReadOnly(False)

        self.gridLayout.addWidget(self.lineEdit_9, 2, 1, 1, 1)


        self.gridLayout_7.addWidget(self.widget_3, 1, 0, 2, 1)

        self.widget_4 = QWidget(ParamWidget)
        self.widget_4.setObjectName(u"widget_4")
        sizePolicy.setHeightForWidth(self.widget_4.sizePolicy().hasHeightForWidth())
        self.widget_4.setSizePolicy(sizePolicy)
        self.widget_4.setMinimumSize(QSize(0, 330))
        self.widget_4.setMaximumSize(QSize(16777215, 16777215))
        self.widget_4.setStyleSheet(u"")
        self.gridLayout_4 = QGridLayout(self.widget_4)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setContentsMargins(20, 20, 20, 20)
        self.comboBox_4 = QComboBox(self.widget_4)
        self.comboBox_4.addItem("")
        self.comboBox_4.addItem("")
        self.comboBox_4.addItem("")
        self.comboBox_4.setObjectName(u"comboBox_4")
        sizePolicy.setHeightForWidth(self.comboBox_4.sizePolicy().hasHeightForWidth())
        self.comboBox_4.setSizePolicy(sizePolicy)
        self.comboBox_4.setMinimumSize(QSize(0, 30))
        self.comboBox_4.setMaximumSize(QSize(1000, 70))
        self.comboBox_4.setFont(font2)

        self.gridLayout_4.addWidget(self.comboBox_4, 8, 1, 1, 2)

        self.label_19 = QLabel(self.widget_4)
        self.label_19.setObjectName(u"label_19")
        sizePolicy.setHeightForWidth(self.label_19.sizePolicy().hasHeightForWidth())
        self.label_19.setSizePolicy(sizePolicy)
        self.label_19.setFont(font2)
        self.label_19.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_4.addWidget(self.label_19, 7, 0, 1, 1)

        self.label_5 = QLabel(self.widget_4)
        self.label_5.setObjectName(u"label_5")
        sizePolicy.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)
        self.label_5.setFont(font2)

        self.gridLayout_4.addWidget(self.label_5, 8, 0, 1, 1)

        self.lineEdit_6 = QLineEdit(self.widget_4)
        self.lineEdit_6.setObjectName(u"lineEdit_6")
        sizePolicy.setHeightForWidth(self.lineEdit_6.sizePolicy().hasHeightForWidth())
        self.lineEdit_6.setSizePolicy(sizePolicy)
        self.lineEdit_6.setMinimumSize(QSize(0, 30))
        self.lineEdit_6.setMaximumSize(QSize(500, 70))
        self.lineEdit_6.setFont(font1)
        self.lineEdit_6.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_4.addWidget(self.lineEdit_6, 10, 2, 1, 1)

        self.spinBox_2 = QSpinBox(self.widget_4)
        self.spinBox_2.setObjectName(u"spinBox_2")
        sizePolicy.setHeightForWidth(self.spinBox_2.sizePolicy().hasHeightForWidth())
        self.spinBox_2.setSizePolicy(sizePolicy)
        self.spinBox_2.setMinimumSize(QSize(0, 30))
        self.spinBox_2.setMaximumSize(QSize(500, 70))
        self.spinBox_2.setFont(font1)
        self.spinBox_2.setValue(1)

        self.gridLayout_4.addWidget(self.spinBox_2, 4, 1, 1, 1)

        self.title4 = QLabel(self.widget_4)
        self.title4.setObjectName(u"title4")
        sizePolicy3.setHeightForWidth(self.title4.sizePolicy().hasHeightForWidth())
        self.title4.setSizePolicy(sizePolicy3)
        self.title4.setMaximumSize(QSize(16777215, 70))
        self.title4.setFont(font3)
        self.title4.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_4.addWidget(self.title4, 0, 0, 2, 3)

        self.label_17 = QLabel(self.widget_4)
        self.label_17.setObjectName(u"label_17")
        sizePolicy.setHeightForWidth(self.label_17.sizePolicy().hasHeightForWidth())
        self.label_17.setSizePolicy(sizePolicy)
        self.label_17.setFont(font2)
        self.label_17.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_4.addWidget(self.label_17, 4, 0, 1, 1)

        self.timeEdit = QTimeEdit(self.widget_4)
        self.timeEdit.setObjectName(u"timeEdit")
        sizePolicy.setHeightForWidth(self.timeEdit.sizePolicy().hasHeightForWidth())
        self.timeEdit.setSizePolicy(sizePolicy)
        self.timeEdit.setMinimumSize(QSize(0, 30))
        self.timeEdit.setMaximumSize(QSize(500, 70))
        self.timeEdit.setFont(font1)
        self.timeEdit.setDateTime(QDateTime(QDate(2024, 1, 1), QTime(22, 59, 0)))
        self.timeEdit.setTime(QTime(22, 59, 0))

        self.gridLayout_4.addWidget(self.timeEdit, 2, 2, 1, 1)

        self.lineEdit_13 = QLineEdit(self.widget_4)
        self.lineEdit_13.setObjectName(u"lineEdit_13")
        sizePolicy.setHeightForWidth(self.lineEdit_13.sizePolicy().hasHeightForWidth())
        self.lineEdit_13.setSizePolicy(sizePolicy)
        self.lineEdit_13.setMinimumSize(QSize(0, 30))
        self.lineEdit_13.setMaximumSize(QSize(500, 70))
        self.lineEdit_13.setFont(font1)
        self.lineEdit_13.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_4.addWidget(self.lineEdit_13, 9, 1, 1, 1)

        self.label_23 = QLabel(self.widget_4)
        self.label_23.setObjectName(u"label_23")
        sizePolicy.setHeightForWidth(self.label_23.sizePolicy().hasHeightForWidth())
        self.label_23.setSizePolicy(sizePolicy)
        self.label_23.setFont(font2)

        self.gridLayout_4.addWidget(self.label_23, 10, 0, 1, 1)

        self.label_14 = QLabel(self.widget_4)
        self.label_14.setObjectName(u"label_14")
        sizePolicy.setHeightForWidth(self.label_14.sizePolicy().hasHeightForWidth())
        self.label_14.setSizePolicy(sizePolicy)
        self.label_14.setMaximumSize(QSize(16777215, 16777215))
        self.label_14.setFont(font2)

        self.gridLayout_4.addWidget(self.label_14, 2, 0, 1, 1)

        self.lineEdit_14 = QLineEdit(self.widget_4)
        self.lineEdit_14.setObjectName(u"lineEdit_14")
        sizePolicy.setHeightForWidth(self.lineEdit_14.sizePolicy().hasHeightForWidth())
        self.lineEdit_14.setSizePolicy(sizePolicy)
        self.lineEdit_14.setMinimumSize(QSize(0, 30))
        self.lineEdit_14.setMaximumSize(QSize(500, 70))
        self.lineEdit_14.setFont(font1)
        self.lineEdit_14.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_4.addWidget(self.lineEdit_14, 10, 1, 1, 1)

        self.lineEdit_5 = QLineEdit(self.widget_4)
        self.lineEdit_5.setObjectName(u"lineEdit_5")
        sizePolicy.setHeightForWidth(self.lineEdit_5.sizePolicy().hasHeightForWidth())
        self.lineEdit_5.setSizePolicy(sizePolicy)
        self.lineEdit_5.setMinimumSize(QSize(0, 30))
        self.lineEdit_5.setMaximumSize(QSize(500, 70))
        self.lineEdit_5.setFont(font1)
        self.lineEdit_5.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_4.addWidget(self.lineEdit_5, 9, 2, 1, 1)

        self.spinBox = QSpinBox(self.widget_4)
        self.spinBox.setObjectName(u"spinBox")
        sizePolicy.setHeightForWidth(self.spinBox.sizePolicy().hasHeightForWidth())
        self.spinBox.setSizePolicy(sizePolicy)
        self.spinBox.setMinimumSize(QSize(0, 30))
        self.spinBox.setMaximumSize(QSize(500, 70))
        self.spinBox.setFont(font1)
        self.spinBox.setValue(2)

        self.gridLayout_4.addWidget(self.spinBox, 4, 2, 1, 1)

        self.timeEdit_2 = QTimeEdit(self.widget_4)
        self.timeEdit_2.setObjectName(u"timeEdit_2")
        sizePolicy.setHeightForWidth(self.timeEdit_2.sizePolicy().hasHeightForWidth())
        self.timeEdit_2.setSizePolicy(sizePolicy)
        self.timeEdit_2.setMinimumSize(QSize(0, 30))
        self.timeEdit_2.setMaximumSize(QSize(500, 70))
        self.timeEdit_2.setFont(font1)
        self.timeEdit_2.setDateTime(QDateTime(QDate(2023, 12, 31), QTime(23, 0, 0)))
        self.timeEdit_2.setTime(QTime(23, 0, 0))

        self.gridLayout_4.addWidget(self.timeEdit_2, 2, 1, 1, 1)

        self.label_21 = QLabel(self.widget_4)
        self.label_21.setObjectName(u"label_21")
        sizePolicy.setHeightForWidth(self.label_21.sizePolicy().hasHeightForWidth())
        self.label_21.setSizePolicy(sizePolicy)
        self.label_21.setMinimumSize(QSize(380, 0))
        self.label_21.setMaximumSize(QSize(500, 16777215))
        self.label_21.setFont(font2)

        self.gridLayout_4.addWidget(self.label_21, 9, 0, 1, 1)

        self.comboBox = QComboBox(self.widget_4)
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.setObjectName(u"comboBox")
        sizePolicy.setHeightForWidth(self.comboBox.sizePolicy().hasHeightForWidth())
        self.comboBox.setSizePolicy(sizePolicy)
        self.comboBox.setMinimumSize(QSize(0, 30))
        self.comboBox.setMaximumSize(QSize(1000, 70))
        self.comboBox.setFont(font1)
        self.comboBox.setLayoutDirection(Qt.LayoutDirection.LeftToRight)

        self.gridLayout_4.addWidget(self.comboBox, 7, 1, 1, 2)


        self.gridLayout_7.addWidget(self.widget_4, 1, 1, 1, 1)

        self.widget_2 = QWidget(ParamWidget)
        self.widget_2.setObjectName(u"widget_2")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.widget_2.sizePolicy().hasHeightForWidth())
        self.widget_2.setSizePolicy(sizePolicy4)
        self.widget_2.setMinimumSize(QSize(0, 0))
        self.widget_2.setMaximumSize(QSize(16777215, 250))
        self.widget_2.setStyleSheet(u"")
        self.gridLayout_3 = QGridLayout(self.widget_2)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(-1, 30, -1, 20)
        self.groupBox = QGroupBox(self.widget_2)
        self.groupBox.setObjectName(u"groupBox")
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setMinimumSize(QSize(0, 50))
        self.groupBox.setMaximumSize(QSize(16777215, 100))
        self.groupBox.setFont(font)
        self.gridLayout_2 = QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setVerticalSpacing(6)
        self.gridLayout_2.setContentsMargins(20, 30, 20, 20)
        self.radioButton = QRadioButton(self.groupBox)
        self.radioButton.setObjectName(u"radioButton")
        self.radioButton.setMinimumSize(QSize(0, 15))
        self.radioButton.setFont(font1)

        self.gridLayout_2.addWidget(self.radioButton, 0, 0, 1, 1)

        self.radioButton_2 = QRadioButton(self.groupBox)
        self.radioButton_2.setObjectName(u"radioButton_2")
        self.radioButton_2.setMinimumSize(QSize(0, 15))
        self.radioButton_2.setFont(font2)

        self.gridLayout_2.addWidget(self.radioButton_2, 0, 1, 1, 1)


        self.gridLayout_3.addWidget(self.groupBox, 0, 0, 1, 1)

        self.comboBox_2 = QComboBox(self.widget_2)
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.setObjectName(u"comboBox_2")
        sizePolicy.setHeightForWidth(self.comboBox_2.sizePolicy().hasHeightForWidth())
        self.comboBox_2.setSizePolicy(sizePolicy)
        self.comboBox_2.setMinimumSize(QSize(0, 30))
        self.comboBox_2.setMaximumSize(QSize(16777215, 70))
        self.comboBox_2.setFont(font2)

        self.gridLayout_3.addWidget(self.comboBox_2, 1, 0, 1, 1)

        self.comboBox_3 = QComboBox(self.widget_2)
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.setObjectName(u"comboBox_3")
        sizePolicy.setHeightForWidth(self.comboBox_3.sizePolicy().hasHeightForWidth())
        self.comboBox_3.setSizePolicy(sizePolicy)
        self.comboBox_3.setMinimumSize(QSize(0, 30))
        self.comboBox_3.setMaximumSize(QSize(16777215, 70))
        self.comboBox_3.setFont(font2)

        self.gridLayout_3.addWidget(self.comboBox_3, 1, 1, 1, 1)

        self.groupBox_2 = QGroupBox(self.widget_2)
        self.groupBox_2.setObjectName(u"groupBox_2")
        sizePolicy.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy)
        self.groupBox_2.setMinimumSize(QSize(0, 0))
        self.groupBox_2.setMaximumSize(QSize(16777215, 100))
        self.groupBox_2.setFont(font)
        self.gridLayout_8 = QGridLayout(self.groupBox_2)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.gridLayout_8.setContentsMargins(-1, 15, -1, 15)
        self.radioButton_3 = QRadioButton(self.groupBox_2)
        self.radioButton_3.setObjectName(u"radioButton_3")
        sizePolicy.setHeightForWidth(self.radioButton_3.sizePolicy().hasHeightForWidth())
        self.radioButton_3.setSizePolicy(sizePolicy)
        self.radioButton_3.setFont(font2)

        self.gridLayout_8.addWidget(self.radioButton_3, 0, 0, 1, 1)

        self.radioButton_4 = QRadioButton(self.groupBox_2)
        self.radioButton_4.setObjectName(u"radioButton_4")
        sizePolicy.setHeightForWidth(self.radioButton_4.sizePolicy().hasHeightForWidth())
        self.radioButton_4.setSizePolicy(sizePolicy)
        self.radioButton_4.setFont(font2)

        self.gridLayout_8.addWidget(self.radioButton_4, 0, 1, 1, 1)


        self.gridLayout_3.addWidget(self.groupBox_2, 0, 1, 1, 1)


        self.gridLayout_7.addWidget(self.widget_2, 2, 1, 1, 1)

        self.pushButton_2 = QPushButton(ParamWidget)
        self.pushButton_2.setObjectName(u"pushButton_2")
        sizePolicy.setHeightForWidth(self.pushButton_2.sizePolicy().hasHeightForWidth())
        self.pushButton_2.setSizePolicy(sizePolicy)
        self.pushButton_2.setMinimumSize(QSize(0, 40))
        self.pushButton_2.setMaximumSize(QSize(16777215, 70))
        self.pushButton_2.setStyleSheet(u"")

        self.gridLayout_7.addWidget(self.pushButton_2, 3, 0, 1, 1)

        self.pushButton = QPushButton(ParamWidget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setEnabled(True)
        sizePolicy.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())
        self.pushButton.setSizePolicy(sizePolicy)
        self.pushButton.setMinimumSize(QSize(0, 40))
        self.pushButton.setMaximumSize(QSize(16777215, 70))
        self.pushButton.setStyleSheet(u"")

        self.gridLayout_7.addWidget(self.pushButton, 3, 1, 1, 1)


        self.retranslateUi(ParamWidget)

        self.comboBox_3.setCurrentIndex(-1)


        QMetaObject.connectSlotsByName(ParamWidget)
    # setupUi

    def retranslateUi(self, ParamWidget):
        ParamWidget.setWindowTitle(QCoreApplication.translate("ParamWidget", u"Form", None))
        self.label_6.setText("")
        self.label_7.setText("")
        self.label_9.setText("")
        self.label_8.setText(QCoreApplication.translate("ParamWidget", u"Date", None))
        self.dateEdit.setDisplayFormat(QCoreApplication.translate("ParamWidget", u"d.M.", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("ParamWidget", u"Renewable energy hub", None))
        self.radioButton_9.setText(QCoreApplication.translate("ParamWidget", u"Household", None))
        self.radioButton_7.setText(QCoreApplication.translate("ParamWidget", u"Industry", None))
        self.radioButton_10.setText(QCoreApplication.translate("ParamWidget", u"Commercial", None))
        self.radioButton_8.setText(QCoreApplication.translate("ParamWidget", u"Power-2-X", None))
        self.label_4.setText(QCoreApplication.translate("ParamWidget", u"Number of solar panels", None))
        self.title1.setText(QCoreApplication.translate("ParamWidget", u"System parameters", None))
        self.label_2.setText(QCoreApplication.translate("ParamWidget", u"Inverter power (kW)", None))
        self.label_12.setText(QCoreApplication.translate("ParamWidget", u"Annual  tempered water consumption (m3)", None))
        self.label_11.setText(QCoreApplication.translate("ParamWidget", u"Water tank capacity (m3)", None))
        self.lineEdit_2.setText(QCoreApplication.translate("ParamWidget", u"2.5", None))
        self.label_3.setText(QCoreApplication.translate("ParamWidget", u"Water heater power (kW)", None))
        self.label_20.setText(QCoreApplication.translate("ParamWidget", u"Solar panel power (Wp)", None))
        self.label.setText(QCoreApplication.translate("ParamWidget", u"Battery capacity (kWh)", None))
        self.lineEdit_4.setText(QCoreApplication.translate("ParamWidget", u"10", None))
        self.lineEdit.setText(QCoreApplication.translate("ParamWidget", u"10", None))
        self.lineEdit_3.setText(QCoreApplication.translate("ParamWidget", u"2.5", None))
        self.lineEdit_12.setText(QCoreApplication.translate("ParamWidget", u"400", None))
        self.label_10.setText(QCoreApplication.translate("ParamWidget", u"Annual electricity consumption (MWh)", None))
        self.lineEdit_9.setText(QCoreApplication.translate("ParamWidget", u"0.2", None))
        self.comboBox_4.setItemText(0, QCoreApplication.translate("ParamWidget", u"positive", None))
        self.comboBox_4.setItemText(1, QCoreApplication.translate("ParamWidget", u"negative", None))
        self.comboBox_4.setItemText(2, QCoreApplication.translate("ParamWidget", u"positive and negative", None))

        self.comboBox_4.setCurrentText(QCoreApplication.translate("ParamWidget", u"positive", None))
        self.label_19.setText(QCoreApplication.translate("ParamWidget", u"Period between activations (Q)", None))
        self.label_5.setText(QCoreApplication.translate("ParamWidget", u"Direction of flexibility service", None))
        self.lineEdit_6.setText(QCoreApplication.translate("ParamWidget", u"80", None))
        self.title4.setText(QCoreApplication.translate("ParamWidget", u"Flexibility parameters", None))
        self.label_17.setText(QCoreApplication.translate("ParamWidget", u"Activation duration (F) & Recovery duration (R)", None))
        self.lineEdit_13.setText(QCoreApplication.translate("ParamWidget", u"1", None))
        self.label_23.setText(QCoreApplication.translate("ParamWidget", u"Flexibility acceptance probability [%] (pos. & neg.)", None))
        self.label_14.setText(QCoreApplication.translate("ParamWidget", u"Flexibility availability start & end", None))
        self.lineEdit_14.setText(QCoreApplication.translate("ParamWidget", u"90", None))
        self.lineEdit_5.setText(QCoreApplication.translate("ParamWidget", u"1", None))
        self.label_21.setText(QCoreApplication.translate("ParamWidget", u"Flexibility incentive [EUR/kW] (pos. & neg.)", None))
        self.comboBox.setItemText(0, QCoreApplication.translate("ParamWidget", u"2", None))
        self.comboBox.setItemText(1, QCoreApplication.translate("ParamWidget", u"4", None))
        self.comboBox.setItemText(2, QCoreApplication.translate("ParamWidget", u"6", None))
        self.comboBox.setItemText(3, QCoreApplication.translate("ParamWidget", u"8", None))
        self.comboBox.setItemText(4, QCoreApplication.translate("ParamWidget", u"12", None))
        self.comboBox.setItemText(5, QCoreApplication.translate("ParamWidget", u"24", None))

        self.comboBox.setCurrentText(QCoreApplication.translate("ParamWidget", u"2", None))
        self.groupBox.setTitle(QCoreApplication.translate("ParamWidget", u"Compare two models", None))
        self.radioButton.setText(QCoreApplication.translate("ParamWidget", u"Yes", None))
        self.radioButton_2.setText(QCoreApplication.translate("ParamWidget", u"No", None))
        self.comboBox_2.setItemText(0, QCoreApplication.translate("ParamWidget", u"With DR", None))
        self.comboBox_2.setItemText(1, QCoreApplication.translate("ParamWidget", u"Without DR", None))

        self.comboBox_2.setPlaceholderText(QCoreApplication.translate("ParamWidget", u"Choose model", None))
        self.comboBox_3.setItemText(0, QCoreApplication.translate("ParamWidget", u"Without DR", None))
        self.comboBox_3.setItemText(1, QCoreApplication.translate("ParamWidget", u"Hysteresis control", None))
        self.comboBox_3.setItemText(2, QCoreApplication.translate("ParamWidget", u"No DR and no peak power penalty", None))

        self.comboBox_3.setPlaceholderText(QCoreApplication.translate("ParamWidget", u"Choose model", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("ParamWidget", u"Heater settings", None))
        self.radioButton_3.setText(QCoreApplication.translate("ParamWidget", u"Continuous", None))
        self.radioButton_4.setText(QCoreApplication.translate("ParamWidget", u"Discrete", None))
        self.pushButton_2.setText(QCoreApplication.translate("ParamWidget", u"Show optimization graphs", None))
        self.pushButton.setText(QCoreApplication.translate("ParamWidget", u"Start optimization", None))
    # retranslateUi

