# -*- coding: utf-8 -*-
"""
Created on Wed Aug 16 10:53:19 2017

@author: Diego L.Guarin -- diego_guarin at meei.harvard.edu
"""
import cv2
import numpy as np
from scipy.spatial.distance import cdist

from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore


from utilities import mark_picture  #this function draws the landmarks and iris circles 
from process_eye import get_iris_manual #this function opens a new window to manually select the iris


"""
This class is in charge of drawing the picture and the landmarks in the main 
window, it also takes care of lifting and re-location of landmarks. 
"""

class ImageViewer(QtWidgets.QGraphicsView):       
    
    def __init__(self):
        #usual parameters to make sure the image can be zoom-in and out and is 
        #possible to move around the zoomed-in view
        super(ImageViewer, self).__init__()
        self._zoom = 0
        self._scene = QtWidgets.QGraphicsScene(self)
        self._photo = QtWidgets.QGraphicsPixmapItem()
        self._scene.addItem(self._photo)
        self.setScene(self._scene)
        self.setTransformationAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setBackgroundBrush(QtGui.QBrush(QtGui.QColor(100,100,100)))
        self.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.setDragMode(QtWidgets.QGraphicsView.RubberBandDrag)
        
        #this is used to show the dots and update the dots in image
        self._shape = None
        self._lefteye = None
        self._righteye = None
        self._opencvimage = None
        self._boundingbox = None
        self._PointToModify = None
        self._points = None
        
        
        #this variable is used to verify is a landmark will be relocated
        self._IsPointLifted = False

        #QtWidgets.QGraphicsView.RubberBandDrag
        
    def setPhoto(self, pixmap = None):
        #this function puts an image in the scece (if pixmap is not None), it
        #sets the zoom to zero 
        self._zoom = 0        
        if pixmap and not pixmap.isNull():
            self.setDragMode(QtWidgets.QGraphicsView.RubberBandDrag)
            self._photo.setPixmap(pixmap)
            self.fitInView()
        else:
            self.setDragMode(QtWidgets.QGraphicsView.NoDrag)
            self._photo.setPixmap(QtGui.QPixmap())

    def fitInView(self):
        #this function takes care of accomodating the view so that it can fit
        #in the scene, it resets the zoom to 0 (i think is a overkill, i took
        #it from somewhere else)
        rect = QtCore.QRectF(self._photo.pixmap().rect())
        #self.setSceneRect(rect)
        if not rect.isNull():
            unity = self.transform().mapRect(QtCore.QRectF(0, 0, 1, 1))
            self.scale(1 / unity.width(), 1 / unity.height())        
            viewrect = self.viewport().rect()
            scenerect = self.transform().mapRect(rect)
            factor = min(viewrect.width() / scenerect.width(),
                     viewrect.height() / scenerect.height())               
            self.scale(factor, factor)
            self.centerOn(rect.center())
            self._zoom = 0 
                        
            
    def zoomFactor(self):
        return self._zoom
    
    def wheelEvent(self, event):
        #this take care of the zoom, it modifies the zoom factor if the mouse 
        #wheel is moved forward or backward by 20%
        if not self._photo.pixmap().isNull():
            move=(event.angleDelta().y()/120)
            if move > 0:
                factor = 1.2
                self._zoom += 1
            else:
                factor = 0.8
                self._zoom -= 1
                                        
            if self._zoom > 0:
                self.scale(factor, factor)
            elif self._zoom <= 0:
                self._zoom = 0
                self.fitInView()
                
    def mousePressEvent(self, event):
        #this function takes care of lifting (if RightClick) and relocating (if
        #a point is lifted and LeftClick) landmarks. It also verifies if the 
        #user wants to manually modify the position of the iris. In that case,
        #it opens up a new window showing only the eye (left or right) where 
        #the user can select four points around the iris
        if not self._photo.pixmap().isNull():
            scenePos = self.mapToScene(event.pos())
            if event.button() == QtCore.Qt.RightButton:
                #if the user RightClick and no point is lifted then verify if 
                #the position of the click is close to one of the landmarks
                if self._IsPointLifted == False:
                    if self._shape is not None:
    
                        x_mousePos = scenePos.toPoint().x()
                        y_mousePos = scenePos.toPoint().y()
                        mousePos=np.array([(x_mousePos, y_mousePos)])                   
                        distance=cdist(np.append(self._shape,
                                        [[self._righteye[0],self._righteye[1]],
                                        [self._lefteye[0],self._lefteye[1]]], axis=0)
                                        , mousePos)
                        distance=distance[:,0]
                        #check is a landmark (including the eyes) is no more than 
                        #3 pixels away from the click. If there is then lift that
                        #landmark from the face                        
                        PointToModify = [i for i, j in enumerate(distance) if j <=3 ]
                        if PointToModify:
                            self._PointToModify = PointToModify[0]
                            if self._PointToModify >= 68:
                                if self._PointToModify == 69:
                                    #if click is in left eye then open up the 
                                    #eye window showing the left eye only 
                                    position = 'left'
                                    temp = get_iris_manual(self._opencvimage, self._shape, position)
                                    if temp is not None:
                                        self._lefteye = temp
                                elif self._PointToModify == 68:
                                    #if click is in right eye then open up the 
                                    #eye window showing the right eye only                                     
                                    position = 'right'
                                    temp = get_iris_manual(self._opencvimage, self._shape, position)
                                    if temp is not None:
                                        self._righteye = temp
                            else:                            
                                self._shape[self._PointToModify] = [-1,-1]
                                self._IsPointLifted = True
                            self.set_update_photo()
            elif event.button() == QtCore.Qt.LeftButton:
                #if the user LeftClick and there is a landmark lifted, then 
                #reposition the landmar in the position of the click 
                self.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)
                if self._IsPointLifted:
                    x_mousePos = scenePos.toPoint().x()
                    y_mousePos = scenePos.toPoint().y()
                    mousePos=np.array([(x_mousePos, y_mousePos)])
                    self._shape[self._PointToModify] = [x_mousePos, y_mousePos]
                    self._IsPointLifted = False
                    self._PointToModify = None
                    self.set_update_photo()

             
            QtWidgets.QGraphicsView.mousePressEvent(self, event)
     

    def set_update_photo(self, toggle=True):
        #this function takes care of updating the view without re-setting the 
        #zoom. Is usefull for when you lift or relocate landmarks or when 
        #drawing lines in the middle of the face
        self._scene.removeItem(self._photo)

        temp_image  = self._opencvimage.copy()   
        
        if toggle: #verify if the user wants to remove the landmarks..
            #if shape then draw 68 landmark points
            if self._shape is not None:
                #mark_picture takes care of drawing the landmarks and the circles
                #in the iris using opencv 
                temp_image = mark_picture(temp_image, self._shape, self._lefteye, self._righteye, self._points)
            
        image = cv2.cvtColor(temp_image,cv2.COLOR_BGR2RGB)
        height, width, channel = image.shape
        bytesPerLine = 3 * width
        img_Qt = QtGui.QImage(image.data, width, height, bytesPerLine, QtGui.QImage.Format_RGB888)
        img_show = QtGui.QPixmap.fromImage(img_Qt)
        
        self._photo.setPixmap(img_show)    
        self._scene.addItem(self._photo)
        self.setDragMode(QtWidgets.QGraphicsView.RubberBandDrag)

        
    def show_entire_image(self):
        #this is a little utility to reset the zoom with a single click
        self.fitInView()
        
        
    def resizeEvent(self, event):
        #this function assure that when the main window is resized the image 
        #is also resized preserving the h/w ratio
        self.fitInView()
        
            
            
    def update_view(self):
        #this function takes care of updating the view by re-setting the zoom.
        #is usefull to place the image in the scene for the first time
        
        
        #if shape then add shape to image
        temp_image  = self._opencvimage.copy()
        
    
        #draw 68 landmark points       
        if self._shape is not None:
           temp_image = mark_picture(temp_image, self._shape, self._lefteye, self._righteye, self._points)

        image = cv2.cvtColor(temp_image,cv2.COLOR_BGR2RGB)
        height, width, channel = image.shape
        bytesPerLine = 3 * width
        img_Qt = QtGui.QImage(image.data, width, height, bytesPerLine, QtGui.QImage.Format_RGB888)
        img_show = QtGui.QPixmap.fromImage(img_Qt)
        
        #show the photo
        self.setPhoto(img_show)
        
        
           
        
        
        

        
            
