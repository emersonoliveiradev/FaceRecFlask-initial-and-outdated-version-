from app import app, db, login_manager, login_user, logout_user, login_required
from flask import Flask, render_template, Response, request, redirect, url_for, flash

#Discocery where is the root path of modules
from app.controllers.camera import VideoCamera
from app.controllers.capture import Capture
from app.controllers.recognizer import Recognizer
from app.controllers.generator import Generator

#Forms e Tables
from app.models.forms import LoginForm, CadastrarAlgoritmoForm, CadastrarUsuarioForm
from app.models.tables import Pessoa, Usuario


@app.route('/home')
@app.route('/index')
@app.route('/')
def index():
    return render_template('index.html')


@app.route("/show_capture")
def show_capture():
    return render_template('capture.html')

@app.route('/face_capture')
def face_capture():
    return Response(gen_capture(), mimetype='multipart/x-mixed-replace; boundary=frame')

#Tentar mandar uma chave aqui pela url, liberando p capturar a imagem
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


#######################
#Algoritmos do Usuário#
#######################
@app.route('/crud-algoritmo', methods=['GET', 'POST'])
def cadastrar_algoritmo():
    if request.method == 'POST':
        nome = request.form['nome']
        algoritmo = request.form['conteudo']
        data = [nome, algoritmo]
        arq = open("/home/haw/PycharmProjects/FaceRecFlask/.virtualenvs/FaceRecFlask/Flask/app/controllers/algoritmos_usuario_id.py", "r+")
        print(arq)
        for l in arq:
            l = l.rstrip()
            print(l)

        arq.write(algoritmo)
        arq.write('\n\n\n')
        arq.close()

        from app.controllers.algoritmos_usuario_id import Operacoes
        o = Operacoes()
        a = o.sum(int(2), int(6))
        print(a)
        print('OK')
        form = CadastrarAlgoritmoForm()
        return listar_algoritmos()

    form = CadastrarAlgoritmoForm()
    return render_template('cadastrar-algoritmo.html', form=form)


@app.route('/atualizar-algoritmo/<int:id>', methods=['GET'])
def atualizar_algoritmo(id):
    if id:
        print("Existe")
    form = CadastrarAlgoritmoForm()
    return render_template('cadastrar-algoritmo.html', form=form)



#Nomes das funções criadas
@app.route('/listar-algoritmos', methods=['GET'])
def listar_algoritmos():
    nome = "algoritmos_usuario_id.py"

    arq = open("/home/haw/PycharmProjects/FaceRecFlask/.virtualenvs/FaceRecFlask/Flask/app/controllers/algoritmos_usuario_id.py", "r+")
    count=0
    lista = []
    for l in arq:
        if "class" in l:
            a = l.index(' ')
            b = l.index(":")
            nome_funcao = l[a:b]
            lista.append(nome_funcao)

            count+=1
    if count==0:
        print("Nenhuma classe encontrada!")

    arq.close()
    data = [nome, lista]
    return render_template('listar-algoritmos.html', data=data)





#######
#Login#
#######
@login_manager.user_loader
def load_user(id):
    return Usuario.query.filter_by(id=id).first()


##########
#Usuarios#
##########
@app.route("/login", methods=['GET','POST'])
def login():
    form_login = LoginForm()
    print("Entrou")
    # Login-Manager
    if form_login.validate_on_submit():
        print("Entrou")
        usuario = Usuario.query.filter_by(email=form_login.email.data).first()
        if usuario and usuario.senha == form_login.senha.data:
            print("Entrou")
            login_user(usuario, force=True, remember=True)
            flash("Logado!")
            return redirect(url_for("index"))
        else:
            flash("Login Inválido!")
            return redirect(url_for("login"))
    return render_template('login.html', form_login=form_login)


@app.route("/usuarios")
def logando():
    usuario = Usuario.query.filter_by(senha='123').first()
    #Adiciona todos os dados do bd da pesssoa
    login_user(usuario)
    return "Está logado"

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))

@app.route("/atual")
@login_required
def atual():
    return "Atual: " + current_user.nome


@app.route("/cadastrar-usuario", methods=['GET','POST'])
def cadastrar_usuario():
    if request.method == 'POST':
        print("Entrou")
        nome = request.form['nome']
        email = request.form['email']
        senha= request.form['senha']
        cpf = request.form['cpf']
        dt_nascimento = request.form['dt_nascimento']

        if nome and email and senha and cpf and dt_nascimento:
            usuario = Usuario(nome, email, senha, cpf, dt_nascimento)
            db.session.add(usuario)
            db.session.commit()
            flash("Cadastro de usuário realizado com sucesso!")
        else:
            print("Falta valores")


        form = CadastrarUsuarioForm()
        return render_template('listar-usuarios.html', form=form)

    form = CadastrarUsuarioForm()
    return render_template('cadastrar-usuario.html', form=form)

@app.route('/listar-usuarios', methods=['GET', 'POST'])
def listar_usuarios():
    data = Usuario.query.all()
    return render_template('listar-usuarios.html', data=data)

@app.route('/excluir-usuario/<int:id>', methods=['GET', 'POST'])
def excluir_usuario(id):
    usuario = Usuario.query.filter_by(id=id).first()
    db.session.delete(usuario)
    db.session.commit()
    data = Usuario.query.all()
    return render_template('listar-usuarios.html', data=data)


if __name__ == '__main__':
    app.run(debug=True)