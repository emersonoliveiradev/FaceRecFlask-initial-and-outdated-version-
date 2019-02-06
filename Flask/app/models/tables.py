# -*- coding: utf-8 -*-
from app import db


class Pessoa(db.Model):
    __tablename__ = "pessoas"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50))

    def __init__(self, nome):
        self.nome = nome

    def __repr__(self):
        return '<Pessoa {}>'.format(self.nome)


# Só retirar o Pessoa pra desaparecer a mensagem
class Usuario(Pessoa, db.Model):
    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50))
    senha = db.Column(db.String(20))
    cpf = db.Column(db.String(20))
    dt_nascimento = db.Column(db.String(20))
    status = db.Column(db.Boolean())
    pessoa = db.Column(db.Integer, db.ForeignKey('pessoas.id'))

    def __init__(self, nome, email, senha, cpf, dt_nascimento):
        super(Usuario, self).__init__(nome)
        self.email = email
        self.senha = senha
        self.cpf = cpf
        self.dt_nascimento = dt_nascimento
        self.pessoa = super().id
        self.status = 1

    # Métodos para gerenciamento do Flask-login
    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return '<Usuario {}>'.format(self.cpf)


class Algoritmo(db.Model):
    __tablename__ = "algoritmos"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(20))
    algoritmo = db.Column(db.Text)
    usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id'))

    def __init__(self, nome, algoritmo, usuario):
        self.nome = nome
        self.algoritmo = algoritmo
        self.usuario = usuario

    def __repr__(self):
        return '<Algoritmo {}>'.format(self.nome)


class Execucao(db.Model):
    __tablename__ = "execucoes"

    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(20))
    algoritmo = db.Column(db.Integer, db.ForeignKey('algoritmos.id'))

    # arquivo_de_detecao = db.Column(db.Integer, db.ForeignKey('arquivos_de_detecao.id'))
    # arquivo_de_reconhecimento = db.Column(db.Integer, db.ForeignKey('arquivos_de_reconhecimento.id'))

    def __init__(self, data, algoritmo):
        self.data = data
        self.algoritmo = algoritmo

    def __repr__(self):
        return '<Execucao {}>'.format(self.id)


class ImagemDaExecucao(db.Model):
    __tablename__ = "imagens_da_execucao"

    id = db.Column(db.Integer, primary_key=True)
    imagem = db.Column(db.String(500))
    execucao = db.Column(db.Integer, db.ForeignKey('execucoes.id'))

    def __init__(self, imagem, execucao):
        self.imagem = imagem
        self.execucao = execucao

    def __repr__(self):
        return '<Imagem da Execucao {}>'.format(self.id)


class FaceDaImagemDaExecucao(db.Model):
    __tablename__ = "faces_da_imagem_da_execucao"

    id = db.Column(db.Integer, primary_key=True)
    face = db.Column(db.String(500))
    id_reconhecimento = db.Column(db.String(10))
    confianca_reconhecimento = db.Column(db.String(10))
    imagem = db.Column(db.Integer, db.ForeignKey('imagens_da_execucao.id'))

    def __init__(self, face, id_reconhecimento, confianca_reconhecimento, imagem):
        self.face = face
        self.id_reconhecimento = id_reconhecimento
        self.confianca_reconhecimento = confianca_reconhecimento
        self.imagem = imagem

    def __repr__(self):
        return '<Face da Imagem da Execucao {}>'.format(self.id)
