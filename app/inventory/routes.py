from flask import Blueprint, render_template, redirect, url_for, request, flash
from app.models import db, Repuesto, Instalacion
from app.forms import RepuestoForm
from flask_login import login_required, current_user


inventory_bp = Blueprint('inventory', __name__, url_prefix='/inventory')

@inventory_bp.route('/')
@login_required
def lista():
    filtro = request.args.get('filtro')
    categoria = request.args.get('categoria')
    busqueda = request.args.get('busqueda')

    query = Repuesto.query

    if filtro == 'bajos':
        query = query.filter(Repuesto.cantidad <= 3).order_by(Repuesto.cantidad.asc())
    else:
        query = query.order_by(Repuesto.nombre.asc())

    if categoria and categoria != 'Todas':
        query = query.filter(Repuesto.categoria == categoria)

    if busqueda:
        query = query.filter(Repuesto.nombre.ilike(f"%{busqueda}%"))

    repuestos = query.all()

    return render_template('inventory/lista.html', repuestos=repuestos)

@inventory_bp.route('/nuevo', methods=['GET', 'POST'])
@login_required
def nuevo():
    form = RepuestoForm()
    if form.validate_on_submit():
        repuesto = Repuesto(
            nombre=form.nombre.data,
            categoria=form.categoria.data,
            precio=form.precio.data,
            cantidad=form.cantidad.data,
            descripcion=form.descripcion.data,
            fecha_ingreso=form.fecha_ingreso.data
        )
        db.session.add(repuesto)
        db.session.commit()
        flash('Repuesto agregado exitosamente!', 'success')
        return redirect(url_for('inventory.lista'))
    return render_template('inventory/formulario_repuesto.html', form=form)

@inventory_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar(id):
    repuesto = Repuesto.query.get_or_404(id)
    form = RepuestoForm(obj=repuesto)
    if form.validate_on_submit():
        repuesto.nombre = form.nombre.data
        repuesto.precio = form.precio.data
        repuesto.categoria = form.categoria.data
        repuesto.cantidad = form.cantidad.data
        repuesto.descripcion = form.descripcion.data
        repuesto.fecha_ingreso = form.fecha_ingreso.data
        db.session.commit()
        flash('Repuesto actualizado exitosamente!', 'success')
        return redirect(url_for('inventory.lista'))
    return render_template('inventory/formulario_repuesto.html', form=form, repuesto=repuesto)

@inventory_bp.route('/eliminar/<int:id>')
@login_required
def eliminar(id):
    repuesto = Repuesto.query.get_or_404(id)
    db.session.delete(repuesto)
    db.session.commit()
    flash('Repuesto eliminado exitosamente!', 'success')
    return redirect(url_for('inventory.lista'))

@inventory_bp.route('/instalados/agregar/<int:id>')
@login_required
def agregar_instalacion(id):
    repuesto = Repuesto.query.get_or_404(id)
    
    if repuesto.cantidad < 1:
        flash('No hay suficiente stock de este repuesto.', 'warning')
        return redirect(url_for('inventory.lista'))

    # Crear nueva instalación
    nueva_instalacion = Instalacion(
        repuesto_id=repuesto.id,
        usuario_id=current_user.id,
        cantidad=1,
        precio=repuesto.precio
    )

    repuesto.cantidad -= 1  # Descontar del inventario
    db.session.add(nueva_instalacion)
    db.session.commit()

    flash(f'Repuesto "{repuesto.nombre}" marcado como instalado.', 'success')
    return redirect(url_for('inventory.lista'))

@inventory_bp.route('/instalados')
@login_required
def ver_instalados():
    instalaciones = Instalacion.query.order_by(Instalacion.fecha.desc()).all()
    return render_template('inventory/instalados.html', instalaciones=instalaciones)


@inventory_bp.route('/instalados/instalar', methods=['POST'])
@login_required
def instalar_repuesto():
    id = request.form.get('id')
    repuesto = Repuesto.query.get_or_404(id)
    if repuesto.cantidad > 0:
        repuesto.cantidad -= 1
        db.session.commit()
    return redirect(url_for('inventory.ver_instalados'))
