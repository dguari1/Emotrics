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
        
        #labels 
        self._label1 = QtWidgets.QLabel('Personalized Calibration Value')
        self._label2 = QtWidgets.QLabel('Iris Diameter')
        self._label3 = QtWidgets.QLabel('Distance between Subject and Camera')
        
        #checkbox
        self._checkBox1 = QtWidgets.QCheckBox('Personalized Calibration Value', self)
        self._checkBox2 = QtWidgets.QCheckBox('Iris Diameter', self)
        self._checkBox2.setChecked(True)
        self._checkBox3 = QtWidgets.QCheckBox('Subject and Camera Distance', self)
        
        
        self._CheckButtonGroup = QtWidgets.QButtonGroup(self)
        self._CheckButtonGroup.addButton(self._checkBox1,1)
        self._CheckButtonGroup.addButton(self._checkBox2,2)
        self._CheckButtonGroup.addButton(self._checkBox3,3)
        
        
        layout = QtWidgets.QGridLayout()
        
        layout.addWidget(self._checkBox1, 0,0,1,1)
        layout.addWidget(QHLine(),1,0)
        layout.addWidget(self._checkBox2, 2,0,1,1)
        layout.addWidget(QHLine(),3,0)
        layout.addWidget(self._checkBox3, 4,0,1,1)
        
        self.setLayout(layout)

class ShowSettings(QtWidgets.QWidget):
    def __init__(self,parent=None):
        super(ShowSettings, self).__init__(parent)
        
        self.setWindowTitle('Settings')
        scriptDir = os.path.dirname(os.path.realpath(__file__))
        self.setWindowIcon(QtGui.QIcon(scriptDir + os.path.sep + 'include' +os.path.sep +'icon_color'+ os.path.sep + 'settings_icon.ico'))
        
        tab1 = CalibrationTab()
        
        self.main_Widget = QtWidgets.QTabWidget(self)
        tab1.setAutoFillBackground(True)
        self.main_Widget.addTab(tab1,tab1._tab_name)
        
        #if tab2 is not None:
        #    tab2.setAutoFillBackground(True)
        #    self.main_Widget.addTab(tab2,tab2._tab_name)
            
        
        #if tab3 is not None:
        #    tab3.setAutoFillBackground(True)
        #    self.main_Widget.addTab(tab3,'Difference')
            
        
        
        
        
        layout=QtWidgets.QVBoxLayout()
        layout.addWidget(self.main_Widget)

       
        self.setLayout(layout)
        #self.show()       
        
if __name__ == '__main__':
    if not QtWidgets.QApplication.instance():
        app = QtWidgets.QApplication(sys.argv)
    else:
        app = QtWidgets.QApplication.instance()
    GUI = ShowSettings()
    GUI.show()
    app.exec_()