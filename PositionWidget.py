from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import numpy
import os
import sys
import qdarkstyle

class PositionWidget(QWidget):
    #positionChanged = pyqtSignal(float)  # Emit the new position value
    def __init__(self,title,min,max):
        super().__init__()
        self.title = title
        self.setMaximumWidth(300)
        self.title_lbl = QLabel(title)
        self.value = QDoubleSpinBox()
        self.value.setRange(min,max)
        self.set_layout()
    def setValue(self,val):
        self.value.setValue(val)



    def set_layout(self):
        self.main_ly = QVBoxLayout()
        self.main_ly.addWidget(self.title_lbl)
        self.main_ly.addWidget(self.value)
        self.main_ly.addStretch()
        self.style()
        self.setLayout(self.main_ly)
    def style(self):
        self.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        self.setStyleSheet("""
            QLabel{
                color:white;
                font:bold 16px;
            }
            QDoubleSpinBox{
                color:#fff;
                background-color:#19232D;
                min-height:1.5em;
                border-radius:5px;
                min-width:3em;
                font: bold 14px;
        }
                    
        """)