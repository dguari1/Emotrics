# Emotrics
Software to autmatically compute facial metrics in unilateral facial paralysis

Emotrics is a python (PyQt5) based application developed to facilitate the estimation of facial measurements in photographs. 
Emotrics works by automatically placing a 68 facial landmarks and using the position of those landmarks to 
estimate a set of facial measurements that can be used to asses facial symmetry and/or evaluate facial neurumuscular diseases. 
Moreover, results can be used to compare pre and post-procedure photographs to asses the effectiveness of treatment. 

Required packages:
- dlib 
- OpenCV 

Video tutorials can be found in ./Tutorial

Executing the code:
Download and install python (I used 3.6), I recomend to install anaconda (https://www.anaconda.com/download/) and use Spider to edit and excute the code. Once conda is installed you can add anaconda to your enviromental variables (in windows) and excute the following commands in the command line (cmd)

- conda install -c menpo opencv3 
- conda install -c menpo dlib

this will allow you to use openCV and dlib in your python installation. There are ways to compile your own version of dlib and OpenCV, google is your friend. However, this is not necesary to use Emotrics. 
Finally, clone this repository and execute Emotrics.py, this will open the Emotric's Graphical User Interface and allows you to use the software. 

Executable files:
Alternatively, you can download an .exe file and run Emotrics without any additional installation. 

Windows 64-bit version of Emotrics can be obtained here:
https://myfiles.meei.harvard.edu/users/hilll/Jowett-Nate/Emotrics.zip?ticket=t_fkYWvlVo

(this application won't work on windows 32-bit, there is not plan to generate a workable 32-bit app, if you are running a 32-bit machine you would need to use Emotrics via source code). 

Currently there is no updated version of Emotrics for Mac or Linux. 

Instructions (for Windows):
Download the .zip file and unzip it. This will create a folder called Emotrics, localize the executable file Emotrics.exe. Double click on it and the app should start. Depending on your computer this can take up to a minute.  




If you use this software please cite the following paper:

Guarin, Diego L., Joseph Dusseldorp, Tessa A. Hadlock, and Nate Jowett. "A machine learning approach for automated facial measurements in facial palsy." JAMA facial plastic surgery (2018).
