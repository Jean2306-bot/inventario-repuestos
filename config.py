import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'clave_insegura_dev')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///inventario.db')
    DEBUG = True

class ProductionConfig(Config):
    # Render te pone DATABASE_URL, pero SQLAlchemy requiere "postgresql://" y no "postgres://"
    uri = os.getenv('DATABASE_URL')
    if uri and uri.startswith('postgres://'):
        uri = uri.replace('postgres://', 'postgresql://', 1)
    SQLALCHEMY_DATABASE_URI = uri
    DEBUG = False

class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    TESTING = True
