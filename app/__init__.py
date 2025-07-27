from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from app.models import db, User

login_manager = LoginManager()
login_manager.login_view = 'auth.login' #redirige a la página de login si no está autenticado

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def create_app():
    app = Flask(__name__)
    app.secret_key = 'Proyecto_seguro'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventario.db'

    db.init_app(app)
    login_manager.init_app(app)

    # Import blueprints
    from app.auth.routes import auth_bp
    from app.main.routes import main_bp
    from app.inventory.routes import inventory_bp

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(inventory_bp)

    return app
