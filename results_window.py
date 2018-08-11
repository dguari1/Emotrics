# -*- coding: utf-8 -*-
"""
Created on Mon Aug 14 15:42:31 2017

@author: Diego L.Guarin -- diego_guarin at meei.harvard.edu
"""
import os
import sys
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore

from example_window import ShowExample


"""
This window present the measurements along with a description and an ilustration
of each measurement. Is composed of Labels and LineEdits, the LineEdits objects
are filled in the main window with the facial metrics computed using the landmarks. 
It allows up to three tabs at the same time and each tab has the same layout. 
"""


class CustomTabResult(QtWidgets.QWidget):
    
    def __init__(self):
        super(CustomTabResult, self) .__init__()

        
        if os.name is 'posix': #is a mac or linux
            scriptDir = os.path.dirname(sys.argv[0])
        else: #is a  windows 
            scriptDir = os.getcwd()
                
        spacerh = QtWidgets.QWidget(self)
        spacerh.setFixedSize(10,0)
        
        spacerv = QtWidgets.QWidget(self)
        spacerv.setFixedSize(0,10)
        
        self._tab_name = 'Tab'
        
        #labels 
        self._label0a = QtWidgets.QLabel('Right')
        self._label0b = QtWidgets.QLabel('Left')
        self._label0c = QtWidgets.QLabel('Difference (absolute)')
        self._label0d = QtWidgets.QLabel('Difference (percent)')
        
        
        
        self._CE = QtWidgets.QLabel('Commisure excursion (mm):')
        self._SA = QtWidgets.QLabel('Smile angle (deg):')
        self._CH = QtWidgets.QLabel('Commisure height deviation (mm):')
        self._UVH = QtWidgets.QLabel('Upper lip height deviation (mm):')
        self._LVH = QtWidgets.QLabel('Lower lip height deviation (mm):')
        self._DS = QtWidgets.QLabel('Dental show (mm):')
        self._MRD1 = QtWidgets.QLabel('Marginal reflex distance 1 (mm):')
        self._MRD2 = QtWidgets.QLabel('Marginal reflex distance 2 (mm):')
        self._BH = QtWidgets.QLabel('Brow height (mm):')
        self._PFH = QtWidgets.QLabel('Palpebral fissure height (mm):')
        #text lines
        
        #Commisure excursion
        self._CE_right = QtWidgets.QLineEdit(self)
        self._CE_right.setText("-")
        self._CE_left = QtWidgets.QLineEdit(self)
        self._CE_left.setText("-")
        self._CE_dev = QtWidgets.QLineEdit(self)
        self._CE_dev.setText("-")
        self._CE_dev_p = QtWidgets.QLineEdit(self)
        self._CE_dev_p.setText("-")
        
        #Smile angle
        self._SA_right = QtWidgets.QLineEdit(self)
        self._SA_right.setText("-")
        self._SA_left = QtWidgets.QLineEdit(self)
        self._SA_left.setText("-")
        self._SA_dev = QtWidgets.QLineEdit(self)
        self._SA_dev.setText("-")      
        self._SA_dev_p = QtWidgets.QLineEdit(self)
        self._SA_dev_p.setText("-")    
        
        #Commisure height
        self._CH_right = QtWidgets.QLineEdit(self)
        self._CH_right.setText("-")
        self._CH_left = QtWidgets.QLineEdit(self)
        self._CH_left.setText("-")
        self._CH_dev = QtWidgets.QLineEdit(self)
        self._CH_dev.setText("-") 
        self._CH_dev_p = QtWidgets.QLineEdit(self)
        self._CH_dev_p.setText("-") 

        #Upper vermillion height
        self._UVH_right = QtWidgets.QLineEdit(self)
        self._UVH_right.setText("-")
        self._UVH_left = QtWidgets.QLineEdit(self)
        self._UVH_left.setText("-")
        self._UVH_dev = QtWidgets.QLineEdit(self)
        self._UVH_dev.setText("-")  
        self._UVH_dev_p = QtWidgets.QLineEdit(self)
        self._UVH_dev_p.setText("-")  
        
        #lower vermillion height 
        self._LVH_right = QtWidgets.QLineEdit(self)
        self._LVH_right.setText("-")
        self._LVH_left = QtWidgets.QLineEdit(self)
        self._LVH_left.setText("-")
        self._LVH_dev = QtWidgets.QLineEdit(self)
        self._LVH_dev.setText("-")
        self._LVH_dev_p = QtWidgets.QLineEdit(self)
        self._LVH_dev_p.setText("-")
        
        #Dental show
        self._DS_right = QtWidgets.QLineEdit(self)
        self._DS_right.setText("-")
        self._DS_left = QtWidgets.QLineEdit(self)
        self._DS_left.setText("-")
        self._DS_dev = QtWidgets.QLineEdit(self)
        self._DS_dev.setText("-")  
        self._DS_dev_p = QtWidgets.QLineEdit(self)
        self._DS_dev_p.setText("-")  
        
        #Marginal reflex distance 1
        self._MRD1_right = QtWidgets.QLineEdit(self)
        self._MRD1_right.setText("-")
        self._MRD1_left = QtWidgets.QLineEdit(self)
        self._MRD1_left.setText("-")
        self._MRD1_dev = QtWidgets.QLineEdit(self)
        self._MRD1_dev.setText("-")  
        self._MRD1_dev_p = QtWidgets.QLineEdit(self)
        self._MRD1_dev_p.setText("-") 
        
        #Marginal reflex distance 2
        self._MRD2_right = QtWidgets.QLineEdit(self)
        self._MRD2_right.setText("-")
        self._MRD2_left = QtWidgets.QLineEdit(self)
        self._MRD2_left.setText("-")
        self._MRD2_dev = QtWidgets.QLineEdit(self)
        self._MRD2_dev.setText("-") 
        self._MRD2_dev_p = QtWidgets.QLineEdit(self)
        self._MRD2_dev_p.setText("-")
        
        #Brown height
        self._BH_right = QtWidgets.QLineEdit(self)
        self._BH_right.setText("-")
        self._BH_left = QtWidgets.QLineEdit(self)
        self._BH_left.setText("-")
        self._BH_dev = QtWidgets.QLineEdit(self)
        self._BH_dev.setText("-")
        self._BH_dev_p = QtWidgets.QLineEdit(self)
        self._BH_dev_p.setText("-")
        
        
        #Palpebral fissure height 
        self._PFH_right = QtWidgets.QLineEdit(self)
        self._PFH_right.setText("-")
        self._PFH_left = QtWidgets.QLineEdit(self)
        self._PFH_left.setText("-")
        self._PFH_dev = QtWidgets.QLineEdit(self)
        self._PFH_dev.setText("-") 
        self._PFH_dev_p = QtWidgets.QLineEdit(self)
        self._PFH_dev_p.setText("-")
        
        
        
        #help buttons
        self._help_CE = QtWidgets.QPushButton('', self)
        self._help_CE.setIcon(QtGui.QIcon(scriptDir + os.path.sep + 'include' +os.path.sep +'icon_color'+ os.path.sep + 'question_icon.png'))
        pixmap_CE = QtGui.QPixmap.fromImage(QtGui.QImage(
        scriptDir + os.path.sep + 'include' +os.path.sep +'measures'+ os.path.sep + 'commissure_excursion.png'))
        text_CE_title = 'Commissure Excursion:'
        text_CE_content = 'Distance from midline vertical / lower lip vermillion junction point to the oral commissure'
        self._help_CE.clicked.connect(lambda: self.push_help_CE(pixmap_CE, text_CE_title, text_CE_content))
        self._help_CE.setIconSize(QtCore.QSize(20,20))
        
        self._help_SA = QtWidgets.QPushButton('', self)
        self._help_SA.setIcon(QtGui.QIcon(scriptDir + os.path.sep + 'include' +os.path.sep +'icon_color'+ os.path.sep + 'question_icon.png'))
        pixmap_SA = QtGui.QPixmap.fromImage(QtGui.QImage(
        scriptDir + os.path.sep + 'include' +os.path.sep +'measures'+ os.path.sep + 'smile_angle.png'))
        text_SA_title = 'Smile Angle:'
        text_SA_content = 'Angle between the horizontal plane at the midline vertical / lower lip vermillion junction point and the oral commissure'
        self._help_SA.clicked.connect(lambda: self.push_help_CE(pixmap_SA, text_SA_title, text_SA_content))
        self._help_SA.setIconSize(QtCore.QSize(20,20))
        
        self._help_CH = QtWidgets.QPushButton('', self)
        self._help_CH.setIcon(QtGui.QIcon(scriptDir + os.path.sep + 'include' +os.path.sep +'icon_color'+ os.path.sep + 'question_icon.png'))
        pixmap_CH = QtGui.QPixmap.fromImage(QtGui.QImage(
        scriptDir + os.path.sep + 'include' +os.path.sep +'measures'+ os.path.sep + 'commissure_deviation_focus.png'))
        text_CH_title = 'Commissure Height Deviation:'
        text_CH_content = 'Vertical distance (red line) between the horizontal plane of the left and right oral commissure'
        self._help_CH.clicked.connect(lambda: self.push_help_CE(pixmap_CH, text_CH_title, text_CH_content))
        self._help_CH.setIconSize(QtCore.QSize(20,20))
        
        self._help_UVH = QtWidgets.QPushButton('', self)
        self._help_UVH.setIcon(QtGui.QIcon(scriptDir + os.path.sep + 'include' +os.path.sep +'icon_color'+ os.path.sep + 'question_icon.png'))
        pixmap_UVH = QtGui.QPixmap.fromImage(QtGui.QImage(
        scriptDir + os.path.sep + 'include' +os.path.sep +'measures'+ os.path.sep + 'upper_lip_height_deviation_focus.png'))
        text_UVH_title = 'Upper Lip Height Deviation:'
        text_UVH_content = 'Vertical distance (red line) between the horizontal planes taken from the upper lip vermillion border (red points) where they intersect with a vertical plane taken midway between the mid-vertical (green line) and the oral commissure'        
        self._help_UVH.clicked.connect(lambda: self.push_help_CE(pixmap_UVH, text_UVH_title, text_UVH_content))
        self._help_UVH.setIconSize(QtCore.QSize(20,20))
        
        self._help_LVH = QtWidgets.QPushButton('', self)
        self._help_LVH.setIcon(QtGui.QIcon(scriptDir + os.path.sep + 'include' +os.path.sep +'icon_color'+ os.path.sep + 'question_icon.png'))
        pixmap_LVH = QtGui.QPixmap.fromImage(QtGui.QImage(
        scriptDir + os.path.sep + 'include' +os.path.sep +'measures'+ os.path.sep + 'lower_lip_height_deviation_focus.png'))
        text_LVH_title = 'Lower Lip Height Deviation:'
        text_LVH_content = 'Vertical distance (red line) between the horizontal planes taken from the lower lip vermillion border points (red dots) where they intersect with a vertical plane (green dotted line) taken midway between the mid-vertical (green line) and the oral commissure'        
        self._help_LVH.clicked.connect(lambda: self.push_help_CE(pixmap_LVH, text_LVH_title, text_LVH_content))
        self._help_LVH.setIconSize(QtCore.QSize(20,20))
        
        self._help_DS = QtWidgets.QPushButton('', self)
        self._help_DS.setIcon(QtGui.QIcon(scriptDir + os.path.sep + 'include' +os.path.sep +'icon_color'+ os.path.sep + 'question_icon.png'))
        pixmap_DS = QtGui.QPixmap.fromImage(QtGui.QImage(
        scriptDir + os.path.sep + 'include' +os.path.sep +'measures'+ os.path.sep + 'dental_show_focus.png'))
        text_DS_title = 'Dental Show:'
        text_DS_content = 'Vertical distance between the mucosal borders of the the upper and lower lip along the vertical plane taken halfway between the mid-vertical and the oral commissure'
        self._help_DS.clicked.connect(lambda: self.push_help_CE(pixmap_DS, text_DS_title, text_DS_content))
        self._help_DS.setIconSize(QtCore.QSize(20,20))  
        
        self._help_MRD1 = QtWidgets.QPushButton('', self)
        self._help_MRD1.setIcon(QtGui.QIcon(scriptDir + os.path.sep + 'include' +os.path.sep +'icon_color'+ os.path.sep + 'question_icon.png'))
        pixmap_MRD1 = QtGui.QPixmap.fromImage(QtGui.QImage(
        scriptDir + os.path.sep + 'include' +os.path.sep +'measures'+ os.path.sep + 'marginal_reflex_distance_1_focus.png'))
        text_MRD1_title = 'Marginal Reflex Distance 1:'
        text_MRD1_content = 'Vertical distance from the mid-pupillary point to the upper eyelid margin'                
        self._help_MRD1.clicked.connect(lambda: self.push_help_CE(pixmap_MRD1, text_MRD1_title, text_MRD1_content))
        self._help_MRD1.setIconSize(QtCore.QSize(20,20))          
              
        self._help_MRD2 = QtWidgets.QPushButton('', self)
        self._help_MRD2.setIcon(QtGui.QIcon(scriptDir + os.path.sep + 'include' +os.path.sep +'icon_color'+ os.path.sep + 'question_icon.png'))
        pixmap_MRD2 = QtGui.QPixmap.fromImage(QtGui.QImage(
        scriptDir + os.path.sep + 'include' +os.path.sep +'measures'+ os.path.sep + 'marginal_reflex_distance_2_focus.png'))
        text_MRD2_title = 'Marginal Reflex Distance 2:'
        text_MRD2_content = 'Vertical distance from the mid-pupillary point to the lower eyelid margin'                
        self._help_MRD2.clicked.connect(lambda: self.push_help_CE(pixmap_MRD2, text_MRD2_title, text_MRD2_content))
        self._help_MRD2.setIconSize(QtCore.QSize(20,20))   
        
        self._help_BH = QtWidgets.QPushButton('', self)
        self._help_BH.setIcon(QtGui.QIcon(scriptDir + os.path.sep + 'include' +os.path.sep +'icon_color'+ os.path.sep + 'question_icon.png'))
        pixmap_BH = QtGui.QPixmap.fromImage(QtGui.QImage(
        scriptDir + os.path.sep + 'include' +os.path.sep +'measures'+ os.path.sep + 'brow_height_focus.png'))
        text_BH_title = 'Brow Height:'
        text_BH_content = 'Vertical distance from the mid-pupillary point to the superior border of the brow'        
        self._help_BH.clicked.connect(lambda: self.push_help_CE(pixmap_BH, text_BH_title, text_BH_content))
        self._help_BH.setIconSize(QtCore.QSize(20,20))    
        
        
        self._help_PFH = QtWidgets.QPushButton('', self)
        self._help_PFH.setIcon(QtGui.QIcon(scriptDir + os.path.sep + 'include' +os.path.sep +'icon_color'+ os.path.sep + 'question_icon.png'))
        pixmap_PFH = QtGui.QPixmap.fromImage(QtGui.QImage(
        scriptDir + os.path.sep + 'include' +os.path.sep +'measures'+ os.path.sep + 'palpebral_fissure_height_focus.png'))
        text_PFH_title = 'Palpebral Fissure Height:'
        text_PFH_content = 'Vertical distance between medial canthi of the two open lids'          
        self._help_PFH.clicked.connect(lambda: self.push_help_CE(pixmap_PFH, text_PFH_title, text_PFH_content))
        self._help_PFH.setIconSize(QtCore.QSize(20,20))    

        layout = QtWidgets.QGridLayout()
        #layout.addWidget(spacerh,0,1)
        layout.addWidget(self._label0a, 0,2,1,1)
        layout.addWidget(spacerh,0,3)
        layout.addWidget(self._label0b, 0,4,1,1)
        layout.addWidget(spacerh,0,5)
        layout.addWidget(self._label0c, 0,6,1,1)
        layout.addWidget(spacerh,0,7)
        layout.addWidget(self._label0d, 0,8,1,1)

        layout.addWidget(spacerv,1,0,6,1)
        layout.addWidget(self._BH, 2,0,1,1)
        layout.addWidget(self._help_BH, 2,1,1,1)
        layout.addWidget(self._BH_right,2,2,1,1)
        layout.addWidget(self._BH_left,2,4,1,1)
        layout.addWidget(self._BH_dev,2,6,1,1)
        layout.addWidget(self._BH_dev_p,2,8,1,1)
        
        layout.addWidget(spacerv,3,0,6,1)
        layout.addWidget(self._MRD1, 4,0,1,1)
        layout.addWidget(self._help_MRD1, 4,1,1,1)
        layout.addWidget(self._MRD1_right,4,2,1,1)
        layout.addWidget(self._MRD1_left,4,4,1,1)
        layout.addWidget(self._MRD1_dev,4,6,1,1)
        layout.addWidget(self._MRD1_dev_p,4,8,1,1)
        
        layout.addWidget(spacerv,5,0,6,1)
        layout.addWidget(self._MRD2, 6,0,1,1)
        layout.addWidget(self._help_MRD2, 6,1,1,1)
        layout.addWidget(self._MRD2_right,6,2,1,1)
        layout.addWidget(self._MRD2_left,6,4,1,1)
        layout.addWidget(self._MRD2_dev,6,6,1,1)
        layout.addWidget(self._MRD2_dev_p,6,8,1,1)
        
        layout.addWidget(spacerv,7,0,6,1)
        layout.addWidget(self._PFH, 8,0,1,1)
        layout.addWidget(self._help_PFH, 8,1,1,1)
        layout.addWidget(self._PFH_right,8,2,1,1)
        layout.addWidget(self._PFH_left,8,4,1,1)
        layout.addWidget(self._PFH_dev,8,6,1,1)
        layout.addWidget(self._PFH_dev_p,8,8,1,1)
        
        layout.addWidget(spacerv,9,0,6,1)
        layout.addWidget(self._CE, 10,0,1,1)
        layout.addWidget(self._help_CE, 10,1,1,1)
        layout.addWidget(self._CE_right,10,2,1,1)
        layout.addWidget(self._CE_left,10,4,1,1)
        layout.addWidget(self._CE_dev,10,6,1,1)
        layout.addWidget(self._CE_dev_p,10,8,1,1)
        
        layout.addWidget(spacerv,11,0,6,1)
        layout.addWidget(self._CH, 12,0,1,1)
        layout.addWidget(self._help_CH, 12,1,1,1)
        layout.addWidget(self._CH_right,12,2,1,1)
        layout.addWidget(self._CH_left,12,4,1,1)
        layout.addWidget(self._CH_dev,12,6,1,1)
        layout.addWidget(self._CH_dev_p,12,8,1,1)
        
        layout.addWidget(spacerv,13,0,6,1)
        layout.addWidget(self._SA, 14,0,1,1)
        layout.addWidget(self._help_SA, 14,1,1,1)
        layout.addWidget(self._SA_right,14,2,1,1)
        layout.addWidget(self._SA_left,14,4,1,1)
        layout.addWidget(self._SA_dev,14,6,1,1)
        layout.addWidget(self._SA_dev_p,14,8,1,1)
        
        layout.addWidget(spacerv,15,0,6,1)
        layout.addWidget(self._UVH, 16,0,1,1)
        layout.addWidget(self._help_UVH, 16,1,1,1)
        layout.addWidget(self._UVH_right,16,2,1,1)
        layout.addWidget(self._UVH_left,16,4,1,1)
        layout.addWidget(self._UVH_dev,16,6,1,1)
        layout.addWidget(self._UVH_dev_p,16,8,1,1)
        
        layout.addWidget(spacerv,17,0,6,1)
        layout.addWidget(self._DS, 18,0,1,1)
        layout.addWidget(self._help_DS, 18,1,1,1)
        layout.addWidget(self._DS_right,18,2,1,1)
        layout.addWidget(self._DS_left,18,4,1,1)
        layout.addWidget(self._DS_dev,18,6,1,1)
        layout.addWidget(self._DS_dev_p,18,8,1,1)
        
        layout.addWidget(spacerv,19,0,6,1)
        layout.addWidget(self._LVH, 20,0,1,1)
        layout.addWidget(self._help_LVH, 20,1,1,1)
        layout.addWidget(self._LVH_right,20,2,1,1)
        layout.addWidget(self._LVH_left,20,4,1,1)
        layout.addWidget(self._LVH_dev,20,6,1,1)
        layout.addWidget(self._LVH_dev_p,20,8,1,1)
        
        self.setLayout(layout)
        
    def push_help_CE(self, pixmap, text_title='', text_content=''):  
        self._Example_window =  ShowExample()
        self._Example_window._view_photo.setPhoto(pixmap)
        self._Example_window.label_title.setText(text_title)
        self._Example_window.label_content.setText(text_content)
        self._Example_window.show()




class ShowResults(QtWidgets.QWidget):
    def __init__(self, tab1,tab2=None, tab3=None, parent=None):
        super(ShowResults, self).__init__(parent)
        
        self.setWindowTitle('Metrics')
        if os.name is 'posix': #is a mac or linux
            scriptDir = os.path.dirname(sys.argv[0])
        else: #is a  windows 
            scriptDir = os.getcwd()
        self.setWindowIcon(QtGui.QIcon(scriptDir + os.path.sep + 'include' +os.path.sep +'icon_color'+ os.path.sep + 'ruler_icon.ico'))
        self._Example_window = None
        
        self.main_Widget = QtWidgets.QTabWidget(self)
        tab1.setAutoFillBackground(True)
        self.main_Widget.addTab(tab1,tab1._tab_name)
        
        if tab2 is not None:
            tab2.setAutoFillBackground(True)
            self.main_Widget.addTab(tab2,tab2._tab_name)
            
        
        if tab3 is not None:
            tab3.setAutoFillBackground(True)
            self.main_Widget.addTab(tab3,'Difference')
            
        
        
        
        
        layout=QtWidgets.QVBoxLayout()
        layout.addWidget(self.main_Widget)

       
        self.setLayout(layout)
        #self.show()       
        
if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    GUI = ShowResults()
    GUI.show()
    app.exec_()
    