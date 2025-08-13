from flask_login import UserMixin
from datetime import datetime
from app import db
from flask_login import current_user


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)


class Repuesto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(100), unique=True, nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    marca = db.Column(db.String(100), nullable=True)
    modelo = db.Column(db.String(100), nullable=False)
    precio_c = db.Column(db.Integer, nullable=False)
    precio_v = db.Column(db.Integer, nullable=False)
    categorias = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    compatibilidad = db.Column(db.Text)
    fecha_ingreso = db.Column(db.DateTime)
    usuario = db.relationship('User', backref='repuestos')

class Instalacion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    repuesto_id = db.Column(db.Integer, db.ForeignKey('repuesto.id'), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    fecha = db.Column(db.DateTime)
    cantidad = db.Column(db.Integer, default=1)
    precio_c = db.Column(db.Integer, nullable=False)
    precio_v = db.Column(db.Integer, nullable=False)

    repuesto = db.relationship('Repuesto', foreign_keys=[repuesto_id], backref='instalaciones')
    usuario = db.relationship('User', foreign_keys=[usuario_id], backref='instalaciones')

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    usuario = db.relationship('User', backref='categorias')

    repuestos = db.relationship('Repuesto', backref='categoria', lazy=True)
    __table_args__ = (
        db.UniqueConstraint('nombre', 'usuario_id', name='unique_category_per_user'),
    )

class Balance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    marca = db.Column(db.String(100), nullable=False)
    modelo = db.Column(db.String(100), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    precio_c = db.Column(db.Integer, nullable=False)
    precio_v = db.Column(db.Integer, nullable=False)
    ganancia = db.Column(db.Integer, nullable=False)
    usuario = db.relationship('User', backref='balances')
    
