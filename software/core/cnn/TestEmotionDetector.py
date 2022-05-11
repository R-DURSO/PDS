import cv2
import API_CNN
import numpy as np
from keras.models import model_from_json
import os

emotion_dict = {0: "Angry", 1: "Disgusted", 2: "Fearful", 3: "Happy", 4: "Neutral", 5: "Sad", 6: "Surprised"}
path = os.path.dirname(__file__)
print(path)

# load json and create model
json_file = open(path + '/model/emotion_model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
emotion_model = model_from_json(loaded_model_json)
# load weights into new model
emotion_model.load_weights(path + "/model/emotion_model.h5")

# start the webcam feed
cap = cv2.VideoCapture(0)

# absolute video path for testing
cap = cv2.VideoCapture(path+"/video/emotion_test.mp4")

while True:
    emotionKey = API_CNN.EmotionDetection(cap, cv2, emotion_model, path, emotion_dict)
    print(emotionKey)
cap.release()
cv2.destroyAllWindows()
