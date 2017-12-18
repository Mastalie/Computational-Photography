import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import subprocess
# import skimage
# import skimage.io as imio
# import skimage.transform as trans
# from skimage.viewer import ImageViewer
import glob
import re
import os
# import skimage.filters as filters
from time import gmtime, strftime, sleep
from scipy import interpolate as interp
# %matplotlib inline

mpl.rcParams['figure.figsize'] = (16.0, 8.0)

def grabImage(sid=1, imres=8, fm=1, cameraNumber=6):
    # I will use the file name dbGrab.... for the image grabbed from the camera. First step is to get rid of previously grabbed images
    cmdA='ssh ubuntu@10.0.1.'+str(cameraNumber)
    cmdB='scp ubuntu@10.0.1.'+str(cameraNumber)
    subprocess.run('rm dbGrab*', \
                   stdout=subprocess.PIPE, shell=True)
    subprocess.run('rm *raw', \
                   stdout=subprocess.PIPE, shell=True)
    #subprocess.run(cmdA+' "rm dbGrab*"', \
    #               stdout=subprocess.PIPE, shell=True)
    #subprocess.run(cmdA+' "rm *.raw"', \
    #              stdout=subprocess.PIPE, shell=True)
    # ok, now let's grab an image on the tegra
    cmD=cmdA+' "nvgstcapture-1.0 -m 1 --sensor-id '+str(sid)+' -A --capture-auto 1 --dump-bayer\
                    --file-name dbGrab --image-res '+ str(imres)+'"'
    subprocess.run(cmD, stdout=subprocess.PIPE, shell=True)
    subprocess.run(cmdB+':dbGrab* ./sample', \
                   stdout=subprocess.PIPE, shell=True)
    subprocess.run(cmdB+':*.raw ./sample', \
                   stdout=subprocess.PIPE, shell=True)
    #ok, now let's find the file name of the image we just grabbed and transfered
    pop=subprocess.run('ls',stdout=subprocess.PIPE, shell=True)
    rePop=pop.stdout
    rePop=rePop.decode("utf-8")
    if fm==1:
        fileName = re.search(r'dbGrab(.*).jpg', rePop)
        fileName=fileName.group()
        pop=plt.imread(fileName)
    else:
        fileName = re.search(r'(.*).raw', rePop)
        fileName=fileName.group()
        pop=np.fromfile(fileName,dtype=np.dtype('i2'))
        pop=pop[250416:]
        pop=np.reshape(pop,(2174,3864))
       # pop=np.append(pop[:,2060:] ,pop[:,:2060],axis=1)
    return pop