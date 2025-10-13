# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'errorwidget.ui'
##
## Created by: Qt User Interface Compiler version 6.5.3
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
from PySide6.QtWidgets import (QApplication, QLabel, QPushButton, QSizePolicy,
    QVBoxLayout, QWidget)

class Ui_ErrorWidget(object):
    def setupUi(self, ErrorWidget):
        if not ErrorWidget.objectName():
            ErrorWidget.setObjectName(u"ErrorWidget")
        ErrorWidget.resize(947, 809)
        ErrorWidget.setStyleSheet(u"QWidget {\n"
"    color: #ffffff;\n"
"}\n"
".QWidget {\n"
"	margin: 5px;\n"
"}\n"
"QWidget#ErrorWidget{\n"
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
"QPushButton {\n"
"	background-color: #43A499;\n"
"}\n"
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
""
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
"   selection-background-color: #555;\n"
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
"    background-color: #041c3d;\n"
"    color: #ffffff;\n"
""
                        "    padding: 5px 15px;\n"
"}\n"
"QSpinBox:hover,\n"
"QDateEdit:hover,\n"
"QTimeEdit:hover,\n"
"QComboBox:hover {\n"
"    color: #51FDBA;\n"
"}\n"
"")
        self.verticalLayout = QVBoxLayout(ErrorWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(ErrorWidget)
        self.label.setObjectName(u"label")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        font = QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setStrikeOut(False)
        font.setKerning(True)
        font.setStyleStrategy(QFont.PreferDefault)
        self.label.setFont(font)
        self.label.setStyleSheet(u"")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout.addWidget(self.label)

        self.pushButton = QPushButton(ErrorWidget)
        self.pushButton.setObjectName(u"pushButton")
        sizePolicy1 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())
        self.pushButton.setSizePolicy(sizePolicy1)
        self.pushButton.setMaximumSize(QSize(16777215, 100))

        self.verticalLayout.addWidget(self.pushButton)

        self.verticalLayout.setStretch(0, 1)

        self.retranslateUi(ErrorWidget)

        QMetaObject.connectSlotsByName(ErrorWidget)
    # setupUi

    def retranslateUi(self, ErrorWidget):
        ErrorWidget.setWindowTitle(QCoreApplication.translate("ErrorWidget", u"Form", None))
        self.label.setText(QCoreApplication.translate("ErrorWidget", u"Error page", None))
        self.pushButton.setText(QCoreApplication.translate("ErrorWidget", u"Return", None))
    # retranslateUi

