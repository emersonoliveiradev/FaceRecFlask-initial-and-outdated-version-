from app import app
from flask import Flask, render_template, Response
from camera import VideoCamera
from capture import Capture
import numpy as np
import cv2

#Create to interpreter of python, control the all aplication
app = Flask(__name__)

#Video streaming generator function
def gen(camera):
    while True:
        frame = camera.get_encoded_frame()
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

#Video streaming home page
@app.route('/')
def index():
    return render_template('layout.html')



#Video streaming home page
@app.route('/')
def home():
    return render_template('layout.html')

@app.route('/face_capture')
def face_capture():
    return render_template('capture.html')

@app.route('/video_feed')
def video_feed():
    #Retorna o que o gerador (função gen()) está gerando
    return Response(gen(VideoCamera()), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)

