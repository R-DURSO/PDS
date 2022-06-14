import cv2 as cv
import numpy as np 
import matplotlib.pyplot as plt
import os 
import scipy.signal as sp
import scipy.ndimage
import math
path = os.path.dirname(__file__)
seuil = 30 
def getdistance(frame):
    ddepth = cv.CV_64F
    greyscale = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    ret, frame = cv.threshold(greyscale, 30, 255, cv.THRESH_BINARY_INV)
    sobel = cv.Sobel(frame, ddepth, 1, 1, ksize=3)

    xstart = 100000
    ystart = 100000
    xend = 0
    yend = 0

    for i in range(2,sobel.shape[0]):
        for j in range(2,sobel.shape[1]):
            if math.isclose(sobel[i][j],255):
                if xend <i :
                    xend = i
                if yend <j :
                    yend = j
                if xstart >i :
                    xstart = i
                if ystart > j :
                    ystart = j


    # print(xend," :x end \n")
    # print(yend," : y end \n")
    # print(xstart," : x start \n")
    # print(ystart," : y start \n")
    dist = math.dist([ystart,xstart],[yend,xend])
    return dist


# frame = cv.imread(path+"/pyramide.jpg")
# # frame = cv.imread(path+"/test_final.jpg")
# frame = cv.resize(frame,(320,240))
# cv.imshow("frame",frame)
# cv.waitKey(0)
# dist  = getdistance(frame)
# print(dist)