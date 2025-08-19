from flask import Blueprint

servicio_tecnico_bp = Blueprint('servicio_tecnico', __name__, template_folder='../templates/servicio_tecnico')

from . import routes
