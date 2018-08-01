import cv2
import numpy as np
from copy import copy
#A diferença está aqui... mas oq???? Por que com o caminho completo não funciona???
from app.controllers.classifier import Classifier
from app.controllers.generator import Generator


class Capture(object):
    def __init__(self):
        self.gen = Generator()
        self.classifier = Classifier()
        self.face_classifier = self.classifier.get_face_classifier()
        self.eye_classifier = self.classifier.get_eye_classifier()
        self.sample = 1
        self.number_of_samples = 30
        self.width = 220
        self.height = 220
        self.show_frame = None
        self.gray_frame = None
        # Refazer aqui!!!!!!!!
        self.id = 5
        self.sample = 1


    def get_face_classifier(self):
        return self.face_classifier

    def get_eye_classifier(self):
        return self.eye_classifier

    def draw_face(self, detected_face):
        for x, y, w, h in detected_face:
            cv2.rectangle(self.show_frame, (x, y), (x + w, y + h), (0, 0, 255), 5)

    def draw_eye(self, detected_eye):
        for (x, y, w, h) in detected_eye:
            cv2.rectangle(self.show_frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

    #Só retirar o "2"
    def capture2(self):
        while True:
            self.show_frame = self.gen.get_decoded_frame()
            self.gray_frame = cv2.cvtColor(self.show_frame, cv2.COLOR_BGR2GRAY)
            detected_faces = self.face_classifier.detectMultiScale(self.gray_frame, scaleFactor=1.5, minSize=(50, 50))
            print("OK1")
            if type(detected_faces) == np.ndarray:
                self.draw_face(detected_faces)
                detected_eyes = self.eye_classifier.detectMultiScale(self.gray_frame, minSize=(20, 20))
                self.draw_eye(detected_eyes)
                print("OK2")
                if cv2.waitKey(1) & 0xFF == ord("c"):
                    print("OK3")
                    cv2.imwrite("database_faces/user." + str(self.id) + "." + str(self.sample) + ".jpg", face_resize)
                    print("Face" + str(self.sample) + " captured")
                    self.sample += 1
            ret, jpeg = cv2.imencode('.jpg', self.show_frame)
            return jpeg.tostring()


    def capture(self):
        while True:
            self.show_frame = self.gen.get_decoded_frame()
            self.gray_frame = cv2.cvtColor(self.show_frame, cv2.COLOR_BGR2GRAY)
            detected_faces = self.face_classifier.detectMultiScale(self.gray_frame, scaleFactor=1.5, minSize=(50, 50))
            if type(detected_faces) == np.ndarray:
                print("Retornando!!!!!!!!!!!!!!!!!")
                return detected_faces, self.show_frame, self.gray_frame
            else:
                print("Não existe faces detectadas")
                return None, self.show_frame, None



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