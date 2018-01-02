import numpy as np
import cv2

class Classifier(object):
    @classmethod
    def __init__(self):
        self.classifier_face = cv2.CascadeClassifier("app/static/classifiers/haarcascade-frontalface-default.xml")
        self.classifier_eye = cv2.CascadeClassifier("app/static/classifiers/haarcascade-eye.xml")


    def get_face_classifier(self):
        return self.classifier_face


    def get_eye_classifier(self):
        return self.classifier_eye





##
##Criar o objeto ou retornar através do self.classifier????????
##
