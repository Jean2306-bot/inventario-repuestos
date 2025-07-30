from flask import Blueprint, render_template
from flask_login import login_required
from app.models import Repuesto
from app.models import db
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
@login_required
def index():
    total_repuestos = Repuesto.query.count()
    categorias = db.session.query(Repuesto.categoria, db.func.count(Repuesto.id)).group_by(Repuesto.categoria).all()
    repuestos_bajos = Repuesto.query.filter(Repuesto.cantidad <= 3).all()
    ultimos_repuestos = Repuesto.query.order_by(Repuesto.fecha_ingreso.desc()).limit(5).all()

    # Convertir categorías a diccionario
    cat_dict = {cat: count for cat, count in categorias}

    return render_template('index.html',
                           total_repuestos=total_repuestos,
                           categorias=cat_dict,
                           repuestos_bajos=repuestos_bajos,
                           ultimos_repuestos=ultimos_repuestos)
