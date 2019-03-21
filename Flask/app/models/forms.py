from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, BooleanField, SubmitField
from wtforms.widgets import TextArea
from wtforms.validators import DataRequired

from wtforms.ext.sqlalchemy.fields import QuerySelectField
from app.models.tables import Usuario, Algoritmo
from app import current_user


class LoginForm(FlaskForm):
    email = StringField("email", validators=[DataRequired()])
    senha = PasswordField("senha", validators=[DataRequired()])


class CadastrarAlgoritmoForm(FlaskForm):
    nome = StringField("nome", validators=[DataRequired()])
    usuario = StringField("usuario", validators=[DataRequired()])
    algoritmo = StringField("algoritmo", widget=TextArea())
    # Verificar como definir o valor do form  textarea


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


class DefinirParametrosExecucaoForm(FlaskForm):
    StringField("email", validators=[DataRequired()])
    usuarios = QuerySelectField('Usuario', default=current_user)
    algoritmos = QuerySelectField('Algoritmo',
                                  query_factory=lambda: Algoritmo.query.filter_by(usuario=current_user.get_id()),
                                  get_label='nome', allow_blank=True,
                                  blank_text=(u'Selecione um algoritmo'), get_pk=lambda x: x.id)
    enviar = SubmitField("Enviar")
