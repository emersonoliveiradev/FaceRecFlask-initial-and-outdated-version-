import cv2
import numpy as np
from copy import copy
#A diferença está aqui... mas oq???? Por que com o caminho completo não funciona???
from app.controllers.classificador import Classificador
from app.controllers.gerador import Gerador


class Capturar(object):
    def __init__(self):
        self.gen = Gerador()
        self.classificador = Classificador()
        self.face_classificador = self.classificador.get_face_classificador()
        self.olho_classificador = self.classificador.get_olho_classificador()
        self.amostra = 1
        self.number_de_amostras = 30
        self.largura = 220
        self.altura = 220
        self.mostrar_frame = None
        self.frame_cinza = None
        # Refazer aqui!!!!!!!!
        self.id = 5
        self.amostra = 1


    def get_face_classificador(self):
        return self.face_classificador

    def get_olho_classificador(self):
        return self.olho_classificador

    def desenhar_face(self, face_detectada):
        for x, y, w, h in face_detectada:
            cv2.rectangle(self.mostrar_frame, (x, y), (x + w, y + h), (0, 0, 255), 5)

    def desenhar_olho(self, olho_detectado):
        for (x, y, w, h) in olho_detectado:
            cv2.rectangle(self.mostrar_frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

    #Só retirar o "2"
    def captura_detectar(self):
        while True:
            self.mostrar_frame = self.gen.get_decoded_frame()
            self.frame_cinza = cv2.cvtColor(self.mostrar_frame, cv2.COLOR_BGR2GRAY)

            faces_detectadas = self.face_classificador.detectMultiScale(self.frame_cinza, scaleFactor=1.5, minSize=(50, 50))
            print("Passou")
            if type(faces_detectadas) == np.ndarray:
                self.desenhar_face(faces_detectadas)
                olhos_detectados = self.olho_classificador.detectMultiScale(self.frame_cinza, minSize=(20, 20))
                self.desenhar_olho(olhos_detectados)
                print("OK2")
                if cv2.waitKey(1) & 0xFF == ord("c"):
                    print("OK3")
                    cv2.imwrite("banco_de_faces/user." + str(self.id) + "." + str(self.amostra) + ".jpg", face_resize)
                    print("Face" + str(self.amostra) + " captured")
                    self.amostra += 1
            ret, jpeg = cv2.imencode('.jpg', self.mostrar_frame)
            return jpeg.tostring()


    def capturar(self):
        while True:
            self.mostrar_frame = self.gen.get_decoded_frame()
            self.frame_cinza = cv2.cvtColor(self.mostrar_frame, cv2.COLOR_BGR2GRAY)
            faces_detectadas = self.face_classificador.detectMultiScale(self.frame_cinza, scaleFactor=1.5, minSize=(50, 50))
            if type(faces_detectadas) == np.ndarray:
                print("Retornando!!!!!!!!!!!!!!!!!")
                return faces_detectadas, self.mostrar_frame, self.frame_cinza
            else:
                print("Não existem faces detectadas")
                return None, self.mostrar_frame, None



'''
        if type(detected_faces) == np.ndarray:
            gray_frame, face_resize = self.found_classifier_face(detected_faces, self.gray_frame)
            ret, jpeg1 = cv2.imencode('.jpg', self.show_frame)
            # ret, jpeg2 = cv2.imencode('.jpg', face_resize)
            return jpeg1.tostring(), face_resize

        return self.show_frame, False
   '''
'''
if __name__ == '__main__':
    cap = Capture()
    cap.capture()
'''
#face = cap.get_eye_classifier()
#cap = Capture()
#cap.capture()

# Criar o objeto ou retornar através do Classifier???????????