# -*- coding: utf-8 -*
import cv2

detectorFace = cv2.CascadeClassifier("classifiers/haarcascade-frontalface-default.xml")
reconhecedor = cv2.face.EigenFaceRecognizer_create()
reconhecedor.read("classifiers/classify_eigen_yale.yml")

largura = 220
altura = 220
lista_faces_cadastradas = ["Emerson", "Wanderson"]
font = cv2.FONT_HERSHEY_COMPLEX_SMALL

camera = cv2.VideoCapture("/home/emerson/PycharmProjects/FaceRecFlask/FaceRecFlask/Flask/app/controllers/pasta-dos-usuarios/u_1_Emerson/arquivos-imageme-video/vidfeo-face-.mp4")

while (True):
    conectado, imagem = camera.read()
    imagemCinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
    facesDetectadas = detectorFace.detectMultiScale(imagemCinza, scaleFactor=10, minSize=(50,50))
    for (x, y, l, a) in facesDetectadas:
        imagemFace = cv2.resize(imagemCinza[y:y + a, x:x + l], (largura, altura))
        cv2.rectangle(imagem, (x, y), (x + l, y + a), (0,0,255), 2)
        id, conf = reconhecedor.predict(imagemFace)
        nome = ""
        nome = lista_faces_cadastradas[id - 1]
        cv2.putText(imagem, nome, (x,y +(a+30)), font, 2, (0,0,255))
        cv2.putText(imagem, str(conf), (x,y + (a+50)), font, 1, (0,0,255))

    cv2.imshow("Face", imagem)
    if cv2.waitKey(1) == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()



