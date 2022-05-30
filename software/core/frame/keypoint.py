import re
import cv2 as cv
import numpy as np 
import matplotlib.pyplot as plt
import os 
import scipy.signal as sp
import scipy.ndimage
path = os.path.dirname(__file__)
# BGR color 
# frame = cv.imread( path + "/carre.pgm")
frame = cv.imread( path + "/rond.png")


seuil = 40 

def binarisation(frame):
    greyFrame = np.zeros((len(frame),len(frame[0])))
    for i in range(len(frame)):
        for j in range(len(frame[0])):
            if (sum(frame[i][j]) / 255) > 20:
                greyFrame[i][j] == 255
            else:
                greyFrame[i,j] = 0

    return greyFrame

def gaussianBlur(frame):
    gaussianFilter = np.array( ([1/16,2/16,1/16],[2/16,4/16,2/16],[1/16,2/16,1/16])) 
    frame = sp.convolve2d(frame,gaussianFilter) 
    return frame

frame = binarisation(frame)
frame = scipy.ndimage.median_filter(frame,size=10)
filterX = np.array( ([-1,0,1],[-2,0,2],[-1,0,1])) 
filterY = np.array( ([-1,-2,-1],[0,0,0],[1,2,1])) 
mask = np.array( ([1,1,1],[1,0,1],[1,1,1]))
# frame = gaussianBlur(frame)
gaussianFilter = np.array( ([1/16,2/16,1/16],[2/16,4/16,2/16],[1/16,2/16,1/16])) 
frameX = sp.convolve2d(frame,filterX,mode="same") 
frameXmasked = sp.convolve2d(frameX,mask,mode="same") 
frameY = sp.convolve2d(frame,filterY,mode="same") 
frameYmasked = sp.convolve2d(frameY,mask,mode="same") 
frameXY =frameX * frameY
frameXYmasked = sp.convolve2d(frameXY,mask,mode="same")
framemax = frameX**2 *frameYmasked**2 + frameY**2*frameXmasked**2 - 2 * frameXY*frameXYmasked
# framemax = frameYmasked*frameYmasked*frameXmasked*frameXmasked - frameXY - 0.05 * (frameXmasked**2 + frameYmasked**2)**2
framemax = framemax / (frameYmasked*frameYmasked + frameXmasked*frameXmasked)
# cv.imshow("greyscaleX", frameXmasked)
# cv.imshow("greyscaleY", frameYmasked)
# cv.imshow("greyscaleXY", frameXYmasked)
cv.imshow("test", framemax)
cv.waitKey(0)
