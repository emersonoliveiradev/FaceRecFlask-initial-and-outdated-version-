from flask import Flask

#Create to interpreter of python, control the all aplication
app = Flask(__name__)

from app.controllers import default