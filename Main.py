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

    def help_clicked(self):
        self.help_w.show()

    def about_clicked(self):
        self.about_w.show()


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
