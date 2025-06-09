import sys
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QLabel,
    QWidget,
    QProgressBar
)
from .LoadingScreen import Ui_LoadingScreen

class LoadingPage(QWidget, Ui_LoadingScreen):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
        

