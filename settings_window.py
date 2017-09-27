# -*- coding: utf-8 -*-
"""
Created on Tue Sep 26 16:10:14 2017

@author: GUARIND
"""

import os
import sys
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore



QtWidgets.QFrame

class QHLine(QtWidgets.QFrame):
    def __init__(self):
        super(QHLine, self).__init__()
        self.setFrameShape(QtWidgets.QFrame.HLine)
        self.setFrameShadow(QtWidgets.QFrame.Sunken)
        
class QVLine(QtWidgets.QFrame):
    def __init__(self):
        super(QHLine, self).__init__()
        self.setFrameShape(QtWidgets.QFrame.VLine)
        self.setFrameShadow(QtWidgets.QFrame.Sunken)

class CalibrationTab(QtWidgets.QWidget):
    
    def __init__(self):
        super(CalibrationTab, self) .__init__()
        
        #spacerh = QHLine()#QtWidgets.QWidget(self)
        #spacerh.setFixedSize(10,0)
        
        #spacerv = QtWidgets.QWidget(self)
        #spacerv.setFixedSize(0,10)
        
        self._tab_name = 'Calibration'
        
        
        #checkbox
        self._checkBox1 = QtWidgets.QCheckBox('Personalized Value', self)
        self._checkBox2 = QtWidgets.QCheckBox('Iris Diameter', self)
        self._checkBox2.setChecked(True)
        #self._checkBox3 = QtWidgets.QCheckBox('Subject and Camera Distance', self)
        
        
        self._CheckButtonGroup = QtWidgets.QButtonGroup(self)
        self._CheckButtonGroup.addButton(self._checkBox1,1)
        self._CheckButtonGroup.addButton(self._checkBox2,2)
        #self._CheckButtonGroup.addButton(self._checkBox3,3)
        
        self._Personalized_Edit = QtWidgets.QLineEdit(self)
        self._Personalized_Edit.setText("")
        self._label1a = QtWidgets.QLabel('px/mm')
        
        
        self._IrisDiameter_Edit = QtWidgets.QLineEdit(self)
        self._IrisDiameter_Edit.setText("11.77")
        self._label2a = QtWidgets.QLabel('mm')
        

        
        layout = QtWidgets.QGridLayout()
        
        layout.addWidget(self._checkBox1, 0,0,1,1)
        layout.addWidget(self._Personalized_Edit, 1,0,1,1)
        layout.addWidget(self._label1a, 1,1,1,1)
        layout.addWidget(QHLine(),2,0)
        layout.addWidget(self._checkBox2, 3,0,1,1)
        layout.addWidget(self._IrisDiameter_Edit, 4,0,1,1)
        layout.addWidget(self._label2a, 4,1,1,1)
        
        self.setLayout(layout)

class ShowSettings(QtWidgets.QWidget):
    def __init__(self,parent=None):
        super(ShowSettings, self).__init__(parent)
        
        self.setWindowTitle('Settings')
        scriptDir = os.path.dirname(os.path.realpath(__file__))
        self.setWindowIcon(QtGui.QIcon(scriptDir + os.path.sep + 'include' +os.path.sep +'icon_color'+ os.path.sep + 'settings_icon.ico'))
        
        self.tab1 = CalibrationTab()
        
        self.main_Widget = QtWidgets.QTabWidget(self)
        self.tab1.setAutoFillBackground(True)
        self.main_Widget.addTab(self.tab1,self.tab1._tab_name)
        
        #if tab2 is not None:
        #    tab2.setAutoFillBackground(True)
        #    self.main_Widget.addTab(tab2,tab2._tab_name)
            
        
        #if tab3 is not None:
        #    tab3.setAutoFillBackground(True)
        #    self.main_Widget.addTab(tab3,'Difference')
        
        self.buttonDone = QtWidgets.QPushButton('Done',self)
        self.buttonDone.clicked.connect(self.handleReturn)
        
        self.buttonCancel = QtWidgets.QPushButton('Cancel', self)
        self.buttonCancel.clicked.connect(self.handleClose)
        

            
        
        
        
        
        layout=QtWidgets.QVBoxLayout()
        layout.addWidget(self.main_Widget)
        
        layout = QtWidgets.QGridLayout()
        layout.addWidget(self.main_Widget,0,0,2,2)
        layout.addWidget(self.buttonDone,2,0,1,1)
        layout.addWidget(self.buttonCancel,2,1,1,1)
       
        self.setLayout(layout)
        #self.show()       
        
    def handleClose(self):
        self.close()
        
    def handleReturn(self):
        if self.tab1._checkBox2.isChecked() == True:
            IrisDiameter = self.tab1._IrisDiameter_Edit.text()
            if not IrisDiameter:               
                QtWidgets.QMessageBox.information(self, 'Error', 
                            'The iris diameter must be larger than zero', 
                            QtWidgets.QMessageBox.Ok)
            else:
                IrisDiameter = float(IrisDiameter)
                if IrisDiameter <= 0:
                    QtWidgets.QMessageBox.information(self, 'Error', 
                            'The iris diameter must be larger than zero', 
                            QtWidgets.QMessageBox.Ok)
                else:
                    print(IrisDiameter)  
            
            
        elif self.tab1._checkBox1.isChecked() == True:
            PersonalizedValue = self.tab1._Personalized_Edit.text()
            if not PersonalizedValue:
                QtWidgets.QMessageBox.information(self, 'Error', 
                            'The personalized calibration value must be larger than zero', 
                            QtWidgets.QMessageBox.Ok)
            else:   
                PersonalizedValue = float(PersonalizedValue)
                if PersonalizedValue <= 0:
                    QtWidgets.QMessageBox.information(self, 'Error', 
                            'The personalized calibration value must be larger than zero', 
                            QtWidgets.QMessageBox.Ok)
                else:
                    print(PersonalizedValue)
        
        
if __name__ == '__main__':
    if not QtWidgets.QApplication.instance():
        app = QtWidgets.QApplication(sys.argv)
    else:
        app = QtWidgets.QApplication.instance()
    GUI = ShowSettings()
    GUI.show()
    app.exec_()