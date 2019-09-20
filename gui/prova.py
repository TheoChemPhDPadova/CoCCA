from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtCore
import sys, time, random, json

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
        self.layout=QVBoxLayout()
        self.button=QPushButton("Push")
        self.button2=QPushButton("Pull")
        self.text=QTextEdit()

        self.lista=QListWidget()
        for i in range(4):
            self.lista.addItem(str(i))

        

        self.button.clicked.connect(self.push)
        self.button2.clicked.connect(self.pull)


        self.layout.addWidget(self.text)
        self.layout.addWidget(self.button)
        self.layout.addWidget(self.button2)
        self.layout.addWidget(self.lista)
        self.setLayout(self.layout)


    def pull(self):
        self.lista.clear()
    def push(self):
        k=4#self.text.toPlainText()
        for i in range(int(k)):
            self.lista.addItem(str(i))


App = QApplication(sys.argv)
window = First()
window.show()
sys.exit(App.exec())







