from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import numpy
import os
import sys
import qdarkstyle

class JointWidget(QWidget):
    #valueChanged = pyqtSignal(int)  # Emit the new joint value
    def __init__(self,title,min,max):
        super().__init__()
        self.title = title
        self.min = min
        self.max = max
        self.value = 0
        self.setMaximumWidth(300)
        self.title_lbl = QLabel(title)
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(self.min,self.max)
        self.slider.valueChanged.connect(self.changed_value)
        self.slider.setValue(0)
        self.input_box = QSpinBox()
        self.input_box.setRange(self.min,self.max)
        self.input_box.valueChanged.connect(self.changed_box_value)
        self.input_box.setValue(0)
        self.set_layout()
    def update_values(self,val):
        val = int(val)
        self.input_box.setValue(val)
        self.value = val
        self.slider.setValue(val)
        print("here----->")
    def changed_value(self,val):
        self.input_box.setValue(val)
        self.value = val
        #self.valueChanged.emit(val)
    def changed_box_value(self,val):
        self.slider.setValue(val)
        self.value = val
        #self.valueChanged.emit(val)
    def set_layout(self):
        self.main_ly = QVBoxLayout()
        self.title_ly = QHBoxLayout()
        self.title_ly.addStretch()
        self.title_ly.addWidget(self.title_lbl)
        self.title_ly.addStretch()
        self.title_ly.addStretch()
        self.main_ly.addLayout(self.title_ly)
        self.main_h_ly = QHBoxLayout()
        self.main_h_ly.addWidget(self.slider)
        self.main_h_ly.addWidget(self.input_box)
        self.main_ly.addLayout(self.main_h_ly)
        self.style()
        self.setLayout(self.main_ly)

    def style(self):
        self.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        self.setStyleSheet("""QLabel{color:white;font:bold 18px;}
        QSlider {
                border-radius: 10px;
            }
            QSlider::groove:horizontal {
                height: 5px;
                background: #00A2FF;
                border-radius: 2px;
            }
            QSlider::handle:horizontal {
                background: #00A2FF;
                width: 16px;
                height: 16px;
                margin: -6px 0;
                border-radius: 8px;
            }
            QSlider::sub-page:horizontal {
                background: #00A2FF;
            }
         QSpinBox{
        color:#fff;
        background-color:#19232D;
        min-height:1.5em;
        border-radius:5px;
        min-width:3em;
        font: bold 14px;

        }
        
        
        """)
