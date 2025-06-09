# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'loadingscreen.ui'
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
from PySide6.QtWidgets import (QApplication, QLabel, QListWidget, QListWidgetItem,
    QProgressBar, QSizePolicy, QWidget)

class Ui_LoadingScreen(object):
    def setupUi(self, LoadingScreen):
        if not LoadingScreen.objectName():
            LoadingScreen.setObjectName(u"LoadingScreen")
        LoadingScreen.resize(1025, 600)
        self.progressBar = QProgressBar(LoadingScreen)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setGeometry(QRect(290, 180, 441, 51))
        self.progressBar.setValue(24)
        self.listWidget = QListWidget(LoadingScreen)
        self.listWidget.setObjectName(u"listWidget")
        self.listWidget.setGeometry(QRect(280, 250, 441, 201))
        self.label = QLabel(LoadingScreen)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(400, 130, 181, 41))
        font = QFont()
        font.setPointSize(12)
        self.label.setFont(font)

        self.retranslateUi(LoadingScreen)

        QMetaObject.connectSlotsByName(LoadingScreen)
    # setupUi

    def retranslateUi(self, LoadingScreen):
        LoadingScreen.setWindowTitle(QCoreApplication.translate("LoadingScreen", u"Form", None))
        self.label.setText(QCoreApplication.translate("LoadingScreen", u"Izvr\u0161avanje optimizacije...", None))
    # retranslateUi

