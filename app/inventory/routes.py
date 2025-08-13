from flask import Blueprint, render_template, redirect, url_for, request, flash
from app.models import db, Repuesto, Instalacion, Category
from app.forms import RepuestoForm, CategoryForm
from flask_login import login_required, current_user
from datetime import datetime
import pytz
from flask import send_file
import io
from openpyxl import Workbook
from sqlalchemy import or_

inventory_bp = Blueprint('inventory', __name__, url_prefix='/inventory')

@inventory_bp.route('/')
@login_required
def lista():
    filtro = request.args.get('filtro')
    categoria_nombre = request.args.get('categorias')
    busqueda = request.args.get('busqueda')
    codigo = request.args.get('codigo')

    query = Repuesto.query.filter(Repuesto.usuario_id == current_user.id)

    # Filtro por cantidad baja
    if filtro == 'bajos':
        query = query.filter(Repuesto.cantidad <= 3).order_by(Repuesto.cantidad.asc())
    else:
        query = query.order_by(Repuesto.modelo.asc())


    if categoria_nombre and categoria_nombre != 'Todas':
        query = query.join(Category).filter(
            Category.nombre == categoria_nombre,
            Category.usuario_id == current_user.id
        )


    # Filtro por búsqueda
    if busqueda:
        query = query.filter(or_(
            Repuesto.modelo.ilike(f"%{busqueda}%"),
            Repuesto.marca.ilike(f"%{busqueda}%"),
            Repuesto.compatibilidad.ilike(f"%{busqueda}%"),
            Repuesto.codigo.ilike(f"%{busqueda}%")
        ))

    repuestos = query.all()
    categorias = Category.query.filter_by(usuario_id=current_user.id).all()  # Para mostrar el filtro dinámico

    return render_template('inventory/lista.html', repuestos=repuestos, categorias=categorias)

@inventory_bp.route('/nuevo', methods=['GET', 'POST'])
@login_required
def nuevo():
    form = RepuestoForm(usuario_id=current_user.id)

    if form.validate_on_submit():
        repuesto = Repuesto(
            codigo = form.codigo.data,
            marca = form.marca.data,
            modelo = form.modelo.data,
            categorias = form.categorias.data,
            precio_c = form.precio_c.data,
            precio_v = form.precio_v.data,
            cantidad = form.cantidad.data,
            compatibilidad = form.compatibilidad.data,
            fecha_ingreso = form.fecha_ingreso.data,
            usuario_id = current_user.id
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
    form = RepuestoForm(usuario_id=current_user.id, obj=repuesto)
    if form.validate_on_submit():
        repuesto.codigo = form.marca.data
        repuesto.marca = form.marca.data
        repuesto.modelo = form.modelo.data
        repuesto.precio_c = form.precio_c.data
        repuesto.precio_v = form.precio_v.data
        repuesto.categorias = form.categorias.data
        repuesto.cantidad = form.cantidad.data
        repuesto.compatibilidad = form.compatibilidad.data
        repuesto.fecha_ingreso = form.fecha_ingreso.data
        db.session.commit()
        flash('Repuesto actualizado exitosamente!', 'success')
        return redirect(url_for('inventory.lista'))
    return render_template('inventory/formulario_repuesto.html', form=form, repuesto=repuesto)

@inventory_bp.route('/eliminar/<int:id>')
@login_required
def eliminar(id):
    repuesto = Repuesto.query.get_or_404(id)
    #verificar que el repuesto pertenece al usuario actual
    if repuesto.usuario_id != current_user.id:
        flash('No tienes permiso para eliminar este repuesto.', 'danger')
        return redirect(url_for('inventory.lista'))
    # Verificar si el repuesto tiene instalaciones asociadas
    if repuesto.instalaciones:
        flash('No se puede eliminar un repuesto con instalaciones asociadas.', 'danger')
        return redirect(url_for('inventory.lista'))
    db.session.delete(repuesto)
    db.session.commit()
    flash('Repuesto eliminado exitosamente!', 'success')
    return redirect(url_for('inventory.lista'))

@inventory_bp.route('/ver/<int:id>')
@login_required
def ver(id):
    repuesto = Repuesto.query.get_or_404(id)
    # Verificar que el repuesto pertenece al usuario actual
    if repuesto.usuario_id != current_user.id:
        flash('No tienes permiso para ver este repuesto.', 'danger')
        return redirect(url_for('inventory.lista'))
    return render_template('inventory/ver_repuesto.html', repuesto=repuesto)

@inventory_bp.route('/instalados/agregar/<int:id>')
@login_required
def agregar_instalacion(id):
    repuesto = Repuesto.query.get_or_404(id)

    # Verificar que el repuesto pertenece al usuario actual
    if repuesto.usuario_id != current_user.id:
        flash('No tienes permiso para instalar este repuesto.', 'danger')
        return redirect(url_for('inventory.lista'))
    
    if repuesto.cantidad < 1:
        flash('No hay suficiente stock de este repuesto.', 'warning')
        return redirect(url_for('inventory.lista'))

    # Crear nueva instalación
    colombia_tz = pytz.timezone("america/bogota")
    fecha_colombia = datetime.now(colombia_tz)

    nueva_instalacion = Instalacion(
        repuesto_id = repuesto.id,
        usuario_id = current_user.id,
        cantidad = 1,
        fecha = fecha_colombia,
        precio_c = repuesto.precio_c,
        precio_v = repuesto.precio_v
    )

    repuesto.cantidad -= 1  # Descontar del inventario
    db.session.add(nueva_instalacion)
    db.session.commit()

    flash(f'Repuesto "{repuesto.modelo}" marcado como instalado.', 'success')
    return redirect(url_for('inventory.lista'))

@inventory_bp.route('/instalados')
@login_required
def ver_instalados():
    instalaciones = Instalacion.query.filter_by(usuario_id=current_user.id)\
        .order_by(Instalacion.fecha.desc()).all()
    return render_template('inventory/instalados.html', instalaciones=instalaciones)

@inventory_bp.route('/instalados/eliminar/<int:id>', methods=['POST'])
@login_required
def eliminar_instalacion(id):
    instalacion = Instalacion.query.get_or_404(id)

    if instalacion.usuario_id != current_user.id:
        flash("No tienes permiso para eliminar esta instalación.", "danger")
        return redirect(url_for('inventory.ver_instalados'))

    # 1️⃣ Obtener el repuesto asociado
    repuesto = Repuesto.query.get(instalacion.repuesto_id)

    if repuesto:
        # 2️⃣ Devolver la cantidad
        repuesto.cantidad += instalacion.cantidad

    # 3️⃣ Eliminar instalación
    db.session.delete(instalacion)
    db.session.commit()

    flash("Instalación eliminada y cantidad devuelta al inventario", "success")
    return redirect(url_for('inventory.ver_instalados'))


@inventory_bp.route('/categorias/crear', methods=['GET', 'POST'])
@login_required
def crear_categorias():
    form = CategoryForm()
    if form.validate_on_submit():
        nombre = form.nombre.data.strip().lower()

        # 🔍 Verifica si ya existe esa categoría para el usuario actual
        categoria_existente = Category.query.filter_by(nombre=nombre, usuario_id=current_user.id).first()

        if categoria_existente:
            flash('Ya tienes una categoría con ese nombre.', 'warning')
        else:
            nueva_categoria = Category(nombre=nombre, usuario_id=current_user.id)
            db.session.add(nueva_categoria)
            db.session.commit()
            flash('Categoría creada exitosamente!', 'success')
            return redirect(url_for('inventory.lista'))

    return render_template('inventory/formulario_categoria.html', form=form)


@inventory_bp.route('/categorias/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_categoria(id):
    categoria = Category.query.get_or_404(id)
    # Verificar que la categoría pertenece al usuario actual
    if categoria.usuario_id != current_user.id:
        flash('No tienes permiso para editar esta categoría.', 'danger')
        return redirect(url_for('inventory.lista'))
    
    form = CategoryForm(obj=categoria)
    if form.validate_on_submit():
        categoria.nombre = form.nombre.data
        db.session.commit()
        flash('Categoría actualizada exitosamente!', 'success')
        return redirect(url_for('inventory.lista'))
    return render_template('inventory/formulario_categoria.html', form=form, categoria=categoria)

@inventory_bp.route('/categorias/eliminar/<int:id>')
@login_required
def eliminar_categoria(id):
    categoria = Category.query.get_or_404(id)
    # Verificar que la categoría pertenece al usuario actual
    if categoria.usuario_id != current_user.id:
        flash('No tienes permiso para eliminar esta categoría.', 'danger')
        return redirect(url_for('inventory.lista'))
    db.session.delete(categoria)
    db.session.commit()
    flash('Categoría eliminada exitosamente!', 'success')
    return redirect(url_for('inventory.lista'))

@inventory_bp.route('/instalados/expcel')
@login_required
def descargar_excel():
    instalaciones = Instalacion.query.filter_by(usuario_id=current_user.id).all()
    
    # Crear un libro de Excel
    wb = Workbook()
    ws = wb.active
    ws.title = "Instalaciones"

    # Agregar encabezados
    ws.append(['ID', 'Repuesto', 'Usuario', 'Fecha', 'Cantidad', 'Precio'])

    # Agregar datos de las instalaciones
    for inst in instalaciones:
        ws.append([
            inst.id,
            inst.repuesto.modelo,
            inst.usuario.username,
            inst.fecha.strftime('%Y-%m-%d %H:%M'),
            inst.cantidad,
            inst.precio_c,
            inst.precio_v
        ])

    #guardar el archivo en memoria
    output = io.BytesIO()
    wb.save(output)
    output.seek(0)

    # Devolver el archivo como respuesta
    return send_file(output, as_attachment=True, download_name='instalaciones.xlsx')

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

@inventory_bp.route('/instalados/pdf')
@login_required
def descargar_pdf():
    instalaciones = Instalacion.query.order_by(Instalacion.fecha.desc()).all()
    
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    c.setFont("Helvetica-Bold", 14)
    c.drawString(200, height - 40, "Historial de Instalaciones")

    c.setFont("Helvetica", 10)
    y = height - 70

    c.drawString(40, y, "Repuesto")
    c.drawString(150, y, "Usuario")
    c.drawString(250, y, "Fecha")
    c.drawString(350, y, "Cantidad")
    c.drawString(420, y, "Precio")
    y -= 20

    for i in instalaciones:
        if y < 50:
            c.showPage()
            y = height - 50

        c.drawString(40, y, i.repuesto.marca + ' ' + i.repuesto.modelo)
        c.drawString(150, y, i.usuario.username)
        c.drawString(250, y, i.fecha.strftime('%Y-%m-%d %H:%M'))
        c.drawString(350, y, str(i.cantidad))
        c.drawString(420, y, f"${i.precio_c} / ${i.precio_v}")
        y -= 18

    c.save()
    buffer.seek(0)
    return send_file(buffer, download_name="instalaciones.pdf", as_attachment=True)
