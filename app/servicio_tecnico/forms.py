from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField
from wtforms import IntegerField, SelectField, TextAreaField, DateField, DecimalField
from wtforms.validators import DataRequired, Email, Length, EqualTo

class RegisterServicioForm(FlaskForm):
    codigo = StringField('Código', validators=[DataRequired()])
    nombre = StringField('Nombre', validators=[DataRequired()])
    cedula = StringField('Cédula', validators=[DataRequired()])
    numero_cel = StringField('Número de Celular', validators=[DataRequired()])
    marca_cel = StringField('Marca del Celular', validators=[DataRequired()])
    modelo_cel = StringField('Modelo del Celular', validators=[DataRequired()])
    daño = StringField('Daño', validators=[DataRequired()])
    descripcion = StringField('Descripción', validators=[DataRequired()])
    precio = DecimalField('Precio', validators=[DataRequired()], places=2)
    submit = SubmitField('Registrar Servicio')