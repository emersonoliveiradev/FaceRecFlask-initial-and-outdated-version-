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


#Só retirar o Pessoa pra desaparecer a mensagem
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
    __tablename__= "algoritmos"

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
