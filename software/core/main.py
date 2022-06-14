# import sensor
import imp
import re
from time import sleep
import numpy as np 
import os
import cnn.API_CNN as cnn 
import sensor
import arm_communication.arduino_serial as arduino_serial
import os 

# 0 camera du pc
# 1 webcam du bras

path = os.path.dirname(__file__)

arm_moving = False
end_option  = False 
objet_value = 0
def fonction1():
    print("fonction 1 appeler ")
    test = arduino_serial.send("1")
def fonction2():
    test = arduino_serial.send("2")
    print("fonction 2 appeler ")
def fonction3():
    test = arduino_serial.send("3")
    print("fonction 3 appeler ")


emotional_vector = {0: "Angry", 1: "Disgusted", 2: "Fearful", 3: "Happy", 4: "Neutral", 5: "Sad", 6: "Surprised"}
emotion_to_action = {0:-3,1:-1,2:-2,3:3,4:0,5:-1,6:2}
object_vector = [,232]
val_objet = [-2,2]
last_emotional_state = 0 
cpt =  0
fonctionActivation = np.array([-2,2])
get_action  = {0:"fonction2",1:"fonction3"}
end_option = False
''' mock variable '''
emotional_vector_mock = np.random.randint(0,6)

''' mock fonction'''
def cnn_mock(vision):
    return emotional_vector_mock

 
def arm_mock(action):
    return False

def emotionUpdate(last_emotional_state,received_emotion,action):
    #TODO  clarification de la méthode de calcul 
    if( last_emotional_state != -1  and received_emotion !=- 1):
        diff = emotion_to_action[last_emotional_state] - emotion_to_action[received_emotion]
        fonctionActivation[action] += diff

def chooseAction(recevied_emotion):
    val = emotion_to_action.get(recevied_emotion) or emotion_to_action[ 
      min(emotion_to_action.keys(), key = lambda key: abs(key-recevied_emotion))]
    return val 

def checkobjet():
    pass

def checkArmMoving():
    if arduino_serial.getwaiting()>0:
            read = arduino_serial.read()
            if read =="end\n" :
                global arm_moving
                arm_moving =  False
            if read == "stop\n":
                global objet_value
                objet_value = checkobjet()

def doARM(val):
    difference_array = np.abs(fonctionActivation-val)
    print(difference_array)
    index = difference_array.argmin()
    print(index)
    globals()[get_action[index]]()
    
    return index

def checkSound(energy):
    if energy > 1400 :
        return True
    return False 
''' main boucle 
'''
logger = open(path+"/logger/programmeExecution.txt", "w")
video2 = sensor.VideoCapture(1)
video = sensor.VideoCapture(0)
sound = sensor.SoundCapture()
energy =  0
print("début du main ")
logger.write("start of execution \n")


# action_cpt = 0
while (1):
    # print("action  : ",action_cpt) 
   # energy =sound.capture()
    logger.write("sound recuperation \n")

    #end_option = checkSound(energy)
    
    received_emotion = cnn.EmotionDetection(video.video)  
    logger.write("cnn utilisation \n") 
    if received_emotion !=- 1 :
        emotional_val = chooseAction(received_emotion)

        logger.write("emotional values checking "+emotional_vector[received_emotion]+" \n") 
        action = doARM(emotional_val)
        
        arm_moving = True
        last_emotional_state = received_emotion
        emotion_modified = False
        logger.write("arm function talking \n")  
        while(arm_moving):
            received_emotion = cnn.EmotionDetection(video.video)
            if emotion_modified is False:
                if last_emotional_state != received_emotion and received_emotion != -1 :
                    print(" nouvelle emotion reçu : ",emotional_vector[received_emotion])
                    emotionUpdate(last_emotional_state,received_emotion,action)
                    logger.write(("emotion status update"+emotional_vector[received_emotion]+" \n"))
                    emotion_modified = True
            checkArmMoving()
        print("end arm moving ")

    if (end_option):
        logger.write(" end of execution")
        break


print("fin de la simulation")