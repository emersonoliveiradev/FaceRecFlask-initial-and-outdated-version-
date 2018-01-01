from flask import Flask
from flask_sqlalchemy import SQLAlchemy

#Create to interpreter of python, control the all aplication
app = Flask(__name__)

#Create config of db and db
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///storage.db'
db = SQLAlchemy(app)


from app.controllers import default