from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtCore
import sys, time, random, json, coor, inpgen
#import const_gen_ui as CGU






class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.title = "CoCCA"
        self.top = 200
        self.left = 500
        self.width = 400
        self.height = 300
        self.size=QtCore.QSize(480,400)
        self.size2=QtCore.QSize(1000,500)
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

        self.data=QCheckBox()
        self.data.setText("Data Manipulation")
        #self.data.setAlignment(Qt.AlignCenter)

        self.anal=QCheckBox()
        self.anal.setText("Analysis")

        self.input=QCheckBox()
        self.input.setText("Input Generation")

        self.group1=QButtonGroup()
        self.group1.addButton(self.data)
        self.group1.addButton(self.anal)
        self.group1.addButton(self.input)


        self.font = QtGui.QFont()
        self.font.setPointSize(18)
        self.font.setBold(True)
        self.font.setWeight(75)

        self.font_smaller = QtGui.QFont()
        self.font_smaller.setPointSize(16)
        self.font_smaller.setWeight(50)
        self.data.setFont(self.font_smaller)
        self.anal.setFont(self.font_smaller)
        self.input.setFont(self.font_smaller)




        vbox = QVBoxLayout()
        grid = QGridLayout()
        grid.addWidget(self.img2,0,0,1,3)
        grid.addWidget(self.data,1,0)
        grid.addWidget(self.anal,1,1)
        grid.addWidget(self.input,1,2)
        grid.addWidget(self.enter,2,0,1,3)
        self.setLayout(grid)
        self.show()

        self.enter.clicked.connect(self.enter_cocca)

    def enter_cocca(self):
        self.dialog = data.Second()
        print("Ciao")
        self.dialog.resize(self.size2)
        self.dialog.show()























App = QApplication(sys.argv)
window = Window()
sys.exit(App.exec())
