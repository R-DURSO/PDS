# import sensor
import imp
from time import sleep
import numpy as np 
import os
import cnn.API_CNN as cnn 
import sensor
import arm_communication.arduino_serial as arduino_serial
import os 



path = os.path.dirname(__file__)

arm_moving = False
end_option  = False 
# TODO a modifier fonction 1 a 3 quand elle seront disponible poour modifier le bras 
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
object_vector = []
last_emotional_state = 0 
cpt =  0
fonctionActivation = np.array([-2,0,2])
get_action  = {0:"fonction1",1:"fonction2",2:"fonction3"}
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

def checkArmMoving():
    return False 

def doARM(val):
    difference_array = np.abs(fonctionActivation-val)
    index = difference_array.argmin()
    # robotsave.write(get_action[index])
    globals()[get_action[index]]()
    
    return index

def checkSound(energy):
    if energy > 1400 :
        return True
    return False 
''' main boucle 
'''
logger = open(path+"/logger/programmeExecution.txt", "w")
# robotsave = open(path+"/logger/robotAction.txt", "w")
video = sensor.VideoCapture()
sound = sensor.SoundCapture()
energy =  0
print("début du main ")
logger.write("start of execution \n")


action_cpt = 0
while (1):
    print("action  : ",action_cpt)
    # TODO faire le check up si le son es trop fort alors on arrête tout 
   # energy =sound.capture()
    print(energy)
    # le print vient de la classe sensor 
    logger.write("sound recuperation \n")

    #end_option = checkSound(energy)
    
    received_emotion = cnn.EmotionDetection(video.video)  
    logger.write("cnn utilisation \n") 
    # mise en fonction de la boucle 
    if received_emotion !=- 1 :
        # robotsave.write("emotion reçu : ",emotional_vector[received_emotion])
        emotional_val = chooseAction(received_emotion)

        logger.write("emotional values checking \n") 
        action = doARM(emotional_val)
        logger.write("arm function talking \n") 
        
        arm_moving = True
        last_emotional_state = received_emotion
        emotion_modified = False 
        while(arm_moving):
            received_emotion = cnn.EmotionDetection(video.video)
            if emotion_modified is False:
                if last_emotional_state != received_emotion and received_emotion != -1 :
                    print(" nouvelle emotion reçu : ",emotional_vector[received_emotion])
                    emotionUpdate(last_emotional_state,received_emotion,action)
                    logger.write("emotion status update")
                    # checkArmMoving()
                    emotion_modified = True
                    arm_moving = checkArmMoving()


    if (end_option):
        logger.write(" end of execution")
        break
    action_cpt = action_cpt + 1 


print("fin de la simulation")