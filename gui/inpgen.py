from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtCore
import sys, time, random, json, coor, common, subprocess
from subprocess import check_output

class Second(QMainWindow):
    def __init__(self, parent=None):
        super(Second, self).__init__(parent)
        self.size=QtCore.QSize(500,800)
        self.form_widget = FormWidget(self)
        self.form_widget.resize(self.size)


        self.setCentralWidget(self.form_widget)

class FormWidget(QWidget):

    def __init__(self, parent):
        super(FormWidget, self).__init__(parent)

        self.layout=QGridLayout(self)
        self.resize(800,800)

        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()


        # Add tabs
        self.tabs.addTab(self.tab1,"Constraint Generator")
        self.tabs.addTab(self.tab2,"NEB Visualizer")

        # Create first tab
        self.tab1.layout = QGridLayout(self)
        self.pushButton1 = QPushButton("Create Input")
        self.const_elem_te=QTextEdit()
        self.const_elem=QLabel("Element to constrain")
        self.const_elem_num_te=QTextEdit()
        self.const_elem_num=QLabel("Atoms to constrain")
        self.file_path_te=QTextEdit()
        self.file_path=QLabel("Path to xyz file")
        self.file_out=QTextEdit()
        self.pippo=QTextEdit()
        self.gaussian=QCheckBox("Gaussian")
        self.gaussian.setChecked(True)
        self.ORCA=QCheckBox("ORCA")
        self.XTB=QCheckBox("XTB")
        self.unconstrain=QLabel("Atoms to un-constrain")
        self.unconstrain_te=QTextEdit()
        self.fileout=QLabel("Label")
        self.fileout.setAlignment(QtCore.Qt.AlignCenter)

        self.layout2=QVBoxLayout()
        self.layout3=QVBoxLayout()

        self.group2=QButtonGroup()
        self.group2.addButton(self.ORCA)
        self.group2.addButton(self.XTB)
        self.group2.addButton(self.gaussian)


        self.tab1.layout.addWidget(self.const_elem_te,1,1,1,2)
        self.tab1.layout.addWidget(self.const_elem,1,0,1,1)
        self.tab1.layout.addWidget(self.const_elem_num_te,2,1,1,2)
        self.tab1.layout.addWidget(self.const_elem_num,2,0,1,1)
        self.tab1.layout.addWidget(self.unconstrain,3,0,1,1)
        self.tab1.layout.addWidget(self.unconstrain_te,3,1,1,2)
        self.tab1.layout.addWidget(self.file_path_te,4,1,1,2)
        self.tab1.layout.addWidget(self.file_path,4,0,1,1)
        self.tab1.layout.addWidget(self.gaussian,0,0,1,1)
        self.tab1.layout.addWidget(self.ORCA,0,1,1,1)
        self.tab1.layout.addWidget(self.XTB,0,2,1,1)
        self.tab1.layout.addWidget(self.pushButton1,5,0,1,3)
        self.tab1.layout.addWidget(self.pippo,0,4,5,1)
        self.tab1.layout.addWidget(self.fileout,5,3,1,2)



        self.tab1.setLayout(self.tab1.layout)

        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

        text=str("ciao\n")
        self.pushButton1.clicked.connect(self.constgen)

################TAB2############################
        self.tab2.layout=QVBoxLayout()
        self.tab2.label=QLabel("Enter path to .interp file")
        self.tab2.path_te=QTextEdit()
        policy = self.tab2.path_te.sizePolicy()
        policy.setVerticalPolicy(QSizePolicy.Minimum)
        self.tab2.path_te.setSizePolicy(policy)
        self.tab2.button=QPushButton("GO")

    

        self.tab2.layout.addWidget(self.tab2.label)
        self.tab2.layout.addWidget(self.tab2.path_te)
        self.tab2.layout.addStretch()
        self.tab2.layout.addWidget(self.tab2.button)
        self.tab2.setLayout(self.tab2.layout)

        self.tab2.button.clicked.connect(self.neb_viz)
    



##############FUNCTIONS##########################

    def appendi(self, text):
        self.pippo.setText("")
        cursor = self.pippo.textCursor()
        cursor.movePosition(cursor.End)
        cursor.insertText(text)
        #cursor.insertText("\n")

    def constgen(self):
        input= self.file_path_te.toPlainText()
        CE= self.const_elem_te.toPlainText()
        CN=self.const_elem_num_te.toPlainText()
        UN=self.unconstrain_te.toPlainText()
        soft="0"
        if self.ORCA.isChecked():
            soft="1"
        elif self.gaussian.isChecked():
            soft="2"
        elif self.XTB.isChecked():
            soft="3"
        s = open(input+"_constraints","w+")
        args=["python","const_gen_parser.py","--noint", "--input",input,"--CE",CE,"--CN",CN,"--UN",UN,"--soft",soft]
        out = check_output(args, encoding="437")
        print(str(out))
        #out, err = p.commmunicate()

        #subprocess.Popen(args, stdout=s) 
        #self.appendi("CIAO")
        #s.close()
        #j=open(input+"_constraints","r")
        #lines=j.readlines()
        #for line in lines:
        self.appendi(str(out))
            #self.appendi("ciao")
        self.fileout.setText("Constraints printed to file: " + input + "_constraints" )
        s.write(out)
        s.close()
        #s.close()

    def neb_viz(self):
        path=self.tab2.path_te.toPlainText()
        print(path)
        args=["python", "neb_viz.py","--input", path]
        subprocess.Popen(args) 



    