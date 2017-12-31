import cv2

class Classifier(object):
    def __init__(self):
        print("Init objeto Classifier")
        self.classifier_face = cv2.CascadeClassifier("classifiers/haarcascade-frontalface-default.xml")
        self.classifier_eye = cv2.CascadeClassifier("classifiers/haarcascade-eye.xml")


    def get_face_classifier(self):
        return self.classifier_face

    
    def get_eye_classifier(self):
        return self.classifier_eye

#Criar o objeto ou retornar através do self.classifier????????

