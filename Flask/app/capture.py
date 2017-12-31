import cv2
import numpy as np
from camera import VideoCamera
from classifier import Classifier

class Capture(object):
    def __init__(self):
        self.cap = VideoCamera()
        self.classifier = Classifier()
        self.face_classifier = self.classifier.get_face_classifier()
        self.eye_classifier = self.classifier.get_face_classifier()
        self.sample = 1
        self.number_of_samples = 30
        self.width = 220
        self.height = 220
        #Remake here!!!!!!!!
        self.id = 5

    def get_face_classifier(self):
        return self.face_classifier

    def get_eye_classifier(self):
        return self.eye_classifier

    def capture(self):
        while(True):
            frame = self.cap.get_frame()
            #Decode frame
            nparr = np.fromstring(frame, np.uint8)
            frame = cv2.imdecode(nparr, cv2.COLOR_BGR2GRAY)
            cv2.imwrite("c.jpg", frame)
            frame = cv2.imdecode(nparr, cv2.COLOR_BGR2GRAY)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            cv2.imwrite("g.jpg", frame)






cap = Capture()
#face = cap.get_eye_classifier()
#print(type(face))
cap.capture()


#Criar o objeto ou retornar através do Classifier???????????