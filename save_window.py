# -*- coding: utf-8 -*-
"""
Created on Sat Dec  2 10:33:30 2017

@author: Diego L.Guarin -- diego_guarin at meei.harvard.edu
"""

import cv2
import numpy as np
import time
import os
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5.QtWidgets import QLabel, QLineEdit, QPushButton, QGridLayout, QFileDialog, QDialog, QComboBox


from utilities import get_info_from_txt
#from utilities import get_landmarks
#from utilities import get_pupil_from_image

from ProcessLandmarks import GetLandmarks


"""
This window will ask for some additional information and then save the facial measurements in a xls document. 

It will also save a txt file with the position of landmarks and eyes

it has an additional functionality where you can add results to an existing xls document by adding and additional row with the information of the current photo

"""

class MyLineEdit(QLineEdit):
    #I created a custom LineEdit object that will clear its content when selected
    #is used for the Patient ID which is initialized by default to the current date
    def __init__(self, parent=None):
        super(MyLineEdit, self).__init__(parent)

    def mousePressEvent(self, event):
        self.clear()   

        
class SaveWindow(QDialog):
    def __init__(self, parent=None, file_name = None):
        super(SaveWindow, self).__init__(parent)
        
        self._Patient = None    #This variable defines if the user is 
                                #trying to save results from a single photo  
                                #or from a patient. If the user is trying to 
                                #save results from a photo then it can select 
                                #the file that the results will be saved to, 
                                #if is saving a patient then this option is not 
                                #avaliable
        self._file_name = file_name
        delimiter = os.path.sep
        temp=self._file_name.split(delimiter)
        photo_location = temp[0:-1]
        photo_name=temp[-1]
        photo_location = delimiter.join(photo_location)

        
        self._photo_name = photo_name[0:-4]  #path + file name
        self._photo_location = photo_location
        self._ID = '' #unique identifier
        self._prevspost = '' #pre-treatment vs post-treatment
        self._surgery = '' #type of surgery
        self._expression = '' #type of expression
        self._other = '' #additional comments
        self._file_to_save = '' #file to add data 

        
        self.initUI()
        
    def initUI(self):
        
        self.setWindowTitle('Save')
        scriptDir = os.path.dirname(os.path.realpath(__file__))
        self.setWindowIcon(QtGui.QIcon(scriptDir + os.path.sep + 'include' +os.path.sep +'icon_color'+ os.path.sep + 'save_icon.ico'))
        
        self.main_Widget = QtWidgets.QWidget(self)
        
        spacerh = QtWidgets.QWidget(self)
        spacerh.setFixedSize(10,0)
        
        spacerv = QtWidgets.QWidget(self)
        spacerv.setFixedSize(0,10)
        
  
        file = QLabel('File Name:')
        self._file = QLineEdit(self)
        self._file.setText(self._photo_name)
        
        SelectFolderButton = QPushButton('Select &Folder', self)
        SelectFolderButton.setFixedWidth(150)
        SelectFolderButton.clicked.connect(self.SelectFolder)
        self._SelectFolder = QLineEdit(self)
        self._SelectFolder.setText(self._photo_location) 
        self._SelectFolder.setFixedWidth(350)
        
        Identifier = QLabel('Photo Identifier:')
        self._Identifier = QLineEdit(self)
        self._Identifier.setText(self._ID)
        
        
        #get the second photo
        PrevsPost = QLabel('Pre or Post Procedure:')
        self._PrevsPost = QComboBox()
        self._PrevsPost.setFixedWidth(110)
        self._PrevsPost.addItem('')
        self._PrevsPost.addItem('Pre - Procedure')
        self._PrevsPost.addItem('Post - Procedure')


        SurgeryType = QLabel('Procedure:')
        self._SurgeryType = QLineEdit(self)
        self._SurgeryType.setText(self._surgery)
        
        ExpressionType = QLabel('Expression:')
        self._ExpressionType = QLineEdit(self)
        self._ExpressionType.setText(self._expression)
        
        AddtitionalComments = QLabel('Addtitional Comments:')
        self._AddtitionalComments = QLineEdit(self)
        self._AddtitionalComments.setText(self._other)       
        
        
        SelectFileButton = QPushButton('&Select File', self)
        SelectFileButton.setFixedWidth(150)
        SelectFileButton.clicked.connect(self.SelectFile)       
        self._SelectFile = QLineEdit(self)
        self._SelectFile.setText(self._file_to_save) 
        
        
        
        SaveButton = QPushButton('&Save', self)
        SaveButton.setFixedWidth(150)
        SaveButton.clicked.connect(self.Done)
        
        CancelButton = QPushButton('&Cancel', self)
        CancelButton.setFixedWidth(150)
        CancelButton.clicked.connect(self.Cancel)
        
        
        layout = QGridLayout()
        layout.addWidget(file, 1,1,1,1)
        layout.addWidget(spacerh,1,2)
        layout.addWidget(self._file, 1,3,1,1)
        
        layout.addWidget(spacerv,2,0)
        
        layout.addWidget(SelectFolderButton, 3,1,1,1)
        layout.addWidget(self._SelectFolder , 3, 3, 1, 1)
       
        layout.addWidget(spacerv,4,0)
        
        layout.addWidget(Identifier, 5,1,1,1)
        layout.addWidget(self._Identifier , 5, 3, 1, 1)
        
        layout.addWidget(spacerv,6,0)
        
        layout.addWidget(PrevsPost, 7,1,1,1)
        layout.addWidget(self._PrevsPost, 7,3,1,1)
        
        layout.addWidget(spacerv,8,0)

        layout.addWidget(SurgeryType,9,1,1,1)
        layout.addWidget(self._SurgeryType,9, 3, 1, 1)
        
        layout.addWidget(spacerv,10,0)
        
        layout.addWidget(ExpressionType, 11,1,1,1)
        layout.addWidget(self._ExpressionType, 11,3,1,1)
        
        layout.addWidget(spacerv,12,0)
        
        layout.addWidget(AddtitionalComments, 13,1,1,1)
        layout.addWidget(self._AddtitionalComments, 13,3,1,1) 
        
        layout.addWidget(spacerv,14,0)
        
        layout.addWidget(SelectFileButton,15,1,1,1)
        layout.addWidget(self._SelectFile,15,3,1,1)
        
        layout.addWidget(spacerv,16,0)
        
        layout.addWidget(SaveButton,17,1,1,1, QtCore.Qt.AlignCenter)
        
        layout.addWidget(CancelButton,17,3,1,1, QtCore.Qt.AlignCenter)

        
        
        #self.main_Widget.setLayout(layout)
        #self.setCentralWidget(self.main_Widget)
        
        self.setLayout(layout)
        
        #self.show()
    

    def Cancel(self):
        self.close()  

        
    def Done(self):
        self.close()
        
    def SelectFolder(self):
        name = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select directory')
        
        if not name:
            pass
        else:
            name = os.path.normpath(name)
            self._photo_location = name
            self._SelectFolder.setText(self._photo_location) 
            self.update()
        
    def SelectFile(self):
        name,_ = QtWidgets.QFileDialog.getOpenFileName(
                self,'Load File',
                '',"Excel Spreadsheet  (*.xls *.xlsx)")
        
        if not name:
            pass
        else:
            name = os.path.normpath(name)
            delimiter = os.path.sep
            temp=name.split(delimiter)
            photo_location = temp[0:-1]
            photo_location = delimiter.join(photo_location)
            

            self._photo_location = photo_location
            self._SelectFolder.setText(self._photo_location) 
            
            self._file_to_save = name
            self._SelectFile.setText(self._file_to_save) 
            self.update()

       
      
if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    #if not QtWidgets.QApplication.instance():
    #    app = QtWidgets.QApplication(sys.argv)
    #else:
    #    app = QtWidgets.QApplication.instance()
       
    GUI =  SaveWindow()
    #GUI.show()
    app.exec_()
    

