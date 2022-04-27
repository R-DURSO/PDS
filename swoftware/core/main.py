import sensor
import numpy as np 
arm_moving = False
end_option  = False 
emotional_vector = []
emotional_vector_mock =[0,0,0,1,0,0,0]
last_emotional_state = 0 
cpt =  0


''' mock fonction'''
def cnn_mock(vision):
    return emotional_vector_mock

 
def arm_mock(action):
    return False

def emotionUpdate():
    return None
def checkArmMoving():
    return None 

def doARM():
    return None
''' main boucle 
'''
video = sensor.VideoCapture()
sound = sensor.SoundCapture()
while (1):
    #TODO mode aquisition des données =>  CNN => sortie du vecteur => action du bras 
    frame = video.view()
    # TODO faire le check up si le son es trop fort alors on arrête tout 
    sound =sound.capture()

    received_emotion = cnn_mock(frame)  # on remplacera par le cnn 
    # mise en fonction de la boucle 
    action = 1
    arm_moving = True
    # doArm(action)
    last_emotional_state = received_emotion
    # TODO 
    emotion_modified = False
    while(arm_moving):
    #TODO aquisition => CNN => maj emotinal vector
        frame = video.view()
        received_emotion = cnn_mock(frame) 
        if emotion_modified == False:
            if last_emotional_state != received_emotion:
                emotionUpdate(last_emotional_state,received_emotion,action)
                # checkArmMoving()
                arm_mock()
                emotion_modified = True
        else : 
            #checkArmMoving()
            arm_mock()
            continue
    if (not end_option):
        break;

'''' idée : 
 - principe de log 
    principe de sauvegarde d'axtion de la dernière interaction'''