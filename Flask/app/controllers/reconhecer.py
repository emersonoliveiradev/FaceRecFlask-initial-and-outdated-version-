import cv2
import numpy as np
#Create my own auxiliary class
#from UsefulFunctions import UsefulFunctions
from app.controllers.capturar import Capturar
from app.controllers.treinar import Treinar


class Reconhecer(object):
    def __init__(self):
        self.treinar = Treinar()
        self.reconhecer_eiggen = self.treinar.get_eiggen()
        #self.eiggen_recognizer.load("app/controllers/classificadores/classify-eigen-yale.yml")  # Refazer e colocar para pegar Usuario + restante
        self.reconhecer_eiggen.read("app/controllers/classificadores/classify-eigen-yale.yml")  # Refazer e colocar para pegar Usuario + restante
        self.capturar = Capturar()


    def encontrar_face(self, face_detectada, frame_cinza):
        face = []
        for x, y, w, h in face_detectada:
            face_redimensionada = cv2.resize(frame_cinza[y:y + h, x:x + w], (220, 220))
            face.append(face_redimensionada)
        return face

    def desenhar_escrever(self, face_detectada, frame, id):
        cont = 0
        for x, y, w, h in face_detectada:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 5)
            cv2.putText(frame, "U - " + str(id[cont][0]) + " | C " + str(int(id[cont][1])), (x, y + (h + 30)), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 255))
            cont +=1

    def rec_detectar(self):
        id = []
        faces_detectadas, mostrar_frame, frame_cinza = self.capturar.capturar()
        if frame_cinza is None:
            ret, jpeg1 = cv2.imencode('.jpg', mostrar_frame)
            return jpeg1.tostring()

        face_redimensionada = self.encontrar_face(faces_detectadas, frame_cinza)
        for face in face_redimensionada:
            t_id = self.reconhecer_eiggen.predict(face)
            id.append(t_id)

        self.desenhar_escrever(faces_detectadas, mostrar_frame, id)
        ret, jpeg1 = cv2.imencode('.jpg', mostrar_frame)
        return jpeg1.tostring()