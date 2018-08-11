# -*- coding: utf-8 -*-
"""
Created on Mon Aug 14 15:42:31 2017

@author: GUARIND
"""
import os
import sys
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore


class ShowResults(QtWidgets.QMainWindow):
    def __init__(self):
        super(ShowResults, self).__init__()
        
        self.setWindowTitle('Metrics')
        if os.name is 'posix': #is a mac or linux
            scriptDir = os.path.dirname(sys.argv[0])
        else: #is a  windows 
            scriptDir = os.getcwd()
                
        self.setWindowIcon(QtGui.QIcon(scriptDir + os.path.sep + 'include' +os.path.sep + 'ruler_icon.ico'))
        self._new_window = None
        
        self.main_Widget = QtWidgets.QWidget(self)
        
        spacerh = QtWidgets.QWidget(self)
        spacerh.setFixedSize(10,0)
        
        spacerv = QtWidgets.QWidget(self)
        spacerv.setFixedSize(0,10)
        
        self._label0a = QtWidgets.QLabel('Right')
        self._label0b = QtWidgets.QLabel('Left')
        self._label0c = QtWidgets.QLabel('Difference')
        
        self._CE = QtWidgets.QLabel('Commisure excursion:')
        self._SA = QtWidgets.QLabel('Smile angle:')
        self._IVD = QtWidgets.QLabel('Inter vermillion distance:')
        self._DS = QtWidgets.QLabel('Dental show:')
        self._ULP = QtWidgets.QLabel('Upper lip position:')
        self._LLP = QtWidgets.QLabel('Lower lip position:')
        self._CH = QtWidgets.QLabel('Commisure height:')
        self._PD = QtWidgets.QLabel('Philtral deviation:')
        self._ULPO = QtWidgets.QLabel('Upper lid position:')
        self._LLPO = QtWidgets.QLabel('Lower Lid Position:')
        self._BP = QtWidgets.QLabel('Brown Position:')
        self._CD = QtWidgets.QLabel('Columelar deviation:')
        self._ABH = QtWidgets.QLabel('Alar base height:')
        
        #Commisure excursion
        self._CE_right = QtWidgets.QLineEdit(self)
        self._CE_right.setText("0")
        self._CE_left = QtWidgets.QLineEdit(self)
        self._CE_left.setText("0")
        self._CE_dev = QtWidgets.QLineEdit(self)
        self._CE_dev.setText("0")
        
        #Smile angle
        self._SA_right = QtWidgets.QLineEdit(self)
        self._SA_right.setText("0")
        self._SA_left = QtWidgets.QLineEdit(self)
        self._SA_left.setText("0")
        self._SA_dev = QtWidgets.QLineEdit(self)
        self._SA_dev.setText("0")        

        #Inter vermillion distance
        self._IVD_right = QtWidgets.QLineEdit(self)
        self._IVD_right.setText("0")
        self._IVD_left = QtWidgets.QLineEdit(self)
        self._IVD_left.setText("0")
        self._IVD_dev = QtWidgets.QLineEdit(self)
        self._IVD_dev.setText("0")  
        
        #Dental show
        self._DS_right = QtWidgets.QLineEdit(self)
        self._DS_right.setText("0")
        self._DS_left = QtWidgets.QLineEdit(self)
        self._DS_left.setText("0")
        self._DS_dev = QtWidgets.QLineEdit(self)
        self._DS_dev.setText("0")  
        
        #Upper lip position
        self._ULP_right = QtWidgets.QLineEdit(self)
        self._ULP_right.setText("0")
        self._ULP_left = QtWidgets.QLineEdit(self)
        self._ULP_left.setText("0")
        self._ULP_dev = QtWidgets.QLineEdit(self)
        self._ULP_dev.setText("0")  

        #Lower lio position
        self._LLP_right = QtWidgets.QLineEdit(self)
        self._LLP_right.setText("0")
        self._LLP_left = QtWidgets.QLineEdit(self)
        self._LLP_left.setText("0")
        self._LLP_dev = QtWidgets.QLineEdit(self)
        self._LLP_dev.setText("0")  
        
        #Commisure height
        self._CH_right = QtWidgets.QLineEdit(self)
        self._CH_right.setText("0")
        self._CH_left = QtWidgets.QLineEdit(self)
        self._CH_left.setText("0")
        self._CH_dev = QtWidgets.QLineEdit(self)
        self._CH_dev.setText("0")  
        
        #Philtral deviation
        self._PD_right = QtWidgets.QLineEdit(self)
        self._PD_right.setText("NA")
        self._PD_left = QtWidgets.QLineEdit(self)
        self._PD_left.setText("NA")
        self._PD_dev = QtWidgets.QLineEdit(self)
        self._PD_dev.setText("0") 
        
        #Upper lid position
        self._ULPO_right = QtWidgets.QLineEdit(self)
        self._ULPO_right.setText("0")
        self._ULPO_left = QtWidgets.QLineEdit(self)
        self._ULPO_left.setText("0")
        self._ULPO_dev = QtWidgets.QLineEdit(self)
        self._ULPO_dev.setText("0")    
        
        #Lower Lid Position
        self._LLPO_right = QtWidgets.QLineEdit(self)
        self._LLPO_right.setText("0")
        self._LLPO_left = QtWidgets.QLineEdit(self)
        self._LLPO_left.setText("0")
        self._LLPO_dev = QtWidgets.QLineEdit(self)
        self._LLPO_dev.setText("0")     
        
        #Brown Position
        self._BP_right = QtWidgets.QLineEdit(self)
        self._BP_right.setText("0")
        self._BP_left = QtWidgets.QLineEdit(self)
        self._BP_left.setText("0")
        self._BP_dev = QtWidgets.QLineEdit(self)
        self._BP_dev.setText("0") 
        
        #Columelar deviation
        self._CD_right = QtWidgets.QLineEdit(self)
        self._CD_right.setText("NA")
        self._CD_left = QtWidgets.QLineEdit(self)
        self._CD_left.setText("NA")
        self._CD_dev = QtWidgets.QLineEdit(self)
        self._CD_dev.setText("0")    
        
        #Alar base height
        self._ABH_right = QtWidgets.QLineEdit(self)
        self._ABH_right.setText("0")
        self._ABH_left = QtWidgets.QLineEdit(self)
        self._ABH_left.setText("0")
        self._ABH_dev = QtWidgets.QLineEdit(self)
        self._ABH_dev.setText("0")        
        
        layout = QtWidgets.QGridLayout()
        layout.addWidget(spacerh,0,1)
        layout.addWidget(self._label0a, 0,2,1,1)
        layout.addWidget(spacerh,0,3)
        layout.addWidget(self._label0b, 0,4,1,1)
        layout.addWidget(spacerh,0,5)
        layout.addWidget(self._label0c, 0,6,1,1)

        layout.addWidget(spacerv,1,0,6,1)
        layout.addWidget(self._CE, 2,0,1,1)
        layout.addWidget(self._CE_right,2,2,1,1)
        layout.addWidget(self._CE_left,2,4,1,1)
        layout.addWidget(self._CE_dev,2,6,1,1)
        
        layout.addWidget(spacerv,3,0,6,1)
        layout.addWidget(self._SA, 4,0,1,1)
        layout.addWidget(self._SA_right,4,2,1,1)
        layout.addWidget(self._SA_left,4,4,1,1)
        layout.addWidget(self._SA_dev,4,6,1,1)
        
        layout.addWidget(spacerv,5,0,6,1)
        layout.addWidget(self._IVD, 6,0,1,1)
        layout.addWidget(self._IVD_right,6,2,1,1)
        layout.addWidget(self._IVD_left,6,4,1,1)
        layout.addWidget(self._IVD_dev,6,6,1,1)
        
        layout.addWidget(spacerv,7,0,6,1)
        layout.addWidget(self._DS, 8,0,1,1)
        layout.addWidget(self._DS_right,8,2,1,1)
        layout.addWidget(self._DS_left,8,4,1,1)
        layout.addWidget(self._DS_dev,8,6,1,1)
        
        layout.addWidget(spacerv,9,0,6,1)
        layout.addWidget(self._ULP, 10,0,1,1)
        layout.addWidget(self._ULP_right,10,2,1,1)
        layout.addWidget(self._ULP_left,10,4,1,1)
        layout.addWidget(self._ULP_dev,10,6,1,1)
        
        layout.addWidget(spacerv,11,0,6,1)
        layout.addWidget(self._LLP, 12,0,1,1)
        layout.addWidget(self._LLP_right,12,2,1,1)
        layout.addWidget(self._LLP_left,12,4,1,1)
        layout.addWidget(self._LLP_dev,12,6,1,1)
        
        layout.addWidget(spacerv,13,0,6,1)
        layout.addWidget(self._CH, 14,0,1,1)
        layout.addWidget(self._CH_right,14,2,1,1)
        layout.addWidget(self._CH_left,14,4,1,1)
        layout.addWidget(self._CH_dev,14,6,1,1)
        
        layout.addWidget(spacerv,15,0,6,1)
        layout.addWidget(self._PD, 16,0,1,1)
        layout.addWidget(self._PD_right,16,2,1,1)
        layout.addWidget(self._PD_left,16,4,1,1)
        layout.addWidget(self._PD_dev,16,6,1,1)
        
        layout.addWidget(spacerv,17,0,6,1)
        layout.addWidget(self._ULPO, 18,0,1,1)
        layout.addWidget(self._ULPO_right,18,2,1,1)
        layout.addWidget(self._ULPO_left,18,4,1,1)
        layout.addWidget(self._ULPO_dev,18,6,1,1)
        
        layout.addWidget(spacerv,19,0,6,1)
        layout.addWidget(self._LLPO, 20,0,1,1)
        layout.addWidget(self._LLPO_right,20,2,1,1)
        layout.addWidget(self._LLPO_left,20,4,1,1)
        layout.addWidget(self._LLPO_dev,20,6,1,1)
        
        layout.addWidget(spacerv,21,0,6,1)
        layout.addWidget(self._BP, 22,0,1,1)
        layout.addWidget(self._BP_right,22,2,1,1)
        layout.addWidget(self._BP_left,22,4,1,1)
        layout.addWidget(self._BP_dev,22,6,1,1)
        
        layout.addWidget(spacerv,23,0,6,1)
        layout.addWidget(self._CD, 24,0,1,1)
        layout.addWidget(self._CD_right,24,2,1,1)
        layout.addWidget(self._CD_left,24,4,1,1)
        layout.addWidget(self._CD_dev,24,6,1,1)
        
        layout.addWidget(spacerv,25,0,6,1)
        layout.addWidget(self._ABH, 26,0,1,1)
        layout.addWidget(self._ABH_right,26,2,1,1)
        layout.addWidget(self._ABH_left,26,4,1,1)
        layout.addWidget(self._ABH_dev,26,6,1,1)
        
        self.main_Widget.setLayout(layout)
        self.setCentralWidget(self.main_Widget)
        
if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    GUI = ShowResults()
    GUI.show()
    app.exec_()
    