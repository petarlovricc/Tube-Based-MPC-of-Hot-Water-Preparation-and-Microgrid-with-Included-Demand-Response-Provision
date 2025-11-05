import sys
import psutil, os
from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import (
    QLabel,
    QWidget,
    QProgressBar
)
from .LoadingScreen import Ui_LoadingScreen
from PySide6.QtGui import QFont, QResizeEvent, QShowEvent
from MILP_formulation.histereza import runHistereza
from MILP_GUI.utils import check_cplex_full_version
from PySide6.QtWidgets import QLabel, QWidget, QSpacerItem, QSizePolicy, QVBoxLayout
from docplex.mp.environment import Environment
class LoadingPage(QWidget, Ui_LoadingScreen):
    def __init__(self, paramPage):
        super().__init__()
        self.setupUi(self)
        self.paramPage = paramPage
       
        # === Spacer prije glavnog teksta (gura ga prema dolje) ===
        topSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout.insertItem(0, topSpacer)

        # === Spacer ispod glavnog teksta (da ga centrira) ===
        bottomSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout.addItem(bottomSpacer)

        # === RAM usage labela fiksno dolje ===
        self.ramLabel = QLabel("RAM usage: 0 MB", self)
        self.ramLabel.setStyleSheet("color: white; font-weight: bold;")
        self.ramLabel.setAlignment(Qt.AlignCenter)
        self.verticalLayout.addWidget(self.ramLabel, alignment=Qt.AlignCenter)

        # Timer za RAM usage
        self.ramTimer = QTimer(self)
        self.ramTimer.timeout.connect(self.updateRamUsage)
        self.ramTimer.start(2000)

        
    

    def loop_through_widgets(self, font):
        for widget in self.findChildren(QWidget):
            widget.setFont(font)

    def resizeEvent(self, event: QResizeEvent):
        super().resizeEvent(event)
        h = self.height()
        new_pt = max(9, h / 20)
        font = self.font()
        font.setBold(True)
        font.setPointSizeF(new_pt)
        self.loop_through_widgets(font)

    def showEvent(self, event: QShowEvent):
        super().showEvent(event)
        h = self.height()
        new_pt = max(9, h / 20)
        font = self.font()
        font.setBold(True)
        font.setPointSizeF(new_pt)
        self.loop_through_widgets(font)

    def updateRamUsage(self):
        """Update RAM usage label with current process memory usage"""
        process = psutil.Process(os.getpid())
        mem = process.memory_info().rss / (1024 * 1024)  # MB
        self.ramLabel.setText(f"RAM usage: {mem:.2f} MB")
