# -*- coding: utf-8 -*-
"""
Created on Wed Aug 16 10:03:21 2017

@author: Diego L.Guarin -- diego_guarin at meei.harvard.edu
"""
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 14 15:42:31 2017

@author: GUARIND
"""
import os
import sys
from PyQt5 import QtWidgets
from PyQt5 import QtGui


from ImageViewerandProcess import ImageViewer

"""
This window serves to show a text line and an image. It doesn't do anaything else
"""


class ShowExample(QtWidgets.QMainWindow):
    def __init__(self):
        super(ShowExample, self).__init__()
        
        self.setWindowTitle('Example')
        #self._new_window = None

        
        
        if os.name is 'posix': #is a mac or linux
            scriptDir = os.path.dirname(sys.argv[0])
        else: #is a  windows 
                scriptDir = os.getcwd()
                
        img_Qt = QtGui.QImage(scriptDir + os.path.sep + 'include' +os.path.sep +'icons'+ os.path.sep + 'Facial-Nerve-Center.jpg')
        pixmap = QtGui.QPixmap.fromImage(img_Qt)
        self._view_photo = ImageViewer()
        self._view_photo.setBackgroundBrush(QtGui.QBrush(QtGui.QColor(230,230,230)))
        self._view_photo.setPhoto(pixmap)
        
        
        self.label_title = QtWidgets.QLabel()
        self.label_title.setText('Sample text')
        self.label_title.setWordWrap(True) 
        self.label_title.setFont(QtGui.QFont("Times",weight=QtGui.QFont.Bold))
        
        self.label_content = QtWidgets.QLabel()
        self.label_content .setText('Sample text')
        self.label_content .setWordWrap(True) 
        #self.label.setMaximumWidth(500)
        
        
        self.main_Widget = QtWidgets.QWidget(self)
        
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.label_title)
        layout.addWidget(self.label_content)
        layout.addWidget(self._view_photo)

        self.main_Widget.setLayout(layout)
        self.setCentralWidget(self.main_Widget)
               
        
        
if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    GUI = ShowExample()
    GUI.show()
    app.exec_()
    
