import cv2
import numpy as np
from copy import copy
#A diferença está aqui... mas oq???? Por que com o caminho completo não funciona???
from classifier import Classifier
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
        # Remake here!!!!!!!!
        self.id = 5
        self.sample = 1


    def get_face_classifier(self):
        return self.face_classifier

    def get_eye_classifier(self):
        return self.eye_classifier

    def found_classifier_face(self, detected_face, frame):
        for x, y, w, h in detected_face:
            # Draw rectangle on the classifier detected
            face_resize = cv2.resize(frame[y:y + h, x:x + w], (self.width, self.height))
            cv2.rectangle(self.show_frame, (x, y), (x + w, y + h), (0, 0, 255), 5)
        return frame, face_resize

    def found_classifier_eye(self, detected_eye, frame):
        for (ex, ey, ew, eh) in detected_eye:
            # Draw rectangle on the classifier detected
            cv2.rectangle(self.show_frame, (ex, ey), (ex + ew, ey + eh), (255, 0, 0), 2)
        return frame

    def capture(self):
        while(True):
            print("Running1")
            print("Running2")
            self.show_frame = self.gen.get_decoded_frame()
            self.gray_frame = cv2.cvtColor(self.show_frame, cv2.COLOR_BGR2GRAY)

            detected_faces = self.face_classifier.detectMultiScale(self.gray_frame, scaleFactor=1.5, minSize=(50, 50))

            if type(detected_faces) != tuple:                
                gray_frame, face_resize = self.found_classifier_face(detected_faces, self.gray_frame)

                detected_eyes = self.eye_classifier.detectMultiScale(self.gray_frame, minSize=(20, 20))
                self.gray_frame = self.found_classifier_eye(detected_eyes, self.gray_frame)                
                if cv2.waitKey(1) & 0xFF == ord("c"):
                    cv2.imwrite("database_faces/user." + str(self.id) + "." + str(self.sample) + ".jpg", face_resize)
                    print("Face" + str(self.sample) + " captured")
                    self.sample += 1

            ret, jpeg = cv2.imencode('.jpg', self.show_frame)
            return jpeg.tostring()


if __name__ == '__main__':
    cap = Capture()
    cap.capture()

#face = cap.get_eye_classifier()
#cap = Capture()
#cap.capture()

# Criar o objeto ou retornar através do Classifier???????????