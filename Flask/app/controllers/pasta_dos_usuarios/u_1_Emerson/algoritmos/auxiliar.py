# -*- coding: utf-8 -*
import cv2

class ReconhecimentoFacial():
    def __init__(self):
        self.detector_de_face = cv2.CascadeClassifier("/home/emerson/PycharmProjects/FaceRecFlask/FaceRecFlask/Flask/app/controllers/pasta_dos_usuarios/u_1_Emerson/arquivos-cascade/haarcascade-frontalface-default.xml")
        self.reconhecedor = cv2.face.EigenFaceRecognizer_create()
        self.reconhecedor.read("/home/emerson/PycharmProjects/FaceRecFlask/FaceRecFlask/Flask/app/controllers/pasta_dos_usuarios/u_1_Emerson/arquivos-de-reconhecimento/classify_eigen_yale.yml")
        self.largura = 220
        self.altura = 220
        self.fonte = cv2.FONT_HERSHEY_COMPLEX_SMALL
        self.camera = cv2.VideoCapture("/home/emerson/PycharmProjects/FaceRecFlask/FaceRecFlask/Flask/app/controllers/pasta_dos_usuarios/u_1_Emerson/arquivos-imagem-e-video/video-face.mp4")
        self.imagem = None
        self.imagem_cinza = None
        self.imagem_desenhada = None
        self.faces_detectadas = None
        # Obrigatorio
        self.status_deteccao = False
        self.status_reconhecimento = False
        self.numero_de_faces = []


    def capturar_detectar(self):
        conectado, self.imagem = self.camera.read()
        if conectado:
            self.imagem_cinza = cv2.cvtColor(self.imagem, cv2.COLOR_BGR2GRAY)
            self.faces_detectadas = self.detector_de_face.detectMultiScale(self.imagem_cinza, scaleFactor=10, minSize=(50, 50))
            return self.imagem_cinza, self.faces_detectadas
        # Obrigatório retornar caso não haja mais entradas
        return "Finalizado"

    def reconhecer_desenhar(self):
        # Obrigatório verificar caso não haja mais entradas
        if self.capturar_detectar() == "Finalizado":
            return "Finalizado"
        else:
            self.imagem_cinza, self.faces_detectadas = self.capturar_detectar()
        if self.faces_detectadas == ():
            self.status_deteccao = True
            print("Vazio")
        for (x, y, l, a) in self.faces_detectadas:
            print("Possui")
            self.status_reconhecimento = True
            #self.numero_de_faces = self.faces_detectadas.shape[0]
            face_recortada = cv2.resize(self.imagem_cinza[y:y + a, x:x + l], (self.largura, self.altura))
            cv2.rectangle(self.imagem, (x, y), (x + l, y + a), (0,0,255), 2)
            id, conf = self.reconhecedor.predict(face_recortada)
            self.numero_de_faces.append((face_recortada, id, conf))
            cv2.putText(self.imagem, str(id), (x, y + (a + 30)), self.fonte, 2, (0, 0, 255))
            cv2.putText(self.imagem, str(conf), (x, y + (a + 50)), self.fonte, 1, (0, 0, 255))

        # Obrigatório converter
        ret, jpeg1 = cv2.imencode('.jpg', self.imagem)

        #Obrigatório retornar uma lista com "imagem codificada", se detectou, se reconheceu, atributos da/das faces detectadas,
        #return [self.imagem, self.status_deteccao, self.status_reconhecimento, self.numero_de_faces, jpeg1.tostring()]
        return {'imagem':self.imagem, 's_deteccao':self.status_deteccao, 's_reconhecimento':self.status_reconhecimento, 'n_faces':self.numero_de_faces, 'imagem_encode':jpeg1.tostring()}



