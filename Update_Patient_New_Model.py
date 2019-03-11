# -*- coding: utf-8 -*-
"""
Created on Fri Mar  8 16:15:59 2019

@author: GUARIND
"""

import cv2
import numpy as np
from ProcessLandmarks import GetLandmarks

from PyQt5 import QtCore
from PyQt5.QtWidgets import QDialog

class UpdatePatientNewModel(QDialog):
    
    def __init__(self, Image=None, ModelName=None):
            
        self._Photo = None
        self._ModelName = None
        self._shape = None
        self._boundingbox = None
        
        self.thread_landmarks_new = QtCore.QThread()  # no parent!

        
        
    def ComputeLandmarks(self, Image=None, ModelName=None):
        
        self._Photo = Image
        self._ModelName = ModelName
        
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
                
        else:
            temp_image = self._Photo.copy()
            #pass

        print('hi')
        print(temp_image.shape)
        #create worker, pass the image to the worker
        ##self.landmarks = GetLandmarks(self._Photo)
        self.landmarks = GetLandmarks(temp_image, self._ModelName)
        print('1')
        #move worker to new thread
        self.landmarks.moveToThread(self.thread_landmarks_new)
        print('2')
        #start the new thread where the landmark processing will be performed
        self.thread_landmarks_new.start() 
        print('3')
        #Connect Thread started signal to Worker operational slot method
        self.thread_landmarks_new.started.connect(self.landmarks.getlandmarks)
        print('4')
        #connect signal emmited by landmarks to a function
        self.landmarks.landmarks.connect(self.ProcessShape)
        print('5')
        #define the end of the thread
        self.landmarks.finished.connect(self.thread_landmarks_new.quit) 
        print('6')
        print(self._shape)
        
    
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
            
            self._shape = shape
            self._boundingbox = boundingbox
                        
        else:
                
            self._shape = None
            self._boundingbox = None
        