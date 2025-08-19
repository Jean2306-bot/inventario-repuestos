from flask_login import current_user
from app import db

class Reparacion(db.Model):
    __tablename__ = 'reparaciones'
    id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(200), nullable=False)
    fecha = db.Column(db.DateTime, nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    usuario = db.relationship('User', back_populates='reparaciones')