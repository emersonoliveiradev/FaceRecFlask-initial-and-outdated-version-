# -*- coding: utf-8 -*-
from app import db

class Pessoa(db.Model):
    __tablename__ = "pessoas"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50))
    email = db.Column(db.String(50))

    def __init__(self, nome, email):
        self.nome = nome
        self.email = email

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
        return '<Pessoa {}>'.format(self.nome)



class Usuario(db.Model):
    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)
    cpf = db.Column(db.String(20))
    dt_nascimento = db.Column(db.String(20))
    pessoa = db.Column(db.Integer, db.ForeignKey('pessoas.id'), nullable=True)

    def __init__(self, nome, email, cpf, dt_nascimento):
        super(PessoaFisica, self).__init__(nome, email)
        self.cpf = cpf
        self.dt_nascimento = dt_nascimento
        self.pessoa = super().id




