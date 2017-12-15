# -*- coding: utf-8 -*-
"""
Created on Wed Aug 23 21:10:25 2017

@author: Diego L.Guarin -- diego_guarin at meei.harvard.edu
"""
from PyQt5 import QtWidgets, QtCore, QtGui
import numpy as np
from utilities import find_circle_from_points

"""
This window show the eye and allows the user to select 4 points around the iris, 
it then fits a circle around these points. The user can accept the circle or 
re-initialize the point selection
"""


class ProcessEye(QtWidgets.QDialog):
    
    def __init__(self, image = None):
        super(ProcessEye, self).__init__()
        self.setWindowTitle('Eye Selection')
        self._circle = None
        self._image = image
        self.label_title = QtWidgets.QLabel()
        self.label_title.setText('Please click on four points around the iris')
        #self.label_title.setWordWrap(True) 
        self.label_title.setMaximumWidth(500)
        self.view = View(self)
        if self._image is not None:
            self.view._image = self._image
            self.view.set_picture()
        self.buttonReset = QtWidgets.QPushButton('Clear', self)
        self.buttonReset.clicked.connect(self.view.handleClearView)
        
        self.buttonDone = QtWidgets.QPushButton('Done',self)
        self.buttonDone.clicked.connect(self.handleReturn)
        
        layout = QtWidgets.QGridLayout(self)
        layout.addWidget(self.label_title,0,0,1,2)
        layout.addWidget(self.view,1,0,1,2)
        layout.addWidget(self.buttonDone,2,0,1,1)
        layout.addWidget(self.buttonReset,2,1,1,1)
        
        
                
    def handleReturn(self):
        if self.view._counter == 4:
            self._circle = self.view._circle
        self.close()
            
class View(QtWidgets.QGraphicsView):
    
    def __init__(self, parent=None):
        super(View, self).__init__(parent)
        
        self._scene = QtWidgets.QGraphicsScene(self)
        self._photo = QtWidgets.QGraphicsPixmapItem()
        self._scene.addItem(self._photo)
        self.setScene(self._scene)
        self.setSceneRect(QtCore.QRectF(self.viewport().rect()))
        
        #this counts the number of click, if it reaches 4 then it stops accepting 
        #more points and draws the cirlce
        self._counter = 0 
        self._circle = None
        #this accomulates the position of the clicks
        self._mouse_pos= np.array([]).reshape(0,2)
        self._image = None
#        pen = QtGui.QPen(QtCore.Qt.green)
#        Rec= QtCore.QRectF(150, 150,300,300)
#        self.scene().addEllipse(Rec, pen)


        
            
    def process_circle(self):
        x = np.array([self._mouse_pos[0,0],self._mouse_pos[1,0],self._mouse_pos[2,0],self._mouse_pos[3,0]])
        y = np.array([self._mouse_pos[0,1],self._mouse_pos[1,1],self._mouse_pos[2,1],self._mouse_pos[3,1]])
        circle = find_circle_from_points(x,y)
        self._circle = [int(circle[0]),int(circle[1]),int(circle[2])]
        
        
        Ellipse = QtWidgets.QGraphicsEllipseItem(0,0,self._circle[2]*2,self._circle[2]*2)
        #ellipse will be green
        pen = QtGui.QPen(QtCore.Qt.green)
        Ellipse.setPen(pen)      
        #if I want to fill the ellipse i should do this:
        #brush = QtGui.QBrush(QtCore.Qt.green) 
        #Ellipse.setPen(brush)
        
        #this is the position of the top-left corner of the ellipse.......
        Ellipse.setPos(circle[0]-self._circle[2],circle[1]-self._circle[2])
        Ellipse.setTransform(QtGui.QTransform())        
        self._scene.addItem(Ellipse)

        
        
    def mousePressEvent(self,event):
        
        if self._counter < 4:
            scenePos = self.mapToScene(event.pos())
            x = scenePos.x()
            y = scenePos.y()
            self._mouse_pos = np.concatenate((self._mouse_pos, [[float(x),float(y)]]), axis=0)
            pen = QtGui.QPen(QtCore.Qt.red)
            brush = QtGui.QBrush(QtCore.Qt.red)
            Rec= QtCore.QRectF(x, y,int(self._scene.width()*(1/100)+1),int(self._scene.width()*(1/100)+1))
            self._scene.addEllipse(Rec, pen, brush)
        
        QtWidgets.QGraphicsView.mousePressEvent(self, event)

    def mouseReleaseEvent(self,event):
#        start = QtCore.QPointF(self.mapToScene(self._start))
#        end = QtCore.QPointF(self.mapToScene(event.pos()))
#        self.scene().addItem(QtWidgets.QGraphicsLineItem(QtCore.QLineF(start, end)))
#        for point in (start, end):
#            text = self.scene().addSimpleText('(%d, %d)' % (point.x(), point.y()))
#            text.setBrush(QtCore.Qt.red)
#            text.setPos(point)
        self._counter +=1
        if self._counter == 4:
            self.process_circle()
        
        QtWidgets.QGraphicsView.mouseReleaseEvent(self, event)
        
        
    def set_picture(self):
        image = self._image.copy()
        height, width, channel = image.shape
        bytesPerLine = 3 * width
        img_Qt = QtGui.QImage(image.data, width, height, bytesPerLine, QtGui.QImage.Format_RGB888)
        img_show = QtGui.QPixmap.fromImage(img_Qt)
        self._photo = QtWidgets.QGraphicsPixmapItem()
        self._photo.setPixmap(img_show)   
        self._scene.addItem(self._photo)
        rect = QtCore.QRectF(self._photo.pixmap().rect())
        self.fitInView(rect)
        self.setSceneRect(rect)
            
    def resizeEvent(self, event):
        rect = QtCore.QRectF(self._photo.pixmap().rect())
        self.fitInView(rect)
        self.setSceneRect(rect)
        
    def handleClearView(self):
        self._scene.clear()
        #self.scene().removeItem(self._photo)
        self.set_picture()
        self._circle = None
        self._counter = 0
        self._mouse_pos= np.array([]).reshape(0,2)
        

        

if __name__ == '__main__':

    import sys
    if not QtWidgets.QApplication.instance():
        app = QtWidgets.QApplication(sys.argv)
    else:
        app = QtWidgets.QApplication.instance()
    
    GUI = ProcessEye()
    #GUI.resize(640, 480)
    GUI.show()
    sys.exit(app.exec_())            
        