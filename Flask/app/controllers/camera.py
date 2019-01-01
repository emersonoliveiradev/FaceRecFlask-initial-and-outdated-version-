import cv2

class VideoCamera(object):
    """
    Documentação da Classe
    """
    def __init__(self):
        self.captura = cv2.VideoCapture(-1)

    def __del__(self):
        self.captura.release()

    def get_decoded_frame(self):
        # Decodificar frame para enviar
        ret, frame = self.captura.read()
        return frame

    def get_encoded_frame(self):
        ret, frame = self.captura.read()
        # Codificar frame para enviar
        ret, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tostring()

    def get_frame(self):
         ret, frame = self.captura.read()
         # Codificar frame para enviar
         ret, jpeg = cv2.imencode('.jpg', frame)
         return jpeg.tostring()


        #frame = cv2.imdecode(jpeg, cv2.COLOR_BGR2GRAY)

    #def __init__(self):
        #self.frames = [open(f + '.jpg', 'rb').read() for f in ['1', '2', '3']]

    #def get_frame(self):
        #return self.frames[int(time()) % 3]
