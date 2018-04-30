from app import app
from flask import Flask, render_template, Response
#Discocery where is the root path of modules
from app.controllers.camera import VideoCamera
from app.controllers.capture import Capture
from app.controllers.recognizer import Recognizer
from app.controllers.generator import Generator
from app.models.forms import LoginForm


@app.route('/home')
@app.route('/index')
@app.route('/')
def index():
    return render_template('index.html')

@app.route("/login")
def login():
    form = LoginForm()
    return render_template('login.html', form=form)



@app.route("/show_capture")
def show_capture():
    return render_template('capture.html')

@app.route('/face_capture')
def face_capture():
    return Response(gen_capture(), mimetype='multipart/x-mixed-replace; boundary=frame')

def gen_capture():
    cap = Capture()
    while True:
        frame = cap.capture2()
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')



@app.route('/face_recognition')
def face_recognition():
    return render_template('recognition.html')

@app.route('/face_recognition_gen')
def face_recognition_gen():
    return Response(gen_recognition(), mimetype='multipart/x-mixed-replace; boundary=frame')

def gen_recognition():
    rec = Recognizer()
    while True:
        frame = rec.rec_detectar()
        if frame == False:
            continue
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')



#Original
@app.route('/video_feed')
def video_feed():
    #Retorna o que o gerador (função gen()) está gerando
    return Response(gen(VideoCamera()), mimetype='multipart/x-mixed-replace; boundary=frame')

#Original
def gen(camera):
    while True:
        frame = camera.get_encoded_frame()
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')



@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/help")
def help():
    return render_template('help.html')



# Receive variable <name>
@app.route('/test', defaults={"name": None})
@app.route('/test/<name>')
def show_name(name):
    return render_template('test.html', name=name)



if __name__ == '__main__':
    app.run(debug=True)