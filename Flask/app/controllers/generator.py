from app.controllers.camera import VideoCamera

#Video streaming generator function
class Generator(object):
    def __init__(self):
        self.video_camera = VideoCamera()

    def gen(camera, ret):
        while True:
            frame = camera.get_frame()
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
            
    def get_decoded_frame(self):
        return self.video_camera.get_decoded_frame()

        
            
    