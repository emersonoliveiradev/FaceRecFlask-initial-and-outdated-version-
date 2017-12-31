import cv2

class VideoCamera(object):
    def __init__(self):
        self.cap = cv2.VideoCapture(0)

    def __del__(self):
        self.video.release()

    def get_frame(self):
        ret, frame = self.cap.read()
        _, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tostring()

