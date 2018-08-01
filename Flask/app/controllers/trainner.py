import cv2
import numpy as np
import os

class Trainner(object):
    def __init__(self):
        #self.eigenface = cv2.face.createEigenFaceRecognizer() #Não colocar os números aqui dentro
        self.eigenface = cv2.face.EigenFaceRecognizer_create()  # Não colocar os números aqui dentro
        #self.fisherface = cv2.face.createFisherFaceRecognizer()
        #self.lbph = cv2.face.createLBPHFaceRecognizer()

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

    def eigenface_trainer(self, faces, ids):
        self.eigenface.train(faces, ids)
        self.eigenface.save("classifiers/classify_eigen_yale.yml")
        return True

    #Para o recognizer
    def get_eiggen(self):
        return self.eigenface

if __name__ == '__main__':
    treinador = Trainner()
    print("Initializing...")
    ids, faces = treinador.get_face_id()
    print("Trainning...")
    treinador.eigenface_trainer(faces, ids)
    print("Finish!")
