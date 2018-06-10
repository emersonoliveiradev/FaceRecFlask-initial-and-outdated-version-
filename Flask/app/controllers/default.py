from app import app, db, login_manager, login_user, logout_user, login_required, current_user
from flask import Flask, render_template, Response, request, redirect, url_for, flash

import os


#Discocery where is the root path of modules
from app.controllers.camera import VideoCamera
from app.controllers.capture import Capture
from app.controllers.recognizer import Recognizer
from app.controllers.generator import Generator

#Forms e Tables
from app.models.forms import LoginForm, CadastrarAlgoritmoForm, CadastrarUsuarioForm, DefinirParametrosForm
from app.models.tables import Algoritmo, Pessoa, Usuario

##################
#Básicas e Câmera#
##################
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


@app.route("/sobre")
def sobre():
    return render_template('sobre.html')


@app.route("/ajuda")
def ajuda():
    return render_template('ajuda.html')


# Receive variable <name>
@app.route('/test', defaults={"name": None})
@app.route('/test/<name>')
def show_name(name):
    return render_template('test.html', name=name)


#######################
#Algoritmos do Usuário##Excluir depois
#######################
@app.route('/crud-algoritmo-velho', methods=['GET', 'POST'])
def cadastrar_algoritmo_velho():
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

@app.route('/atualizar-algoritmo-velho/<int:id>', methods=['GET'])
def atualizar_algoritmo_velho(id):
    if id:
        print("Existe")
    form = CadastrarAlgoritmoForm()
    return render_template('cadastrar-algoritmo.html', form=form)

@app.route('/listar-algoritmos-velho', methods=['GET'])
def listar_algoritmos_velho():
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


##########
# Usuarios#
##########

@app.route("/cadastrar-usuarios", methods=['GET', 'POST'])
def cadastrar_usuarios():
    if request.method == 'POST':
        print("Entrou")
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        cpf = request.form['cpf']
        dt_nascimento = request.form['dt_nascimento']

        if nome and email and senha and cpf and dt_nascimento:
            usuario = Usuario(nome, email, senha, cpf, dt_nascimento)
            db.session.add(usuario)
            db.session.commit()
            flash("Cadastro realizado com sucesso!")
            usuarios = Usuario.query.all()
            return redirect(url_for('listar_usuarios', usuarios=usuarios))
        else:
            flash("Todos os valores são necessarios ao cadastro!")
            usuarios = Usuario.query.all()
            return redirect(url_for('cadastrar_usuarios', usuarios=usuarios))

    form = CadastrarUsuarioForm()
    return render_template('usuario/cadastrar-usuarios.html', form=form)


@app.route('/listar-usuarios', methods=['GET', 'POST'])
def listar_usuarios():
    usuarios = Usuario.query.all()
    return render_template('usuario/listar-usuarios.html', usuarios=usuarios)


@app.route('/excluir-usuario/<int:id>', methods=['GET', 'POST'])
def excluir_usuario(id):
    usuario = Usuario.query.filter_by(id=id).first()
    if usuario:
        db.session.delete(usuario)
        db.session.commit()
        flash("Exclusão realizada com sucesso!")
        usuarios = Usuario.query.all()
        return redirect(url_for('listar_usuarios', usuarios=usuarios))
    else:
        flash("Exclusão não conluída!")
        usuarios = Usuario.query.all()
        return redirect(url_for('listar_usuarios', usuarios=usuarios))


@app.route('/atualizar-usuario/<int:id>', methods=['GET', 'POST'])
@app.route('/atualizar-usuario', methods=['POST'])
def atualizar_usuario(id=None):
    if id != None and request.method == "GET":
        usuario = Usuario.query.filter_by(id=id).first()
        form = CadastrarUsuarioForm()
        return render_template('usuario/atualizar-usuario.html', form=form, usuario=usuario)
    elif request.method == "POST":
        nome = request.form['nome']
        email = request.form['email']
        cpf = request.form['cpf']
        dt_nascimento = request.form['dt_nascimento']
        if nome or email or cpf or dt_nascimento:
            usuario = Usuario.query.filter_by(id=id).first()
            usuario.nome = nome
            usuario.email = email
            usuario.cpf = cpf
            usuario.dt_nacimento = dt_nascimento
            flash("Atualização realizada com sucesso!")
            db.session.commit()
        usuarios = Usuario.query.all()
        return redirect(url_for('listar_usuarios', usuarios=usuarios))



############
#Algortimos#
############
@app.route('/cadastrar-algoritmos', methods=['GET', 'POST'])
def cadastrar_algoritmos():
    if request.method == 'POST':
        nome = request.form['nome']
        algoritmo = request.form['algoritmo']
        usuario = current_user.get_id()

        if nome and algoritmo and usuario:
            algoritmo = Algoritmo(nome, algoritmo, usuario)
            db.session.add(algoritmo)
            db.session.commit()
            flash("Cadastro de algoritmo realizado com sucesso!")
            return redirect(url_for('listar_algoritmos'))

    form = CadastrarAlgoritmoForm()
    return render_template('algoritmo/cadastrar-algoritmos.html', form=form)


@app.route('/listar-algoritmos', methods=['GET'])
def listar_algoritmos():
    algoritmos = Algoritmo.query.filter_by(usuario=current_user.get_id()).all()
    return render_template('algoritmo/listar-algoritmos.html', algoritmos=algoritmos)


@app.route('/excluir-algoritmo/<int:id>', methods=['GET', 'POST'])
def excluir_algoritmo(id):
    algoritmo = Algoritmo.query.filter_by(id=id).first()
    if algoritmo:
        db.session.delete(algoritmo)
        db.session.commit()
        flash("Exclusão realizada com sucesso!")
        return redirect(url_for('listar_algoritmos'))
    else:
        flash("Exclusão não conluída!")
        return redirect(url_for('listar_algoritmos'))


@app.route('/atualizar-algoritmo/<int:id>', methods=['GET', 'POST'])
def atualizar_algoritmo(id=None):
    if id!=None and request.method=="GET":
        algoritmo = Algoritmo.query.filter_by(id=id).first()
        form = CadastrarAlgoritmoForm()
        return render_template('algoritmo/atualizar-algoritmo.html', form=form, algoritmo=algoritmo)
    elif id and request.method=="POST":
        nome = request.form['nome']
        algoritmo_atributo = request.form['algoritmo']
        usuario = request.form['usuario']
        if nome or algoritmo_atributo or usuario:
            algoritmo = Algoritmo.query.filter_by(id=id).first()
            algoritmo.nome = nome
            algoritmo.algoritmo = algoritmo_atributo
            db.session.commit()
            flash("Atualização realizada com sucesso!")
        else:
            flash("Nenhum valor foi alterado!")
        return redirect(url_for('listar_algoritmos'))

    return redirect(url_for('listar_algoritmos'))





################

#Temporario
base_url = "/home/haw/PycharmProjects/FaceRecFlask/.virtualenvs/FaceRecFlask/Flask/app/controllers/algoritmos/"

@app.route('/instanciar-algoritmo/<int:id>', methods=['GET'])
def instanciar_algoritmo(id):
    url_pasta_usuario = base_url + "usuario_" + current_user.get_id() + "_" + current_user.nome
    url_arquivo_usuario = base_url + "usuario_" + current_user.get_id() + "_" + current_user.nome + "/MeusAlgoritmos.py"

    if os.path.isdir(url_pasta_usuario) and os.path.isfile(url_arquivo_usuario):
        arquivo = open(url_arquivo_usuario, "r+")
        """
        Caso eu precise ler o arquivo 
        for linha in arquivo:
            linha = linha.rstrip()
            print(linha)
        """
        #algoritmos = Algoritmo.query.filter_by(id=id, usuario=current_user.get_id()).all()
        algoritmo = Algoritmo.query.filter_by(id=id, usuario=current_user.get_id()).all()

        for a in algoritmo:
            print(a.algoritmo)
            arquivo.write(a.algoritmo)
            arquivo.write('\n\n\n\n')

        arquivo.close()

        import importlib

        #classe = importlib.import_module("app.controllers.algoritmos.usuario_" + current_user.get_id() + "_" + current_user.nome + ".MeusAlgoritmos" + ".Eigenfaces")
        pacote = importlib.import_module("app.controllers.algoritmos.usuario_" + current_user.get_id() + "_" + current_user.nome + ".MeusAlgoritmos")
        print(type(pacote))
        #print(dir(classe))
        #algoritmo_escolhido = pacote.nomeDoAlgoritmo()

        #print(dir(svm))
        algoritmos = Algoritmo.query.filter_by(usuario=current_user.get_id()).all()
        svm="A"
        return render_template('algoritmo/listar-algoritmos.html', algoritmos=algoritmos, svm=svm)
    else:
        os.mkdir(url_pasta_usuario)
        os.system("touch " + url_arquivo_usuario)
        flash("Pasta do usuário e Arquivo do usuário criados com sucesso!")

    return "Ok"



#######################
#crawler_de_algoritmos# Ver aqui
#######################
@app.route('/mapear-algoritmo/<int:id>', methods=['GET'])
def mapear_algoritmo(id):
    url_pasta_usuario = base_url + "usuario_" + current_user.get_id() + "_" + current_user.nome
    url_arquivo_usuario = base_url + "usuario_" + current_user.get_id() + "_" + current_user.nome + "/MeusAlgoritmos.py"

    if os.path.isdir(url_pasta_usuario) and os.path.isfile(url_arquivo_usuario):
        arquivo = open(url_arquivo_usuario, "r+")
        algoritmo = Algoritmo.query.filter_by(id=id, usuario=current_user.get_id()).first()

        meu_algoritmo = algoritmo.algoritmo
        lista_de_parametros = ["ValorA", "ValorB","ValorC","ValorD"]
        """
        mapear e identificar paramentros aqui
        for a in meu_algoritmo:
            
            if a == "<":
                    print(a.number())

        if "<<" in meu_algoritmo:
            print("OK")
    
        Depois só retornar a lista com os parametros            
        """
        print("Entrou")
        form_parametros = DefinirParametrosForm()
        return render_template('algoritmo/parametros.html', form_parametros=form_parametros, parametros=lista_de_parametros)
    else:
        os.mkdir(url_pasta_usuario)
        os.system("touch " + url_arquivo_usuario)
        flash("Pasta do usuário e Arquivo do usuário criados com sucesso!")

    return "Ok"


@app.route('/mapeado-algoritmo/<parametros>', methods=['POST'])
def mapeado_algoritmo(parametros):
    if request.method == "POST":
        print(type(parametros))
        for p in parametros:
            print(request.form[ab])
        return "ok"



@app.route('/instanciar-algoritmo-funciona/<int:id>', methods=['GET'])
def instanciar_algoritmo_funciona(id):
    url_pasta_usuario = base_url + "usuario_" + current_user.get_id() + "_" + current_user.nome
    url_arquivo_usuario = base_url + "usuario_" + current_user.get_id() + "_" + current_user.nome + "/MeusAlgoritmos.py"

    if os.path.isdir(url_pasta_usuario) and os.path.isfile(url_arquivo_usuario):
        arquivo = open(url_arquivo_usuario, "r+")
        """
        Caso eu precise ler o arquivo 
        for linha in arquivo:
            linha = linha.rstrip()
            print(linha)
        """
        # algoritmos = Algoritmo.query.filter_by(id=id, usuario=current_user.get_id()).all()
        algoritmos = Algoritmo.query.filter_by(usuario=current_user.get_id()).all()
        lista_de_algoritmos = []
        for algoritmo in algoritmos:
            lista_de_algoritmos.append(algoritmo)

        for a in lista_de_algoritmos:
            print(a.algoritmo)
            arquivo.write(a.algoritmo)
            arquivo.write('\n\n\n\n')

        arquivo.close()

        import importlib
        algoritmo_escolhido = importlib.import_module(
            "app.controllers.algoritmos.usuario_" + current_user.get_id() + "_" + current_user.nome + ".MeusAlgoritmos")
        # print(dir(algoritmo_escolhido))
        svm = algoritmo_escolhido.SVM()

        # print(dir(svm))
        algoritmos = Algoritmo.query.filter_by(usuario=current_user.get_id()).all()
        return render_template('algoritmo/listar-algoritmos.html', algoritmos=algoritmos, svm=svm)
        # return "OK2"
    else:
        os.mkdir(url_pasta_usuario)
        os.system("touch " + url_arquivo_usuario)
        flash("Pasta do usuário e Arquivo do usuário criados com sucesso!")

    return "Ok"

#########


#Login e Sessão....
#print(current_user.id)
#print(current_user.nome)
#print(current_user.cpf)


#######
#Login#
#######
@login_manager.user_loader
def load_user(id):
    return Usuario.query.filter_by(id=id).first()


@app.route("/login", methods=['GET','POST'])
def login():
    form_login = LoginForm()

    # Login-Manager
    if request.method == "POST":
        if form_login.validate_on_submit():
            usuario = Usuario.query.filter_by(email=form_login.email.data).first()
            flash(usuario.senha)
            if usuario and usuario.senha == form_login.senha.data:
                login_user(usuario, force=True, remember=True)
                flash("Logado!")
                return redirect(url_for("index"))
            else:
                flash("Login Inválido!")
                return redirect(url_for("login"))
    return render_template('login.html', form_login=form_login)


#não tô usando
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





if __name__ == '__main__':
    app.run(debug=True)