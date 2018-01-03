import cv2
import numpy as np
import os


class Trainner(object):
    def __init__(self):
        self.eigenface_trainer = cv2.face.createEigenFaceRecognizer(50, 0)
        self.fisherface_trainer = cv2.face.createFisherFaceRecognizer()
        self.lbph_trainer = cv2.face.createLBPHFaceRecognizer()

    @classmethod
    def get_face_id(self):
        #List the files in the database_faces and add the directory
        path = [os.path.join('database_faces', f) for f in os.listdir('database_faces')]
        faces, ids = [], []

        for path_user in path:
            user_face = cv2.cvtColor(cv2.imread(path_user), cv2.COLOR_BGR2GRAY)
            #Refazer.... não reconhece ids compostos por mais de um número
            id = int(os.path.split(path_user)[-1].split('.')[1])
            ids.append(id)
            faces.append(user_face)
        return np.array(ids), faces

    def eigenface_trainer(self):
        ids, faces = get_face_id()
        self.eigenface_trainer.train(faces, ids)
        self.eigenface_trainer.save("classifiers/classify_eigen_yale.yml")
        return True


