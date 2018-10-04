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
    
    def __init__(self,parent=None, CalibrationType = 'Iris', CalibrationValue = 11.77):
        super(CalibrationTab, self) .__init__(parent)
        
        #spacerh = QHLine()#QtWidgets.QWidget(self)
        #spacerh.setFixedSize(10,0)
        
        #spacerv = QtWidgets.QWidget(self)
        #spacerv.setFixedSize(0,10)
        
        self._tab_name = 'Calibration'
        
        self._CalibrationType = CalibrationType
        self._CalibratioValue = CalibrationValue
        
        
        #checkbox
        self._checkBox2 = QtWidgets.QCheckBox('Personalized Value', self)
        self._checkBox1 = QtWidgets.QCheckBox('Iris Diameter', self)

        #self._checkBox3 = QtWidgets.QCheckBox('Subject and Camera Distance', self)
        
        
        self._CheckButtonGroup = QtWidgets.QButtonGroup(self)
        self._CheckButtonGroup.addButton(self._checkBox1,1)
        self._CheckButtonGroup.addButton(self._checkBox2,2)
        #self._CheckButtonGroup.addButton(self._checkBox3,3)
        
        self._Personalized_Edit = QtWidgets.QLineEdit(self)
        #self._Personalized_Edit.setText("")
        self._label2a = QtWidgets.QLabel('mm/px')
        
        
        self._IrisDiameter_Edit = QtWidgets.QLineEdit(self)
        #self._IrisDiameter_Edit.setText("11.77")
        self._label1a = QtWidgets.QLabel('mm')
        
        
        if self._CalibrationType == 'Iris':
            self._checkBox1.setChecked(True)
            self._checkBox2.setChecked(False)
            self._Personalized_Edit.setText("")
            self._IrisDiameter_Edit.setText(str(self._CalibratioValue))
        else:
            self._checkBox1.setChecked(False) 
            self._checkBox2.setChecked(True)
            self._Personalized_Edit.setText(str(self._CalibratioValue))
            self._IrisDiameter_Edit.setText("")
        

        
        layout = QtWidgets.QGridLayout()
        
        layout.addWidget(self._checkBox1, 0,0,1,1)
        layout.addWidget(self._IrisDiameter_Edit, 1,0,1,1)
        layout.addWidget(self._label1a, 1,1,1,1)
        layout.addWidget(QHLine(),2,0)
        layout.addWidget(self._checkBox2, 3,0,1,1)
        layout.addWidget(self._Personalized_Edit, 4,0,1,1)
        layout.addWidget(self._label2a, 4,1,1,1)
        
        self.setLayout(layout)
        

class ModelTab(QtWidgets.QWidget):
    
    def __init__(self,parent=None, ModelName='iBUG'):
        super(ModelTab, self) .__init__(parent)
        
        if os.name is 'posix': #is a mac or linux
            scriptDir = os.path.dirname(sys.argv[0])
        else: #is a  windows 
            scriptDir = os.getcwd()
        
        #spacerh = QHLine()#QtWidgets.QWidget(self)
        #spacerh.setFixedSize(10,0)
        
        #spacerv = QtWidgets.QWidget(self)
        #spacerv.setFixedSize(0,10)
        
        self._ModelName=ModelName
        
        self._tab_name = 'Model'
        
        
        #checkbox
        self._checkBox2 = QtWidgets.QCheckBox('iBUG Database', self)
        self._checkBox1 = QtWidgets.QCheckBox('MEEI Database', self)
        if self._ModelName == 'iBUG':
            self._checkBox1.setChecked(False)
            self._checkBox2.setChecked(True)
        else:
            self._checkBox1.setChecked(True) 
            self._checkBox2.setChecked(False)
        #self._checkBox3 = QtWidgets.QCheckBox('Subject and Camera Distance', self)
        
        
        self._CheckButtonGroup = QtWidgets.QButtonGroup(self)
        self._CheckButtonGroup.addButton(self._checkBox1,1)
        self._CheckButtonGroup.addButton(self._checkBox2,2)
        #self._CheckButtonGroup.addButton(self._checkBox3,3)
        
        self._help_checkBox1 = QtWidgets.QPushButton('', self)
        self._help_checkBox1.setIcon(QtGui.QIcon(scriptDir + os.path.sep + 'include' +os.path.sep +'icon_color'+ os.path.sep + 'question_icon.png'))
        self._help_checkBox1.clicked.connect(lambda: self.push_help_checkBox1())
        self._help_checkBox1.setIconSize(QtCore.QSize(20,20))
        
        
        self._help_checkBox2 = QtWidgets.QPushButton('', self)
        self._help_checkBox2.setIcon(QtGui.QIcon(scriptDir + os.path.sep + 'include' +os.path.sep +'icon_color'+ os.path.sep + 'question_icon.png'))
        self._help_checkBox2.clicked.connect(lambda: self.push_help_checkBox2())
        self._help_checkBox2.setIconSize(QtCore.QSize(20,20))
        

        
        layout = QtWidgets.QGridLayout()
        
        layout.addWidget(self._checkBox1, 0,0)
        layout.addWidget(self._help_checkBox1, 0,1)
        layout.addWidget(QHLine(),1,0,1,2)
        layout.addWidget(self._checkBox2, 2,0,1,1)
        layout.addWidget(self._help_checkBox2, 2,1,1,1)
        
        self.setLayout(layout)
        
        
    def push_help_checkBox1(self):
        QtWidgets.QMessageBox.information(self, 'MEEI Database', 
                            'Database created using front face, standard clinical photographs from facial palsy patients', 
                            QtWidgets.QMessageBox.Ok)
              
    def push_help_checkBox2(self):
        QtWidgets.QMessageBox.information(self, 'iBUG Database', 
                            'Database created as part of the iBUG project, it contains thousands of images taken in the wild along with face portaits obtained from the web', 
                            QtWidgets.QMessageBox.Ok)   
        
        
#class LandmarksSizeandColorTab(QtWidgets.QWidget):
#    
#    def __init__(self,parent=None, LandmarksSize=1, LandmarksColor=None):
#        super(LandmarksSizeandColorTab, self) .__init__(parent)
#        
#        if os.name is 'posix': #is a mac or linux
#            scriptDir = os.path.dirname(sys.argv[0])
#        else: #is a  windows 
#            scriptDir = os.getcwd()
#        
#        #spacerh = QHLine()#QtWidgets.QWidget(self)
#        #spacerh.setFixedSize(10,0)
#        
#        #spacerv = QtWidgets.QWidget(self)
#        #spacerv.setFixedSize(0,10)
#        
#        self._LandmarksSize = LandmarksSize 
#        self._LandmarksColor = LandmarksColor
#        
#        self._tab_name = 'Landmarks'
#        
#        
#        #checkbox
#        self._checkBox2 = QtWidgets.QCheckBox('iBUG Database', self)
#        self._checkBox1 = QtWidgets.QCheckBox('MEEI Database', self)
#        if self._ModelName == 'iBUG':
#            self._checkBox1.setChecked(False)
#            self._checkBox2.setChecked(True)
#        else:
#            self._checkBox1.setChecked(True) 
#            self._checkBox2.setChecked(False)
#        #self._checkBox3 = QtWidgets.QCheckBox('Subject and Camera Distance', self)
#        
#        
#        self._CheckButtonGroup = QtWidgets.QButtonGroup(self)
#        self._CheckButtonGroup.addButton(self._checkBox1,1)
#        self._CheckButtonGroup.addButton(self._checkBox2,2)
#        #self._CheckButtonGroup.addButton(self._checkBox3,3)
#        
#        self._help_checkBox1 = QtWidgets.QPushButton('', self)
#        self._help_checkBox1.setIcon(QtGui.QIcon(scriptDir + os.path.sep + 'include' +os.path.sep +'icon_color'+ os.path.sep + 'question_icon.png'))
#        self._help_checkBox1.clicked.connect(lambda: self.push_help_checkBox1())
#        self._help_checkBox1.setIconSize(QtCore.QSize(20,20))
#        
#        
#        self._help_checkBox2 = QtWidgets.QPushButton('', self)
#        self._help_checkBox2.setIcon(QtGui.QIcon(scriptDir + os.path.sep + 'include' +os.path.sep +'icon_color'+ os.path.sep + 'question_icon.png'))
#        self._help_checkBox2.clicked.connect(lambda: self.push_help_checkBox2())
#        self._help_checkBox2.setIconSize(QtCore.QSize(20,20))
#        
#
#        
#        layout = QtWidgets.QGridLayout()
#        
#        layout.addWidget(self._checkBox1, 0,0)
#        layout.addWidget(self._help_checkBox1, 0,1)
#        layout.addWidget(QHLine(),1,0,1,2)
#        layout.addWidget(self._checkBox2, 2,0,1,1)
#        layout.addWidget(self._help_checkBox2, 2,1,1,1)
#        
#        self.setLayout(layout)
#        
#        
#    def push_help_checkBox1(self):
#        QtWidgets.QMessageBox.information(self, 'MEEI Database', 
#                            'Database created using front face, standard clinical photographs from facial palsy patients', 
#                            QtWidgets.QMessageBox.Ok)
#              
#    def push_help_checkBox2(self):
#        QtWidgets.QMessageBox.information(self, 'iBUG Database', 
#                            'Database created as part of the iBUG project, it contains thousands of images taken in the wild along with face portaits obtained from the web', 
#                            QtWidgets.QMessageBox.Ok)   

class ShowSettings(QtWidgets.QDialog):
    def __init__(self,parent=None, ModelName='iBUG', CalibrationType='Iris', CalibrationValue=11.77):
        super(ShowSettings, self).__init__(parent)
        
        self.setWindowTitle('Settings')
        if os.name is 'posix': #is a mac or linux
            scriptDir = os.path.dirname(sys.argv[0])
        else: #is a  windows 
            scriptDir = os.getcwd()
   
        self.setWindowIcon(QtGui.QIcon(scriptDir + os.path.sep + 'include' +os.path.sep +'icon_color'+ os.path.sep + 'settings_icon.ico'))
        
        
        self._ModelName = ModelName
        self._CalibrationType = CalibrationType
        self._CalibrationValue = CalibrationValue
        
        self.tab1 = CalibrationTab(self, self._CalibrationType, self._CalibrationValue)
        self.tab2 = ModelTab(self, self._ModelName)
        
        self.main_Widget = QtWidgets.QTabWidget(self)
        self.tab1.setAutoFillBackground(True)
        self.tab2.setAutoFillBackground(True)
        self.main_Widget.addTab(self.tab1,self.tab1._tab_name)
        self.main_Widget.addTab(self.tab2,self.tab2._tab_name)

        
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
        if self.tab1._checkBox1.isChecked() == True:
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
                    self.close() 
            
            
        elif self.tab1._checkBox2.isChecked() == True:
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
                    self.close()
        
        
if __name__ == '__main__':
    if not QtWidgets.QApplication.instance():
        app = QtWidgets.QApplication(sys.argv)
    else:
        app = QtWidgets.QApplication.instance()
    GUI = ShowSettings()
    #GUI.show()
    app.exec_()