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
            cv2.putText(frame, "U - " + str(id[cont][0]) + " | C " + str(int(id[cont][1])), (x, y + (h + 30)), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 255))
            cont +=1

    def rec_detectar(self):
        id = []
        detected_faces, show_frame, gray_frame = self.capture.capture()
        if gray_frame is None:
            ret, jpeg1 = cv2.imencode('.jpg', show_frame)
            return jpeg1.tostring()

        face_resize = self.found_classifier_face(detected_faces, gray_frame)
        for face in face_resize:
            t_id = self.eiggen_recognizer.predict(face)
            id.append(t_id)
        self.draw_and_put_face(detected_faces, show_frame, id)
        ret, jpeg1 = cv2.imencode('.jpg', show_frame)
        return jpeg1.tostring()