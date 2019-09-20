from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtCore
import sys, time, random, json


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.title = "CoCCA"
        self.top = 200
        self.left = 500
        self.width = 400
        self.height = 300
        self.size=QtCore.QSize(480,400)
        self.setWindowIcon(QtGui.QIcon("icon.png"))
        self.setWindowTitle(self.title)
        self.img2=QLabel(self)
        self.img2.setText("2")
        self.img2.setAlignment(QtCore.Qt.AlignCenter)
        self.movie2 = QtGui.QMovie("giphy.gif")
        self.img2.setMovie(self.movie2)
        self.movie2.setScaledSize(self.size)
        self.movie2.start()
        self.enter=QPushButton(self)
        self.enter.setText("Enter CoCCA")
        self.enter.setFont(self.font())

        self.font = QtGui.QFont()
        self.font.setPointSize(18)
        self.font.setBold(True)
        self.font.setWeight(75)

        self.dialog = Second(self)


        vbox = QVBoxLayout()
        grid = QGridLayout()
        grid.addWidget(self.img2,1,1)
        grid.addWidget(self.enter,2,1)
        self.setLayout(grid)
        self.show()

        self.enter.clicked.connect(self.enter_cocca)

    def enter_cocca(self):
        print("Ciao")
        self.dialog.show()


class Second(QWidget):
    def __init__(self, parent=None):
        super(Second, self).__init__(parent)
        



   
















App = QApplication(sys.argv)
window = Window()
sys.exit(App.exec())