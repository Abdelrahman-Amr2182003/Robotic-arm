from roboticstoolbox.backends.PyPlot import PyPlot
import roboticstoolbox as rtb
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import numpy
import os
import sys
import matplotlib.pyplot as plt
from roboticstoolbox import RevoluteDH, PrismaticDH

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class RobotWidget(QWidget):
    def __init__(self, robot_properties, parent=None):
        super().__init__(parent)

        self.robot = self.create_robot(robot_properties)

        # Create the Robotics Toolbox environment with improved visual settings
        self.env = PyPlot()
        self.env.launch()

        # Define a robot using Peter Corke's Robotics Toolbox
        #robot = rtb.models.DH.Puma560()

        # Plot the robot using the initial configuration
        self.env.add(self.robot)
        #robot.plot(robot.qz, block=False)

        # Integrate the matplotlib figure into the PyQt5 layout
        #widget = QWidget()
        layout = QVBoxLayout()
        self.canvas = self.env.fig.canvas
        layout.addWidget(self.canvas)

        # Add a navigation toolbar for zooming and panning
        #self.add_navigation_toolbar(layout)

        self.setLayout(layout)
        #self.setCentralWidget(widget)
        #self.show()

    def create_robot(self, properties):
        links = []
        for prop in properties:
            link = RevoluteDH(a=prop['a'], alpha=prop['alpha'], d=prop['d'], offset=prop['offset'])
            link.qlim = prop['qlim']
            links.append(link)
        return rtb.DHRobot(links)
    def create_custom_figure(self):
        # Custom figure settings
        fig = plt.figure(figsize=(8, 6), dpi=100)
        plt.style.use('ggplot')  # Example style
        return fig

    def add_navigation_toolbar(self, layout):
        # Add matplotlib navigation toolbar for interactivity
        toolbar = NavigationToolbar(self.canvas, self)
        layout.addWidget(toolbar)