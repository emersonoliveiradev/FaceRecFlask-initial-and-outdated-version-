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



class Usuario(db.Model):
    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50))
    senha = db.Column(db.String(20))
    cpf = db.Column(db.String(20))
    dt_nascimento = db.Column(db.String(20))
    status = db.Column(db.Boolean())
    pessoa_id = db.Column(db.Integer, db.ForeignKey('pessoas.id'), nullable=True)
    pessoa = db.relationship('Pessoa', backref=db.backref('pessoas', lazy=True))

    def __init__(self, nome, email, senha, cpf, dt_nascimento, status=1):
        super(PessoaFisica, self).__init__(nome)
        self.email = email
        self.senha = senha
        self.cpf = cpf
        self.dt_nascimento = dt_nascimento
        self.pessoa = super().id
        self.status = status

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

