# -*- coding: utf-8 -*-
"""
Created on Mon Aug 14 22:12:59 2017

@author: Diego L.Guarin -- diego_guarin at meei.harvard.edu
"""
import os
import numpy as np
import cv2
from scipy import linalg
import pandas as pd

#from dlib import get_frontal_face_detector
#from dlib import shape_predictor
#from dlib import rectangle

from measurements import get_measurements_from_data

"""
This is where the main computations are performed. 
"""


def shape_to_np(shape,dtype="int"):
    #function to transform the results provided by dlib into usable np arrays
    coords=np.zeros((68,2),dtype=dtype)
    #the figure was reduced by 10 to speed things-up
    for i in range(0,68):
        coords[i] = (shape.part(i).x, shape.part(i).y)
        
    return coords

def get_info_from_txt(file):
    #function to read the landmark, iris and bounding box location from txt files
    shape=np.zeros((68,2),dtype=int)
    left_pupil = np.zeros((1,3),dtype=int)
    right_pupil = np.zeros((1,3),dtype=int)
    bounding_box = np.zeros((1,4),dtype=int)
    
    cont_landmarks = 0
    get_landmarks = 0
    
    get_leftpupil = 0
    cont_leftpupil = 0
    
    get_rightpupil = 0
    cont_rightpupil = 0
    
    get_boundingbox = 0
    cont_boundingbox = 0 
    with open(file, 'r') as file:
        for i,line in enumerate(file):    
            if i == 4:    
                get_landmarks=1
            if i == 72:
                get_landmarks=0
                
            if get_landmarks == 1:
                temp=(line[:]).split(',')
                shape[cont_landmarks,0]=int(temp[0])
                shape[cont_landmarks,1]=int(temp[1])
                cont_landmarks += 1
                
            if i == 74:
                get_leftpupil = 1
            if i == 77:
                get_leftpupil = 0
                
            if get_leftpupil == 1:
                left_pupil[0,cont_leftpupil]=int(line[:])
                cont_leftpupil += 1
    
            if i == 79:
                get_rightpupil = 1
            if i == 82:
                get_rightpupil = 0
                
            if get_rightpupil == 1:            
                right_pupil[0,cont_rightpupil]=int(line[:])
                cont_rightpupil += 1 
                
            if i == 84:
                get_boundingbox = 1
            if i == 88:
                get_boundingbox = 0
                 
            if get_boundingbox == 1 :
                bounding_box[0,cont_boundingbox] = int(line[:])
                cont_boundingbox +=1
     
    lefteye=[left_pupil[0,0],left_pupil[0,1],left_pupil[0,2]]
    righteye=[right_pupil[0,0],right_pupil[0,1],right_pupil[0,2]]
    
    if cont_boundingbox > 0 :
        boundingbox = [bounding_box[0,0],bounding_box[0,1],bounding_box[0,2],bounding_box[0,3]]    
    else:
        boundingbox = [0,0,0,0]
    
    if lefteye[2] < 0 and righteye[2] >0:
        #left eye is closed, use right iris diameter and locate iris in center of eye
        lefteye[2] = righteye[2]           
        x_eye = shape[42:47,0]
        y_eye = shape[42:47,1]
        lefteye[0] = int(np.round(np.mean(x_eye),0))
        lefteye[1] = int(np.round(np.mean(y_eye),0))
        #message = 'Left Eye Closed'
         
    if righteye[2] < 0 and lefteye[2] >0:
        #Right eye is closed, use left iris diameter and locate iris in center of eye
        righteye[2] = lefteye[2]
        x_eye = shape[36:41,0]
        y_eye = shape[36:41,1]
        righteye[0] = int(np.round(np.mean(x_eye),0))
        righteye[1] = int(np.round(np.mean(y_eye),0))
        #message = 'Right Eye Closed'
            
    if righteye[2] < 0 and lefteye[2] <0:
        #both eyes are closed, use 1/4 of eye lenght as radius
        #and the center of mass of the eye as the center
        
        #for left eye 
        x_eye = shape[42:47,0]
        y_eye = shape[42:47,1]
        lefteye[0] = int(np.round(np.mean(x_eye),0))
        lefteye[1] = int(np.round(np.mean(y_eye),0))
        lefteye[2] = int(np.round((shape[45,0]-lefteye[0])/2))
        
        #for right eye 
        x_eye = shape[36:41,0]
        y_eye = shape[36:41,1]
        righteye[0] = int(np.round(np.mean(x_eye),0))
        righteye[1] = int(np.round(np.mean(y_eye),0))
        righteye[2] = int(np.round((shape[39,0]-righteye[0])/2))
        #message = 'Both Eyes Closed'
           
    return shape, lefteye, righteye, boundingbox

def get_landmark_size(shape):
    if shape[36,1]!=-1 and shape[39,1]!=-1:
        size_landmarks = np.round(0.025*np.sqrt((shape[39,0]-shape[36,0])**2 + (shape[39,1]-shape[36,1])**2),0)
        size_landmarks = int(np.floor(size_landmarks))
    else:
        size_landmarks = np.round(0.025*np.sqrt((shape[42,0]-shape[45,0])**2 + (shape[42,1]-shape[45,1])**2),0)
        size_landmarks = int(np.floor(size_landmarks))  
        
    return size_landmarks
    

def mark_picture(image, shape, circle_left, circle_right, points = None, size_landmarks = None):
    #function to draw on the image the landmaks, iris circles and lines
    
    h,w,_=image.shape
    
    #if requested, then draw a two lines to divide the face
    if points is not None:
        if h < 1000: #image is small, make lines of 2 pixel
            cv2.line(image,points[0],points[1],(0,255,0),2)        
            cv2.line(image,points[2],points[3],(0,255,0),2)
            cv2.line(image,points[4],points[5],(0,255,0),2)
        else:
            cv2.line(image,points[0],points[1],(0,255,0),4)        
            cv2.line(image,points[2],points[3],(0,255,0),4)
            cv2.line(image,points[4],points[5],(0,255,0),4)            


    #draw 68 landmark points
    aux=1
    if size_landmarks is None:
        if shape[36,1]!=-1 and shape[39,1]!=-1:
            size_landmarks = np.round(0.025*np.sqrt((shape[39,0]-shape[36,0])**2 + (shape[39,1]-shape[36,1])**2),0)
            size_landmarks = int(np.floor(size_landmarks))
        else:
            size_landmarks = np.round(0.025*np.sqrt((shape[42,0]-shape[45,0])**2 + (shape[42,1]-shape[45,1])**2),0)
            size_landmarks = int(np.floor(size_landmarks)) 


    for (x,y) in shape:
        if x>0:
            #mark_size=int(w/180)
            #if mark_size>4: mark_size=4
            #size_landmarks = 4
            if aux == 62 or aux == 64 or aux == 38 or aux == 39 or aux == 44 or aux == 45:
                cv2.circle(image, (x,y), size_landmarks , (0,255,255),-1)
            elif aux == 63 :
                cv2.circle(image, (x,y), size_landmarks+1 , (0,255,255),-1)
            elif aux == 67 :
                cv2.circle(image, (x,y), size_landmarks+1 , (0,0,255),-1)
            else:
                cv2.circle(image, (x,y), size_landmarks , (0,0,255),-1)
            cv2.putText(image, str(aux), (x-2,y-2), cv2.FONT_HERSHEY_DUPLEX, 0.125*size_landmarks, (0,0,0), 1)
            #           
        aux +=1
    
    #draw left iris
    if circle_left[2]>0:
        if h < 1000: #image is small, make circle of 1 pixel
            cv2.circle(image, 
               tuple([int(circle_left[0]),
               int(circle_left[1])]),
               int(circle_left[2]),(0,255,0),1)
        else:  #image is large, make circle of 2 pixel
            cv2.circle(image, 
               tuple([int(circle_left[0]),
               int(circle_left[1])]),
               int(circle_left[2]),(0,255,0),2)            
    
        cv2.circle(image, 
               tuple([int(circle_left[0]),
               int(circle_left[1])]),
               int(circle_left[2]/4),(0,255,0),-1)
    
    #draw right iris
    if circle_right[2]>0:
        if h < 1000: #image is small, make circle of 1 pixel
            cv2.circle(image, 
               tuple([int(circle_right[0]),
               int(circle_right[1])]),
               int(circle_right[2]),(0,255,0),1)
        else: #image is large, make circle of 2 pixel
            cv2.circle(image, 
               tuple([int(circle_right[0]),
               int(circle_right[1])]),
               int(circle_right[2]),(0,255,0),2)
        cv2.circle(image, 
               tuple([int(circle_right[0]),
               int(circle_right[1])]),
               int(circle_right[2]/4),(0,255,0),-1)
    
    return image

def estimate_lines(InputImage,circle_left, circle_right):
    #function to estimate the line that connects the center of the eyes and a 
    #new, perpendicular line in the middle
    
    h, w, _ = InputImage.shape
    
    x_1=circle_right[0]
    y_1=circle_right[1]
    
    x_2=circle_left[0]
    y_2=circle_left[1]
    
    #find the point in the middle of the line
    x_m=((x_2-x_1)/2)+x_1
    m=(y_2-y_1)/(x_2-x_1)   
    y_m=(y_1+m*(x_m-x_1))
    
    x_m=int(round(x_m,0))
    y_m=int(round(y_m,0))
    angle=np.arctan(m)+np.pi/2
    
    
    x_p1=int(round(x_m+0.5*h*np.cos(angle)))
    y_p1=int(round(y_m+0.5*h*np.sin(angle)))
    
    x_p2=int(round(x_m-0.25*h*np.cos(angle)))
    y_p2=int(round(y_m-0.25*h*np.sin(angle)))     
    
    
    points=[(x_1,y_1),(x_2,y_2),(x_m,y_m),(x_p1,y_p1),(x_m,y_m),(x_p2, y_p2)]
    
    return points


def find_circle_from_points(x,y):
    #this function finds the center and radius of a circle from a set of points 
    #in the circle. x and y are the coordinates of the points. 
    
    # coordinates of the barycenter
    x_m = np.mean(x)
    y_m = np.mean(y)

    # calculation of the reduced coordinates
    u = x - x_m
    v = y - y_m

    # linear system defining the center (uc, vc) in reduced coordinates:
    #    Suu * uc +  Suv * vc = (Suuu + Suvv)/2
    #    Suv * uc +  Svv * vc = (Suuv + Svvv)/2
    Suv  = sum(u*v)
    Suu  = sum(u**2)
    Svv  = sum(v**2)
    Suuv = sum(u**2 * v)
    Suvv = sum(u * v**2)
    Suuu = sum(u**3)
    Svvv = sum(v**3)

    # Solving the linear system
    A = np.array([ [ Suu, Suv ], [Suv, Svv]])
    B = np.array([ Suuu + Suvv, Svvv + Suuv ])/2.0
    uc, vc = linalg.solve(A,B)

    xc_1 = x_m + uc
    yc_1 = y_m + vc

    # Calcul des distances au centre (xc_1, yc_1)
    Ri_1     = np.sqrt((x-xc_1)**2 + (y-yc_1)**2)
    R_1      = np.mean(Ri_1)

    
    circle=[int(xc_1),int(yc_1),int(R_1)]
    #circle.append((int(xc_1),int(yc_1),int(R_1)))
    
    return circle
##this function has been deprecated, the landmark localization is now performed in a separate thread. See Landmaks.py
#def get_landmarks(image):
#    #function to automatically localize the landmarks in the a face image using 
#    #dlib algorithm 
#    detector = get_frontal_face_detector()
#    scriptDir = os.path.dirname(os.path.realpath(__file__))
#    predictor = shape_predictor(scriptDir + os.path.sep + 'include' +os.path.sep +'data'+ os.path.sep + 'shape_predictor_68_face_landmarks.dat')
#    
#    gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
#        
#    #resize image to speed up face dectection
#    height, width = gray.shape[:2]  
#    newWidth=200
#    ScalingFactor=width/newWidth
#    newHeight=int(height/ScalingFactor)
#    smallImage=cv2.resize(gray, (newWidth, newHeight), interpolation=cv2.INTER_AREA)
#
#    #detect face in image using dlib.get_frontal_face_detector()
#    rects = detector(smallImage,1)
#    if len(rects) == 1:   
#        #now we have only one face in the image
#        #function to obtain facial landmarks using dlib 
#        #given an image and a face
#        #rectangle
#        for (i, rect) in enumerate(rects):
#            # determine the facial landmarks for the face region, then
#            # convert the facial landmark (x, y)-coordinates to a NumPy array
#
#            #adjust face position using the scaling factor
#            mod_rect=rectangle(
#                    left=int(rect.left() * ScalingFactor), 
#                    top=int(rect.top() * ScalingFactor), 
#                    right=int(rect.right() * ScalingFactor), 
#                    bottom=int(rect.bottom() * ScalingFactor))
#   
#            #predict facial landmarks 
#            shape = predictor(image, mod_rect)   
#        
#            #transform shape object to np.matrix type
#            shape = shape_to_np(shape)
#            
#    else:
#        shape = None
#        
#        
#    return shape
#
##this function has been deprecated, the landmark localization is now performed in a separate thread. See Landmaks.py
#def get_pupil(InputImage):
#    
#    #this function appplies a modified Daugman procedure for iris detection.
#    #See 'How Iris Recognition Works, Jhon Dougman - IEEE Transactions on 
#    #circuits and systems for video technology, January 2004'
#    
#    #get dimension of image 
#    h_eye, w_eye, d_eye = InputImage.shape
#    
#    #this is the variable that will be return after processing
#    circle=[]
#    
#    #verify that it is a color image
#    if d_eye < 3:
#        print('Pupil cannot be detected -- Color image is required')
#        #circle=[int(w_eye/2), int(h_eye/2), int(w_eye/4)]
#        circle=[-1,-1,-1]
#        return circle
#        
#    #verify that the eye is open  
#    #print(w_eye/h_eye)
#    if w_eye/h_eye > 3.2:
#        print('Pupil cannot be detected -- Eye is closed')
#        circle=[int(w_eye/2), int(h_eye/2), int(w_eye/4)]
#        return circle
#    
#    #reduce brightness to help with light-colored eyes
#    InputImage=np.array(InputImage*0.75+0, dtype=InputImage.dtype)
#    
#    #split image into its different color channels 
#    b,g,r = cv2.split(InputImage)
#    
#    #and create a new gray-image combining the blue and green channels, this 
#    #will help to differentiate between the iris and sclera 
#    #the function cv2.add guarantees that the resulting image has values 
#    #between 0 (white) and 255 (black)
#    bg = cv2.add(b,g)
#    #filter the image to smooth the borders
#    bg = cv2.GaussianBlur(bg,(3,3),0)
#    
#    #we assume that the radii of the iris is between 1/5.5 and 1/3.5 times the eye 
#    #width (this value was obtained after measuring multiple eye images, it only
#    #works if the eye section was obtained via dlib)
#    Rmin=int(w_eye/5.5)
#    Rmax=int(w_eye/3.5)
#    radius=range(Rmin,Rmax+1)
#    
#    result_value=np.zeros(bg.shape, dtype=float)
#    result_index_ratio=np.zeros(bg.shape, dtype=bg.dtype)
#    mask = np.zeros(bg.shape, dtype=bg.dtype)
#    
#    #apply the Dougnman's procedure for iris detection. In this case I modify the 
#    #procedure instead of use a full circunference it only uses 1/5 of 
#    #a circunference. The procedure uses a circle between -35deg-0deg and 
#    #180deg-215deg if the center beeing analized is located in the top half of the 
#    #eye image, and a circle between 0deg-35deg and 145deg-180deg if the center 
#    #beeing analized is located in the bottom half of the eye image
#    
#    possible_x=range(Rmin,w_eye-Rmin)
#    possible_y=range(0,h_eye)
#    for x in possible_x:
#        for y in possible_y:  
#                      
#            intensity=[]
#            for r in radius:
#                
#                if y>=int(h_eye/2):
#                    temp_mask=mask.copy()   
#                    #cv2.circle(temp_mask,(x,y),r,(255,255,255),1)
#                    cv2.ellipse(temp_mask, (x,y), (r,r), 0, -35, 0, (255,255,255),1)
#                    cv2.ellipse(temp_mask, (x,y), (r,r), 0, 180, 215, (255,255,255),1)
#                    processed = cv2.bitwise_and(bg,temp_mask)
#                    intensity.append(cv2.sumElems(processed)[0]/(2*3.141516*r))
#                
#                else:
#                    temp_mask=mask.copy()   
#                    #cv2.circle(temp_mask,(x,y),r,(255,255,255),1)
#                    cv2.ellipse(temp_mask, (x,y), (r,r), 0, 0, 35, (255,255,255),1)
#                    cv2.ellipse(temp_mask, (x,y), (r,r), 0, 145, 180, (255,255,255),1)
#                    processed = cv2.bitwise_and(bg,temp_mask)
#                    intensity.append(cv2.sumElems(processed)[0]/(2*3.141516*r))                
#    
#    
#            diff_vector=np.diff(intensity)
#            max_value=max(diff_vector)
#            max_index = [i for i, j in enumerate(diff_vector) if j == max_value]   
#            result_value[y,x]=max_value
#            result_index_ratio[y,x]=max_index[0]
#        
#    
#    
#    #the results are filtered by a Gaussian filter, as suggested by Daugman
#    result_value=cv2.GaussianBlur(result_value,(7,7),0)
#    
#    
#    
#    #now we need to find the center and radii that show the largest change in 
#    #intensity    
#    matrix = result_value
#    needle = np.max(matrix)
#    
#    matrix_dim = w_eye
#    item_index = 0
#    for row in matrix:
#        for i in row:
#            if i == needle:
#                break
#            item_index += 1
#        if i == needle:
#            break
#    
#    #this is the center and radius of the selected circle
#    c_y_det=int(item_index / matrix_dim) 
#    c_x_det=item_index % matrix_dim
#    r_det=radius[result_index_ratio[c_y_det,c_x_det]]
#    
#    circle=[c_x_det,c_y_det,r_det]   
#    
#    return circle 
#
##this function has been deprecated, the landmark localization is now performed in a separate thread. See Landmaks.py
#def get_pupil_from_image(Image, shape, position):
#    
#    #function that selects the eye from a face image and uses -get_pupil- to 
#    #localize the iris. 
#
#    if position == 'left':
#        #Left Eye
#        x_left = shape[42,0]
#        w_left = (shape[45,0]-x_left)
#        y_left = min(shape[43,1],shape[44,1])
#        h_left = (max(shape[46,1],shape[47,1])-y_left)
#        Eye = Image.copy()
#        Eye = Eye[(y_left-5):(y_left+h_left+5),(x_left-5):(x_left+w_left+5)]
#        selected_circle = get_pupil(Eye)
#        selected_circle[0]=selected_circle[0]+x_left-5
#        selected_circle[1]=selected_circle[1]+y_left-5
#    elif position == 'right':
#        x_right = shape[36,0]
#        w_right = (shape[39,0]-x_right)
#        y_right = min(shape[37,1],shape[38,1])
#        h_right = (max(shape[41,1],shape[40,1])-y_right)
#        Eye = Image.copy()
#        Eye = Eye[(y_right-5):(y_right+h_right+5),(x_right-5):(x_right+w_right+5)]
#        selected_circle = get_pupil(Eye)
#        selected_circle[0]=selected_circle[0]+x_right-5
#        selected_circle[1]=selected_circle[1]+y_right-5
#        
#        
#    return selected_circle



def save_snaptshot_to_file(image, name):
    #saving image to file :)
    cv2.imwrite(name,image)
    
    
def save_txt_file(file_name,shape,circle_left,circle_right, boundingbox):
    
    #save the file name, landmarks and iris position into a txt file
    
    file_no_ext=file_name[0:-4]
    delimiter = os.path.sep
    temp=file_name.split(delimiter)
    photo_name=temp[-1]
    
    #create temporaty files with the information from the landamarks and 
    #both eyes
    #this piece is a bit weird, it creates three temporary files that are used
    #to create the final file, these files are then eliminated. This is
    #simplest (and easiest) way that i found to do this
    np.savetxt(file_no_ext +'_temp_shape.txt', shape, delimiter=',',
                   fmt='%i', newline='\r')
    
    np.savetxt(file_no_ext + '_temp_circle_left.txt', circle_left, delimiter=',',
                   fmt='%i', newline='\r')
    
    np.savetxt(file_no_ext + '_temp_circle_right.txt', circle_right, delimiter=',',
                   fmt='%i', newline='\r')
    
    np.savetxt(file_no_ext + '_temp_boundingbox.txt', boundingbox, delimiter=',',
                   fmt='%i', newline='\r')
        
    #create a new file that will contain the information, the file will have 
    #the same name as the original picture 
    #if the file exists then remove it -- sorry
    if os.path.isfile(file_no_ext+'.txt'):
        os.remove(file_no_ext + '.txt')           
        
    #now start writing in it
    with open(file_no_ext + '.txt','a') as f:
        #start writing content in the file 
        #(\n indicates new line), (# indicates that the line will be ignored)
        f.write('# File name { \n')
        f.write(photo_name)
        f.write('\n# } \n')
        
        f.write('# 68 facial Landmarks [x,y] { \n')
        with open(file_no_ext +'_temp_shape.txt','r') as temp_f:
            f.write(temp_f.read())
        f.write('# } \n')
            
        f.write('# Left iris [x,y,r] { \n')
        with open(file_no_ext + '_temp_circle_left.txt','r') as temp_f:
            f.write(temp_f.read())
        f.write('# } \n')
            
        f.write('# Right iris [x,y,r] { \n')
        with open(file_no_ext + '_temp_circle_right.txt','r') as temp_f:
            f.write(temp_f.read())
        f.write('# } \n')
            
        f.write('# Face bounding Box [top(x), left(y), width, height] { \n')
        with open(file_no_ext + '_temp_boundingbox.txt','r') as temp_f:
            f.write(temp_f.read())
        f.write('# }')
        
    
    os.remove(file_no_ext +'_temp_shape.txt')
    os.remove(file_no_ext + '_temp_circle_left.txt')
    os.remove(file_no_ext + '_temp_circle_right.txt')
    os.remove(file_no_ext + '_temp_boundingbox.txt')
    
def save_xls_file(file_name, MeasurementsLeft, MeasurementsRight, MeasurementsDeviation, MeasurementsPercentual):
    #saves the facial metrics into a xls file. It works only for a single photo
    
    file_no_ext=file_name[0:-4]
    delimiter = os.path.sep
    temp=file_name.split(delimiter)
    photo_name=temp[-1]
    
    number_of_measurements = 9
    Columns = ['Right','Left','Deviation (absolute)','Deviation (percent)']
    Columns = Columns * number_of_measurements
    
    temp = ['Brow Height', 'Marginal Reflex Distance 1', 'Marginal Reflex Distance 2', 
            'Commisure Excursion', 'Commisure Height Deviation', 'Smile Angle',
            'Upper Lip Height Deviation', 'Dental Show', 'Lower Lip Height Deviation']
    number_of_repetitions=4
    Header = [item for item in temp for i in range(number_of_repetitions)]
    
    
    elements = ['BH', 'MRD1', 'MRD2', 'CE', 'CH', 'SA', 'UVH', 'DS', 'LVH']
    BH = np.array([[MeasurementsRight.BrowHeight,MeasurementsLeft.BrowHeight,MeasurementsDeviation.BrowHeight,MeasurementsPercentual.BrowHeight]],dtype=object)
    MRD1 = np.array([[MeasurementsRight.MarginalReflexDistance1, MeasurementsLeft.MarginalReflexDistance1,MeasurementsDeviation.MarginalReflexDistance1,MeasurementsPercentual.MarginalReflexDistance1]], dtype=object)
    MRD2 = np.array([[MeasurementsRight.MarginalReflexDistance2, MeasurementsLeft.MarginalReflexDistance2,MeasurementsDeviation.MarginalReflexDistance2,MeasurementsPercentual.MarginalReflexDistance2]],dtype=object)
    CE = np.array([[MeasurementsRight.CommissureExcursion, MeasurementsLeft.CommissureExcursion,MeasurementsDeviation.CommissureExcursion,MeasurementsPercentual.CommissureExcursion]],dtype=object)
    CH = np.array([['', '',MeasurementsDeviation.CommisureHeightDeviation,'']],dtype=object)
    SA = np.array([[MeasurementsRight.SmileAngle, MeasurementsLeft.SmileAngle,MeasurementsDeviation.SmileAngle,MeasurementsPercentual.SmileAngle]],dtype=object)
    UVH = np.array([['', '',MeasurementsDeviation.UpperLipHeightDeviation,'']],dtype=object)
    DS = np.array([[MeasurementsRight.DentalShow, MeasurementsLeft.DentalShow,MeasurementsDeviation.DentalShow,MeasurementsPercentual.DentalShow]],dtype=object)
    LVH = np.array([['', '',MeasurementsDeviation.LowerLipHeightDeviation,'']],dtype=object)
    
    
    
    fill=BH
    for i in elements:
        if i is not 'BH':
            fill = np.append(fill, eval(i), axis = 1)
    
    
    
    Index = [photo_name]
    
    
    df = pd.DataFrame(fill, index = Index, columns = Columns)
    df.columns = pd.MultiIndex.from_tuples(list(zip(Header,df.columns)))
    
    
    df.to_excel(file_no_ext+'.xlsx',index = True)
    

def save_xls_file_patient(path,Patient,CalibrationType,CalibrationValue):
    #saves the facial metrics into a xls file. It works only for a patient (two photos)
    
    
    number_of_measurements = 9
    Columns = ['Right','Left','Deviation (absolute)','Deviation (percent)']
    Columns = Columns * number_of_measurements
    
    temp = ['Brow Height', 'Marginal Reflex Distance 1', 'Marginal Reflex Distance 2', 
            'Commisure Excursion', 'Commisure Height Deviation', 'Smile Angle',
            'Upper Lip Height Deviation', 'Dental Show', 'Lower Lip Height Deviation']
    number_of_repetitions=4
    Header = [item for item in temp for i in range(number_of_repetitions)]
    
    elements = ['BH', 'MRD1', 'MRD2', 'CE', 'CH', 'SA', 'UVH', 'DS', 'LVH']
    #first photo
    MeasurementsLeftFirst, MeasurementsRightFirst, MeasurementsDeviation, MeasurementsPercentual = get_measurements_from_data(Patient.FirstPhoto._shape,Patient.FirstPhoto._lefteye,Patient.FirstPhoto._righteye,CalibrationType,CalibrationValue)
    

    BH = np.array([[MeasurementsRightFirst.BrowHeight,MeasurementsLeftFirst.BrowHeight,MeasurementsDeviation.BrowHeight,MeasurementsPercentual.BrowHeight]],dtype=object)
    MRD1 = np.array([[MeasurementsRightFirst.MarginalReflexDistance1, MeasurementsLeftFirst.MarginalReflexDistance1,MeasurementsDeviation.MarginalReflexDistance1,MeasurementsPercentual.MarginalReflexDistance1]], dtype=object)
    MRD2 = np.array([[MeasurementsRightFirst.MarginalReflexDistance2, MeasurementsLeftFirst.MarginalReflexDistance2,MeasurementsDeviation.MarginalReflexDistance2,MeasurementsPercentual.MarginalReflexDistance2]],dtype=object)
    CE = np.array([[MeasurementsRightFirst.CommissureExcursion, MeasurementsLeftFirst.CommissureExcursion,MeasurementsDeviation.CommissureExcursion,MeasurementsPercentual.CommissureExcursion]],dtype=object)
    CH = np.array([['', '',MeasurementsDeviation.CommisureHeightDeviation,'']],dtype=object)
    SA = np.array([[MeasurementsRightFirst.SmileAngle, MeasurementsLeftFirst.SmileAngle,MeasurementsDeviation.SmileAngle,MeasurementsPercentual.SmileAngle]],dtype=object)
    UVH = np.array([['', '',MeasurementsDeviation.UpperLipHeightDeviation,'']],dtype=object)
    DS = np.array([[MeasurementsRightFirst.DentalShow, MeasurementsLeftFirst.DentalShow,MeasurementsDeviation.DentalShow,MeasurementsPercentual.DentalShow]],dtype=object)
    LVH = np.array([['', '',MeasurementsDeviation.LowerLipHeightDeviation,'']],dtype=object)
        
    fillFirst=BH
    for i in elements:
        if i is not 'BH':
            fillFirst = np.append(fillFirst, eval(i), axis = 1)
      
    #Second photo
    MeasurementsLeftSecond, MeasurementsRightSecond, MeasurementsDeviation, MeasurementsPercentual = get_measurements_from_data(Patient.SecondPhoto._shape,Patient.SecondPhoto._lefteye,Patient.SecondPhoto._righteye,CalibrationType,CalibrationValue)

    BH = np.array([[MeasurementsRightSecond.BrowHeight,MeasurementsLeftSecond.BrowHeight,MeasurementsDeviation.BrowHeight,MeasurementsPercentual.BrowHeight]],dtype=object)
    MRD1 = np.array([[MeasurementsRightSecond.MarginalReflexDistance1, MeasurementsLeftSecond.MarginalReflexDistance1,MeasurementsDeviation.MarginalReflexDistance1,MeasurementsPercentual.MarginalReflexDistance1]], dtype=object)
    MRD2 = np.array([[MeasurementsRightSecond.MarginalReflexDistance2, MeasurementsLeftSecond.MarginalReflexDistance2,MeasurementsDeviation.MarginalReflexDistance2,MeasurementsPercentual.MarginalReflexDistance2]],dtype=object)
    CE = np.array([[MeasurementsRightSecond.CommissureExcursion, MeasurementsLeftSecond.CommissureExcursion,MeasurementsDeviation.CommissureExcursion,MeasurementsPercentual.CommissureExcursion]],dtype=object)
    CH = np.array([['', '',MeasurementsDeviation.CommisureHeightDeviation,'']],dtype=object)
    SA = np.array([[MeasurementsRightSecond.SmileAngle, MeasurementsLeftSecond.SmileAngle,MeasurementsDeviation.SmileAngle,MeasurementsPercentual.SmileAngle]],dtype=object)
    UVH = np.array([['', '',MeasurementsDeviation.UpperLipHeightDeviation,'']],dtype=object)
    DS = np.array([[MeasurementsRightSecond.DentalShow, MeasurementsLeftSecond.DentalShow,MeasurementsDeviation.DentalShow,MeasurementsPercentual.DentalShow]],dtype=object)
    LVH = np.array([['', '',MeasurementsDeviation.LowerLipHeightDeviation,'']],dtype=object)
        
    fillSecond=BH
    for i in elements:
        if i is not 'BH':
            fillSecond = np.append(fillSecond, eval(i), axis = 1)
    
    #difference       
    BH = np.array([[MeasurementsRightFirst.BrowHeight-MeasurementsRightSecond.BrowHeight,MeasurementsLeftFirst.BrowHeight-MeasurementsLeftSecond.BrowHeight,'','']],dtype=object)
    MRD1 = np.array([[MeasurementsRightFirst.MarginalReflexDistance1-MeasurementsRightSecond.MarginalReflexDistance1, MeasurementsLeftFirst.MarginalReflexDistance1-MeasurementsLeftSecond.MarginalReflexDistance1,'','']], dtype=object)
    MRD2 = np.array([[MeasurementsRightFirst.MarginalReflexDistance2-MeasurementsRightSecond.MarginalReflexDistance2, MeasurementsLeftFirst.MarginalReflexDistance2-MeasurementsLeftSecond.MarginalReflexDistance2,'','']],dtype=object)
    CE = np.array([[MeasurementsRightFirst.CommissureExcursion-MeasurementsRightSecond.CommissureExcursion,MeasurementsLeftFirst.CommissureExcursion-MeasurementsLeftSecond.CommissureExcursion,'','']],dtype=object)
    CH = np.array([['', '','','']],dtype=object)
    SA = np.array([[MeasurementsRightFirst.SmileAngle-MeasurementsRightSecond.SmileAngle, MeasurementsLeftFirst.SmileAngle-MeasurementsLeftSecond.SmileAngle,'','']],dtype=object)
    UVH = np.array([['', '','','']],dtype=object)
    DS = np.array([[MeasurementsRightFirst.DentalShow-MeasurementsRightSecond.DentalShow,MeasurementsLeftFirst.DentalShow-MeasurementsLeftSecond.DentalShow,'','']],dtype=object)
    LVH = np.array([['', '','','']],dtype=object)
        
    fillDifference=BH
    for i in elements:
        if i is not 'BH':
            fillDifference = np.append(fillDifference, eval(i), axis = 1)
    
  

    Index = [Patient.FirstPhoto._ID, Patient.SecondPhoto._ID, 'Difference']

    df = pd.DataFrame(np.vstack((fillFirst, fillSecond, fillDifference)), index = Index, columns = Columns)
    df.columns = pd.MultiIndex.from_tuples(list(zip(Header,df.columns)))
    

    
    delimiter = os.path.sep
    temp=path.split(delimiter)
    path=temp[:-1]
    path=delimiter.join(path)

    file_name = path + delimiter + Patient.patient_ID +'.xlsx'
   
    df.to_excel(file_name,index = True)