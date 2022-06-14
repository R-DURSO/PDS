from time import sleep
from tracemalloc import start
from turtle import st
import cv2 as cv
import pyaudio as pa 
import numpy as np
import math
# image settings 
IMG_WIDTH = 320
IMG_HEIGHT = 240

# voice settings 
CHUNK = 1420
FORMAT = pa.paInt16
RECORD_SECONDS = 5
RATE=44100
INPUT =  0

# cv.useOptimized()

class VideoCapture():

    def __init__(self,x):
        self.etat = True
        self.frameSize = (320,240)
        self.video = cv.VideoCapture(x,cv.CAP_DSHOW)
        self.greyscale = None
        self.frame = None
        self.ret = None
    def getFrame(self):
        return self.frame
    def getGreyscale(self):
        return self.greyscale
    def view(self):
            self.ret , self.frame = self.video.read()
            self.greyscale =  cv.cvtColor(self.frame, cv.COLOR_BGR2GRAY)
            cv.imshow("output",self.frame) 
            cv.waitKey(1)
    def stop(self):
        self.video.release()
class SoundCapture():
    def __init__(self) :
        self.etat = True
        self.energy = 0
        self.p = pa.PyAudio()
        info = self.p.get_host_api_info_by_index(0)
        numdevices = info.get('deviceCount')
        # we define the current channel of webcam sound 
        for i in range(0, numdevices):
            if (self.p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
                if("Microphone (USB Audio Device)"== self.p.get_device_info_by_host_api_device_index(0, i).get('name')):
                    INPUT = i
        # création du flux 
        # sound capture
        self.stream= self.p.open(format=FORMAT, channels=INPUT, rate=RATE, input=True, frames_per_buffer=CHUNK, input_device_index=INPUT)

        '''TODO faire que un son fort ne fait pas de math domain error , feature ne doit pas contenir de nombre négatif 
        si on son est trop fort alors le minimal de feature et inf a -5k'''
    def capture(self) : 

            data = self.stream.read(CHUNK, exception_on_overflow = False)      
            feature = np.fromstring(data, dtype=np.int16) #feature =! 1024
                                       #conversion in int
            self.energy = math.sqrt(np.sum(np.square(feature, dtype=np.int32))/len(feature))    #calculate energies
            # print(self.energy)
            return self.energy
    def getEnergy(self):
        return self.energy
    def stop(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()

