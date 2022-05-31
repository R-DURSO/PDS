import cv2 as cv


# image settings 
IMG_WIDTH = 320
IMG_HEIGHT = 240

frameSize = (320,240)
video = cv.VideoCapture(1,cv.CAP_DSHOW)
ret, frame = video.read()
cv.imshow("output",frame) 
cv.waitKey(0)
input()
