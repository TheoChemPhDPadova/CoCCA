from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import argparse
import itertools

import numpy as np
import numpy.linalg as la


from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtOpenGL import *
from PyQt5 import QtCore
import sys, time, random, json, coor, common, subprocess
from subprocess import check_output
from OpenGL.GL import *
from OpenGL.GLU import *
import pyqtgraph.opengl as gl


class Fourth(QMainWindow):
    def __init__(self, parent=None):
        super(Fourth, self).__init__(parent)
        self.form_widget = FormWidget(self)
        self.setCentralWidget(self.form_widget)

class FormWidget(QWidget):

    def __init__(self, parent):
        super(FormWidget, self).__init__(parent)

        self.layout = QGridLayout()
        self.pushButton = QPushButton("Create Input")
        self.startButton = QPushButton("Start")
        #self.pippo = QLabel("layout")
        #self.pluto = GLWidget(self)

        self.view = gl.GLViewWidget()

        ## create three grids, add each to the self.view
        
        
        
        """self.sphere = gl.GLMeshItem(meshdata=self.md, smooth=True)
        self.sphere2 = gl.GLMeshItem(meshdata=self.md, smooth=True)
        self.cyl     = gl.GLMeshItem(meshdata=self.md_cyl, smooth=True)
        self.view.addItem(self.cyl)
        self.view.addItem(self.sphere)
        #self.view.addItem(self.sphere2)
        self.cyl.rotate(90,0,1,0)
        self.cyl.translate(-1,0,0)
        self.cyl.setColor([0.1,0.2,0.3,1])
        self.sphere2.translate(1,0,0)
        self.sphere2.setColor([1,1,1,1])
        self.sphere.translate(-1,0,0)
        self.sphere2.setColor([0.5,0.2,0.4,1])

        ## rotate x and y grids to face the correct direction
        self.xgrid.rotate(90, 0, 1, 0)
        self.ygrid.rotate(90, 1, 0, 0)

        ## scale each grid differently
        self.xgrid.scale(0.2, 0.1, 0.1)
        self.ygrid.scale(0.2, 0.1, 0.1)
        self.zgrid.scale(0.1, 0.2, 0.1)"""


        self.layout.addWidget(self.pushButton)
        self.layout.addWidget(self.startButton)
        self.layout.addWidget(self.view)
        #self.layout.addWidget(GLWidget())
        self.setLayout(self.layout)
        

        self.pushButton.clicked.connect(self.show)
        self.startButton.clicked.connect(self.plot_line)

    def mass_center(self):
        ifile  = coor.XYZ("CO2.xyz")
        self.CM_x = (ifile.xyz[0][0]+ifile.xyz[1][0]+ifile.xyz[2][0])/3
        self.CM_y = (ifile.xyz[0][1]+ifile.xyz[1][1]+ifile.xyz[2][1])/3
        self.M_z = (ifile.xyz[0][2]+ifile.xyz[1][2]+ifile.xyz[2][2])/3
        print(CM_x,CM_y,CM_z)


    def show(self):
        ifile = coor.XYZ("CO2.xyz")
        print(ifile.element)

        self.xgrid = gl.GLAxisItem()
        self.ygrid = gl.GLAxisItem()
        self.zgrid = gl.GLAxisItem()
        self.xgrid.rotate(90, 0, 1, 0)
        self.ygrid.rotate(90, 1, 0, 0)
        self.CM_x = (ifile.xyz[0][0]+ifile.xyz[1][0]+ifile.xyz[2][0])/3
        self.CM_y = (ifile.xyz[0][1]+ifile.xyz[1][1]+ifile.xyz[2][1])/3
        self.CM_z = (ifile.xyz[0][2]+ifile.xyz[1][2]+ifile.xyz[2][2])/3
        CM=[(ifile.xyz[0][0]+ifile.xyz[1][0]+ifile.xyz[2][0])/3,(ifile.xyz[0][1]+ifile.xyz[1][1]+ifile.xyz[2][1])/3,(ifile.xyz[0][2]+ifile.xyz[1][2]+ifile.xyz[2][2])/3]
        self.md =gl.MeshData.sphere(rows=100, cols=100, radius=0.2)
        self.md_cyl = gl.MeshData.cylinder(rows=20, cols=20, radius=[0.1,0.1], length=2)
        self.bond1= gl.GLMeshItem(meshdata=self.md_cyl, smooth=True)
        self.atom=dict()
        bond=dict()
        color={"C":[0.5,0.5,0.5,1],"O":[1,0,0,1]}
        self.translated_crd=dict()
        for n, item in enumerate(ifile.xyz):
            self.atom[n] = gl.GLMeshItem(meshdata=self.md, smooth=True)
            self.translated_crd[n]=([item[0]-CM[0],item[1]-CM[1],item[2]-CM[2]])
            self.atom[n].translate(self.translated_crd[n][0],self.translated_crd[n][1],self.translated_crd[n][2])
            self.atom[n].setColor(color[ifile.element[n]])
            self.view.addItem(self.atom[n])
            self.view.setCameraPosition(pos=CM, distance=10, elevation=15, azimuth=90)
            #self.view.pan(-2.547046059, 1.914865471,-1.798001685)
        
        #self.view.addItem(self.bond1)
        self.view.addItem(self.xgrid)
        self.view.addItem(self.ygrid)
        self.view.addItem(self.zgrid)


        self.displace = [0,0,0.1]




        #self.view.addItem(self.sphere2)
        #self.

    def draw_bond(self):
        ifile=coor.XYZ("CO2.xyz")
        dists = scipy.spatial.distance.pdist(ifile.xyz,'dists')
        for n,item in enumerate(ifile.xyz):
            try:
                cyl_crd = [(self.translated_crd[n][0]),(self.translated_crd[n][1]),(self.translated_crd[n][2])]
                v1=[(self.translated_crd[n][0]),(self.translated_crd[n][1]),(self.translated_crd[n][2]+2)]
                v2=[(self.translated_crd[n+1][0]),(self.translated_crd[n+1][1]),(self.translated_crd[n+1][2])]

                self.md_cyl = gl.MeshData.cylinder(rows=20, cols=20, radius=[0.05,0.05], length=self.dist12(self.translated_crd[n],self.translated_crd[n+1]))
                self.bond1= gl.GLMeshItem(meshdata=self.md_cyl, smooth=True)
                
                curve_vec_1 = np.array(v1)
                curve_vec_2 = np.array(v2)
                a,b = (curve_vec_1/ np.linalg.norm(curve_vec_1)).reshape(3), (curve_vec_2/ np.linalg.norm(curve_vec_2)).reshape(3)
                v = np.cross(a,b)
                c = np.dot(a,b)
                s = np.linalg.norm(v)
                I = np.identity(3)
                vXStr = '{} {} {}; {} {} {}; {} {} {}'.format(0, -v[2], v[1], v[2], 0, -v[0], -v[1], v[0], 0)
                k = np.matrix(vXStr)
                r = I + k + np.matmul(k,k) * ((1 -c)/(s**2))
                #print(r)
                #print(r.dot(curve_vec_1))
                #print(np.sqrt(np.square(r[2,1])+np.square(r[2,2])))
                angl_x=np.arctan2(r[2,1],r[2,2])
                angl_y=np.arctan2(-r[2,0],np.sqrt(np.square(r[2,1])+np.square(r[2,2])))
                angl_z=np.arctan2(r[1,0],r[0,0])
                
                #return(angl_x,angl_y,angl_z)
                self.bond1.translate(cyl_crd[0],cyl_crd[1],cyl_crd[2])
                self.bond1.rotate(np.rad2deg(angl_x),1,0,0)
                self.bond1.rotate(np.rad2deg(angl_y),0,1,0)
                self.bond1.rotate(np.rad2deg(angl_z),0,0,1)
                
                self.view.addItem(self.bond1)
            except:
                break         

    def dist12(self, a, b):
        anp = np.array(a)
        bnp = np.array(b)
        dist=np.linalg.norm(anp-bnp)
        return(dist)
    def plot_line(self):
        p=np.array([self.translated_crd[0],self.translated_crd[1]])
        line=gl.GLLinePlotItem(pos=p, color=[0.3,0.4,0.5,1], width=20, antialias=True)
        self.view.addItem(line)



    def start(self):
        if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
            QtGui.QApplication.instance().exec_()

    def set_plotdata(self, name, points, color, width):
        self.traces[name].setData(pos=points, color=color, width=width)

    def update(self):
        for i in range(10):
            self.atom[0].translate(self.translated_crd[0][0]+i*self.displace[0],self.translated_crd[0][1]+i*self.displace[1],self.translated_crd[0][2]+i*self.displace[2])

    def animation(self):
        timer = QtCore.QTimer()
        timer.timeout.connect(self.update)
        timer.start(20)
        self.start()
    
class Fifth(QMainWindow):
    def __init__(self, parent=None):
        super(Fifth, self).__init__(parent)
        self.ogl = GLWidget(self)
        self.form=FormWidget(self)
        self.setCentralWidget(self.ogl)







