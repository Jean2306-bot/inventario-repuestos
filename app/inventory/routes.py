from flask import Blueprint

inventory_bp = Blueprint('inventory', __name__, url_prefix='/inventory')
@inventory_bp.route('/')
def inventory():
    return "Inventory Page"