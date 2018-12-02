import cv2

class Classificador(object):
    @classmethod
    def __init__(self):
        self.classificador_face = cv2.CascadeClassifier("app/static/classificadores/haarcascade-frontalface-default.xml")
        self.classificador_olho = cv2.CascadeClassifier("app/static/classificadores/haarcascade-eye.xml")


    def get_face_classificador(self):
        return self.classificador_face


    def get_olho_classificador(self):
        return self.classificador_olho






##
##Criar o objeto ou retornar através do self.classifier????????
##


##
##Criar o objeto ou retornar através do self.classifier????????
##
