from builtins import classmethod

__autor__ = "Emerson Pereira Oliveira"
__email__ = "emersonhaw@gmail.com"

# -*- coding: utf-8 -*-

#####################
##Imports essenciais#
#####################
from app import app, db, login_manager, login_user, logout_user, login_required, current_user
from flask import Flask, render_template, Response, request, redirect, url_for, flash, session

###############################################
##Descobrir onde está a pasta root dos módulos#
###############################################
from app.controllers.camera import VideoCamera
from app.controllers.capturar import Capturar
from app.controllers.reconhecer import Reconhecer
from app.controllers.gerador import Gerador



########################
##Formulários e tabelas#
########################
from app.models.forms import LoginForm, CadastrarAlgoritmoForm, CadastrarUsuarioForm, DefinirParametrosForm, DefinirParametrosExecucaoForm
from app.models.tables import Algoritmo, Pessoa, Usuario, Execucao, ImagemDaExecucao, FaceDaImagemDaExecucao

##############################
##Verificar outra alternativa#
##############################
import os
from datetime import datetime

##########
## Operações nas imagens
#############
import cv2


##########
##Básicas#
##########
@app.route('/home')
@app.route('/index')
@app.route('/')
def index():
    if not current_user.get_id():
        return redirect(url_for('login'))
    session["num"] = "Simmmmmmmmmmmmmmmmmmmmmmm"
    print(session["num"])
    return render_template('index.html')

########
##Criar#
########
@app.route("/sobre")
def sobre():
    return render_template('sobre.html')

########
##Criar#
########
@app.route("/ajuda")
def ajuda():
    return render_template('ajuda.html')


#########
##Câmera#
#########

#######################################################################
##1.1 - Cria o template captura.html (Ele chama a rota /capturar_face)#
#######################################################################
@app.route("/mostrar_captura")
def mostrar_captura():
    if not current_user.get_id():
        return redirect(url_for('login'))
    return render_template('captura.html')


#################################################################################################
##1.2 - Usado pelo mostrar_captura. Retorna a imagem passada pela Função Geradora gen_capturar()#
#################################################################################################
@app.route('/capturar_face')
def capturar_face():
    if not current_user.get_id():
        return redirect(url_for('login'))
    return Response(gen_capturar(), mimetype='multipart/x-mixed-replace; boundary=frame')


####################################################################
##1.3 - Tratamento do frame (detectar olhos e face) e yield gerador#
####################################################################
def gen_capturar():
    cap = Capturar()
    while True:
        # Chamo a função capturar
        frame = cap.captura_detectar()
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


####################################################################################
##2.1 - Cria o template reconhecer.html (Ele chama a rota /gerador_reconhecer_face)#
####################################################################################
@app.route('/reconhecer_face')
def reconhecer_face():
    if not current_user.get_id():
        return redirect(url_for('login'))
    return render_template('reconhecer.html')


############################################################################################################
##2.2 - Usado pelo reconhecer_face. Retorna a imagem passada pela Função Geradora gerador_reconhecer_face()#
############################################################################################################
@app.route('/gerador_reconhecer_face')
def gerador_reconhecer_face():
    return Response(gerador_reconhecer(), mimetype='multipart/x-mixed-replace; boundary=frame')


########################################################################
##2.3 - Tratamento do frame (detectar face e reconhecer)e yield gerador#
########################################################################
def gerador_reconhecer():
    rec = Reconhecer()
    while True:
        frame = rec.rec_detectar()
        if frame == False:
            continue
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


#######################
##Original - Não usado#
#######################
@app.route('/video_feed')
def video_feed():
    #Retorna o que o gerador (função gen()) está gerando
    return Response(gen(VideoCamera()), mimetype='multipart/x-mixed-replace; boundary=frame')


###########
##Original#
###########
def gen(camera):
    while True:
        frame = camera.get_encoded_frame()
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


###########
##Usuarios#
###########
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


############
#Algoritmos#
############
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
    return render_template('algoritmo/cadastrar-pasta_dos_usuarios.html', form=form)


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



########################################################
##Caminho raiz da pasta dos algoritmosdentro do sistema#
########################################################
base_url = "/home/emerson/PycharmProjects/FaceRecFlask/FaceRecFlask/Flask/pasta_dos_usuarios/"


##################################################################
##Mapeamento dos parâmetros da função criada pelo usuário - Busca#
##################################################################
@app.route('/execucao-mapear-algoritmo/<int:id>', methods=['GET'])
def mapear_algoritmo(id):
    if not current_user.get_id():
        return redirect(url_for('login'))

    url_pasta_usuario = base_url + "u_" + current_user.get_id() + "_" + current_user.nome
    url_arquivo_usuario = base_url + "u_" + current_user.get_id() + "_" + current_user.nome + "/algoritmos/auxiliar.py"

    # Existe a pasta e o arquivo?
    if os.path.isdir(url_pasta_usuario) and os.path.isfile(url_arquivo_usuario):
        arquivo = open(url_arquivo_usuario, "r+")
        algoritmo = Algoritmo.query.filter_by(id=id, usuario=current_user.get_id()).first()

        meu_algoritmo = algoritmo.algoritmo
        # Lista_de_parametros = ["ValorA", "ValorB","ValorC","ValorD", "ValorE"]

        # Mapear e identificar paramentros aqui
        frase = meu_algoritmo
        tamanho = len(frase)
        param = []
        i = 0

        # Vasculha o código atrás das bandeiras
        # Definido onde está a "bandeira" dos parâmetros definidos
        # Extrai o nome do parâmetro
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
        #Template que mostra os nomes dos parâmetros e os campos vazios pra preencher
        return render_template('algoritmo/parametros.html', form_parametros=form_parametros, parametros=param, id_algoritmo=algoritmo.id)
    else:
        #Criar a pasta do usuário e o arquivo
        os.mkdir(url_pasta_usuario)
        os.mkdir(url_pasta_usuario + "/algoritmos")
        os.mkdir(url_pasta_usuario + "/arquivos-cascade")
        os.mkdir(url_pasta_usuario + "/arquivos-imagem-e-video")
        os.mkdir(url_pasta_usuario + "/arquivos-de-reconhecimento")
        os.mkdir(url_pasta_usuario + "/bancos-de-faces")
        os.system("touch " + url_arquivo_usuario)

        flash("Pasta do usuário e Arquivo do usuário criados com sucesso!")
        return redirect(url_for('mapear_algoritmo', id=id))

########################################
# Segunda parte do mapeamento - Escrita#
########################################
@app.route('/mapeado-algoritmo/<int:id>', methods=['POST'])
def mapeado_algoritmo(id):
    if not current_user.get_id():
        return redirect(url_for('login'))

    if request.method == "POST":
        #Pegar as listas que criei no template, de nome e valor - OK
        lista_nome = request.form.getlist("lista_nome[]")
        lista_valor = request.form.getlist("lista_valor[]")
        #Acesso pelo Índice - print(lista_nome[1]) -
        print(lista_nome)
        print(lista_valor)

        url_pasta_usuario = base_url + "u_" + current_user.get_id() + "_" + current_user.nome
        url_arquivo_usuario = base_url + "u_" + current_user.get_id() + "_" + current_user.nome + "/algoritmos/auxiliar.py"

        if os.path.isdir(url_pasta_usuario) and os.path.isfile(url_arquivo_usuario):
            print("Foi Aqui - Agora resta a função de substituição dos parâmetros pelos valores")
            arquivo = open(url_arquivo_usuario, "r+")
            algoritmo = Algoritmo.query.filter_by(id=id, usuario=current_user.get_id()).first()
            meu_algoritmo = algoritmo.algoritmo

            # frase2 = ["param1", "param2", "param3", "param4"]
            i=0
            for p in lista_nome:
                #meu_algoritmo = meu_algoritmo.replace("<<" + str(p) + ">>", str(p) + "=" + lista_valor[i])
                meu_algoritmo = meu_algoritmo.replace("<<" + str(p) + ">>", lista_valor[i])
                print(meu_algoritmo)
                i+=1

            arquivo.write(meu_algoritmo)
            arquivo.write('\n\n\n\n')
            arquivo.close()

    return "ok-Sim"
    #return redirect(url_for('instanciar_algoritmo_funciona', id=id, lista_nome=lista_nome, lista_valor=lista_valor))
    #return "ok - O mapeamento está ok... Continuar a partir daqui para a rota de Instancia de algoritmo"
#










#############################Importante
###########Continuar daqui
# Processar a execução
####################################################################################
##2.1 - Cria o template processar-execucao.html (Ela chama a rota ZZZZZZZZ#
####################################################################################
@app.route('/processar-execucao', methods=['GET','POST'])
def processar_execucao():
    if not current_user.get_id():
        return redirect(url_for('login'))
    return render_template('/execucao/processar-execucao.html')


############################################################################################################
##2.2 - Usado pelo reconhecer_face. Retorna a imagem passada pela Função Geradora gerador_reconhecer_face()#
############################################################################################################
@app.route('/gerador-processar-execucao')
def gerador_processar_execucao():
    return Response(gerador_execucao(), mimetype='multipart/x-mixed-replace; boundary=frame')

########################################################################
##2.3 - Tratamento do frame (detectar face e reconhecer)e yield gerador#
########################################################################
def gerador_execucao():
    #rec = Reconhecer()
    from app.controllers.pasta_dos_usuarios.u_1_Emerson.algoritmos.auxiliar import ReconhecimentoFacial
    rec = ReconhecimentoFacial()
    while True:
        lista = rec.reconhecer_desenhar()
        if lista == "Finalizado":
            #Terminou
            pass
        frame = lista['imagem_encode']
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        processar_execucao_final(lista)




def processar_execucao_final(lista):
    # Depois lembrar de pegar ou em uma sessão ou outra coisa, o algoritmo usado, aalgoritmo, arq_cascade e arq_reconhecimento
    # Recortar faces para salvar no banco de dados
    if lista['s_deteccao'] == True:
        if lista['s_reconhecimento'] == True:
            for face in lista['n_faces']:
                print("Achou - " + str(face[0]))
                print("Achou - " + str(face[1]))
                print("Achou - " + str(face[2]))

                #
                # Ver como se cria uma sessão e criar uma apenas para o algoritmo usado, algoritmo, arq_cascade e arq_reconhecimento
                # e demais dados informado no mapeamento

                execucao = Execucao("Data", algoritmo, usuario)
                db.session.add(algoritmo)
                db.session.commit()
                flash("Cadastro de algoritmo realizado com sucesso!")

    # Salvar tudo






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










#Ignorar esse
@app.route('/instanciar-algoritmo-funciona/<int:id>', methods=['GET'])
def instanciar_algoritmo_funciona(id):
    if not current_user.get_id():
        return redirect(url_for('login'))

    url_pasta_usuario = base_url + "u_" + current_user.get_id() + "_" + current_user.nome
    url_arquivo_usuario = base_url + "u_" + current_user.get_id() + "_" + current_user.nome + "/algoritmos/auxiliar.py"

    if os.path.isdir(url_pasta_usuario) and os.path.isfile(url_arquivo_usuario):
        arquivo = open(url_arquivo_usuario, "r+")
        #Retorna um objeto do tipo Algoritmo com seus atributos (id, nome, algoritmo, usuario)
        algoritmo = Algoritmo.query.filter_by(usuario=current_user.get_id(), id=id).first()

        #Receber os demais valores do url_for()

        print("Aqui46")
        #lista_nome = request.form.getlist('lista_nome[0]')
        #lista_valor = request.form.getlist('lista_valor')
        print(id)
        #print(listar_valor)
        #print(algoritmo.algoritmo)

        #frase2 = ["param1", "param2", "param3", "param4"]
        #for p in param:
            #frase = frase.replace("<<" + str(p) + ">>", frase2[1])


        arquivo.write(algoritmo.algoritmo)
        arquivo.write('\n\n\n\n')
        arquivo.close()
    else:
        os.mkdir(url_pasta_usuario)
        os.system("touch " + url_arquivo_usuario)
        flash("Pasta do usuário e Arquivo do usuário criados com sucesso!")

    return "Ok2"



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
            if usuario and usuario.senha == form_login.senha.data:
                login_user(usuario, force=True, remember=True)
                flash("Seja bem-vindo " + usuario.nome + "!")
                return redirect(url_for("index"))
            else:
                flash("Login Inválido!")
                return redirect(url_for("login"))

    return render_template('login.html', form_login=form_login)


#não tô usando
@app.route("/usuarios")
def logando():
    if not current_user.get_id():
        return redirect(url_for('login'))

    usuario = Usuario.query.filter_by(senha='123').first()
    #Adiciona todos os dados do bd da pesssoa
    login_user(usuario)
    return "Está logado"


@app.route("/logout")
@login_required
def logout():
    if not current_user.get_id():
        return redirect(url_for('login'))

    logout_user()
    return redirect(url_for("index"))


@app.route("/atual")
@login_required
def atual():
    if not current_user.get_id():
        return redirect(url_for('login'))

    return "Atual: " + current_user.nome

##############
#Cadastrar-se#
##############
@app.route("/cadastrar-se")
def cadastrar():
    return render_template('login.html')










#############
#Execução####
#############
@app.route("/execucao-escolher-algoritmo")
def execucao_escolher_algoritmo():
    url_pasta_usuario = base_url + "u_" + current_user.get_id() + "_" + current_user.nome
    url_arquivo_usuario = base_url + "u_" + current_user.get_id() + "_" + current_user.nome + "/algoritmos/auxiliar.py"

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

# Ter opção de fazer upload de videos, arqs cascade e yaml
@app.route('/execucao-mapear-algoritmo', methods=['POST'])
def execucao_mapear_algoritmo():
    if not current_user.get_id():
        return redirect(url_for('login'))

    session["id_usuario"] = current_user.get_id()
    session["id_algoritmo"] = request.form['algoritmos']
    id_algoritmo = request.form['algoritmos']


    url_pasta_usuario = base_url + "u_" + current_user.get_id() + "_" + current_user.nome
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

    #Remover do HTML. usar o valor da session e fazer a verificação da existẽncia dele
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
            #print(session)

            #caminho = "app.controllers.pasta_dos_usuarios.u_ " + "" + id_usuario + "_Emerson.algoritmos.auxiliar"
            #print(caminho)
            #from app.controllers.pasta_dos_usuarios.u_1_Emerson.algoritmos.auxiliar import ReconhecimentoFacial
            #Fazer  isso ficar variável - id_usuário
            #caminho = __import__('pasta.auxiliar')
            caminho = __import__('pasta_dos_usuarios.u_1_Emerson.algoritmos.auxiliar')
            print(dir(caminho))
            rec = getattr(caminho, 'ReconhecimentoFacial')
            rec2 = rec()

            #from caminho import ReconhecimentoFacial

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



# Continuar do relatório... SAlvar na seção e no BD





if __name__ == '__main__':
    app.run(debug=True)