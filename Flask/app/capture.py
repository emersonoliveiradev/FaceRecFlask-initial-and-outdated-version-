import cv2
from camera import VideoCamera
from classifier import Classifier

class Capture(object):
    def __init__(self):
        self.classifier = Classifier()
        self.face_classifier = self.classifier.get_face_classifier()
        self.eye_classifier = self.classifier.get_face_classifier()

    def get_face_classifier(self):
        return self.face_classifier



################
cap = Capture()
face = cap.get_face_classifier()
print(type(face))

#Criar o objeto ou retornar através do Classifier???????????