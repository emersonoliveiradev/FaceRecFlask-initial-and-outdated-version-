from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, BooleanField
from wtforms.widgets import TextArea
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField("username", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])
    remember_me = BooleanField("remember_me")

class CadastrarAlgoritmoForm(FlaskForm):
    nome = StringField("nome", validators=[DataRequired()])
    conteudo = StringField("conteudo",  widget=TextArea())
