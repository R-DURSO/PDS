import pyaudio
import wave
import numpy as np
import math

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RECORD_SECONDS = 5
RATE=44100
WAVE_OUTPUT_FILENAME = "voice.wav"
INPUT_DEVICE_INDEX = 1            # Device dependant

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK, input_device_index=1)

print("Recording...")

frames = []
  
for t in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
                     #read the audio source
    data = stream.read(CHUNK, exception_on_overflow = False)   
    feature = np.fromstring(data, dtype=np.int16) #feature =! 1024
                                       #conversion in int
    feature = math.sqrt(np.sum(np.square(feature, dtype=np.int32))/len(feature))    #calculate energies
    print("energy : ", feature)

print("Done")

# Stop
stream.stop_stream()
stream.close()

p.terminate()