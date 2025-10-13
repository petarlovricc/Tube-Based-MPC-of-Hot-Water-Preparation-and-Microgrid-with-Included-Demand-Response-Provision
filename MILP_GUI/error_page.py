import sys
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QLabel,
    QWidget,
    QProgressBar
)
from .ErrorWidget import Ui_ErrorWidget
from PySide6.QtGui import QResizeEvent, QFont, QShowEvent


class ErrorPage(QWidget, Ui_ErrorWidget):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        

    def loop_through_widgets(self, font):
        for widget in self.findChildren(QWidget):
            widget.setFont(font)

        buttonfont = self.pushButton.font()
        buttonfont.setPointSize(font.pointSize()*20/70*1.2)
        self.pushButton.setFont(buttonfont)
        
    
    def resizeEvent(self, event: QResizeEvent):
                super().resizeEvent(event)
                
                # Heuristic: base size on window height
                h = self.height()
                new_pt = max(9, h / 20)  # adjust divisor as needed
                font = self.font()
                font.setBold(True)
                font.setPointSizeF(new_pt)
                self.loop_through_widgets(font)
                print(new_pt)

    def showEvent(self, event: QShowEvent):
                super().showEvent(event)
                
                # Heuristic: base size on window height
                h = self.height()
                new_pt = max(9, h / 20)  # adjust divisor as needed
                font = self.font()
                font.setBold(True)
                font.setPointSizeF(new_pt)
                self.loop_through_widgets(font)
               
    
        

