from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6 import uic
import numpy as np
import pandas as pd
from itertools import combinations
import sys


def pol2cart(r, theta):  # define function polar form <--> cartesian
    z = r * np.exp(1j * (theta * np.pi / 180))
    x, y = z.real, z.imag
    return complex(x, y)


def cart2pol(x, y):
    z = x + y * 1j
    r, theta_rad = np.abs(z), np.angle(z)
    theta = theta_rad * 180 / np.pi
    return r, theta


def cal_distance(xa, xb, ya, yb):  # *function find Distance between 2 point
    distance = np.sqrt((xa - xb) ** 2 + (ya - yb) ** 2)
    return distance


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("ui/MainCal.ui", self)
        self.help_w = HelpWindow()
        self.about_w = AboutWindow()
        # Font Setup For ErrorDialog
        font = QFont()
        font.setFamily("Leelawadee UI")
        font.setPointSize(12)
        self.error_dialog = QErrorMessage()
        self.error_dialog.setFont(font)
        # define Var
        self.case = None
        self.r_115 = 0.012825
        self.r_22 = 0.00799
        self.gmr_115 = 0.05069
        self.line_current_115 = 1606.539
        self.line_current_22 = 8397.8
        self.EPSILON_0 = 8.854 * pow(10, -12)
        self.v_safe = 12000
        # event control
        self.actionHelp.triggered.connect(self.help_clicked)
        self.actionAbout_US.triggered.connect(self.about_clicked)
        self.calculate_btn.clicked.connect(self.calculate_clicked)

    def help_clicked(self):
        self.help_w.show()

    def about_clicked(self):
        self.about_w.show()

    def calculate_clicked(self):
        if self.case1.isChecked():
            self.case = 1
            self.maincalc()
        elif self.case2.isChecked():
            self.case = 2
            self.maincalc()
        elif self.case3.isChecked():
            self.case = 3
            self.maincalc()
        elif self.case4.isChecked():
            self.case = 4
            self.maincalc()
        elif self.case5.isChecked():
            self.case = 5
            self.maincalc()
        elif self.case6.isChecked():
            self.case = 6
            self.maincalc()
        else:
            self.error_dialog.showMessage(
                'Please Select electric pole type \n กรุณาเลือกชนิดของเสาไฟฟ้าที่ต้องการคำนวณ')

    def maincalc(self):
        obj_size = float(self.conduc_size.text())
        inter_h = float(self.inter_y.text())
        inter_x = float(self.inter_x.text())
        range_x = float(self.max_h.text())
        range_y = float(self.max_dis.text())
        self.testlabel.setText("Finish")


class HelpWindow(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("ui/Help.ui", self)


class AboutWindow(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("ui/About.ui", self)


app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec()
