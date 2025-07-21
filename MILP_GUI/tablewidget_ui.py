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
    QPushButton, QSizePolicy, QTableWidget, QTableWidgetItem,
    QVBoxLayout, QWidget)

class Ui_TableWidget(object):
    def setupUi(self, TableWidget):
        if not TableWidget.objectName():
            TableWidget.setObjectName(u"TableWidget")
        TableWidget.resize(944, 509)
        self.verticalLayout_2 = QVBoxLayout(TableWidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.widget_5 = QWidget(TableWidget)
        self.widget_5.setObjectName(u"widget_5")
        self.widget_5.setStyleSheet(u"QWidget #widget_5 {\n"
"	background-color: rgba(245, 245, 245, 0.9);\n"
"	border-radius: 8px;\n"
"	border-style:dotted;\n"
"}\n"
"")
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
        self.label.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.label)

        self.comboBox = QComboBox(self.widget_5)
        self.comboBox.setObjectName(u"comboBox")

        self.verticalLayout.addWidget(self.comboBox)

        self.tableWidget = QTableWidget(self.widget_5)
        self.tableWidget.setObjectName(u"tableWidget")

        self.verticalLayout.addWidget(self.tableWidget)

        self.graphButton = QPushButton(self.widget_5)
        self.graphButton.setObjectName(u"graphButton")

        self.verticalLayout.addWidget(self.graphButton)


        self.verticalLayout_2.addWidget(self.widget_5)


        self.retranslateUi(TableWidget)

        QMetaObject.connectSlotsByName(TableWidget)
    # setupUi

    def retranslateUi(self, TableWidget):
        TableWidget.setWindowTitle(QCoreApplication.translate("TableWidget", u"Form", None))
        self.label.setText(QCoreApplication.translate("TableWidget", u"REZULTATI OPTIMIZACIJE", None))
        self.graphButton.setText(QCoreApplication.translate("TableWidget", u"Povratak", None))
    # retranslateUi

