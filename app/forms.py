from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField
from wtforms import IntegerField, SelectField, TextAreaField, DateField
from wtforms.validators import DataRequired, Email, Length, EqualTo
from app.models import Category

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=64)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=128)])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(), EqualTo('password', message='Las contraseñas deben coincidir')
    ])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    emailname = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RepuestoForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired()])
    categorias = SelectField('Categorías', choices=[])
    precio = IntegerField('Precio', validators=[DataRequired()])
    cantidad = IntegerField('Cantidad', validators=[DataRequired()])
    descripcion = TextAreaField('Descripción')
    fecha_ingreso = DateField('Fecha de ingreso')
    submit = SubmitField('Guardar')

    def __init__(self, *args, **kwargs):
        super(RepuestoForm, self).__init__(*args, **kwargs)
        self.categorias.choices = [(str(c.id), c.nombre) for c in Category.query.all()]


class CategoryForm(FlaskForm):
    nombre = StringField('Nombre de la categoría', validators=[DataRequired()])
    submit = SubmitField('Guardar')