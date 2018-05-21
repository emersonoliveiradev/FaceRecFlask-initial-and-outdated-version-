import cv2

class VideoCamera(object):
    def __init__(self):
        self.cap = cv2.VideoCapture(0)

    def __del__(self):
        self.cap.release()

    def get_decoded_frame(self):
        ret, frame = self.cap.read()
        return frame

    def get_encoded_frame(self):
        ret, frame = self.cap.read()
        #Encode frame
        ret, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tostring()

    def get_frame(self):
         ret, frame = self.cap.read()
         # Encode frame
         ret, jpeg = cv2.imencode('.jpg', frame)
         return jpeg.tostring()


        #frame = cv2.imdecode(jpeg, cv2.COLOR_BGR2GRAY)

    #def __init__(self):
        #self.frames = [open(f + '.jpg', 'rb').read() for f in ['1', '2', '3']]

    #def get_frame(self):
        #return self.frames[int(time()) % 3]
