from time import sleep
from tracemalloc import start
import cv2 as cv
import pyaudio as pa 
import numpy as np
import math
import threading
import time
# image settings 
IMG_WIDTH = 320
IMG_HEIGHT = 240

# voice settings 
CHUNK = 1024
FORMAT = pa.paInt16
RECORD_SECONDS = 5
RATE=44100
INPUT =  0

# the thead will be used 
global video_thread  
global sound_thread  
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



class SoundCapture():
    def __init__(self) :
        self.open = True
        self.energy = 0
        p = pa.PyAudio()
        info = p.get_host_api_info_by_index(0)
        numdevices = info.get('deviceCount')
        # we define the current channel of webcam sound 
        for i in range(0, numdevices):
            if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
                if("Microphone (USB Audio Device)"== p.get_device_info_by_host_api_device_index(0, i).get('name')):
                    INPUT = i
        # création du flux 
        # sound capture
        self.stream= p.open(format=FORMAT, channels=INPUT, rate=RATE, input=True, frames_per_buffer=CHUNK, input_device_index=INPUT)
    def capture(self) : 
                          #read the audio source
        while(self.open == True):
            data = self.stream.read(CHUNK, exception_on_overflow = False)      
            feature = np.fromstring(data, dtype=np.int16) #feature =! 1024
                                       #conversion in int
            self.energy = math.sqrt(np.sum(np.square(feature, dtype=np.int32))/len(feature))    #calculate energies
    def stop(self):
        if self.open==True:  
            self.open=False
        else: 
            pass
    def getEnergy(self):
        return self.energy
    def start(self):
        sound_thread = threading.Thread(target=self.capture)
        sound_thread.start()

# TODO le traitement du sont de l'image sera fait ici 
class analyse():
    def __init__(self):
        self.open = True
    def getData(self):
        # print(video_thread.getFrame())
        print(sound_thread.getEnergy())
        # time.sleep(10)
        self.open = True
    
    def recuperation(self):
        while(self.open == True):
            self.getData()
    def stop(self):
        if self.open==True:  
            self.open=False
        else: 
            pass
    def start(self):
        analyse_thread = threading.Thread(target=self.recuperation)
        analyse_thread.start()

it = 0 
while (it  < 10):
    # video_thread = VideoCapture()
    # video_thread.start()
    sound_thread = SoundCapture()
    sound_thread.start()
    analyse_thread = analyse()
    analyse_thread.start()
    it += 1 
sound_thread.stop()
analyse_thread.stop()