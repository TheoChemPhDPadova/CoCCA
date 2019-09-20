from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtCore
import sys, time, random, json, coor, style, logging
from coor import *
import utilities as ut

class Third(QMainWindow):
    def __init__(self, parent=None):
        super(Third, self).__init__(parent)
        self.size=QtCore.QSize(500,800)
        self.form_widget = FormWidget(self)
        self.form_widget.resize(self.size)


        self.setCentralWidget(self.form_widget)

        self.setStyleSheet("""
            QPushButton{
                border: 2px solid #8f8f91;
                border-radius: 6px;
                background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                      stop: 0 #f6f7fa, stop: 1 #dadbde);
                min-width: 80px;
            }

            QPushButton:pressed{
                border: 2px solid #8f8f91;
                border-radius: 6px;
                background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                      stop: 0   #838383, stop: 1  #3a3a3a);
                min-width: 80px;
            }

            QLabel{

            color: "white";
            }

           

             QMainWindow{

                background-color: #4d4d4d



            }

            
                           """)



class FormWidget(QWidget):



    def __init__(self, parent):
        super(FormWidget, self).__init__(parent)

        self.layout=QGridLayout(self)
        self.resize(800,800)

        self.go=QPushButton("Detect")
        self.print=QPushButton("print")

        self.chain=QLabel("Chain")
        self.chain_list=QListWidget()
        

        self.residue=QLabel("Residue Number")
        self.res_list=QTextEdit()


        self.cutoff_val=QTextEdit("0")
        self.cutoff=QLabel("Cutoff Value")

        self.res=QLabel("Atom Types Detected")
        self.res_at=QListWidget()

        self.path_to_file=QLabel("Path to PDB file")
        self.path=QTextEdit()
        self.open=QPushButton("Open PDB")

        self.neigh_list=QTextEdit()
        self.inputfile=QPushButton("Input")
        self.inputpath=QTextEdit()

        #a=[]
        #for item in self.pdb.resid:
        #	if item in a:
        #		continue
        #	else:
        #		a.append(item)
        #for item in a:
        #	self.res_list.addItem(item)

        self.go.clicked.connect(self.find_neighbor)
        self.print.clicked.connect(self.print_neigh)
        self.open.clicked.connect(self.open_pdb)
        self.inputfile.clicked.connect(self.run_input)



        self.layout.addWidget(self.inputpath,0,0,1,1)
        self.layout.addWidget(self.inputfile,1,0,1,1)
        self.layout.addWidget(self.path,0,1,1,1)
        self.layout.addWidget(self.open,1,1,1,1)
        self.layout.addWidget(self.chain,2,0)
        self.layout.addWidget(self.chain_list,2,1,1,1)
        self.layout.addWidget(self.residue,3,0)
        self.layout.addWidget(self.res_list,3,1)
        self.layout.addWidget(self.go,4,1,1,1)
        self.layout.addWidget(self.res,5,0,1,1)
        self.layout.addWidget(self.res_at,5,1,1,1)
        self.layout.addWidget(self.cutoff,6,0,1,1)
        self.layout.addWidget(self.cutoff_val,6,1,1,1)
        self.layout.addWidget(self.neigh_list,0,2,8,1)
        self.layout.addWidget(self.print,8,2,1,1)
        

        logging.basicConfig(level=logging.WARNING)
        self.log = logging.getLogger('log')

        self.interactive=False
    

    def appendi(self, text):
        cursor = self.neigh_list.textCursor()
        cursor.movePosition(cursor.End)
        cursor.insertText(text)
        cursor.insertText("\n")


   		
   		#print("\nDetected Atom Type in", SEL_RSN, PRT[SEL_CHAIN][SEL_RSN][0][2], ":\n")

    def find_neighbor(self):
      try:
        self.go.setText("Detect")
        self.SEL_CHAIN = self.chain_list.currentItem().text()
        self.SEL_RSN = self.res_list.toPlainText()
        #if item in self.res_at:
         # self.res_at.remove(item)
        if len(self.res_at) > 0:
              for i in range(len(self.res_at)):
                self.res_at.takeItem(i)
        for i in self.PRT[self.SEL_CHAIN][self.SEL_RSN]:
   		    self.res_at.addItem(i[1])
   		    #print(">> ", i[1])
      except:
        self.go.setText("No chain or residue")
   	

    def print_neigh(self):
      if self.interactive:
        self.SEL_AT = self.res_at.currentItem().text()
      
      THR_DIST = float(self.cutoff_val.toPlainText())#input("Select cutoff distance...\t"))
      #try:
        #SEL_AT = self.res_at.currentItem().text()
      TGT = [i for i in self.PRT[self.SEL_CHAIN][self.SEL_RSN] if i[1] == self.SEL_AT][0]
      DIST_TGT = {}

      for i in self.PRT[self.SEL_CHAIN]:
   		    for j in self.PRT[self.SEL_CHAIN][i]:
   		        distance = ut.dist([TGT[5], TGT[6], TGT[7]], [j[5], j[6], j[7]])
   		        if j[4] not in DIST_TGT:
   		            DIST_TGT[j[4]] = distance
   		        elif j[4] in DIST_TGT:
   		            if distance < float(DIST_TGT[j[4]]):
   		                DIST_TGT[j[4]] = distance
   		        else:
   		            print("ERROR!")
      POS_AA = ["ARG", "HIS", "LYS"]
      NEG_AA = ["ASP", "GLU"]
      self.vecout=[]

      try:
          #while True:
        self.vecout.append("ResID\tDIST\tAA\tCHARGE\n")
        for i in DIST_TGT:
            if DIST_TGT[i] <= THR_DIST and self.PRT[self.SEL_CHAIN][i][0][2] in POS_AA:
                self.vecout.append(("{}\t{:.3f}\t{}\t+1".format(i, DIST_TGT[i], self.PRT[self.SEL_CHAIN][i][0][2])))
            elif DIST_TGT[i] <= THR_DIST and self.PRT[self.SEL_CHAIN][i][0][2] in NEG_AA:
                self.vecout.append(("{}\t{:.3f}\t{}\t-1".format(i, DIST_TGT[i], self.PRT[self.SEL_CHAIN][i][0][2])))
            elif DIST_TGT[i] <= THR_DIST:
                self.vecout.append(("{}\t{:.3f}\t{}".format(i, DIST_TGT[i], self.PRT[self.SEL_CHAIN][i][0][2])))
        #except KeyboardInterrupt:
         # print("\n\nClosed by user...bye bye...")

        self.neigh_list.setText("")
        for item in self.vecout:
            self.appendi(item)

      except Exception:
        self.log.exception('Error from throws():')
        self.neigh_list.setText("")
        self.neigh_list.setText("No atom selected")

    def open_pdb(self):
      self.interactive=True      
      try:
          self.PRT = coor.PDB(self.path.toPlainText()).prot
          self.pdb=coor.PDB(self.path.toPlainText())
          if len(self.chain_list) > 0:
              for i in range(len(self.chain_list)):
                self.chain_list.takeItem(i)
          if len(self.res_at) > 0:
              for i in range(len(self.res_at)):
                self.res_at.takeItem(i)
          self.res_list.setText("")
          self.neigh_list.setText("")
          self.cutoff_val.setText("0")
          for item in self.pdb.prot:
            self.chain_list.addItem(item)
      except:
          self.path.setText("")
          self.path.setText("File not found \nPlease insert file path")

    def run_input(self):
      try:
        a=[]
        with open(self.inputpath.toPlainText(),"r") as gi:
            lines=gi.readlines()
            for line in lines:
              a.append(line.split())
            self.SEL_CHAIN = a[2][1]
            self.SEL_RSN = a[2][2]
            self.SEL_AT = a[2][3]
            self.PRT = coor.PDB(a[1][1]).prot
            print(self.SEL_AT, self.SEL_CHAIN, self.SEL_RSN)
            if len(self.chain_list) > 0:
              for i in range(self.chain_list.count()):
                self.chain_list.takeItem(i)
            self.chain_list.addItem(a[2][1])
            self.res_list.setText(a[2][2])
            if len(self.res_at) > 0:
              for i in range(self.res_at.count()):
                self.res_at.takeItem(i)
            self.res_at.addItem(a[2][3])
            self.cutoff_val.setText(a[2][4])
            self.dist=a[2][4]
            self.print_neigh()
      except Exception:
        self.log.exception('Error from run_input():')
        self.inputfile.setText("File not Found")


#style.set_style

       
   		

      



