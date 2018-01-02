import cv2
import numpy as np
from camera import VideoCamera
from classifier import Classifier

class Capture(object):
    def __init__(self):
        self.cap = VideoCamera()
        self.classifier = Classifier()
        self.face_classifier = self.classifier.get_face_classifier()
        self.eye_classifier = self.classifier.get_eye_classifier()
        self.sample = 1
        self.number_of_samples = 30
        self.width = 220
        self.height = 220
        # Remake here!!!!!!!!
        self.id = 5
        self.sample = 1

    def get_face_classifier(self):
        return self.face_classifier

    def get_eye_classifier(self):
        return self.eye_classifier

    #Not in use for in the moment
    #@classmethod
    def found_classifier_face(self, detected_face, frame):
        for x, y, w, h in detected_face:
            # Draw rectangle on the classifier detected
            face_resize = cv2.resize(frame[y:y + h, x:x + w], (self.width, self.height))
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 5)
        return frame, face_resize

    def found_classifier_eye(self, detected_eye, frame):
        for (ex, ey, ew, eh) in detected_eye:
            # Draw rectangle on the classifier detected
            cv2.rectangle(frame, (ex, ey), (ex + ew, ey + eh), (255, 0, 0), 2)
        return frame

    def capture(self):
        while(True):
            coded_frame = self.cap.get_frame()

            # Decode frame
            nparr = np.fromstring(coded_frame, np.uint8)
            decoded_frame = cv2.imdecode(nparr, cv2.COLOR_BGR2GRAY)
            gray_frame = cv2.cvtColor(decoded_frame, cv2.COLOR_BGR2GRAY)

            # Detect faces
            detected_faces = self.face_classifier.detectMultiScale(gray_frame, scaleFactor=1.5, minSize=(50,50))
            if type(detected_faces) != tuple:
                gray_frame, face_resize = self.found_classifier_face(detected_faces, gray_frame)

                detected_eyes = self.eye_classifier.detectMultiScale(gray_frame, minSize=(20,20))
                gray_frame = self.found_classifier_eye(detected_eyes, gray_frame)
                if cv2.waitKey(1) & 0xFF == ord("c"):
                    print("Entrou")
                    #Save faces in the database_faces
                    cv2.imwrite("database_faces/user." + str(self.id) + "." + str(self.sample) + ".jpg", face_resize)
                    print("Face" + str(self.sample) + " captured")
                    self.sample += 1

                cv2.imshow("Show", gray_frame)
                cv2.waitKey(1)


cap = Capture()
# face = cap.get_eye_classifier()
# print(type(face))
cap.capture()