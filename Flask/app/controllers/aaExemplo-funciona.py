# -*- coding: utf-8 -*
#Já deveria ter no ambiente
import cv2

# Teria que escolher na interface gráfica
# Uma variável/função do sistema buscaria o caminho, teria que ficar na pasta dele
detectorFace = cv2.CascadeClassifier("classificadores/haarcascade-frontalface-default.xml")

# Teria que escolher na interface gráfica
reconhecedor = cv2.face.EigenFaceRecognizer_create()
reconhecedor.read("classificadores/classify_eigen_yale.yml")

largura, altura = 220, 220
font = cv2.FONT_HERSHEY_COMPLEX_SMALL
camera = cv2.VideoCapture()


lista_faces_cadastradas = ["Emerson", "Wanderson"]


while (True):
    conectado, imagem = camera.read()
    imagemCinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
    facesDetectadas = detectorFace.detectMultiScale(imagemCinza, scaleFactor=1.5, minSize=(50,50))
    for (x, y, l, a) in facesDetectadas:
        imagemFace = cv2.resize(imagemCinza[y:y + a, x:x + l], (largura, altura))
        cv2.rectangle(imagem, (x, y), (x + l, y + a), (0,0,255), 2)
        id, conf = reconhecedor.predict(imagemFace)
        nome = ""
        nome = lista_faces_cadastradas[id - 1]
        """
        if id == 1:
            nome = 'Emerson'
        elif id == 2:
            nome = 'Wanderson'
        """
        cv2.putText(imagem, nome, (x,y +(a+30)), font, 2, (0,0,255))
        cv2.putText(imagem, str(conf), (x,y + (a+50)), font, 1, (0,0,255))

    cv2.imshow("Face", imagem)
    if cv2.waitKey(1) == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()