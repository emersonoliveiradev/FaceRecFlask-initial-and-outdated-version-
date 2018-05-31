from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin

#Create to interpreter of python, control the all aplication
app = Flask(__name__)

#Create config of db and db
app.config.from_object('config')
db = SQLAlchemy(app)

#Create instance migrate - Aplication and my DataBase
migrate = Migrate(app, db)

#Create instance manager - Commands for initializing
manager = Manager(app)
manager.add_command('db', MigrateCommand)
manager.add_command('runserver', Server(host="0.0.0.0", port=8000))

#Instância da Login-Manager
login_manager = LoginManager()
login_manager.init_app(app)

from app.controllers import default
from app.models import tables