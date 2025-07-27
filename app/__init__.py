from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login' #redirige a la página de login si no está autenticado

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'proyecto_secreto')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../instance/app.sqlite'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    login_manager.init_app(app)

    # Import blueprints
    from .auth import routes as auth_routes
    from .main import routes as main_routes
    from .inventory import routes as inventory_routes

    # Register blueprints
    app.register_blueprint(auth_routes.auth_bp)
    app.register_blueprint(main_routes.main_bp)
    app.register_blueprint(inventory_routes.inventory_bp)

    return app
