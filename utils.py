def stack_h_ly(elems):
    h_ly = QHBoxLayout()
    for elem in elems:
        if elem == 'strech':
            h_ly.addStretch()
        else:
            h_ly.addWidget(elem)
    return h_ly

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import qdarkstyle
def stack_v_ly(elems):
    v_ly = QVBoxLayout()
    for elem in elems:
        if elem == 'strech':
            v_ly.addStretch()
        else:
            v_ly.addWidget(elem)
    return v_ly


def stack_ly_v_ly(elems):
    v_ly = QVBoxLayout()
    for elem in elems:
        if elem == 'strech':
            v_ly.addStretch()
        else:
            v_ly.addLayout(elem)
    return v_ly


def stack_ly_h_ly(elems):
    h_ly = QHBoxLayout()
    for elem in elems:
        if elem == 'strech':
            h_ly.addStretch()
        else:
            h_ly.addLayout(elem)
    return h_ly