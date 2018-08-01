from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, BooleanField
from wtforms.widgets import TextArea
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    email = StringField("email", validators=[DataRequired()])
    senha = PasswordField("senha", validators=[DataRequired()])


class CadastrarAlgoritmoForm(FlaskForm):
    nome = StringField("nome", validators=[DataRequired()])
    usuario = StringField("usuario", validators=[DataRequired()])
    algoritmo = StringField("algoritmo", widget=TextArea())
    #Verificar como definir o valor do form  textarea


class CadastrarUsuarioForm(FlaskForm):
    nome = StringField("email", validators=[DataRequired()])
    email = StringField("email", validators=[DataRequired()])
    senha = PasswordField("senha", validators=[DataRequired()])
    cpf = StringField("email", validators=[DataRequired()])
    dt_nascimento = StringField("email", validators=[DataRequired()])

class DefinirParametrosForm(FlaskForm):
    p1 = StringField("p1", validators=[DataRequired()])
    p2 = StringField("p2", validators=[DataRequired()])
    p3 = StringField("p3", validators=[DataRequired()])

