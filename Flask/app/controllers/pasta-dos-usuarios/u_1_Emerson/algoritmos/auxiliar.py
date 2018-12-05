# -*- coding: utf-8 -*
import cv2

detectorFace = cv2.CascadeClassifier("classifiers/<<nome_do_arquivo_xml>>")
reconhecedor = <<metodo_de_reconhecimento>>
reconhecedor.read("classifiers/<<nome_do_arquivo_yale>>")

largura = <<largura>>
altura = <<altura>>
lista_faces_cadastradas = ["Emerson", "Wanderson"]
font = cv2.FONT_HERSHEY_COMPLEX_SMALL

camera = cv2.VideoCapture(<<numero_da_camera>>)

while (True):
    conectado, imagem = camera.read()
    imagemCinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
    facesDetectadas = detectorFace.detectMultiScale(imagemCinza, scaleFactor=<<fator_de_escala>>, minSize=(<<tamanho_minimo_x>>,<<tamanho_minimo_y>>))
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



