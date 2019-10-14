from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtCore
import sys, time, random, json, coor, inpgen, neigh_find_gui, visualizer
#import const_gen_ui as CGU



class First(QMainWindow):
    def __init__(self, parent=None):
        super(First, self).__init__(parent)
        self.size=QtCore.QSize(500,800)
        self.finestra = Window(self)
        self.finestra.resize(self.size)
        self.title="CoCCA"


        self.setCentralWidget(self.finestra)
        self.setWindowTitle(self.title)

        self.setStyleSheet("""
            QPushButton{
                border: 2px solid #8f8f91;
                border-radius: 6px;
                background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                      stop: 0 #f6f7fa, stop: 1 #dadbde);
                min-width: 80px;
            }

            QLabel{

            color: "white";
            }
            QCheckBox{

            color: "white";
            }
            
             QMainWindow{

                background-color:#4d4d4d



            }

            
                           """)


class Window(QWidget):
    def __init__(self,parent):
        super(Window, self).__init__(parent)
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
        if self.anal.isChecked():
            self.dialog = neigh_find_gui.Third()
        elif self.data.isChecked():
            self.dialog = visualizer.Fourth()
        else:
            self.dialog = inpgen.Second()
        print("Ciao")
        self.dialog.resize(self.size2)
        self.dialog.show()























App = QApplication(sys.argv)
window = First()
window.show()
sys.exit(App.exec())
