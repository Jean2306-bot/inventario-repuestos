from flask_login import UserMixin
from datetime import datetime
from app import db
from flask_login import current_user


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)


class Repuesto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    precio = db.Column(db.Integer, nullable=False)
    categoria = db.Column(db.String(50), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    descripcion = db.Column(db.Text)
    fecha_ingreso = db.Column(db.DateTime)

class Instalacion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    repuesto_id = db.Column(db.Integer, db.ForeignKey('repuesto.id'), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    cantidad = db.Column(db.Integer, default=1)
    precio = db.Column(db.Integer, nullable=False)

    repuesto = db.relationship('Repuesto', foreign_keys=[repuesto_id], backref='instalaciones')
    usuario = db.relationship('User', foreign_keys=[usuario_id], backref='instalaciones')

