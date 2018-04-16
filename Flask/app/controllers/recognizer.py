import cv2
import numpy as np
#Create my own auxiliary class
#from UsefulFunctions import UsefulFunctions
from app.controllers.capture import Capture
from app.controllers.trainner import Trainner


class Recognizer(object):
    def __init__(self):
        self.trainner = Trainner()
        self.eiggen_recognizer = self.trainner.get_eiggen()
        self.eiggen_recognizer.load("app/controllers/classifiers/classify_eigen_yale.yml")  # Refazer e colocar para pegar Usuario + restante
        self.capture = Capture()


    def rec_detectar(self):
        id = 0
        imagem, face = self.capture.capture()
        #O predict espera um nd.array
        print(self.eiggen_recognizer.predict(face))
        print(str(id))
        return imagem


'''
if __name__ == '__main__':
    recognizer = Recognizer()
    print(type(recognizer.arquivo_yml))
'''

