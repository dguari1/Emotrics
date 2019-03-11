# -*- coding: utf-8 -*-
"""
Created on Sun Aug 27 18:17:25 2017

@author: Diego L.Guarin -- diego_guarin at meei.harvard.edu
"""

from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from PyQt5 import QtWidgets, QtGui

from dlib import get_frontal_face_detector
from dlib import shape_predictor
from dlib import rectangle

import cv2
import os
import numpy as np
import sys

class GetLandmarks(QObject):
    
    finished = pyqtSignal()
    landmarks = pyqtSignal(object, int, object, object, object)
    
    def __init__(self, image, ModelName):
        super(GetLandmarks, self).__init__()
        self._image = image
        self._ModelName  = ModelName
        self._shape = np.zeros((68,2),dtype=int)
        self._lefteye = [-1,-1,-1]
        self._righteye = [-1,-1,-1]
        self._boundingbox = [-1,-1,-1,-1]
        
    
    @pyqtSlot()
    def getlandmarks(self):
        #function to automatically localize the landmarks in the a face image using 
        #dlib algorithm 
        detector = get_frontal_face_detector()
        if os.name is 'posix': #is a mac or linux
            scriptDir = os.path.dirname(sys.argv[0])
        else: #is a  windows 
            scriptDir = os.getcwd()
        if self._ModelName == 'iBUG':  #user wants to use iBUGS model
            predictor = shape_predictor(scriptDir + os.path.sep + 'include' +os.path.sep +'data'+ os.path.sep + 'shape_predictor_68_face_landmarks.dat')
        elif self._ModelName == 'MEE':  #user wants to use MEE model
            predictor = shape_predictor(scriptDir + os.path.sep + 'include' +os.path.sep +'data'+ os.path.sep + 'mee_shape_predictor_68_face_landmarks.dat')
        else: #user wants to use own model        
            predictor = shape_predictor(os.path.normpath(self._ModelName))
            

        #make a local copy of the image
        image = self._image.copy()
        height, width, d = image.shape                        
        if d > 1:
            #transform to gray 
            gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        #resize to speed up face dectection
        #height, width = gray.shape[:2]  
        newWidth=200
        ScalingFactor=width/newWidth
        newHeight=int(height/ScalingFactor)
        smallImage=cv2.resize(gray, (newWidth, newHeight), interpolation=cv2.INTER_AREA)

        #detect face in image using dlib.get_frontal_face_detector()
        rects = detector(smallImage,1)
        
        if len(rects) == 0 : #if no face detected then try again with the full size image
                rects = detector(gray,1)            
        
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
                #shape_dlib = predictor(gray, rect) 
                #transform shape object to np.matrix type
                for k in range(0,68):
                    self._shape[k] = (shape_dlib.part(k).x, shape_dlib.part(k).y)
                    if self._shape[k,0]<= 0 : self._shape[k,0] = 1
                    if self._shape[k,1]<= 0 : self._shape[k,1] = 1
            
                #position of the face in the image
                self._boundingbox=[int(rect.left() * ScalingFactor), 
                                   int(rect.top() * ScalingFactor),
                                   int(rect.right() * ScalingFactor) - int(rect.left() * ScalingFactor),
                                   int(rect.bottom() * ScalingFactor) - int(rect.top() * ScalingFactor)]
            
            #the landmarks where properly estimated, now find the iris
            #the function get_iris will update the variables _lefteye and _righteye
            self.get_iris()
            
            #it finished processing the face, now emit the results
            self.landmarks.emit(self._shape, len(rects), self._lefteye, self._righteye, self._boundingbox)
            
            #now inform that is over
            self.finished.emit()
            
        else: #not face or multiple faces 
            
            #emit an empty array 
            self.landmarks.emit(self._shape, len(rects), self._lefteye, self._righteye, self._boundingbox)
            
            #now inform that is over
            self.finished.emit()
            
            
    def get_iris(self):
        #function that selects the eye from a face image and uses -get_pupil- to 
        #localize the iris. 


        #Left Eye
        x_left = self._shape[42,0]
        w_left = (self._shape[45,0]-x_left)
        y_left = min(self._shape[43,1],self._shape[44,1])
        h_left = (max(self._shape[46,1],self._shape[47,1])-y_left)
        Eye = self._image.copy()
        Eye = Eye[(y_left-5):(y_left+h_left+5),(x_left-5):(x_left+w_left+5)]
        
        selected_circle_left = self.process_eye(Eye)
        selected_circle_left[0]=int(selected_circle_left[0])+x_left-5
        selected_circle_left[1]=int(selected_circle_left[1])+y_left-5
        selected_circle_left[2]=int(selected_circle_left[2])
        
        self._lefteye = selected_circle_left
        
        #Right Eye    
        x_right = self._shape[36,0]
        w_right = (self._shape[39,0]-x_right)
        y_right = min(self._shape[37,1],self._shape[38,1])
        h_right = (max(self._shape[41,1],self._shape[40,1])-y_right)
        Eye = self._image.copy()
        Eye = Eye[(y_right-5):(y_right+h_right+5),(x_right-5):(x_right+w_right+5)]
        
        selected_circle_right = self.process_eye(Eye)
        selected_circle_right[0]=int(selected_circle_right[0])+x_right-5
        selected_circle_right[1]=int(selected_circle_right[1])+y_right-5
        selected_circle_right[2]=int(selected_circle_right[2])
            
        self._righteye = selected_circle_right
            
    def process_eye(self, InputImage):
        #this function appplies a modified Daugman procedure for iris detection.
        #See 'How Iris Recognition Works, Jhon Dougman - IEEE Transactions on 
        #circuits and systems for video technology, January 2004'
        
        #get dimension of image 
        h_eye, w_eye, d_eye = InputImage.shape
        
        #this is the variable that will be return after processing
        circle=[]
        
        #verify that it is a color image
        if d_eye < 3:
            print('Pupil cannot be detected -- Color image is required')
            #circle=[int(w_eye/2), int(h_eye/2), int(w_eye/4)]
            circle=[-1,-1,-1]
            return circle
            
        #verify that the eye is open  
        #print(w_eye/h_eye)
        if w_eye/h_eye > 3.2:
            print('Pupil cannot be detected -- Eye is closed')
            circle=[int(w_eye/2), int(h_eye/2), int(w_eye/4)]
            return circle
        
        #reduce brightness to help with light-colored eyes
        InputImage=np.array(InputImage*0.75+0, dtype=InputImage.dtype)
        
        #split image into its different color channels 
        b,g,r = cv2.split(InputImage)
        
        #and create a new gray-image combining the blue and green channels, this 
        #will help to differentiate between the iris and sclera 
        #the function cv2.add guarantees that the resulting image has values 
        #between 0 (white) and 255 (black)
        bg = cv2.add(b,g)
        #filter the image to smooth the borders
        bg = cv2.GaussianBlur(bg,(3,3),0)
        
        #we assume that the radii of the iris is between 1/5.5 and 1/3.5 times the eye 
        #width (this value was obtained after measuring multiple eye images, it only
        #works if the eye section was obtained via dlib)
        Rmin=int(w_eye/5.5)
        Rmax=int(w_eye/3.5)
        radius=range(Rmin,Rmax+1)
        
        result_value=np.zeros(bg.shape, dtype=float)
        result_index_ratio=np.zeros(bg.shape, dtype=bg.dtype)
        mask = np.zeros(bg.shape, dtype=bg.dtype)
        
        #apply the Dougnman's procedure for iris detection. In this case I modify the 
        #procedure instead of use a full circunference it only uses 1/5 of 
        #a circunference. The procedure uses a circle between -35deg-0deg and 
        #180deg-215deg if the center beeing analized is located in the top half of the 
        #eye image, and a circle between 0deg-35deg and 145deg-180deg if the center 
        #beeing analized is located in the bottom half of the eye image
        
        possible_x=range(Rmin,w_eye-Rmin)
        possible_y=range(0,h_eye)
        for x in possible_x:
            for y in possible_y:  
                          
                intensity=[]
                for r in radius:
                    
                    if y>=int(h_eye/2):
                        temp_mask=mask.copy()   
                        #cv2.circle(temp_mask,(x,y),r,(255,255,255),1)
                        cv2.ellipse(temp_mask, (x,y), (r,r), 0, -35, 0, (255,255,255),1)
                        cv2.ellipse(temp_mask, (x,y), (r,r), 0, 180, 215, (255,255,255),1)
                        processed = cv2.bitwise_and(bg,temp_mask)
                        intensity.append(cv2.sumElems(processed)[0]/(2*3.141516*r))
                    
                    else:
                        temp_mask=mask.copy()   
                        #cv2.circle(temp_mask,(x,y),r,(255,255,255),1)
                        cv2.ellipse(temp_mask, (x,y), (r,r), 0, 0, 35, (255,255,255),1)
                        cv2.ellipse(temp_mask, (x,y), (r,r), 0, 145, 180, (255,255,255),1)
                        processed = cv2.bitwise_and(bg,temp_mask)
                        intensity.append(cv2.sumElems(processed)[0]/(2*3.141516*r))                
        
        
                diff_vector=np.diff(intensity)
                max_value=max(diff_vector)
                max_index = [i for i, j in enumerate(diff_vector) if j == max_value]   
                result_value[y,x]=max_value
                result_index_ratio[y,x]=max_index[0]
            
        
        
        #the results are filtered by a Gaussian filter, as suggested by Daugman
        result_value=cv2.GaussianBlur(result_value,(7,7),0)
        
        
        
        #now we need to find the center and radii that show the largest change in 
        #intensity    
        matrix = result_value
        needle = np.max(matrix)
        
        matrix_dim = w_eye
        item_index = 0
        for row in matrix:
            for i in row:
                if i == needle:
                    break
                item_index += 1
            if i == needle:
                break
        
        #this is the center and radius of the selected circle
        c_y_det=int(item_index / matrix_dim) 
        c_x_det=item_index % matrix_dim
        r_det=radius[result_index_ratio[c_y_det,c_x_det]]
        
        circle=[c_x_det,c_y_det,r_det]   
        
        return circle 