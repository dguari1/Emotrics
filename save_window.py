# -*- coding: utf-8 -*-
"""
Created on Sat Dec  2 10:33:30 2017

@author: Diego L.Guarin -- diego_guarin at meei.harvard.edu
"""
import os
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5.QtWidgets import QLabel, QLineEdit, QPushButton, QGridLayout, QFileDialog, QDialog, QComboBox, QGroupBox


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
                                
        self._name_of_file = file_name  #this variable stores the name of the 
                                        #file, it won't be modified during 
                                        #execution                        
                                
        self._file_name = file_name     #this variable stores the name of the 
                                        #file to be displayed. It will be 
                                        #modified during execution 
        filename, file_extension = os.path.splitext(self._file_name) 
        delimiter = os.path.sep
        temp=filename.split(delimiter)
        photo_location = temp[0:-1]
        photo_location = delimiter.join(photo_location)
        photo_name=temp[-1]
       
        
        self._file_name = photo_name  #path + file name
        self._photo_location = photo_location
        self._ID = photo_name #unique identifier
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
        self._file.setText(self._file_name)
        
        self.SelectFolderButton = QPushButton('Select &Folder', self)
        self.SelectFolderButton.setFixedWidth(150)
        self.SelectFolderButton.clicked.connect(self.SelectFolder)
        self._SelectFolder = QLineEdit(self)
        self._SelectFolder.setText(self._photo_location) 
        self._SelectFolder.setFixedWidth(350)
        
        
        NewFileBox = QGroupBox('Create new File')
        NewFileBoxLayout = QGridLayout()
        NewFileBoxLayout.addWidget(file,0,0)
        NewFileBoxLayout.addWidget(spacerh,0,1)
        NewFileBoxLayout.addWidget(self._file,0,2)
        NewFileBoxLayout.addWidget(spacerv,1,0)
        NewFileBoxLayout.addWidget(self.SelectFolderButton,2,0)
        NewFileBoxLayout.addWidget(self._SelectFolder,2,2)
        NewFileBox.setLayout(NewFileBoxLayout)
        
        
        SelectFileButton = QPushButton('&Select File', self)
        SelectFileButton.setFixedWidth(150)
        SelectFileButton.clicked.connect(self.SelectFile)       
        self._SelectFile = QLineEdit(self)
        self._SelectFile.setText(self._file_to_save) 
        
        
        AppendFileBox = QGroupBox('Append to Existing File')
        AppendFileBoxLayout = QGridLayout()
        AppendFileBoxLayout.addWidget(SelectFileButton,0,0)
        AppendFileBoxLayout.addWidget(spacerh,0,1)
        AppendFileBoxLayout.addWidget(self._SelectFile,0,2)
        AppendFileBox.setLayout(AppendFileBoxLayout)
        
        
        Identifier = QLabel('Photo Identifier:')
        Identifier.setFixedWidth(120)
        self._Identifier = QLineEdit(self)
        self._Identifier.setText(self._ID)
        
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
        
        AdditionalInformationBox = QGroupBox('Optional Information')
        AdditionalInformationBoxLayout = QGridLayout()
        
        AdditionalInformationBoxLayout.addWidget(Identifier,0,0)
        AdditionalInformationBoxLayout.addWidget(spacerh,0,1)
        AdditionalInformationBoxLayout.addWidget(self._Identifier,0,2)
        
        AdditionalInformationBoxLayout.addWidget(spacerv,1,0)
        
        AdditionalInformationBoxLayout.addWidget(PrevsPost,2,0)
        AdditionalInformationBoxLayout.addWidget(self._PrevsPost,2,2)
        
        #AdditionalInformationBoxLayout.addWidget(spacerv,3,0) 
        
        AdditionalInformationBoxLayout.addWidget(SurgeryType,4,0)
        AdditionalInformationBoxLayout.addWidget(self._SurgeryType,4,2)
        
        #AdditionalInformationBoxLayout.addWidget(spacerv,5,0) 

        AdditionalInformationBoxLayout.addWidget(ExpressionType,6,0)
        AdditionalInformationBoxLayout.addWidget(self._ExpressionType,6,2)
        
        #AdditionalInformationBoxLayout.addWidget(spacerv,7,0)         

        AdditionalInformationBoxLayout.addWidget(AddtitionalComments,8,0)
        AdditionalInformationBoxLayout.addWidget(self._AddtitionalComments,8,2)    
        
        AdditionalInformationBox.setLayout(AdditionalInformationBoxLayout)
        
        
        
        SaveButton = QPushButton('&Save', self)
        SaveButton.setFixedWidth(150)
        SaveButton.clicked.connect(self.Done)
        
        CancelButton = QPushButton('&Cancel', self)
        CancelButton.setFixedWidth(150)
        CancelButton.clicked.connect(self.Cancel)
        
        
        ButtonBox = QGroupBox('')
        ButtonBoxLayout = QGridLayout()
        ButtonBoxLayout.addWidget(SaveButton,0,0,QtCore.Qt.AlignCenter)
        ButtonBoxLayout.addWidget(spacerh,0,1)
        ButtonBoxLayout.addWidget(CancelButton,0,2,QtCore.Qt.AlignCenter)
        ButtonBox.setLayout(ButtonBoxLayout)
        ButtonBox.setStyleSheet("QGroupBox {  border: 0px solid gray;}");
        
        layout = QGridLayout()

        layout.addWidget(NewFileBox,0,0,2,2)
        
        layout.addWidget(spacerv,1,0)
        
        layout.addWidget(AppendFileBox,2,0,1,2)
               
        
        layout.addWidget(AdditionalInformationBox,4,0,8,2)        
        
        layout.addWidget(ButtonBox,17,0,1,2)
        
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
            
            if not self._SelectFolder.isEnabled():        
                self._file.setEnabled(True)
                self._SelectFolder.setEnabled(True)
                self._SelectFile.setText('') 
                
                filename, file_extension = os.path.splitext(self._name_of_file) 
                delimiter = os.path.sep
                temp=filename.split(delimiter)
                photo_name=temp[-1]
                self._file.setText(photo_name)
                
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
            filename, file_extension = os.path.splitext(name)           
            temp=filename.split(delimiter)
            photo_location = temp[0:-1]
            photo_location = delimiter.join(photo_location)
            photo_name=temp[-1]
            
            self._file_name = photo_name
            
            self._file.setText(self._file_name)
            self._file.setEnabled(False)
            
            
            

            self._photo_location = photo_location
            self._SelectFolder.setText(self._photo_location) 
            self._SelectFolder.setEnabled(False)
            #self.SelectFolderButton.setEnabled(False)
            
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
    

