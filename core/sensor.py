from time import sleep
from tracemalloc import start
import cv2 as cv
import pyaudio as pa 
import numpy as np
import math
import threading
# image settings 
IMG_WIDTH = 320
IMG_HEIGHT = 240

# voice settings 
CHUNK = 1024
FORMAT = pa.paInt16
CHANNELS = 2 
RECORD_SECONDS = 5
RATE=44100
INPUT_DEVICE_INDEX = 4 

# the thead will be used 
global video_thread  
global sound_Thread  
global analyse_thread 
class VideoCapture():

    def __init__(self):
        self.open = True
        self.frameSize = (320,240)
        self.video = cv.VideoCapture(0)
        self.greyscale = None
        self.frame = None
    
    def stop(self):
        if self.open==True:
                    
            self.open=False
            self.video_out.release()
            self.video_cap.release()
            cv.destroyAllWindows()         
        else: 
            pass
    def getFrame(self):
        return self.frame
    def getGreyscale(self):
        return self.greyscale
    
    def view(self):
        while (self.open == True):
            ret , self.frame = self.video.read()
            self.greyscale =  cv.cvtColor(self.frame, cv.COLOR_BGR2GRAY)
            cv.imshow("output",self.frame) 
            cv.waitKey(1)
        # Launches the video function using a thread
    def start(self):
        video_thread = threading.Thread(target=self.view)
        video_thread.start()

class analyse():
    def getData(self):
        print(video_thread)
    
    def recuperation(self):
        while(1):
            self.getData()

    def start(self):
        analyse_thread = threading.Thread(target=self.recuperation)
        analyse_thread.start()

# # Video capture and processing
# cap = cv.VideoCapture(0)
# cap.set(cv.CAP_PROP_FRAME_WIDTH, IMG_WIDTH)    # Set lower resolution
# cap.set(cv.CAP_PROP_FRAME_HEIGHT, IMG_HEIGHT)  # for faster capture

# # audio capture
# p = pa.PyAudio()
# stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK, input_device_index=4)
# #prepare the output of camera 
# cv.namedWindow("output",cv.WINDOW_NORMAL)
# cv.moveWindow("output",200,200)

# TODO condition de sortie a définir 
# while(1):
#     # image capture
#     ret , frame = cap.read()
    # cv.imshow("output",frame) 
    # cv.waitKey(1)
#     greyscale =  cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
#     # sound capture
#     data = stream.read(CHUNK, exception_on_overflow = False)                        #read the audio source
#     feature = np.fromstring(data, dtype=np.int16) #feature =! 1024
#                                        #conversion in int
#     feature = math.sqrt(np.sum(np.square(feature, dtype=np.int32))/len(feature))    #calculate energies
#     print("energy : ", feature)

video_thread = VideoCapture()
video_thread.start()
analyse_thread = analyse()
analyse_thread.start()
