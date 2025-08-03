import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
migrate = Migrate()

def create_app():
    app = Flask(__name__)

    # Escoge la configuración basada en el entorno
    env = os.getenv('FLASK_ENV', 'development')

    if env == 'production':
        app.config.from_object('config.ProductionConfig')
    elif env == 'testing':
        app.config.from_object('config.TestingConfig')
    else:
        app.config.from_object('config.DevelopmentConfig')

    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    from app.models import User, Instalacion

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from app.auth.routes import auth_bp
    from app.main.routes import main_bp
    from app.inventory.routes import inventory_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(inventory_bp)

    return app
