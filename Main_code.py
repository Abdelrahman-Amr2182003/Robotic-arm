from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import numpy
import os
import sys
import qdarkstyle
from Jointwidget import JointWidget
from PositionWidget import PositionWidget
from utils import *
from RobotWidget import RobotWidget
import numpy as np
import matplotlib.pyplot as plt
from spatialmath import SE3
from serial import Serial
import time as T


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(800,800)
        self.x = 0
        self.y = 0
        self.z = 0
        self.gripper_angle = 0
        self.setWindowTitle("Robotic arm controll Program")
        self.ser_connected = False
        self.ser = None
        self.gripper_open = False






        self.refresh_serial()


        self.j1_w = JointWidget("Joint 1",0,180)
        self.j2_w = JointWidget("Joint 2", 0, 180)
        self.j3_w = JointWidget("Joint 3", 0, 180)
        self.j4_w = JointWidget("Joint 4", 0, 180)
        self.j5_w = JointWidget("Joint 5", 0, 180)
        #self.j6_w = JointWidget("Joint 6", 0, 180)
        self.gripper_btn = QPushButton("")
        self.gripper_btn.setIcon(QIcon(os.path.join("icons", "closed_gripper.png")))
        self.gripper_btn.setIconSize(QSize(40,40))
        self.gripper_btn.setStyleSheet(self.search_btn_style())
        self.gripper_btn.clicked.connect(self.gripper_btn_fn)

        self.refresh_btn = QPushButton("")
        self.refresh_btn.setIcon(QIcon(os.path.join("icons", "refresh.png")))
        self.refresh_btn.setIconSize(QSize(40,40))
        self.refresh_btn.setStyleSheet(self.search_btn_style())
        self.refresh_btn.clicked.connect(self.refresh_serial)

        self.x_w = PositionWidget("X",0,1000)
        self.y_w = PositionWidget("Y", 0, 1000)
        self.z_w = PositionWidget("Z", 0, 1000)
        self.motors_speed = JointWidget("Motors Speed",1,100)




        robot_properties = [
            {'d': 78.3, 'a': 0, 'alpha': np.pi / 2, 'offset': 0, 'qlim': np.radians([-180, 180])},  # Joint 1
            {'a': 86.83, 'd': 0, 'alpha': 0, 'offset': 0, 'qlim': np.radians([-180, 180])},  # Joint 2
            {'a': 100.47, 'd': 0, 'alpha': 0, 'offset': 0, 'qlim': np.radians([-180, 180])},  # Joint 3
            {'d': 0, 'a': 70.13+134.49, 'alpha': np.pi / 2, 'offset': 0, 'qlim': np.radians([-180, 180])},  # Joint 4
            {'a':0 , 'd':0 , 'alpha':0, 'offset': 0, 'qlim': np.radians([-180, 180])}  # Joint 5
        ]

        self.robot_widget = RobotWidget(robot_properties)
        self.fk_btn = QPushButton("Forward Kinematics")
        self.fk_btn.clicked.connect(self.update_robot_joint)
        self.fk_btn.setStyleSheet(self.btn_style())
        self.ik_btn = QPushButton("Inverse Kienmatics")
        self.ik_btn.clicked.connect(self.update_robot_position)
        self.ik_btn.setStyleSheet(self.btn_style())
        self.set_layout()
        self.show()



    def search_btn_style(self):
        return """

           QPushButton{
               border: none;
               background: none;
               background-color:#333e50;
               min-width:50px;
               min-height:50px;
               border-radius:25px;
               max-width:50px;
               max-height:50px;
               }
               QPushButton::hover{
                   background-color:#3b495a;
               }

           """
    def btn_style(self):
        return """
            QPushButton{
                        border: 1px solid #09C7DB;
                        background-color:#052659;
                        color:white;
                        border-radius:10px;
                       min-width:10em;
                        max-width:10em;
                        min-height:2em;
                        font:bold 14px;
                        border: 1px solid #09C7DB;
                    }

                    QPushButton::hover{
                        background-color:#7DA0CA;
                        color:white;
                        border-radius:10px;
                        min-width:10em;
                        max-width:10em;
                        min-height:2em;
                        font:bold 14px;
                        }
        
        
        """
    def noop_pause(*args, **kwargs):
        pass

    def update_robot_position(self):
        # Update the corresponding coordinate based on the input axis

        self.x = self.x_w.value.value()
        self.y = self.y_w.value.value()
        self.z = self.z_w.value.value()

        # Ensure that x, y, z have been initialized; otherwise, initialize them to some default
        if hasattr(self, 'x') and hasattr(self, 'y') and hasattr(self, 'z'):
            # Create the SE3 object for the position
            T = SE3(self.x, self.y, self.z)

            # Perform IK
            q = self.robot_widget.robot.ikine_LM(T)  # Pass the SE3 object

            if q.success:
                self.robot_widget.robot.q = q.q  # Update joint angles
                self.robot_widget.env.step()  # Update the environment

                self.robot_widget.canvas.draw()  # Redraw the canvas
                self.j1_w.update_values(np.degrees(q.q[0]))
                self.j2_w.update_values(np.degrees(q.q[1]))
                self.j3_w.update_values(np.degrees(q.q[2])+90)
                self.j4_w.update_values(np.degrees(q.q[3])-90)
                self.j5_w.update_values(np.degrees(q.q[4]))
                self.send_angles_and_speed()
            else:
                pass
    def gripper_btn_fn(self):
        if not self.gripper_open:
            self.gripper_angle = 10# given that zero is closed
            self.gripper_btn.setIcon(QIcon(os.path.join("icons", "open_gripper.png")))
            self.gripper_btn.setIconSize(QSize(40,40))
            self.gripper_open = True

        else:
            self.gripper_angle = 150  # given that zero is closed
            self.gripper_btn.setIcon(QIcon(os.path.join("icons", "closed_gripper.png")))
            self.gripper_btn.setIconSize(QSize(40,40))
            self.gripper_open = False
    def refresh_serial(self):
        try:
            if self.ser_connected:
                self.ser.close()

            self.ser = Serial(port = "COM5", baudrate = 9600)
            self.ser_connected = True
            T.sleep(2)
            print("connected")
        except Exception as e:
            print("error is ",e)
            self.ser = None
            self.ser_connected = False

    def send_angles_and_speed(self):
        # Construct the message to be sent
        angles = [self.j1_w.value,self.j2_w.value,self.j2_w.value,self.j3_w.value,self.j4_w.value,self.j5_w.value,self.gripper_angle]
        speed = self.motors_speed.value
        message = ','.join(map(str, angles)) + ',' + str(speed) + '\n'
        if self.ser_connected:
            try:
                self.ser.write(message.encode())
            except Exception as e:
                print(e)
                self.refresh_serial()
                self.ser.write(message.encode())
    def update_robot_joint(self):
        original_pause = plt.pause  # Save the original function
        plt.pause = self.noop_pause  # Temporarily override plt.pause

        try:
            q_degrees = np.array([self.j1_w.value, self.j2_w.value, self.j3_w.value-90,
                                  self.j4_w.value+90, self.j5_w.value])
            q = np.radians(q_degrees)  # Convert to radians

            # Update the robot configuration
            self.robot_widget.robot.q = q
            T = self.robot_widget.robot.fkine(q)

            # Update UI elements for position
            self.x_w.value.setValue(T.t[0])
            self.y_w.value.setValue(T.t[1])
            self.z_w.value.setValue(T.t[2])

            # If the environment requires an explicit refresh or update step
            self.robot_widget.env.step()  # Update the environment if needed
            self.robot_widget.canvas.draw()
            self.send_angles_and_speed()
        finally:
            plt.pause = original_pause  # Restore the original plt.pause function
    def closeEvent(self, event):
        pass
    def style(self):
        self.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())

    def set_layout(self):
        self.main_ly = QHBoxLayout()
        self.main_ly.setAlignment(Qt.AlignTop)
        self.fk_ly = QVBoxLayout()
        self.fk_ly.addWidget(self.j1_w)
        self.fk_ly.addWidget(self.j2_w)
        self.fk_ly.addWidget(self.j3_w)
        self.fk_ly.addWidget(self.j4_w)
        self.fk_ly.addWidget(self.j5_w)
        self.fk_ly.addWidget(self.motors_speed)
        self.fk_ly.addWidget(self.fk_btn)
        self.fk_ly.addStretch(1)
        self.main_ly.addLayout(self.fk_ly)
        self.ik_ly = QVBoxLayout()
        self.ik_h_1_ly = QHBoxLayout()
        self.ik_h_1_ly.addWidget(self.x_w)
        self.ik_h_1_ly.addStretch()
        self.ik_h_1_ly.addWidget(self.refresh_btn)
        self.ik_ly.addLayout(self.ik_h_1_ly)

        self.ik_h_2_ly = QHBoxLayout()
        self.ik_h_2_ly.addWidget(self.y_w)
        self.ik_h_2_ly.addStretch()
        self.ik_h_2_ly.addWidget(self.gripper_btn)
        self.ik_ly.addLayout(self.ik_h_2_ly)


        self.ik_ly.addWidget(self.z_w)
        self.ik_ly.addWidget(self.ik_btn)

        self.ik_ly.addStretch(1)

        self.main_ly.addLayout(self.ik_ly)
        #self.main_ly.addStretch(1)
        self.main_ly.addWidget(self.robot_widget)

        self.style()
        self.setLayout(self.main_ly)

if __name__ == "__main__":
    os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "1"
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    os.environ["QT_SCALE_FACTOR"] = "1"

    app = QApplication(sys.argv)
    app.setAttribute(Qt.AA_EnableHighDpiScaling)
    mw = MainWindow()
    sys.exit(app.exec_())