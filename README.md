# Emotrics
Software to autmatically compute facial metrics in unilateral facial paralysis

Emotrics is a python (PyQt5) based application developed to facilitate the estimation of facial measurements in photographs. 

Emotrics works by automatically placing a set of 68 facial landmarks in photographs, the position of the landmarks can be easily adjusted to improve accuracy. Emotrics uses the landmarks to estimate a set of facial metrics that might be used for assessment of facial symmetry and function. 
Moreover, Emotrics can be compare metrics from two photographs of the same subject taken at different time points. 

If you use this code, please cite:
- Guarin, D. L., Dusseldorp, J., Hadlock, T. A., & Jowett, N. (2018). A machine learning approach for automated facial measurements in facial palsy. JAMA facial plastic surgery, 20(4), 335-337.

Emotrics has been used in many research studies, here are some examples:
- Greene, J. J., Tavares, J., Guarin, D. L., & Hadlock, T. (2019). Clinician and automated assessments of facial function following eyelid weight placement. JAMA facial plastic surgery, 21(5), 387-392.
- Greene, J. J., Tavares, J., Mohan, S., Jowett, N., & Hadlock, T. (2018). Long-term outcomes of free gracilis muscle transfer for smile reanimation in children. The Journal of pediatrics, 202, 279-284.
- Dusseldorp, J. R., van Veen, M. M., Guarin, D. L., Quatela, O., Jowett, N., & Hadlock, T. A. (2019). Spontaneity assessment in dually innervated gracilis smile reanimation surgery. JAMA facial plastic surgery, 21(6), 551-557.
- Guntinas-Lichius, O., Silver, C. E., Thielker, J., Bernal-Sprekelsen, M., Bradford, C. R., De Bree, R., ... & Ferlito, A. (2018). Management of the facial nerve in parotid cancer: preservation or resection and reconstruction. European Archives of Oto-rhino-laryngology, 275(11), 2615-2626.
- Perez, P. B., Gunter, A. E., Moody, M. P., Vincent, A. G., Perez, C. R., Serra, R. M., & Hohman, M. H. (2021). Investigating Long-Term Brow Stabilization by Endotine-Assisted Endoscopic Brow Lift with Concomitant Upper Lid Blepharoplasty. Annals of Otology, Rhinology & Laryngology, 0003489421997653.

## How to use Emotrics
### Tutorial
A video tutorial of Emotris is avaliable online 

Full tutoria can be found here: https://www.youtube.com/watch?v=PqXcu_WxaY0

A short tutorial can be found here: https://www.youtube.com/watch?v=LBJu-3ZmV2c


## How obtain Emotrics

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

### Executable files:
Alternatively, you can download an .exe file and run Emotrics without any additional installation. 

A Windows 64-bit version of Emotrics can be obtained here:
https://myfiles.meei.harvard.edu/users/hilll/Jowett-Nate/Emotrics.zip?ticket=t_fkYWvlVo

(this application won't work on windows 32-bit, there is not plan to generate a workable 32-bit app, if you are running a 32-bit machine you should use Emotrics via source code). 

Currently there is no updated version of Emotrics for Mac or Linux. 

Instructions (for Windows):
Download the .zip file and unzip it. This will create a folder called Emotrics, localize the executable file Emotrics.exe. Double click on it and the app should start. Depending on your computer this can take up to a minute.  

