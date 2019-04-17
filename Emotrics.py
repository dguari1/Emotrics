# -*- coding: utf-8 -*-
"""
Created on Sat Aug 12 18:41:24 2017

@author: Diego L.Guarin -- diego_guarin at meei.harvard.edu
"""
import os 
import sys
import cv2
import numpy as np

from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore




from results_window import ShowResults
from results_window import CustomTabResult

from ImageViewerandProcess import ImageViewer
from patient_window import CreatePatient


from measurements import get_measurements_from_data

from utilities import estimate_lines
from utilities import get_info_from_txt
#from utilities import get_landmarks
#from utilities import get_pupil_from_image
from utilities import mark_picture
from utilities import save_snaptshot_to_file
from utilities import save_txt_file
from utilities import save_xls_file_patient
from utilities import get_landmark_size

from ProcessLandmarks import GetLandmarks

from save_window import SaveWindow
from settings_window import ShowSettings





"""
This is the main window of the program, it contains a ToolBar and a GraphicsView objects. 

The toolbar includes actions for:
    - Load Image: Loads an image and localizes the landmarks and iris in the image. 
    If the image is not a single face then it skips the landmark and iris 
    localization. If the landmark information is available in a txt file then 
    the program uses this to place the landmarks and skips the automatic landmark
    localization.
    
    - Create Patient: Opens up a new window where the user can load two images 
    that will be compared, the landmark and iris localization is perform during
    the image loading so that if the image is not a single face the user will be
    informed and won't be allowed to continue. The only ways to close the new 
    window are by loading to valid images (single faces) or cancelling. In this
    window is possible to assign an ID to the patient (by default is the current
    date) and to each photo. 
    Future improvements might include facial recognition to verify that both 
    photos are from the same patient 
    
    - Change photo: allows to move between the patient photos. It is un-active  
    if there is no patient. Once the patient is created this action becomes 
    active
    
    - Fit image to window: Fits the image to the current size of the window. 
    Useful after zoom-in the picture to go back to full-view in one click
    
    - Match iris diameter: Makes sure that both iris have the same diameter by 
    enlarging the smaller circle fitted to the iris. Is usefull when one eye is 
    closed and is difficul to properly find the iris size.
    
    - Find face center: It fits a line connecting the center of both iris and 
    a new, perperdicular line in the middle. It is usefull to divide the 
    face vertically. 
    
    - Toggle landmarks: It toggles on or off the landmarks from the face, is 
    usefull if you want to see the face without anything added to it.
    
    - Facial metrics: It opens up a new window displaying a set of important 
    facial metrics. In there is possible to see a description and a graphical 
    explanation of each metric. It has two different modes: If a single image 
    is being processed, the new window will present a table containing the 
    metrics for both sides of the face, the absolute difference and a percent
    difference based on the non-paralyzed side measurements. If a patient is
    being analyzed (two photos) the new window contains three tabs, one for each 
    image and a third one computing the variation in the metrics between both
    images. This is useful to compare pre and post-operative cases.
    
    - Save results: Produces two files in the selected folder. 
    One text (.txt) file containing the landmarks information, and an excel (.xls)
    file containing the facial metrics. If the a patient is being processed (two
    images) then the excel file contains information about each image and the 
    difference. The excel file name will be the same as the photo file name but 
    can be easily changed within the same manu. User can also chose to append 
    results to an existing xls file.
    
    - Save current view: Saves the current view as png or jpg file. 
    
    - Settings: Allows for further customization of the 
    software. It facilitates the selection of scale (currently we assume that 
    the iris diamater is 11.77mm), and the selection of the model used for 
    landmark detection. Avaliable models:
        - iBUG -> Trained with in the wild photos
        - MEE -> trained with facial palsy patients photos
    
    - Exit: Exits the program 
"""


class window(QtWidgets.QWidget):
    
    def __init__(self):
        super(window, self).__init__()
        #self.setGeometry(5,60,700,500)
        
        self.setWindowTitle('Emotrics')    
        
        if os.name is 'posix': #is a mac or linux
            scriptDir = os.path.dirname(sys.argv[0])
        else: #is a  windows 
            scriptDir = os.getcwd()


        self.setWindowIcon(QtGui.QIcon(scriptDir + os.path.sep + 'include' +os.path.sep +'icon_color'+ os.path.sep + 'meei_3WR_icon.ico'))
        
        self._new_window = None
        self._file_name = None
        self._Patient = None
        self._tab1_results = None
        self._tab2_results = None         
        self._tab3_results = None    
        self._toggle_landmaks = True
        self._toggle_lines = True
        
        self._whichPhotofromPatient = None # variable used to figure out which photo from patient is being analyzed 
        
        
        self._Scale = 1  #this variable carries the scale of the image if it 
                        #needs to be resized, if Scale = 1 then the origina 
                        #image was used for processing. If Scale > 1 then 
                        #the original image was too large and a resized image
                        #was used for processing
        
        
        # create Thread  to take care of the landmarks and iris estimation   
        self.thread_landmarks = QtCore.QThread()  # no parent!
        
        
        #these are additional steps that i had to take to be able to update the model on the fly...
        self.threadFirstPhoto = QtCore.QThread()  # no parent!
        self.threadSecondPhoto = QtCore.QThread()  # no parent!
        
        
        self._CalibrationType = 'Iris'  #_CalibrationType can be 'Iris' or 'Manual'
        self._CalibrationValue = 11.77 #calibration parameter
        
        self._ModelName = 'MEE' #_ModelType can be 'iBUGS' or 'MEE'
        
      
        #initialize the User Interface
        self.initUI()
        
    def initUI(self):
        #local directory
        
        if os.name is 'posix': #is a mac or linux
            scriptDir = os.path.dirname(sys.argv[0])
        else: #is a  windows 
            scriptDir = os.getcwd()

        #read the image from file        
        img_Qt = QtGui.QImage(scriptDir + os.path.sep + 'include' +os.path.sep +'icon_color'+ os.path.sep + 'Facial-Nerve-Center.jpg')
        img_show = QtGui.QPixmap.fromImage(img_Qt)
        
        #the image will be displayed in the custom ImageViewer
        self.displayImage = ImageViewer()      
        self.displayImage.setPhoto(img_show)    
        
        #toolbar         
        loadAction = QtWidgets.QAction('Load image', self)
        loadAction.setIcon(QtGui.QIcon(scriptDir + os.path.sep + 'include' +os.path.sep +'icon_color'+ os.path.sep + 'load_icon.png'))
        loadAction.triggered.connect(self.load_file)
        
        createPatientAction = QtWidgets.QAction('Create patient', self)
        createPatientAction.setIcon( QtGui.QIcon(scriptDir + os.path.sep + 'include' +os.path.sep +'icon_color'+ os.path.sep + 'patient_icon.png'))
        createPatientAction.triggered.connect(self.CreatePatient)
        
        #this action will be only active when a patient is created (i.e., there
        #are two photos to analize), that's why I'm making it a persisten 
        #element of the class, so that its state (Enble=True or Enable=False)
        #can be modified during the execution of the program 
        self.changephotoAction = QtWidgets.QAction('Change image', self)
        self.changephotoAction.setIcon(QtGui.QIcon(scriptDir + os.path.sep + 'include' +os.path.sep +'icon_color'+ os.path.sep + 'change_photo_icon.png'))
        self.changephotoAction.setEnabled(False)
        self.changephotoAction.triggered.connect(self.ChangePhoto)
        
        fitAction = QtWidgets.QAction('Fit image to window', self)
        fitAction.setIcon(QtGui.QIcon(scriptDir + os.path.sep + 'include' +os.path.sep +'icon_color'+ os.path.sep + 'fit_to_size_icon.png'))
        fitAction.triggered.connect(self.displayImage.show_entire_image)
        
        eyeAction = QtWidgets.QAction('Match iris diameter', self)
        eyeAction.setIcon(QtGui.QIcon(scriptDir + os.path.sep + 'include' +os.path.sep +'icon_color'+ os.path.sep + 'eye_icon.png'))
        eyeAction.triggered.connect(self.match_iris)

        eyeLoad = QtWidgets.QAction('Import iris position and diameter', self)
        eyeLoad.setIcon(QtGui.QIcon(scriptDir + os.path.sep + 'include' +os.path.sep +'icon_color'+ os.path.sep + 'eye_icon_import.png'))
        eyeLoad.triggered.connect(self.load_iris)
        
        centerAction = QtWidgets.QAction('Find face center', self)
        centerAction.setIcon(QtGui.QIcon(scriptDir + os.path.sep + 'include' +os.path.sep +'icon_color'+ os.path.sep + 'center_icon.png'))
        centerAction.triggered.connect(self.face_center)
        
        toggleAction = QtWidgets.QAction('Toggle landmarks', self)
        toggleAction.setIcon(QtGui.QIcon(scriptDir + os.path.sep + 'include' +os.path.sep +'icon_color'+ os.path.sep + 'toggle-icon.png'))
        toggleAction.triggered.connect(self.toggle_landmarks)
        
        measuresAction = QtWidgets.QAction('Facial metrics', self)
        measuresAction.setIcon(QtGui.QIcon(scriptDir + os.path.sep + 'include' +os.path.sep +'icon_color'+ os.path.sep + 'ruler_icon.png'))
        measuresAction.triggered.connect(self.create_new_window)
        
        saveAction = QtWidgets.QAction('Save results', self)
        saveAction.setIcon(QtGui.QIcon(scriptDir + os.path.sep + 'include' +os.path.sep +'icon_color'+ os.path.sep + 'save_icon.png'))
        saveAction.triggered.connect(self.save_results)
        
        snapshotAction = QtWidgets.QAction('Save current view', self)
        snapshotAction.setIcon(QtGui.QIcon(scriptDir + os.path.sep + 'include' +os.path.sep +'icon_color'+ os.path.sep + 'snapshot_icon.png'))
        snapshotAction.triggered.connect(self.save_snapshot)
        
        settingsAction = QtWidgets.QAction('Change Settings', self)
        settingsAction.setIcon(QtGui.QIcon(scriptDir + os.path.sep + 'include' +os.path.sep +'icon_color'+ os.path.sep + 'settings-icon.png'))
        settingsAction.triggered.connect(self.settings)
        
        AboutAction = QtWidgets.QAction('About', self)
        AboutAction.setIcon(QtGui.QIcon(scriptDir + os.path.sep + 'include' +os.path.sep +'icon_color'+ os.path.sep + 'question_icon.png'))
        AboutAction.triggered.connect(self.about_app)
        
        exitAction = QtWidgets.QAction('Exit', self)
        exitAction.setIcon(QtGui.QIcon(scriptDir + os.path.sep + 'include' +os.path.sep +'icon_color'+ os.path.sep + 'exit_icon.png'))
        exitAction.triggered.connect(self.close_app)
                
        
        #create the toolbar and add the actions 
        self.toolBar = QtWidgets.QToolBar(self)
        self.toolBar.addActions((loadAction, createPatientAction, self.changephotoAction, 
                                 fitAction, eyeAction, eyeLoad,centerAction, toggleAction,
                                 measuresAction, snapshotAction, saveAction,  settingsAction, 
                                 AboutAction,exitAction))
        
        #set the size of each icon to 50x50
        self.toolBar.setIconSize(QtCore.QSize(50,50))
        
        for action in self.toolBar.actions():
            widget = self.toolBar.widgetForAction(action)
            widget.setFixedSize(50, 50)
           
        self.toolBar.setMinimumSize(self.toolBar.sizeHint())
        self.toolBar.setStyleSheet('QToolBar{spacing:5px;}')

        
        #the main window consist of the toolbar and the ImageViewer
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.toolBar)
        layout.addWidget(self.displayImage)
        self.setLayout(layout)
        

        
        self.show()
        
    def CreatePatient(self):
        #Opens a new window where the patient informaiton will be provided
        #it waits until all the valid information has been provided before 
        #moving forward
        
        
        #close the measurement window if open 
        if self._new_window is not None:
            self._new_window.close()
        
        ##delete previous patients is any is in memory
        #if self._Patient is not None:
        #    self._Patient = None
            
        temp = CreatePatient(self, self._ModelName)
        temp.exec_()  #this action replaces temp.show()
        #in this care the program will stop until the window created by 
        #CreatePatient is closed, and this window can only be closed if two 
        #valid images are provided or if the user clicks cancel

        #verifry that the user actually created a patient and didn't just hit 
        #cancel        
        if temp._Patient is not None :
            #if there is a new patient then:
            
            #Assign the patient Class to the appropiate variable
            self._Patient = temp._Patient 
            
            #now that we have the patient info (two photos) we need to show the
            #first photo (and allow the user to modify its info) and activate 
            #the change photo action 
            self.changephotoAction.setEnabled(True)
            
            #now pour all the information obtained in the create patient window 
            #into the imagedisplay object. The FirstPhoto will be presented first 
            self._file_name = self._Patient.FirstPhoto._file_name
            self.displayImage._opencvimage = self._Patient.FirstPhoto._photo
            self.displayImage._lefteye = self._Patient.FirstPhoto._lefteye 
            self.displayImage._righteye = self._Patient.FirstPhoto._righteye
            self.displayImage._shape = self._Patient.FirstPhoto._shape
            self.displayImage._points = self._Patient.FirstPhoto._points
            self.displayImage._boundingbox = self._Patient.FirstPhoto._boundingbox
            #change 3/7/2019
            if self.displayImage._landmark_size is None:
                self.displayImage._landmark_size = get_landmark_size(self.displayImage._shape)
            
            #reset the Imagedisplay object to show the image
            self.displayImage.update_view()
            self.setWindowTitle('Emotrics - '+self._Patient.patient_ID+' -- '+self._file_name.split(os.path.sep)[-1])
        
    def ChangePhoto(self):
        #function used to change the current photo of the patient
        self._toggle_lines = True #set the toggle lines to true
        #if this button is active it means that the patient was successfully 
        #created and there are two photos to work with. The user can use this
        #button to navigate between those two photos
        if self._file_name == self._Patient.FirstPhoto._file_name:
            #the first photo is on memory and we wnat to move to the second photo.
            
            #first update the information from the screen to the memory on the
            #first photo
            self._Patient.FirstPhoto._lefteye = self.displayImage._lefteye
            self._Patient.FirstPhoto._righteye = self.displayImage._righteye
            self._Patient.FirstPhoto._shape =  self.displayImage._shape
            self._Patient.FirstPhoto._points = self.displayImage._points
            
            #now update the displayImage object with the second photo info 
            self._file_name = self._Patient.SecondPhoto._file_name
            self.displayImage._opencvimage = self._Patient.SecondPhoto._photo
            self.displayImage._lefteye = self._Patient.SecondPhoto._lefteye 
            self.displayImage._righteye = self._Patient.SecondPhoto._righteye
            self.displayImage._shape = self._Patient.SecondPhoto._shape
            self.displayImage._points = self._Patient.SecondPhoto._points
            self.displayImage._boundingbox = self._Patient.SecondPhoto._boundingbox
            #change 3/7/2019
            if self.displayImage._landmark_size is None:
                self.displayImage._landmark_size = get_landmark_size(self.displayImage._shape)
            
        elif self._file_name == self._Patient.SecondPhoto._file_name:
            #the second photo is on memory and we wnat to move to the first photo
            #first update the information from the screen to the memory on the
            #second photo
            self._Patient.SecondPhoto._lefteye = self.displayImage._lefteye
            self._Patient.SecondPhoto._righteye = self.displayImage._righteye
            self._Patient.SecondPhoto._shape =  self.displayImage._shape
            self._Patient.SecondPhoto._points = self.displayImage._points
            
            #just update the displayImage object with the First photo info
            self._file_name = self._Patient.FirstPhoto._file_name
            self.displayImage._opencvimage = self._Patient.FirstPhoto._photo
            self.displayImage._lefteye = self._Patient.FirstPhoto._lefteye 
            self.displayImage._righteye = self._Patient.FirstPhoto._righteye
            self.displayImage._shape = self._Patient.FirstPhoto._shape
            self.displayImage._points = self._Patient.FirstPhoto._points
            self.displayImage._boundingbox = self._Patient.FirstPhoto._boundingbox
            #change 3/7/2019
            if self.displayImage._landmark_size is None:
                self.displayImage._landmark_size = get_landmark_size(self.displayImage._shape)
      
        #reset the Imagedisplay object to show the imagew
        self.displayImage.update_view()
        self.setWindowTitle('Emotrics - '+self._Patient.patient_ID+' -- '+self._file_name.split(os.path.sep)[-1])
        
        
    def create_new_window(self):
        #this creates a new window to display all the facial metrics, there 
        #are two modes, one if there is no Patient (self._Patient = None)
        #and another if there is a patient (two photos)
        if self._Patient is None:
        
            if self.displayImage._shape is not None:
                #if the measurements window is already open then close it
                if self._new_window is not None:
                    self._new_window.close()
                    self._new_window = None
                
                #compute the facial metrics using the landmarks 
                MeasurementsLeft, MeasurementsRight, MeasurementsDeviation, MeasurementsPercentual = get_measurements_from_data(self.displayImage._shape, self.displayImage._lefteye, self.displayImage._righteye, self._CalibrationType, self._CalibrationValue)
                
                #send all the information the the appropiate places in the window 
                self._tab1_results  =  CustomTabResult()
                
                #filling t_new_window_tab1_results he info for the right
                self._tab1_results._CE_right.setText('{0:.2f}'.format(MeasurementsRight.CommissureExcursion))
                self._tab1_results._SA_right.setText('{0:.2f}'.format(MeasurementsRight.SmileAngle))
                self._tab1_results._DS_right.setText('{0:.2f}'.format(MeasurementsRight.DentalShow))
                self._tab1_results._MRD1_right.setText('{0:.2f}'.format(MeasurementsRight.MarginalReflexDistance1))
                self._tab1_results._MRD2_right.setText('{0:.2f}'.format(MeasurementsRight.MarginalReflexDistance2))
                self._tab1_results._BH_right.setText('{0:.2f}'.format(MeasurementsRight.BrowHeight))
                self._tab1_results._PFH_right.setText('{0:.2f}'.format(MeasurementsRight.PalpebralFissureHeight))
    
                
                #filling the info for the left
                self._tab1_results._CE_left.setText('{0:.2f}'.format(MeasurementsLeft.CommissureExcursion))
                self._tab1_results._SA_left.setText('{0:.2f}'.format(MeasurementsLeft.SmileAngle))
                self._tab1_results._DS_left.setText('{0:.2f}'.format(MeasurementsLeft.DentalShow))
                self._tab1_results._MRD1_left.setText('{0:.2f}'.format(MeasurementsLeft.MarginalReflexDistance1))
                self._tab1_results._MRD2_left.setText('{0:.2f}'.format(MeasurementsLeft.MarginalReflexDistance2))
                self._tab1_results._BH_left.setText('{0:.2f}'.format(MeasurementsLeft.BrowHeight))
                self._tab1_results._PFH_left.setText('{0:.2f}'.format(MeasurementsLeft.PalpebralFissureHeight))
                
                #deviation
                self._tab1_results._CE_dev.setText('{0:.2f}'.format(MeasurementsDeviation.CommissureExcursion))
                self._tab1_results._SA_dev.setText('{0:.2f}'.format(MeasurementsDeviation.SmileAngle))
                self._tab1_results._MRD1_dev.setText('{0:.2f}'.format(MeasurementsDeviation.MarginalReflexDistance1))
                self._tab1_results._MRD2_dev.setText('{0:.2f}'.format(MeasurementsDeviation.MarginalReflexDistance2))
                self._tab1_results._BH_dev.setText('{0:.2f}'.format(MeasurementsDeviation.BrowHeight))
                self._tab1_results._DS_dev.setText('{0:.2f}'.format(MeasurementsDeviation.DentalShow))
                self._tab1_results._CH_dev.setText('{0:.2f}'.format(MeasurementsDeviation.CommisureHeightDeviation))
                self._tab1_results._UVH_dev.setText('{0:.2f}'.format(MeasurementsDeviation.UpperLipHeightDeviation))
                self._tab1_results._LVH_dev.setText('{0:.2f}'.format(MeasurementsDeviation.LowerLipHeightDeviation))
                self._tab1_results._PFH_dev.setText('{0:.2f}'.format(MeasurementsDeviation.PalpebralFissureHeight))
                
                
                self._tab1_results._CE_dev_p.setText('{0:.2f}'.format(MeasurementsPercentual.CommissureExcursion))
                self._tab1_results._SA_dev_p.setText('{0:.2f}'.format(MeasurementsPercentual.SmileAngle))
                self._tab1_results._MRD1_dev_p.setText('{0:.2f}'.format(MeasurementsPercentual.MarginalReflexDistance1))
                self._tab1_results._MRD2_dev_p.setText('{0:.2f}'.format(MeasurementsPercentual.MarginalReflexDistance2))
                self._tab1_results._BH_dev_p.setText('{0:.2f}'.format(MeasurementsPercentual.BrowHeight))
                self._tab1_results._DS_dev_p.setText('{0:.2f}'.format(MeasurementsPercentual.DentalShow))
                self._tab1_results._PFH_dev_p.setText('{0:.2f}'.format(MeasurementsPercentual.PalpebralFissureHeight))
                
                
                delimiter = os.path.sep
                temp=self._file_name.split(delimiter)
                photo_name=temp[-1]
                photo_name=photo_name[0:-4]
                self._tab1_results._tab_name=photo_name
                
                
                #say to the window that presents the results that there is only 1 tab
                self._new_window = ShowResults(self._tab1_results)
                #show the window with the results 
                self._new_window.show()
                
        else:
            #here there is a patient and so the result window will have three tabs
            if (self._Patient.FirstPhoto._shape is not None) and (self._Patient.SecondPhoto._shape is not None):
                #if the measurements window is already open then close it
                if self._new_window is not None:
                    self._new_window.close()
                    self._new_window = None
                    
                 
                 #update the information from the display to memory    
                if self._file_name == self._Patient.FirstPhoto._file_name:
                    #the first photo is being displayed, update the information 
                    #from the screen to the memory 
                    self._Patient.FirstPhoto._lefteye = self.displayImage._lefteye
                    self._Patient.FirstPhoto._righteye = self.displayImage._righteye
                    self._Patient.FirstPhoto._shape =  self.displayImage._shape
                    self._Patient.FirstPhoto._points = self.displayImage._points
            
            
                elif self._file_name == self._Patient.SecondPhoto._file_name:
                    #the second photo is on display, update the information 
                    #sfrom the screen to the memory on the econd photo
                    self._Patient.SecondPhoto._lefteye = self.displayImage._lefteye
                    self._Patient.SecondPhoto._righteye = self.displayImage._righteye
                    self._Patient.SecondPhoto._shape =  self.displayImage._shape
                    self._Patient.SecondPhoto._points = self.displayImage._points
            

                    
                #compute the facial metrics for the first photo and fill the information 
                MeasurementsLeftFirst, MeasurementsRightFirst, MeasurementsDeviation, MeasurementsPercentual = get_measurements_from_data(self._Patient.FirstPhoto._shape, self._Patient.FirstPhoto._lefteye, self._Patient.FirstPhoto._righteye, self._CalibrationType, self._CalibrationValue)
                
                self._tab1_results  =  CustomTabResult()
                
                #filling t_new_window_tab1_results he info for the right
                self._tab1_results._CE_right.setText('{0:.2f}'.format(MeasurementsRightFirst.CommissureExcursion))
                self._tab1_results._SA_right.setText('{0:.2f}'.format(MeasurementsRightFirst.SmileAngle))
                self._tab1_results._DS_right.setText('{0:.2f}'.format(MeasurementsRightFirst.DentalShow))
                self._tab1_results._MRD1_right.setText('{0:.2f}'.format(MeasurementsRightFirst.MarginalReflexDistance1))
                self._tab1_results._MRD2_right.setText('{0:.2f}'.format(MeasurementsRightFirst.MarginalReflexDistance2))
                self._tab1_results._BH_right.setText('{0:.2f}'.format(MeasurementsRightFirst.BrowHeight))
                self._tab1_results._PFH_right.setText('{0:.2f}'.format(MeasurementsRightFirst.PalpebralFissureHeight))
                
                #filling the info for the left
                self._tab1_results._CE_left.setText('{0:.2f}'.format(MeasurementsLeftFirst.CommissureExcursion))
                self._tab1_results._SA_left.setText('{0:.2f}'.format(MeasurementsLeftFirst.SmileAngle))
                self._tab1_results._DS_left.setText('{0:.2f}'.format(MeasurementsLeftFirst.DentalShow))
                self._tab1_results._MRD1_left.setText('{0:.2f}'.format(MeasurementsLeftFirst.MarginalReflexDistance1))
                self._tab1_results._MRD2_left.setText('{0:.2f}'.format(MeasurementsLeftFirst.MarginalReflexDistance2))
                self._tab1_results._BH_left.setText('{0:.2f}'.format(MeasurementsLeftFirst.BrowHeight))
                self._tab1_results._PFH_left.setText('{0:.2f}'.format(MeasurementsLeftFirst.PalpebralFissureHeight))
                
                #deviation
                self._tab1_results._CE_dev.setText('{0:.2f}'.format(MeasurementsDeviation.CommissureExcursion))
                self._tab1_results._SA_dev.setText('{0:.2f}'.format(MeasurementsDeviation.SmileAngle))
                self._tab1_results._MRD1_dev.setText('{0:.2f}'.format(MeasurementsDeviation.MarginalReflexDistance1))
                self._tab1_results._MRD2_dev.setText('{0:.2f}'.format(MeasurementsDeviation.MarginalReflexDistance2))
                self._tab1_results._BH_dev.setText('{0:.2f}'.format(MeasurementsDeviation.BrowHeight))
                self._tab1_results._DS_dev.setText('{0:.2f}'.format(MeasurementsDeviation.DentalShow))
                self._tab1_results._CH_dev.setText('{0:.2f}'.format(MeasurementsDeviation.CommisureHeightDeviation))
                self._tab1_results._UVH_dev.setText('{0:.2f}'.format(MeasurementsDeviation.UpperLipHeightDeviation))
                self._tab1_results._LVH_dev.setText('{0:.2f}'.format(MeasurementsDeviation.LowerLipHeightDeviation))
                self._tab1_results._PFH_dev.setText('{0:.2f}'.format(MeasurementsDeviation.PalpebralFissureHeight))
                
                self._tab1_results._CE_dev_p.setText('{0:.2f}'.format(MeasurementsPercentual.CommissureExcursion))
                self._tab1_results._SA_dev_p.setText('{0:.2f}'.format(MeasurementsPercentual.SmileAngle))
                self._tab1_results._MRD1_dev_p.setText('{0:.2f}'.format(MeasurementsPercentual.MarginalReflexDistance1))
                self._tab1_results._MRD2_dev_p.setText('{0:.2f}'.format(MeasurementsPercentual.MarginalReflexDistance2))
                self._tab1_results._BH_dev_p.setText('{0:.2f}'.format(MeasurementsPercentual.BrowHeight))
                self._tab1_results._DS_dev_p.setText('{0:.2f}'.format(MeasurementsPercentual.DentalShow))
                self._tab1_results._PFH_dev_p.setText('{0:.2f}'.format(MeasurementsPercentual.PalpebralFissureHeight))
                
                
                self._tab1_results._tab_name=self._Patient.FirstPhoto._ID
                
                
                #compute the facial metrics for the second photo and fill the information 
                MeasurementsLeftSecond, MeasurementsRightSecond, MeasurementsDeviation, MeasurementsPercentual = get_measurements_from_data(self._Patient.SecondPhoto._shape, self._Patient.SecondPhoto._lefteye, self._Patient.SecondPhoto._righteye, self._CalibrationType, self._CalibrationValue)
                
                self._tab2_results  =  CustomTabResult()
                
                #filling t_new_window_tab1_results he info for the right
                self._tab2_results._CE_right.setText('{0:.2f}'.format(MeasurementsRightSecond.CommissureExcursion))
                self._tab2_results._SA_right.setText('{0:.2f}'.format(MeasurementsRightSecond.SmileAngle))
                self._tab2_results._DS_right.setText('{0:.2f}'.format(MeasurementsRightSecond.DentalShow))
                self._tab2_results._MRD1_right.setText('{0:.2f}'.format(MeasurementsRightSecond.MarginalReflexDistance1))
                self._tab2_results._MRD2_right.setText('{0:.2f}'.format(MeasurementsRightSecond.MarginalReflexDistance2))
                self._tab2_results._BH_right.setText('{0:.2f}'.format(MeasurementsRightSecond.BrowHeight))
                self._tab2_results._PFH_right.setText('{0:.2f}'.format(MeasurementsRightSecond.PalpebralFissureHeight))
    
                
                #filling the info for the left
                self._tab2_results._CE_left.setText('{0:.2f}'.format(MeasurementsLeftSecond.CommissureExcursion))
                self._tab2_results._SA_left.setText('{0:.2f}'.format(MeasurementsLeftSecond.SmileAngle))
                self._tab2_results._DS_left.setText('{0:.2f}'.format(MeasurementsLeftSecond.DentalShow))
                self._tab2_results._MRD1_left.setText('{0:.2f}'.format(MeasurementsLeftSecond.MarginalReflexDistance1))
                self._tab2_results._MRD2_left.setText('{0:.2f}'.format(MeasurementsLeftSecond.MarginalReflexDistance2))
                self._tab2_results._BH_left.setText('{0:.2f}'.format(MeasurementsLeftSecond.BrowHeight))
                self._tab2_results._PFH_left.setText('{0:.2f}'.format(MeasurementsLeftSecond.PalpebralFissureHeight))
                
                #deviation
                self._tab2_results._CE_dev.setText('{0:.2f}'.format(MeasurementsDeviation.CommissureExcursion))
                self._tab2_results._SA_dev.setText('{0:.2f}'.format(MeasurementsDeviation.SmileAngle))
                self._tab2_results._MRD1_dev.setText('{0:.2f}'.format(MeasurementsDeviation.MarginalReflexDistance1))
                self._tab2_results._MRD2_dev.setText('{0:.2f}'.format(MeasurementsDeviation.MarginalReflexDistance2))
                self._tab2_results._BH_dev.setText('{0:.2f}'.format(MeasurementsDeviation.BrowHeight))
                self._tab2_results._DS_dev.setText('{0:.2f}'.format(MeasurementsDeviation.DentalShow))
                self._tab2_results._CH_dev.setText('{0:.2f}'.format(MeasurementsDeviation.CommisureHeightDeviation))
                self._tab2_results._UVH_dev.setText('{0:.2f}'.format(MeasurementsDeviation.UpperLipHeightDeviation))
                self._tab2_results._LVH_dev.setText('{0:.2f}'.format(MeasurementsDeviation.LowerLipHeightDeviation))
                self._tab2_results._PFH_dev.setText('{0:.2f}'.format(MeasurementsDeviation.PalpebralFissureHeight))
                
                self._tab2_results._CE_dev_p.setText('{0:.2f}'.format(MeasurementsPercentual.CommissureExcursion))
                self._tab2_results._SA_dev_p.setText('{0:.2f}'.format(MeasurementsPercentual.SmileAngle))
                self._tab2_results._MRD1_dev_p.setText('{0:.2f}'.format(MeasurementsPercentual.MarginalReflexDistance1))
                self._tab2_results._MRD2_dev_p.setText('{0:.2f}'.format(MeasurementsPercentual.MarginalReflexDistance2))
                self._tab2_results._BH_dev_p.setText('{0:.2f}'.format(MeasurementsPercentual.BrowHeight))
                self._tab2_results._DS_dev_p.setText('{0:.2f}'.format(MeasurementsPercentual.DentalShow))
                self._tab2_results._PFH_dev_p.setText('{0:.2f}'.format(MeasurementsPercentual.PalpebralFissureHeight))
                
                
                self._tab2_results._tab_name=self._Patient.SecondPhoto._ID
                
                
                #compute the the different between both photos and fill the information 
                self._tab3_results  =  CustomTabResult()
                
                #filling tab3_results with the difference between the two photos
                self._tab3_results._CE_right.setText('{0:.2f}'.format(-MeasurementsRightFirst.CommissureExcursion+MeasurementsRightSecond.CommissureExcursion))
                self._tab3_results._SA_right.setText('{0:.2f}'.format(-MeasurementsRightFirst.SmileAngle+MeasurementsRightSecond.SmileAngle))
                self._tab3_results._DS_right.setText('{0:.2f}'.format(-MeasurementsRightFirst.DentalShow+MeasurementsRightSecond.DentalShow))
                self._tab3_results._MRD1_right.setText('{0:.2f}'.format(-MeasurementsRightFirst.MarginalReflexDistance1+MeasurementsRightSecond.MarginalReflexDistance1))
                self._tab3_results._MRD2_right.setText('{0:.2f}'.format(-MeasurementsRightFirst.MarginalReflexDistance2+MeasurementsRightSecond.MarginalReflexDistance2))
                self._tab3_results._BH_right.setText('{0:.2f}'.format(-MeasurementsRightFirst.BrowHeight+MeasurementsRightSecond.BrowHeight))
                self._tab3_results._PFH_right.setText('{0:.2f}'.format(-MeasurementsRightFirst.PalpebralFissureHeight+MeasurementsRightSecond.PalpebralFissureHeight))
                
                #filling the info for the left
                self._tab3_results._CE_left.setText('{0:.2f}'.format(-MeasurementsLeftFirst.CommissureExcursion+MeasurementsLeftSecond.CommissureExcursion))
                self._tab3_results._SA_left.setText('{0:.2f}'.format(-MeasurementsLeftFirst.SmileAngle+MeasurementsLeftSecond.SmileAngle))
                self._tab3_results._DS_left.setText('{0:.2f}'.format(-MeasurementsLeftFirst.DentalShow+MeasurementsLeftSecond.DentalShow))
                self._tab3_results._MRD1_left.setText('{0:.2f}'.format(-MeasurementsLeftFirst.MarginalReflexDistance1+MeasurementsLeftSecond.MarginalReflexDistance1))
                self._tab3_results._MRD2_left.setText('{0:.2f}'.format(-MeasurementsLeftFirst.MarginalReflexDistance2+MeasurementsLeftSecond.MarginalReflexDistance2))
                self._tab3_results._BH_left.setText('{0:.2f}'.format(-MeasurementsLeftFirst.BrowHeight+MeasurementsLeftSecond.BrowHeight))
                self._tab3_results._PFH_left.setText('{0:.2f}'.format(-MeasurementsLeftFirst.PalpebralFissureHeight+MeasurementsLeftSecond.PalpebralFissureHeight))
                
                
                #say to the window that presents the results that there are 3 tabs
                self._new_window = ShowResults(self._tab1_results, self._tab2_results, self._tab3_results)
                #show the window with the results
                self._new_window.show()
            
            
                   
        
    def match_iris(self):
        #make both iris have the same diameter as the bigger one
        if self.displayImage._lefteye is not None :
            if self.displayImage._lefteye[2] < self.displayImage._righteye[2]:
                self.displayImage._lefteye[2] = self.displayImage._righteye[2]
            elif self.displayImage._lefteye[2] > self.displayImage._righteye[2]:
                self.displayImage._righteye[2] = self.displayImage._lefteye[2]
            elif self.displayImage._lefteye[2] == self.displayImage._righteye[2]:
                pass
            
            self._toggle_lines = True 
            self.displayImage._points = None
            self.displayImage.set_update_photo()  
        
        
    def face_center(self):
        #find a line connecting the center of both iris and then fit a perperdicular
        #line in the middle
        if self.displayImage._shape is not None:
            
            if self._toggle_lines == True:
                self._toggle_lines = False
                points =  estimate_lines(self.displayImage._opencvimage, 
                                     self.displayImage._lefteye, 
                                     self.displayImage._righteye)
                self.displayImage._points = points
                self.displayImage.set_update_photo()
            else:
                self.displayImage._points = None
                self.displayImage.set_update_photo()
                self._toggle_lines = True    
            
            
    def load_file(self):
        
        #load a file using the widget
        name,_ = QtWidgets.QFileDialog.getOpenFileName(
                self,'Load Image',
                '',"Image files (*.png *.jpg *.jpeg *.tif *.tiff *.PNG *.JPG *.JPEG *.TIF *.TIFF)")
        
        if not name:
            pass
        else:
            #the user will load an single image so get rid of Patient and the
            # changephotoAction in the toolbar
            self._Patient = None
            self.changephotoAction.setEnabled(False)
            
            #if windows then transform / to \ (python stuffs)
            name = os.path.normpath(name)
            self._file_name = name
            #if the measurements window is open then close it
            if self._new_window is not None:
                self._new_window.close()
            #load image
            self.displayImage._opencvimage = cv2.imread(name)

            #if the photo was already processed then get the information for the
            #txt file, otherwise process the photo using the landmark ans pupil
            #localization algorithms 
            file_txt=name[:-4]
            file_txt = (file_txt + '.txt')
            if os.path.isfile(file_txt):
                shape,lefteye,righteye,boundingbox = get_info_from_txt(file_txt)
                self.displayImage._lefteye = lefteye
                self.displayImage._righteye = righteye 
                self.displayImage._shape = shape
                self.displayImage._boundingbox = boundingbox
                self.displayImage._points = None
                #change 3/7/2019
                self.displayImage._landmark_size = get_landmark_size(self.displayImage._shape)
                
                self.displayImage.update_view()

                self.setWindowTitle('Emotrics - '+self._file_name.split(os.path.sep)[-1])
            else:
               self.getShapefromImage()
                
    
    def getShapefromImage(self, update=False):
        
        #if the image is too large then it needs to be resized....
        h,w,d = self.displayImage._opencvimage.shape

        #if the image is too big then we need to resize it so that the landmark 
        #localization process can be performed in a reasonable time 
        self._Scale = 1  #start from a clear initial scale
        if h > 1500 or w > 1500 :
            if h >= w :
                h_n = 1500
                self._Scale = h/h_n
                w_n = int(np.round(w/self._Scale,0))
                #self.displayImage._opencvimage=cv2.resize(self.displayImage._opencvimage, (w_n, h_n), interpolation=cv2.INTER_AREA)
                temp_image = cv2.resize(self.displayImage._opencvimage, (w_n, h_n), interpolation=cv2.INTER_AREA)
                #self._image = image
            else :
                w_n = 1500
                self._Scale = w/w_n
                h_n = int(np.round(h/self._Scale,0))
                #self.displayImage._opencvimage=cv2.resize(self.displayImage._opencvimage, (w_n, h_n), interpolation=cv2.INTER_AREA)
                temp_image = cv2.resize(self.displayImage._opencvimage, (w_n, h_n), interpolation=cv2.INTER_AREA)
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
#                        cv2.imwrite(name,self.displayImage._opencvimage)
        else:
            #the image is of appropiate dimensions so no need for modification
            temp_image = self.displayImage._opencvimage.copy()
            #pass
        
        #get the landmarks using dlib, and the and the iris 
        #using Dougman's algorithm  
        #This is done in a separate thread to prevent the gui from 
        #freezing and crashing
        

        #create worker, pass the image to the worker
        #self.landmarks = GetLandmarks(self.displayImage._opencvimage)
        self.landmarks = GetLandmarks(temp_image, self._ModelName)
        #move worker to new thread
        self.landmarks.moveToThread(self.thread_landmarks)
        #start the new thread where the landmark processing will be performed
        self.thread_landmarks.start() 
        #Connect Thread started signal to Worker operational slot method
        self.thread_landmarks.started.connect(self.landmarks.getlandmarks)
        
        #connect signal emmited by landmarks to a function
        if update: #this is a model update, treat it like that    
            self.landmarks.landmarks.connect(self.ProcessShape_update)            
        else: #this is a new image, treat it like that  
            self.landmarks.landmarks.connect(self.ProcessShape)
                        
        #define the end of the thread
        self.landmarks.finished.connect(self.thread_landmarks.quit)

            
    def ProcessShape(self, shape, numFaces, lefteye, righteye, boundingbox):
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
            
            
            #update shape and bounding box always 
            self.displayImage._shape = shape
            self.displayImage._boundingbox = boundingbox
            self.displayImage._lefteye = lefteye
            self.displayImage._righteye = righteye
                
            #compute landmark size only if not avaliable
            #change 3/7/2019
            if self.displayImage._landmark_size is None:
                self.displayImage._landmark_size = get_landmark_size(self.displayImage._shape)
            
            #
            self.displayImage._points = None
        
            self.setWindowTitle('Emotrics - '+self._file_name.split(os.path.sep)[-1])
        elif numFaces == 0:
            #no face in image then shape is None
            self.displayImage._shape = None
            #inform the user
            QtWidgets.QMessageBox.warning(self,"Warning",
                    "No face in the image.\nIf the image does contain a face plase modify the brightness and try again.",
                        QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.NoButton)
        elif numFaces > 1:
            #multiple faces in image then shape is None
            self.displayImage._shape = None
            #inform the user
            QtWidgets.QMessageBox.warning(self,"Warning",
                    "Multiple faces in the image.\nPlease load an image with a single face.",
                        QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.NoButton)
          
        self.displayImage.update_view()
        
        
    #changed this on 3/9/19
    def ProcessShape_update(self, shape, numFaces, lefteye, righteye, boundingbox):
        #we know that there is a face, so we don't need to check if there are multiple faces 
           
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
                
                
        #just update the landmarks and bouding box
        self.displayImage._shape = shape
        self.displayImage._boundingbox = boundingbox
        self.displayImage.set_update_photo() 

           
    
    def load_iris(self):
        #load a file using the widget
        name,_ = QtWidgets.QFileDialog.getOpenFileName(
                self,'Load Iris Position and Diameter',
                '',"Image files (*.png *.jpg *.jpeg *.tif *.tiff *.PNG *.JPG *.JPEG *.TIF *.TIFF)")
        
        if not name:
            pass
        else:
            #if windows then transform / to \ (python stuffs)
            name = os.path.normpath(name)
            #if the measurements window is open then close it, the measures will be updated with the new eyes position
            if self._new_window is not None:
                self._new_window.close()

            #if the photo was already processed then get the information for the
            #txt file, otherwise process the photo using the landmark ans pupil
            #localization algorithms 
            file_txt=name[:-4]
            file_txt = (file_txt + '.txt')
            if os.path.isfile(file_txt):
                shape,lefteye,righteye,_ = get_info_from_txt(file_txt)
                
                dx_left = lefteye[0]-shape[27,0]
                dy_left = shape[27,1]-lefteye[1]
                
                dx_right = shape[27,0]-righteye[0]
                dy_right = shape[27,1]-righteye[1]
                
                self.displayImage._lefteye = [self.displayImage._shape[27,0]+dx_left, self.displayImage._shape[27,1]-dy_left,lefteye[2]]
                self.displayImage._righteye = [self.displayImage._shape[27,0]-dx_right, self.displayImage._shape[27,1]-dy_right,lefteye[2]]
                self.displayImage.set_update_photo()
                
            else:
                QtWidgets.QMessageBox.warning(self,"Warning",
                    "Iris information for this photograph is not avaliable",
                        QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.NoButton)
                
#                self.displayImage._lefteye = lefteye
#                self.displayImage._righteye = righteye 
#                self.displayImage.set_update_photo()
            
        
            
    def toggle_landmarks(self):
        #Hide - show the landmarks 
        if self._toggle_landmaks is True:
            self._toggle_landmaks = False
            self.displayImage.set_update_photo(self._toggle_landmaks)
        elif self._toggle_landmaks is False:
            self._toggle_landmaks = True
            self.displayImage.set_update_photo(self._toggle_landmaks)
                        
            
    def save_snapshot(self):
        #save the current view 
        if self.displayImage._opencvimage is not None:
            proposed_name = self._file_name[:-4]+'-landmarks'
            name,_ = QtWidgets.QFileDialog.getSaveFileName(self, 'Save File',proposed_name, 'png (*.png);;jpg (*.jpg);; jpeg (*.jpeg)')
            if not name:
                pass
            else:
                #if shape then add shape to image
                temp_image  = self.displayImage._opencvimage.copy()
    
                #draw 68 landmark points       
                if self.displayImage._shape is not None:
                   temp_image = mark_picture(temp_image, self.displayImage._shape, self.displayImage._lefteye, self.displayImage._righteye, self.displayImage._points, self.displayImage._landmark_size)
                   
                save_snaptshot_to_file(temp_image,name)

    def save_results(self):
        #save the results in a txt and xls files. There are two modes, one if 
        #there is no patient and another is the is a patient (two photos)
        if self._Patient is None: #this implies that there is a single photo
            if self._file_name is not None:
                if self.displayImage._shape is not None:
                    save_txt_file(self._file_name, self.displayImage._shape, self.displayImage._lefteye, self.displayImage._righteye, self.displayImage._boundingbox)
                    MeasurementsLeft, MeasurementsRight, MeasurementsDeviation, MeasurementsPercentual = get_measurements_from_data(self.displayImage._shape, self.displayImage._lefteye, self.displayImage._righteye, self._CalibrationType, self._CalibrationValue)
#                    save_xls_file(self._file_name, MeasurementsLeft, MeasurementsRight, MeasurementsDeviation, MeasurementsPercentual)
#                    
                    temp = SaveWindow(self, self._file_name, MeasurementsLeft, MeasurementsRight, MeasurementsDeviation, MeasurementsPercentual)
                    temp.exec_()
        else:#this implies that the user created a patient and wants to analize two photos
            #get the current info from screen and update the memory
            if self._file_name == self._Patient.FirstPhoto._file_name:
                #the first photo is on memory and we wnat to move to the second photo.
                
                #first update the information from the screen to the memory on the
                #first photo
                self._Patient.FirstPhoto._lefteye = self.displayImage._lefteye
                self._Patient.FirstPhoto._righteye = self.displayImage._righteye
                self._Patient.FirstPhoto._shape =  self.displayImage._shape
                self._Patient.FirstPhoto._points = self.displayImage._points
                
            
            elif self._file_name == self._Patient.SecondPhoto._file_name:
                #the second photo is on memory and we wnat to move to the first photo
                #first update the information from the screen to the memory on the
                #second photo
                self._Patient.SecondPhoto._lefteye = self.displayImage._lefteye
                self._Patient.SecondPhoto._righteye = self.displayImage._righteye
                self._Patient.SecondPhoto._shape =  self.displayImage._shape
                self._Patient.SecondPhoto._points = self.displayImage._points

        
            #now save results 
            save_txt_file(self._Patient.FirstPhoto._file_name, self._Patient.FirstPhoto._shape, self._Patient.FirstPhoto._lefteye, self._Patient.FirstPhoto._righteye,  self._Patient.FirstPhoto._boundingbox)    
            save_txt_file(self._Patient.SecondPhoto._file_name, self._Patient.SecondPhoto._shape, self._Patient.SecondPhoto._lefteye, self._Patient.SecondPhoto._righteye, self._Patient.SecondPhoto._boundingbox)
            save_xls_file_patient(self._file_name,self._Patient, self._CalibrationType, self._CalibrationValue)

            
    
    def settings(self):
        #this new window allows the user to:
            #1) modify the calibration parameter used to compute all the real-life measurements 
            #2) Select the model used for landmakr estimation
        #we send the current values to the window so that the values can be preserved when a new photo is loaded
        Settings = ShowSettings(self, self._ModelName, self._CalibrationType, self._CalibrationValue, size_landmarks = self.displayImage._landmark_size, shape = self.displayImage._shape)
        Settings.exec_()
        
        if Settings.isCanceled:  #the person just clickes cancel, don't do anything
            pass
        else:        
            #get values from the window and update appropiate parameters 
            if Settings.tab1._checkBox1.isChecked() == True:
                self._CalibrationType = 'Iris'
                self._CalibrationValue = float(Settings.tab1._IrisDiameter_Edit.text())
            elif Settings.tab1._checkBox2.isChecked() == True:
                self._CalibrationType = 'Manual'
                self._CalibrationValue = float(Settings.tab1._Personalized_Edit.text())
             
                
            #these options requiere a possible re-calculation of landmarks and re-draw 
            
            #check if the user decided to change the model
            old_modelName = self._ModelName
            is_model_changed = False
            if Settings.tab2._checkBox2.isChecked() == True:
                self._ModelName = 'iBUG'
            elif Settings.tab2._checkBox1.isChecked() == True:
                self._ModelName = 'MEE'
            elif Settings.tab2._checkBox2.isChecked() == False and Settings.tab2._checkBox1.isChecked() == False:
                self._ModelName = Settings.tab2._ModelName
                
            if old_modelName == self._ModelName  :
                pass
            else:
                is_model_changed = True
                
            #print(self._ModelName)
                
               
            #check if the user decided to change the landmark size
            user_size_landmark = Settings.tab3._Landmark_Size_Edit.text()
            old_size_landmark = self.displayImage._landmark_size
            is_landmark_changed = False
            if user_size_landmark is "":
                size_landmarks = old_size_landmark
            elif int(user_size_landmark) ==  0: #used entered zero, just ignore it 
                size_landmarks = old_size_landmark
            else:
                size_landmarks = int(user_size_landmark)
                
            if size_landmarks == old_size_landmark:
                pass
            else:
                is_landmark_changed = True
                #update landmark size information 
                self.displayImage._landmark_size = size_landmarks
            
    
            
            #if model is the same and landmark changed the just re-draw landmarks
            if is_landmark_changed == True and is_model_changed == False:            
                self.displayImage.set_update_photo()
                
            #if the model changed, re-compute landmark localization and re-draw 
            if is_model_changed == True:
                
                if self.displayImage._shape is not None: #there is an image already there
                    #used changed the model, so we need to re-calculate the landmarks for the photos
                    if self._Patient is None: #there is only one image so just recalculate everything for that image. 
                        self.getShapefromImage(update=True)
                    else: #there is a patient in memory (two images), so we need to work on both images.
                        
                        #this can be improve to remove some unnecesary steps... If someone reads this, please work on it.
                        
                        #Here is the plan: we will take each image and will create a new qthread to process each image at the time 
                        #will then pass the info into a new function that will take care of updating that particular image
                        #finally, will update the current view
                        
                        self.UpdateFirstPhoto_Patient()
                        

                    
    def UpdateFirstPhoto_Patient(self):
        
        h,w,d = self._Patient.FirstPhoto._photo.shape

        #if the image is too big then we need to resize it so that the landmark 
        #localization process can be performed in a reasonable time 
        self._Scale = 1  #start from a clear initial scale
        if h > 1500 or w > 1500 :
            if h >= w :
                h_n = 1500
                self._Scale = h/h_n
                w_n = int(np.round(w/self._Scale,0))
                temp_image = cv2.resize(self._Patient.FirstPhoto._photo, (w_n, h_n), interpolation=cv2.INTER_AREA)
            else :
                w_n = 1500
                self._Scale = w/w_n
                h_n = int(np.round(h/self._Scale,0))
                temp_image = cv2.resize(self._Patient.FirstPhoto._photo, (w_n, h_n), interpolation=cv2.INTER_AREA)
         
        else:
            temp_image = self._Patient.FirstPhoto._photo.copy()
            
        
        self.landmarksFirstPhoto = GetLandmarks(temp_image, self._ModelName)
        self.landmarksFirstPhoto.moveToThread(self.threadFirstPhoto)
        self.threadFirstPhoto.start()
        self.threadFirstPhoto.started.connect(self.landmarksFirstPhoto.getlandmarks)
        self.landmarksFirstPhoto.landmarks.connect(self.ProcessShape_UpdateFirstPhoto)
        
        self.landmarksFirstPhoto.finished.connect(self.threadFirstPhoto.quit)
        
    def ProcessShape_UpdateFirstPhoto(self, shape, numFaces, lefteye, righteye, boundingbox):
        #this function takes care of updating the FirstPhoto from patient
        
        #we know that there is a face, so we don't need to check if there are multiple faces 
           
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
                
                
        #just update the landmarks and bouding box
        self._Patient.FirstPhoto._shape = shape
        self._Patient.FirstPhoto._boundingbox = boundingbox
        
        
        #verify if the FirstPhoto is currently on screen 
        if self._file_name == self._Patient.FirstPhoto._file_name:
            #the update the view
            self.displayImage._shape = shape
            self.displayImage._boundingbox = boundingbox
            self.displayImage.set_update_photo() 
            
            
        #first photo done, now do secondphoto
        self.UpdateSecondPhoto_Patient()
        
    def UpdateSecondPhoto_Patient(self):
        
        h,w,d = self._Patient.SecondPhoto._photo.shape

        #if the image is too big then we need to resize it so that the landmark 
        #localization process can be performed in a reasonable time 
        self._Scale = 1  #start from a clear initial scale
        if h > 1500 or w > 1500 :
            if h >= w :
                h_n = 1500
                self._Scale = h/h_n
                w_n = int(np.round(w/self._Scale,0))
                temp_image = cv2.resize(self._Patient.SecondPhoto._photo, (w_n, h_n), interpolation=cv2.INTER_AREA)
            else :
                w_n = 1500
                self._Scale = w/w_n
                h_n = int(np.round(h/self._Scale,0))
                temp_image = cv2.resize(self._Patient.SecondPhoto._photo, (w_n, h_n), interpolation=cv2.INTER_AREA)
         
        else:
            temp_image = self._Patient.SecondPhoto._photo.copy()
            
        
        self.landmarksSecondPhoto = GetLandmarks(temp_image, self._ModelName)
        
        self.landmarksSecondPhoto.moveToThread(self.threadSecondPhoto)
        self.threadSecondPhoto.start()
        self.threadSecondPhoto.started.connect(self.landmarksSecondPhoto.getlandmarks)
        self.landmarksSecondPhoto.landmarks.connect(self.ProcessShape_UpdateSecondPhoto)
        
        self.landmarksSecondPhoto.finished.connect(self.threadSecondPhoto.quit)
        
    def ProcessShape_UpdateSecondPhoto(self, shape, numFaces, lefteye, righteye, boundingbox):
        #this function takes care of updating the SecondPhoto from patient
        
        #we know that there is a face, so we don't need to check if there are multiple faces 
           
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
                
                
        #just update the landmarks and bouding box

        self._Patient.SecondPhoto._shape = shape
        self._Patient.SecondPhoto._boundingbox = boundingbox
        
        
        #verify if the FirstPhoto is currently on screen 
        if self._file_name == self._Patient.SecondPhoto._file_name:
            #the update the view
            self.displayImage._shape = shape
            self.displayImage._boundingbox = boundingbox
            self.displayImage.set_update_photo()             
           
            
    def about_app(self):
        
        #show a window with some information
        QtWidgets.QMessageBox.information(self, 'Emotrics', 
                            'Emotrics is a tool for estimation of objective facial measurements, it uses machine learning to automatically localize facial landmarks in photographs. Its objective is to reduce subjectivity in the evaluation of facial palsy.\n\nEmotrics was developed by: Diego L. Guarin, PhD. at the Facial Nerve Centre, Massachusetts Eye and Ear Infirmary; part of Harvard Medical School.\n\nA tutorial can be found by searching for Emotrics on YouTube.\n\nThis is an open source software provided with absolutely no guarantees. You can run, study, share and modify the software. It is distributed under the GNU General Public License.\n\nThis software was written in Python, source code and additional information can be found in github.com/dguari1/Emotrics ', 
                            QtWidgets.QMessageBox.Ok)     
            
    def close_app(self):  
        
        #ask is the user really wants to close the app
        choice = QtWidgets.QMessageBox.question(self, 'Message', 
                            'Do you want to exit?', QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)

        if choice == QtWidgets.QMessageBox.Yes :
            self.close()
            app.exec_()
        else:
            pass  
        
    def closeEvent(self, event):
        #we need to close all the windows before closing the program  
        if self._new_window is not None:
            self._new_window.close()
        event.accept()
        

if __name__ == '__main__':
    
    if not QtWidgets.QApplication.instance():
        app = QtWidgets.QApplication(sys.argv)
    else:
        app = QtWidgets.QApplication.instance()
    
    app.setStyle(QtWidgets.QStyleFactory.create('Cleanlooks'))
        
    GUI = window()
    
    #GUI.show()
    app.exec_()
    
