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


    def found_classifier_face(self, detected_face, gray_frame):
        face = []
        for x, y, w, h in detected_face:
            face_resize = cv2.resize(gray_frame[y:y + h, x:x + w], (220, 220))
            face.append(face_resize)
        return face

    def draw_and_put_face(self, detected_face, frame, id):
        cont = 0
        for x, y, w, h in detected_face:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 5)
            cv2.putText(frame, str(id[cont]), (x, y + (h + 30)), cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, (0, 0, 255))


    def rec_detectar(self):
        id = []
        detected_faces, show_frame, gray_frame = self.capture.capture()
        face_resize = self.found_classifier_face(detected_faces, gray_frame)
        for face in face_resize:
            t_id = self.eiggen_recognizer.predict(face)
            id.append(t_id)
            print(id)
        self.draw_and_put_face(detected_faces, show_frame, id)
        ret, jpeg1 = cv2.imencode('.jpg', show_frame)
        return jpeg1.tostring()


        print("Não reconheceu")
        #O predict espera um nd.array
        #print(type(face))
        #print(self.eiggen_recognizer.predict(face))
        #print(str(id))
        #return imagem


'''
if __name__ == '__main__':
    recognizer = Recognizer()
    print(type(recognizer.arquivo_yml))
    
    
    
    
    
    
    
        def rec_detectar(self):
        print("Entrou")
        detected_faces, show_frame, gray_frame = self.capture.capture()
        for fx, fy, fw, fh in detected_faces:
            face_resize = cv2.resize(gray_frame[fy:fy + fh, fx:fx + fw], (220, 220))
            cv2.rectangle(show_frame, (fx, fy), (fx + fw, fy + fh), (0, 0, 255), 5)
            print(type(face_resize))
            print("Errando aqui")            
            id = self.eiggen_recognizer.predict(face_resize)
            print("Errando aqui2")
            if str(id) == '1' or str(id) == '2' or str(id) == '3':
                print(id)
                print("Reconheceu aqui!!!")
            print(id)
            cv2.putText(show_frame, str(id), (fx, fy + (fh + 30)), cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, (0, 0, 255))
            ret, jpeg1 = cv2.imencode('.jpg', show_frame)
            return jpeg1.tostring()
'''

