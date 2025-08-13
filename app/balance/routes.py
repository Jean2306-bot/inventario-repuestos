from app.models import Instalacion, Repuesto, db
from sqlalchemy import func
from flask_login import current_user
from flask import Blueprint, render_template
from flask_login import login_required
from . import balance_bp

@balance_bp.route('/balance')
@login_required
def balance():
    # Ganancias totales = (precio venta - precio compra) * cantidad instalada
    ganancias_totales = db.session.query(
        func.sum((Instalacion.precio_v - Instalacion.precio_c) * Instalacion.cantidad)
    ).filter_by(usuario_id=current_user.id).scalar() or 0

    # Ventas totales = precio venta * cantidad instalada
    ventas_totales = db.session.query(
        func.sum(Instalacion.precio_v * Instalacion.cantidad)
    ).filter_by(usuario_id=current_user.id).scalar() or 0

    # Capital invertido en inventario actual
    capital_inventario = db.session.query(
        func.sum(Repuesto.cantidad * Repuesto.precio_c)
    ).filter_by(usuario_id=current_user.id).scalar() or 0

    # Valor de venta del inventario actual
    valor_inventario = db.session.query(
        func.sum(Repuesto.cantidad * Repuesto.precio_v)
    ).filter_by(usuario_id=current_user.id).scalar() or 0

    return render_template(
        'balance/balance.html',
        ganancias=ganancias_totales,
        ventas=ventas_totales,
        capital=capital_inventario,
        valor_inventario=valor_inventario
    )

