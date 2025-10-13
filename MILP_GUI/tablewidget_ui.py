# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'tablewidget.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QHeaderView, QLabel,
    QPushButton, QSizePolicy, QTabWidget, QTableWidget,
    QTableWidgetItem, QVBoxLayout, QWidget)

class Ui_TableWidget(object):
    def setupUi(self, TableWidget):
        if not TableWidget.objectName():
            TableWidget.setObjectName(u"TableWidget")
        TableWidget.resize(1058, 645)
        TableWidget.setStyleSheet(u"QWidget {\n"
"    color: #ffffff;\n"
"}\n"
".QWidget {\n"
"	margin: 5px;\n"
"}\n"
"QTabBar::tab:hover {\n"
"    color:  #51FDBA;\n"
"}\n"
"QWidget#tab,\n"
"QWidget#tab_2 {\n"
"    background-color: #002949;\n"
"}\n"
"QWidget#TableWidget{\n"
"background: qlineargradient(\n"
"        spread:pad,\n"
"        x1:0, y1:0,\n"
"        x2:1, y2:0,\n"
"        stop:0   #0C0C31,     \n"
"        stop:0.5 #06032E,     \n"
"        stop:1   #0C0C31     \n"
"    );	\n"
"}\n"
"\n"
"QTabWidget::pane {\n"
"  border: 1px solid #002949;\n"
"  top:-1px; \n"
"  background: #002949;\n"
"} \n"
"\n"
"QTabBar::tab {\n"
"  background: #041c3d; \n"
"  border: 1px solid #041c3d; \n"
"  /* Round only the top-left and top-right corners */\n"
"    border-top-left-radius: 10px;\n"
"    border-top-right-radius: 10px;\n"
"\n"
"    /* Make bottom corners square */\n"
"    border-bottom-right-radius: 0px;\n"
"    border-bottom-left-radius: 0px;\n"
"  padding: 15px;\n"
"} \n"
"\n"
"QTabBar::tab:selected { \n"
"  background: #002949; \n"
"  marg"
                        "in-bottom: -1px; \n"
"}\n"
".QWidget {\n"
"	background-color: #091539;\n"
"}\n"
"\n"
"QLineEdit,  QGroupBox {\n"
"    background-color: #041c3d;\n"
"    color: #ffffff;\n"
"    border: 1px solid #2a628f;\n"
"    padding: 8px 4px;\n"
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
"    font-weight: bold;\n"
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
"QComboBox QAbstractItemView {\n"
"   background-color: #041c3d;\n"
"   color: #ffffff;\n"
"   border: 1px solid #2a628f;\n"
"   padding: 8px;\n"
"   border-radius: 4px;\n"
"   selection-background-co"
                        "lor: #555;\n"
"   selection-color: #fff;\n"
"	outline: 0;\n"
"}\n"
"\n"
"QComboBox QAbstractItemView::item:hover {\n"
"    background-color: #15415A;\n"
"	outline: 0;\n"
"}\n"
"QComboBox QAbstractItemView::item:selected {\n"
"    background-color: #15415A;\n"
"	outline: 0;\n"
"	\n"
"}\n"
"\n"
"QRadioButton::hover {\n"
"color: #51FDBA;\n"
"}\n"
"\n"
"\n"
"QLineEdit:disabled  {\n"
"    color: #45CACB;\n"
"}\n"
"QLabel:disabled QLabel {\n"
"     color: #45CACB;\n"
"}\n"
"QSpinBox, QDateEdit, QTimeEdit, QComboBox{\n"
"    background-color: #002949;\n"
"    color: #ffffff;\n"
"    padding: 5px 15px;\n"
"}\n"
"QSpinBox:hover,\n"
"QDateEdit:hover,\n"
"QTimeEdit:hover,\n"
"QComboBox:hover {\n"
"    color: #51FDBA;\n"
"}\n"
"\n"
"QTableView, QTableWidget {\n"
"    background-color:  #041c3d;\n"
"          /* Table body */\n"
"    gridline-color: transparent;        /* Hide grid lines if desired */\n"
"}\n"
"\n"
"QHeaderView::section {\n"
"    background-color: #041c3d;          /* Header sections */\n"
"    color: whit"
                        "e;                       /* Header text color for good contrast */\n"
"    border: none;                       /* Remove default header borders */\n"
"}\n"
"\n"
"QTableCornerButton::section {\n"
"    background-color:#041c3d;         /* Top-left corner area */\n"
"    border: none;\n"
"}\n"
"QTableWidget, QTableView {\n"
"    border: 2px solid #45CACB;       /* Light teal border around the entire table */\n"
"	border-radius: 5px;\n"
"    gridline-color: #45CACB;         /* Match the grid lines to the border color for consistency */\n"
"}\n"
"\n"
"")
        self.verticalLayout_2 = QVBoxLayout(TableWidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.widget_5 = QWidget(TableWidget)
        self.widget_5.setObjectName(u"widget_5")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_5.sizePolicy().hasHeightForWidth())
        self.widget_5.setSizePolicy(sizePolicy)
        self.widget_5.setStyleSheet(u"")
        self.verticalLayout = QVBoxLayout(self.widget_5)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(self.widget_5)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setUnderline(False)
        font.setStrikeOut(False)
        font.setStyleStrategy(QFont.PreferDefault)
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout.addWidget(self.label)

        self.comboBox = QComboBox(self.widget_5)
        self.comboBox.setObjectName(u"comboBox")
        self.comboBox.setMaximumSize(QSize(16777215, 16777215))

        self.verticalLayout.addWidget(self.comboBox)

        self.tabWidget = QTabWidget(self.widget_5)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.verticalLayout_3 = QVBoxLayout(self.tab)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.tableWidget = QTableWidget(self.tab)
        self.tableWidget.setObjectName(u"tableWidget")
        sizePolicy.setHeightForWidth(self.tableWidget.sizePolicy().hasHeightForWidth())
        self.tableWidget.setSizePolicy(sizePolicy)

        self.verticalLayout_3.addWidget(self.tableWidget)

        self.graphButton = QPushButton(self.tab)
        self.graphButton.setObjectName(u"graphButton")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.graphButton.sizePolicy().hasHeightForWidth())
        self.graphButton.setSizePolicy(sizePolicy1)
        self.graphButton.setMaximumSize(QSize(16777215, 100))

        self.verticalLayout_3.addWidget(self.graphButton)

        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.verticalLayout_4 = QVBoxLayout(self.tab_2)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.tableWidget_2 = QTableWidget(self.tab_2)
        self.tableWidget_2.setObjectName(u"tableWidget_2")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.tableWidget_2.sizePolicy().hasHeightForWidth())
        self.tableWidget_2.setSizePolicy(sizePolicy2)

        self.verticalLayout_4.addWidget(self.tableWidget_2)

        self.graphButton_2 = QPushButton(self.tab_2)
        self.graphButton_2.setObjectName(u"graphButton_2")
        sizePolicy1.setHeightForWidth(self.graphButton_2.sizePolicy().hasHeightForWidth())
        self.graphButton_2.setSizePolicy(sizePolicy1)
        self.graphButton_2.setMaximumSize(QSize(16777215, 100))

        self.verticalLayout_4.addWidget(self.graphButton_2)

        self.tabWidget.addTab(self.tab_2, "")

        self.verticalLayout.addWidget(self.tabWidget)


        self.verticalLayout_2.addWidget(self.widget_5)


        self.retranslateUi(TableWidget)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(TableWidget)
    # setupUi

    def retranslateUi(self, TableWidget):
        TableWidget.setWindowTitle(QCoreApplication.translate("TableWidget", u"Form", None))
        self.label.setText(QCoreApplication.translate("TableWidget", u"Optimization results", None))
        self.graphButton.setText(QCoreApplication.translate("TableWidget", u"Back to graphs", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("TableWidget", u"Cost metrics", None))
        self.graphButton_2.setText(QCoreApplication.translate("TableWidget", u"Return to graphs", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("TableWidget", u"Energy metrics", None))
    # retranslateUi

