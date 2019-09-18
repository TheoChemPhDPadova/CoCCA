from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtCore
import sys, time, random, json, coor

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
        self.tabs.addTab(self.tab2,"Altro")

        # Create first tab
        self.tab1.layout = QGridLayout(self)
        self.pushButton1 = QPushButton("Create Input")
        self.const_elem_te=QTextEdit()
        self.const_elem=QLabel("Elem")
        self.const_elem_num_te=QTextEdit()
        self.const_elem_num=QLabel("Num")
        self.file_path_te=QTextEdit()
        self.file_path=QLabel("Path")
        self.file_out=QTextEdit()
        self.pippo=QTextEdit()
        self.gaussian=QCheckBox("Gaussian")
        self.ORCA=QCheckBox("ORCA")
        self.XTB=QCheckBox("XTB")

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
        self.tab1.layout.addWidget(self.file_path_te,3,1,1,2)
        self.tab1.layout.addWidget(self.file_path,3,0,1,1)
        self.tab1.layout.addWidget(self.gaussian,0,0,1,1)
        self.tab1.layout.addWidget(self.ORCA,0,1,1,1)
        self.tab1.layout.addWidget(self.XTB,0,2,1,1)
        self.tab1.layout.addWidget(self.pushButton1,4,1,1,3)
        self.tab1.layout.addWidget(self.pippo,0,4,6,1)


        self.tab1.setLayout(self.tab1.layout)

        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

        text=str("ciao\n")
        self.pushButton1.clicked.connect(self.check_elem_const)

    def appendi(self, text):
        cursor = self.pippo.textCursor()
        cursor.movePosition(cursor.End)
        cursor.insertText(text)
        cursor.insertText("\n")



    def check_elem_const(self):
        self.filename=self.file_path_te.toPlainText()
        #self.appendi(str(filename))
        self.const_elem_list= self.const_elem_te.toPlainText()
        self.const_elem_num= self.const_elem_num_te.toPlainText()
        print(self.const_elem_num)
        #self.appendi(str(const_elem_list))
        self.const_gen()
        #print(self.vecout)
        self.pippo.setText("")
        for item in self.vecout:
            self.appendi(str(item))

    def multiple_parser(self, inp_list):
        """Multiple input parser"""
        out_list = []
        for k in inp_list:
            if "-" in k:
                for l in range(int(k.split("-")[0]), int(k.split("-")[1]) + 1):
                    if int(l) not in out_list:
                        out_list.append(int(l))
            else:
                if int(k) not in out_list:
                    out_list.append(int(k))
        return out_list

    def const_gen(self):
                self.vecout=[]
                FILENAME = "./example.xyz"
                XMOL = coor.XYZ(FILENAME)

                self.vecout.append(("\nNumber of atoms:\t\t" + str(XMOL.natoms)))
                self.vecout.append(("Elements in molecule:\t\t" + ", ".join(set(XMOL.element))))
                self.vecout.append("\n\nINPUT START\n\n")

                INPUT_INDEX = self.const_elem_list.split() #input("\nEnter the element(s) to constrain.\nMultiple elements constraints are possible (e.g.: C O).\nDifferent elements must be separated by a SPACE.\nSpecial tokens are allowed (e.g.: All)\n\nSelection\n").split()
                CONST_INDEX = []
                print(INPUT_INDEX)

                for idx, val in enumerate(XMOL.element):
                    if val in INPUT_INDEX:
                        CONST_INDEX.append(idx + 1)
                        if "All" in INPUT_INDEX:
                            CONST_INDEX = [i for i in range(1, XMOL.natoms + 1)]

                #print(CONST_INDEX)
                INPUT_INDEX =  self.const_elem_num.split() #input("\nDo you want to CONSTRAIN some particular atom?\n\n").split()

                for i in self.multiple_parser(INPUT_INDEX):
                                if int(i) not in CONST_INDEX:
                                    CONST_INDEX.append(int(i))

                #INPUT_INDEX =  10 #input("\nDo you want to UN-CONSTRAIN some particular atom?\n\n").split()

                #for i in multiple_parser(INPUT_INDEX):
                #                        if int(i) in CONST_INDEX:
                #                                CONST_INDEX.remove(int(i))

                FREE_INDEX = list({int(i) for i in range(1, XMOL.natoms + 1)} - set(CONST_INDEX))

                SOFT =  "1" #input("Select software:\n1)\tORCA\n2)\tGaussian\n3)\txTB\n")

                if self.gaussian.isChecked():
                    SOFT = "2"
                if self.XTB.isChecked():
                    SOFT = "3"
                if SOFT == "1":
                    self.vecout.append(("%GEOM"))
                    self.vecout.append(("  Constraints"))
                    for i in CONST_INDEX:
                        self.vecout.append(("    {C " + str(i-1) + " C}"))
                    self.vecout.append(("  End"))
                    self.vecout.append(("END"))
                    CONST_INDEX[:] = [x - 1 for x in CONST_INDEX]
                    FREE_INDEX[:] = [x - 1 for x in FREE_INDEX]
                    self.vecout.append(("\nTo project-out the immaginary frequencies due to frozen atoms in a vibrational analysis use:\n"))
                    self.vecout.append(("%FREQ"))
                    self.vecout.append(("  AnFreq    False"))
                    self.vecout.append(("  NumFreq   True"))
                    self.vecout.append(("  Partial_Hess"))
                    self.vecout.append(("    {" + " ".join(map(str, CONST_INDEX)) + "}"))
                    self.vecout.append(("  End"))
                    self.vecout.append(("END"))

                elif SOFT == "2":
                        self.vecout.append(("\nModredundant syntax is available below but it is suggested to use the classical frozen syntax (Atom 0/-1 X Y Z) at the end of this report:\n"))
                        for i in CONST_INDEX:
                            self.vecout.append(("X " + str(i) + " F"))
                        self.vecout.append(("\nTo project-out the immaginary frequencies due to frozen atoms in a vibrational analysis change the coordinates using the frozen syntax (Atom 0/-1 X Y Z):\n"))
                        for idx, val in enumerate(XMOL.element):
                            if idx+1 in FREE_INDEX:
                                self.vecout.append(("{}   {} \t{:.10f}\t {:.10f}\t {:.10f}".format(val, "0", XMOL.xyz[idx][0], XMOL.xyz[idx][1], XMOL.xyz[idx][2])))
                            elif idx+1 in CONST_INDEX:
                                self.vecout.append(("{}  {} \t{:.10f}\t {:.10f}\t {:.10f}".format(val, "-1", XMOL.xyz[idx][0], XMOL.xyz[idx][1], XMOL.xyz[idx][2])))
                            else:
                                self.vecout.append(("ERROR!!! Something wrong just happened... :("))

                elif SOFT == "3":
                        XTB_OPT = "n" #input("Do you like to freeze atoms in hessian calculation? (All immaginary mode due to frozen atoms will be projected out) [y/n]\n")
                        #if xtb_hess.isChecked():
                        #    XTB_OPT="y"
                        self.vecout.append(("\n$fix"))
                        for i in CONST_INDEX:
                            self.vecout.append(("atoms: " + str(i)))
                        if XTB_OPT == "y":
                            for i in CONST_INDEX:
                                self.vecout.append(("freeze: " + str(i)))
                                self.vecout.append(("end"))
                print(self.vecout)
                self.vecout.append("\n\nINPUT END\n\n")

    def check_selection(self):
        if self.main_selection.currentRow() == 0:
            print ("UNO")
        elif self.main_selection.currentRow() == 1:
            print("DUE")
        elif self.main_selection.currentRow() == 2:
            print("TRE")
