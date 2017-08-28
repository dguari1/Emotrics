# -*- coding: utf-8 -*-
"""
Created on Sun Aug 27 18:17:25 2017

@author: diego
"""

from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot


from dlib import get_frontal_face_detector
from dlib import shape_predictor
from dlib import rectangle

import cv2
import os
import numpy as np

class GetLandmarks(QObject):
    
    finished = pyqtSignal()
    shape = pyqtSignal(object)
    
    def __init__(self, image):
        super(GetLandmarks, self).__init__()
        self._image = image
        
    
    @pyqtSlot()
    def getlandmarks(self):
        #function to automatically localize the landmarks in the a face image using 
        #dlib algorithm 
        detector = get_frontal_face_detector()
        scriptDir = os.path.dirname(os.path.realpath(__file__))
        predictor = shape_predictor(scriptDir + os.path.sep + 'include' +os.path.sep +'data'+ os.path.sep + 'shape_predictor_68_face_landmarks.dat')
        #make a local copy of the image
        image = self._image.copy 
        #transform to gray 
        gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        
        #resize to speed up face dectection
        height, width = gray.shape[:2]  
        newWidth=200
        ScalingFactor=width/newWidth
        newHeight=int(height/ScalingFactor)
        smallImage=cv2.resize(gray, (newWidth, newHeight), interpolation=cv2.INTER_AREA)

        #detect face in image using dlib.get_frontal_face_detector()
        rects = detector(smallImage,1)
        if len(rects) == 1:   
            #now we have only one face in the image
            #function to obtain facial landmarks using dlib 
            #given an image and a face
            #rectangle
            for (i, rect) in enumerate(rects):
                # determine the facial landmarks for the face region, then
                # convert the facial landmark (x, y)-coordinates to a NumPy array
    
                #adjust face position using the scaling factor
                mod_rect=rectangle(
                        left=int(rect.left() * ScalingFactor), 
                        top=int(rect.top() * ScalingFactor), 
                        right=int(rect.right() * ScalingFactor), 
                        bottom=int(rect.bottom() * ScalingFactor))
       
                #predict facial landmarks 
                shape_dlib = predictor(image, mod_rect)   
            
                #transform shape object to np.matrix type
                shape = shape_to_np(shape)
                
        else:
            shape = None