from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.models import Repuesto, Category
from app.models import db
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
@login_required
def index():
    total_repuestos = Repuesto.query.filter_by(usuario_id=current_user.id).count()
    categorias = db.session.query(Repuesto.categorias, db.func.count(Repuesto.id)).filter_by(usuario_id=current_user.id).group_by(Repuesto.categorias).all()
    repuestos_bajos = Repuesto.query.filter(Repuesto.cantidad <= 3, Repuesto.usuario_id == current_user.id).all()
    ultimos_repuestos = Repuesto.query.filter_by(usuario_id=current_user.id).order_by(Repuesto.fecha_ingreso.desc()).limit(5).all()

    # Convertir categorías a diccionario
    cat_dict = {cat: count for cat, count in categorias}

    return render_template('index.html',
                           total_repuestos=total_repuestos,
                           categorias=cat_dict,
                           repuestos_bajos=repuestos_bajos,
                           ultimos_repuestos=ultimos_repuestos)
