from .forms import RegisterServicioForm
from . import servicio_tecnico_bp
from flask import render_template
from flask_login import login_required

servicio_tecnico_bp.route('/servicio_tecnico/registro', methods=['GET', 'POST'])
@login_required
def registro_servicio():
    form = RegisterServicioForm()
    if form.validate_on_submit():
        servicio = {
            'codigo': form.codigo.data,
            'nombre': form.nombre.data,
            'cedula': form.cedula.data,
            'numero_cel': form.numero_cel.data,
            'marca_cel': form.marca_cel.data,
            'modelo_cel': form.modelo_cel.data,
            'daño': form.daño.data,
            'descripcion': form.descripcion.data,
            'precio': form.precio.data
        }
    return render_template('index.html', form=form)
