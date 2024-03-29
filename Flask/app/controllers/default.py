# -*- coding: utf-8 -*-
__autor__ = "Emerson Pereira Oliveira"
__email__ = "emersonhaw@gmail.com"


# Imports essenciais
from app import app, db, login_manager, login_user, logout_user, login_required, current_user
from flask import Flask, render_template, Response, request, redirect, url_for, flash, session


# Descobrir onde está a pasta root dos módulos
from app.controllers.camera import VideoCamera
from app.controllers.capturar import Capturar
from app.controllers.reconhecer import Reconhecer
from app.controllers.gerador import Gerador


# Formulários e tabelas
from app.models.forms import LoginForm, CadastrarAlgoritmoForm, CadastrarUsuarioForm, DefinirParametrosForm, DefinirParametrosExecucaoForm
from app.models.tables import Algoritmo, Pessoa, Usuario, Execucao, ImagemDaExecucao, FaceDaImagemDaExecucao


# Verificar outra alternativa
import os
from datetime import datetime


# Operações com imagens
import cv2


# Login
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
            if usuario and usuario.senha == form_login.senha.data:
                login_user(usuario, force=True, remember=True)
                flash("Seja bem-vindo " + usuario.nome + "!")
                return redirect(url_for("index"))
            else:
                flash("Login Inválido!")
                return redirect(url_for("login"))
    return render_template('login.html', form_login=form_login)


# Cadastrar-se
@app.route("/cadastrar-se")
def cadastrar():
    return render_template('login.html')


@app.route("/logout")
@login_required
def logout():
    if not current_user.get_id():
        return redirect(url_for('login'))
    logout_user()
    return redirect(url_for("index"))


# Início #
@app.route('/home')
@app.route('/index')
@app.route('/')
def index():
    if not current_user.get_id():
        return redirect(url_for('login'))
    return render_template('index.html')


# Criar
@app.route("/sobre")
def sobre():
    return render_template('sobre.html')


# Criar
@app.route("/ajuda")
def ajuda():
    return render_template('ajuda.html')


# (Excesso?) 1.1 - Cria o template captura.html (Ele chama a rota /capturar_face)#
@app.route("/mostrar_captura")
def mostrar_captura():
    if not current_user.get_id():
        return redirect(url_for('login'))
    return render_template('captura.html')


# (Excesso?) 1.2 - Usado pelo mostrar_captura. Retorna a imagem passada pela Função Geradora gen_capturar()#
@app.route('/capturar_face')
def capturar_face():
    if not current_user.get_id():
        return redirect(url_for('login'))
    return Response(gen_capturar(), mimetype='multipart/x-mixed-replace; boundary=frame')


# (Excesso?) 1.3 - Tratamento do frame (detectar olhos e face) e yield gerador
def gen_capturar():
    cap = Capturar()
    while True:
        frame = cap.captura_detectar()
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


# (Excesso?) 2.1 - Cria o template reconhecer.html (Ele chama a rota /gerador_reconhecer_face)#
@app.route('/reconhecer_face')
def reconhecer_face():
    if not current_user.get_id():
        return redirect(url_for('login'))
    return render_template('reconhecer.html')


# (Excesso?) 2.2 - Usado pelo reconhecer_face. Retorna a imagem passada pela Função Geradora gerador_reconhecer_face()
@app.route('/gerador_reconhecer_face')
def gerador_reconhecer_face():
    return Response(gerador_reconhecer(), mimetype='multipart/x-mixed-replace; boundary=frame')


# (Excesso?)2.3 - Tratamento do frame (detectar face e reconhecer)e yield gerador
def gerador_reconhecer():
    rec = Reconhecer()
    while True:
        frame = rec.rec_detectar()
        if frame == False:
            continue
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


# USUÁRIOS
@app.route("/cadastrar-usuarios", methods=['GET', 'POST'])
def cadastrar_usuarios():
    if not current_user.get_id():
        return redirect(url_for('login'))
    if request.method == 'POST':
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
    if not current_user.get_id():
        return redirect(url_for('login'))
    usuarios = Usuario.query.all()
    form = CadastrarUsuarioForm()
    return render_template('usuario/listar-usuarios.html', usuarios=usuarios, form=form)


@app.route('/excluir-usuario/<int:id>', methods=['GET', 'POST'])
def excluir_usuario(id):
    if not current_user.get_id():
        return redirect(url_for('login'))
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
    if not current_user.get_id():
        return redirect(url_for('login'))
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


# ALGORITMOS #
@app.route('/cadastrar-algoritmo', methods=['GET', 'POST'])
def cadastrar_algoritmos():
    if not current_user.get_id():
        return redirect(url_for('login'))
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
    if not current_user.get_id():
        return redirect(url_for('login'))
    algoritmos = Algoritmo.query.filter_by(usuario=current_user.get_id()).all()
    return render_template('algoritmo/listar-algoritmos.html', algoritmos=algoritmos)


@app.route('/excluir-algoritmo/<int:id>', methods=['GET', 'POST'])
def excluir_algoritmo(id):
    if not current_user.get_id():
        return redirect(url_for('login'))
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
    if not current_user.get_id():
        return redirect(url_for('login'))
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



# CONSTANTES
# Caminho raiz da pasta dos algoritmos dentro do sistema
base_url = "/home/emerson/PycharmProjects/FaceRecFlask/FaceRecFlask/Flask/pasta_dos_usuarios/"

# Criar função get_base_url
def get_base_url():
    return "/home/emerson/PycharmProjects/FaceRecFlask/FaceRecFlask/Flask/pasta_dos_usuarios/"

# Criar função get_base_url_pasta
def get_base_url_pasta():
    return get_base_url() + "u_" + current_user.get_id()  + "_" + current_user.nome

# Criar função get_base_url_arquivo_init


# Criar função get_base_url_arquivo_auxiliar
def get_base_url_arquivo_auxiliar():
    return get_base_url() + "u_" + current_user.get_id() + "_" + current_user.nome + "/algoritmos/auxiliar.py"


# Execução
@app.route("/execucao-escolher-algoritmo")
def execucao_escolher_algoritmo():
    url_pasta_usuario = get_base_url_pasta()
    url_arquivo_usuario = get_base_url_arquivo_auxiliar()
    # Fazer apenas uma vez - Colocar todas as criações antes
    arquivo = open(base_url + "/__init__.py", "a+")
    arquivo.write("\nfrom .u_" + current_user.get_id() + "_" + current_user.nome + ".algoritmos.auxiliar import ReconhecimentoFacial")
    arquivo.close()
    ###
    arquivo = open(url_pasta_usuario + "/__init__.py", "w")
    arquivo.write("\nfrom .algoritmos.auxiliar import ReconhecimentoFacial")
    arquivo.close()
    if os.path.isdir(url_pasta_usuario) and os.path.isfile(url_arquivo_usuario):
        pass
    else:
        os.mkdir(url_pasta_usuario)
        #Adicionar o caminho de todos os usuários aqui
        os.system("touch " + base_url + "/__init__.py")
        os.mkdir(url_pasta_usuario + "/algoritmos")
        # Adicionar o caminho de todos os usuários aqui
        os.system("touch " + base_url + "/__init__.py")
        os.mkdir(url_pasta_usuario + "/arquivos-cascade")
        os.mkdir(url_pasta_usuario + "/arquivos-imagem-e-video")
        os.mkdir(url_pasta_usuario + "/arquivos-de-reconhecimento")
        os.mkdir(url_pasta_usuario + "/bancos-de-faces")
        os.system("touch " + url_arquivo_usuario)
        flash("Pasta do usuário e Arquivo do usuário criados com sucesso!")
    form_execucao = DefinirParametrosExecucaoForm()
    return render_template('execucao/execucao-escolher-algoritmo.html', form_execucao=form_execucao)


@app.route('/execucao-mapear-algoritmo', methods=['POST'])
def execucao_mapear_algoritmo():
    if not current_user.get_id():
        return redirect(url_for('login'))

    session["id_usuario"] = current_user.get_id()
    session["id_algoritmo"] = request.form['algoritmos']
    id_algoritmo = request.form['algoritmos']


    url_pasta_usuario = base_url + "u_" + current_user .get_id() + "_" + current_user.nome
    url_arquivo_usuario = base_url + "u_" + current_user.get_id() + "_" + current_user.nome + "/algoritmos/auxiliar.py"


    if os.path.isdir(url_pasta_usuario) and os.path.isfile(url_arquivo_usuario):
        arquivo = open(url_arquivo_usuario, "r+")
        algoritmo = Algoritmo.query.filter_by(id=id_algoritmo, usuario=current_user.get_id()).first()
        meu_algoritmo = algoritmo.algoritmo
        frase = meu_algoritmo
        tamanho = len(frase)
        param = []
        i = 0
        for i in range(0, tamanho):
            if frase[i] == "<":
                if frase[i + 1] == "<":
                    j = i + 2
                    for j in range(j, tamanho):
                        if frase[j] == ">":
                            if frase[j + 1] == ">":
                                novo_parametro = ""             #Limpar a variável
                                for c in range(i + 2, j):
                                    novo_parametro += frase[c]
                                param.append(novo_parametro)
                                break
        form_parametros = DefinirParametrosForm()
        return render_template('algoritmo/parametros.html', form_parametros=form_parametros, parametros=param, id_algoritmo=algoritmo.id)
    else:
        pass
    flash("Pasta do usuário e Arquivo do usuário criados com sucesso!")
    return redirect(url_for('mapear_algoritmo', id=id))


@app.route('/execucao-algoritmo-mapeado', methods=['POST'])
def excecucao_algoritmo_mapeado():
    if not current_user.get_id():
        return redirect(url_for('login'))
    #Remover do HTML. usar o valor da session e fazer a verificação da existência dele
    id_algoritmo = request.form['id_algoritmo']
    if request.method == "POST":
        lista_nome = request.form.getlist("lista_nome[]")
        lista_valor = request.form.getlist("lista_valor[]")
        url_pasta_usuario = base_url + "u_" + current_user.get_id() + "_" + current_user.nome
        url_arquivo_usuario = base_url + "u_" + current_user.get_id() + "_" + current_user.nome + "/algoritmos/auxiliar.py"
        if os.path.isdir(url_pasta_usuario) and os.path.isfile(url_arquivo_usuario):
            arquivo = open(url_arquivo_usuario, "r+")
            algoritmo = Algoritmo.query.filter_by(id=id_algoritmo, usuario=current_user.get_id()).first()
            meu_algoritmo = algoritmo.algoritmo
            i=0
            for p in lista_nome:
                meu_algoritmo = meu_algoritmo.replace("<<" + str(p) + ">>", lista_valor[i])
                i+=1
            arquivo.write(meu_algoritmo)
            arquivo.write('\n\n\n\n')
            arquivo.close()
    return render_template('/execucao/processar-execucao.html')





############################################################################################################
##2.2 - Usado pelo reconhecer_face. Retorna a imagem passada pela Função Geradora gerador_reconhecer_face()#
############################################################################################################
@app.route('/execucao-gerador-processar-execucao')
def execucao_gerador_processar_execucao():
    return Response(execucao_gerador_execucao(id_usuario=session["id_usuario"], id_algoritmo=session["id_algoritmo"], now=datetime.now().strftime('%Y-%m-%d %H:%M:%S')), mimetype='multipart/x-mixed-replace; boundary=frame')


#https://sempreupdate.com.br/python-import-e-chamada-de-metodo-dinamica/
#https://stackoverflow.com/questions/14071135/import-file-using-string-as-name
#http://www.logicus.com.br/alguns-exemplos-do-modulo-sys-no-python/


# Problemas de escopo
def execucao_gerador_execucao(id_usuario, id_algoritmo, now):
    with app.app_context():
        with app.test_request_context():
            session["eu"] = "Emerson"
            caminho = __import__('pasta_dos_usuarios.u_1_Emerson.algoritmos.auxiliar')
            print(dir(caminho))
            rec = getattr(caminho, 'ReconhecimentoFacial')
            rec2 = rec()
            while True:
                lista = rec2.reconhecer_desenhar()
                print(type(lista))
                if lista == "Finalizado":
                    break
                frame = lista['imagem_encode']
                yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
                execucao_processar_execucao_final(lista, id_algoritmo, now)


def execucao_processar_execucao_final(lista, id_algoritmo, now):
    # Depois lembrar de pegar ou em uma sessão ou outra coisa, o algoritmo usado, aalgoritmo, arq_cascade e arq_reconhecimento
    # Recortar faces para salvar no banco de dados
    if lista['s_deteccao'] == True:
        if lista['s_reconhecimento'] == True:
            for face in lista['n_faces']:
                execucao = Execucao(now, id_algoritmo)
                db.session.add(execucao)
                db.session.commit()
                #flash("Cadastro de algoritmo realizado com sucesso!")

@app.route('/execucao-relatorio')
def excecucao_relatorio():
    return render_template('/execucao/execucao-relatorio.html')



# Continuar do relatório... Salvar na seção e no BD.....



# Criar rota para recortar as faces detectadas e salvar
# Depois criar rota para exibir os resultados na tela
# Criar tabela
# Execucao
#   id
#   data
#   algoritmo fk
#   arq_cascade fk
#   arq_reconhecimento fk
#
# Ex_imagens
#   id
#   imagem
#   execucao fk
#   s_deteccao
#
#
# Ex_face_na_imagem
#   id
#   face
#   s_reconhecimento
#   id_reconhecimento
#   conf_reconhecimento
#   imagem fk

#Login e Sessão....
#print(current_user.id)
#print(current_user.nome)
#print(current_user.cpf)

# Ter opção de fazer upload de videos, arqs cascade e yaml


if __name__ == '__main__':
    app.run(debug=True)