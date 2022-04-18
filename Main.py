from PyQt6.QtWidgets import *
from PyQt6 import uic
import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.help_w = HelpWindow()
        self.about_w = AboutWindow()
        uic.loadUi("ui/MainCal.ui", self)
        self.actionHelp.triggered.connect(self.help_clicked)
        self.actionAbout_US.triggered.connect(self.about_clicked)
        self.calculate_btn.clicked.connect(self.calculate_clicked)

    def help_clicked(self):
        self.help_w.show()

    def about_clicked(self):
        self.about_w.show()

    def calculate_clicked(self):
        if self.case1.isChecked():
            self.testlabel.setText("1")
        elif self.case2.isChecked():
            self.testlabel.setText("2")
        elif self.case3.isChecked():
            self.testlabel.setText("3")
        elif self.case4.isChecked():
            self.testlabel.setText("4")
        elif self.case5.isChecked():
            self.testlabel.setText("5")
        elif self.case6.isChecked():
            self.testlabel.setText("6")


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
