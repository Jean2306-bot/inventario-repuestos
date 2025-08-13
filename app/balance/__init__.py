from flask import Blueprint

balance_bp = Blueprint('balance', __name__, template_folder='../templates/balance')

from . import routes
