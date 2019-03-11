# -*- coding: utf-8 -*-
"""
Created on Sat Aug 19 12:54:17 2017

@author: Diego L.Guarin -- diego_guarin at meei.harvard.edu
"""

import os
import cv2
import numpy as np
import time
import sys
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5.QtWidgets import QLabel, QLineEdit, QPushButton, QGridLayout, QFileDialog, QDialog


from utilities import get_info_from_txt
#from utilities import get_landmarks
#from utilities import get_pupil_from_image

from ProcessLandmarks import GetLandmarks


"""
This window will ask for the patient information:
    - Patient ID (defautl current date)
    - First Photo and photo ID
    - Second Photo and photo ID
"""


class PhotoObject(object):
    #this is all the information associated with a photo
    def __init__(self):
        self._photo = None
        self._file_name = None
        self._name = ''
        self._ID = ''
        self._shape = None
        self._lefteye = None
        self._righteye = None
        self._points = None
        self._boundingbox = None

class Patient(object):
    #this is all the information associated with a patient 
    def __init__(self):
        self.patient_ID = time.strftime("%d-%m-%Y")
        self.FirstPhoto = PhotoObject()       
        self.SecondPhoto = PhotoObject()
        
    #def setPhotoObject
        
        
class MyLineEdit(QLineEdit):
    #I created a custom LineEdit object that will clear its content when selected
    #is used for the Patient ID which is initialized by default to the current date
    def __init__(self, parent=None):
        super(MyLineEdit, self).__init__(parent)

    def mousePressEvent(self, event):
        self.clear()   

        
class CreatePatient(QDialog):
    
    def __init__(self, parent=None, ModelName='iBUG'):
        super(CreatePatient, self).__init__(parent)
        
        self._Patient = None    #This variable is the final output of this 
                                #Widget. Its final value depends on the method 
                                #used to exit:
                                #If [X] or 'Cancel' (_ExitFlag = False) then the 
                                #ouput is None 
                                #If 'Done' (_ExitFlag = True) then the ouput is 
                                #a class->Patient containing two images and their
                                #information
   
        self._ExitFlag = False  #flag used to validate if the program should 
                                #return an empty output of an output with all
                                #the valid information. If the subject presses 
                                #'Cancel' or [X] to exit then _ExitFlag = False, 
                                #however, if the subject presses 'Done' and all
                                #the conditions are fullfiled then 
                                #_ExitFlag = True
                                
        self._ModelName  = ModelName #model that will be used for landmark 
                                     #localization
                                
                                
        #the estimation of landmarks and iris radius will be performed in a 
        #different thread to prevent the UI from freezing and crashing
        # create Thread  to take care of the landmarks and iris estimation   
        self.thread_landmarks = QtCore.QThread()  # no parent!
        
        self._Photo = None #this variable will contain the image
        self._file_name = None #this variable will contain the path + file name
        self._name = None #this variable will contain the file name
        self._PhotoPosition = None #First or second photo, this variable will carry that information
        
        self._Scale = 1
        
        
        self.initUI()
        
    def initUI(self):
        
        self.setWindowTitle('Create Patient')
        if os.name is 'posix': #is a mac or linux
            scriptDir = os.path.dirname(sys.argv[0])
        else: #is a  windows 
            scriptDir = os.getcwd()
        self.setWindowIcon(QtGui.QIcon(scriptDir + os.path.sep + 'include' +os.path.sep +'icon_color'+ os.path.sep + 'patient_icon.ico'))
        
        self.main_Widget = QtWidgets.QWidget(self)
        
        spacerh = QtWidgets.QWidget(self)
        spacerh.setFixedSize(20,0)
        
        spacerv = QtWidgets.QWidget(self)
        spacerv.setFixedSize(0,20)
        
        #create the patient object that will contain the ID and photos
        self._Patient= Patient()
        
        
        Patiend_ID_label = QLabel('Patient ID:')
        self._Patient_ID = MyLineEdit(self)
        self._Patient_ID.setText(self._Patient.patient_ID)
        
        #get the first photo
        FirstPhoto_label = QLabel('First Photo:')
        self._loadFirstPhoto = QPushButton('Load File', self)
        self._loadFirstPhoto.setFixedWidth(150)
        self._loadFirstPhoto.clicked.connect(lambda: self.LoadImage('first'))

        FirstPhoto_name_label = QLabel('File name:')
        self._FirstPhoto_name = QLineEdit(self)
        FirstPhoto_ID_label = QLabel('Photo ID:')
        self._FirstPhoto_ID = QLineEdit(self)
        
        #get the second photo
        SecondPhoto_label = QLabel('Second Photo:')
        self._loadSecondPhoto = QPushButton('Load File', self)
        self._loadSecondPhoto.setFixedWidth(150)
        self._loadSecondPhoto.clicked.connect(lambda: self.LoadImage('second'))

        SecondPhoto_name_label = QLabel('File name:')
        self._SecondPhoto_name = QLineEdit(self)
        SecondPhoto_ID_label = QLabel('Photo ID:')
        self._SecondPhoto_ID = QLineEdit(self)       
        
        
        DoneButton = QPushButton('&Done', self)
        DoneButton.setFixedWidth(150)
        DoneButton.clicked.connect(self.Done)
        CancelButton = QPushButton('&Cancel', self)
        CancelButton.setFixedWidth(150)
        CancelButton.clicked.connect(self.Cancel)
        
        
        layout = QGridLayout()
        layout.addWidget(Patiend_ID_label, 1,1,1,1)
        layout.addWidget(spacerh,1,2)
        layout.addWidget(self._Patient_ID, 1,3,1,1)
        
        layout.addWidget(spacerv,2,0)
       
        layout.addWidget(FirstPhoto_label, 3,1,1,1)
        layout.addWidget(spacerh,3,1)
        layout.addWidget(self._loadFirstPhoto, 3, 3, 1, 1)
        
        layout.addWidget(FirstPhoto_name_label, 4,1,1,1)
        layout.addWidget(self._FirstPhoto_name, 4,3,1,1)
        layout.addWidget(spacerh, 4,4)
        layout.addWidget(FirstPhoto_ID_label, 4,5,1,1)
        layout.addWidget(self._FirstPhoto_ID, 4,7,1,1)
        
        layout.addWidget(spacerv,5,0)

        layout.addWidget(SecondPhoto_label, 6,1,1,1)
        layout.addWidget(spacerh,6,1)
        layout.addWidget(self._loadSecondPhoto, 6, 3, 1, 1)
        
        layout.addWidget(SecondPhoto_name_label, 7,1,1,1)
        layout.addWidget(self._SecondPhoto_name, 7,3,1,1)
        layout.addWidget(spacerh, 7,4)
        layout.addWidget(SecondPhoto_ID_label, 7,5,1,1)
        layout.addWidget(self._SecondPhoto_ID, 7,7,1,1)      
        
        layout.addWidget(spacerv,8,0)
        layout.addWidget(DoneButton,9,3,1,1)
        layout.addWidget(spacerh, 9,4)
        layout.addWidget(CancelButton,9,5,1,1)

        
        
        #self.main_Widget.setLayout(layout)
        #self.setCentralWidget(self.main_Widget)
        
        self.setLayout(layout)
        
        #self.show()
    

    def Cancel(self):
        #we need to make sure that we are providing the correct information
        #to the main window, _ExitFlag = False -> No output after closing
        #_ExitFlag = True -> Valid output after closing
        self._ExitFlag = False
        self.close()  

        
    def Done(self):
        #check that everything was loaded before going back to the main window
        if (self._Patient.FirstPhoto is None) and (self._Patient.SecondPhoto is None):
            QtWidgets.QMessageBox.warning(self, "Error", 'No photo was loaded')
        elif (self._Patient.FirstPhoto is None) or (self._Patient.SecondPhoto is None):
            QtWidgets.QMessageBox.warning(self, "Error", 'Two photos are required')
        elif str(self._FirstPhoto_name.text()) == 'Invalid file':
            QtWidgets.QMessageBox.warning(self, "Error", 'The first photo is not valid')
        elif str(self._SecondPhoto_name.text()) == 'Invalid file':
            QtWidgets.QMessageBox.warning(self, "Error", 'The second photo is not valid')
        else:
            #Everything was loaded, now verify the photo IDs
            
            #if there is no photo ID then use the file name
            if str(self._FirstPhoto_ID.text()) == '':
                self._FirstPhoto_ID.setText(str(self._FirstPhoto_name.text()))
            if str(self._SecondPhoto_ID.text()) == '':
                self._SecondPhoto_ID.setText(str(self._SecondPhoto_name.text()))  
            
            #get the ID provided by the user and assignit to the photo object 
            self._Patient.FirstPhoto._ID = str(self._FirstPhoto_ID.text())
            self._Patient.SecondPhoto._ID = str(self._SecondPhoto_ID.text())
            
            #get the patient ID provided by the user 
            self._Patient.patient_ID = str(self._Patient_ID.text())
            
            #we need to make sure that we are providing the correct information
            #to the main window, _ExitFlag = False -> No output after closing
            #_ExitFlag = True -> Valid output after closing
            self._ExitFlag = True
            #all is done, close this window and return to the main window 
            self.close()

       
    #we need to make sure that if the subject closes the window (by pressing 
    #[X], 'Cancel' or 'Done') then the appropiate output is returned.
    #if [X] or 'Cancel' (_ExitFlag = False) then the ouput is None 
    #is 'Done' (_ExitFlag = True) then the ouput is a class Patient containing 
    #all the information
    def closeEvent(self, event):
        #we need to make sure that we are providing the correct information
        #to the main window, _ExitFlag = False -> output after closing is None
        #_ExitFlag = True -> Valid output after closing
        #this information will be used in the main window to decide wheter 
        #start processing as patient or not
        if self._ExitFlag is False:
            self._Patient = None
        event.accept()

    def LoadImage(self,position):
        #load a file using the widget
        name,_ = QFileDialog.getOpenFileName(
                self,'Load Image',
                '',"Image files (*.png *.jpg *.jpeg *.tif *.tiff *.PNG *.JPG *.JPEG *.TIF *.TIFF)")
        if not name:
            pass
        else:
            #if windows then transform / to \ (python stuffs)
            name = os.path.normpath(name)
            #load image into memory 
            self._Photo = cv2.imread(name)
            #is this information going to be the first or second photo, that 
            #information is in the variable 'position'
            self._PhotoPosition = position

            #get the image name (separete it from the path)
            delimiter = os.path.sep
            split_name=name.split(delimiter)
            
            #the variable 'name' contains the file name and the path, we now
            #get the file name and assign it to the photo object
            self._file_name = name
            self._name = split_name[-1]
            
            

            
            #if the photo was already processed then get the information for the
            #txt file, otherwise process the photo using the landmark ans pupil
            #localization algorithms 
            file_txt=name[:-4]
            file_txt = (file_txt + '.txt')
            if os.path.isfile(file_txt):
                shape,lefteye,righteye, boundingbox = get_info_from_txt(file_txt)
                
                #create a temporary photo object and fill its values. This variable
                #contains all the information that will be passed to the main 
                #window 
                temp_photo = PhotoObject()
                temp_photo._file_name = self._file_name
                temp_photo._name = self._name
                temp_photo._photo = self._Photo                
                temp_photo._lefteye = lefteye
                temp_photo._righteye = righteye 
                temp_photo._boundingbox = boundingbox
                temp_photo._shape = shape
                temp_photo._points = None
                #put all the information in the correct place (according to 
                #'position')
                self.AssignPhoto(temp_photo, self._PhotoPosition, 1)
            else:
                                #if the image is too large then it needs to be resized....
                h,w,d = self._Photo.shape

                #if the image is too big then we need to resize it so that the landmark 
                #localization process can be performed in a reasonable time 
                self._Scale = 1
                if h > 1500 or w > 1500 :
                    if h >= w :
                        h_n = 1500
                        self._Scale = h/h_n
                        w_n = int(np.round(w/self._Scale,0))
                        #self._Photo=cv2.resize(self._Photo, (w_n, h_n), interpolation=cv2.INTER_AREA)
                        temp_image = cv2.resize(self._Photo, (w_n, h_n), interpolation=cv2.INTER_AREA)
                        #self._image = image
                    else :
                        w_n = 1500
                        self._Scale = w/w_n
                        h_n = int(np.round(h/self._Scale,0))
                        #self._Photo=cv2.resize(self._Photo, (w_n, h_n), interpolation=cv2.INTER_AREA)
                        temp_image = cv2.resize(self._Photo, (w_n, h_n), interpolation=cv2.INTER_AREA)
                        #self._image = image     
                 
                    
#                    #now that the image has been reduced, ask the user if the image 
#                    #should be saved for continue the processing, otherwise the 
#                    #processing cannot continue with the large image
#                    
#                    #get the image name (separete it from the path)
#                    delimiter = os.path.sep
#                    split_name=name.split(delimiter)
#            
#                    #the variable 'name' contains the file name and the path, we now
#                    #get the file name and assign it to the photo object
#                    file_name = split_name[-1]
#                    new_file_name = file_name[:-4]+'_small.png'
#                    
#                    choice = QtWidgets.QMessageBox.information(self, 'Large Image', 
#                            'The image is too large to process.\n\nPressing OK will create a new file\n%s\nin the current folder. This file will be used for processing.\nOtherwise, click Close to finalize the App.'%new_file_name, 
#                            QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Close, QtWidgets.QMessageBox.Ok)
#
#                    if choice == QtWidgets.QMessageBox.Close :
#                        self.close()
#                        app.exec_()
#                    else:
#                        #create a new, smaller image and use that for processing
#                        name = name[:-4]+'_small.png'
#                        self._file_name = name
#                        cv2.imwrite(name,self._Photo)
#                        
#                        self._name = self._name[:-4]+'_small.png'
                else:
                    temp_image = self._Photo.copy()
                    #pass
                
                
                
                
                #get the landmarks using dlib, and the and the iris 
                #using Dougman's algorithm  
                #This is done in a separate thread to prevent the gui from 
                #freezing and crashing
                
                #create worker, pass the image to the worker
                ##self.landmarks = GetLandmarks(self._Photo)
                self.landmarks = GetLandmarks(temp_image, self._ModelName)
                #move worker to new thread
                self.landmarks.moveToThread(self.thread_landmarks)
                #start the new thread where the landmark processing will be performed
                self.thread_landmarks.start() 
                #Connect Thread started signal to Worker operational slot method
                self.thread_landmarks.started.connect(self.landmarks.getlandmarks)
                #connect signal emmited by landmarks to a function
                self.landmarks.landmarks.connect(self.ProcessShape)
                #define the end of the thread
                self.landmarks.finished.connect(self.thread_landmarks.quit) 
                
                
                
    def ProcessShape(self, shape, numFaces, lefteye, righteye, boundingbox):
        #the process that occured in another thread provide the shape and iris
        #information, if there is only one face then we store that information 
        #in a temporal variable 'temp_photo' and pass that to the main window 
        temp_photo = PhotoObject()
        if numFaces == 1 :            
            
            if self._Scale is not 1: #in case that a smaller image was used for 
                                     #processing, then update the landmark 
                                     #position with the scale factor
                for k in range(0,68):
                    shape[k] = [int(np.round(shape[k,0]*self._Scale,0)) ,
                                int(np.round(shape[k,1]*self._Scale,0))]
                    
                for k in range(0,3):
                    lefteye[k] = int(np.round(lefteye[k]*self._Scale,0))
                    righteye[k] = int(np.round(righteye[k]*self._Scale,0))
                    
                for k in range(0,4):
                    boundingbox[k] = int(np.round(boundingbox[k]*self._Scale,0))
                    
            
            temp_photo._file_name = self._file_name
            temp_photo._name = self._name
            temp_photo._photo = self._Photo     
            temp_photo._shape = shape
            temp_photo._lefteye = lefteye
            temp_photo._righteye = righteye
            temp_photo._boundingbox = boundingbox
            temp_photo._points = None
            
            #put all the information in the correct place (according to 
            #'position')
            self.AssignPhoto(temp_photo, self._PhotoPosition, numFaces)
        else: 
            #no face in image then shape is None
            
            #put all the information in the correct place (according to 
            #'position')
            self.AssignPhoto(temp_photo, self._PhotoPosition, numFaces)


    def AssignPhoto(self, photo_info, position, numFaces):
        #decideAssign whether the user loaded the first or second photo 
        if position is 'first':
            setattr(self._Patient, 'FirstPhoto', photo_info)
            #self._Patient.FirstPhoto = temp_photo
            if self._Patient.FirstPhoto._shape is not None:
                #present the file name to the user 
                self._FirstPhoto_name.setText(photo_info._name)
            else:
                #if there is not ladmark information (not face or 
                #multiple faces) then inform that the file is invalid
                self._FirstPhoto_name.setText('Invalid file')
                if numFaces == 0:
                    QtWidgets.QMessageBox.warning(self,"Warning",
                    "No face in the image.\nIf the image does contain a face plase modify the brightness and try again.",
                        QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.NoButton)
                elif numFaces > 1:
                    QtWidgets.QMessageBox.warning(self,"Warning",
                    "Multiple faces in the image.\nPlease load an image with a single face.",
                        QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.NoButton)
    
        elif position is 'second':
            setattr(self._Patient, 'SecondPhoto', photo_info)
            #self._Patient.SecondPhoto = temp_photo
            if self._Patient.SecondPhoto._shape is not None:
                #present the file name to the user 
                self._SecondPhoto_name.setText(photo_info._name)
            else:
                #if there is not ladmark information (not face or 
                #multiple faces) then inform that the file is invalid
                self._SecondPhoto_name.setText('Invalid file')
                if numFaces == 0:
                    QtWidgets.QMessageBox.warning(self,"Warning",
                    "No face in the image.\nIf the image does contain a face plase modify the brightness and try again.",
                        QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.NoButton)
                elif numFaces > 1:
                    QtWidgets.QMessageBox.warning(self,"Warning",
                    "Multiple faces in the image.\nPlease load an image with a single face.",
                        QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.NoButton)
        
                                
        
if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    #if not QtWidgets.QApplication.instance():
    #    app = QtWidgets.QApplication(sys.argv)
    #else:
    #    app = QtWidgets.QApplication.instance()
       
    GUI = CreatePatient()
    #GUI.show()
    app.exec_()
    

