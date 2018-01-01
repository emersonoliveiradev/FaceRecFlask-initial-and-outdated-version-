from app import app
from flask import Flask, render_template, Response
#Discocery where is the root path of modules
from app.controllers.camera import VideoCamera
from app.controllers.capture import Capture
from app.controllers.generator import Generator


# The 'render_template, search in path templates automatically by default
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/face_capture')
def face_capture():
    return render_template('capture.html')


#Video streaming generator function
def gen(camera):
    while True:
        frame = camera.get_encoded_frame()
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/video_feed')
def video_feed():
    #Retorna o que o gerador (função gen()) está gerando
    return Response(gen(VideoCamera()), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(debug=True)

