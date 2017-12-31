import cv2

class Classifier(object):
    def __init__(self):
        self.classifier_face = cv2.CascadeClassifier("classifiers/haarcascade-frontalface-default.xml")
        self.classifier_eye = cv2.CascadeClassifier("classifiers/haarcascade-eye.xml")

    def __del__(self):
        self.classifier_face.release()
        self.classifier_eye.release()

    def get_classifier(self, name):
        if name == "face":
            return self.classifier_face
        elif name == "eye":
            return self.classifier_eye
        else:
            return False


