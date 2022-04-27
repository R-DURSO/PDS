# import sensor
import numpy as np 
arm_moving = False
end_option  = False 
# TODO a modifier fonction 1 a 3 quand elle seront disponible poour modifier le bras 
def fonction1():
    print("fonction 1 appeler ")
def fonction2():
    print("fonction 2 appeler ")
def fonction3():
    print("fonction 3 appeler ")
emotional_vector = {0: "Angry", 1: "Disgusted", 2: "Fearful", 3: "Happy", 4: "Neutral", 5: "Sad", 6: "Surprised"}
emotion_to_action = {0:-3,1:-1,2:-2,3:3,4:0,5:-1,6:2}
object_vector = []
last_emotional_state = 0 
cpt =  0
fonctionActivation = np.array([-2,0,2])
get_action  = {0:"fonction1",1:"fonction2",2:"fonction3"}
''' mock variable '''
emotional_vector_mock = {}

''' mock fonction'''
def cnn_mock(vision):
    return emotional_vector_mock

 
def arm_mock(action):
    return False

def emotionUpdate(last_emotional_state,received_emotion,action):
    diff = emotion_to_action[last_emotional_state] - emotion_to_action[received_emotion]
    print(diff)
    fonctionActivation[action] += diff

def chooseAction(recevied_emotion):
    val = emotion_to_action.get(recevied_emotion) or emotion_to_action[ 
      min(emotion_to_action.keys(), key = lambda key: abs(key-recevied_emotion))]
    return val 

def checkArmMoving():
    return None 

def doARM(val):
    difference_array = np.abs(fonctionActivation-val)
    index = difference_array.argmin()
    globals()[get_action[index]]()
    
    return index

def checkSound(Sound):
    pass

''' main boucle 
'''
# video = sensor.VideoCapture()
# sound = sensor.SoundCapture()
# while (1):
#     #TODO mode aquisition des données =>  CNN => sortie du vecteur => action du bras 
#     frame = video.view()
#     # TODO faire le check up si le son es trop fort alors on arrête tout 
#     sound =sound.capture()
#     checkSound(sound)
#     received_emotion = cnn_mock(frame)  # on remplacera par le cnn 
#     # mise en fonction de la boucle 
#     emotional_val = chooseAction(received_emotion)
#     action = doARM(emotional_val)
#     arm_moving = True
#     last_emotional_state = received_emotion
#     emotion_modified = False 
#     while(arm_moving):
#         frame = video.view()
#         received_emotion = cnn_mock(frame) 
#         if emotion_modified == False:
#             if last_emotional_state != received_emotion:
#                 emotionUpdate(last_emotional_state,received_emotion,action)
#                 # checkArmMoving()
#                 arm_mock()
#                 emotion_modified = True
#         checkArmMoving()
#     if (not end_option):
#         break
'''' idée : 
 - principe de log 
    principe de sauvegarde d'axtion de la dernière interaction'''


'''  le CNN retourne le chiffre '''

def modificationValEm():
    print(fonctionActivation)
    val = chooseAction(3)
    print(val)
    val = doARM(val)
    print(val)
    emotionUpdate(1,3,2)
    print(fonctionActivation)
    val = chooseAction(3)
    print(val)
    val = doARM(val)
    print(val)

modificationValEm()
