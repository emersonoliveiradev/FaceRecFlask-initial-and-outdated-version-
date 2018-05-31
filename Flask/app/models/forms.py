from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, BooleanField
from wtforms.widgets import TextArea
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    email = StringField("email", validators=[DataRequired()])
    senha = PasswordField("senha", validators=[DataRequired()])


class CadastrarAlgoritmoForm(FlaskForm):
    nome = StringField("nome", validators=[DataRequired()])
    conteudo = StringField("conteudo",  widget=TextArea())
