# -*- coding: utf-8 -*-
from flask import Flask, render_template,url_for,request,session,redirect,jsonify
from flask import flash
import time
import os

#LIBRERIAS PARA GENERAR REPORTE
import cStringIO
from flask import make_response, Flask, send_file
from reportlab.pdfgen.canvas import Canvas
#OTRAS LIBRERIAS
from reportlab.lib.pagesizes import letter,A4,landscape
from reportlab.lib.enums import TA_LEFT,TA_CENTER
from reportlab.platypus import Paragraph, Frame, KeepInFrame
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib.units import inch
#-----------------------------

from model import Modelo

app=Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/')


#*****************************PAGINA LOGIN INICIO ****************************************************
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        if Modelo().modelo_login(request.form['username'],request.form['pass']):
            return redirect(url_for('index'))
        else:
            flash('Credenciales Invalidas')
            return redirect(url_for('login'))
    return render_template('login.html')
#*****************************PAGINA LOGIN FIN ****************************************************






#*****************************PAGINA PRINCIPAL INICIO ****************************************************
@app.route('/index', methods=['GET'])
def index():
     if 'username' in session:
        return render_template('index.html',usuario=session['username'],roles=session['rol'],tipo=session['tipo'])
     else:
        return redirect(url_for('login'))
# *****************************PAGINA PRINCIPAL INICIO ****************************************************







#*******************************************ADMINISTRAR EMPLEADO INICIO ************************************************************
@app.route('/administrar_empleado', methods=['POST','GET']) #REGISTRAR EMPLEADOS
def administrar_empleado():
    if request.method == 'POST':

        if request.form['rol']=='Seleccionar' or request.form['estado']=='Seleccionar':
            flash("Ingrese los datos de manera correcta")
            return redirect(url_for('administrar_empleado'))



        if Modelo().Modelo_empleado(request.form['username'].encode('utf-8').strip(), request.form['pass'], request.form['rol'],
                                    request.form['estado'], request.form['nombre'], request.form['apellido'],
                                    request.form['ci'], request.form['especialidad'], request.form['email'],
                                    request.form['cargo'], request.form['ff']):
            flash("Datos insertados correctamente")
            return redirect(url_for('administrar_empleado'))
        else:
            flash("Operacion fallida el usuario ya existe")
            return redirect(url_for('administrar_empleado'))
    if 'username' in session:
        return render_template('administrar_empleado.html',empleados=Modelo().Modelo_mostrar_empleado(),lista_roles=Modelo().lista_roles(),usuario=session['username'],roles=session['rol'],tipo=session['tipo'])
    else:
        return redirect(url_for('login'))

@app.route('/actualizar_empleado', methods=['POST','GET']) #ACTUALIZAR EMPLEADO
def actualizar_empleado():
    if request.method == 'POST':

        if request.form['rol']=='Seleccionar' or request.form['estado']=='Seleccionar':
            flash("Ingrese los datos de manera correcta")
            return redirect(url_for('administrar_empleado'))

        if Modelo().Modelo_actualizar_empleado(request.form['id'],request.form['username'], request.form['pass'], request.form['rol'],
                                    request.form['estado'], request.form['nombre'], request.form['apellido'],
                                    request.form['ci'], request.form['especialidad'], request.form['email'],
                                    request.form['cargo'], request.form['ff']):
            flash("Datos actualizados con exito")
            return redirect(url_for('administrar_empleado'))
        else:
            flash("error al actualizar datos")
            return redirect(url_for('administrar_empleado'))
    if 'username' in session:
        return redirect(url_for('administrar_empleado'))
    else:
        return redirect(url_for('login'))

@app.route('/eliminar/<string:id_data>', methods = ['GET']) #ELIMINAR EMPLEADO
def eliminar(id_data):
    if Modelo().Modelo_eliminar(id_data):
        flash("Registro ha sido eliminado con exito")
        return redirect(url_for('administrar_empleado'))
    else:
        flash("No se puede eliminar al administrador")
        return redirect(url_for('administrar_empleado'))


@app.route('/reporte_empleado/', methods = ['GET'])#REPORTE EMPLEADO
def reporte_empleado():
    Rempleado=Modelo().Modelo_reporte_empleado()
    os.remove(Rempleado)
    return redirect(url_for('administrar_empleado'))


#*******************************************ADMINISTRAR EMPLEADO FIN ************************************************************









#******************************************* ADMINISTRAR ESTUDIANTE INICIO***************************************************
@app.route('/administrar_estudiante', methods=['POST','GET']) #REGISTRAR ESTUDIANTE
def administrar_estudiante():
    if request.method == 'POST':

        if request.form['semestre']=='Seleccionar' or request.form['rol']=='Seleccionar' or request.form['estado']=='Seleccionar':
            flash("Ingrese los datos de manera correcta")
            return redirect(url_for('administrar_estudiante'))


        if Modelo().Modelo_estudiante(request.form['codigo'].title(), request.form['ci'], request.form['rol'],
                                    request.form['semestre'], request.form['nombre'].title(), request.form['apellido'],
                                    request.form['ci'], request.form['codigo'].title(), request.form['correo'],request.form['estado']):
            flash("Datos insertados correctamente")
            return redirect(url_for('administrar_estudiante'))
        else:
            flash("Operacion fallida el usuario ya existe")
            return redirect(url_for('administrar_estudiante'))
    if 'username' in session:
        return render_template('administrar_estudiante.html', usuario=session['username'],roles=session['rol'],estudiante=Modelo().Modelo_mostrar_estudiante(),lista_roles=Modelo().lista_roles(),tipo=session['tipo'])
    else:
        return redirect(url_for('login'))

@app.route('/actualizar_estudiante', methods=['POST','GET']) # ACTUALIZAR ESTUDIANTE
def actualizar_estudiante():
    if request.method == 'POST':

        if request.form['semestre']=='Seleccionar' or request.form['rol']=='Seleccionar' or request.form['estado']=='Seleccionar':
            flash("Ingrese los datos de manera correcta")
            return redirect(url_for('administrar_estudiante'))

        if Modelo().Modelo_actualizar_estudiante(request.form['id'], request.form['rol'],
                                    request.form['semestre'], request.form['nombre'].title(), request.form['apellido'].title(),
                                    request.form['ci'], request.form['codigo'].title(), request.form['correo'],request.form['estado']):
            flash("Datos actualizados con exito")
            return redirect(url_for('administrar_estudiante'))
        else:
            flash("No se actualizo estudiante")
            return redirect(url_for('administrar_estudiante'))
    if 'username' in session:
        return redirect(url_for('administrar_estudiante'))
    else:
        return redirect(url_for('login'))

@app.route('/eliminar_estudiante/<string:id_data>', methods = ['GET'])  #ELIMINAR ESTUDIANTE
def eliminar_estudiante(id_data):
    Modelo().Modelo_eliminar_estudiante(id_data)
    flash("Registro ha sido eliminado con exito")
    return redirect(url_for('administrar_estudiante'))

@app.route('/reporte_estudiante/', methods = ['GET']) #REPORTE ESTUDIANTE
def reporte_estudiante():
    estudent= Modelo().Modelo_reporte_estudiante()
    os.remove(estudent)
    return redirect(url_for('administrar_estudiante'))
#******************************************* ADMINISTRAR ESTUDIANTE FIN***************************************************









#******************************************* ADMINISTRAR ROLES INICIO***************************************************
@app.route('/administrar_rol', methods=['POST','GET']) #REGISTRAR ROLES
def administrar_rol():
    if request.method == 'POST':


        if Modelo().Modelo_rol(request.form['rol_usuario'],[request.form.getlist('opcion1')!=[],request.form.getlist('opcion2')!=[],request.form.getlist('opcion3')!=[],request.form.getlist('opcion4')!=[],request.form.getlist('opcion5')!=[],request.form.getlist('opcion6')!=[]]):
            flash("Datos insertados correctamente")
            return redirect(url_for('administrar_rol'))
        else:
            flash("Operacion fallida el rol ya existe")
            return redirect(url_for('administrar_rol'))
    if 'username' in session:
        return render_template('administrar_roles.html',usuario=session['username'],roles=session['rol'],rol=Modelo().Modelo_mostrar_roles(),tipo=session['tipo'])
    else:
        return redirect(url_for('login'))

@app.route('/actualizar_rol', methods=['POST','GET'])  #ACTUALIZAR ROLES
def actualizar_rol():
    if request.method == 'POST':
        if Modelo().Modelo_actualizar_roles(request.form['id'],request.form['rol_usuario'],[request.form.getlist('opcion1')!=[],request.form.getlist('opcion2')!=[],request.form.getlist('opcion3')!=[],request.form.getlist('opcion4')!=[],request.form.getlist('opcion5')!=[],request.form.getlist('opcion6')!=[]]):
            flash("Datos actualizados con exito")
            return redirect(url_for('administrar_rol'))
        else:
            flash("No se actualizo el rol")
            return redirect(url_for('administrar_rol'))
    if 'username' in session:
        return redirect(url_for('administrar_rol'))
    else:
        return redirect(url_for('login'))

@app.route('/eliminar_rol/<string:id_data>', methods = ['GET']) #ELIMINAR ROLES
def eliminar_rol(id_data):
    Modelo().Modelo_eliminar_rol(id_data)
    flash("Registro ha sido eliminado con exito")
    return redirect(url_for('administrar_rol'))

#******************************************* ADMINISTRAR ROLES INICIO***************************************************













#******************************************* ADMINISTRAR CLIENTES INICIO ***************************************************

@app.route('/administrar_clientes', methods=['POST','GET'])
def administrar_clientes():
    if request.method == 'POST':
        if Modelo().Modelo_clientes(request.form['nombres'].title(), request.form['apellidos'].title(),
                                              request.form['ci'],request.form['email'], request.form['telefono']):
            flash("Datos Insertados Correctamente")
            return redirect(url_for('administrar_clientes'))
        else:
            flash("Operacion fallida el usuario ya existe")
            return redirect(url_for('administrar_clientes'))
    if 'username' in session:
        return render_template('administrar_clientes.html', usuario=session['username'],clientes=Modelo().Modelo_mostrar_clientes(),roles=session['rol'],tipo=session['tipo'])
    else:
        return redirect(url_for('login'))

#
@app.route('/actualizar_clientes', methods=['POST','GET'])
def actualizar_clientes():
    if request.method == 'POST':
        if Modelo().Modelo_actualizar_cliente(request.form['id'],request.form['nombres'].title(), request.form['apellidos'].title(), request.form['ci'],
                                    request.form['email'], request.form['telefono']):
            flash("Datos actualizados con exito")
            return redirect(url_for('administrar_clientes'))
        else:
            flash("No se actualizo cliente")
            return redirect(url_for('administrar_clientes'))
    if 'username' in session:
        return redirect(url_for('administrar_clientes'))
    else:
        return redirect(url_for('login'))
#
@app.route('/eliminar_cliente/<string:id_data>', methods = ['GET'])
def eliminar_cliente(id_data):
    Modelo().Modelo_eliminar_cliente(id_data)
    flash("Registro ha sido eliminado con exito")
    return redirect(url_for('administrar_clientes'))

@app.route('/reporte_cliente/', methods = ['GET']) #REPORTE ESTUDIANTE
def reporte_cliente():
    cliente= Modelo().Modelo_reporte_cliente()
    os.remove(cliente)
    return redirect(url_for('administrar_clientes'))



@app.route('/solicitud_trabajo_externo', methods=['POST','GET'])
def solicitud_trabajo_externo():
    if request.method == 'POST':
        if Modelo().Modelo_solicitud_trabajo_externo(solicitante=request.form['solicitante'].title(),laboratista=request.form['laboratista'].title(),proyecto=request.form['proyecto'].title(),ubicacion=request.form['ubicacion'].title(),descripcion_muestra=request.form['descripcionmuestra'].title(),tipo_muestra=request.form['tipomuestra'].title(),jefe_de_carrera=request.form['jefecarrera'].title(),codigo=request.form['codigo'].title(),fecha_ensayo=request.form['fechaensayo'].title(),fecha_muestreo=request.form['fechamuestreo'].title(),fecha_entrega=request.form['fechaentrega'].title(),ensayos_solicitados=request.form['estado'].title()):
            flash("Datos Insertados Correctamente")
            return redirect(url_for('solicitud_trabajo_externo'))
        else:
            flash("Operacion fallida el la solicitu ya existe")
            return redirect(url_for('solicitud_trabajo_externo'))
    if 'username' in session:
        return render_template('administrar_solicitud_trabajo_externo.html', usuario=session['username'],clientes=Modelo().Modelo_mostrar_clientes(),roles=session['rol'],solicitud_tb_ex=Modelo().Modelo_mostrar_solicitud_trabajo_externo(),tipo=session['tipo'])
    else:
        return redirect(url_for('login'))

#
@app.route('/actualizar_solicitud_trabajo_externo', methods=['POST','GET'])
def actualizar_solicitud_trabajo_externo():
    if request.method == 'POST':
        if Modelo().Modelo_actualizar_actualizar_solicitud_trabajo_externo(solicitante=request.form['solicitante'].title(),laboratista=request.form['laboratista'].title(),proyecto=request.form['proyecto'].title(),ubicacion=request.form['ubicacion'].title(),descripcion_muestra=request.form['descripcionmuestra'].title(),tipo_muestra=request.form['tipomuestra'].title(),jefe_de_carrera=request.form['jefecarrera'].title(),codigo=request.form['codigo'].title(),fecha_ensayo=request.form['fechaensayo'].title(),fecha_muestreo=request.form['fechamuestreo'].title(),fecha_entrega=request.form['fechaentrega'].title(),ensayos_solicitados=request.form['estado'].title(),_id=request.form['id']):
            flash("Datos actualizados con exito")
            return redirect(url_for('solicitud_trabajo_externo'))
        else:
            flash("No se actualizo los datos")
            return redirect(url_for('solicitud_trabajo_externo'))
    if 'username' in session:
        return redirect(url_for('solicitud_trabajo_externo'))
    else:
        return redirect(url_for('login'))

@app.route('/eliminar_solicitud_trabajo_externo/<string:id_data>', methods = ['GET'])
def eliminar_solicitud_trabajo_externo(id_data):
    Modelo().Modelo_eliminar_solicitud_trabajo_externo(id_data)
    flash("Registro ha sido eliminado con exito")
    return redirect(url_for('solicitud_trabajo_externo'))


@app.route('/reporte_solicitud_trabajo_externo/', methods = ['GET']) #REPORTE ESTUDIANTE
def reporte_solicitud_trabajo_externo():
    solicitud_trabajo_externo= Modelo().Modelo_reporte_solicitud_trabajo_externo()
    os.remove(solicitud_trabajo_externo)
    return redirect(url_for('solicitud_trabajo_externo'))
#******************************************* ADMINISTRAR CLIENTES  Y SOLICITUDES EXTERNAS FIN ***************************************************









#******************************************* ADMINISTRAR EQUIPOS DE LABORATORIO INICIO *********************************
@app.route('/administrar_insumo_equipos', methods=['POST','GET'])  #REGISTRAR EQUIPOS
def administrar_insumo_equipos():
    if request.method == 'POST':
        if Modelo().Modelo_registrar_equipos(request.form['nombreactivo'].title(), request.form['codanterior'],
                                    request.form['codactivo'], request.form['estadoactivo'].title(), request.form['fechacompra'],
                                    request.form['descactivo'].title(),[request.form.getlist('opcion1') != [],request.form.getlist('opcion2') != [],request.form.getlist('opcion3') != [],request.form.getlist('opcion4') != [],request.form.getlist('opcion5') != [],request.form.getlist('opcion6') != [],request.form.getlist('opcion7') != [],request.form.getlist('opcion8') != [],request.form.getlist('opcion9') != [],request.form.getlist('opcion10') != [],request.form.getlist('opcion11') != [],request.form.getlist('opcion12') != [],request.form.getlist('opcion13') != [],request.form.getlist('opcion14') != [],request.form.getlist('opcion15') != [],request.form.getlist('opcion16') != [],request.form.getlist('opcion17') != [],request.form.getlist('opcion18') != [],request.form.getlist('opcion19') != [],request.form.getlist('opcion20') != []]):
            flash("Datos insertados correctamente")
            return redirect(url_for('administrar_insumo_equipos'))
        else:
            flash("Operacion fallida el codigo ya existe")
            return redirect(url_for('administrar_insumo_equipos'))

    if 'username' in session:
        return render_template('administrar_insumos_equipos.html',usuario=session['username'],roles=session['rol'],equipos=Modelo().Modelo_mostrar_equipos(),tipo=session['tipo'])
    else:
        return redirect(url_for('login'))


@app.route('/actualizar_equipos', methods=['POST','GET'])  #ACTUALIZAR EQUIPOS
def actualizar_equipos():
    if request.method == 'POST':
        if Modelo().Modelo_actualizar_equipos(request.form['id'], request.form['nombreactivo'], request.form['codanterior'],
                                    request.form['codactivo'], request.form['estadoactivo'], request.form['fechacompra'],
                                    request.form['descactivo'],[request.form.getlist('opcion1') != [],request.form.getlist('opcion2') != [],request.form.getlist('opcion3') != [],request.form.getlist('opcion4') != [],request.form.getlist('opcion5') != [],request.form.getlist('opcion6') != [],request.form.getlist('opcion7') != [],request.form.getlist('opcion8') != [],request.form.getlist('opcion9') != [],request.form.getlist('opcion10') != [],request.form.getlist('opcion11') != [],request.form.getlist('opcion12') != [],request.form.getlist('opcion13') != [],request.form.getlist('opcion14') != [],request.form.getlist('opcion15') != [],request.form.getlist('opcion16') != [],request.form.getlist('opcion17') != [],request.form.getlist('opcion18') != [],request.form.getlist('opcion19') != [],request.form.getlist('opcion20') != []]):
            flash("Datos actualizados con exito")
            return redirect(url_for('administrar_insumo_equipos'))
        else:
            flash("No se actualizaron los datos  ")
            return redirect(url_for('administrar_insumo_equipos'))
    if 'username' in session:
        return render_template('administrar_insumos_equipos.html', usuario=session['username'],roles=session['rol'],tipo=session['tipo'])
    else:
        return redirect(url_for('login'))

@app.route('/eliminar_equipo/<string:id_data>', methods=['GET'])   #ELIMINAR EQUIPOS
def eliminar_equipo(id_data):
    
    if Modelo().Modelo_eliminar_global(id_data):
        flash("Registro ha sido eliminado con exito")
        return redirect(url_for('administrar_insumo_equipos'))
    else:
        flash("No se puede eliminar al administrador")
        return redirect(url_for('administrar_insumo_equipos'))


@app.route('/reporte_equipos/', methods = ['GET'])     # REPORTE EQUIPOS DE LABORATORIO
def reporte_equipos():
    equipo= Modelo().Modelo_reporte_equipos()
    os.remove(equipo)
    return redirect(url_for('administrar_insumo_equipos'))
#******************************************* ADMINISTRAR EQUIPOS DE LABORATORIO FIN ************************************











#******************************************* ADMINISTRAR MATERIALES DE LABORATORIO INICIO *****************************
@app.route('/administrar_insumo_materiales', methods=['POST','GET'])  #REGISTRAR EQUIPOS
def administrar_insumo_materiales():
    if request.method == 'POST':
        if Modelo().Modelo_registrar_materiales(request.form['nombreactivo'].title(),time.strftime("%Y-%m-%d"),
                                    request.form['descactivo'].title(),[request.form.getlist('opcion1') != [],request.form.getlist('opcion2') != [],request.form.getlist('opcion3') != [],request.form.getlist('opcion4') != [],request.form.getlist('opcion5') != [],request.form.getlist('opcion6') != [],request.form.getlist('opcion7') != [],request.form.getlist('opcion8') != [],request.form.getlist('opcion9') != [],request.form.getlist('opcion10') != [],request.form.getlist('opcion11') != [],request.form.getlist('opcion12') != [],request.form.getlist('opcion13') != [],request.form.getlist('opcion14') != [],request.form.getlist('opcion15') != [],request.form.getlist('opcion16') != [],request.form.getlist('opcion17') != [],request.form.getlist('opcion18') != [],request.form.getlist('opcion19') != [],request.form.getlist('opcion20') != []]):
            flash("Datos insertados correctamente")
            return redirect(url_for('administrar_insumo_materiales'))
        else:
            flash("Operacion fallida el codigo ya existe")
            return redirect(url_for('administrar_insumo_materiales'))
    if 'username' in session:
        return render_template('administrar_insumos_materiales.html',usuario=session['username'],roles=session['rol'],equipos=Modelo().Modelo_mostrar_materiales(),tipo=session['tipo'])
    else:
        return redirect(url_for('login'))


@app.route('/actualizar_materiales', methods=['POST','GET'])  #ACTUALIZAR EQUIPOS
def actualizar_materiales():
    if request.method == 'POST':
        if Modelo().Modelo_actualizar_materiales(request.form['id'], request.form['nombreactivo'],
                                    request.form['descactivo'],[request.form.getlist('opcion1') != [],request.form.getlist('opcion2') != [],request.form.getlist('opcion3') != [],request.form.getlist('opcion4') != [],request.form.getlist('opcion5') != [],request.form.getlist('opcion6') != [],request.form.getlist('opcion7') != [],request.form.getlist('opcion8') != [],request.form.getlist('opcion9') != [],request.form.getlist('opcion10') != [],request.form.getlist('opcion11') != [],request.form.getlist('opcion12') != [],request.form.getlist('opcion13') != [],request.form.getlist('opcion14') != [],request.form.getlist('opcion15') != [],request.form.getlist('opcion16') != [],request.form.getlist('opcion17') != [],request.form.getlist('opcion18') != [],request.form.getlist('opcion19') != [],request.form.getlist('opcion20') != []]):
            flash("Datos actualizados con exito")
            return redirect(url_for('administrar_insumo_materiales'))
        else:
            flash("No se actualizaron los datos  ")
            return redirect(url_for('administrar_insumo_materiales'))
    if 'username' in session:
        return render_template('administrar_insumos_materiales.html', usuario=session['username'],roles=session['rol'],tipo=session['tipo'])
    else:
        return redirect(url_for('login'))

@app.route('/eliminar_material/<string:id_data>', methods=['GET'])   #ELIMINAR EQUIPOS
def eliminar_material(id_data):

    if Modelo().Modelo_eliminar_materiales(id_data):
        flash("Registro ha sido eliminado con exito")
        return redirect(url_for('administrar_insumo_materiales'))
    else:
        flash("No se elimino registro")
        return redirect(url_for('administrar_insumo_materiales'))


@app.route('/reporte_materiales/', methods = ['GET'])     # REPORTE EQUIPOS DE LABORATORIO
def reporte_materiales():
    materiales= Modelo().Modelo_reporte_materiales()
    os.remove(materiales)
    return redirect(url_for('administrar_insumo_materiales'))

#******************************************* ADMINISTRAR EQUIPOS DE LABORATORIO FIN *********************************







#******************************************* ADMINISTRAR MATERIALES DE LABORATORIO INICIO *********************************
@app.route('/administrar_insumo_Reactivos', methods=['POST','GET'])  #REGISTRAR EQUIPOS
def administrar_insumo_Reactivos():
    if request.method == 'POST':

        if Modelo().Modelo_registrar_reactivos(request.form['nombreactivo'].title(),request.form['fechavencimiento'],time.strftime("%Y-%m-%d"),
                                    [request.form.getlist('opcion1') != [],request.form.getlist('opcion2') != [],request.form.getlist('opcion3') != [],request.form.getlist('opcion4') != [],request.form.getlist('opcion5') != [],request.form.getlist('opcion6') != [],request.form.getlist('opcion7') != [],request.form.getlist('opcion8') != [],request.form.getlist('opcion9') != [],request.form.getlist('opcion10') != [],request.form.getlist('opcion11') != [],request.form.getlist('opcion12') != [],request.form.getlist('opcion13') != [],request.form.getlist('opcion14') != [],request.form.getlist('opcion15') != [],request.form.getlist('opcion16') != [],request.form.getlist('opcion17') != [],request.form.getlist('opcion18') != [],request.form.getlist('opcion19') != [],request.form.getlist('opcion20') != []]):
            flash("Datos insertados correctamente")
            return redirect(url_for('administrar_insumo_Reactivos'))
        else:
            flash("Operacion fallida el codigo ya existe")
            return redirect(url_for('administrar_insumo_Reactivos'))

    if 'username' in session:
        return render_template('administrar_insumos_reactivos.html',usuario=session['username'],roles=session['rol'],equipos=Modelo().Modelo_mostrar_reactivos(),tipo=session['tipo'])
    else:
        return redirect(url_for('login'))


@app.route('/actualizar_reactivos', methods=['POST','GET'])  #ACTUALIZAR EQUIPOS
def actualizar_reactivos():
    if request.method == 'POST':
        if Modelo().Modelo_actualizar_reactivos(request.form['id'], request.form['nombreactivo'],
                                    request.form['fechavencimiento'],[request.form.getlist('opcion1') != [],request.form.getlist('opcion2') != [],request.form.getlist('opcion3') != [],request.form.getlist('opcion4') != [],request.form.getlist('opcion5') != [],request.form.getlist('opcion6') != [],request.form.getlist('opcion7') != [],request.form.getlist('opcion8') != [],request.form.getlist('opcion9') != [],request.form.getlist('opcion10') != [],request.form.getlist('opcion11') != [],request.form.getlist('opcion12') != [],request.form.getlist('opcion13') != [],request.form.getlist('opcion14') != [],request.form.getlist('opcion15') != [],request.form.getlist('opcion16') != [],request.form.getlist('opcion17') != [],request.form.getlist('opcion18') != [],request.form.getlist('opcion19') != [],request.form.getlist('opcion20') != []]):
            flash("Datos actualizados con exito")
            return redirect(url_for('administrar_insumo_Reactivos'))
        else:
            flash("No se actualizaron los datos  ")
            return redirect(url_for('administrar_insumo_Reactivos'))
    if 'username' in session:
        return redirect(url_for('administrar_insumo_Reactivos'))
    else:
        return redirect(url_for('login'))

@app.route('/eliminar_reactivo/<string:id_data>', methods=['GET'])   #ELIMINAR EQUIPOS
def eliminar_reactivo(id_data):

    if Modelo().Modelo_eliminar_reactivo(id_data):
        flash("Registro ha sido eliminado con exito")
        return redirect(url_for('administrar_insumo_Reactivos'))
    else:
        flash("No se elimino registro")
        return redirect(url_for('administrar_insumo_Reactivos'))


@app.route('/reporte_reactivos/', methods = ['GET'])     # REPORTE EQUIPOS DE LABORATORIO
def reporte_reactivos():
    reactivos= Modelo().Modelo_reporte_reactivos()
    os.remove(reactivos)
    return redirect(url_for('administrar_insumo_Reactivos'))
#******************************************* ADMINISTRAR EQUIPOS DE LABORATORIO FIN ************************************








#*************************** FORMULARIO DE SOLICITUD DE LABORATORIO Y EQUIPOS INTERFAZ LOGIN INICIO ********************

@app.route('/administrar_solicitud_lab', methods=['POST','GET']) #MOSTRAR SOLICITUDES DE LABORATORIO
def administrar_solicitud_lab():
    return render_template('formulario_de_requerimientos.html',usuario=session['username'],roles=session['rol'],datoslb=session['datos_sol_lab'],tipo=session['tipo'])


@app.route('/registro_formulario_de_requerimientos', methods=['POST','GET'])  #REGISTRAR DATOS SOLICITUD DE LABORATORIO
def registro_formulario_de_requerimientos():
    if request.method == 'POST':
        if Modelo().Modelo_solicitud_laboratorio(nombre=request.form['nombre'],ci=request.form['ci'],carrera=request.form['carrera'],asignatura=request.form['asignatura'],semestre=request.form['semestre'],practica_laboratorio=request.form['opcion'],fecha_solicitud=time.strftime("%Y-%m-%d"),solicitante=request.form['solicitante'],materiales=[request.form['materiales1'],request.form['materiales2'],request.form['materiales3'],request.form['materiales4'],request.form['materiales5'],request.form['materiales6'],request.form['materiales7'],request.form['materiales8']],equipos=[request.form['equipos1'],request.form['equipos2'],request.form['equipos3'],request.form['equipos4']],reactivos=[request.form['reactivo1'],request.form['reactivo2'],request.form['reactivo3'],request.form['reactivo4'],request.form['reactivo5'],request.form['reactivo6'],request.form['reactivo7'],request.form['reactivo8']],correo_electronico=request.form['correo'],fecha_uso_laboratorio=request.form['fecha_uso'],hora_uso_laboratorio=request.form['hora'],estado="Ninguno",observaciones='Ninguno'):
            flash("Se envio el formulario de solicitud correctamente")
            return redirect(url_for('administrar_solicitud_lab'))
        else:
            flash("Error no se envio el formulario de solicitud")
            return redirect(url_for('administrar_solicitud_lab'))
    else:
        return redirect(url_for('administrar_solicitud_lab'))

@app.route('/_get_data/', methods=['POST'])
def _get_data():
    return jsonify({'data': render_template('formulario_de_requerimientos2.html',materiales=Modelo().Modelo_select_materiales(request.form['opcion']),equipos=Modelo().Modelo_select_dinamico(request.form['opcion']),reactivos=Modelo().Modelo_select_reactivos(request.form['opcion']))})

@app.route('/formulario_de_prestamo_de_equipos', methods=['POST','GET']) #MOSTRAR SOLICITUDES DE LABORATORIO
def formulario_de_prestamo_de_equipos():
    return render_template('formulario_de_prestamo_de_materiales.html',equipos=Modelo().Modelo_mostrar_lista(),usuario=session['username'],roles=session['rol'],datoslb=session['datos_sol_lab'],tipo=session['tipo'])


@app.route('/registrar_formulario_de_prestamo_de_equipos', methods=['POST','GET'])    #REGISTRAR DATOS SOLICITUD DE EQUIPOS
def registrar_formulario_de_prestamo_de_equipos():
    if request.method == 'POST':
        if Modelo().Modelo_solicitud_de_equipos(nombre=request.form['nombre'],ci=request.form['ci'],carrera=request.form['carrera'],sala_de_trabajo=request.form['sala_de_trabajo'],asignatura=request.form['asignatura'],proposito_uso_de_equipo=request.form['practica_lb'],fecha_solicitud=time.strftime("%Y-%m-%d"),
                                                    equipos=[request.form['equipo1'],request.form['equipo2'],request.form['equipo3'],request.form['equipo4'],request.form['equipo5'],request.form['equipo6'],request.form['equipo7'],request.form['equipo8'],request.form['equipo9'],request.form['equipo10']],
                                                    correo_electronico=request.form['correo'],fecha_uso_de_equipo=request.form['fecha_uso'],hora_uso_de_equipo=request.form['hora'],estado="Ninguno",observaciones="Ninguno"):
            flash("Se envio el formulario de solicitud correctamente")
            return redirect(url_for('formulario_de_prestamo_de_equipos'))
        else:
            flash("Error no se envio el formulario de solicitud")
            return redirect(url_for('formulario_de_prestamo_de_equipos'))
    return redirect(url_for('formulario_de_prestamo_de_equipos'))
#*************************** FORMULARIO DE SOLICITUD DE LABORATORIO Y EQUIPOS INTERFAZ LOGIN FIN **************************










#************************************** ADMINISTRAR SOLICITUDES DE USO DE LABORATORIO INICIO ******************************
@app.route('/administrar_solicitudes', methods=['POST','GET']) #MOSTRAR SOLICITUDES DE LABORATORIO
def administrar_solicitudes():
    return render_template('administrar_solicitudes_laboratorio.html',usuario=session['username'],roles=session['rol'],rol=Modelo().Modelo_mostrar_solicitudes_laboratorio(),tipo=session['tipo'])


@app.route('/aceptar/<string:id_data>', methods = ['GET','POST'])  #BOTON ACEPTAR SOLICITUD
def aceptar(id_data):
    if Modelo().Modelo_aceptacion_solicitud(id_data):
        flash("Se envio el mensaje de aceptacion al correo")
        return redirect(url_for('administrar_solicitudes'))
    else:
        flash("Operacion fallida al enviar el correo")
        return redirect(url_for('administrar_solicitudes'))

@app.route('/rechazar/<string:id_data>', methods=['GET', 'POST'])   #BOTON RECHAZAR SOLICITUD
def rechazar(id_data):
    if Modelo().Modelo_rechazo_de_solicitud(id_data):
        flash("Se envio el mensaje de rechazo de la solicitud al correo")
        return redirect(url_for('administrar_solicitudes'))
    else:
        flash("Operacion fallida al enviar el correo")
        return redirect(url_for('administrar_solicitudes'))


@app.route('/observaciones', methods=['POST','GET'])       #BOTON OBSERVAR SOLICITUD EN CASO NO DEVOLVER TODOS LOS MATERILES
def observaciones():
    if request.method == 'POST':
        if Modelo().Modelo_observaciones(request.form['id'],request.form['observaciones']):
            return redirect(url_for('administrar_solicitudes'))
        else:
            return redirect(url_for('administrar_solicitudes'))
    if 'username' in session:
        return redirect(url_for('administrar_solicitudes'))
    else:
        return redirect(url_for('login'))


@app.route('/eliminar_solicitud_lab/<string:id_data>', methods=['GET'])    #ELIMINAR UNA VEZ SE AYA CUMPLIDO EL USO Y LA DEVOLUCION DE LOS MATERILES
def eliminar_solicitud_lab(id_data):
    if Modelo().Modelo_eliminar_solicitudes_lab(id_data):
        flash("La solicitud ha sido eliminado con exito")
        return redirect(url_for('administrar_solicitudes'))
    else:
        flash("No se pudo eliminar la solicitud")
        return redirect(url_for('administrar_solicitudes'))


@app.route('/reporte_solicitudes_laboratorio/', methods = ['GET'])      #REPORTE DEL FORMULARIO DE SOLICITUD
def reporte_solicitudes_laboratorio():
    solicitud_lab=Modelo().Modelo_reporte_solicitud_laboratorio()
    os.remove(solicitud_lab)
    return redirect(url_for('administrar_solicitudes'))

@app.route('/reporte_formulario_solicitud_lab/<string:id_data>', methods = ['GET'])      #REPORTE DEL FORMULARIO DE SOLICITUD
def reporte_formulario_solicitud_lab(id_data):
    a= Modelo().Modelo_reporte_formulario_solicitud_laboratorio(id_data)
    return reporte_solicitud_de_uso_de_laboratorio(a)
#************************************** ADMINISTRAR SOLICITUDES DE USO DE LABORATORIO INICIO ********************************







#************************************** ADMINISTRAR SOLICITUDES DE USO DE EQUIPOS INICIO ***************************
@app.route('/administrar_solicitudes_equipos', methods=['POST','GET']) #MOSTRAR SOLICITUDES DE LABORATORIO
def administrar_solicitudes_equipos():
    return render_template('administrar_solicitudes_equipos.html',usuario=session['username'],roles=session['rol'],rol=Modelo().Modelo_mostrar_solicitudes_equipos(),tipo=session['tipo'])


@app.route('/aceptar_solicitud_equipo/<string:id_data>', methods = ['GET','POST'])  #BOTON ACEPTAR SOLICITUD
def aceptar_solicitud_equipo(id_data):
    if Modelo().Modelo_aceptacion_solicitud_equipo(id_data):
        flash("Se envio el mensaje de aceptacion al correo")
        return redirect(url_for('administrar_solicitudes_equipos'))
    else:
        flash("Operacion fallida al enviar el correo")
        return redirect(url_for('administrar_solicitudes_equipos'))

@app.route('/rechazar_solicitud_equipos/<string:id_data>', methods=['GET', 'POST'])   #BOTON RECHAZAR SOLICITUD
def rechazar_solicitud_equipos(id_data):
    if Modelo().Modelo_rechazo_de_solicitud_equipos(id_data):
        flash("Se envio el mensaje de rechazo de la solicitud al correo")
        return redirect(url_for('administrar_solicitudes_equipos'))
    else:
        flash("Operacion fallida al enviar el correo")
        return redirect(url_for('administrar_solicitudes_equipos'))


@app.route('/observaciones_solicitud_equipos', methods=['POST','GET'])       #BOTON OBSERVAR SOLICITUD EN CASO NO DEVOLVER TODOS LOS MATERILES
def observaciones_solicitud_equipos():
    if request.method == 'POST':
        if Modelo().Modelo_observaciones_solicitud_equipos(request.form['id'],request.form['observaciones']):
            return redirect(url_for('administrar_solicitudes_equipos'))
        else:
            return redirect(url_for('administrar_solicitudes_equipos'))
    if 'username' in session:
        return redirect(url_for('administrar_solicitudes_equipos'))
    else:
        return redirect(url_for('login'))

@app.route('/eliminar_solicitud_equipos/<string:id_data>', methods=['GET'])    #ELIMINAR UNA VEZ SE AYA CUMPLIDO EL USO Y LA DEVOLUCION DE LOS MATERILES
def eliminar_solicitud_equipos(id_data):
    if Modelo().Modelo_eliminar_solicitudes_equipos(id_data):
        flash("La solicitud ha sido eliminado con exito")
        return redirect(url_for('administrar_solicitudes_equipos'))
    else:
        flash("No se pudo eliminar la solicitud")
        return redirect(url_for('administrar_solicitudes_equipos'))


@app.route('/reporte_solicitudes_equipos/', methods = ['GET'])      #REPORTE DEL FORMULARIO DE SOLICITUD  #falta terminar **************************************************************************
def reporte_solicitudes_equipos():
    solicitud_equipo=Modelo().Modelo_reporte_solicitud_equipos()
    os.remove(solicitud_equipo)
    return redirect(url_for('administrar_solicitudes_equipos'))


@app.route('/reporte_formulario_solicitud_equipos/<string:id_data>', methods = ['GET'])      #REPORTE DEL FORMULARIO DE SOLICITUD
def reporte_formulario_solicitud_equipos(id_data):
    a= Modelo().Modelo_reporte_formulario_solicitud_equipos(id_data)
    return solicitud_de_prestamo_de_equipos_de_laboratorio(a)
#************************************** ADMINISTRAR SOLICITUDES DE USO DE EQUIPOS INICIO *****************************************









#********************************************* ENSAYOS CONTENIDO DE HUMEDAD  ***********************************************************************

@app.route('/contenido_humedad', methods=['GET','POST'])#solo mostrar
def contenido_humedad():
    titulo='CONTENIDO DE HUMEDAD (ASTM D2216)'
    return render_template('ensayo_contenido_de_humedad1.html', titulo=titulo, usuario=session['username'],roles=session['rol'],tipo=session['tipo'],dato=Modelo().Modelo_mostrar_solicitud_trabajo_externo())

@app.route('/calcular_contenido_humedad', methods=['GET','POST'])
def calcular_contenido_humedad():
    titulo = 'CONTENIDO DE HUMEDAD (ASTM D2216)'
    if request.method == 'POST':
        resultado=Modelo().Modelo_calculo_contenido_humedad(datos_generales=[request.form['proyecto'].title(),request.form['ubicacion'].title(),request.form['descmuestra'].title(),request.form['tipomuestra'].title(),request.form['laboratista'].title(),request.form['solicitante'].title(),request.form['jefecarrera'].title(),time.strftime("%Y-%m-%d")],datos_muestra_laboratorio=[request.form['contenedor1'].title(),request.form['contenedor2'].title(),request.form['contenedor3'].title(),request.form['masa1'],request.form['masahumedo1'],request.form['masaseco1'],request.form['masa2'],request.form['masahumedo2'],request.form['masaseco2'],request.form['masa3'],request.form['masahumedo3'],request.form['masaseco3']],usuario=session['username'],ci=session['cedula'],ensayo=titulo)
        if resultado[0]==1:
            flash(resultado[1])
            return redirect(url_for('contenido_humedad'))
        else:
            return render_template('ensayo_contenido_de_humedad1_resultado.html', titulo=titulo, usuario=session['username'],roles=session['rol'], resultado=1, datos=Modelo().Modelo_mostrar_datos_contenido_humedad(),tipo=session['tipo'],dato=Modelo().Modelo_mostrar_solicitud_trabajo_externo())
    else:
        return redirect(url_for('contenido_humedad'))



@app.route('/modificar_calculo_contenido_humedad', methods=['GET','POST'])
def modificar_calculo_contenido_humedad():
    titulo = 'CONTENIDO DE HUMEDAD (ASTM D2216)'
    if request.method == 'POST':
        resultado=Modelo().Modelo_modificar_calculo_contenido_humedad(datos_generales=[request.form['proyecto'].title(),request.form['ubicacion'].title(),request.form['descmuestra'].title(),request.form['tipomuestra'].title(),request.form['laboratista'].title(),request.form['solicitante'].title(),request.form['jefecarrera'].title(),time.strftime("%Y-%m-%d")],datos_muestra_laboratorio=[request.form['contenedor1'].title(),request.form['contenedor2'].title(),request.form['contenedor3'].title(),request.form['masa1'],request.form['masahumedo1'],request.form['masaseco1'],request.form['masa2'],request.form['masahumedo2'],request.form['masaseco2'],request.form['masa3'],request.form['masahumedo3'],request.form['masaseco3']],usuario=session['username'],ci=session['cedula'],_id=request.form['id'])

        if resultado[0]==1:
            flash(resultado[1])
            return redirect(url_for('contenido_humedad'))
        else:
            return render_template('ensayo_contenido_de_humedad1_resultado.html', titulo=titulo, usuario=session['username'],roles=session['rol'], resultado=1, datos=Modelo().Modelo_mostrar_datos_contenido_humedad(),tipo=session['tipo'],dato=Modelo().Modelo_mostrar_solicitud_trabajo_externo())
    else:
        return redirect(url_for('contenido_humedad'))

@app.route('/reporte_contenido_humedad/<string:id_data>', methods = ['GET'])      #REPORTE DEL FORMULARIO DE SOLICITUD
def reporte_contenido_humedad(id_data):
    datos = Modelo().Modelo_reporte_contenido_humedad(id_data)
    a=reporte_humedad(datos)
    return a
# ********************************************* ENSAYOS CONTENIDO DE HUMEDAD FIN ***********************************************************************









# /************************************************************ GRANULOMETRIA ENSAYO ************************************************************************

@app.route('/granulometria', methods=['GET','POST'])
def granulometria():
    titulo='GRANULOMETRIA (ASTM D422)'
    return render_template('ensayo_de_granulometria.html', titulo=titulo, usuario=session['username'],roles=session['rol'],LL=Modelo().Modelo_lista_limite_liquido(),tipo=session['tipo'],dato=Modelo().Modelo_mostrar_solicitud_trabajo_externo())


@app.route('/calcular_granulometria', methods=['GET','POST'])
def calcular_granulometria():
    titulo = 'GRANULOMETRIA (ASTM D422)'
    ip=0
    if request.method == 'POST':
        if str(request.form['limite_liquido'])=='seleccionar':
            granulometria=Modelo().Modelo_granulometria(datos_generales=[request.form['proyecto'].title(),request.form['ubicacion'].title(),request.form['descmuestra'].title(),request.form['tipomuestra'].title(),request.form['laboratista'].title(),request.form['solicitante'].title(),request.form['jefecarrera'].title(),time.strftime("%Y-%m-%d")],datos_muestra_laboratorio=[request.form['masarecipiente1'],request.form['masarecipiente2'],request.form['masamuestraseca'],request.form['masasecagrueso'],request.form['masaretenida1'],request.form['masaretenida2'],request.form['masaretenida3'],request.form['masaretenida4'],request.form['masaretenida5'],request.form['masaretenida6'],request.form['masaretenida7'],request.form['masaretenida8'],request.form['masaretenida9'],request.form['masaretenida10'],request.form['masaretenida11'],request.form['masaretenida12'],request.form['masaretenida13'],request.form['masaretenida14'],'seleccionar','ninguno'],usuario=session['username'],ci=session['cedula'],ensayo=titulo)
        else:
            for i in Modelo().Modelo_lista_limite_liquido():

                if i[0] == float(request.form['limite_liquido']):
                    ip= i[1]
            granulometria=Modelo().Modelo_granulometria(datos_generales=[request.form['proyecto'].title(),request.form['ubicacion'].title(),request.form['descmuestra'].title(),request.form['tipomuestra'].title(),request.form['laboratista'].title(),request.form['solicitante'].title(),request.form['jefecarrera'].title(),time.strftime("%Y-%m-%d")],datos_muestra_laboratorio=[request.form['masarecipiente1'],request.form['masarecipiente2'],request.form['masamuestraseca'],request.form['masasecagrueso'],request.form['masaretenida1'],request.form['masaretenida2'],request.form['masaretenida3'],request.form['masaretenida4'],request.form['masaretenida5'],request.form['masaretenida6'],request.form['masaretenida7'],request.form['masaretenida8'],request.form['masaretenida9'],request.form['masaretenida10'],request.form['masaretenida11'],request.form['masaretenida12'],request.form['masaretenida13'],request.form['masaretenida14'],float(request.form['limite_liquido']),ip],usuario=session['username'],ci=session['cedula'],ensayo=titulo)
        if granulometria[0]==1:
            flash("error de calculo con desface de : " + str(round(granulometria[1], 2)))
            return redirect(url_for('granulometria'))
        else:
            return render_template('ensayo_de_granulometria_resultado.html', titulo=titulo, usuario=session['username'],roles=session['rol'], resultado=1, datos=Modelo().Modelo_mostrar_datos_granulometria(),LL=Modelo().Modelo_lista_limite_liquido(),tipo=session['tipo'],dato=Modelo().Modelo_mostrar_solicitud_trabajo_externo())
    else:
        return redirect(url_for('granulometria'))


        

@app.route('/modificar_calculo_granulometria', methods=['GET','POST'])
def modificar_calculo_granulometria():
    titulo = 'GRANULOMETRIA (ASTM D422)'
    if request.method == 'POST':

        if str(request.form['limite_liquido'])=='seleccionar':
            granulometria=Modelo().Modelo_modificar_calculo_granulometria(datos_generales=[request.form['proyecto'].title(),request.form['ubicacion'].title(),request.form['descmuestra'].title(),request.form['tipomuestra'].title(),request.form['laboratista'].title(),request.form['solicitante'].title(),request.form['jefecarrera'].title(),time.strftime("%Y-%m-%d")],datos_muestra_laboratorio=[request.form['masarecipiente1'],request.form['masarecipiente2'],request.form['masamuestraseca'],request.form['masasecagrueso'],request.form['masaretenida1'],request.form['masaretenida2'],request.form['masaretenida3'],request.form['masaretenida4'],request.form['masaretenida5'],request.form['masaretenida6'],request.form['masaretenida7'],request.form['masaretenida8'],request.form['masaretenida9'],request.form['masaretenida10'],request.form['masaretenida11'],request.form['masaretenida12'],request.form['masaretenida13'],request.form['masaretenida14'],'seleccionar','ninguno'],usuario=session['username'],ci=session['cedula'],_id=request.form['id'])
        else:
            for i in Modelo().Modelo_lista_limite_liquido():

                if i[0] == float(request.form['limite_liquido']):
                    ip= i[1]
            granulometria=Modelo().Modelo_modificar_calculo_granulometria(datos_generales=[request.form['proyecto'].title(),request.form['ubicacion'].title(),request.form['descmuestra'].title(),request.form['tipomuestra'].title(),request.form['laboratista'].title(),request.form['solicitante'].title(),request.form['jefecarrera'].title(),time.strftime("%Y-%m-%d")],datos_muestra_laboratorio=[request.form['masarecipiente1'],request.form['masarecipiente2'],request.form['masamuestraseca'],request.form['masasecagrueso'],request.form['masaretenida1'],request.form['masaretenida2'],request.form['masaretenida3'],request.form['masaretenida4'],request.form['masaretenida5'],request.form['masaretenida6'],request.form['masaretenida7'],request.form['masaretenida8'],request.form['masaretenida9'],request.form['masaretenida10'],request.form['masaretenida11'],request.form['masaretenida12'],request.form['masaretenida13'],request.form['masaretenida14'],float(request.form['limite_liquido']),ip],usuario=session['username'],ci=session['cedula'],_id=request.form['id'])
        if granulometria[0]==1:
            flash("error de calculo con desface de : " +str(round(granulometria[1],2)))
            return render_template('ensayo_de_granulometria_resultado.html', titulo=titulo, usuario=session['username'],roles=session['rol'], resultado=1, datos=Modelo().Modelo_mostrar_datos_granulometria(),LL=Modelo().Modelo_lista_limite_liquido(),tipo=session['tipo'],dato=Modelo().Modelo_mostrar_solicitud_trabajo_externo())
        else:
            return render_template('ensayo_de_granulometria_resultado.html', titulo=titulo, usuario=session['username'],roles=session['rol'], resultado=1, datos=Modelo().Modelo_mostrar_datos_granulometria(),LL=Modelo().Modelo_lista_limite_liquido(),tipo=session['tipo'],dato=Modelo().Modelo_mostrar_solicitud_trabajo_externo())
    else:
        return redirect(url_for('granulometria'))

@app.route('/reporte_granulometria_astm/<string:id_data>', methods = ['GET'])      #REPORTE DEL FORMULARIO DE SOLICITUD
def reporte_granulometria_astm(id_data):
    titulo = 'GRANULOMETRIA (ASTM D422)'
    a= Modelo().Modelo_reporte_granulometria_astm(id_data)
    return reporte_granulometria_astm2(a)
# ************************************************************* GRANULOMETRIA FIN ***************************************************************************















# /************************************************************ LIMITES DE CONSISTENCIA ENSAYO ************************************************************************

@app.route('/limites_de_consistencia', methods=['GET','POST'])
def limites_de_consistencia():
    titulo='LIMITES DE CONSISTENCIA (ASTM D4318)'
    return render_template('ensayo_limites_de_consistencia_astm.html', titulo=titulo, usuario=session['username'],roles=session['rol'],tipo=session['tipo'],dato=Modelo().Modelo_mostrar_solicitud_trabajo_externo())

@app.route('/calculo_limites_de_consistencia', methods=['GET','POST'])
def calculo_limites_de_consistencia():
    titulo = 'LIMITES DE CONSISTENCIA (ASTM D4318)'
    if request.method == 'POST':
        a=Modelo().Modelo_limites_de_consistencia_astm(datos_generales=[request.form['proyecto'].title(),request.form['ubicacion'].title(),request.form['descmuestra'].title(),request.form['tipomuestra'].title(),request.form['laboratista'].title(),request.form['solicitante'].title(),request.form['jefecarrera'].title(),time.strftime("%Y-%m-%d")],datos_muestra_laboratorio=[[request.form['contenedor1'],request.form['contenedor2'],request.form['contenedor3'],request.form['contenedorlp1'],request.form['contenedorlp2'],request.form['contenedorlp3']]
            ,[[request.form['masarecipiente1'],request.form['numerogolpes1'],request.form['masahumedo1'],request.form['masaseco1']],[request.form['masarecipiente2'],request.form['numerogolpes2'],request.form['masahumedo2'],request.form['masaseco2']],[request.form['masarecipiente3'],request.form['numerogolpes3'],request.form['masahumedo3'],request.form['masaseco3']]]
            ,[[request.form['masarecipientelp1'],request.form['masahumedolp1'],request.form['masasecolp1']],[request.form['masarecipientelp2'],request.form['masahumedolp2'],request.form['masasecolp2']],[request.form['masarecipientelp3'],request.form['masahumedolp3'],request.form['masasecolp3']]]],usuario=session['username'],ci=session['cedula'],ensayo=titulo)
        if a[0]==1:
            flash(str(a[1]))
            return redirect(url_for('limites_de_consistencia'))
        else:
            return render_template('ensayo_limites_de_consistencia_astm_resultado.html', titulo=titulo, usuario=session['username'],
                               roles=session['rol'], resultado=1, datos=Modelo().Modelo_mostrar_datos_limites_astm(),tipo=session['tipo'],dato=Modelo().Modelo_mostrar_solicitud_trabajo_externo())

    return  redirect(url_for('limites_de_consistencia'))



@app.route('/modificar_calculo_limites_astm', methods=['GET','POST'])
def modificar_calculo_limites_astm():
    titulo = 'LIMITES DE CONSISTENCIA (ASTM D4318)'
    if request.method == 'POST':
        a=Modelo().Modelo_modificar_calculo_limites_astm(datos_generales=[request.form['proyecto'].title(),request.form['ubicacion'].title(),request.form['descmuestra'].title(),request.form['tipomuestra'].title(),request.form['laboratista'].title(),request.form['solicitante'].title(),request.form['jefecarrera'].title(),time.strftime("%Y-%m-%d")],datos_muestra_laboratorio=[[request.form['contenedor1'],request.form['contenedor2'],request.form['contenedor3'],request.form['contenedorlp1'],request.form['contenedorlp2'],request.form['contenedorlp3']]
            ,[[request.form['masarecipiente1'],request.form['numerogolpes1'],request.form['masahumedo1'],request.form['masaseco1']],[request.form['masarecipiente2'],request.form['numerogolpes2'],request.form['masahumedo2'],request.form['masaseco2']],[request.form['masarecipiente3'],request.form['numerogolpes3'],request.form['masahumedo3'],request.form['masaseco3']]]
            ,[[request.form['masarecipientelp1'],request.form['masahumedolp1'],request.form['masasecolp1']],[request.form['masarecipientelp2'],request.form['masahumedolp2'],request.form['masasecolp2']],[request.form['masarecipientelp3'],request.form['masahumedolp3'],request.form['masasecolp3']]]],usuario=session['username'],ci=session['cedula'],_id=request.form['id'])
        if a[0]==1:
            flash(str(a[1]))
            return render_template('ensayo_limites_de_consistencia_astm_resultado.html', titulo=titulo, usuario=session['username'],roles=session['rol'], resultado=1, datos=Modelo().Modelo_mostrar_datos_limites_astm(),tipo=session['tipo'],dato=Modelo().Modelo_mostrar_solicitud_trabajo_externo())
        else:
            return render_template('ensayo_limites_de_consistencia_astm_resultado.html', titulo=titulo, usuario=session['username'],roles=session['rol'], resultado=1, datos=Modelo().Modelo_mostrar_datos_limites_astm(),tipo=session['tipo'],dato=Modelo().Modelo_mostrar_solicitud_trabajo_externo())
    else:
        return redirect(url_for('limites_de_consistencia'))


@app.route('/reporte_limite_de_consistencia_astm_d4318/<string:id_data>', methods = ['GET'])      #REPORTE DEL FORMULARIO DE SOLICITUD
def reporte_limite_de_consistencia_astm_d4318(id_data):
    datos= Modelo().Modelo_reporte_limite_de_consistencia_astm_d4318(id_data)
    a = reporte_limite_consistencia_astm(datos)
    return a



# ************************************************************* LIMITES DE CONSISTENCIA FIN ***************************************************************************
















# /************************************************************ PROCTOR MODIFICADO ASTM ************************************************************************

@app.route('/proctor_modificadoASTM', methods=['GET','POST'])
def proctor_modificadoASTM():
    titulo='COMPACTACION PROCTOR MODIFICADO (ASTM D1557)'
    return render_template('ensayo_compactacion_proctor_modificado_astm.html', titulo=titulo, usuario=session['username'],roles=session['rol'],tipo=session['tipo'],dato=Modelo().Modelo_mostrar_solicitud_trabajo_externo())



@app.route('/calculo_proctor_modificadoASTM', methods=['GET','POST'])
def calculo_proctor_modificadoASTM():
    titulo='COMPACTACION PROCTOR MODIFICADO (ASTM D1557)'
    if request.method == 'POST':

        if str(request.form['volumen'])=='':
            proctor=Modelo().Modelo_calculo_proctor_modificado_astm(datos_generales=[request.form['proyecto'].title(),request.form['ubicacion'].title(),request.form['descmuestra'].title(),request.form['tipomuestra'].title(),request.form['laboratista'].title(),request.form['solicitante'].title(),request.form['jefecarrera'].title(),time.strftime("%Y-%m-%d")],datos_muestra_laboratorio=[[request.form['metodo'],request.form['gravedad'],request.form['diametro'],request.form['altura'],0],[request.form['PMS1'],request.form['PMS2'],request.form['PMS3'],request.form['PMS4'],request.form['PMS5']],[request.form['PM1'],request.form['PM2'],request.form['PM3'],request.form['PM4'],request.form['PM5']],[request.form['numerocontenedor1'],request.form['numerocontenedor2'],request.form['numerocontenedor3'],request.form['numerocontenedor4'],request.form['numerocontenedor5'],request.form['numerocontenedor6'],request.form['numerocontenedor7'],request.form['numerocontenedor8'],request.form['numerocontenedor9'],request.form['numerocontenedor10']],[[request.form['MR1'],request.form['MRSH1'],request.form['MRSS1']],[request.form['MR2'],request.form['MRSH2'],request.form['MRSS2']],[request.form['MR3'],request.form['MRSH3'],request.form['MRSS3']],[request.form['MR4'],request.form['MRSH4'],request.form['MRSS4']],[request.form['MR5'],request.form['MRSH5'],request.form['MRSS5']],[request.form['MR6'],request.form['MRSH6'],request.form['MRSS6']],[request.form['MR7'],request.form['MRSH7'],request.form['MRSS7']],[request.form['MR8'],request.form['MRSH8'],request.form['MRSS8']],[request.form['MR9'],request.form['MRSH9'],request.form['MRSS9']],[request.form['MR10'],request.form['MRSH10'],request.form['MRSS10']]]],usuario=session['username'],ci=session['cedula'],ensayo=titulo)
        else:
            proctor=Modelo().Modelo_calculo_proctor_modificado_astm(datos_generales=[request.form['proyecto'].title(),request.form['ubicacion'].title(),request.form['descmuestra'].title(),request.form['tipomuestra'].title(),request.form['laboratista'].title(),request.form['solicitante'].title(),request.form['jefecarrera'].title(),time.strftime("%Y-%m-%d")],datos_muestra_laboratorio=[[request.form['metodo'],request.form['gravedad'],request.form['diametro'],request.form['altura'],request.form['volumen']],[request.form['PMS1'],request.form['PMS2'],request.form['PMS3'],request.form['PMS4'],request.form['PMS5']],[request.form['PM1'],request.form['PM2'],request.form['PM3'],request.form['PM4'],request.form['PM5']],[request.form['numerocontenedor1'],request.form['numerocontenedor2'],request.form['numerocontenedor3'],request.form['numerocontenedor4'],request.form['numerocontenedor5'],request.form['numerocontenedor6'],request.form['numerocontenedor7'],request.form['numerocontenedor8'],request.form['numerocontenedor9'],request.form['numerocontenedor10']],[[request.form['MR1'],request.form['MRSH1'],request.form['MRSS1']],[request.form['MR2'],request.form['MRSH2'],request.form['MRSS2']],[request.form['MR3'],request.form['MRSH3'],request.form['MRSS3']],[request.form['MR4'],request.form['MRSH4'],request.form['MRSS4']],[request.form['MR5'],request.form['MRSH5'],request.form['MRSS5']],[request.form['MR6'],request.form['MRSH6'],request.form['MRSS6']],[request.form['MR7'],request.form['MRSH7'],request.form['MRSS7']],[request.form['MR8'],request.form['MRSH8'],request.form['MRSS8']],[request.form['MR9'],request.form['MRSH9'],request.form['MRSS9']],[request.form['MR10'],request.form['MRSH10'],request.form['MRSS10']]]],usuario=session['username'],ci=session['cedula'],ensayo=titulo)
        if proctor[0]==1:
            flash(str(proctor[1]))
            return redirect(url_for('proctor_modificadoASTM'))
        else:
            return render_template('ensayo_compactacion_proctor_modificado_astm_resultado.html', titulo=titulo, usuario=session['username'],roles=session['rol'],resultado=1, datos=Modelo().Modelo_mostrar_datos_proctor_astm(),tipo=session['tipo'],dato=Modelo().Modelo_mostrar_solicitud_trabajo_externo())
    else:
        return redirect(url_for('proctor_modificadoASTM'))





#
@app.route('/modificar_calculo_proctor_modificadoASTM', methods=['GET', 'POST'])
def modificar_calculo_proctor_modificadoASTM():
    titulo = 'COMPACTACION PROCTOR MODIFICADO (ASTM D1557)'
    if request.method == 'POST':
        if str(request.form['volumen']) == '':
            print "1 :", request.form['id']
            proctor=Modelo().Modelo_modificar_proctor_modificado_astm(datos_generales=[request.form['proyecto'].title(),request.form['ubicacion'].title(),request.form['descmuestra'].title(),request.form['tipomuestra'].title(),request.form['laboratista'].title(),request.form['solicitante'].title(),request.form['jefecarrera'].title(),time.strftime("%Y-%m-%d")],datos_muestra_laboratorio=[[request.form['metodo'],request.form['gravedad'],request.form['diametro'],request.form['altura'],0],[request.form['PMS1'],request.form['PMS2'],request.form['PMS3'],request.form['PMS4'],request.form['PMS5']],[request.form['PM1'],request.form['PM2'],request.form['PM3'],request.form['PM4'],request.form['PM5']],[request.form['numerocontenedor1'],request.form['numerocontenedor2'],request.form['numerocontenedor3'],request.form['numerocontenedor4'],request.form['numerocontenedor5'],request.form['numerocontenedor6'],request.form['numerocontenedor7'],request.form['numerocontenedor8'],request.form['numerocontenedor9'],request.form['numerocontenedor10']],[[request.form['MR1'],request.form['MRSH1'],request.form['MRSS1']],[request.form['MR2'],request.form['MRSH2'],request.form['MRSS2']],[request.form['MR3'],request.form['MRSH3'],request.form['MRSS3']],[request.form['MR4'],request.form['MRSH4'],request.form['MRSS4']],[request.form['MR5'],request.form['MRSH5'],request.form['MRSS5']],[request.form['MR6'],request.form['MRSH6'],request.form['MRSS6']],[request.form['MR7'],request.form['MRSH7'],request.form['MRSS7']],[request.form['MR8'],request.form['MRSH8'],request.form['MRSS8']],[request.form['MR9'],request.form['MRSH9'],request.form['MRSS9']],[request.form['MR10'],request.form['MRSH10'],request.form['MRSS10']]]],usuario=session['username'],ci=session['cedula'],_id=request.form['id'])
        else:
            proctor=Modelo().Modelo_modificar_proctor_modificado_astm(datos_generales=[request.form['proyecto'].title(),request.form['ubicacion'].title(),request.form['descmuestra'].title(),request.form['tipomuestra'].title(),request.form['laboratista'].title(),request.form['solicitante'].title(),request.form['jefecarrera'].title(),time.strftime("%Y-%m-%d")],datos_muestra_laboratorio=[[request.form['metodo'],request.form['gravedad'],request.form['diametro'],request.form['altura'],request.form['volumen']],[request.form['PMS1'],request.form['PMS2'],request.form['PMS3'],request.form['PMS4'],request.form['PMS5']],[request.form['PM1'],request.form['PM2'],request.form['PM3'],request.form['PM4'],request.form['PM5']],[request.form['numerocontenedor1'],request.form['numerocontenedor2'],request.form['numerocontenedor3'],request.form['numerocontenedor4'],request.form['numerocontenedor5'],request.form['numerocontenedor6'],request.form['numerocontenedor7'],request.form['numerocontenedor8'],request.form['numerocontenedor9'],request.form['numerocontenedor10']],[[request.form['MR1'],request.form['MRSH1'],request.form['MRSS1']],[request.form['MR2'],request.form['MRSH2'],request.form['MRSS2']],[request.form['MR3'],request.form['MRSH3'],request.form['MRSS3']],[request.form['MR4'],request.form['MRSH4'],request.form['MRSS4']],[request.form['MR5'],request.form['MRSH5'],request.form['MRSS5']],[request.form['MR6'],request.form['MRSH6'],request.form['MRSS6']],[request.form['MR7'],request.form['MRSH7'],request.form['MRSS7']],[request.form['MR8'],request.form['MRSH8'],request.form['MRSS8']],[request.form['MR9'],request.form['MRSH9'],request.form['MRSS9']],[request.form['MR10'],request.form['MRSH10'],request.form['MRSS10']]]],usuario=session['username'],ci=session['cedula'],_id=request.form['id'])
        if proctor[0] == 1:
            flash(str(proctor[1]))
            return redirect(url_for('proctor_modificadoASTM'))
            #return render_template('ensayo_compactacion_proctor_modificado_astm_resultado.html', titulo=titulo, usuario=session['username'],roles=session['rol'],resultado=1, datos=Modelo().Modelo_mostrar_datos_proctor_astm(),tipo=session['tipo'],dato=Modelo().Modelo_mostrar_solicitud_trabajo_externo())
        else:
            return render_template('ensayo_compactacion_proctor_modificado_astm_resultado.html', titulo=titulo, usuario=session['username'],roles=session['rol'],resultado=1, datos=Modelo().Modelo_mostrar_datos_proctor_astm(),tipo=session['tipo'],dato=Modelo().Modelo_mostrar_solicitud_trabajo_externo())
    else:
        return redirect(url_for('proctor_modificadoASTM'))


@app.route('/reporte_proctor_modificado_astm/<string:id_data>', methods = ['GET'])      #REPORTE DEL FORMULARIO DE SOLICITUD
def reporte_proctor_modificado_astm(id_data):
    a= Modelo().Modelo_reporte_proctor_modificado_astm(id_data)
    return reporte_proctor_modificado_astm2(a)

# ************************************************************* PROCTOR FIN ***************************************************************************






# /************************************************************ LIMITES DE CONSISTENCIA AASHTO ************************************************************************

@app.route('/limites_de_consistencia_AASHTO', methods=['GET','POST'])
def limites_de_consistencia_AASHTO():
    titulo='LIMITES DE CONSISTENCIA (AASHTO T-89)'
    return render_template('ensayo_limites_de_consistencia_aashto.html', titulo=titulo, usuario=session['username'],roles=session['rol'],tipo=session['tipo'],dato=Modelo().Modelo_mostrar_solicitud_trabajo_externo())

@app.route('/calculo_limites_de_consistencia_aashto', methods=['GET','POST'])
def calculo_limites_de_consistencia_aashto():
    titulo = 'LIMITES DE CONSISTENCIA (AASHTO T-89)'
    if request.method == 'POST':
        a=Modelo().Modelo_limites_de_consistencia_aashto(datos_generales=[request.form['proyecto'].title(),request.form['ubicacion'].title(),request.form['descmuestra'].title(),request.form['tipomuestra'].title(),request.form['laboratista'].title(),request.form['solicitante'].title(),request.form['jefecarrera'].title(),time.strftime("%Y-%m-%d")],datos_muestra_laboratorio=[[request.form['contenedor1'],request.form['contenedor2'],request.form['contenedor3'],request.form['contenedor4'],request.form['contenedorlp1'],request.form['contenedorlp2'],request.form['contenedorlp3']]
            ,[[request.form['masarecipiente1'],request.form['numerogolpes1'],request.form['masahumedo1'],request.form['masaseco1']],[request.form['masarecipiente2'],request.form['numerogolpes2'],request.form['masahumedo2'],request.form['masaseco2']],[request.form['masarecipiente3'],request.form['numerogolpes3'],request.form['masahumedo3'],request.form['masaseco3']],[request.form['masarecipiente4'],request.form['numerogolpes4'],request.form['masahumedo4'],request.form['masaseco4']]]
            ,[[request.form['masarecipientelp1'],request.form['masahumedolp1'],request.form['masasecolp1']],[request.form['masarecipientelp2'],request.form['masahumedolp2'],request.form['masasecolp2']],[request.form['masarecipientelp3'],request.form['masahumedolp3'],request.form['masasecolp3']]]],usuario=session['username'],ci=session['cedula'],ensayo=titulo)
        if a[0]==1:
            flash(str(a[1]))
            return redirect(url_for('limites_de_consistencia_AASHTO'))
        else:
            print "que pasa"
            print "listaaaa",Modelo().Modelo_mostrar_datos_limites_aashto()
            return render_template('ensayo_limites_de_consistencia_aashto_resultado.html', titulo=titulo, usuario=session['username'],
                               roles=session['rol'], resultado=1, datos=Modelo().Modelo_mostrar_datos_limites_aashto(),tipo=session['tipo'],dato=Modelo().Modelo_mostrar_solicitud_trabajo_externo())

    return  redirect(url_for('limites_de_consistencia_AASHTO'))



@app.route('/modificar_calculo_limites_aashto', methods=['GET','POST'])
def modificar_calculo_limites_aashto():
    titulo = 'LIMITES DE CONSISTENCIA (AASHTO T-89)'
    if request.method == 'POST':
        a=Modelo().Modelo_modificar_calculo_limites_aashto(datos_generales=[request.form['proyecto'].title(),request.form['ubicacion'].title(),request.form['descmuestra'].title(),request.form['tipomuestra'].title(),request.form['laboratista'].title(),request.form['solicitante'].title(),request.form['jefecarrera'].title(),time.strftime("%Y-%m-%d")],datos_muestra_laboratorio=[[request.form['contenedor1'],request.form['contenedor2'],request.form['contenedor3'],request.form['contenedor4'],request.form['contenedorlp1'],request.form['contenedorlp2'],request.form['contenedorlp3']]
            ,[[request.form['masarecipiente1'],request.form['numerogolpes1'],request.form['masahumedo1'],request.form['masaseco1']],[request.form['masarecipiente2'],request.form['numerogolpes2'],request.form['masahumedo2'],request.form['masaseco2']],[request.form['masarecipiente3'],request.form['numerogolpes3'],request.form['masahumedo3'],request.form['masaseco3']],[request.form['masarecipiente4'],request.form['numerogolpes4'],request.form['masahumedo4'],request.form['masaseco4']]]
            ,[[request.form['masarecipientelp1'],request.form['masahumedolp1'],request.form['masasecolp1']],[request.form['masarecipientelp2'],request.form['masahumedolp2'],request.form['masasecolp2']],[request.form['masarecipientelp3'],request.form['masahumedolp3'],request.form['masasecolp3']]]],usuario=session['username'],ci=session['cedula'],_id=request.form['id'])
        if a[0]==1:
            flash(str(a[1]))
            return render_template('ensayo_limites_de_consistencia_aashto_resultado.html', titulo=titulo, usuario=session['username'],roles=session['rol'], resultado=1, datos=Modelo().Modelo_mostrar_datos_limites_aashto(),tipo=session['tipo'],dato=Modelo().Modelo_mostrar_solicitud_trabajo_externo())
        else:
            return render_template('ensayo_limites_de_consistencia_aashto_resultado.html', titulo=titulo, usuario=session['username'],roles=session['rol'], resultado=1, datos=Modelo().Modelo_mostrar_datos_limites_aashto(),tipo=session['tipo'],dato=Modelo().Modelo_mostrar_solicitud_trabajo_externo())
    else:
        return render_template('ensayo_limites_de_consistencia_aashto_resultado.html', titulo=titulo, usuario=session['username'],roles=session['rol'], resultado=1, datos=Modelo().Modelo_mostrar_datos_limites_aashto(),tipo=session['tipo'],dato=Modelo().Modelo_mostrar_solicitud_trabajo_externo())


@app.route('/reporte_limite_de_consistencia_aashto_t89/<string:id_data>', methods = ['GET'])      #REPORTE DEL FORMULARIO DE SOLICITUD
def reporte_limite_de_consistencia_aashto_t89(id_data):
    titulo = 'LIMITES DE CONSISTENCIA (AASHTO T-89)'
    a= Modelo().Modelo_reporte_limite_de_consistencia_aashto_t89(id_data)
    return reporte_limite_conssitencia_aashto2(a)

# # ************************************************************* LIMITES DE CONSISTENCIA FIN ***************************************************************************
#









# /************************************************************ PROCTOR MODIFICADO AASHTO ************************************************************************

@app.route('/proctor_modificadoAASHTO', methods=['GET','POST'])
def proctor_modificadoAASHTO():
    titulo='COMPACTACION PROCTOR MODIFICADO (AASHTO T-180)'
    return render_template('ensayo_compactacion_proctor_modificado_aashto.html', titulo=titulo.encode('utf-8'), usuario=session['username'],roles=session['rol'],tipo=session['tipo'],dato=Modelo().Modelo_mostrar_solicitud_trabajo_externo())


@app.route('/calculo_proctor_modificadoAASHTO', methods=['GET','POST'])
def calculo_proctor_modificadoAASHTO():
    titulo='COMPACTACION PROCTOR MODIFICADO (AASHTO T-180)'
    if request.method == 'POST':

        if str(request.form['volumen'])=='':
            proctor=Modelo().Modelo_calculo_proctor_modificado_aashto(datos_generales=[request.form['proyecto'].title(),request.form['ubicacion'].title(),request.form['descmuestra'].title(),request.form['tipomuestra'].title(),request.form['laboratista'].title(),request.form['solicitante'].title(),request.form['jefecarrera'].title(),time.strftime("%Y-%m-%d")],datos_muestra_laboratorio=[[request.form['metodo'],request.form['gravedad'],request.form['diametro'],request.form['altura'],0],[request.form['PMS1'],request.form['PMS2'],request.form['PMS3'],request.form['PMS4'],request.form['PMS5']],[request.form['PM1'],request.form['PM2'],request.form['PM3'],request.form['PM4'],request.form['PM5']],[request.form['numerocontenedor1'],request.form['numerocontenedor2'],request.form['numerocontenedor3'],request.form['numerocontenedor4'],request.form['numerocontenedor5'],request.form['numerocontenedor6'],request.form['numerocontenedor7'],request.form['numerocontenedor8'],request.form['numerocontenedor9'],request.form['numerocontenedor10']],[[request.form['MR1'],request.form['MRSH1'],request.form['MRSS1']],[request.form['MR2'],request.form['MRSH2'],request.form['MRSS2']],[request.form['MR3'],request.form['MRSH3'],request.form['MRSS3']],[request.form['MR4'],request.form['MRSH4'],request.form['MRSS4']],[request.form['MR5'],request.form['MRSH5'],request.form['MRSS5']],[request.form['MR6'],request.form['MRSH6'],request.form['MRSS6']],[request.form['MR7'],request.form['MRSH7'],request.form['MRSS7']],[request.form['MR8'],request.form['MRSH8'],request.form['MRSS8']],[request.form['MR9'],request.form['MRSH9'],request.form['MRSS9']],[request.form['MR10'],request.form['MRSH10'],request.form['MRSS10']]]],usuario=session['username'],ci=session['cedula'],ensayo=titulo)
        else:
            proctor=Modelo().Modelo_calculo_proctor_modificado_aashto(datos_generales=[request.form['proyecto'].title(),request.form['ubicacion'].title(),request.form['descmuestra'].title(),request.form['tipomuestra'].title(),request.form['laboratista'].title(),request.form['solicitante'].title(),request.form['jefecarrera'].title(),time.strftime("%Y-%m-%d")],datos_muestra_laboratorio=[[request.form['metodo'],request.form['gravedad'],request.form['diametro'],request.form['altura'],request.form['volumen']],[request.form['PMS1'],request.form['PMS2'],request.form['PMS3'],request.form['PMS4'],request.form['PMS5']],[request.form['PM1'],request.form['PM2'],request.form['PM3'],request.form['PM4'],request.form['PM5']],[request.form['numerocontenedor1'],request.form['numerocontenedor2'],request.form['numerocontenedor3'],request.form['numerocontenedor4'],request.form['numerocontenedor5'],request.form['numerocontenedor6'],request.form['numerocontenedor7'],request.form['numerocontenedor8'],request.form['numerocontenedor9'],request.form['numerocontenedor10']],[[request.form['MR1'],request.form['MRSH1'],request.form['MRSS1']],[request.form['MR2'],request.form['MRSH2'],request.form['MRSS2']],[request.form['MR3'],request.form['MRSH3'],request.form['MRSS3']],[request.form['MR4'],request.form['MRSH4'],request.form['MRSS4']],[request.form['MR5'],request.form['MRSH5'],request.form['MRSS5']],[request.form['MR6'],request.form['MRSH6'],request.form['MRSS6']],[request.form['MR7'],request.form['MRSH7'],request.form['MRSS7']],[request.form['MR8'],request.form['MRSH8'],request.form['MRSS8']],[request.form['MR9'],request.form['MRSH9'],request.form['MRSS9']],[request.form['MR10'],request.form['MRSH10'],request.form['MRSS10']]]],usuario=session['username'],ci=session['cedula'],ensayo=titulo)
        if proctor[0]==1:
            flash(str(proctor[1]))
            return redirect(url_for('proctor_modificadoAASHTO'))
        else:
            return render_template('ensayo_compactacion_proctor_modificado_aashto_resultado.html', titulo=titulo, usuario=session['username'],roles=session['rol'],resultado=1, datos=Modelo().Modelo_mostrar_datos_proctor_aashto(),tipo=session['tipo'],dato=Modelo().Modelo_mostrar_solicitud_trabajo_externo())
    else:
        return redirect(url_for('proctor_modificadoAASHTO'))



@app.route('/modificar_calculo_proctor_modificadoAASHTO', methods=['GET', 'POST'])
def modificar_calculo_proctor_modificadoAASHTO():
    titulo = 'COMPACTACION PROCTOR MODIFICADO (AASHTO T-180)'
    if request.method == 'POST':
        if str(request.form['volumen']) == '':
            print "1 :", request.form['id']
            proctor=Modelo().Modelo_modificar_proctor_modificado_aashto(datos_generales=[request.form['proyecto'].title(),request.form['ubicacion'].title(),request.form['descmuestra'].title(),request.form['tipomuestra'].title(),request.form['laboratista'].title(),request.form['solicitante'].title(),request.form['jefecarrera'].title(),time.strftime("%Y-%m-%d")],datos_muestra_laboratorio=[[request.form['metodo'],request.form['gravedad'],request.form['diametro'],request.form['altura'],0],[request.form['PMS1'],request.form['PMS2'],request.form['PMS3'],request.form['PMS4'],request.form['PMS5']],[request.form['PM1'],request.form['PM2'],request.form['PM3'],request.form['PM4'],request.form['PM5']],[request.form['numerocontenedor1'],request.form['numerocontenedor2'],request.form['numerocontenedor3'],request.form['numerocontenedor4'],request.form['numerocontenedor5'],request.form['numerocontenedor6'],request.form['numerocontenedor7'],request.form['numerocontenedor8'],request.form['numerocontenedor9'],request.form['numerocontenedor10']],[[request.form['MR1'],request.form['MRSH1'],request.form['MRSS1']],[request.form['MR2'],request.form['MRSH2'],request.form['MRSS2']],[request.form['MR3'],request.form['MRSH3'],request.form['MRSS3']],[request.form['MR4'],request.form['MRSH4'],request.form['MRSS4']],[request.form['MR5'],request.form['MRSH5'],request.form['MRSS5']],[request.form['MR6'],request.form['MRSH6'],request.form['MRSS6']],[request.form['MR7'],request.form['MRSH7'],request.form['MRSS7']],[request.form['MR8'],request.form['MRSH8'],request.form['MRSS8']],[request.form['MR9'],request.form['MRSH9'],request.form['MRSS9']],[request.form['MR10'],request.form['MRSH10'],request.form['MRSS10']]]],usuario=session['username'],ci=session['cedula'],_id=request.form['id'])
        else:
            proctor=Modelo().Modelo_modificar_proctor_modificado_aashto(datos_generales=[request.form['proyecto'].title(),request.form['ubicacion'].title(),request.form['descmuestra'].title(),request.form['tipomuestra'].title(),request.form['laboratista'].title(),request.form['solicitante'].title(),request.form['jefecarrera'].title(),time.strftime("%Y-%m-%d")],datos_muestra_laboratorio=[[request.form['metodo'],request.form['gravedad'],request.form['diametro'],request.form['altura'],request.form['volumen']],[request.form['PMS1'],request.form['PMS2'],request.form['PMS3'],request.form['PMS4'],request.form['PMS5']],[request.form['PM1'],request.form['PM2'],request.form['PM3'],request.form['PM4'],request.form['PM5']],[request.form['numerocontenedor1'],request.form['numerocontenedor2'],request.form['numerocontenedor3'],request.form['numerocontenedor4'],request.form['numerocontenedor5'],request.form['numerocontenedor6'],request.form['numerocontenedor7'],request.form['numerocontenedor8'],request.form['numerocontenedor9'],request.form['numerocontenedor10']],[[request.form['MR1'],request.form['MRSH1'],request.form['MRSS1']],[request.form['MR2'],request.form['MRSH2'],request.form['MRSS2']],[request.form['MR3'],request.form['MRSH3'],request.form['MRSS3']],[request.form['MR4'],request.form['MRSH4'],request.form['MRSS4']],[request.form['MR5'],request.form['MRSH5'],request.form['MRSS5']],[request.form['MR6'],request.form['MRSH6'],request.form['MRSS6']],[request.form['MR7'],request.form['MRSH7'],request.form['MRSS7']],[request.form['MR8'],request.form['MRSH8'],request.form['MRSS8']],[request.form['MR9'],request.form['MRSH9'],request.form['MRSS9']],[request.form['MR10'],request.form['MRSH10'],request.form['MRSS10']]]],usuario=session['username'],ci=session['cedula'],_id=request.form['id'])
        if proctor[0] == 1:
            flash(str(proctor[1]))
            return redirect(url_for('proctor_modificadoAASHTO'))
            #return render_template('ensayo_compactacion_proctor_modificado_astm_resultado.html', titulo=titulo, usuario=session['username'],roles=session['rol'],resultado=1, datos=Modelo().Modelo_mostrar_datos_proctor_astm(),tipo=session['tipo'],dato=Modelo().Modelo_mostrar_solicitud_trabajo_externo())
        else:
            return render_template('ensayo_compactacion_proctor_modificado_aashto_resultado.html', titulo=titulo, usuario=session['username'],roles=session['rol'],resultado=1, datos=Modelo().Modelo_mostrar_datos_proctor_aashto(),tipo=session['tipo'],dato=Modelo().Modelo_mostrar_solicitud_trabajo_externo())
    else:
        return render_template('ensayo_compactacion_proctor_modificado_aashto_resultado.html', titulo=titulo, usuario=session['username'],roles=session['rol'],resultado=1, datos=Modelo().Modelo_mostrar_datos_proctor_aashto(),tipo=session['tipo'],dato=Modelo().Modelo_mostrar_solicitud_trabajo_externo())


@app.route('/reporte_proctor_modificado_aashto/<string:id_data>', methods = ['GET'])      #REPORTE DEL FORMULARIO DE SOLICITUD
def reporte_proctor_modificado_aashto(id_data):
    a= Modelo().Modelo_reporte_proctor_modificado_aashto(id_data)
    return reporte_proctor_modificado_aashto2(a)


# ************************************************************* PROCTOR FIN ***************************************************************************






# /************************************************************ PROCTOR ESTANDAR AASHTO ************************************************************************

@app.route('/proctor_estandar_AASHTO', methods=['GET','POST'])
def proctor_estandar_AASHTO():
    titulo='COMPACTACION PROCTOR ESTANDAR (AASHTO T-99)'
    return render_template('ensayo_compactacion_proctor_estandar_aashto.html', titulo=titulo.encode('utf-8'), usuario=session['username'],roles=session['rol'],tipo=session['tipo'],dato=Modelo().Modelo_mostrar_solicitud_trabajo_externo())


@app.route('/calculo_proctor_estandar_AASHTO', methods=['GET','POST'])
def calculo_proctor_estandar_AASHTO():
    titulo = 'COMPACTACION PROCTOR ESTANDAR (AASHTO T-99)'
    if request.method == 'POST':

        if str(request.form['volumen'])=='':
            proctor=Modelo().Modelo_calculo_proctor_estandar_aashto(datos_generales=[request.form['proyecto'].title(),request.form['ubicacion'].title(),request.form['descmuestra'].title(),request.form['tipomuestra'].title(),request.form['laboratista'].title(),request.form['solicitante'].title(),request.form['jefecarrera'].title(),time.strftime("%Y-%m-%d")],datos_muestra_laboratorio=[[request.form['metodo'],request.form['gravedad'],request.form['diametro'],request.form['altura'],0],[request.form['PMS1'],request.form['PMS2'],request.form['PMS3'],request.form['PMS4'],request.form['PMS5']],[request.form['PM1'],request.form['PM2'],request.form['PM3'],request.form['PM4'],request.form['PM5']],[request.form['numerocontenedor1'],request.form['numerocontenedor2'],request.form['numerocontenedor3'],request.form['numerocontenedor4'],request.form['numerocontenedor5'],request.form['numerocontenedor6'],request.form['numerocontenedor7'],request.form['numerocontenedor8'],request.form['numerocontenedor9'],request.form['numerocontenedor10']],[[request.form['MR1'],request.form['MRSH1'],request.form['MRSS1']],[request.form['MR2'],request.form['MRSH2'],request.form['MRSS2']],[request.form['MR3'],request.form['MRSH3'],request.form['MRSS3']],[request.form['MR4'],request.form['MRSH4'],request.form['MRSS4']],[request.form['MR5'],request.form['MRSH5'],request.form['MRSS5']],[request.form['MR6'],request.form['MRSH6'],request.form['MRSS6']],[request.form['MR7'],request.form['MRSH7'],request.form['MRSS7']],[request.form['MR8'],request.form['MRSH8'],request.form['MRSS8']],[request.form['MR9'],request.form['MRSH9'],request.form['MRSS9']],[request.form['MR10'],request.form['MRSH10'],request.form['MRSS10']]]],usuario=session['username'],ci=session['cedula'],ensayo=titulo)
        else:
            proctor=Modelo().Modelo_calculo_proctor_estandar_aashto(datos_generales=[request.form['proyecto'].title(),request.form['ubicacion'].title(),request.form['descmuestra'].title(),request.form['tipomuestra'].title(),request.form['laboratista'].title(),request.form['solicitante'].title(),request.form['jefecarrera'].title(),time.strftime("%Y-%m-%d")],datos_muestra_laboratorio=[[request.form['metodo'],request.form['gravedad'],request.form['diametro'],request.form['altura'],request.form['volumen']],[request.form['PMS1'],request.form['PMS2'],request.form['PMS3'],request.form['PMS4'],request.form['PMS5']],[request.form['PM1'],request.form['PM2'],request.form['PM3'],request.form['PM4'],request.form['PM5']],[request.form['numerocontenedor1'],request.form['numerocontenedor2'],request.form['numerocontenedor3'],request.form['numerocontenedor4'],request.form['numerocontenedor5'],request.form['numerocontenedor6'],request.form['numerocontenedor7'],request.form['numerocontenedor8'],request.form['numerocontenedor9'],request.form['numerocontenedor10']],[[request.form['MR1'],request.form['MRSH1'],request.form['MRSS1']],[request.form['MR2'],request.form['MRSH2'],request.form['MRSS2']],[request.form['MR3'],request.form['MRSH3'],request.form['MRSS3']],[request.form['MR4'],request.form['MRSH4'],request.form['MRSS4']],[request.form['MR5'],request.form['MRSH5'],request.form['MRSS5']],[request.form['MR6'],request.form['MRSH6'],request.form['MRSS6']],[request.form['MR7'],request.form['MRSH7'],request.form['MRSS7']],[request.form['MR8'],request.form['MRSH8'],request.form['MRSS8']],[request.form['MR9'],request.form['MRSH9'],request.form['MRSS9']],[request.form['MR10'],request.form['MRSH10'],request.form['MRSS10']]]],usuario=session['username'],ci=session['cedula'],ensayo=titulo)
        if proctor[0]==1:
            flash(str(proctor[1]))
            return redirect(url_for('proctor_estandar_AASHTO'))
        else:
            return render_template('ensayo_compactacion_proctor_estandar_aashto_resultado.html', titulo=titulo, usuario=session['username'],roles=session['rol'],resultado=1, datos=Modelo().Modelo_mostrar_datos_proctor_estandar_aashto(),tipo=session['tipo'],dato=Modelo().Modelo_mostrar_solicitud_trabajo_externo())
    else:
        return redirect(url_for('proctor_estandar_AASHTO'))



@app.route('/modificar_calculo_proctor_estandar_AASHTO', methods=['GET', 'POST'])
def modificar_calculo_proctor_estandar_AASHTO():
    titulo = 'COMPACTACION PROCTOR ESTANDAR (AASHTO T-99)'
    if request.method == 'POST':
        if str(request.form['volumen']) == '':
            proctor=Modelo().Modelo_modificar_proctor_estandar_aashto(datos_generales=[request.form['proyecto'].title(),request.form['ubicacion'].title(),request.form['descmuestra'].title(),request.form['tipomuestra'].title(),request.form['laboratista'].title(),request.form['solicitante'].title(),request.form['jefecarrera'].title(),time.strftime("%Y-%m-%d")],datos_muestra_laboratorio=[[request.form['metodo'],request.form['gravedad'],request.form['diametro'],request.form['altura'],0],[request.form['PMS1'],request.form['PMS2'],request.form['PMS3'],request.form['PMS4'],request.form['PMS5']],[request.form['PM1'],request.form['PM2'],request.form['PM3'],request.form['PM4'],request.form['PM5']],[request.form['numerocontenedor1'],request.form['numerocontenedor2'],request.form['numerocontenedor3'],request.form['numerocontenedor4'],request.form['numerocontenedor5'],request.form['numerocontenedor6'],request.form['numerocontenedor7'],request.form['numerocontenedor8'],request.form['numerocontenedor9'],request.form['numerocontenedor10']],[[request.form['MR1'],request.form['MRSH1'],request.form['MRSS1']],[request.form['MR2'],request.form['MRSH2'],request.form['MRSS2']],[request.form['MR3'],request.form['MRSH3'],request.form['MRSS3']],[request.form['MR4'],request.form['MRSH4'],request.form['MRSS4']],[request.form['MR5'],request.form['MRSH5'],request.form['MRSS5']],[request.form['MR6'],request.form['MRSH6'],request.form['MRSS6']],[request.form['MR7'],request.form['MRSH7'],request.form['MRSS7']],[request.form['MR8'],request.form['MRSH8'],request.form['MRSS8']],[request.form['MR9'],request.form['MRSH9'],request.form['MRSS9']],[request.form['MR10'],request.form['MRSH10'],request.form['MRSS10']]]],usuario=session['username'],ci=session['cedula'],_id=request.form['id'])
        else:
            proctor=Modelo().Modelo_modificar_proctor_estandar_aashto(datos_generales=[request.form['proyecto'].title(),request.form['ubicacion'].title(),request.form['descmuestra'].title(),request.form['tipomuestra'].title(),request.form['laboratista'].title(),request.form['solicitante'].title(),request.form['jefecarrera'].title(),time.strftime("%Y-%m-%d")],datos_muestra_laboratorio=[[request.form['metodo'],request.form['gravedad'],request.form['diametro'],request.form['altura'],request.form['volumen']],[request.form['PMS1'],request.form['PMS2'],request.form['PMS3'],request.form['PMS4'],request.form['PMS5']],[request.form['PM1'],request.form['PM2'],request.form['PM3'],request.form['PM4'],request.form['PM5']],[request.form['numerocontenedor1'],request.form['numerocontenedor2'],request.form['numerocontenedor3'],request.form['numerocontenedor4'],request.form['numerocontenedor5'],request.form['numerocontenedor6'],request.form['numerocontenedor7'],request.form['numerocontenedor8'],request.form['numerocontenedor9'],request.form['numerocontenedor10']],[[request.form['MR1'],request.form['MRSH1'],request.form['MRSS1']],[request.form['MR2'],request.form['MRSH2'],request.form['MRSS2']],[request.form['MR3'],request.form['MRSH3'],request.form['MRSS3']],[request.form['MR4'],request.form['MRSH4'],request.form['MRSS4']],[request.form['MR5'],request.form['MRSH5'],request.form['MRSS5']],[request.form['MR6'],request.form['MRSH6'],request.form['MRSS6']],[request.form['MR7'],request.form['MRSH7'],request.form['MRSS7']],[request.form['MR8'],request.form['MRSH8'],request.form['MRSS8']],[request.form['MR9'],request.form['MRSH9'],request.form['MRSS9']],[request.form['MR10'],request.form['MRSH10'],request.form['MRSS10']]]],usuario=session['username'],ci=session['cedula'],_id=request.form['id'])
        if proctor[0] == 1:
            flash(str(proctor[1]))
            return redirect(url_for('proctor_estandar_AASHTO'))
            #return render_template('ensayo_compactacion_proctor_modificado_astm_resultado.html', titulo=titulo, usuario=session['username'],roles=session['rol'],resultado=1, datos=Modelo().Modelo_mostrar_datos_proctor_astm(),tipo=session['tipo'],dato=Modelo().Modelo_mostrar_solicitud_trabajo_externo())
        else:
            return render_template('ensayo_compactacion_proctor_estandar_aashto_resultado.html', titulo=titulo, usuario=session['username'],roles=session['rol'],resultado=1, datos=Modelo().Modelo_mostrar_datos_proctor_estandar_aashto(),tipo=session['tipo'],dato=Modelo().Modelo_mostrar_solicitud_trabajo_externo())
    else:
        return render_template('ensayo_compactacion_proctor_estandar_aashto_resultado.html', titulo=titulo, usuario=session['username'],roles=session['rol'],resultado=1, datos=Modelo().Modelo_mostrar_datos_proctor_estandar_aashto(),tipo=session['tipo'],dato=Modelo().Modelo_mostrar_solicitud_trabajo_externo())


@app.route('/reporte_proctor_estandar_aashto/<string:id_data>', methods = ['GET'])      #REPORTE DEL FORMULARIO DE SOLICITUD
def reporte_proctor_estandar_aashto(id_data):
    a= Modelo().Modelo_reporte_proctor_estandar_aashto(id_data)
    return reporte_proctor_estandar_aashto2(a)

# # ************************************************************* PROCTOR FIN ***************************************************************************



#****************************************************** GRANULOMETRIA AASHTO T-27 **************************************

@app.route('/granulometria_aashto', methods=['GET','POST'])
def granulometria_aashto():
    titulo='GRANULOMETRIA (AASHTO T-27)'
    return render_template('ensayo_de_granulometria_aashto.html', titulo=titulo, usuario=session['username'],roles=session['rol'],LL=Modelo().Modelo_lista_limite_liquido_aashto(),tipo=session['tipo'],dato=Modelo().Modelo_mostrar_solicitud_trabajo_externo())


@app.route('/calcular_granulometria_aashto', methods=['GET','POST'])
def calcular_granulometria_aashto():
    titulo = 'GRANULOMETRIA (AASHTO T-27)'
    ip=0
    if request.method == 'POST':
        t = [request.form['t1'],request.form['t2'],request.form['t3'],request.form['t4'],request.form['t5'],request.form['t6'],request.form['t7'],request.form['t8'],request.form['t9']]
        tamiz = [item for item in t if len(item) > 0]

        pr = [request.form['pg1'],request.form['pg2'],request.form['pg3'],request.form['pg4'],request.form['pg5'],request.form['pg6'],request.form['pg7'],request.form['pg8'],request.form['pg9']]
        peso_ret = [item for item in pr if len(item) > 0]

        if len(tamiz)!=len(peso_ret):
            flash("ingrese los datos de manera correcta")
            return redirect(url_for('granulometria_aashto'))

        if str(request.form['limite_liquido'])=='seleccionar':
            granulometria=Modelo().Modelo_granulometria_aashto(datos_generales=[request.form['proyecto'].title(),request.form['ubicacion'].title(),request.form['descmuestra'].title(),request.form['tipomuestra'].title(),request.form['laboratista'].title(),request.form['solicitante'].title(),request.form['jefecarrera'].title(),time.strftime("%Y-%m-%d")],datos_muestra_laboratorio=[[request.form['p1'],request.form['p2'],request.form['pc'],request.form['pht'],request.form['sh']],tamiz,peso_ret,[request.form['pf1'],request.form['pf2'],request.form['pf3'],],['seleccionar','ninguno']],usuario=session['username'],ci=session['cedula'],ensayo=titulo)
        else:
            for i in Modelo().Modelo_lista_limite_liquido_aashto():
                if i[0] == float(request.form['limite_liquido']):
                    ip= i[1]
            granulometria=Modelo().Modelo_granulometria_aashto(datos_generales=[request.form['proyecto'].title(),request.form['ubicacion'].title(),request.form['descmuestra'].title(),request.form['tipomuestra'].title(),request.form['laboratista'].title(),request.form['solicitante'].title(),request.form['jefecarrera'].title(),time.strftime("%Y-%m-%d")],datos_muestra_laboratorio=[[request.form['p1'],request.form['p2'],request.form['pc'],request.form['pht'],request.form['sh']],tamiz,peso_ret,[request.form['pf1'],request.form['pf2'],request.form['pf3'],],[request.form['limite_liquido'],ip]],usuario=session['username'],ci=session['cedula'],ensayo=titulo)
        if granulometria[0]==1:
            flash(str(granulometria[1]))
            return redirect(url_for('granulometria_aashto'))
        else:
            return render_template('ensayo_de_granulometria_aashto_resultado.html', titulo=titulo, usuario=session['username'],roles=session['rol'], resultado=1, datos=Modelo().Modelo_mostrar_datos_granulometria_aashto(),tam_tamiz=len(Modelo().Modelo_mostrar_datos_granulometria_aashto()['datos_muestra_laboratorio'][1]),LL=Modelo().Modelo_lista_limite_liquido_aashto(),tipo=session['tipo'],dato=Modelo().Modelo_mostrar_solicitud_trabajo_externo())
    else:
        return redirect(url_for('granulometria_aashto'))



@app.route('/modificar_calculo_granulometria_aashto', methods=['GET','POST'])
def modificar_calculo_granulometria_aashto():
    titulo = 'GRANULOMETRIA (AASHTO T-27)'
    if request.method == 'POST':
        t = [request.form['t1'],request.form['t2'],request.form['t3'],request.form['t4'],request.form['t5'],request.form['t6'],request.form['t7'],request.form['t8'],request.form['t9']]
        tamiz = [item for item in t if len(item) > 0]

        pr = [request.form['pg1'],request.form['pg2'],request.form['pg3'],request.form['pg4'],request.form['pg5'],request.form['pg6'],request.form['pg7'],request.form['pg8'],request.form['pg9']]
        peso_ret = [item for item in pr if len(item) > 0]

        if len(tamiz)!=len(peso_ret):
            flash("ingrese los datos de manera correcta")
            return render_template('ensayo_de_granulometria_aashto_resultado.html', titulo=titulo, usuario=session['username'],roles=session['rol'], resultado=1, datos=Modelo().Modelo_mostrar_datos_granulometria_aashto(),tam_tamiz=len(Modelo().Modelo_mostrar_datos_granulometria_aashto()['datos_muestra_laboratorio'][1]),LL=Modelo().Modelo_lista_limite_liquido_aashto(),tipo=session['tipo'],dato=Modelo().Modelo_mostrar_solicitud_trabajo_externo())

        if str(request.form['limite_liquido'])=='seleccionar':

            granulometria=Modelo().Modelo_modificar_calculo_granulometria_aashto(datos_generales=[request.form['proyecto'].title(),request.form['ubicacion'].title(),request.form['descmuestra'].title(),request.form['tipomuestra'].title(),request.form['laboratista'].title(),request.form['solicitante'].title(),request.form['jefecarrera'].title(),time.strftime("%Y-%m-%d")],datos_muestra_laboratorio=[[request.form['p1'],request.form['p2'],request.form['pc'],request.form['pht'],request.form['sh']],tamiz,peso_ret,[request.form['pf1'],request.form['pf2'],request.form['pf3'],],['seleccionar','ninguno']],usuario=session['username'],ci=session['cedula'],ensayo=titulo,_id=request.form['id'])
        else:
            for i in Modelo().Modelo_lista_limite_liquido_aashto():
                if i[0] == float(request.form['limite_liquido']):
                    ip= i[1]
            granulometria=Modelo().Modelo_modificar_calculo_granulometria_aashto(datos_generales=[request.form['proyecto'].title(),request.form['ubicacion'].title(),request.form['descmuestra'].title(),request.form['tipomuestra'].title(),request.form['laboratista'].title(),request.form['solicitante'].title(),request.form['jefecarrera'].title(),time.strftime("%Y-%m-%d")],datos_muestra_laboratorio=[[request.form['p1'],request.form['p2'],request.form['pc'],request.form['pht'],request.form['sh']],tamiz,peso_ret,[request.form['pf1'],request.form['pf2'],request.form['pf3'],],[request.form['limite_liquido'],ip]],usuario=session['username'],ci=session['cedula'],ensayo=titulo,_id=request.form['id'])
        if granulometria[0]==1:
            flash("error de calculo con desface de : " +str(round(granulometria[1],2)))
            return render_template('ensayo_de_granulometria_aashto_resultado.html', titulo=titulo, usuario=session['username'],roles=session['rol'], resultado=1, datos=Modelo().Modelo_mostrar_datos_granulometria_aashto(),tam_tamiz=len(Modelo().Modelo_mostrar_datos_granulometria_aashto()['datos_muestra_laboratorio'][1]),LL=Modelo().Modelo_lista_limite_liquido_aashto(),tipo=session['tipo'],dato=Modelo().Modelo_mostrar_solicitud_trabajo_externo())
        else:
            return render_template('ensayo_de_granulometria_aashto_resultado.html', titulo=titulo, usuario=session['username'],roles=session['rol'], resultado=1, datos=Modelo().Modelo_mostrar_datos_granulometria_aashto(),tam_tamiz=len(Modelo().Modelo_mostrar_datos_granulometria_aashto()['datos_muestra_laboratorio'][1]),LL=Modelo().Modelo_lista_limite_liquido_aashto(),tipo=session['tipo'],dato=Modelo().Modelo_mostrar_solicitud_trabajo_externo())
    else:
        return redirect(url_for('granulometria_aashto'))

@app.route('/reporte_granulometria_aashto/<string:id_data>', methods = ['GET'])      #REPORTE DEL FORMULARIO DE SOLICITUD
def reporte_granulometria_aashto(id_data):
    a= Modelo().Modelo_reporte_granulometria_aashto(id_data)
    return reporte_granulometria_aashto_2(a)
#------------------------------------------------------ GRANULOMETRIA AASHTO T-27 FIN ----------------------------------

#************************************** LIME DE CONTRACCION ************************************************************
@app.route('/limite_de_contraccion_astm', methods=['GET','POST'])
def limite_de_contraccion_astm():
    titulo='LIMITE DE CONTRACCIÓN (ASTM D427)'.decode('utf-8').strip() # si funciona yheaaa
    return render_template('ensayo_limite_de_contraccion_astm.html', titulo=titulo, usuario=session['username'],roles=session['rol'],tipo=session['tipo'],dato=Modelo().Modelo_mostrar_solicitud_trabajo_externo())


@app.route('/calcular_limite_de_contraccion_astm', methods=['GET','POST'])
def calcular_limite_de_contraccion_astm():
    titulo = 'LIMITE DE CONTRACCIÓN (ASTM D427)'.decode('utf-8').strip()
    if request.method == 'POST':

        resultado=Modelo().Modelo_calculo_limite_de_contraccion_astm(datos_generales=[request.form['proyecto'].title(),request.form['ubicacion'].title(),request.form['descmuestra'].title(),request.form['tipomuestra'].title(),request.form['laboratista'].title(),request.form['solicitante'].title(),request.form['jefecarrera'].title(),time.strftime("%Y-%m-%d")],datos_muestra_laboratorio=[request.form['DM'],request.form['MMRV'],request.form['MRC'],request.form['MRCMH'],request.form['MRCMS'],request.form['MMD'],request.form['TA']],usuario=session['username'],ci=session['cedula'],ensayo=titulo)
        if resultado[0]==1:
            flash(resultado[1])
            return redirect(url_for('limite_de_contraccion_astm'))
        else:
            return render_template('ensayo_limite_de_contraccion_astm_resultado.html', titulo=titulo, usuario=session['username'],roles=session['rol'], resultado=1, datos=Modelo().Modelo_mostrar_datos_limite_de_contraccion(),tipo=session['tipo'],dato=Modelo().Modelo_mostrar_solicitud_trabajo_externo())
    else:
        return redirect(url_for('limite_de_contraccion_astm'))

@app.route('/modificar_calculo_limite_de_contraccion_astm', methods=['GET','POST'])
def modificar_calculo_limite_de_contraccion_astm():
    titulo = 'LIMITE DE CONTRACCIÓN (ASTM D427)'.decode('utf-8').strip()
    if request.method == 'POST':
        resultado=Modelo().Modelo_modificar_calculo_limite_de_contraccion(datos_generales=[request.form['proyecto'].title(),request.form['ubicacion'].title(),request.form['descmuestra'].title(),request.form['tipomuestra'].title(),request.form['laboratista'].title(),request.form['solicitante'].title(),request.form['jefecarrera'].title(),time.strftime("%Y-%m-%d")],datos_muestra_laboratorio=[request.form['DM'],request.form['MMRV'],request.form['MRC'],request.form['MRCMH'],request.form['MRCMS'],request.form['MMD'],request.form['TA']],usuario=session['username'],ci=session['cedula'],_id=request.form['id'])
        if resultado[0]==1:
            flash(resultado[1])
            return redirect(url_for('limite_de_contraccion_astm'))
        else:
            return render_template('ensayo_limite_de_contraccion_astm_resultado.html', titulo=titulo, usuario=session['username'],roles=session['rol'], resultado=1, datos=Modelo().Modelo_mostrar_datos_limite_de_contraccion(),tipo=session['tipo'],dato=Modelo().Modelo_mostrar_solicitud_trabajo_externo())
    else:
        return redirect(url_for('limite_de_contraccion_astm'))

@app.route('/reporte_limite_de_contraccion_astm/<string:id_data>', methods = ['GET'])      #REPORTE DEL FORMULARIO DE SOLICITUD
def reporte_limite_de_contraccion_astm(id_data):
    a= Modelo().Modelo_reporte_limite_de_contraccion_astm(id_data)
    return reporte_limite_de_contraccion_astm2(a)
#-----------------------------------------------------------------------------------------------------------------------






#******************************************* CONO DE ARENA ASTM D 1555 *************************************************
@app.route('/cono_de_arena_astm', methods=['GET','POST'])
def cono_de_arena_astm():
    titulo='CONO DE ARENA (ASTM D1556-64)'.decode('utf-8').strip() # si funciona yheaaa
    return render_template('ensayo_cono_de_arena_astm.html', titulo=titulo, usuario=session['username'],roles=session['rol'],PROCTOR=Modelo().Modelo_lista_proctor_densidad_maxima(),tipo=session['tipo'],dato=Modelo().Modelo_mostrar_solicitud_trabajo_externo())





@app.route('/calcular_cono_de_arena_astm', methods=['GET','POST'])
def calcular_cono_de_arena_astm():
    titulo = 'CONO DE ARENA (ASTM D1556-64)'.decode('utf-8').strip()  # si funciona yheaaa
    if request.method == 'POST':

        cpua=[request.form['peso_recipiente_vacio1'],request.form['peso_recipiente_arena2'],request.form['volumen3']]
        calculo_peso_unitario_arena = [item for item in cpua if len(item) > 0]
        pua=[request.form['peso_unitario_arena1'],request.form['peso_unitario_arena2'],request.form['peso_unitario_arena3'],request.form['peso_unitario_arena4']]
        peso_unitario_arena = [item for item in pua if len(item) > 0]

        if len(calculo_peso_unitario_arena)==3:
            calc_peso_unitario=[request.form['peso_recipiente_vacio1'],request.form['peso_recipiente_arena2'],request.form['volumen3']]
            estado = 1
        else:
            if len(peso_unitario_arena)<4:
                flash("error ingrese los datos de peso unitario de la arena de manerea correcta")
                return redirect(url_for('cono_de_arena_astm'))
            else:
                estado=2
                calc_peso_unitario=[0,0,0]

        humedad=[[request.form['numero_cont1'],request.form['masa_recip1'],request.form['masa_cont_humedo1'],request.form['masa_cont_seco1']],[request.form['numero_cont2'],request.form['masa_recip2'],request.form['masa_cont_humedo2'],request.form['masa_cont_seco2']],[request.form['numero_cont3'],request.form['masa_recip3'],request.form['masa_cont_humedo3'],request.form['masa_cont_seco3']],[request.form['numero_cont4'],request.form['masa_recip4'],request.form['masa_cont_humedo4'],request.form['masa_cont_seco4']]]
        cono=[[request.form['peso_unitario_arena1'],request.form['volumen_cono1'],request.form['profundidad1'],request.form['grado_especificacion1'],request.form['peso_frasco_arena_antes1'],request.form['peso_frasco_arena_despues1'],request.form['peso_muestra_humeda1'],request.form['pozo1']],[request.form['peso_unitario_arena2'],request.form['volumen_cono2'],request.form['profundidad2'],request.form['grado_especificacion2'],request.form['peso_frasco_arena_antes2'],request.form['peso_frasco_arena_despues2'],request.form['peso_muestra_humeda2'],request.form['pozo2']],[request.form['peso_unitario_arena3'],request.form['volumen_cono3'],request.form['profundidad3'],request.form['grado_especificacion3'],request.form['peso_frasco_arena_antes3'],request.form['peso_frasco_arena_despues3'],request.form['peso_muestra_humeda3'],request.form['pozo3']],[request.form['peso_unitario_arena4'],request.form['volumen_cono4'],request.form['profundidad4'],request.form['grado_especificacion4'],request.form['peso_frasco_arena_antes4'],request.form['peso_frasco_arena_despues4'],request.form['peso_muestra_humeda4'],request.form['pozo4']]]
        datos=[[request.form['numero_solici1'],request.form['fecha_soli1'],request.form['material_proce1'],request.form['progesiva1'],request.form['progesiva2'],request.form['lado1'],request.form['tramo_inicio1'],request.form['tramo_inicio2'],request.form['tramo_final1'],request.form['tramo_final2'],request.form['fecha_ejec1'],request.form['capa1'],request.form['progresiva_ensayo1'],request.form['progresiva_ensayo2'],request.form['ladof1']],[request.form['numero_solici2'],request.form['fecha_soli2'],request.form['material_proce2'],request.form['progesiva3'],request.form['progesiva4'],request.form['lado2'],request.form['tramo_inicio3'],request.form['tramo_inicio4'],request.form['tramo_final3'],request.form['tramo_final4'],request.form['fecha_ejec2'],request.form['capa2'],request.form['progresiva_ensayo3'],request.form['progresiva_ensayo4'],request.form['ladof2']],[request.form['numero_solici3'],request.form['fecha_soli3'],request.form['material_proce3'],request.form['progesiva5'],request.form['progesiva6'],request.form['lado3'],request.form['tramo_inicio5'],request.form['tramo_inicio6'],request.form['tramo_final5'],request.form['tramo_final6'],request.form['fecha_ejec3'],request.form['capa3'],request.form['progresiva_ensayo5'],request.form['progresiva_ensayo6'],request.form['ladof3']],[request.form['numero_solici4'],request.form['fecha_soli4'],request.form['material_proce4'],request.form['progesiva7'],request.form['progesiva8'],request.form['lado4'],request.form['tramo_inicio7'],request.form['tramo_inicio8'],request.form['tramo_final7'],request.form['tramo_final8'],request.form['fecha_ejec4'],request.form['capa4'],request.form['progresiva_ensayo7'],request.form['progresiva_ensayo8'],request.form['ladof4']]]
        enviar_datos=[datos,[humedad,cono,request.form['densidad_maxima_proctor1'],estado,calc_peso_unitario]]

        cono_arena=Modelo().Modelo_calculo_cono_de_arena(datos_generales=[request.form['proyecto'].title(),request.form['ubicacion'].title(),request.form['descmuestra'].title(),request.form['tipomuestra'].title(),request.form['laboratista'].title(),request.form['solicitante'].title(),request.form['jefecarrera'].title(),time.strftime("%Y-%m-%d")],datos_muestra_laboratorio=enviar_datos,usuario=session['username'],ci=session['cedula'],ensayo=titulo)

        if cono_arena[0]==1:
            flash(str(cono_arena[1]))
            return redirect(url_for('cono_de_arena_astm'))
        else:
            return render_template('ensayo_cono_de_arena_astm_resultado.html', titulo=titulo, usuario=session['username'],roles=session['rol'], resultado=1, datos=Modelo().Modelo_mostrar_datos_cono_de_arena_astm(),PROCTOR=Modelo().Modelo_lista_proctor_densidad_maxima(),tipo=session['tipo'],dato=Modelo().Modelo_mostrar_solicitud_trabajo_externo())
    else:
        return redirect(url_for('cono_de_arena_astm'))



@app.route('/modificar_calculo_cono_de_arena_astm', methods=['GET','POST'])
def modificar_calculo_cono_de_arena_astm():
    titulo = 'CONO DE ARENA (ASTM D1556-64)'.decode('utf-8').strip()  # si funciona yheaaa
    if request.method == 'POST':

        cpua = [request.form['peso_recipiente_vacio1'], request.form['peso_recipiente_arena2'],request.form['volumen3']]
        calculo_peso_unitario_arena = [item for item in cpua if len(item) > 0]
        pua=[request.form['peso_unitario_arena1'],request.form['peso_unitario_arena2'],request.form['peso_unitario_arena3'],request.form['peso_unitario_arena4']]
        peso_unitario_arena = [item for item in pua if len(item) > 0]

        if len(calculo_peso_unitario_arena)==3:
            calc_peso_unitario=[request.form['peso_recipiente_vacio1'],request.form['peso_recipiente_arena2'],request.form['volumen3']]
            estado = 1
        else:
            if len(peso_unitario_arena)<4:
                flash("error ingrese los datos de peso unitario de la arena de manerea correcta")
                return redirect(url_for('cono_de_arena_astm'))
            else:
                estado=2
                calc_peso_unitario=[0,0,0]

        humedad=[[request.form['numero_cont1'],request.form['masa_recip1'],request.form['masa_cont_humedo1'],request.form['masa_cont_seco1']],[request.form['numero_cont2'],request.form['masa_recip2'],request.form['masa_cont_humedo2'],request.form['masa_cont_seco2']],[request.form['numero_cont3'],request.form['masa_recip3'],request.form['masa_cont_humedo3'],request.form['masa_cont_seco3']],[request.form['numero_cont4'],request.form['masa_recip4'],request.form['masa_cont_humedo4'],request.form['masa_cont_seco4']]]
        cono=[[request.form['peso_unitario_arena1'],request.form['volumen_cono1'],request.form['profundidad1'],request.form['grado_especificacion1'],request.form['peso_frasco_arena_antes1'],request.form['peso_frasco_arena_despues1'],request.form['peso_muestra_humeda1'],request.form['pozo1']],[request.form['peso_unitario_arena2'],request.form['volumen_cono2'],request.form['profundidad2'],request.form['grado_especificacion2'],request.form['peso_frasco_arena_antes2'],request.form['peso_frasco_arena_despues2'],request.form['peso_muestra_humeda2'],request.form['pozo2']],[request.form['peso_unitario_arena3'],request.form['volumen_cono3'],request.form['profundidad3'],request.form['grado_especificacion3'],request.form['peso_frasco_arena_antes3'],request.form['peso_frasco_arena_despues3'],request.form['peso_muestra_humeda3'],request.form['pozo3']],[request.form['peso_unitario_arena4'],request.form['volumen_cono4'],request.form['profundidad4'],request.form['grado_especificacion4'],request.form['peso_frasco_arena_antes4'],request.form['peso_frasco_arena_despues4'],request.form['peso_muestra_humeda4'],request.form['pozo4']]]
        datos=[[request.form['numero_solici1'],request.form['fecha_soli1'],request.form['material_proce1'],request.form['progesiva1'],request.form['progesiva2'],request.form['lado1'],request.form['tramo_inicio1'],request.form['tramo_inicio2'],request.form['tramo_final1'],request.form['tramo_final2'],request.form['fecha_ejec1'],request.form['capa1'],request.form['progresiva_ensayo1'],request.form['progresiva_ensayo2'],request.form['ladof1']],[request.form['numero_solici2'],request.form['fecha_soli2'],request.form['material_proce2'],request.form['progesiva3'],request.form['progesiva4'],request.form['lado2'],request.form['tramo_inicio3'],request.form['tramo_inicio4'],request.form['tramo_final3'],request.form['tramo_final4'],request.form['fecha_ejec2'],request.form['capa2'],request.form['progresiva_ensayo3'],request.form['progresiva_ensayo4'],request.form['ladof2']],[request.form['numero_solici3'],request.form['fecha_soli3'],request.form['material_proce3'],request.form['progesiva5'],request.form['progesiva6'],request.form['lado3'],request.form['tramo_inicio5'],request.form['tramo_inicio6'],request.form['tramo_final5'],request.form['tramo_final6'],request.form['fecha_ejec3'],request.form['capa3'],request.form['progresiva_ensayo5'],request.form['progresiva_ensayo6'],request.form['ladof3']],[request.form['numero_solici4'],request.form['fecha_soli4'],request.form['material_proce4'],request.form['progesiva7'],request.form['progesiva8'],request.form['lado4'],request.form['tramo_inicio7'],request.form['tramo_inicio8'],request.form['tramo_final7'],request.form['tramo_final8'],request.form['fecha_ejec4'],request.form['capa4'],request.form['progresiva_ensayo7'],request.form['progresiva_ensayo8'],request.form['ladof4']]]
        enviar_datos=[datos,[humedad,cono,request.form['densidad_maxima_proctor1'],estado,calc_peso_unitario]]

        resultado=Modelo().Modelo_modificar_calculo_cono_de_arena_astm(datos_generales=[request.form['proyecto'].title(),request.form['ubicacion'].title(),request.form['descmuestra'].title(),request.form['tipomuestra'].title(),request.form['laboratista'].title(),request.form['solicitante'].title(),request.form['jefecarrera'].title(),time.strftime("%Y-%m-%d")],datos_muestra_laboratorio=enviar_datos,usuario=session['username'],ci=session['cedula'],_id=request.form['id'])
        if resultado[0]==1:
            flash(resultado[1])
            return redirect(url_for('cono_de_arena_astm'))
        else:
            return render_template('ensayo_cono_de_arena_astm_resultado.html', titulo=titulo, usuario=session['username'],roles=session['rol'], resultado=1, datos=Modelo().Modelo_mostrar_datos_cono_de_arena_astm(),PROCTOR=Modelo().Modelo_lista_proctor_densidad_maxima(),tipo=session['tipo'],dato=Modelo().Modelo_mostrar_solicitud_trabajo_externo())
    else:
        return render_template('ensayo_cono_de_arena_astm_resultado.html', titulo=titulo, usuario=session['username'],roles=session['rol'], resultado=1, datos=Modelo().Modelo_mostrar_datos_cono_de_arena_astm(),PROCTOR=Modelo().Modelo_lista_proctor_densidad_maxima(),tipo=session['tipo'],dato=Modelo().Modelo_mostrar_solicitud_trabajo_externo())


@app.route('/reporte_cono_de_arena_astm/<string:id_data>', methods = ['GET'])      #REPORTE DEL FORMULARIO DE SOLICITUD
def reporte_cono_de_arena_astm(id_data):
    a= Modelo().Modelo_reporte_cono_de_arena_astm(id_data)
    return reporte_cono_de_arena2(a)


#-----------------------------------------------------------------------------------------------------------------------








########################################### ENSAYOS DE GEOTECNIA #####################################################

# /************************************************************ CBR ENSAYO ************************************************************************

@app.route('/cbr_astm', methods=['GET','POST'])
def cbr_astm():
    titulo='INDICE DE SOPORTE CALIFORNIA CBR (ASTM D1883-99)'.decode('utf-8').strip()
    return render_template('ensayo_indice_de_soporte_cbr_astm.html', titulo=titulo, usuario=session['username'],roles=session['rol'],tipo=session['tipo'],dato=Modelo().Modelo_mostrar_solicitud_trabajo_externo())






@app.route('/calcular_cbr_astm', methods=['GET','POST'])
def calcular_cbr_astm():
    titulo = 'INDICE DE SOPORTE CALIFORNIA CBR (ASTM D1883-99)'.decode('utf-8').strip()  # si funciona yheaaa
    if request.method == 'POST':


        compactacion=[[[request.form['peso_hum_antes1'],request.form['peso_molde1'],request.form['volumen_muestra1']],[request.form['peso_hum_despues1']]],[[request.form['peso_hum_antes2'],request.form['peso_molde2'],request.form['volumen_muestra2']],[request.form['peso_hum_despues2']]],[[request.form['peso_hum_antes3'],request.form['peso_molde3'],request.form['volumen_muestra3']],[request.form['peso_hum_despues3']]]]
        humedad=[[[[request.form['masa_recipiente1'],request.form['masa_rec_hum1'],request.form['masa_rec_seco1'],request.form['num_recipiente1']],[request.form['masa_recipiente2'],request.form['masa_rec_hum2'],request.form['masa_rec_seco2'],request.form['num_recipiente2']]],[[request.form['masa_recipiente3'],request.form['masa_rec_hum3'],request.form['masa_rec_seco3'],request.form['num_recipiente3']],[request.form['masa_recipiente4'],request.form['masa_rec_hum4'],request.form['masa_rec_seco4'],request.form['num_recipiente4']]]],[[[request.form['masa_recipiente5'],request.form['masa_rec_hum5'],request.form['masa_rec_seco5'],request.form['num_recipiente5']],[request.form['masa_recipiente6'],request.form['masa_rec_hum6'],request.form['masa_rec_seco6'],request.form['num_recipiente6']]],[[request.form['masa_recipiente7'],request.form['masa_rec_hum7'],request.form['masa_rec_seco7'],request.form['num_recipiente7']],[request.form['masa_recipiente8'],request.form['masa_rec_hum8'],request.form['masa_rec_seco8'],request.form['num_recipiente8']]]],[[[request.form['masa_recipiente9'],request.form['masa_rec_hum9'],request.form['masa_rec_seco9'],request.form['num_recipiente9']],[request.form['masa_recipiente10'],request.form['masa_rec_hum10'],request.form['masa_rec_seco10'],request.form['num_recipiente10']]],[[request.form['masa_recipiente11'],request.form['masa_rec_hum11'],request.form['masa_rec_seco11'],request.form['num_recipiente11']],[request.form['masa_recipiente12'],request.form['masa_rec_hum12'],request.form['masa_rec_seco12'],request.form['num_recipiente12']]]]]
        expansion = [[request.form['lectura_exten1'], request.form['lectura_exten2'],request.form['lectura_exten3'], request.form['lectura_exten4'], request.form['lectura_exten5']], [request.form['lectura_exten6'], request.form['lectura_exten7'],request.form['lectura_exten8'], request.form['lectura_exten9'], request.form['lectura_exten10']], [request.form['lectura_exten11'], request.form['lectura_exten12'],request.form['lectura_exten13'], request.form['lectura_exten14'], request.form['lectura_exten15']]]
        fecha_hora=[[request.form['fecha1'],request.form['fecha2'],request.form['fecha3'],request.form['fecha4'],request.form['fecha5']],[request.form['hora1'],request.form['hora2'],request.form['hora3'],request.form['hora4'],request.form['hora5']]]
        L1=[request.form['lectura_dial1'],request.form['lectura_dial2'],request.form['lectura_dial3'],request.form['lectura_dial4'],request.form['lectura_dial5'],request.form['lectura_dial6'],request.form['lectura_dial7'],request.form['lectura_dial8'],request.form['lectura_dial9'],request.form['lectura_dial10'],request.form['lectura_dial11'],request.form['lectura_dial12']]
        lectura_dial_1 = [item for item in L1 if len(item) > 0]
        L2=[request.form['lectura_dial13'],request.form['lectura_dial14'],request.form['lectura_dial15'],request.form['lectura_dial16'],request.form['lectura_dial17'],request.form['lectura_dial18'],request.form['lectura_dial19'],request.form['lectura_dial20'],request.form['lectura_dial21'],request.form['lectura_dial22'],request.form['lectura_dial23'],request.form['lectura_dial24']]
        lectura_dial_2 = [item for item in L2 if len(item) > 0]
        L3=[request.form['lectura_dial25'],request.form['lectura_dial26'],request.form['lectura_dial27'],request.form['lectura_dial28'],request.form['lectura_dial29'],request.form['lectura_dial30'],request.form['lectura_dial31'],request.form['lectura_dial32'],request.form['lectura_dial33'],request.form['lectura_dial34'],request.form['lectura_dial35'],request.form['lectura_dial36']]
        lectura_dial_3 = [item for item in L3 if len(item) > 0]

        if len(lectura_dial_1)!= len(lectura_dial_2) or len(lectura_dial_1)!= len(lectura_dial_3) or len(lectura_dial_2)!= len(lectura_dial_3) :
            flash("Ingrese los valores de lectura dia correctamente")
            return redirect(url_for('cbr_astm'))
        lectura_dial_total= [lectura_dial_1,lectura_dial_2,lectura_dial_3]
        datos_compactacion=[request.form['molde1'],request.form['molde2'],request.form['molde3'],request.form['num_capas1'],request.form['num_capas2'],request.form['num_capas3'],request.form['num_golpes1'],request.form['num_golpes2'],request.form['num_golpes3']]
        enviar=[compactacion,humedad,[fecha_hora,expansion],lectura_dial_total,request.form['numero_abaco'],datos_compactacion]
        cbr=Modelo().Modelo_calculo_CBR_astm(datos_generales=[request.form['proyecto'].title(),request.form['ubicacion'].title(),request.form['descmuestra'].title(),request.form['tipomuestra'].title(),request.form['laboratista'].title(),request.form['solicitante'].title(),request.form['jefecarrera'].title(),time.strftime("%Y-%m-%d")],datos_muestra_laboratorio=enviar,usuario=session['username'],ci=session['cedula'],ensayo=titulo)

        if cbr[0]==1:
            flash(str(cbr[1]))
            return redirect(url_for('cbr_astm'))
        else:
            return render_template('ensayo_indice_de_soporte_cbr_astm_resultado.html', titulo=titulo, usuario=session['username'],roles=session['rol'], resultado=1, datos=Modelo().Modelo_mostrar_datos_indice_de_soporte_cbr_astm(),tipo=session['tipo'],dato=Modelo().Modelo_mostrar_solicitud_trabajo_externo())
    else:
        return redirect(url_for('cbr_astm'))





@app.route('/modificar_calculo_cbr_astm', methods=['GET','POST'])
def modificar_calculo_cbr_astm():
    titulo = 'INDICE DE SOPORTE CALIFORNIA CBR (ASTM D1883-99)'.decode('utf-8').strip()  # si funciona yheaaa
    if request.method == 'POST':


        compactacion=[[[request.form['peso_hum_antes1'],request.form['peso_molde1'],request.form['volumen_muestra1']],[request.form['peso_hum_despues1']]],[[request.form['peso_hum_antes2'],request.form['peso_molde2'],request.form['volumen_muestra2']],[request.form['peso_hum_despues2']]],[[request.form['peso_hum_antes3'],request.form['peso_molde3'],request.form['volumen_muestra3']],[request.form['peso_hum_despues3']]]]
        humedad=[[[[request.form['masa_recipiente1'],request.form['masa_rec_hum1'],request.form['masa_rec_seco1'],request.form['num_recipiente1']],[request.form['masa_recipiente2'],request.form['masa_rec_hum2'],request.form['masa_rec_seco2'],request.form['num_recipiente2']]],[[request.form['masa_recipiente3'],request.form['masa_rec_hum3'],request.form['masa_rec_seco3'],request.form['num_recipiente3']],[request.form['masa_recipiente4'],request.form['masa_rec_hum4'],request.form['masa_rec_seco4'],request.form['num_recipiente4']]]],[[[request.form['masa_recipiente5'],request.form['masa_rec_hum5'],request.form['masa_rec_seco5'],request.form['num_recipiente5']],[request.form['masa_recipiente6'],request.form['masa_rec_hum6'],request.form['masa_rec_seco6'],request.form['num_recipiente6']]],[[request.form['masa_recipiente7'],request.form['masa_rec_hum7'],request.form['masa_rec_seco7'],request.form['num_recipiente7']],[request.form['masa_recipiente8'],request.form['masa_rec_hum8'],request.form['masa_rec_seco8'],request.form['num_recipiente8']]]],[[[request.form['masa_recipiente9'],request.form['masa_rec_hum9'],request.form['masa_rec_seco9'],request.form['num_recipiente9']],[request.form['masa_recipiente10'],request.form['masa_rec_hum10'],request.form['masa_rec_seco10'],request.form['num_recipiente10']]],[[request.form['masa_recipiente11'],request.form['masa_rec_hum11'],request.form['masa_rec_seco11'],request.form['num_recipiente11']],[request.form['masa_recipiente12'],request.form['masa_rec_hum12'],request.form['masa_rec_seco12'],request.form['num_recipiente12']]]]]
        expansion = [[request.form['lectura_exten1'], request.form['lectura_exten2'],request.form['lectura_exten3'], request.form['lectura_exten4'], request.form['lectura_exten5']], [request.form['lectura_exten6'], request.form['lectura_exten7'],request.form['lectura_exten8'], request.form['lectura_exten9'], request.form['lectura_exten10']], [request.form['lectura_exten11'], request.form['lectura_exten12'],request.form['lectura_exten13'], request.form['lectura_exten14'], request.form['lectura_exten15']]]
        fecha_hora=[[request.form['fecha1'],request.form['fecha2'],request.form['fecha3'],request.form['fecha4'],request.form['fecha5']],[request.form['hora1'],request.form['hora2'],request.form['hora3'],request.form['hora4'],request.form['hora5']]]
        L1=[request.form['lectura_dial1'],request.form['lectura_dial2'],request.form['lectura_dial3'],request.form['lectura_dial4'],request.form['lectura_dial5'],request.form['lectura_dial6'],request.form['lectura_dial7'],request.form['lectura_dial8'],request.form['lectura_dial9'],request.form['lectura_dial10'],request.form['lectura_dial11'],request.form['lectura_dial12']]
        lectura_dial_1 = [item for item in L1 if len(item) > 0]
        L2=[request.form['lectura_dial13'],request.form['lectura_dial14'],request.form['lectura_dial15'],request.form['lectura_dial16'],request.form['lectura_dial17'],request.form['lectura_dial18'],request.form['lectura_dial19'],request.form['lectura_dial20'],request.form['lectura_dial21'],request.form['lectura_dial22'],request.form['lectura_dial23'],request.form['lectura_dial24']]
        lectura_dial_2 = [item for item in L2 if len(item) > 0]
        L3=[request.form['lectura_dial25'],request.form['lectura_dial26'],request.form['lectura_dial27'],request.form['lectura_dial28'],request.form['lectura_dial29'],request.form['lectura_dial30'],request.form['lectura_dial31'],request.form['lectura_dial32'],request.form['lectura_dial33'],request.form['lectura_dial34'],request.form['lectura_dial35'],request.form['lectura_dial36']]
        lectura_dial_3 = [item for item in L3 if len(item) > 0]

        if len(lectura_dial_1)!= len(lectura_dial_2) or len(lectura_dial_1)!= len(lectura_dial_3) or len(lectura_dial_2)!= len(lectura_dial_3) :
            flash("Ingrese los valores de lectura dia correctamente")
            return redirect(url_for('cbr_astm'))
        lectura_dial_total= [lectura_dial_1,lectura_dial_2,lectura_dial_3]
        datos_compactacion=[request.form['molde1'],request.form['molde2'],request.form['molde3'],request.form['num_capas1'],request.form['num_capas2'],request.form['num_capas3'],request.form['num_golpes1'],request.form['num_golpes2'],request.form['num_golpes3']]
        enviar=[compactacion,humedad,[fecha_hora,expansion],lectura_dial_total,request.form['numero_abaco'],datos_compactacion]


        resultado=Modelo().Modelo_modificar_calculo_cbr_astm(datos_generales=[request.form['proyecto'].title(),request.form['ubicacion'].title(),request.form['descmuestra'].title(),request.form['tipomuestra'].title(),request.form['laboratista'].title(),request.form['solicitante'].title(),request.form['jefecarrera'].title(),time.strftime("%Y-%m-%d")],datos_muestra_laboratorio=enviar,usuario=session['username'],ci=session['cedula'],_id=request.form['id'])
        if resultado[0]==1:
            flash(resultado[1])
            return redirect(url_for('cbr_astm'))
        else:
            return render_template('ensayo_indice_de_soporte_cbr_astm_resultado.html', titulo=titulo, usuario=session['username'],roles=session['rol'], resultado=1, datos=Modelo().Modelo_mostrar_datos_indice_de_soporte_cbr_astm(),tipo=session['tipo'],dato=Modelo().Modelo_mostrar_solicitud_trabajo_externo())
    else:
        return render_template('ensayo_indice_de_soporte_cbr_astm_resultado.html', titulo=titulo, usuario=session['username'],roles=session['rol'], resultado=1, datos=Modelo().Modelo_mostrar_datos_indice_de_soporte_cbr_astm(),tipo=session['tipo'],dato=Modelo().Modelo_mostrar_solicitud_trabajo_externo())


@app.route('/reporte_indice_de_soporte_cbr_astm/<string:id_data>', methods = ['GET'])      #REPORTE DEL FORMULARIO DE SOLICITUD
def reporte_indice_de_soporte_cbr_astm(id_data):
    a= Modelo().Modelo_reporte_indice_de_soporte_cbr_astm(id_data)
    return reporte_indice_de_soporte_astm(a)

# ************************************************************* CBR FIN ***************************************************************************




#****************************************** corte directo geotecnia inicio *********************************************
@app.route('/corte_directo_astm', methods=['GET','POST'])
def corte_directo_astm():
    titulo = 'CORTE DIRECTO (ASTM D3080)'
    return render_template('ensayo_corte_directo_geotecnia.html', titulo=titulo, usuario=session['username'],roles=session['rol'],PROCTOR=Modelo().Modelo_lista_proctor_densidad_maxima(),tipo=session['tipo'],dato=Modelo().Modelo_mostrar_solicitud_trabajo_externo())



@app.route('/calcular_corte_directo_astm', methods=['GET','POST'])
def calcular_corte_directo_astm():
    titulo = 'CORTE DIRECTO (ASTM D3080)'
    if request.method == 'POST':
        # muestra N#1
        dxprueba = [request.form['Dx1'],request.form['Dx2'],request.form['Dx3'],request.form['Dx4'],request.form['Dx5'],request.form['Dx6'],request.form['Dx7'],request.form['Dx8'],request.form['Dx9'],request.form['Dx10'],request.form['Dx11']]
        dx1 = [item for item in dxprueba if len(item) > 0]
        lectura_dyprueba = [request.form['Dy1'],request.form['Dy2'],request.form['Dy3'],request.form['Dy4'],request.form['Dy5'],request.form['Dy6'],request.form['Dy7'],request.form['Dy8'],request.form['Dy9'],request.form['Dy10'],request.form['Dy11']]
        lectura_dy1 = [item for item in lectura_dyprueba if len(item) > 0]
        lectura_de_fuerza_prueba = [request.form['lecturafuerza1'],request.form['lecturafuerza2'],request.form['lecturafuerza3'],request.form['lecturafuerza4'],request.form['lecturafuerza5'],request.form['lecturafuerza6'],request.form['lecturafuerza7'],request.form['lecturafuerza8'],request.form['lecturafuerza9'],request.form['lecturafuerza10'],request.form['lecturafuerza11']]
        lectura_de_fuerza1 = [item for item in lectura_de_fuerza_prueba if len(item) > 0]

        ## muestra N#2
        dxprueba2 = [request.form['Dxx1'],request.form['Dxx2'],request.form['Dxx3'],request.form['Dxx4'],request.form['Dxx5'],request.form['Dxx6'],request.form['Dxx7'],request.form['Dxx8'],request.form['Dxx9'],request.form['Dxx10'],request.form['Dxx11']]
        dx2 = [item for item in dxprueba2 if len(item) > 0]
        lectura_dyprueba2 = [request.form['Dyy1'],request.form['Dyy2'],request.form['Dyy3'],request.form['Dyy4'],request.form['Dyy5'],request.form['Dyy6'],request.form['Dyy7'],request.form['Dyy8'],request.form['Dyy9'],request.form['Dyy10'],request.form['Dyy11']]
        lectura_dy2 = [item for item in lectura_dyprueba2 if len(item) > 0]
        lectura_de_fuerza_prueba2 = [request.form['lecturafuerzados1'],request.form['lecturafuerzados2'],request.form['lecturafuerzados3'],request.form['lecturafuerzados4'],request.form['lecturafuerzados5'],request.form['lecturafuerzados6'],request.form['lecturafuerzados7'],request.form['lecturafuerzados8'],request.form['lecturafuerzados9'],request.form['lecturafuerzados10'],request.form['lecturafuerzados11']]
        lectura_de_fuerza2 = [item for item in lectura_de_fuerza_prueba2 if len(item) > 0]

        ### muestra N#3
        dxprueba3 = [request.form['Dxxx1'],request.form['Dxxx2'],request.form['Dxxx3'],request.form['Dxxx4'],request.form['Dxxx5'],request.form['Dxxx6'],request.form['Dxxx7'],request.form['Dxxx8'],request.form['Dxxx9'],request.form['Dxxx10'],request.form['Dxxx11']]
        dx3 = [item for item in dxprueba3 if len(item) > 0]
        lectura_dyprueba3 = [request.form['Dyyy1'],request.form['Dyyy2'],request.form['Dyyy3'],request.form['Dyyy4'],request.form['Dyyy5'],request.form['Dyyy6'],request.form['Dyyy7'],request.form['Dyyy8'],request.form['Dyyy9'],request.form['Dyyy10'],request.form['Dyyy11']]
        lectura_dy3 = [item for item in lectura_dyprueba3 if len(item) > 0]
        lectura_de_fuerza_prueba3 = [request.form['lecturafuerzatres1'],request.form['lecturafuerzatres2'],request.form['lecturafuerzatres3'],request.form['lecturafuerzatres4'],request.form['lecturafuerzatres5'],request.form['lecturafuerzatres6'],request.form['lecturafuerzatres7'],request.form['lecturafuerzatres8'],request.form['lecturafuerzatres9'],request.form['lecturafuerzatres10'],request.form['lecturafuerzatres11']]
        lectura_de_fuerza3 = [item for item in lectura_de_fuerza_prueba3 if len(item) > 0]

        datos=[[dx1,lectura_dy1,lectura_de_fuerza1],[dx2,lectura_dy2,lectura_de_fuerza2],[dx3,lectura_dy3,lectura_de_fuerza3]]
        dimecion_interior = [request.form['dimension1'], request.form['dimension2'], request.form['alturainicialproveta']]
        regrecion = [[float(request.form['carganormal1']),float(request.form['carganormal2']),float(request.form['carganormal3'])], [float(request.form['esfuerzonormal1']),float(request.form['esfuerzonormal2']),float(request.form['esfuerzonormal3'])]]
        enviar=[datos,dimecion_interior,regrecion]
        corte_D=Modelo().Modelo_calculo_corte_directo_astm(datos_generales=[request.form['proyecto'].title(),request.form['ubicacion'].title(),request.form['descmuestra'].title(),request.form['tipomuestra'].title(),request.form['laboratista'].title(),request.form['solicitante'].title(),request.form['jefecarrera'].title(),time.strftime("%Y-%m-%d")],datos_muestra_laboratorio=enviar,usuario=session['username'],ci=session['cedula'],ensayo=titulo)

        if corte_D[0]==1:
            flash(str(corte_D[1]))
            return redirect(url_for('corte_directo_astm'))
        else:
            return render_template('ensayo_corte_directo_geotecnia_resultado.html', titulo=titulo, usuario=session['username'],roles=session['rol'], resultado=1, datos=Modelo().Modelo_mostrar_corte_directo_astm(),tipo=session['tipo'],dato=Modelo().Modelo_mostrar_solicitud_trabajo_externo())
    else:
        return redirect(url_for('corte_directo_astm'))





@app.route('/modificar_calculo_corte_directo_astm', methods=['GET','POST'])
def modificar_calculo_corte_directo_astm():
    titulo = 'CORTE DIRECTO (ASTM D3080)'
    if request.method == 'POST':

        # # muestra N#1
        dxprueba = [request.form['Dx1'],request.form['Dx2'],request.form['Dx3'],request.form['Dx4'],request.form['Dx5'],request.form['Dx6'],request.form['Dx7'],request.form['Dx8'],request.form['Dx9'],request.form['Dx10'],request.form['Dx11']]
        dx1 = [item for item in dxprueba if len(item) > 0]
        lectura_dyprueba = [request.form['Dy1'],request.form['Dy2'],request.form['Dy3'],request.form['Dy4'],request.form['Dy5'],request.form['Dy6'],request.form['Dy7'],request.form['Dy8'],request.form['Dy9'],request.form['Dy10'],request.form['Dy11']]
        lectura_dy1 = [item for item in lectura_dyprueba if len(item) > 0]
        lectura_de_fuerza_prueba = [request.form['lecturafuerza1'],request.form['lecturafuerza2'],request.form['lecturafuerza3'],request.form['lecturafuerza4'],request.form['lecturafuerza5'],request.form['lecturafuerza6'],request.form['lecturafuerza7'],request.form['lecturafuerza8'],request.form['lecturafuerza9'],request.form['lecturafuerza10'],request.form['lecturafuerza11']]
        lectura_de_fuerza1 = [item for item in lectura_de_fuerza_prueba if len(item) > 0]

        ## muestra N#2
        dxprueba2 = [request.form['Dxx1'],request.form['Dxx2'],request.form['Dxx3'],request.form['Dxx4'],request.form['Dxx5'],request.form['Dxx6'],request.form['Dxx7'],request.form['Dxx8'],request.form['Dxx9'],request.form['Dxx10'],request.form['Dxx11']]
        dx2 = [item for item in dxprueba2 if len(item) > 0]
        lectura_dyprueba2 = [request.form['Dyy1'],request.form['Dyy2'],request.form['Dyy3'],request.form['Dyy4'],request.form['Dyy5'],request.form['Dyy6'],request.form['Dyy7'],request.form['Dyy8'],request.form['Dyy9'],request.form['Dyy10'],request.form['Dyy11']]
        lectura_dy2 = [item for item in lectura_dyprueba2 if len(item) > 0]
        lectura_de_fuerza_prueba2 = [request.form['lecturafuerzados1'],request.form['lecturafuerzados2'],request.form['lecturafuerzados3'],request.form['lecturafuerzados4'],request.form['lecturafuerzados5'],request.form['lecturafuerzados6'],request.form['lecturafuerzados7'],request.form['lecturafuerzados8'],request.form['lecturafuerzados9'],request.form['lecturafuerzados10'],request.form['lecturafuerzados11']]
        lectura_de_fuerza2 = [item for item in lectura_de_fuerza_prueba2 if len(item) > 0]

        ### muestra N#3
        dxprueba3 = [request.form['Dxxx1'],request.form['Dxxx2'],request.form['Dxxx3'],request.form['Dxxx4'],request.form['Dxxx5'],request.form['Dxxx6'],request.form['Dxxx7'],request.form['Dxxx8'],request.form['Dxxx9'],request.form['Dxxx10'],request.form['Dxxx11']]
        dx3 = [item for item in dxprueba3 if len(item) > 0]
        lectura_dyprueba3 = [request.form['Dyyy1'],request.form['Dyyy2'],request.form['Dyyy3'],request.form['Dyyy4'],request.form['Dyyy5'],request.form['Dyyy6'],request.form['Dyyy7'],request.form['Dyyy8'],request.form['Dyyy9'],request.form['Dyyy10'],request.form['Dyyy11']]
        lectura_dy3 = [item for item in lectura_dyprueba3 if len(item) > 0]
        lectura_de_fuerza_prueba3 = [request.form['lecturafuerzatres1'],request.form['lecturafuerzatres2'],request.form['lecturafuerzatres3'],request.form['lecturafuerzatres4'],request.form['lecturafuerzatres5'],request.form['lecturafuerzatres6'],request.form['lecturafuerzatres7'],request.form['lecturafuerzatres8'],request.form['lecturafuerzatres9'],request.form['lecturafuerzatres10'],request.form['lecturafuerzatres11']]
        lectura_de_fuerza3 = [item for item in lectura_de_fuerza_prueba3 if len(item) > 0]

        datos=[[dx1,lectura_dy1,lectura_de_fuerza1],[dx2,lectura_dy2,lectura_de_fuerza2],[dx3,lectura_dy3,lectura_de_fuerza3]]
        dimecion_interior = [request.form['dimension1'], request.form['dimension2'], request.form['alturainicialproveta']]
        regrecion = [[float(request.form['carganormal1']),float(request.form['carganormal2']),float(request.form['carganormal3'])], [float(request.form['esfuerzonormal1']),float(request.form['esfuerzonormal2']),float(request.form['esfuerzonormal3'])]]
        enviar=[datos,dimecion_interior,regrecion]

        resultado=Modelo().Modelo_modificar_calculo_corte_directo_astm(datos_generales=[request.form['proyecto'].title(),request.form['ubicacion'].title(),request.form['descmuestra'].title(),request.form['tipomuestra'].title(),request.form['laboratista'].title(),request.form['solicitante'].title(),request.form['jefecarrera'].title(),time.strftime("%Y-%m-%d")],datos_muestra_laboratorio=enviar,usuario=session['username'],ci=session['cedula'],_id=request.form['id'])
        if resultado[0]==1:
            flash(resultado[1])
            return redirect(url_for('corte_directo_astm'))
        else:
            return render_template('ensayo_corte_directo_geotecnia_resultado.html', titulo=titulo, usuario=session['username'],roles=session['rol'], resultado=1, datos=Modelo().Modelo_mostrar_corte_directo_astm(),tipo=session['tipo'],dato=Modelo().Modelo_mostrar_solicitud_trabajo_externo())
    else:
        return render_template('ensayo_corte_directo_geotecnia_resultado.html', titulo=titulo, usuario=session['username'],roles=session['rol'], resultado=1, datos=Modelo().Modelo_mostrar_corte_directo_astm(),tipo=session['tipo'],dato=Modelo().Modelo_mostrar_solicitud_trabajo_externo())


@app.route('/reporte_corte_directo_astm_geotec/<string:id_data>', methods = ['GET'])      #REPORTE DEL FORMULARIO DE SOLICITUD
def reporte_corte_directo_astm_geotec(id_data):
    a= Modelo().Modelo_reporte_corte_directo_geotecnia(id_data)
    return reporte_corte_directo_astm_geotecnia(a)
#****************************************** corte directo geotecnia fin ************************************************






#**************************************** LISTA DE ENSAYOS DE GEOTECNIA ************************************************
@app.route('/administrar_lista_de_ensayos_de_geotecnia', methods=['POST','GET']) #MOSTRAR SOLICITUDES DE LABORATORIO
def administrar_lista_de_ensayos_de_geotecnia():
    return render_template('emi_lista_de_ensayos_geotecnia.html', usuario=session['username'],lista_ensayos_suelos=Modelo().Modelo_mostrar_lista_de_ensayos_de_geotecnia(),roles=session['rol'],tipo=session['tipo'])

@app.route('/eliminar_lista_ensayos_geotecnia/<string:id_data>', methods=['GET'])    #ELIMINAR UNA VEZ SE AYA CUMPLIDO EL USO Y LA DEVOLUCION DE LOS MATERILES
def eliminar_lista_ensayos_geotecnia(id_data):
    if Modelo().Modelo_eliminar_lista_ensayos_geotecnia(id_data):
        flash("El registro ha sido eliminado con exito")
        return redirect(url_for('administrar_lista_de_ensayos_de_geotecnia'))
    else:
        flash("No se pudo eliminar el registro")
        return redirect(url_for('administrar_lista_de_ensayos_de_geotecnia'))

########################################################################################################################################################################









#*************************************************** LISTA DE ENSAYOS DE SUELOS ****************************************
@app.route('/administrar_lista_de_ensayos_de_suelos', methods=['POST','GET']) #MOSTRAR SOLICITUDES DE LABORATORIO
def administrar_lista_de_ensayos_de_suelos():
    return render_template('emi_lista_de_ensayos_suelos.html', usuario=session['username'],lista_ensayos_suelos=Modelo().Modelo_mostrar_lista_de_ensayos_de_suelos(),roles=session['rol'],tipo=session['tipo'])





@app.route('/eliminar_lista_ensayos_suelos/<string:id_data>', methods=['GET'])    #ELIMINAR UNA VEZ SE AYA CUMPLIDO EL USO Y LA DEVOLUCION DE LOS MATERILES
def eliminar_lista_ensayos_suelos(id_data):
    if Modelo().Modelo_eliminar_lista_ensayos_suelos(id_data):
        flash("El registro ha sido eliminado con exito")
        return redirect(url_for('administrar_lista_de_ensayos_de_suelos'))
    else:
        flash("No se pudo eliminar el registro")
        return redirect(url_for('administrar_lista_de_ensayos_de_suelos'))
#*************************************************** LISTA DE ENSAYOS DE SUELOS FIN **********************************

#**************************************CERRAR SESSION ******************************************************************

@app.route('/cerrar_sesion')
def cerrar_sesion():
    if 'username' in session:
        session.pop('username')
        session.pop('rol')
        session.pop('cedula')
        return redirect(url_for('login'))





#*************######################*****************   REPORTES DE LOS ENSAYOS ******************######################
def reporte_humedad(datos):
    humedad = datos[1]
    output = cStringIO.StringIO()
    canvas = Canvas("contenido_humedad.pdf", pagesize=letter)
    canvas.setLineWidth(.3)
    canvas.setFont('Helvetica', 10)

    canvas.line(60, 760, 550, 760)  # punto x1, y1 , x2, y2 #HORIZONTAL
    canvas.line(60, 760, 60, 700)  # VERTICAL
    canvas.line(60, 700, 550, 700)  # HORIZONTAL
    canvas.line(550, 760, 550, 700)  # VERTICAL
    canvas.line(190, 760, 190, 700)  # VERTICAL
    canvas.line(400, 760, 400, 700)  # VERTICAL
    # CAJETIN PEQUENO
    canvas.line(400, 745, 550, 745)  # HORIZONTAL
    canvas.line(400, 730, 550, 730)  # HORIZONTAL
    canvas.line(400, 715, 550, 715)  # HORIZONTAL
    canvas.line(470, 760, 470, 715)  # VERTICAL
    # Inseratmos la imagen en el documento

    canvas.drawImage("static/img/emi.jpeg", 70, 710, width=115, height=40)

    # TITULO
    frame1 = Frame(190, 700, 210, 60, showBoundary=1)  # Frame(movX,movY,margenAncho,mrgenAlto)
    bodyStyle = ParagraphStyle('normal', fontSize=24, leading=28, spaceBefore=30, alignment=TA_CENTER)
    s = datos[0]
    story = [Paragraph(s, bodyStyle)]
    story_inframe = KeepInFrame(210, 1 * inch, story)
    frame1.addFromList([story_inframe], canvas)
    # interlineado=740

    # DATOS
    posx = 410
    canvas.setFont('Helvetica', 10)
    canvas.drawString(posx, 750, 'Codigo:')
    canvas.drawString(posx, 735, 'Aprobacion:')
    canvas.drawString(posx, 720, 'Version:')
    canvas.drawString(posx + 70, 750, 'C5117-9')
    canvas.drawString(posx + 70, 735, 'Aprobado')
    canvas.drawString(posx + 70, 720, 'Version 1.1')
    canvas.drawString(posx + 30, 703, 'Página 1 de 1')

    # SEGUNDA CAJETILLA
    puntoAx = 60
    puntoBx = 550
    puntoY = 698
    puntoMedio = (puntoAx + puntoBx) / 2

    canvas.line(60, 680, 550,
                680)  # horizontal arriba (largohacialaIZQUIERDA ,arribaIZQ , largo de la linea hacia la derecha ,arribaDER)
    canvas.setFont('Helvetica', 12)
    canvas.drawString(235, 665, 'A. DATOS GENRALES')  # (# ,  arriba , #)
    canvas.line(60, 680, 60,
                568)  # vertical iquierdo  (mover linea hacia derecha punto arriba, linea hacia arriba, mover linea hacia derecha punto abajo)
    canvas.line(550, 680, 550, 568)  # vertical DERECHO
    canvas.line(60, 661, 550, 661)  ## horizontal abajo
    # primero
    canvas.setFont('Helvetica', 9)
    canvas.drawString(160, 651, 'Proyecto')
    canvas.line(60, 649, 550, 649)  ## horizontal abajo2
    canvas.line(300, 660, 300, 568)  # vertical2 MEDIO
    canvas.drawString(400, 651, 'Fecha')
    canvas.setFont('Helvetica', 12)
    canvas.drawString(70, 633, humedad['datos_generales'][0])
    canvas.drawString(310, 633, humedad['datos_generales'][7])
    canvas.line(60, 630, 550, 630)  ## horizontal abajo3
    # segundo
    canvas.setFont('Helvetica', 9)
    canvas.drawString(160, 620, 'Ubicacion')
    canvas.drawString(400, 620, 'Laboratista')
    canvas.line(60, 618, 550, 618)  ## horizontal abajo4
    canvas.line(60, 599, 550, 599)  ## horizontal abajo5
    canvas.setFont('Helvetica', 12)
    canvas.drawString(70, 602, humedad['datos_generales'][1])
    canvas.drawString(310, 602, humedad['datos_generales'][4])

    # tercero
    canvas.setFont('Helvetica', 9)
    canvas.drawString(120, 589, 'Descripcion De La Muestra')
    canvas.drawString(380, 589, 'Tipo De Muestra')
    canvas.line(60, 587, 550, 587)  ## horizontal abajo6
    canvas.line(60, 568, 550, 568)  ## horizontal abajo7
    canvas.setFont('Helvetica', 12)
    canvas.drawString(70, 571, humedad['datos_generales'][2])
    canvas.drawString(310, 571, humedad['datos_generales'][3])

    # tabla calculos
    canvas.line(60, 520, 550, 520)  ## horizontal abajo8
    canvas.line(60, 490, 550, 490)  ## horizontal abajo9
    canvas.line(60, 520, 60,
                250)  # vertical iquierdo  (mover linea hacia derecha punto arriba, linea hacia arriba, mover linea hacia derecha punto abajo)
    canvas.line(550, 520, 550, 220)  # vertical DERECHO
    canvas.setFont('Helvetica', 12)
    canvas.drawString(120, 498, 'B. CALCULO DETERMINACION DEL CONTENIDO DE HUMEDAD')
    canvas.line(500, 490, 500, 250)  # vertical2 MEDIO
    canvas.line(450, 490, 450, 250)  # vertical2 MEDIO
    canvas.line(400, 490, 400, 220)  # vertical2 MEDIO
    canvas.drawString(80, 465, 'Numero de muestra')
    canvas.drawString(420, 465, '1')
    canvas.drawString(470, 465, '2')
    canvas.drawString(520, 465, '3')
    canvas.line(60, 460, 550, 460)  ## horizontal abajo9
    canvas.drawString(80, 435, 'Numero de contenedor')
    canvas.drawString(410, 435, humedad['datos_muestra_laboratorio'][0])
    canvas.drawString(460, 435, humedad['datos_muestra_laboratorio'][1])
    canvas.drawString(510, 435, humedad['datos_muestra_laboratorio'][2])
    canvas.line(60, 430, 550, 430)  ## horizontal abajo9
    canvas.drawString(80, 405, 'Masa de contenedor (g) Mc')
    canvas.drawString(410, 405, humedad['datos_muestra_laboratorio'][3])
    canvas.drawString(460, 405, humedad['datos_muestra_laboratorio'][6])
    canvas.drawString(510, 405, humedad['datos_muestra_laboratorio'][9])
    canvas.line(60, 400, 550, 400)  ## horizontal abajo9
    canvas.drawString(80, 375, 'Masa de contenedor + muestra húmeda (g) M1')
    canvas.drawString(410, 375, humedad['datos_muestra_laboratorio'][4])
    canvas.drawString(460, 375, humedad['datos_muestra_laboratorio'][7])
    canvas.drawString(510, 375, humedad['datos_muestra_laboratorio'][10])
    canvas.line(60, 370, 550, 370)  ## horizontal abajo9
    canvas.drawString(80, 345, 'Masa de contenedor + muestra seca (g) M2')
    canvas.drawString(410, 345, humedad['datos_muestra_laboratorio'][5])
    canvas.drawString(460, 345, humedad['datos_muestra_laboratorio'][8])
    canvas.drawString(510, 345, humedad['datos_muestra_laboratorio'][11])
    canvas.line(60, 340, 550, 340)  ## horizontal abajo9
    canvas.drawString(80, 315, 'Masa de agua Mw = M1 - M2 (g)')
    canvas.drawString(410, 315, str(humedad['resultados_del_ensayo'][4]))
    canvas.drawString(460, 315, str(humedad['resultados_del_ensayo'][5]))
    canvas.drawString(510, 315, str(humedad['resultados_del_ensayo'][6]))
    canvas.line(60, 310, 550, 310)  ## horizontal abajo9
    canvas.drawString(80, 285, 'Masa de solidos Ms = M2 - Mc (g)')
    canvas.drawString(410, 285, str(humedad['resultados_del_ensayo'][7]))
    canvas.drawString(460, 285, str(humedad['resultados_del_ensayo'][8]))
    canvas.drawString(510, 285, str(humedad['resultados_del_ensayo'][9]))
    canvas.line(60, 280, 550, 280)  ## horizontal abajo9
    canvas.drawString(80, 255, 'Contenido de Humedad w (%) = (Mw/Ms)*100')
    canvas.drawString(410, 255, str(humedad['resultados_del_ensayo'][0]))
    canvas.drawString(460, 255, str(humedad['resultados_del_ensayo'][1]))
    canvas.drawString(510, 255, str(humedad['resultados_del_ensayo'][2]))
    canvas.line(60, 250, 550, 250)  ## horizontal abajo9
    canvas.drawString(460, 225, str(humedad['resultados_del_ensayo'][3]))
    canvas.line(400, 220, 550, 220)  ## horizontal abajo9

    # observaciones
    canvas.drawString(80, 195, 'D. OBSERVACIONES')
    canvas.line(60, 170, 550, 170)  ## horizontal abajo9
    linea7 = 480
    # FIRMAS
    canvas.drawString(70, 95, 'Firma del jefe de carrera')
    canvas.drawString(420, 95, 'Firma del tecnico')
    canvas.line(puntoAx, puntoY - linea7 - 110, puntoMedio - 90, puntoY - linea7 - 110)
    canvas.line(puntoMedio + 80, puntoY - linea7 - 110, puntoBx, puntoY - linea7 - 110)

    # DATOS ACREDITACION
    linea8y = 70
    canvas.drawString(90, linea8y - 10, 'ELABORADO POR')
    canvas.drawString(260, linea8y - 10, 'REVISADO POR')
    canvas.drawString(420, linea8y - 10, 'APROBADO POR')

    canvas.line(puntoAx, linea8y, puntoBx, linea8y)
    linea8y = linea8y - 15
    canvas.line(puntoAx, linea8y, puntoBx, linea8y)
    linea8y = linea8y - 25
    canvas.line(puntoAx, linea8y, puntoBx, linea8y)
    canvas.line(puntoAx, linea8y + 40, puntoAx, linea8y)  # vertical
    canvas.line(puntoBx, linea8y + 40, puntoBx, linea8y)  # vertical
    canvas.line(puntoMedio - 90, linea8y + 40, puntoMedio - 90, linea8y)  # vertical
    canvas.line(puntoMedio + 90, linea8y + 40, puntoMedio + 90, linea8y)  # vertical

    # FIN COPIAR
    canvas.save()
    pdf_out = output.getvalue()
    output.close()
    filename = 'contenido_humedad.pdf'
    response = make_response(pdf_out)
    response.headers['Content-Disposition'] = "attachment; filename"
    response.mimetype = 'application/pdf'
    # send_file(filename, as_attachment=False)
    # os.remove('contenido_humedad.pdf')
    return send_file(filename, as_attachment=False)

################################### RPLIMITES_ASTM ###################################################################

def reporte_limite_consistencia_astm(datos_limite_astm):
    datos = datos_limite_astm[1]
    output = cStringIO.StringIO()
    canvas = Canvas("limites_consistencia_astm.pdf", pagesize=letter)
    canvas.setLineWidth(.3)
    canvas.setFont('Helvetica', 10)

    canvas.line(60, 760, 550, 760)  # punto x1, y1 , x2, y2 #HORIZONTAL
    canvas.line(60, 760, 60, 700)  # VERTICAL
    canvas.line(60, 700, 550, 700)  # HORIZONTAL
    canvas.line(550, 760, 550, 700)  # VERTICAL
    canvas.line(190, 760, 190, 700)  # VERTICAL
    canvas.line(400, 760, 400, 700)  # VERTICAL
    # CAJETIN PEQUENO
    canvas.line(400, 745, 550, 745)  # HORIZONTAL
    canvas.line(400, 730, 550, 730)  # HORIZONTAL
    canvas.line(400, 715, 550, 715)  # HORIZONTAL
    canvas.line(470, 760, 470, 715)  # VERTICAL
    canvas.drawImage("static/img/emi.jpeg", 70, 710, width=115, height=40)

    # TITULO
    frame1 = Frame(190, 700, 210, 60, showBoundary=1)  # Frame(movX,movY,margenAncho,mrgenAlto)
    bodyStyle = ParagraphStyle('normal', fontSize=24, leading=28, spaceBefore=30, alignment=TA_CENTER)
    s = datos_limite_astm[0]
    story = [Paragraph(s, bodyStyle)]
    story_inframe = KeepInFrame(210, 1 * inch, story)
    frame1.addFromList([story_inframe], canvas)
    # interlineado=740
    story = []
    # DATOS
    posx = 410
    canvas.setFont('Helvetica', 10)
    canvas.drawString(posx, 750, 'Codigo:')
    canvas.drawString(posx, 735, 'Aprobacion:')
    canvas.drawString(posx, 720, 'Version:')
    canvas.drawString(posx + 70, 750, 'C5117-9')
    canvas.drawString(posx + 70, 735, 'Aprobado')
    canvas.drawString(posx + 70, 720, 'Version 1.1')
    canvas.drawString(posx + 30, 703, 'Página 1 de 1')

    # SEGUNDA CAJETILLA
    puntoAx = 60
    puntoBx = 550
    puntoY = 698
    puntoMedio = (puntoAx + puntoBx) / 2

    canvas.line(60, 695, 550,
                695)  # horizontal arriba (largohacialaIZQUIERDA ,arribaIZQ , largo de la linea hacia la derecha ,arribaDER)
    canvas.setFont('Helvetica', 10)
    canvas.drawString(235, 680, 'A. DATOS GENRALES')  # (# ,  arriba , #)
    canvas.line(60, 700, 60,
                489)  # vertical iquierdo  (mover linea hacia derecha punto arriba, linea hacia arriba, mover linea hacia derecha punto abajo)
    canvas.line(550, 700, 550, 489)  # vertical DERECHO
    canvas.line(60, 678, 550, 678)  ## horizontal abajo
    # primero
    canvas.setFont('Helvetica', 9)
    canvas.drawString(160, 670, 'Proyecto')
    canvas.drawString(400, 670, 'Fecha')
    canvas.line(60, 668, 550, 668)  ## horizontal abajo2
    canvas.line(300, 678, 300, 607)  # vertical2 MEDIO
    canvas.setFont('Helvetica', 12)
    canvas.drawString(70, 657, datos['datos_generales'][0])
    canvas.drawString(310, 657, datos['datos_generales'][7])
    canvas.line(60, 655, 550, 655)  ## horizontal abajo3
    # segundo
    canvas.setFont('Helvetica', 9)
    canvas.drawString(160, 647, 'Ubicacion')
    canvas.drawString(400, 647, 'Laboratista')
    canvas.line(60, 645, 550, 645)  ## horizontal abajo4
    canvas.setFont('Helvetica', 12)
    canvas.drawString(70, 634, datos['datos_generales'][1])
    canvas.drawString(310, 634, datos['datos_generales'][4])
    canvas.line(60, 631, 550, 631)  ## horizontal abajo5

    # tercero
    canvas.setFont('Helvetica', 9)
    canvas.drawString(120, 623, 'Descripcion De La Muestra')
    canvas.drawString(380, 623, 'Tipo De Muestra')
    canvas.line(60, 620, 550, 620)  ## horizontal abajo6
    canvas.setFont('Helvetica', 12)
    canvas.drawString(70, 609, datos['datos_generales'][2])
    canvas.drawString(310, 609, datos['datos_generales'][3])
    canvas.line(60, 607, 550, 607)  ## horizontal abajo7

    # datos de calculo
    canvas.setFont('Helvetica', 10)
    canvas.drawString(200, 596, 'B. DETERMINACION DEL LIMITE LIQUIDO')
    canvas.line(60, 594, 550, 594)  ## horizontal
    canvas.line(500, 488.8, 500, 594)  # vertical MEDIO
    canvas.line(450, 488.8, 450, 594)  # vertical MEDIO
    canvas.line(400, 488.8, 400, 594)  # vertical MEDIO
    canvas.drawString(65, 583, 'Numero de contenedor')
    canvas.drawString(415.5, 583, datos['datos_muestra_laboratorio'][0][0])
    canvas.drawString(463.5, 583, datos['datos_muestra_laboratorio'][0][1])
    canvas.drawString(511.5, 583, datos['datos_muestra_laboratorio'][0][2])
    canvas.line(60, 580, 550, 580)  ## horizontal
    canvas.drawString(65, 570, 'Masa recipiente (g) Mr')
    canvas.drawString(415.5, 570, datos['datos_muestra_laboratorio'][1][0][0])
    canvas.drawString(463.5, 570, datos['datos_muestra_laboratorio'][1][1][0])
    canvas.drawString(511.5, 570, datos['datos_muestra_laboratorio'][1][2][0])
    canvas.line(60, 567, 550, 567)  ## horizontal
    canvas.drawString(65, 557, 'Numero de golpes N')
    canvas.drawString(420, 557, datos['datos_muestra_laboratorio'][1][0][1])
    canvas.drawString(469, 557, datos['datos_muestra_laboratorio'][1][1][1])
    canvas.drawString(519, 557, datos['datos_muestra_laboratorio'][1][2][1])
    canvas.line(60, 554, 550, 554)  ## horizontal
    canvas.drawString(65, 544, 'Masa del reciente + suelo humedo (g) Mw+r')
    canvas.drawString(415.5, 544, datos['datos_muestra_laboratorio'][1][0][2])
    canvas.drawString(463.5, 544, datos['datos_muestra_laboratorio'][1][1][2])
    canvas.drawString(511.5, 544, datos['datos_muestra_laboratorio'][1][2][2])
    canvas.line(60, 541, 550, 541)  ## horizontal
    canvas.drawString(65, 531, 'Masa del reciente + suelo seco (g) Md+r')
    canvas.drawString(415.5, 531, datos['datos_muestra_laboratorio'][1][0][3])
    canvas.drawString(463.5, 531, datos['datos_muestra_laboratorio'][1][1][3])
    canvas.drawString(511.5, 531, datos['datos_muestra_laboratorio'][1][2][3])
    canvas.line(60, 528, 550, 528)  ## horizontal
    canvas.drawString(65, 518, 'Masa del agua (g) Mw')
    canvas.drawString(415.5, 518, str(datos['resultados_del_ensayo'][0][2][0]))
    canvas.drawString(463.5, 518, str(datos['resultados_del_ensayo'][0][2][1]))
    canvas.drawString(511.5, 518, str(datos['resultados_del_ensayo'][0][2][2]))
    canvas.line(60, 515, 550, 515)  ## horizontal
    canvas.drawString(65, 505, 'Masa de suelo seco (g) Md')
    canvas.drawString(415.5, 505, str(datos['resultados_del_ensayo'][0][3][0]))
    canvas.drawString(463.5, 505, str(datos['resultados_del_ensayo'][0][3][1]))
    canvas.drawString(511.5, 505, str(datos['resultados_del_ensayo'][0][3][2]))
    canvas.line(60, 502, 550, 502)  ## horizontal
    canvas.drawString(65, 492, 'Contenido de humedad w (%)')
    canvas.drawString(415.5, 492, str(datos['resultados_del_ensayo'][0][0][0]))
    canvas.drawString(463.5, 492, str(datos['resultados_del_ensayo'][0][0][1]))
    canvas.drawString(511.5, 492, str(datos['resultados_del_ensayo'][0][0][2]))
    canvas.line(60, 489, 550, 489)  ## horizontal

    # LL - Lp - IP
    canvas.line(350, 430, 550, 430)  ## horizontal
    canvas.line(350, 417, 550, 417)  ## horizontal
    canvas.line(350, 404, 550, 404)  ## horizontal
    canvas.line(350, 391, 550, 391)  ## horizontal
    canvas.line(350, 430, 350, 390)  # vertical IZQ
    canvas.line(490, 430, 490, 390)  # vertical MEDIO
    canvas.line(550, 430, 550, 390)  # vertical DER
    canvas.drawString(352, 420, 'Limite Liquido')
    canvas.drawString(505, 420, str(datos['resultados_del_ensayo'][0][4][0][0]))
    canvas.drawString(352, 407, 'Limite Plastico')
    canvas.drawString(505, 407, str(datos['resultados_del_ensayo'][1][3]))
    canvas.drawString(352, 394, 'Indice de Plasticidad')
    canvas.drawString(505, 394, str(datos['resultados_del_ensayo'][2]))
    # imagen ensayo
    canvas.drawImage("static/" + datos['direccion_de_grafico'], 100, 328, width=200,
                     height=160)  # izquierda, abajo

    canvas.line(60, 299, 550, 299)  ## horizontal abajo9
    canvas.line(60, 286, 550, 286)  ## horizontal abajo9
    canvas.line(60, 273, 550, 273)  ## horizontal abajo9
    canvas.line(60, 260, 550, 260)  ## horizontal abajo9
    canvas.line(60, 247, 550, 247)  ## horizontal abajo9
    canvas.line(60, 234, 550, 234)  ## horizontal abajo9
    canvas.line(60, 221, 550, 221)  ## horizontal abajo9
    canvas.line(60, 208, 550, 208)  ## horizontal abajo9
    canvas.line(60, 195, 550, 195)  ## horizontal abajo9
    canvas.line(60, 195, 60,
                299)  # vertical iquierdo  (mover linea hacia derecha punto arriba, linea hacia arriba, mover linea hacia derecha punto abajo)
    canvas.line(500, 195, 500, 286)  # vertical Medio
    canvas.line(450, 195, 450, 286)  # vertical Medio
    canvas.line(400, 195, 400, 286)  # vertical Medio
    canvas.line(550, 195, 550, 299)  # vertical dercho
    canvas.setFont('Helvetica', 10)
    canvas.drawString(190, 289, 'C. DETERMINACION DEL LIMITE PLASTICO')
    canvas.drawString(65, 276, 'Numero de contenedor')
    canvas.drawString(415.5, 276, datos['datos_muestra_laboratorio'][0][3])
    canvas.drawString(463.5, 276, datos['datos_muestra_laboratorio'][0][4])
    canvas.drawString(511.5, 276, datos['datos_muestra_laboratorio'][0][5])
    # -----------------------------------------------------------------------
    canvas.drawString(65, 263, 'Masa recipiente (g) Mr')
    canvas.drawString(414, 263, datos['datos_muestra_laboratorio'][2][0][0])
    canvas.drawString(462, 263, datos['datos_muestra_laboratorio'][2][1][0])
    canvas.drawString(510, 263, datos['datos_muestra_laboratorio'][2][2][0])
    # ----------------------------------------------------------------------
    canvas.drawString(65, 250, 'Masa del contenedor + suelo humedo (g) Mw+r')
    canvas.drawString(414, 250, datos['datos_muestra_laboratorio'][2][0][1])
    canvas.drawString(462, 250, datos['datos_muestra_laboratorio'][2][1][1])
    canvas.drawString(510, 250, datos['datos_muestra_laboratorio'][2][2][1])
    # -----------------------------------------------------------------------
    canvas.drawString(65, 237, 'Masa del contenedor + suelo seco (g) Md+r')
    canvas.drawString(414, 237, datos['datos_muestra_laboratorio'][2][0][2])
    canvas.drawString(462, 237, datos['datos_muestra_laboratorio'][2][1][2])
    canvas.drawString(510, 237, datos['datos_muestra_laboratorio'][2][2][2])
    # -----------------------------------------------------------------------
    canvas.drawString(65, 224, 'Masa del agua (g) Mw')
    canvas.drawString(414, 224, str(datos['resultados_del_ensayo'][1][1][0]))
    canvas.drawString(462, 224, str(datos['resultados_del_ensayo'][1][1][1]))
    canvas.drawString(510, 224, str(datos['resultados_del_ensayo'][1][1][2]))
    # ----------------------------------------------------------------------
    canvas.drawString(65, 211, 'Masa del suelo seco (g) Md')
    canvas.drawString(414, 211, str(datos['resultados_del_ensayo'][1][2][0]))
    canvas.drawString(462, 211, str(datos['resultados_del_ensayo'][1][2][1]))
    canvas.drawString(510, 211, str(datos['resultados_del_ensayo'][1][2][2]))
    # ------------------------------------------------------------------------
    canvas.drawString(65, 198, 'Contenido de humedad w (%)')
    canvas.drawString(414, 198, str(datos['resultados_del_ensayo'][1][0][0]))
    canvas.drawString(462, 198, str(datos['resultados_del_ensayo'][1][0][1]))
    canvas.drawString(510, 198, str(datos['resultados_del_ensayo'][1][0][2]))

    # observaciones
    canvas.drawString(80, 150, 'D. OBSERVACIONES')
    canvas.line(60, 140, 550, 140)  ## horizontal abajo9
    linea7 = 480
    # FIRMAS
    canvas.drawString(70, 95, 'Firma del jefe de carrera')
    canvas.drawString(420, 95, 'Firma del tecnico')
    canvas.line(puntoAx, puntoY - linea7 - 110, puntoMedio - 90, puntoY - linea7 - 110)
    canvas.line(puntoMedio + 80, puntoY - linea7 - 110, puntoBx, puntoY - linea7 - 110)

    # DATOS ACREDITACION
    linea8y = 70
    canvas.drawString(90, linea8y - 10, 'ELABORADO POR')
    canvas.drawString(260, linea8y - 10, 'REVISADO POR')
    canvas.drawString(420, linea8y - 10, 'APROBADO POR')

    canvas.line(puntoAx, linea8y, puntoBx, linea8y)
    linea8y = linea8y - 15
    canvas.line(puntoAx, linea8y, puntoBx, linea8y)
    linea8y = linea8y - 25
    canvas.line(puntoAx, linea8y, puntoBx, linea8y)
    canvas.line(puntoAx, linea8y + 40, puntoAx, linea8y)  # vertical
    canvas.line(puntoBx, linea8y + 40, puntoBx, linea8y)  # vertical
    canvas.line(puntoMedio - 90, linea8y + 40, puntoMedio - 90, linea8y)  # vertical
    canvas.line(puntoMedio + 90, linea8y + 40, puntoMedio + 90, linea8y)  # vertical
    # FIN COPIAR
    canvas.save()
    pdf_out = output.getvalue()
    output.close()
    filename = 'limites_consistencia_astm.pdf'
    response = make_response(pdf_out)
    response.headers['Content-Disposition'] = "attachment; filename"
    response.mimetype = 'application/pdf'
    # send_file(filename, as_attachment=False)
    # os.remove('contenido_humedad.pdf')
    return send_file(filename, as_attachment=False)

############################################# RPGRANULOMETRIAASTM #####################################################

def reporte_granulometria_astm2(datosgranulometriaastm):
    datos=datosgranulometriaastm[1]
    output = cStringIO.StringIO()
    canvas = Canvas("granulometriaastm.pdf", pagesize=letter)  # granulometria nombre del pdf
    canvas.setLineWidth(.3)
    canvas.setFont('Helvetica', 10)

    canvas.line(60, 760, 550, 760)  # punto x1, y1 , x2, y2 #HORIZONTAL
    canvas.line(60, 760, 60, 700)  # VERTICAL
    canvas.line(60, 700, 550, 700)  # HORIZONTAL
    canvas.line(550, 760, 550, 700)  # VERTICAL
    canvas.line(190, 760, 190, 700)  # VERTICAL
    canvas.line(400, 760, 400, 700)  # VERTICAL
    # CAJETIN PEQUENO
    canvas.line(400, 745, 550, 745)  # HORIZONTAL
    canvas.line(400, 730, 550, 730)  # HORIZONTAL
    canvas.line(400, 715, 550, 715)  # HORIZONTAL
    canvas.line(470, 760, 470, 715)  # VERTICAL
    canvas.drawImage("static/img/emi.jpeg", 70, 710, width=115, height=40)

    # TITULO
    frame1 = Frame(190, 700, 210, 60, showBoundary=1)  # Frame(movX,movY,margenAncho,mrgenAlto)
    bodyStyle = ParagraphStyle('normal', fontSize=24, leading=28, spaceBefore=30, alignment=TA_CENTER)
    s = datosgranulometriaastm[0]
    story = [Paragraph(s, bodyStyle)]
    story_inframe = KeepInFrame(210, 1 * inch, story)
    frame1.addFromList([story_inframe], canvas)
    # interlineado=740
    story = []
    # DATOS
    posx = 410
    canvas.setFont('Helvetica', 10)
    canvas.drawString(posx, 750, 'Codigo:')
    canvas.drawString(posx, 735, 'Aprobacion:')
    canvas.drawString(posx, 720, 'Version:')
    canvas.drawString(posx + 70, 750, 'C5102-0')
    canvas.drawString(posx + 70, 735, 'Aprobado')
    canvas.drawString(posx + 70, 720, 'Version 1.1')
    canvas.drawString(posx + 30, 703, 'Página 1 de 1')

    # SEGUNDA CAJETILLA
    puntoAx = 60
    puntoBx = 550
    puntoY = 698
    puntoMedio = (puntoAx + puntoBx) / 2

    canvas.line(60, 695, 550,
                695)  # horizontal arriba (largohacialaIZQUIERDA ,arribaIZQ , largo de la linea hacia la derecha ,arribaDER)
    canvas.setFont('Helvetica', 10)
    canvas.drawString(235, 680, 'A. DATOS GENRALES')  # (# ,  arriba , #)
    canvas.line(60, 700, 60,
                502)  # vertical iquierdo  (mover linea hacia derecha punto arriba, linea hacia arriba, mover linea hacia derecha punto abajo)
    canvas.line(550, 700, 550, 502)  # vertical DERECHO
    canvas.line(60, 678, 550, 678)  ## horizontal abajo
    # primero
    canvas.setFont('Helvetica', 9)
    canvas.drawString(160, 670, 'Proyecto')
    canvas.drawString(400, 670, 'Fecha')
    canvas.line(60, 668, 550, 668)  ## horizontal abajo2
    canvas.line(300, 678, 300, 607)  # vertical2 MEDIO
    canvas.setFont('Helvetica', 12)
    canvas.drawString(70, 657, datos['datos_generales'][0])
    canvas.drawString(310, 657, datos['datos_generales'][7])
    canvas.line(60, 655, 550, 655)  ## horizontal abajo3
    # segundo
    canvas.setFont('Helvetica', 9)
    canvas.drawString(160, 647, 'Ubicacion')
    canvas.drawString(400, 647, 'Laboratista')
    canvas.line(60, 645, 550, 645)  ## horizontal abajo4
    canvas.setFont('Helvetica', 12)
    canvas.drawString(70, 634, datos['datos_generales'][1])
    canvas.drawString(310, 634, datos['datos_generales'][4])
    canvas.line(60, 631, 550, 631)  ## horizontal abajo5

    # tercero
    canvas.setFont('Helvetica', 9)
    canvas.drawString(120, 623, 'Descripcion De La Muestra')
    canvas.drawString(380, 623, 'Tipo De Muestra')
    canvas.line(60, 620, 550, 620)  ## horizontal abajo6
    canvas.setFont('Helvetica', 12)
    canvas.drawString(70, 609, datos['datos_generales'][2])
    canvas.drawString(310, 609, datos['datos_generales'][3])
    canvas.line(60, 607, 550, 607)  ## horizontal abajo7

    # datos de calculo
    canvas.setFont('Helvetica', 10)
    canvas.drawString(200, 596, 'B. CALCULO ANALISIS GRANULOMETRICO')
    canvas.line(60, 594, 550, 594)  ## horizontal
    canvas.line(480, 502, 480, 594)  # vertical MEDIO
    canvas.drawString(65, 583, 'Masa recipiente (g) Mr1')
    canvas.drawString(500, 583, datos['datos_muestra_laboratorio'][0])
    canvas.line(60, 580, 550, 580)  ## horizontal
    canvas.drawString(65, 570, 'Masa de la muestra seca + reciente (g) Ms + reciente(1)')
    canvas.drawString(500, 570, datos['datos_muestra_laboratorio'][2])
    canvas.line(60, 567, 550, 567)  ## horizontal
    canvas.drawString(65, 557, 'Masa de la muestra seca(g) Ms')
    canvas.drawString(500, 557, str(datos['resultados_del_ensayo'][0][0]))
    canvas.line(60, 554, 550, 554)  ## horizontal
    canvas.drawString(65, 544, 'Masa del reciente(g) Mr2')
    canvas.drawString(500, 544, datos['datos_muestra_laboratorio'][1])
    canvas.line(60, 541, 550, 541)  ## horizontal
    canvas.drawString(65, 531, 'Masa seca del material grueso + recipiente(g) M grueso + recipiente(2)')
    canvas.drawString(500, 531, datos['datos_muestra_laboratorio'][3])
    canvas.line(60, 528, 550, 528)  ## horizontal
    canvas.drawString(65, 518, 'Masa seca del material grueso(g) M grueso')
    canvas.drawString(500, 518, str(datos['resultados_del_ensayo'][0][1]))
    canvas.line(60, 515, 550, 515)  ## horizontal
    canvas.drawString(65, 505, 'Masa seca del material fino')
    canvas.drawString(500, 505, str(datos['resultados_del_ensayo'][0][2]))
    canvas.line(60, 502, 550, 502)  ## horizontal

    # tabla calculos

    for i in range(16):
        canvas.line(60, 480 - i * 13, 370, 480 - i * 13)  ## horizontal

    canvas.line(60, 480, 60,
                285)  # vertical iquierdo  (mover linea hacia derecha punto arriba, linea hacia arriba, mover linea hacia derecha punto abajo)
    canvas.line(370, 480, 370, 285)  # vertical dercho
    canvas.setFont('Helvetica', 8)
    canvas.drawString(65, 470, 'Tamiz Nº')
    canvas.drawString(75, 457, datos['resultados_del_ensayo'][1][0])
    canvas.drawString(75, 444, datos['resultados_del_ensayo'][1][1])
    canvas.drawString(75, 431, datos['resultados_del_ensayo'][1][2])
    canvas.drawString(72, 418, datos['resultados_del_ensayo'][1][3])
    canvas.drawString(72, 405, datos['resultados_del_ensayo'][1][4])
    canvas.drawString(72, 392, datos['resultados_del_ensayo'][1][5])
    canvas.drawString(72, 379, datos['resultados_del_ensayo'][1][6])
    canvas.drawString(72, 366, datos['resultados_del_ensayo'][1][7])
    canvas.drawString(70, 353, datos['resultados_del_ensayo'][1][8])
    canvas.drawString(70, 340, datos['resultados_del_ensayo'][1][9])
    canvas.drawString(70, 327, datos['resultados_del_ensayo'][1][10])
    canvas.drawString(70, 314, datos['resultados_del_ensayo'][1][11])
    canvas.drawString(70, 301, datos['resultados_del_ensayo'][1][12])
    canvas.drawString(66, 288, datos['resultados_del_ensayo'][1][13])
    canvas.line(100, 480, 100, 285)
    canvas.drawString(101, 470, 'Diametro(mm)')
    canvas.drawString(115, 457, str(datos['resultados_del_ensayo'][2][0]))
    canvas.drawString(115, 444, str(datos['resultados_del_ensayo'][2][1]))
    canvas.drawString(115, 431, str(datos['resultados_del_ensayo'][2][2]))
    canvas.drawString(115, 418, str(datos['resultados_del_ensayo'][2][3]))
    canvas.drawString(115, 405, str(datos['resultados_del_ensayo'][2][4]))
    canvas.drawString(115, 392, str(datos['resultados_del_ensayo'][2][5]))
    canvas.drawString(115, 379, str(datos['resultados_del_ensayo'][2][6]))
    canvas.drawString(115, 366, str(datos['resultados_del_ensayo'][2][7]))
    canvas.drawString(115, 353, str(datos['resultados_del_ensayo'][2][8]))
    canvas.drawString(115, 340, str(datos['resultados_del_ensayo'][2][9]))
    canvas.drawString(115, 327, str(datos['resultados_del_ensayo'][2][10]))
    canvas.drawString(115, 314, str(datos['resultados_del_ensayo'][2][11]))
    canvas.drawString(115, 301, str(datos['resultados_del_ensayo'][2][12]))
    canvas.drawString(115, 288, str(datos['resultados_del_ensayo'][2][13]))
    canvas.line(152.5, 480, 152.5, 272)

    canvas.drawString(154, 470, 'Masa ret(g)')
    canvas.drawString(160, 457, str(datos['resultados_del_ensayo'][3][0]))
    canvas.drawString(160, 444, str(datos['resultados_del_ensayo'][3][1]))
    canvas.drawString(160, 431, str(datos['resultados_del_ensayo'][3][2]))
    canvas.drawString(160, 418, str(datos['resultados_del_ensayo'][3][3]))
    canvas.drawString(160, 405, str(datos['resultados_del_ensayo'][3][4]))
    canvas.drawString(160, 392, str(datos['resultados_del_ensayo'][3][5]))
    canvas.drawString(160, 379, str(datos['resultados_del_ensayo'][3][6]))
    canvas.drawString(160, 366, str(datos['resultados_del_ensayo'][3][7]))
    canvas.drawString(160, 353, str(datos['resultados_del_ensayo'][3][8]))
    canvas.drawString(160, 340, str(datos['resultados_del_ensayo'][3][9]))
    canvas.drawString(160, 327, str(datos['resultados_del_ensayo'][3][10]))
    canvas.drawString(160, 314, str(datos['resultados_del_ensayo'][3][11]))
    canvas.drawString(160, 301, str(datos['resultados_del_ensayo'][3][12]))
    canvas.drawString(160, 288, str(datos['resultados_del_ensayo'][3][13]))
    canvas.drawString(160, 275, str(datos['resultados_del_ensayo'][3][14]))
    canvas.line(196, 480, 196, 272)  # vetical
    canvas.line(152.5, 272, 196, 272)  # linea de abajo de la ultima celda

    canvas.drawString(197, 470, 'Masa ret-acumulada(g)')
    canvas.drawString(220, 457, str(datos['resultados_del_ensayo'][4][0]))
    canvas.drawString(220, 444, str(datos['resultados_del_ensayo'][4][1]))
    canvas.drawString(220, 431, str(datos['resultados_del_ensayo'][4][2]))
    canvas.drawString(220, 418, str(datos['resultados_del_ensayo'][4][3]))
    canvas.drawString(220, 405, str(datos['resultados_del_ensayo'][4][4]))
    canvas.drawString(220, 392, str(datos['resultados_del_ensayo'][4][5]))
    canvas.drawString(220, 379, str(datos['resultados_del_ensayo'][4][6]))
    canvas.drawString(220, 366, str(datos['resultados_del_ensayo'][4][7]))
    canvas.drawString(220, 353, str(datos['resultados_del_ensayo'][4][8]))
    canvas.drawString(220, 340, str(datos['resultados_del_ensayo'][4][9]))
    canvas.drawString(220, 327, str(datos['resultados_del_ensayo'][4][10]))
    canvas.drawString(220, 314, str(datos['resultados_del_ensayo'][4][11]))
    canvas.drawString(220, 301, str(datos['resultados_del_ensayo'][4][12]))
    canvas.drawString(220, 288, str(datos['resultados_del_ensayo'][4][13]))
    canvas.line(280, 480, 280, 285)

    canvas.drawString(281, 470, '% Retenido')
    canvas.drawString(290, 457, str(datos['resultados_del_ensayo'][5][0]))
    canvas.drawString(290, 444, str(datos['resultados_del_ensayo'][5][1]))
    canvas.drawString(290, 431, str(datos['resultados_del_ensayo'][5][2]))
    canvas.drawString(290, 418, str(datos['resultados_del_ensayo'][5][3]))
    canvas.drawString(290, 405, str(datos['resultados_del_ensayo'][5][4]))
    canvas.drawString(290, 392, str(datos['resultados_del_ensayo'][5][5]))
    canvas.drawString(290, 379, str(datos['resultados_del_ensayo'][5][6]))
    canvas.drawString(290, 366, str(datos['resultados_del_ensayo'][5][7]))
    canvas.drawString(290, 353, str(datos['resultados_del_ensayo'][5][8]))
    canvas.drawString(290, 340, str(datos['resultados_del_ensayo'][5][9]))
    canvas.drawString(290, 327, str(datos['resultados_del_ensayo'][5][10]))
    canvas.drawString(290, 314, str(datos['resultados_del_ensayo'][5][11]))
    canvas.drawString(290, 301, str(datos['resultados_del_ensayo'][5][12]))
    canvas.drawString(290, 288, str(datos['resultados_del_ensayo'][5][13]))
    canvas.line(324, 480, 324, 285)

    canvas.drawString(325, 470, '% Que pasa')
    canvas.drawString(335, 457, str(datos['resultados_del_ensayo'][6][0]))
    canvas.drawString(335, 444, str(datos['resultados_del_ensayo'][6][1]))
    canvas.drawString(335, 431, str(datos['resultados_del_ensayo'][6][2]))
    canvas.drawString(335, 418, str(datos['resultados_del_ensayo'][6][3]))
    canvas.drawString(335, 405, str(datos['resultados_del_ensayo'][6][4]))
    canvas.drawString(335, 392, str(datos['resultados_del_ensayo'][6][5]))
    canvas.drawString(335, 379, str(datos['resultados_del_ensayo'][6][6]))
    canvas.drawString(335, 366, str(datos['resultados_del_ensayo'][6][7]))
    canvas.drawString(335, 353, str(datos['resultados_del_ensayo'][6][8]))
    canvas.drawString(335, 340, str(datos['resultados_del_ensayo'][6][9]))
    canvas.drawString(335, 327, str(datos['resultados_del_ensayo'][6][10]))
    canvas.drawString(335, 314, str(datos['resultados_del_ensayo'][6][11]))
    canvas.drawString(335, 301, str(datos['resultados_del_ensayo'][6][12]))
    canvas.drawString(335, 288, str(datos['resultados_del_ensayo'][6][13]))
    # tabla de cc cu D60


    canvas.line(60, 265, 550, 265)  ## horizontal abajo9
    canvas.line(60, 252, 550, 252)  ## horizontal abajo9
    canvas.line(60, 239, 550, 239)  ## horizontal abajo9
    canvas.line(60, 226, 550, 226)  ## horizontal abajo9
    canvas.line(60, 213, 370, 213)  ## horizontal abajo9
    canvas.line(60, 200, 370, 200)  ## horizontal abajo9
    canvas.drawString(65, 255, 'D60 =')
    canvas.drawString(320, 255, str(datos['resultados_del_ensayo'][7][0]))
    canvas.drawString(65, 242, 'D30 =')
    canvas.drawString(320, 242, str(datos['resultados_del_ensayo'][7][1]))
    canvas.drawString(65, 229, 'D10 =')
    canvas.drawString(320, 229, str(datos['resultados_del_ensayo'][7][2]))
    # ----------------------------------------------------------------------
    canvas.drawString(65, 216, 'Cc (Coeficiente de curvatura)')
    canvas.drawString(320, 216, str(datos['resultados_del_ensayo'][8][0]))
    canvas.drawString(65, 203, 'Cu (Coeficiente de uniformidad)')
    canvas.drawString(320, 203, str(datos['resultados_del_ensayo'][8][1]))

    # ----------------------------------------------------------------------
    canvas.drawString(375, 255, "% Grava =")
    canvas.drawString(500, 255, str(datos['resultados_del_ensayo'][9][0]))
    canvas.drawString(375, 242, "% Arena =")
    canvas.drawString(500, 242, str(datos['resultados_del_ensayo'][9][2]))
    canvas.drawString(375, 229, "% Finos =")
    canvas.drawString(500, 229, str(datos['resultados_del_ensayo'][9][1]))
    canvas.line(60, 200, 60,
                265)  # vertical iquierdo  (mover linea hacia derecha punto arriba, linea hacia arriba, mover linea hacia derecha punto abajo)
    canvas.line(370, 200, 370, 265)  # vertical dercho
    canvas.line(550, 226, 550, 265)  # vertical dercho

    # imagen ensayo
    canvas.drawImage("static/" + datos['direccion_de_grafico'][0], 371, 330, width=200,
                     height=120)  # izquierda, abajo

    # observaciones
    canvas.drawString(80, 150, 'D. OBSERVACIONES')
    canvas.line(60, 140, 550, 140)  ## horizontal abajo9
    linea7 = 480
    # FIRMAS
    canvas.drawString(70, 95, 'Firma del jefe de carrera')
    canvas.drawString(420, 95, 'Firma del tecnico')
    canvas.line(puntoAx, puntoY - linea7 - 110, puntoMedio - 90, puntoY - linea7 - 110)
    canvas.line(puntoMedio + 80, puntoY - linea7 - 110, puntoBx, puntoY - linea7 - 110)

    # DATOS ACREDITACION
    linea8y = 70
    canvas.drawString(90, linea8y - 10, 'ELABORADO POR')
    canvas.drawString(260, linea8y - 10, 'REVISADO POR')
    canvas.drawString(420, linea8y - 10, 'APROBADO POR')

    canvas.line(puntoAx, linea8y, puntoBx, linea8y)
    linea8y = linea8y - 15
    canvas.line(puntoAx, linea8y, puntoBx, linea8y)
    linea8y = linea8y - 25
    canvas.line(puntoAx, linea8y, puntoBx, linea8y)
    canvas.line(puntoAx, linea8y + 40, puntoAx, linea8y)  # vertical
    canvas.line(puntoBx, linea8y + 40, puntoBx, linea8y)  # vertical
    canvas.line(puntoMedio - 90, linea8y + 40, puntoMedio - 90, linea8y)  # vertical
    canvas.line(puntoMedio + 90, linea8y + 40, puntoMedio + 90, linea8y)  # vertical

    # FIN COPIAR

    canvas.save()
    pdf_out = output.getvalue()
    output.close()
    filename = 'granulometriaastm.pdf'
    response = make_response(pdf_out)
    response.headers['Content-Disposition'] = "attachment; filename"
    response.mimetype = 'application/pdf'
    # return response
    return send_file(filename, as_attachment=False)


########################################## RPGRANULOMETRIAAASHTO ##################################################

def reporte_granulometria_aashto_2(datosgranulometriaaashto):
    datos=datosgranulometriaaashto[1]
    output = cStringIO.StringIO()
    canvas = Canvas("granulometriaAASHTO.pdf", pagesize=letter)  # granulometria nombre del pdf
    canvas.setLineWidth(.3)
    canvas.setFont('Helvetica', 10)

    canvas.line(60, 760, 550, 760)  # punto x1, y1 , x2, y2 #HORIZONTAL
    canvas.line(60, 760, 60, 700)  # VERTICAL
    canvas.line(60, 700, 550, 700)  # HORIZONTAL
    canvas.line(550, 760, 550, 700)  # VERTICAL
    canvas.line(190, 760, 190, 700)  # VERTICAL
    canvas.line(400, 760, 400, 700)  # VERTICAL
    # CAJETIN PEQUENO
    canvas.line(400, 745, 550, 745)  # HORIZONTAL
    canvas.line(400, 730, 550, 730)  # HORIZONTAL
    canvas.line(400, 715, 550, 715)  # HORIZONTAL
    canvas.line(470, 760, 470, 715)  # VERTICAL
    canvas.drawImage("static/img/emi.jpeg", 70, 710, width=115, height=40)

    # TITULO
    frame1 = Frame(190, 700, 210, 60, showBoundary=1)  # Frame(movX,movY,margenAncho,mrgenAlto)
    bodyStyle = ParagraphStyle('normal', fontSize=24, leading=28, spaceBefore=30, alignment=TA_CENTER)
    s = datosgranulometriaaashto[0]
    story = [Paragraph(s, bodyStyle)]
    story_inframe = KeepInFrame(210, 1 * inch, story)
    frame1.addFromList([story_inframe], canvas)
    # interlineado=740
    story = []
    # DATOS
    posx = 410
    canvas.setFont('Helvetica', 10)
    canvas.drawString(posx, 750, 'Codigo:')
    canvas.drawString(posx, 735, 'Aprobacion:')
    canvas.drawString(posx, 720, 'Version:')
    canvas.drawString(posx + 70, 750, 'C5102-0')
    canvas.drawString(posx + 70, 735, 'Aprobado')
    canvas.drawString(posx + 70, 720, 'Version 1.1')
    canvas.drawString(posx + 30, 703, 'Página 1 de 1')


    # SEGUNDA CAJETILLA
    puntoAx = 60
    puntoBx = 550
    puntoY = 698
    puntoMedio = (puntoAx + puntoBx) / 2

    canvas.line(60, 695, 550,
                695)  # horizontal arriba (largohacialaIZQUIERDA ,arribaIZQ , largo de la linea hacia la derecha ,arribaDER)
    canvas.setFont('Helvetica', 10)
    canvas.drawString(235, 680, 'A. DATOS GENRALES')  # (# ,  arriba , #)
    canvas.line(60, 700, 60,
                502)  # vertical iquierdo  (mover linea hacia derecha punto arriba, linea hacia arriba, mover linea hacia derecha punto abajo)
    canvas.line(550, 700, 550, 489)  # vertical DERECHO
    canvas.line(60, 678, 550, 678)  ## horizontal abajo
    # primero
    canvas.setFont('Helvetica', 9)
    canvas.drawString(160, 670, 'Proyecto')
    canvas.drawString(400, 670, 'Fecha')
    canvas.line(60, 668, 550, 668)  ## horizontal abajo2
    canvas.line(300, 678, 300, 607)  # vertical2 MEDIO
    canvas.setFont('Helvetica', 12)
    canvas.drawString(70, 657, datos['datos_generales'][0])
    canvas.drawString(310, 657, datos['datos_generales'][7])
    canvas.line(60, 655, 550, 655)  ## horizontal abajo3
    # segundo
    canvas.setFont('Helvetica', 9)
    canvas.drawString(160, 647, 'Ubicacion')
    canvas.drawString(400, 647, 'Laboratista')
    canvas.line(60, 645, 550, 645)  ## horizontal abajo4
    canvas.setFont('Helvetica', 12)
    canvas.drawString(70, 634, datos['datos_generales'][1])
    canvas.drawString(310, 634, datos['datos_generales'][4])
    canvas.line(60, 631, 550, 631)  ## horizontal abajo5

    # tercero
    canvas.setFont('Helvetica', 9)
    canvas.drawString(120, 623, 'Descripcion De La Muestra')
    canvas.drawString(380, 623, 'Tipo De Muestra')
    canvas.line(60, 620, 550, 620)  ## horizontal abajo6
    canvas.setFont('Helvetica', 12)
    canvas.drawString(70, 609, datos['datos_generales'][2])
    canvas.drawString(310, 609, datos['datos_generales'][3])
    canvas.line(60, 607, 550, 607)  ## horizontal abajo7

    # datos de calculo
    canvas.setFont('Helvetica', 10)
    canvas.drawString(240, 596, 'B. DATOS TECNICOS')
    canvas.line(60, 594, 550, 594)  ## horizontal
    canvas.line(300, 489, 300, 594)  # vertical MEDIO
    canvas.line(240, 502, 240, 580)  # vertical MEDIO
    canvas.line(480, 489, 480, 580)  # vertical MEDIO
    canvas.drawString(105, 583, 'HUMEDAD HIGROSCOPICA %Hh')
    canvas.drawString(350, 583, 'MUESTRA TOTAL SECA Pst')

    canvas.line(60, 580, 550, 580)  ## horizontal
    canvas.drawString(65, 570, 'Suelo humedo + capsula P1')
    canvas.drawString(245, 570, datos['datos_muestra_laboratorio'][0][0])
    canvas.line(60, 567, 550, 567)  ## horizontal
    canvas.drawString(65, 557, 'Suelo seco + capsula P2')
    canvas.drawString(245, 557, str(datos['datos_muestra_laboratorio'][0][1]))
    canvas.line(60, 554, 550, 554)  ## horizontal
    canvas.drawString(65, 544, 'Masa del agua Pa')
    canvas.drawString(245, 544, str(datos['resultados_del_ensayo'][0][0]))
    canvas.line(60, 541, 550, 541)  ## horizontal
    canvas.drawString(65, 531, 'Masa de la capsula PC')
    canvas.drawString(245, 531, str(datos['datos_muestra_laboratorio'][0][2]))
    canvas.line(60, 528, 550, 528)  ## horizontal
    canvas.drawString(65, 518, 'Masa del suelo seco Ps')
    canvas.drawString(245, 518, str(datos['resultados_del_ensayo'][0][1]))
    canvas.line(60, 515, 550, 515)  ## horizontal
    canvas.drawString(65, 505, 'Porcentaje humedad %Hh')
    canvas.drawString(245, 505, str(datos['resultados_del_ensayo'][0][2]))
    canvas.line(60, 502, 550, 502)  ## horizontal

    # ------- MUESTRA TOTAL SECA -------------------------
    canvas.drawString(305, 570, 'Muestra total húmeda Pht')
    canvas.drawString(490, 570, datos['datos_muestra_laboratorio'][0][3])
    canvas.drawString(305, 557, 'Agregado grueso (Ret Nro 4)')
    canvas.drawString(490, 557, str(datos['resultados_del_ensayo'][0][3]))
    canvas.drawString(305, 544, 'Pasa Nro 4 humedo Mh')
    canvas.drawString(490, 544, str(datos['resultados_del_ensayo'][0][4]))
    canvas.drawString(305, 531, 'Pasa Nro 4 seco Ms')
    canvas.drawString(490, 531, str(datos['resultados_del_ensayo'][0][5]))
    canvas.drawString(305, 518, 'Muestra total seca Pst')
    canvas.drawString(490, 518, str(datos['resultados_del_ensayo'][0][6]))
    canvas.drawString(305, 505, 'Pasa Nro 4 humedo Sh')
    canvas.drawString(490, 505, str(datos['datos_muestra_laboratorio'][0][4]))
    canvas.line(300, 489, 550, 489)  ## horizontal
    canvas.drawString(305, 492, 'Pasa Nro 4 seco Ss')
    canvas.drawString(490, 492, str(datos['resultados_del_ensayo'][0][7]))

    canvas.line(60, 480, 370, 480)  ## horizontal
    canvas.setFont('Helvetica', 8)
    canvas.drawString(61, 465, 'Tamiz Nº')
    canvas.drawString(103, 465, 'Peso Retenido.(gr)')
    canvas.drawString(184, 471, 'Retenido acumulado')

    canvas.drawString(187, 460, 'grs')
    canvas.drawString(235, 460, '%')
    canvas.drawString(268, 465, 'Tamaño (mm)')
    canvas.drawString(322, 465, '% Que pasa')
    canvas.line(172, 470, 265, 470)  ## horizontal retenido acumulado

    # tabla calculos


    pru = datos['datos_muestra_laboratorio'][1]
    for i in range(len(pru) + 1):
        canvas.line(60, 454 - i * 13, 370, 454 - i * 13)  ## horizontal

    if len(pru) == 4:
        canvas.line(60, 480, 60,
                    402)  # vertical iquierdo  (mover linea hacia derecha punto arriba, linea hacia arriba, mover linea hacia derecha punto abajo)
        canvas.line(100, 480, 100, 402)
        canvas.line(172, 480, 172, 402)
        canvas.line(220, 470, 220, 402)  # vetical retenido acumulado
        canvas.line(265, 480, 265, 402)  # vetical
        canvas.line(320, 480, 320, 402)
        canvas.line(370, 480, 370, 402)  # vertical dercho

    canvas.setFont('Helvetica', 8)

    canvas.drawString(75, 444, datos['datos_muestra_laboratorio'][1][0])
    canvas.drawString(75, 431, datos['datos_muestra_laboratorio'][1][1])
    canvas.drawString(72, 418, datos['datos_muestra_laboratorio'][1][2])
    canvas.drawString(72, 405, datos['datos_muestra_laboratorio'][1][3])
    if len(pru) == 5:
        canvas.line(60, 480, 60,
                    389)  # vertical iquierdo  (mover linea hacia derecha punto arriba, linea hacia arriba, mover linea hacia derecha punto abajo)
        canvas.line(100, 480, 100, 389)
        canvas.line(172, 480, 172, 389)
        canvas.line(220, 470, 220, 389)  # vetical retenido acumulado
        canvas.line(265, 480, 265, 389)  # vetical
        canvas.line(320, 480, 320, 389)
        canvas.line(370, 480, 370, 389)  # vertical dercho
        canvas.drawString(72, 392, datos['datos_muestra_laboratorio'][1][4])
    if len(pru) == 6:
        canvas.line(60, 480, 60,
                    376)  # vertical iquierdo  (mover linea hacia derecha punto arriba, linea hacia arriba, mover linea hacia derecha punto abajo)
        canvas.line(100, 480, 100, 376)
        canvas.line(172, 480, 172, 376)
        canvas.line(220, 470, 220, 376)  # vetical retenido acumulado
        canvas.line(265, 480, 265, 376)  # vetical
        canvas.line(320, 480, 320, 376)
        canvas.line(370, 480, 370, 376)  # vertical dercho
        canvas.drawString(72, 392, datos['datos_muestra_laboratorio'][1][4])
        canvas.drawString(72, 379, datos['datos_muestra_laboratorio'][1][5])
    if len(pru) == 7:
        canvas.line(60, 480, 60,
                    363)  # vertical iquierdo  (mover linea hacia derecha punto arriba, linea hacia arriba, mover linea hacia derecha punto abajo)
        canvas.line(100, 480, 100, 363)
        canvas.line(172, 480, 172, 363)
        canvas.line(220, 470, 220, 363)  # vetical retenido acumulado
        canvas.line(265, 480, 265, 363)  # vetical
        canvas.line(320, 480, 320, 363)
        canvas.line(370, 480, 370, 363)  # vertical dercho
        canvas.drawString(72, 392, datos['datos_muestra_laboratorio'][1][4])
        canvas.drawString(72, 379, datos['datos_muestra_laboratorio'][1][5])
        canvas.drawString(72, 366, datos['datos_muestra_laboratorio'][1][6])
    if len(pru) == 8:
        canvas.line(60, 480, 60,
                    350)  # vertical iquierdo  (mover linea hacia derecha punto arriba, linea hacia arriba, mover linea hacia derecha punto abajo)
        canvas.line(100, 480, 100, 350)
        canvas.line(172, 480, 172, 350)
        canvas.line(220, 470, 220, 350)  # vetical retenido acumulado
        canvas.line(265, 480, 265, 350)  # vetical
        canvas.line(320, 480, 320, 350)
        canvas.line(370, 480, 370, 350)  # vertical dercho
        canvas.drawString(72, 392, datos['datos_muestra_laboratorio'][1][4])
        canvas.drawString(72, 379, datos['datos_muestra_laboratorio'][1][5])
        canvas.drawString(72, 366, datos['datos_muestra_laboratorio'][1][6])
        canvas.drawString(72, 353, datos['datos_muestra_laboratorio'][1][7])
    if len(pru) == 9:
        canvas.line(60, 480, 60,
                    337)  # vertical iquierdo  (mover linea hacia derecha punto arriba, linea hacia arriba, mover linea hacia derecha punto abajo)
        canvas.line(100, 480, 100, 337)
        canvas.line(172, 480, 172, 337)
        canvas.line(220, 470, 220, 337)  # vetical retenido acumulado
        canvas.line(265, 480, 265, 337)  # vetical
        canvas.line(320, 480, 320, 337)
        canvas.line(370, 480, 370, 337)  # vertical dercho
        canvas.drawString(72, 392, datos['datos_muestra_laboratorio'][1][4])
        canvas.drawString(72, 379, datos['datos_muestra_laboratorio'][1][5])
        canvas.drawString(72, 366, datos['datos_muestra_laboratorio'][1][6])
        canvas.drawString(72, 353, datos['datos_muestra_laboratorio'][1][7])
        canvas.drawString(72, 340, datos['datos_muestra_laboratorio'][1][8])

    #########################3canvas.line(100, 480, 100, 285)


    canvas.drawString(110, 444, str(datos['datos_muestra_laboratorio'][2][0]))
    canvas.drawString(110, 431, str(datos['datos_muestra_laboratorio'][2][1]))
    canvas.drawString(110, 418, str(datos['datos_muestra_laboratorio'][2][2]))
    canvas.drawString(110, 405, str(datos['datos_muestra_laboratorio'][2][3]))

    if len(pru) == 5:
        canvas.drawString(110, 392, str(datos['datos_muestra_laboratorio'][2][4]))
    if len(pru) == 6:
        canvas.drawString(110, 392, str(datos['datos_muestra_laboratorio'][2][4]))
        canvas.drawString(110, 379, str(datos['datos_muestra_laboratorio'][2][5]))
    if len(pru) == 7:
        canvas.drawString(110, 392, str(datos['datos_muestra_laboratorio'][2][4]))
        canvas.drawString(110, 379, str(datos['datos_muestra_laboratorio'][2][5]))
        canvas.drawString(110, 366, str(datos['datos_muestra_laboratorio'][2][6]))
    if len(pru) == 8:
        canvas.drawString(110, 392, str(datos['datos_muestra_laboratorio'][2][4]))
        canvas.drawString(110, 379, str(datos['datos_muestra_laboratorio'][2][5]))
        canvas.drawString(110, 366, str(datos['datos_muestra_laboratorio'][2][6]))
        canvas.drawString(110, 353, str(datos['datos_muestra_laboratorio'][2][7]))
    if len(pru) == 9:
        canvas.drawString(110, 392, str(datos['datos_muestra_laboratorio'][2][4]))
        canvas.drawString(110, 379, str(datos['datos_muestra_laboratorio'][2][5]))
        canvas.drawString(110, 366, str(datos['datos_muestra_laboratorio'][2][6]))
        canvas.drawString(110, 353, str(datos['datos_muestra_laboratorio'][2][7]))
        canvas.drawString(110, 340, str(datos['datos_muestra_laboratorio'][2][8]))

    canvas.drawString(175, 444, str(datos['resultados_del_ensayo'][4][0][0]))
    canvas.drawString(175, 431, str(datos['resultados_del_ensayo'][4][0][1]))
    canvas.drawString(175, 418, str(datos['resultados_del_ensayo'][4][0][2]))
    canvas.drawString(175, 405, str(datos['resultados_del_ensayo'][4][0][3]))
    if len(pru) == 5:
        canvas.drawString(175, 392, str(datos['resultados_del_ensayo'][4][0][4]))
    if len(pru) == 6:
        canvas.drawString(175, 392, str(datos['resultados_del_ensayo'][4][0][4]))
        canvas.drawString(175, 379, str(datos['resultados_del_ensayo'][4][0][5]))
    if len(pru) == 7:
        canvas.drawString(175, 392, str(datos['resultados_del_ensayo'][4][0][4]))
        canvas.drawString(175, 379, str(datos['resultados_del_ensayo'][4][0][5]))
        canvas.drawString(175, 366, str(datos['resultados_del_ensayo'][4][0][6]))
    if len(pru) == 8:
        canvas.drawString(175, 392, str(datos['resultados_del_ensayo'][4][0][4]))
        canvas.drawString(175, 379, str(datos['resultados_del_ensayo'][4][0][5]))
        canvas.drawString(175, 366, str(datos['resultados_del_ensayo'][4][0][6]))
        canvas.drawString(175, 353, str(datos['resultados_del_ensayo'][4][0][7]))
    if len(pru) == 9:
        canvas.drawString(175, 392, str(datos['resultados_del_ensayo'][4][0][4]))
        canvas.drawString(175, 379, str(datos['resultados_del_ensayo'][4][0][5]))
        canvas.drawString(175, 366, str(datos['resultados_del_ensayo'][4][0][6]))
        canvas.drawString(175, 353, str(datos['resultados_del_ensayo'][4][0][7]))
        canvas.drawString(175, 340, str(datos['resultados_del_ensayo'][4][0][8]))

    canvas.drawString(225, 444, str(datos['resultados_del_ensayo'][4][1][0]))
    canvas.drawString(225, 431, str(datos['resultados_del_ensayo'][4][1][1]))
    canvas.drawString(225, 418, str(datos['resultados_del_ensayo'][4][1][2]))
    canvas.drawString(225, 405, str(datos['resultados_del_ensayo'][4][1][3]))
    if len(pru) == 5:
        canvas.drawString(225, 392, str(datos['resultados_del_ensayo'][4][1][4]))
    if len(pru) == 6:
        canvas.drawString(225, 392, str(datos['resultados_del_ensayo'][4][1][4]))
        canvas.drawString(225, 379, str(datos['resultados_del_ensayo'][4][1][5]))
    if len(pru) == 7:
        canvas.drawString(225, 392, str(datos['resultados_del_ensayo'][4][1][4]))
        canvas.drawString(225, 379, str(datos['resultados_del_ensayo'][4][1][5]))
        canvas.drawString(225, 366, str(datos['resultados_del_ensayo'][4][1][6]))
    if len(pru) == 8:
        canvas.drawString(225, 392, str(datos['resultados_del_ensayo'][4][1][4]))
        canvas.drawString(225, 379, str(datos['resultados_del_ensayo'][4][1][5]))
        canvas.drawString(225, 366, str(datos['resultados_del_ensayo'][4][1][6]))
        canvas.drawString(225, 353, str(datos['resultados_del_ensayo'][4][1][7]))
    if len(pru) == 9:
        canvas.drawString(225, 392, str(datos['resultados_del_ensayo'][4][1][4]))
        canvas.drawString(225, 379, str(datos['resultados_del_ensayo'][4][1][5]))
        canvas.drawString(225, 366, str(datos['resultados_del_ensayo'][4][1][6]))
        canvas.drawString(225, 353, str(datos['resultados_del_ensayo'][4][1][7]))
        canvas.drawString(225, 340, str(datos['resultados_del_ensayo'][4][1][8]))

    canvas.drawString(275, 444, str(datos['resultados_del_ensayo'][4][2][0]))
    canvas.drawString(275, 431, str(datos['resultados_del_ensayo'][4][2][1]))
    canvas.drawString(275, 418, str(datos['resultados_del_ensayo'][4][2][2]))
    canvas.drawString(275, 405, str(datos['resultados_del_ensayo'][4][2][3]))
    if len(pru) == 5:
        canvas.drawString(275, 392, str(datos['resultados_del_ensayo'][4][2][4]))
    if len(pru) == 6:
        canvas.drawString(275, 392, str(datos['resultados_del_ensayo'][4][2][4]))
        canvas.drawString(275, 379, str(datos['resultados_del_ensayo'][4][2][5]))
    if len(pru) == 7:
        canvas.drawString(275, 392, str(datos['resultados_del_ensayo'][4][2][4]))
        canvas.drawString(275, 379, str(datos['resultados_del_ensayo'][4][2][5]))
        canvas.drawString(275, 366, str(datos['resultados_del_ensayo'][4][2][6]))
    if len(pru) == 8:
        canvas.drawString(275, 392, str(datos['resultados_del_ensayo'][4][2][4]))
        canvas.drawString(275, 379, str(datos['resultados_del_ensayo'][4][2][5]))
        canvas.drawString(275, 366, str(datos['resultados_del_ensayo'][4][2][6]))
        canvas.drawString(275, 353, str(datos['resultados_del_ensayo'][4][2][7]))
    if len(pru) == 9:
        canvas.drawString(275, 392, str(datos['resultados_del_ensayo'][4][2][4]))
        canvas.drawString(275, 379, str(datos['resultados_del_ensayo'][4][2][5]))
        canvas.drawString(275, 366, str(datos['resultados_del_ensayo'][4][2][6]))
        canvas.drawString(275, 353, str(datos['resultados_del_ensayo'][4][2][7]))
        canvas.drawString(275, 340, str(datos['resultados_del_ensayo'][4][2][8]))

    canvas.drawString(328, 444, str(datos['resultados_del_ensayo'][4][3][0]))
    canvas.drawString(328, 431, str(datos['resultados_del_ensayo'][4][3][1]))
    canvas.drawString(328, 418, str(datos['resultados_del_ensayo'][4][3][2]))
    canvas.drawString(328, 405, str(datos['resultados_del_ensayo'][4][3][3]))

    if len(pru) == 5:
        canvas.drawString(328, 392, str(datos['resultados_del_ensayo'][4][3][4]))
    if len(pru) == 6:
        canvas.drawString(328, 392, str(datos['resultados_del_ensayo'][4][3][4]))
        canvas.drawString(328, 379, str(datos['resultados_del_ensayo'][4][3][5]))
    if len(pru) == 7:
        canvas.drawString(328, 392, str(datos['resultados_del_ensayo'][4][3][4]))
        canvas.drawString(328, 379, str(datos['resultados_del_ensayo'][4][3][5]))
        canvas.drawString(328, 366, str(datos['resultados_del_ensayo'][4][3][6]))
    if len(pru) == 8:
        canvas.drawString(328, 392, str(datos['resultados_del_ensayo'][4][3][4]))
        canvas.drawString(328, 379, str(datos['resultados_del_ensayo'][4][3][5]))
        canvas.drawString(328, 366, str(datos['resultados_del_ensayo'][4][3][6]))
        canvas.drawString(328, 353, str(datos['resultados_del_ensayo'][4][3][7]))
    if len(pru) == 9:
        canvas.drawString(328, 392, str(datos['resultados_del_ensayo'][4][3][4]))
        canvas.drawString(328, 379, str(datos['resultados_del_ensayo'][4][3][5]))
        canvas.drawString(328, 366, str(datos['resultados_del_ensayo'][4][3][6]))
        canvas.drawString(328, 353, str(datos['resultados_del_ensayo'][4][3][7]))
        canvas.drawString(328, 340, str(datos['resultados_del_ensayo'][4][3][8]))
    # imagen ensayo
    canvas.drawImage("static/" + datos['direccion_de_grafico'], 371, 355, width=200, height=120)  # izquierda, abajo


    canvas.line(60, 320, 430, 320)  ## horizontal

    canvas.line(60, 320, 60,
                255)  # vertical iquierdo  (mover linea hacia derecha punto arriba, linea hacia arriba, mover linea hacia derecha punto abajo)
    canvas.line(100, 320, 100, 255)
    canvas.line(172, 320, 172, 255)
    canvas.line(220, 310, 220, 255)  # vetical retenido acumulado
    canvas.line(265, 320, 265, 255)  # vetical
    canvas.line(320, 320, 320, 255)
    canvas.line(379, 320, 379, 255)  # vertical
    canvas.line(430, 320, 430, 255)  # vertical dercho
    canvas.line(172, 310, 265, 310)  ## horizontal retenido acumulado

    for i in range(4):
        canvas.line(60, 294 - i * 13, 430, 294 - i * 13)  ## horizontal

    canvas.setFont('Helvetica', 8)
    canvas.drawString(61, 305, 'Tamiz Nº')
    canvas.drawString(103, 305, 'Peso Retenido.(gr)')
    canvas.drawString(184, 312, 'Retenido acumulado')

    canvas.drawString(187, 300, 'grs')
    canvas.drawString(235, 300, '%')

    canvas.drawString(268, 311, '% Que pasa')
    canvas.drawString(268, 302, 'de mortero')
    canvas.drawString(322, 305, 'Tamaño (mm)')
    canvas.drawString(383, 305, '% Que pasa')

    # ------- DATOS ----------------------  datos['datos_muestra_laboratorio'][3]
    canvas.drawString(65, 285, str(datos['resultados_del_ensayo'][5][5][0]))
    canvas.drawString(65, 272, str(datos['resultados_del_ensayo'][5][5][1]))
    canvas.drawString(65, 259, str(datos['resultados_del_ensayo'][5][5][2]))
    # ---------- peso retenido-----------------------------------------------
    canvas.drawString(110, 285, str(datos['datos_muestra_laboratorio'][3][0]))
    canvas.drawString(110, 272, str(datos['datos_muestra_laboratorio'][3][1]))
    canvas.drawString(110, 259, str(datos['datos_muestra_laboratorio'][3][2]))
    # ----------     gr   -----------------------------------------------
    canvas.drawString(175, 285, str(datos['resultados_del_ensayo'][5][0][0]))
    canvas.drawString(175, 272, str(datos['resultados_del_ensayo'][5][0][1]))
    canvas.drawString(175, 259, str(datos['resultados_del_ensayo'][5][0][2]))

    # ----------     %   -----------------------------------------------
    canvas.drawString(225, 285, str(datos['resultados_del_ensayo'][5][1][0]))
    canvas.drawString(225, 272, str(datos['resultados_del_ensayo'][5][1][1]))
    canvas.drawString(225, 259, str(datos['resultados_del_ensayo'][5][1][2]))

    # ----------     mortero  -----------------------------------------------
    canvas.drawString(280, 285, str(datos['resultados_del_ensayo'][5][2][0]))
    canvas.drawString(280, 272, str(datos['resultados_del_ensayo'][5][2][1]))
    canvas.drawString(280, 259, str(datos['resultados_del_ensayo'][5][2][2]))

    # ----------     tamano mm  -----------------------------------------------
    canvas.drawString(340, 285, str(datos['resultados_del_ensayo'][5][3][0]))
    canvas.drawString(340, 272, str(datos['resultados_del_ensayo'][5][3][1]))
    canvas.drawString(340, 259, str(datos['resultados_del_ensayo'][5][3][2]))

    # ----------     que pasa  -----------------------------------------------
    canvas.drawString(390, 285, str(datos['resultados_del_ensayo'][5][4][0]))
    canvas.drawString(390, 272, str(datos['resultados_del_ensayo'][5][4][1]))
    canvas.drawString(390, 259, str(datos['resultados_del_ensayo'][5][4][2]))

    canvas.line(60, 239, 550, 239)  ## horizontal abajo9
    canvas.line(60, 226, 550, 226)  ## horizontal abajo9
    canvas.line(60, 213, 550, 213)  ## horizontal abajo9
    canvas.line(60, 200, 550, 200)  ## horizontal abajo9
    canvas.line(60, 187, 370, 187)  ## horizontal abajo9
    canvas.line(60, 174, 370, 174)  ## horizontal abajo9

    canvas.drawString(65, 229, 'D60 =')
    canvas.drawString(320, 229, str(datos['resultados_del_ensayo'][1][0]))
    canvas.drawString(65, 216, 'D30 =')
    canvas.drawString(320, 216, str(datos['resultados_del_ensayo'][1][1]))
    canvas.drawString(65, 203, 'D10 =')
    canvas.drawString(320, 203, str(datos['resultados_del_ensayo'][1][2]))
    # # ----------------------------------------------------------------------
    canvas.drawString(65, 190, 'Cc (Coeficiente de curvatura)')
    canvas.drawString(320, 190, str(datos['resultados_del_ensayo'][2][0]))
    canvas.drawString(65, 177, 'Cu (Coeficiente de uniformidad)')
    canvas.drawString(320, 177, str(datos['resultados_del_ensayo'][2][1]))
    #
    # # ----------------------------------------------------------------------
    canvas.drawString(375, 229, "% Grava =")
    canvas.drawString(500, 229, str(datos['resultados_del_ensayo'][3][0]))
    canvas.drawString(375, 216, "% Arena =")
    canvas.drawString(500, 216, str(datos['resultados_del_ensayo'][3][2]))
    canvas.drawString(375, 203, "% Finos =")
    canvas.drawString(500, 203, str(datos['resultados_del_ensayo'][3][1]))
    canvas.line(60, 174, 60,
                239)  # vertical iquierdo  (mover linea hacia derecha punto arriba, linea hacia arriba, mover linea hacia derecha punto abajo)
    canvas.line(370, 174, 370, 239)  # vertical dercho
    canvas.line(550, 200, 550, 239)  # vertical dercho

    #
    # observaciones
    canvas.drawString(80, 150, 'D. OBSERVACIONES')
    canvas.line(60, 140, 550, 140)  ## horizontal abajo9
    linea7 = 480
    # FIRMAS
    canvas.drawString(70, 95, 'Firma del jefe de carrera')
    canvas.drawString(420, 95, 'Firma del tecnico')
    canvas.line(puntoAx, puntoY - linea7 - 110, puntoMedio - 90, puntoY - linea7 - 110)
    canvas.line(puntoMedio + 80, puntoY - linea7 - 110, puntoBx, puntoY - linea7 - 110)

    # DATOS ACREDITACION
    linea8y = 90
    canvas.drawString(90, linea8y - 10, 'ELABORADO POR')
    canvas.drawString(260, linea8y - 10, 'REVISADO POR')
    canvas.drawString(420, linea8y - 10, 'APROBADO POR')

    canvas.line(puntoAx, linea8y, puntoBx, linea8y)
    linea8y = linea8y - 15
    canvas.line(puntoAx, linea8y, puntoBx, linea8y)
    linea8y = linea8y - 25
    canvas.line(puntoAx, linea8y, puntoBx, linea8y)
    canvas.line(puntoAx, linea8y + 40, puntoAx, linea8y)  # vertical
    canvas.line(puntoBx, linea8y + 40, puntoBx, linea8y)  # vertical
    canvas.line(puntoMedio - 90, linea8y + 40, puntoMedio - 90, linea8y)  # vertical
    canvas.line(puntoMedio + 90, linea8y + 40, puntoMedio + 90, linea8y)  # vertical

    # FIN COPIAR

    canvas.save()
    pdf_out = output.getvalue()
    output.close()
    filename = 'granulometriaAASHTO.pdf'
    response = make_response(pdf_out)
    response.headers['Content-Disposition'] = "attachment; filename"
    response.mimetype = 'application/pdf'
    # return response
    return send_file(filename, as_attachment=False)

# ############################################# PRLIMITES DE CONSSITENCIA AASHTO ######################################

def reporte_limite_conssitencia_aashto2(datoslimitesCaashto):
    datos=datoslimitesCaashto[1]
    output = cStringIO.StringIO()
    canvas = Canvas("limite_consistencia_aashto.pdf", pagesize=letter)  # granulometria nombre del pdf
    canvas.setLineWidth(.3)
    canvas.setFont('Helvetica', 10)

    canvas.line(60, 760, 550, 760)  # punto x1, y1 , x2, y2 #HORIZONTAL
    canvas.line(60, 760, 60, 700)  # VERTICAL
    canvas.line(60, 700, 550, 700)  # HORIZONTAL
    canvas.line(550, 760, 550, 700)  # VERTICAL
    canvas.line(190, 760, 190, 700)  # VERTICAL
    canvas.line(400, 760, 400, 700)  # VERTICAL
    # CAJETIN PEQUENO
    canvas.line(400, 745, 550, 745)  # HORIZONTAL
    canvas.line(400, 730, 550, 730)  # HORIZONTAL
    canvas.line(400, 715, 550, 715)  # HORIZONTAL
    canvas.line(470, 760, 470, 715)  # VERTICAL
    canvas.drawImage("static/img/emi.jpeg", 70, 710, width=115, height=40)

    # TITULO
    frame1 = Frame(190, 700, 210, 60, showBoundary=1)  # Frame(movX,movY,margenAncho,mrgenAlto)
    bodyStyle = ParagraphStyle('normal', fontSize=24, leading=28, spaceBefore=30, alignment=TA_CENTER)
    s = datoslimitesCaashto[0]
    story = [Paragraph(s, bodyStyle)]
    story_inframe = KeepInFrame(210, 1 * inch, story)
    frame1.addFromList([story_inframe], canvas)
    # interlineado=740
    story = []
    # DATOS
    posx = 410
    canvas.setFont('Helvetica', 10)
    canvas.drawString(posx, 750, 'Codigo:')
    canvas.drawString(posx, 735, 'Aprobacion:')
    canvas.drawString(posx, 720, 'Version:')
    canvas.drawString(posx + 70, 750, 'C5117-9')
    canvas.drawString(posx + 70, 735, 'Aprobado')
    canvas.drawString(posx + 70, 720, 'Version 1.1')
    canvas.drawString(posx + 30, 703, 'Página 1 de 1')

    # SEGUNDA CAJETILLA
    puntoAx = 60
    puntoBx = 550
    puntoY = 698
    puntoMedio = (puntoAx + puntoBx) / 2

    canvas.line(60, 695, 550,
                695)  # horizontal arriba (largohacialaIZQUIERDA ,arribaIZQ , largo de la linea hacia la derecha ,arribaDER)
    canvas.setFont('Helvetica', 10)
    canvas.drawString(235, 680, 'A. DATOS GENRALES')  # (# ,  arriba , #)
    canvas.line(60, 700, 60,
                489)  # vertical iquierdo  (mover linea hacia derecha punto arriba, linea hacia arriba, mover linea hacia derecha punto abajo)
    canvas.line(550, 700, 550, 489)  # vertical DERECHO
    canvas.line(60, 678, 550, 678)  ## horizontal abajo
    # primero
    canvas.setFont('Helvetica', 9)
    canvas.drawString(160, 670, 'Proyecto')
    canvas.drawString(400, 670, 'Fecha')
    canvas.line(60, 668, 550, 668)  ## horizontal abajo2
    canvas.line(300, 678, 300, 607)  # vertical2 MEDIO
    canvas.setFont('Helvetica', 12)
    canvas.drawString(70, 657, datos['datos_generales'][0])
    canvas.drawString(310, 657, datos['datos_generales'][7])
    canvas.line(60, 655, 550, 655)  ## horizontal abajo3
    # segundo
    canvas.setFont('Helvetica', 9)
    canvas.drawString(160, 647, 'Ubicacion')
    canvas.drawString(400, 647, 'Laboratista')
    canvas.line(60, 645, 550, 645)  ## horizontal abajo4
    canvas.setFont('Helvetica', 12)
    canvas.drawString(70, 634, datos['datos_generales'][1])
    canvas.drawString(310, 634, datos['datos_generales'][4])
    canvas.line(60, 631, 550, 631)  ## horizontal abajo5

    # tercero
    canvas.setFont('Helvetica', 9)
    canvas.drawString(120, 623, 'Descripcion De La Muestra')
    canvas.drawString(380, 623, 'Tipo De Muestra')
    canvas.line(60, 620, 550, 620)  ## horizontal abajo6
    canvas.setFont('Helvetica', 12)
    canvas.drawString(70, 609, datos['datos_generales'][2])
    canvas.drawString(310, 609, datos['datos_generales'][3])
    canvas.line(60, 607, 550, 607)  ## horizontal abajo7

    # datos de calculo
    canvas.setFont('Helvetica', 10)
    canvas.drawString(200, 596, 'B. DETERMINACION DEL LIMITE LIQUIDO')
    canvas.line(60, 594, 550, 594)  ## horizontal
    canvas.line(500, 488.8, 500, 594)  # vertical MEDIO
    canvas.line(450, 488.8, 450, 594)  # vertical MEDIO
    canvas.line(400, 488.8, 400, 594)  # vertical MEDIO
    canvas.line(350, 488.8, 350, 594)  # vertical MEDIO
    canvas.drawString(65, 583, 'Numero de contenedor')
    canvas.drawString(370, 583, datos['datos_muestra_laboratorio'][0][0])
    canvas.drawString(420, 583, datos['datos_muestra_laboratorio'][0][1])
    canvas.drawString(465, 583, datos['datos_muestra_laboratorio'][0][2])
    canvas.drawString(520, 583, datos['datos_muestra_laboratorio'][0][3])
    canvas.line(60, 580, 550, 580)  ## horizontal
    canvas.drawString(65, 570, 'Masa recipiente (g) Mr')
    canvas.drawString(355, 570, datos['datos_muestra_laboratorio'][1][0][0])
    canvas.drawString(405, 570, datos['datos_muestra_laboratorio'][1][1][0])
    canvas.drawString(455.5, 570, datos['datos_muestra_laboratorio'][1][2][0])
    canvas.drawString(505, 570, datos['datos_muestra_laboratorio'][1][3][0])
    canvas.line(60, 567, 550, 567)  ## horizontal
    canvas.drawString(65, 557, 'Numero de golpes N')
    canvas.drawString(370, 557, datos['datos_muestra_laboratorio'][1][0][1])
    canvas.drawString(420, 557, datos['datos_muestra_laboratorio'][1][1][1])
    canvas.drawString(465, 557, datos['datos_muestra_laboratorio'][1][2][1])
    canvas.drawString(520, 557, datos['datos_muestra_laboratorio'][1][3][1])
    canvas.line(60, 554, 550, 554)  ## horizontal
    canvas.drawString(65, 544, 'Masa del reciente + suelo humedo (g) Mw+r')
    canvas.drawString(355, 544, datos['datos_muestra_laboratorio'][1][0][2])
    canvas.drawString(405, 544, datos['datos_muestra_laboratorio'][1][1][2])
    canvas.drawString(455.5, 544, datos['datos_muestra_laboratorio'][1][2][2])
    canvas.drawString(505, 544, datos['datos_muestra_laboratorio'][1][3][2])
    canvas.line(60, 541, 550, 541)  ## horizontal
    canvas.drawString(65, 531, 'Masa del reciente + suelo seco (g) Md+r')
    canvas.drawString(355, 531, datos['datos_muestra_laboratorio'][1][0][3])
    canvas.drawString(405, 531, datos['datos_muestra_laboratorio'][1][1][3])
    canvas.drawString(455.5, 531, datos['datos_muestra_laboratorio'][1][2][3])
    canvas.drawString(505, 531, datos['datos_muestra_laboratorio'][1][3][3])
    canvas.line(60, 528, 550, 528)  ## horizontal
    canvas.drawString(65, 518, 'Masa del agua (g) Mw')
    canvas.drawString(355, 518, str(datos['resultados_del_ensayo'][0][2][0]))
    canvas.drawString(405, 518, str(datos['resultados_del_ensayo'][0][2][1]))
    canvas.drawString(455.5, 518, str(datos['resultados_del_ensayo'][0][2][2]))
    canvas.drawString(505, 518, str(datos['resultados_del_ensayo'][0][2][3]))
    canvas.line(60, 515, 550, 515)  ## horizontal
    canvas.drawString(65, 505, 'Masa de suelo seco (g) Md')
    canvas.drawString(355, 505, str(datos['resultados_del_ensayo'][0][3][0]))
    canvas.drawString(405, 505, str(datos['resultados_del_ensayo'][0][3][1]))
    canvas.drawString(455.5, 505, str(datos['resultados_del_ensayo'][0][3][2]))
    canvas.drawString(505, 505, str(datos['resultados_del_ensayo'][0][3][3]))
    canvas.line(60, 502, 550, 502)  ## horizontal
    canvas.drawString(65, 492, 'Contenido de humedad w (%)')
    canvas.drawString(355, 492, str(datos['resultados_del_ensayo'][0][0][0]))
    canvas.drawString(405, 492, str(datos['resultados_del_ensayo'][0][0][1]))
    canvas.drawString(455.5, 492, str(datos['resultados_del_ensayo'][0][0][2]))
    canvas.drawString(505, 492, str(datos['resultados_del_ensayo'][0][0][3]))
    canvas.line(60, 489, 550, 489)  ## horizontal

    # LL - Lp - IP
    canvas.line(350, 430, 550, 430)  ## horizontal
    canvas.line(350, 417, 550, 417)  ## horizontal
    canvas.line(350, 404, 550, 404)  ## horizontal
    canvas.line(350, 391, 550, 391)  ## horizontal
    canvas.line(350, 430, 350, 390)  # vertical IZQ
    canvas.line(490, 430, 490, 390)  # vertical MEDIO
    canvas.line(550, 430, 550, 390)  # vertical DER
    canvas.drawString(352, 420, 'Limite Liquido')
    canvas.drawString(505, 420, str(datos['resultados_del_ensayo'][0][4][0][0]))
    canvas.drawString(352, 407, 'Limite Plastico')
    canvas.drawString(505, 407, str(datos['resultados_del_ensayo'][1][3]))
    canvas.drawString(352, 394, 'Indice de Plasticidad')
    canvas.drawString(505, 394, str(datos['resultados_del_ensayo'][2]))
    # imagen ensayo
    canvas.drawImage("static/" + datos['direccion_de_grafico'], 100, 328, width=200,
                     height=160)  # izquierda, abajo

    canvas.line(60, 299, 550, 299)  ## horizontal abajo9
    canvas.line(60, 286, 550, 286)  ## horizontal abajo9
    canvas.line(60, 273, 550, 273)  ## horizontal abajo9
    canvas.line(60, 260, 550, 260)  ## horizontal abajo9
    canvas.line(60, 247, 550, 247)  ## horizontal abajo9
    canvas.line(60, 234, 550, 234)  ## horizontal abajo9
    canvas.line(60, 221, 550, 221)  ## horizontal abajo9
    canvas.line(60, 208, 550, 208)  ## horizontal abajo9
    canvas.line(60, 195, 550, 195)  ## horizontal abajo9
    canvas.line(60, 195, 60,
                299)  # vertical iquierdo  (mover linea hacia derecha punto arriba, linea hacia arriba, mover linea hacia derecha punto abajo)
    canvas.line(500, 195, 500, 286)  # vertical Medio
    canvas.line(450, 195, 450, 286)  # vertical Medio
    canvas.line(400, 195, 400, 286)  # vertical Medio
    canvas.line(550, 195, 550, 299)  # vertical dercho
    canvas.setFont('Helvetica', 10)
    canvas.drawString(190, 289, 'C. DETERMINACION DEL LIMITE PLASTICO')
    canvas.drawString(65, 276, 'Numero de contenedor')
    canvas.drawString(415.5, 276, datos['datos_muestra_laboratorio'][0][4])
    canvas.drawString(463.5, 276, datos['datos_muestra_laboratorio'][0][5])
    canvas.drawString(511.5, 276, datos['datos_muestra_laboratorio'][0][6])
    # -----------------------------------------------------------------------
    canvas.drawString(65, 263, 'Masa recipiente (g) Mr')
    canvas.drawString(414, 263, datos['datos_muestra_laboratorio'][2][0][0])
    canvas.drawString(462, 263, datos['datos_muestra_laboratorio'][2][1][0])
    canvas.drawString(510, 263, datos['datos_muestra_laboratorio'][2][2][0])
    # ----------------------------------------------------------------------
    canvas.drawString(65, 250, 'Masa del contenedor + suelo humedo (g) Mw+r')
    canvas.drawString(414, 250, datos['datos_muestra_laboratorio'][2][0][1])
    canvas.drawString(462, 250, datos['datos_muestra_laboratorio'][2][1][1])
    canvas.drawString(510, 250, datos['datos_muestra_laboratorio'][2][2][1])
    # -----------------------------------------------------------------------
    canvas.drawString(65, 237, 'Masa del contenedor + suelo seco (g) Md+r')
    canvas.drawString(414, 237, datos['datos_muestra_laboratorio'][2][0][2])
    canvas.drawString(462, 237, datos['datos_muestra_laboratorio'][2][1][2])
    canvas.drawString(510, 237, datos['datos_muestra_laboratorio'][2][2][2])
    # -----------------------------------------------------------------------
    canvas.drawString(65, 224, 'Masa del agua (g) Mw')
    canvas.drawString(414, 224, str(datos['resultados_del_ensayo'][1][1][0]))
    canvas.drawString(462, 224, str(datos['resultados_del_ensayo'][1][1][1]))
    canvas.drawString(510, 224, str(datos['resultados_del_ensayo'][1][1][2]))
    # ----------------------------------------------------------------------
    canvas.drawString(65, 211, 'Masa del suelo seco (g) Md')
    canvas.drawString(414, 211, str(datos['resultados_del_ensayo'][1][2][0]))
    canvas.drawString(462, 211, str(datos['resultados_del_ensayo'][1][2][1]))
    canvas.drawString(510, 211, str(datos['resultados_del_ensayo'][1][2][2]))
    # ------------------------------------------------------------------------
    canvas.drawString(65, 198, 'Contenido de humedad w (%)')
    canvas.drawString(414, 198, str(datos['resultados_del_ensayo'][1][0][0]))
    canvas.drawString(462, 198, str(datos['resultados_del_ensayo'][1][0][1]))
    canvas.drawString(510, 198, str(datos['resultados_del_ensayo'][1][0][2]))

    # observaciones
    canvas.drawString(80, 150, 'D. OBSERVACIONES')
    canvas.line(60, 140, 550, 140)  ## horizontal abajo9
    linea7 = 480
    # FIRMAS
    canvas.drawString(70, 95, 'Firma del jefe de carrera')
    canvas.drawString(420, 95, 'Firma del tecnico')
    canvas.line(puntoAx, puntoY - linea7 - 110, puntoMedio - 90, puntoY - linea7 - 110)
    canvas.line(puntoMedio + 80, puntoY - linea7 - 110, puntoBx, puntoY - linea7 - 110)

    # DATOS ACREDITACION
    linea8y = 70
    canvas.drawString(90, linea8y - 10, 'ELABORADO POR')
    canvas.drawString(260, linea8y - 10, 'REVISADO POR')
    canvas.drawString(420, linea8y - 10, 'APROBADO POR')

    canvas.line(puntoAx, linea8y, puntoBx, linea8y)
    linea8y = linea8y - 15
    canvas.line(puntoAx, linea8y, puntoBx, linea8y)
    linea8y = linea8y - 25
    canvas.line(puntoAx, linea8y, puntoBx, linea8y)
    canvas.line(puntoAx, linea8y + 40, puntoAx, linea8y)  # vertical
    canvas.line(puntoBx, linea8y + 40, puntoBx, linea8y)  # vertical
    canvas.line(puntoMedio - 90, linea8y + 40, puntoMedio - 90, linea8y)  # vertical
    canvas.line(puntoMedio + 90, linea8y + 40, puntoMedio + 90, linea8y)  # vertical

    # FIN COPIAR

    canvas.save()
    pdf_out = output.getvalue()
    output.close()
    filename = 'limite_consistencia_aashto.pdf'
    response = make_response(pdf_out)
    response.headers['Content-Disposition'] = "attachment; filename"
    response.mimetype = 'application/pdf'
    # return response

    return send_file(filename, as_attachment=False)


###################################### RPLMITE DE CONTRACCION  ######################################################

def reporte_limite_de_contraccion_astm2(datoslimiteCastm):
    datos=datoslimiteCastm[1]

    output = cStringIO.StringIO()
    canvas = Canvas("limite_contraccion_astm.pdf", pagesize=letter)
    canvas.setLineWidth(.3)
    canvas.setFont('Helvetica', 10)

    canvas.line(60, 760, 550, 760)  # punto x1, y1 , x2, y2 #HORIZONTAL
    canvas.line(60, 760, 60, 700)  # VERTICAL
    canvas.line(60, 700, 550, 700)  # HORIZONTAL
    canvas.line(550, 760, 550, 700)  # VERTICAL
    canvas.line(190, 760, 190, 700)  # VERTICAL
    canvas.line(400, 760, 400, 700)  # VERTICAL
    # CAJETIN PEQUENO
    canvas.line(400, 745, 550, 745)  # HORIZONTAL
    canvas.line(400, 730, 550, 730)  # HORIZONTAL
    canvas.line(400, 715, 550, 715)  # HORIZONTAL
    canvas.line(470, 760, 470, 715)  # VERTICAL

    canvas.drawImage("static/img/emi.jpeg", 70, 710, width=115, height=40)

    # TITULO
    frame1 = Frame(190, 700, 210, 60, showBoundary=1)  # Frame(movX,movY,margenAncho,mrgenAlto)
    bodyStyle = ParagraphStyle('normal', fontSize=24, leading=28, spaceBefore=30, alignment=TA_CENTER)
    s = datoslimiteCastm[0]
    story = [Paragraph(s, bodyStyle)]
    story_inframe = KeepInFrame(210, 1 * inch, story)
    frame1.addFromList([story_inframe], canvas)
    # interlineado=740

    # DATOS
    posx = 410
    canvas.setFont('Helvetica', 10)
    canvas.drawString(posx, 750, 'Codigo:')
    canvas.drawString(posx, 735, 'Aprobacion:')
    canvas.drawString(posx, 720, 'Version:')
    canvas.drawString(posx + 70, 750, 'C5102-0')
    canvas.drawString(posx + 70, 735, 'Aprobado')
    canvas.drawString(posx + 70, 720, 'Version 1.1')
    canvas.drawString(posx + 30, 703, 'Página 1 de 1')

    # SEGUNDA CAJETILLA
    puntoAx = 60
    puntoBx = 550
    puntoY = 698
    puntoMedio = (puntoAx + puntoBx) / 2

    canvas.line(60, 680, 550,
                680)  # horizontal arriba (largohacialaIZQUIERDA ,arribaIZQ , largo de la linea hacia la derecha ,arribaDER)
    canvas.setFont('Helvetica', 12)
    canvas.drawString(235, 665, 'A. DATOS GENRALES')  # (# ,  arriba , #)
    canvas.line(60, 680, 60,
                568)  # vertical iquierdo  (mover linea hacia derecha punto arriba, linea hacia arriba, mover linea hacia derecha punto abajo)
    canvas.line(550, 680, 550, 568)  # vertical DERECHO
    canvas.line(60, 661, 550, 661)  ## horizontal abajo
    # primero
    canvas.setFont('Helvetica', 9)
    canvas.drawString(160, 651, 'Proyecto')
    canvas.line(60, 649, 550, 649)  ## horizontal abajo2
    canvas.line(300, 660, 300, 568)  # vertical2 MEDIO
    canvas.drawString(400, 651, 'Fecha')
    canvas.setFont('Helvetica', 12)
    canvas.drawString(70, 633, datos['datos_generales'][0])
    canvas.drawString(310, 633, datos['datos_generales'][7])
    canvas.line(60, 630, 550, 630)  ## horizontal abajo3
    # segundo
    canvas.setFont('Helvetica', 9)
    canvas.drawString(160, 620, 'Ubicacion')
    canvas.drawString(400, 620, 'Laboratista')
    canvas.line(60, 618, 550, 618)  ## horizontal abajo4
    canvas.line(60, 599, 550, 599)  ## horizontal abajo5
    canvas.setFont('Helvetica', 12)
    canvas.drawString(70, 602, datos['datos_generales'][1])
    canvas.drawString(310, 602, datos['datos_generales'][4])

    # tercero
    canvas.setFont('Helvetica', 9)
    canvas.drawString(120, 589, 'Descripcion De La Muestra')
    canvas.drawString(380, 589, 'Tipo De Muestra')
    canvas.line(60, 587, 550, 587)  ## horizontal abajo6
    canvas.line(60, 568, 550, 568)  ## horizontal abajo7
    canvas.setFont('Helvetica', 12)
    canvas.drawString(70, 571, datos['datos_generales'][2])
    canvas.drawString(310, 571, datos['datos_generales'][3])

    # # tabla calculos
    canvas.line(60, 550, 550, 550)  ## horizontal
    canvas.line(60, 530, 550, 530)  ## horizontal
    canvas.line(60, 550, 60, 230)  # vertical iquierdo
    canvas.line(550, 550, 550, 230)  # vertical DERECHO
    canvas.setFont('Helvetica', 12)
    canvas.drawString(120, 535, 'B. CALCULO DETERMINACION DEL CONTENIDO DE HUMEDAD')

    canvas.line(450, 530, 450, 290)  # vertical2 MEDIO

    canvas.line(450, 270, 450, 230)  # vertical2 MEDIO
    canvas.drawString(65, 515, 'Densidad del mercurio (cm3)M')
    canvas.drawString(478, 515, datos['datos_muestra_laboratorio'][0])
    canvas.line(60, 510, 550, 510)  ## horizontal
    canvas.drawString(65, 495, 'Masa del mercurio en el recipiente de vidrio (g)')
    canvas.drawString(478, 495, datos['datos_muestra_laboratorio'][1])
    canvas.line(60, 490, 550, 490)  ## horizontal
    canvas.drawString(65, 475, 'Volumen inicial del recipiente de vidrio')
    canvas.drawString(478, 475, str(datos['resultados_del_ensayo'][0]))
    canvas.line(60, 470, 550, 470)  ## horizontal
    canvas.drawString(65, 455, 'Masa del recipiente de contracción (g) Mrc')
    canvas.drawString(478, 455, str(datos['datos_muestra_laboratorio'][2]))
    canvas.line(60, 450, 550, 450)  ## horizontal
    canvas.drawString(65, 435, 'Masa del recipiente de contraccion mas la muestra húmeda (g) Mw')
    canvas.drawString(478, 435, str(datos['datos_muestra_laboratorio'][3]))
    canvas.line(60, 430, 550, 430)  ## horizontal
    canvas.drawString(65, 415, 'Masa del recipiente de contraccion mas la muestra seca (g) Md')
    canvas.drawString(478, 415, str(datos['datos_muestra_laboratorio'][4]))
    canvas.line(60, 410, 550, 410)  ## horizontal
    canvas.drawString(65, 395, 'Masa del mercurio desplazado (g)')
    canvas.drawString(478, 395, str(datos['datos_muestra_laboratorio'][5]))
    canvas.line(60, 390, 550, 390)  ## horizontal
    canvas.drawString(65, 375, 'Masa de la muestra humeda (g) M1')
    canvas.drawString(478, 375, str(datos['resultados_del_ensayo'][1]))
    canvas.line(60, 370, 550, 370)  ## horizontal
    canvas.drawString(65, 355, 'Masa de la muestra seca (g) M2')
    canvas.drawString(478, 355, str(datos['resultados_del_ensayo'][2]))
    canvas.line(60, 350, 550, 350)  ## horizontal
    canvas.drawString(65, 335, 'Volumen de mercurio desplazado (cm3) Vo')
    canvas.drawString(478, 335, str(datos['resultados_del_ensayo'][3]))
    canvas.line(60, 330, 550, 330)  ## horizontal
    canvas.drawString(65, 315, 'Contenido de humedad inicial (%) wi')
    canvas.drawString(478, 315, str(datos['resultados_del_ensayo'][4]))
    canvas.line(60, 310, 550, 310)  ## horizontal
    canvas.drawString(65, 295, 'Cambio en el contenido de humedad (%) Δw')
    canvas.drawString(478, 295, str(datos['resultados_del_ensayo'][5]))
    canvas.line(60, 290, 550, 290)  ## horizontal

    canvas.line(60, 270, 550, 270)  ## horizontal
    canvas.drawString(65, 255, 'Límite de contracción (SL)%')
    canvas.drawString(478, 255, str(datos['resultados_del_ensayo'][6]))
    canvas.line(60, 250, 550, 250)  ## horizontal
    canvas.drawString(65, 235, 'Índice de contracción')
    canvas.drawString(478, 235, str(datos['resultados_del_ensayo'][7]))
    canvas.line(60, 230, 550, 230)  ## horizontal

    # observaciones
    canvas.drawString(80, 195, 'D. OBSERVACIONES')
    canvas.line(60, 170, 550, 170)  ## horizontal abajo9
    linea7 = 480
    # FIRMAS
    canvas.drawString(70, 95, 'Firma del jefe de carrera')
    canvas.drawString(420, 95, 'Firma del tecnico')
    canvas.line(puntoAx, puntoY - linea7 - 110, puntoMedio - 90, puntoY - linea7 - 110)
    canvas.line(puntoMedio + 80, puntoY - linea7 - 110, puntoBx, puntoY - linea7 - 110)

    # DATOS ACREDITACION
    linea8y = 70
    canvas.drawString(90, linea8y - 10, 'ELABORADO POR')
    canvas.drawString(260, linea8y - 10, 'REVISADO POR')
    canvas.drawString(420, linea8y - 10, 'APROBADO POR')

    canvas.line(puntoAx, linea8y, puntoBx, linea8y)
    linea8y = linea8y - 15
    canvas.line(puntoAx, linea8y, puntoBx, linea8y)
    linea8y = linea8y - 25
    canvas.line(puntoAx, linea8y, puntoBx, linea8y)
    canvas.line(puntoAx, linea8y + 40, puntoAx, linea8y)  # vertical
    canvas.line(puntoBx, linea8y + 40, puntoBx, linea8y)  # vertical
    canvas.line(puntoMedio - 90, linea8y + 40, puntoMedio - 90, linea8y)  # vertical
    canvas.line(puntoMedio + 90, linea8y + 40, puntoMedio + 90, linea8y)  # vertical

    # FIN COPIAR

    canvas.save()
    pdf_out = output.getvalue()

    output.close()
    filename = 'limite_contraccion_astm.pdf'
    response = make_response(pdf_out)
    response.headers['Content-Disposition'] = "attachment; filename"
    response.mimetype = 'application/pdf'
    # return response
    return send_file(filename, as_attachment=False)





#################################### RPPROCTOR MODIFICADO ASTM ######################################################

def reporte_proctor_modificado_astm2(datoPMASTM):
    datos=datoPMASTM[1]

    output = cStringIO.StringIO()
    canvas = Canvas("proctor_modificado_astm.pdf", pagesize=letter)
    canvas.setLineWidth(.3)
    canvas.setFont('Helvetica', 10)

    canvas.line(60, 760, 550, 760)  # punto x1, y1 , x2, y2 #HORIZONTAL
    canvas.line(60, 760, 60, 700)  # VERTICAL
    canvas.line(60, 700, 550, 700)  # HORIZONTAL
    canvas.line(550, 760, 550, 700)  # VERTICAL
    canvas.line(190, 760, 190, 700)  # VERTICAL
    canvas.line(400, 760, 400, 700)  # VERTICAL
    # CAJETIN PEQUENO
    canvas.line(400, 745, 550, 745)  # HORIZONTAL
    canvas.line(400, 730, 550, 730)  # HORIZONTAL
    canvas.line(400, 715, 550, 715)  # HORIZONTAL
    canvas.line(470, 760, 470, 715)  # VERTICAL
    canvas.drawImage("static/img/emi.jpeg", 70, 710, width=115, height=40)

    # TITULO
    frame1 = Frame(190, 700, 210, 60, showBoundary=1)  # Frame(movX,movY,margenAncho,mrgenAlto)
    bodyStyle = ParagraphStyle('normal', fontSize=24, leading=28, spaceBefore=30, alignment=TA_CENTER)
    s = datoPMASTM[0]
    story = [Paragraph(s, bodyStyle)]
    story_inframe = KeepInFrame(210, 1 * inch, story)
    frame1.addFromList([story_inframe], canvas)
    # interlineado=740
    story = []
    # DATOS
    posx = 410
    canvas.setFont('Helvetica', 10)
    canvas.drawString(posx, 750, 'Codigo:')
    canvas.drawString(posx, 735, 'Aprobacion:')
    canvas.drawString(posx, 720, 'Version:')
    canvas.drawString(posx + 70, 750, 'C5117-9')
    canvas.drawString(posx + 70, 735, 'Aprobado')
    canvas.drawString(posx + 70, 720, 'Version 1.1')
    canvas.drawString(posx + 30, 703, 'Página 1 de 1')

    # SEGUNDA CAJETILLA
    puntoAx = 60
    puntoBx = 550
    puntoY = 698
    puntoMedio = (puntoAx + puntoBx) / 2

    canvas.line(60, 695, 550,
                695)  # horizontal arriba (largohacialaIZQUIERDA ,arribaIZQ , largo de la linea hacia la derecha ,arribaDER)
    canvas.setFont('Helvetica', 10)
    canvas.drawString(235, 680, 'A. DATOS GENRALES')  # (# ,  arriba , #)
    canvas.line(60, 700, 60,
                366)  # vertical iquierdo  (mover linea hacia derecha punto arriba, linea hacia arriba, mover linea hacia derecha punto abajo)
    canvas.line(550, 700, 550, 340)  # vertical DERECHO
    canvas.line(60, 678, 550, 678)  ## horizontal abajo

    # primero
    canvas.setFont('Helvetica', 9)
    canvas.drawString(160, 670, 'Proyecto')
    canvas.drawString(400, 670, 'Fecha')
    canvas.line(60, 668, 550, 668)  ## horizontal abajo2
    canvas.line(300, 678, 300, 607)  # vertical2 MEDIO
    canvas.setFont('Helvetica', 12)
    canvas.drawString(70, 657, datos['datos_generales'][0])
    canvas.drawString(310, 657, datos['datos_generales'][7])
    canvas.line(60, 655, 550, 655)  ## horizontal abajo3
    # segundo
    canvas.setFont('Helvetica', 9)
    canvas.drawString(160, 647, 'Ubicacion')
    canvas.drawString(400, 647, 'Laboratista')
    canvas.line(60, 645, 550, 645)  ## horizontal abajo4
    canvas.setFont('Helvetica', 12)
    canvas.drawString(70, 634, datos['datos_generales'][1])
    canvas.drawString(310, 634, datos['datos_generales'][4])
    canvas.line(60, 631, 550, 631)  ## horizontal abajo5

    # tercero
    canvas.setFont('Helvetica', 9)
    canvas.drawString(120, 623, 'Descripcion De La Muestra')
    canvas.drawString(380, 623, 'Tipo De Muestra')
    canvas.line(60, 620, 550, 620)  ## horizontal abajo6
    canvas.setFont('Helvetica', 12)
    canvas.drawString(70, 609, datos['datos_generales'][2])
    canvas.drawString(310, 609, datos['datos_generales'][3])
    canvas.line(60, 607, 550, 607)  ## horizontal abajo7

    # datos de calculo
    canvas.setFont('Helvetica', 10)
    canvas.drawString(235, 596, 'B. DATOS TECNICOS')
    canvas.line(60, 594, 550, 594)  ## horizontal
    canvas.line(280, 554, 280, 594)  # vertical MEDIO

    canvas.drawString(65, 583, 'Metodo utilizado')
    canvas.drawString(245, 583, datos['datos_muestra_laboratorio'][0][0])
    canvas.drawString(285, 583, "Diametro del molde (mm)")
    canvas.drawString(508, 583, datos['datos_muestra_laboratorio'][0][2])
    canvas.line(60, 580, 550, 580)  ## horizontal
    canvas.drawString(65, 570, 'Gravedad especifica')
    canvas.drawString(245, 570, datos['datos_muestra_laboratorio'][0][1])
    canvas.drawString(285, 570, "Altura del molde (mm)")
    canvas.drawString(508, 570, datos['datos_muestra_laboratorio'][0][3])
    canvas.line(60, 567, 550, 567)  ## horizontal
    canvas.drawString(65, 556, 'Volumen (cm3)')
    canvas.drawString(245, 556, datos['datos_muestra_laboratorio'][0][4])
    canvas.line(60, 554, 550, 554)  ## horizontal
    canvas.drawString(235, 543, 'C. PESO UNITARIO')
    canvas.line(60, 541, 550, 541)  ## horizontal
    canvas.line(325, 476, 325, 541)  # vertical MEDIO
    canvas.line(370, 476, 370, 541)  # vertical MEDIO
    canvas.line(415, 476, 415, 541)  # vertical MEDIO
    canvas.line(460, 476, 460, 541)  # vertical MEDIO
    canvas.line(505, 476, 505, 541)  # vertical MEDIO

    canvas.line(60, 528, 550, 528)  ## horizontal

    canvas.drawString(65, 531, 'Masa del agua (g) Mw')
    canvas.drawString(345, 531, "1")
    canvas.drawString(390, 531, "2")
    canvas.drawString(435, 531, "3")
    canvas.drawString(480, 531, "4")
    canvas.drawString(525, 531, "5")
    canvas.line(60, 515, 550, 515)  ## horizontal
    canvas.drawString(65, 518, 'Peso molde + suelo (g) M2')
    canvas.drawString(330, 518, datos['datos_muestra_laboratorio'][1][0])
    canvas.drawString(376, 518, datos['datos_muestra_laboratorio'][1][1])
    canvas.drawString(422, 518, datos['datos_muestra_laboratorio'][1][2])
    canvas.drawString(466, 518, datos['datos_muestra_laboratorio'][1][3])
    canvas.drawString(512, 518, datos['datos_muestra_laboratorio'][1][4])

    canvas.line(60, 502, 550, 502)  ## horizontal
    canvas.drawString(65, 505, 'Peso molde (g) M1')
    canvas.drawString(330, 505, datos['datos_muestra_laboratorio'][2][0])
    canvas.drawString(376, 505, datos['datos_muestra_laboratorio'][2][1])
    canvas.drawString(422, 505, datos['datos_muestra_laboratorio'][2][2])
    canvas.drawString(466, 505, datos['datos_muestra_laboratorio'][2][3])
    canvas.drawString(512, 505, datos['datos_muestra_laboratorio'][2][4])

    canvas.line(60, 489, 550, 489)  ## horizontal
    canvas.drawString(65, 492, 'Peso humedo del suelo (g) M')
    canvas.drawString(330, 492, str(datos['resultados_del_ensayo'][0][0]))
    canvas.drawString(376, 492, str(datos['resultados_del_ensayo'][0][1]))
    canvas.drawString(422, 492, str(datos['resultados_del_ensayo'][0][2]))
    canvas.drawString(466, 492, str(datos['resultados_del_ensayo'][0][3]))
    canvas.drawString(512, 492, str(datos['resultados_del_ensayo'][0][4]))

    canvas.line(60, 476, 550, 476)  ## horizontal
    canvas.drawString(65, 479, 'Peso humedo del suelo (g) M')
    canvas.drawString(330, 479, str(datos['resultados_del_ensayo'][1][0]))
    canvas.drawString(376, 479, str(datos['resultados_del_ensayo'][1][1]))
    canvas.drawString(422, 479, str(datos['resultados_del_ensayo'][1][2]))
    canvas.drawString(466, 479, str(datos['resultados_del_ensayo'][1][3]))
    canvas.drawString(512, 479, str(datos['resultados_del_ensayo'][1][4]))

    canvas.line(60, 470, 550, 470)  ## horizontal
    canvas.drawString(235, 460, 'D. CONTENIDO DE HUMEDAD')
    canvas.line(60, 457, 550, 457)  # horizontal

    canvas.line(262, 457, 262, 366)  # vertical MEDIO
    canvas.line(290, 457, 290, 392)  # vertical MEDIO
    canvas.line(318, 457, 318, 341)  # vertical MEDIO
    canvas.line(348, 457, 348, 392)  # vertical MEDIO
    canvas.line(377, 457, 377, 366)  # vertical MEDIO
    canvas.line(406, 457, 406, 392)  # vertical MEDIO
    canvas.line(435, 457, 435, 366)  # vertical MEDIO
    canvas.line(463, 457, 463, 392)  # vertical MEDIO
    canvas.line(492, 457, 492, 341)  # vertical MEDIO
    canvas.line(521, 457, 521, 392)  # vertical MEDIO
    canvas.drawString(65, 447, 'Numero de contenedor')
    canvas.drawString(268, 447, datos['datos_muestra_laboratorio'][3][0])
    canvas.drawString(295, 447, datos['datos_muestra_laboratorio'][3][1])
    canvas.drawString(328, 447, datos['datos_muestra_laboratorio'][3][2])
    canvas.drawString(355, 447, datos['datos_muestra_laboratorio'][3][3])
    canvas.drawString(388, 447, datos['datos_muestra_laboratorio'][3][4])
    canvas.drawString(420, 447, datos['datos_muestra_laboratorio'][3][5])
    canvas.drawString(445, 447, datos['datos_muestra_laboratorio'][3][6])
    canvas.drawString(470, 447, datos['datos_muestra_laboratorio'][3][7])
    canvas.drawString(502, 447, datos['datos_muestra_laboratorio'][3][8])
    canvas.drawString(530, 447, datos['datos_muestra_laboratorio'][3][9])
    # canvas.drawString(502, 447, datos['datos_muestra_laboratorio'][3][10])
    # canvas.drawString(530, 447, datos['datos_muestra_laboratorio'][3][11])

    canvas.line(60, 444, 550, 444)  ## horizontal
    canvas.drawString(65, 434, 'Masa recipiente (g) Mr')
    canvas.drawString(263, 434, datos['datos_muestra_laboratorio'][4][0][0])
    canvas.drawString(291, 434, datos['datos_muestra_laboratorio'][4][1][0])
    canvas.drawString(320, 434, datos['datos_muestra_laboratorio'][4][2][0])
    canvas.drawString(349, 434, datos['datos_muestra_laboratorio'][4][3][0])
    canvas.drawString(379, 434, datos['datos_muestra_laboratorio'][4][4][0])
    canvas.drawString(408, 434, datos['datos_muestra_laboratorio'][4][5][0])
    canvas.drawString(437, 434, datos['datos_muestra_laboratorio'][4][6][0])
    canvas.drawString(465, 434, datos['datos_muestra_laboratorio'][4][7][0])
    canvas.drawString(494, 434, datos['datos_muestra_laboratorio'][4][8][0])
    canvas.drawString(522, 434, datos['datos_muestra_laboratorio'][4][9][0])

    canvas.line(60, 431, 550, 431)  ## horizontal0-13
    canvas.drawString(65, 421, 'Masa del recipiente + suelo humedo')
    canvas.drawString(263, 421, datos['datos_muestra_laboratorio'][4][0][1])
    canvas.drawString(291, 421, datos['datos_muestra_laboratorio'][4][1][1])
    canvas.drawString(320, 421, datos['datos_muestra_laboratorio'][4][2][1])
    canvas.drawString(349, 421, datos['datos_muestra_laboratorio'][4][3][1])
    canvas.drawString(379, 421, datos['datos_muestra_laboratorio'][4][4][1])
    canvas.drawString(408, 421, datos['datos_muestra_laboratorio'][4][5][1])
    canvas.drawString(437, 421, datos['datos_muestra_laboratorio'][4][6][1])
    canvas.drawString(465, 421, datos['datos_muestra_laboratorio'][4][7][1])
    canvas.drawString(494, 421, datos['datos_muestra_laboratorio'][4][8][1])
    canvas.drawString(522, 421, datos['datos_muestra_laboratorio'][4][9][1])

    canvas.line(60, 418, 550, 418)  ## horizontal0-13
    canvas.drawString(65, 408, 'Masa del recipiente + suelo seco')
    canvas.drawString(263, 408, datos['datos_muestra_laboratorio'][4][0][2])
    canvas.drawString(291, 408, datos['datos_muestra_laboratorio'][4][1][2])
    canvas.drawString(320, 408, datos['datos_muestra_laboratorio'][4][2][2])
    canvas.drawString(349, 408, datos['datos_muestra_laboratorio'][4][3][2])
    canvas.drawString(379, 408, datos['datos_muestra_laboratorio'][4][4][2])
    canvas.drawString(408, 408, datos['datos_muestra_laboratorio'][4][5][2])
    canvas.drawString(437, 408, datos['datos_muestra_laboratorio'][4][6][2])
    canvas.drawString(465, 408, datos['datos_muestra_laboratorio'][4][7][2])
    canvas.drawString(494, 408, datos['datos_muestra_laboratorio'][4][8][2])
    canvas.drawString(522, 408, datos['datos_muestra_laboratorio'][4][9][2])

    canvas.line(60, 405, 550, 405)  ## horizontal0-13
    canvas.drawString(65, 395, 'Contenido de humedad w (%)')
    canvas.drawString(263, 395, str(datos['resultados_del_ensayo'][2][0][0]))
    canvas.drawString(291, 395, str(datos['resultados_del_ensayo'][2][0][1]))
    canvas.drawString(320, 395, str(datos['resultados_del_ensayo'][2][0][2]))
    canvas.drawString(349, 395, str(datos['resultados_del_ensayo'][2][0][3]))
    canvas.drawString(379, 395, str(datos['resultados_del_ensayo'][2][0][4]))
    canvas.drawString(408, 395, str(datos['resultados_del_ensayo'][2][0][5]))
    canvas.drawString(437, 395, str(datos['resultados_del_ensayo'][2][0][6]))
    canvas.drawString(465, 395, str(datos['resultados_del_ensayo'][2][0][7]))
    canvas.drawString(494, 395, str(datos['resultados_del_ensayo'][2][0][8]))
    canvas.drawString(522, 395, str(datos['resultados_del_ensayo'][2][0][9]))

    canvas.line(60, 392, 550, 392)  ## horizontal0-13
    canvas.drawString(65, 382, 'Humedad promedio w (%)')
    canvas.drawString(280, 382, str(datos['resultados_del_ensayo'][3][0]))
    canvas.drawString(340, 382, str(datos['resultados_del_ensayo'][3][1]))
    canvas.drawString(395, 382, str(datos['resultados_del_ensayo'][3][2]))
    canvas.drawString(450, 382, str(datos['resultados_del_ensayo'][3][3]))
    canvas.drawString(510, 382, str(datos['resultados_del_ensayo'][3][4]))

    canvas.line(60, 379, 550, 379)  ## horizontal0-13
    canvas.drawString(65, 369, 'Peso unitario seco yd kN/m3')
    canvas.drawString(280, 369, str(datos['resultados_del_ensayo'][4][0]))
    canvas.drawString(340, 369, str(datos['resultados_del_ensayo'][4][1]))
    canvas.drawString(395, 369, str(datos['resultados_del_ensayo'][4][2]))
    canvas.drawString(450, 369, str(datos['resultados_del_ensayo'][4][3]))
    canvas.drawString(510, 369, str(datos['resultados_del_ensayo'][4][4]))

    canvas.line(60, 366, 550, 366)  ## horizontal0-13
    canvas.drawString(320, 356, 'Peso unitario seco max yd kN/m3')
    canvas.drawString(510, 356, str(datos['resultados_del_ensayo'][5][0]))
    canvas.line(318, 353, 550, 353)  ## horizontal0-13
    canvas.drawString(320, 343, 'Contenido de humedad optimo w (%)')
    canvas.drawString(510, 343, str(datos['resultados_del_ensayo'][5][1]))
    canvas.line(318, 340, 550, 340)  ## horizontal0-13

    # # imagen ensayo
    canvas.drawImage("static/" + datos['direccion_de_grafico'], 80, 205, width=200, height=160)  # izquierda, abajo

    # observaciones
    canvas.drawString(80, 150, 'D. OBSERVACIONES')
    canvas.line(60, 140, 550, 140)  ## horizontal abajo9
    linea7 = 480
    # FIRMAS
    canvas.drawString(70, 95, 'Firma del jefe de carrera')
    canvas.drawString(420, 95, 'Firma del tecnico')
    canvas.line(puntoAx, puntoY - linea7 - 110, puntoMedio - 90, puntoY - linea7 - 110)
    canvas.line(puntoMedio + 80, puntoY - linea7 - 110, puntoBx, puntoY - linea7 - 110)

    # DATOS ACREDITACION
    linea8y = 70
    canvas.drawString(90, linea8y - 10, 'ELABORADO POR')
    canvas.drawString(260, linea8y - 10, 'REVISADO POR')
    canvas.drawString(420, linea8y - 10, 'APROBADO POR')

    canvas.line(puntoAx, linea8y, puntoBx, linea8y)
    linea8y = linea8y - 15
    canvas.line(puntoAx, linea8y, puntoBx, linea8y)
    linea8y = linea8y - 25
    canvas.line(puntoAx, linea8y, puntoBx, linea8y)
    canvas.line(puntoAx, linea8y + 40, puntoAx, linea8y)  # vertical
    canvas.line(puntoBx, linea8y + 40, puntoBx, linea8y)  # vertical
    canvas.line(puntoMedio - 90, linea8y + 40, puntoMedio - 90, linea8y)  # vertical
    canvas.line(puntoMedio + 90, linea8y + 40, puntoMedio + 90, linea8y)  # vertical

    # FIN COPIAR

    canvas.save()
    pdf_out = output.getvalue()

    output.close()
    filename = 'proctor_modificado_astm.pdf'
    response = make_response(pdf_out)
    response.headers['Content-Disposition'] = "attachment; filename"
    response.mimetype = 'application/pdf'
    # return response
    return send_file(filename, as_attachment=False)

# ######################################## PRPROCTOR_MODIFICADO AASHTO ######################################

def reporte_proctor_modificado_aashto2(datos_proctorMAASHTO):

    datos=datos_proctorMAASHTO[1]

    output = cStringIO.StringIO()
    canvas = Canvas("proctor_modificado_aashto2.pdf", pagesize=letter)
    canvas.setLineWidth(.3)
    canvas.setFont('Helvetica', 10)

    canvas.line(60, 760, 550, 760)  # punto x1, y1 , x2, y2 #HORIZONTAL
    canvas.line(60, 760, 60, 700)  # VERTICAL
    canvas.line(60, 700, 550, 700)  # HORIZONTAL
    canvas.line(550, 760, 550, 700)  # VERTICAL
    canvas.line(190, 760, 190, 700)  # VERTICAL
    canvas.line(400, 760, 400, 700)  # VERTICAL
    # CAJETIN PEQUENO
    canvas.line(400, 745, 550, 745)  # HORIZONTAL
    canvas.line(400, 730, 550, 730)  # HORIZONTAL
    canvas.line(400, 715, 550, 715)  # HORIZONTAL
    canvas.line(470, 760, 470, 715)  # VERTICAL
    canvas.drawImage("static/img/emi.jpeg", 70, 710, width=115, height=40)

    # TITULO
    frame1 = Frame(190, 700, 210, 60, showBoundary=1)  # Frame(movX,movY,margenAncho,mrgenAlto)
    bodyStyle = ParagraphStyle('normal', fontSize=30, leading=28, spaceBefore=30, alignment=TA_CENTER)
    s = datos_proctorMAASHTO[0]
    story = [Paragraph(s, bodyStyle)]
    story_inframe = KeepInFrame(210, 1 * inch, story)
    frame1.addFromList([story_inframe], canvas)
    # interlineado=740
    story = []
    # DATOS
    posx = 410
    canvas.setFont('Helvetica', 10)
    canvas.drawString(posx, 750, 'Codigo:')
    canvas.drawString(posx, 735, 'Aprobacion:')
    canvas.drawString(posx, 720, 'Version:')
    canvas.drawString(posx + 70, 750, 'C5117-9')
    canvas.drawString(posx + 70, 735, 'Aprobado')
    canvas.drawString(posx + 70, 720, 'Version 1.1')
    canvas.drawString(posx + 30, 703, 'Página 1 de 1')

    # SEGUNDA CAJETILLA
    puntoAx = 60
    puntoBx = 550
    puntoY = 698
    puntoMedio = (puntoAx + puntoBx) / 2

    canvas.line(60, 695, 550,
                695)  # horizontal arriba (largohacialaIZQUIERDA ,arribaIZQ , largo de la linea hacia la derecha ,arribaDER)
    canvas.setFont('Helvetica', 10)
    canvas.drawString(235, 680, 'A. DATOS GENRALES')  # (# ,  arriba , #)
    canvas.line(60, 700, 60,
                366)  # vertical iquierdo  (mover linea hacia derecha punto arriba, linea hacia arriba, mover linea hacia derecha punto abajo)
    canvas.line(550, 700, 550, 340)  # vertical DERECHO
    canvas.line(60, 678, 550, 678)  ## horizontal abajo

    # primero
    canvas.setFont('Helvetica', 9)
    canvas.drawString(160, 670, 'Proyecto')
    canvas.drawString(400, 670, 'Fecha')
    canvas.line(60, 668, 550, 668)  ## horizontal abajo2
    canvas.line(300, 678, 300, 607)  # vertical2 MEDIO
    canvas.setFont('Helvetica', 12)
    canvas.drawString(70, 657, datos['datos_generales'][0])
    canvas.drawString(310, 657, datos['datos_generales'][7])
    canvas.line(60, 655, 550, 655)  ## horizontal abajo3
    # segundo
    canvas.setFont('Helvetica', 9)
    canvas.drawString(160, 647, 'Ubicacion')
    canvas.drawString(400, 647, 'Laboratista')
    canvas.line(60, 645, 550, 645)  ## horizontal abajo4
    canvas.setFont('Helvetica', 12)
    canvas.drawString(70, 634, datos['datos_generales'][1])
    canvas.drawString(310, 634, datos['datos_generales'][4])
    canvas.line(60, 631, 550, 631)  ## horizontal abajo5

    # tercero
    canvas.setFont('Helvetica', 9)
    canvas.drawString(120, 623, 'Descripcion De La Muestra')
    canvas.drawString(380, 623, 'Tipo De Muestra')
    canvas.line(60, 620, 550, 620)  ## horizontal abajo6
    canvas.setFont('Helvetica', 12)
    canvas.drawString(70, 609, datos['datos_generales'][2])
    canvas.drawString(310, 609, datos['datos_generales'][3])
    canvas.line(60, 607, 550, 607)  ## horizontal abajo7

    # datos de calculo
    canvas.setFont('Helvetica', 10)
    canvas.drawString(235, 596, 'B. DATOS TECNICOS')
    canvas.line(60, 594, 550, 594)  ## horizontal
    canvas.line(280, 554, 280, 594)  # vertical MEDIO

    canvas.drawString(65, 583, 'Metodo utilizado')
    canvas.drawString(245, 583, datos['datos_muestra_laboratorio'][0][0])
    canvas.drawString(285, 583, "Diametro del molde (mm)")
    canvas.drawString(508, 583, datos['datos_muestra_laboratorio'][0][2])
    canvas.line(60, 580, 550, 580)  ## horizontal
    canvas.drawString(65, 570, 'Gravedad especifica')
    canvas.drawString(245, 570, datos['datos_muestra_laboratorio'][0][1])
    canvas.drawString(285, 570, "Altura del molde (mm)")
    canvas.drawString(508, 570, datos['datos_muestra_laboratorio'][0][3])
    canvas.line(60, 567, 550, 567)  ## horizontal
    canvas.drawString(65, 556, 'Volumen (cm3)')
    canvas.drawString(245, 556, datos['datos_muestra_laboratorio'][0][4])
    canvas.line(60, 554, 550, 554)  ## horizontal
    canvas.drawString(235, 543, 'C. PESO UNITARIO')
    canvas.line(60, 541, 550, 541)  ## horizontal
    canvas.line(325, 476, 325, 541)  # vertical MEDIO
    canvas.line(370, 476, 370, 541)  # vertical MEDIO
    canvas.line(415, 476, 415, 541)  # vertical MEDIO
    canvas.line(460, 476, 460, 541)  # vertical MEDIO
    canvas.line(505, 476, 505, 541)  # vertical MEDIO

    canvas.line(60, 528, 550, 528)  ## horizontal

    canvas.drawString(65, 531, 'Masa del agua (g) Mw')
    canvas.drawString(345, 531, "1")
    canvas.drawString(390, 531, "2")
    canvas.drawString(435, 531, "3")
    canvas.drawString(480, 531, "4")
    canvas.drawString(525, 531, "5")
    canvas.line(60, 515, 550, 515)  ## horizontal
    canvas.drawString(65, 518, 'Peso molde + suelo (g) M2')
    canvas.drawString(330, 518, datos['datos_muestra_laboratorio'][1][0])
    canvas.drawString(376, 518, datos['datos_muestra_laboratorio'][1][1])
    canvas.drawString(422, 518, datos['datos_muestra_laboratorio'][1][2])
    canvas.drawString(466, 518, datos['datos_muestra_laboratorio'][1][3])
    canvas.drawString(512, 518, datos['datos_muestra_laboratorio'][1][4])

    canvas.line(60, 502, 550, 502)  ## horizontal
    canvas.drawString(65, 505, 'Peso molde (g) M1')
    canvas.drawString(330, 505, datos['datos_muestra_laboratorio'][2][0])
    canvas.drawString(376, 505, datos['datos_muestra_laboratorio'][2][1])
    canvas.drawString(422, 505, datos['datos_muestra_laboratorio'][2][2])
    canvas.drawString(466, 505, datos['datos_muestra_laboratorio'][2][3])
    canvas.drawString(512, 505, datos['datos_muestra_laboratorio'][2][4])

    canvas.line(60, 489, 550, 489)  ## horizontal
    canvas.drawString(65, 492, 'Peso humedo del suelo (g) M')
    canvas.drawString(330, 492, str(datos['resultados_del_ensayo'][0][0]))
    canvas.drawString(376, 492, str(datos['resultados_del_ensayo'][0][1]))
    canvas.drawString(422, 492, str(datos['resultados_del_ensayo'][0][2]))
    canvas.drawString(466, 492, str(datos['resultados_del_ensayo'][0][3]))
    canvas.drawString(512, 492, str(datos['resultados_del_ensayo'][0][4]))

    canvas.line(60, 476, 550, 476)  ## horizontal
    canvas.drawString(65, 479, 'Peso humedo del suelo (g) M')
    canvas.drawString(330, 479, str(datos['resultados_del_ensayo'][1][0]))
    canvas.drawString(376, 479, str(datos['resultados_del_ensayo'][1][1]))
    canvas.drawString(422, 479, str(datos['resultados_del_ensayo'][1][2]))
    canvas.drawString(466, 479, str(datos['resultados_del_ensayo'][1][3]))
    canvas.drawString(512, 479, str(datos['resultados_del_ensayo'][1][4]))

    canvas.line(60, 470, 550, 470)  ## horizontal
    canvas.drawString(235, 460, 'D. CONTENIDO DE HUMEDAD')
    canvas.line(60, 457, 550, 457)  # horizontal

    canvas.line(262, 457, 262, 366)  # vertical MEDIO
    canvas.line(290, 457, 290, 392)  # vertical MEDIO
    canvas.line(318, 457, 318, 341)  # vertical MEDIO
    canvas.line(348, 457, 348, 392)  # vertical MEDIO
    canvas.line(377, 457, 377, 366)  # vertical MEDIO
    canvas.line(406, 457, 406, 392)  # vertical MEDIO
    canvas.line(435, 457, 435, 366)  # vertical MEDIO
    canvas.line(463, 457, 463, 392)  # vertical MEDIO
    canvas.line(492, 457, 492, 341)  # vertical MEDIO
    canvas.line(521, 457, 521, 392)  # vertical MEDIO
    canvas.drawString(65, 447, 'Numero de contenedor')
    canvas.drawString(268, 447, datos['datos_muestra_laboratorio'][3][0])
    canvas.drawString(295, 447, datos['datos_muestra_laboratorio'][3][1])
    canvas.drawString(328, 447, datos['datos_muestra_laboratorio'][3][2])
    canvas.drawString(355, 447, datos['datos_muestra_laboratorio'][3][3])
    canvas.drawString(388, 447, datos['datos_muestra_laboratorio'][3][4])
    canvas.drawString(420, 447, datos['datos_muestra_laboratorio'][3][5])
    canvas.drawString(445, 447, datos['datos_muestra_laboratorio'][3][6])
    canvas.drawString(470, 447, datos['datos_muestra_laboratorio'][3][7])
    canvas.drawString(502, 447, datos['datos_muestra_laboratorio'][3][8])
    canvas.drawString(530, 447, datos['datos_muestra_laboratorio'][3][9])
    # canvas.drawString(502, 447, datos['datos_muestra_laboratorio'][3][10])
    # canvas.drawString(530, 447, datos['datos_muestra_laboratorio'][3][11])

    canvas.line(60, 444, 550, 444)  ## horizontal
    canvas.drawString(65, 434, 'Masa recipiente (g) Mr')
    canvas.drawString(263, 434, datos['datos_muestra_laboratorio'][4][0][0])
    canvas.drawString(291, 434, datos['datos_muestra_laboratorio'][4][1][0])
    canvas.drawString(320, 434, datos['datos_muestra_laboratorio'][4][2][0])
    canvas.drawString(349, 434, datos['datos_muestra_laboratorio'][4][3][0])
    canvas.drawString(379, 434, datos['datos_muestra_laboratorio'][4][4][0])
    canvas.drawString(408, 434, datos['datos_muestra_laboratorio'][4][5][0])
    canvas.drawString(437, 434, datos['datos_muestra_laboratorio'][4][6][0])
    canvas.drawString(465, 434, datos['datos_muestra_laboratorio'][4][7][0])
    canvas.drawString(494, 434, datos['datos_muestra_laboratorio'][4][8][0])
    canvas.drawString(522, 434, datos['datos_muestra_laboratorio'][4][9][0])

    canvas.line(60, 431, 550, 431)  ## horizontal0-13
    canvas.drawString(65, 421, 'Masa del recipiente + suelo humedo')
    canvas.drawString(263, 421, datos['datos_muestra_laboratorio'][4][0][1])
    canvas.drawString(291, 421, datos['datos_muestra_laboratorio'][4][1][1])
    canvas.drawString(320, 421, datos['datos_muestra_laboratorio'][4][2][1])
    canvas.drawString(349, 421, datos['datos_muestra_laboratorio'][4][3][1])
    canvas.drawString(379, 421, datos['datos_muestra_laboratorio'][4][4][1])
    canvas.drawString(408, 421, datos['datos_muestra_laboratorio'][4][5][1])
    canvas.drawString(437, 421, datos['datos_muestra_laboratorio'][4][6][1])
    canvas.drawString(465, 421, datos['datos_muestra_laboratorio'][4][7][1])
    canvas.drawString(494, 421, datos['datos_muestra_laboratorio'][4][8][1])
    canvas.drawString(522, 421, datos['datos_muestra_laboratorio'][4][9][1])

    canvas.line(60, 418, 550, 418)  ## horizontal0-13
    canvas.drawString(65, 408, 'Masa del recipiente + suelo seco')
    canvas.drawString(263, 408, datos['datos_muestra_laboratorio'][4][0][2])
    canvas.drawString(291, 408, datos['datos_muestra_laboratorio'][4][1][2])
    canvas.drawString(320, 408, datos['datos_muestra_laboratorio'][4][2][2])
    canvas.drawString(349, 408, datos['datos_muestra_laboratorio'][4][3][2])
    canvas.drawString(379, 408, datos['datos_muestra_laboratorio'][4][4][2])
    canvas.drawString(408, 408, datos['datos_muestra_laboratorio'][4][5][2])
    canvas.drawString(437, 408, datos['datos_muestra_laboratorio'][4][6][2])
    canvas.drawString(465, 408, datos['datos_muestra_laboratorio'][4][7][2])
    canvas.drawString(494, 408, datos['datos_muestra_laboratorio'][4][8][2])
    canvas.drawString(522, 408, datos['datos_muestra_laboratorio'][4][9][2])

    canvas.line(60, 405, 550, 405)  ## horizontal0-13
    canvas.drawString(65, 395, 'Contenido de humedad w (%)')
    canvas.drawString(263, 395, str(datos['resultados_del_ensayo'][2][0][0]))
    canvas.drawString(291, 395, str(datos['resultados_del_ensayo'][2][0][1]))
    canvas.drawString(320, 395, str(datos['resultados_del_ensayo'][2][0][2]))
    canvas.drawString(349, 395, str(datos['resultados_del_ensayo'][2][0][3]))
    canvas.drawString(379, 395, str(datos['resultados_del_ensayo'][2][0][4]))
    canvas.drawString(408, 395, str(datos['resultados_del_ensayo'][2][0][5]))
    canvas.drawString(437, 395, str(datos['resultados_del_ensayo'][2][0][6]))
    canvas.drawString(465, 395, str(datos['resultados_del_ensayo'][2][0][7]))
    canvas.drawString(494, 395, str(datos['resultados_del_ensayo'][2][0][8]))
    canvas.drawString(522, 395, str(datos['resultados_del_ensayo'][2][0][9]))

    canvas.line(60, 392, 550, 392)  ## horizontal0-13
    canvas.drawString(65, 382, 'Humedad promedio w (%)')
    canvas.drawString(280, 382, str(datos['resultados_del_ensayo'][3][0]))
    canvas.drawString(340, 382, str(datos['resultados_del_ensayo'][3][1]))
    canvas.drawString(395, 382, str(datos['resultados_del_ensayo'][3][2]))
    canvas.drawString(450, 382, str(datos['resultados_del_ensayo'][3][3]))
    canvas.drawString(510, 382, str(datos['resultados_del_ensayo'][3][4]))

    canvas.line(60, 379, 550, 379)  ## horizontal0-13
    canvas.drawString(65, 369, 'Peso unitario seco yd kN/m3')
    canvas.drawString(280, 369, str(datos['resultados_del_ensayo'][4][0]))
    canvas.drawString(340, 369, str(datos['resultados_del_ensayo'][4][1]))
    canvas.drawString(395, 369, str(datos['resultados_del_ensayo'][4][2]))
    canvas.drawString(450, 369, str(datos['resultados_del_ensayo'][4][3]))
    canvas.drawString(510, 369, str(datos['resultados_del_ensayo'][4][4]))

    canvas.line(60, 366, 550, 366)  ## horizontal0-13
    canvas.drawString(320, 356, 'Peso unitario seco max yd kN/m3')
    canvas.drawString(510, 356, str(datos['resultados_del_ensayo'][5][0]))
    canvas.line(318, 353, 550, 353)  ## horizontal0-13
    canvas.drawString(320, 343, 'Contenido de humedad optimo w (%)')
    canvas.drawString(510, 343, str(datos['resultados_del_ensayo'][5][1]))
    canvas.line(318, 340, 550, 340)  ## horizontal0-13

    # # imagen ensayo
    canvas.drawImage("static/" + datos['direccion_de_grafico'], 80, 205, width=200, height=160)  # izquierda, abajo

    # observaciones
    canvas.drawString(80, 150, 'D. OBSERVACIONES')
    canvas.line(60, 140, 550, 140)  ## horizontal abajo9
    linea7 = 480
    # FIRMAS
    canvas.drawString(70, 95, 'Firma del jefe de carrera')
    canvas.drawString(420, 95, 'Firma del tecnico')
    canvas.line(puntoAx, puntoY - linea7 - 110, puntoMedio - 90, puntoY - linea7 - 110)
    canvas.line(puntoMedio + 80, puntoY - linea7 - 110, puntoBx, puntoY - linea7 - 110)

    # DATOS ACREDITACION
    linea8y = 70
    canvas.drawString(90, linea8y - 10, 'ELABORADO POR')
    canvas.drawString(260, linea8y - 10, 'REVISADO POR')
    canvas.drawString(420, linea8y - 10, 'APROBADO POR')

    canvas.line(puntoAx, linea8y, puntoBx, linea8y)
    linea8y = linea8y - 15
    canvas.line(puntoAx, linea8y, puntoBx, linea8y)
    linea8y = linea8y - 25
    canvas.line(puntoAx, linea8y, puntoBx, linea8y)
    canvas.line(puntoAx, linea8y + 40, puntoAx, linea8y)  # vertical
    canvas.line(puntoBx, linea8y + 40, puntoBx, linea8y)  # vertical
    canvas.line(puntoMedio - 90, linea8y + 40, puntoMedio - 90, linea8y)  # vertical
    canvas.line(puntoMedio + 90, linea8y + 40, puntoMedio + 90, linea8y)  # vertical

    # FIN COPIAR

    canvas.save()
    pdf_out = output.getvalue()

    output.close()
    filename = 'proctor_modificado_aashto2.pdf'
    response = make_response(pdf_out)
    response.headers['Content-Disposition'] = "attachment; filename"
    response.mimetype = 'application/pdf'
    # return response
    return send_file(filename, as_attachment=False)



# ######################################## PRPROCTOR_ESTANDAR AASHTO ######################################

def reporte_proctor_estandar_aashto2(datos_proctorEAASHTO):
    datos=datos_proctorEAASHTO[1]

    output = cStringIO.StringIO()
    canvas = Canvas("proctor_estandar_aashto.pdf", pagesize=letter)
    canvas.setLineWidth(.3)
    canvas.setFont('Helvetica', 10)

    canvas.line(60, 760, 550, 760)  # punto x1, y1 , x2, y2 #HORIZONTAL
    canvas.line(60, 760, 60, 700)  # VERTICAL
    canvas.line(60, 700, 550, 700)  # HORIZONTAL
    canvas.line(550, 760, 550, 700)  # VERTICAL
    canvas.line(190, 760, 190, 700)  # VERTICAL
    canvas.line(400, 760, 400, 700)  # VERTICAL
    # CAJETIN PEQUENO
    canvas.line(400, 745, 550, 745)  # HORIZONTAL
    canvas.line(400, 730, 550, 730)  # HORIZONTAL
    canvas.line(400, 715, 550, 715)  # HORIZONTAL
    canvas.line(470, 760, 470, 715)  # VERTICAL
    canvas.drawImage("static/img/emi.jpeg", 70, 710, width=115, height=40)

    # TITULO
    frame1 = Frame(190, 700, 210, 60, showBoundary=1)  # Frame(movX,movY,margenAncho,mrgenAlto)
    bodyStyle = ParagraphStyle('normal', fontSize=30, leading=28, spaceBefore=30, alignment=TA_CENTER)
    s = datos_proctorEAASHTO[0]
    story = [Paragraph(s, bodyStyle)]
    story_inframe = KeepInFrame(210, 1 * inch, story)
    frame1.addFromList([story_inframe], canvas)
    # interlineado=740
    story = []
    # DATOS
    posx = 410
    canvas.setFont('Helvetica', 10)
    canvas.drawString(posx, 750, 'Codigo:')
    canvas.drawString(posx, 735, 'Aprobacion:')
    canvas.drawString(posx, 720, 'Version:')
    canvas.drawString(posx + 70, 750, 'C5117-9')
    canvas.drawString(posx + 70, 735, 'Aprobado')
    canvas.drawString(posx + 70, 720, 'Version 1.1')
    canvas.drawString(posx + 30, 703, 'Página 1 de 1')

    # SEGUNDA CAJETILLA
    puntoAx = 60
    puntoBx = 550
    puntoY = 698
    puntoMedio = (puntoAx + puntoBx) / 2

    canvas.line(60, 695, 550,
                695)  # horizontal arriba (largohacialaIZQUIERDA ,arribaIZQ , largo de la linea hacia la derecha ,arribaDER)
    canvas.setFont('Helvetica', 10)
    canvas.drawString(235, 680, 'A. DATOS GENRALES')  # (# ,  arriba , #)
    canvas.line(60, 700, 60,
                366)  # vertical iquierdo  (mover linea hacia derecha punto arriba, linea hacia arriba, mover linea hacia derecha punto abajo)
    canvas.line(550, 700, 550, 340)  # vertical DERECHO
    canvas.line(60, 678, 550, 678)  ## horizontal abajo

    # primero
    canvas.setFont('Helvetica', 9)
    canvas.drawString(160, 670, 'Proyecto')
    canvas.drawString(400, 670, 'Fecha')
    canvas.line(60, 668, 550, 668)  ## horizontal abajo2
    canvas.line(300, 678, 300, 607)  # vertical2 MEDIO
    canvas.setFont('Helvetica', 12)
    canvas.drawString(70, 657, datos['datos_generales'][0])
    canvas.drawString(310, 657, datos['datos_generales'][7])
    canvas.line(60, 655, 550, 655)  ## horizontal abajo3
    # segundo
    canvas.setFont('Helvetica', 9)
    canvas.drawString(160, 647, 'Ubicacion')
    canvas.drawString(400, 647, 'Laboratista')
    canvas.line(60, 645, 550, 645)  ## horizontal abajo4
    canvas.setFont('Helvetica', 12)
    canvas.drawString(70, 634, datos['datos_generales'][1])
    canvas.drawString(310, 634, datos['datos_generales'][4])
    canvas.line(60, 631, 550, 631)  ## horizontal abajo5

    # tercero
    canvas.setFont('Helvetica', 9)
    canvas.drawString(120, 623, 'Descripcion De La Muestra')
    canvas.drawString(380, 623, 'Tipo De Muestra')
    canvas.line(60, 620, 550, 620)  ## horizontal abajo6
    canvas.setFont('Helvetica', 12)
    canvas.drawString(70, 609, datos['datos_generales'][2])
    canvas.drawString(310, 609, datos['datos_generales'][3])
    canvas.line(60, 607, 550, 607)  ## horizontal abajo7

    # datos de calculo
    canvas.setFont('Helvetica', 10)
    canvas.drawString(235, 596, 'B. DATOS TECNICOS')
    canvas.line(60, 594, 550, 594)  ## horizontal
    canvas.line(280, 554, 280, 594)  # vertical MEDIO

    canvas.drawString(65, 583, 'Metodo utilizado')
    canvas.drawString(245, 583, datos['datos_muestra_laboratorio'][0][0])
    canvas.drawString(285, 583, "Diametro del molde (mm)")
    canvas.drawString(508, 583, datos['datos_muestra_laboratorio'][0][2])
    canvas.line(60, 580, 550, 580)  ## horizontal
    canvas.drawString(65, 570, 'Gravedad especifica')
    canvas.drawString(245, 570, datos['datos_muestra_laboratorio'][0][1])
    canvas.drawString(285, 570, "Altura del molde (mm)")
    canvas.drawString(508, 570, datos['datos_muestra_laboratorio'][0][3])
    canvas.line(60, 567, 550, 567)  ## horizontal
    canvas.drawString(65, 556, 'Volumen (cm3)')
    canvas.drawString(245, 556, datos['datos_muestra_laboratorio'][0][4])
    canvas.line(60, 554, 550, 554)  ## horizontal
    canvas.drawString(235, 543, 'C. PESO UNITARIO')
    canvas.line(60, 541, 550, 541)  ## horizontal
    canvas.line(325, 476, 325, 541)  # vertical MEDIO
    canvas.line(370, 476, 370, 541)  # vertical MEDIO
    canvas.line(415, 476, 415, 541)  # vertical MEDIO
    canvas.line(460, 476, 460, 541)  # vertical MEDIO
    canvas.line(505, 476, 505, 541)  # vertical MEDIO

    canvas.line(60, 528, 550, 528)  ## horizontal

    canvas.drawString(65, 531, 'Masa del agua (g) Mw')
    canvas.drawString(345, 531, "1")
    canvas.drawString(390, 531, "2")
    canvas.drawString(435, 531, "3")
    canvas.drawString(480, 531, "4")
    canvas.drawString(525, 531, "5")
    canvas.line(60, 515, 550, 515)  ## horizontal
    canvas.drawString(65, 518, 'Peso molde + suelo (g) M2')
    canvas.drawString(330, 518, datos['datos_muestra_laboratorio'][1][0])
    canvas.drawString(376, 518, datos['datos_muestra_laboratorio'][1][1])
    canvas.drawString(422, 518, datos['datos_muestra_laboratorio'][1][2])
    canvas.drawString(466, 518, datos['datos_muestra_laboratorio'][1][3])
    canvas.drawString(512, 518, datos['datos_muestra_laboratorio'][1][4])

    canvas.line(60, 502, 550, 502)  ## horizontal
    canvas.drawString(65, 505, 'Peso molde (g) M1')
    canvas.drawString(330, 505, datos['datos_muestra_laboratorio'][2][0])
    canvas.drawString(376, 505, datos['datos_muestra_laboratorio'][2][1])
    canvas.drawString(422, 505, datos['datos_muestra_laboratorio'][2][2])
    canvas.drawString(466, 505, datos['datos_muestra_laboratorio'][2][3])
    canvas.drawString(512, 505, datos['datos_muestra_laboratorio'][2][4])

    canvas.line(60, 489, 550, 489)  ## horizontal
    canvas.drawString(65, 492, 'Peso humedo del suelo (g) M')
    canvas.drawString(330, 492, str(datos['resultados_del_ensayo'][0][0]))
    canvas.drawString(376, 492, str(datos['resultados_del_ensayo'][0][1]))
    canvas.drawString(422, 492, str(datos['resultados_del_ensayo'][0][2]))
    canvas.drawString(466, 492, str(datos['resultados_del_ensayo'][0][3]))
    canvas.drawString(512, 492, str(datos['resultados_del_ensayo'][0][4]))

    canvas.line(60, 476, 550, 476)  ## horizontal
    canvas.drawString(65, 479, 'Peso humedo del suelo (g) M')
    canvas.drawString(330, 479, str(datos['resultados_del_ensayo'][1][0]))
    canvas.drawString(376, 479, str(datos['resultados_del_ensayo'][1][1]))
    canvas.drawString(422, 479, str(datos['resultados_del_ensayo'][1][2]))
    canvas.drawString(466, 479, str(datos['resultados_del_ensayo'][1][3]))
    canvas.drawString(512, 479, str(datos['resultados_del_ensayo'][1][4]))

    canvas.line(60, 470, 550, 470)  ## horizontal
    canvas.drawString(235, 460, 'D. CONTENIDO DE HUMEDAD')
    canvas.line(60, 457, 550, 457)  # horizontal

    canvas.line(262, 457, 262, 366)  # vertical MEDIO
    canvas.line(290, 457, 290, 392)  # vertical MEDIO
    canvas.line(318, 457, 318, 341)  # vertical MEDIO
    canvas.line(348, 457, 348, 392)  # vertical MEDIO
    canvas.line(377, 457, 377, 366)  # vertical MEDIO
    canvas.line(406, 457, 406, 392)  # vertical MEDIO
    canvas.line(435, 457, 435, 366)  # vertical MEDIO
    canvas.line(463, 457, 463, 392)  # vertical MEDIO
    canvas.line(492, 457, 492, 341)  # vertical MEDIO
    canvas.line(521, 457, 521, 392)  # vertical MEDIO
    canvas.drawString(65, 447, 'Numero de contenedor')
    canvas.drawString(268, 447, datos['datos_muestra_laboratorio'][3][0])
    canvas.drawString(295, 447, datos['datos_muestra_laboratorio'][3][1])
    canvas.drawString(328, 447, datos['datos_muestra_laboratorio'][3][2])
    canvas.drawString(355, 447, datos['datos_muestra_laboratorio'][3][3])
    canvas.drawString(388, 447, datos['datos_muestra_laboratorio'][3][4])
    canvas.drawString(420, 447, datos['datos_muestra_laboratorio'][3][5])
    canvas.drawString(445, 447, datos['datos_muestra_laboratorio'][3][6])
    canvas.drawString(470, 447, datos['datos_muestra_laboratorio'][3][7])
    canvas.drawString(502, 447, datos['datos_muestra_laboratorio'][3][8])
    canvas.drawString(530, 447, datos['datos_muestra_laboratorio'][3][9])


    canvas.line(60, 444, 550, 444)  ## horizontal
    canvas.drawString(65, 434, 'Masa recipiente (g) Mr')
    canvas.drawString(263, 434, datos['datos_muestra_laboratorio'][4][0][0])
    canvas.drawString(291, 434, datos['datos_muestra_laboratorio'][4][1][0])
    canvas.drawString(320, 434, datos['datos_muestra_laboratorio'][4][2][0])
    canvas.drawString(349, 434, datos['datos_muestra_laboratorio'][4][3][0])
    canvas.drawString(379, 434, datos['datos_muestra_laboratorio'][4][4][0])
    canvas.drawString(408, 434, datos['datos_muestra_laboratorio'][4][5][0])
    canvas.drawString(437, 434, datos['datos_muestra_laboratorio'][4][6][0])
    canvas.drawString(465, 434, datos['datos_muestra_laboratorio'][4][7][0])
    canvas.drawString(494, 434, datos['datos_muestra_laboratorio'][4][8][0])
    canvas.drawString(522, 434, datos['datos_muestra_laboratorio'][4][9][0])

    canvas.line(60, 431, 550, 431)  ## horizontal0-13
    canvas.drawString(65, 421, 'Masa del recipiente + suelo humedo')
    canvas.drawString(263, 421, datos['datos_muestra_laboratorio'][4][0][1])
    canvas.drawString(291, 421, datos['datos_muestra_laboratorio'][4][1][1])
    canvas.drawString(320, 421, datos['datos_muestra_laboratorio'][4][2][1])
    canvas.drawString(349, 421, datos['datos_muestra_laboratorio'][4][3][1])
    canvas.drawString(379, 421, datos['datos_muestra_laboratorio'][4][4][1])
    canvas.drawString(408, 421, datos['datos_muestra_laboratorio'][4][5][1])
    canvas.drawString(437, 421, datos['datos_muestra_laboratorio'][4][6][1])
    canvas.drawString(465, 421, datos['datos_muestra_laboratorio'][4][7][1])
    canvas.drawString(494, 421, datos['datos_muestra_laboratorio'][4][8][1])
    canvas.drawString(522, 421, datos['datos_muestra_laboratorio'][4][9][1])

    canvas.line(60, 418, 550, 418)  ## horizontal0-13
    canvas.drawString(65, 408, 'Masa del recipiente + suelo seco')
    canvas.drawString(263, 408, datos['datos_muestra_laboratorio'][4][0][2])
    canvas.drawString(291, 408, datos['datos_muestra_laboratorio'][4][1][2])
    canvas.drawString(320, 408, datos['datos_muestra_laboratorio'][4][2][2])
    canvas.drawString(349, 408, datos['datos_muestra_laboratorio'][4][3][2])
    canvas.drawString(379, 408, datos['datos_muestra_laboratorio'][4][4][2])
    canvas.drawString(408, 408, datos['datos_muestra_laboratorio'][4][5][2])
    canvas.drawString(437, 408, datos['datos_muestra_laboratorio'][4][6][2])
    canvas.drawString(465, 408, datos['datos_muestra_laboratorio'][4][7][2])
    canvas.drawString(494, 408, datos['datos_muestra_laboratorio'][4][8][2])
    canvas.drawString(522, 408, datos['datos_muestra_laboratorio'][4][9][2])

    canvas.line(60, 405, 550, 405)  ## horizontal0-13
    canvas.drawString(65, 395, 'Contenido de humedad w (%)')
    canvas.drawString(263, 395, str(datos['resultados_del_ensayo'][2][0][0]))
    canvas.drawString(291, 395, str(datos['resultados_del_ensayo'][2][0][1]))
    canvas.drawString(320, 395, str(datos['resultados_del_ensayo'][2][0][2]))
    canvas.drawString(349, 395, str(datos['resultados_del_ensayo'][2][0][3]))
    canvas.drawString(379, 395, str(datos['resultados_del_ensayo'][2][0][4]))
    canvas.drawString(408, 395, str(datos['resultados_del_ensayo'][2][0][5]))
    canvas.drawString(437, 395, str(datos['resultados_del_ensayo'][2][0][6]))
    canvas.drawString(465, 395, str(datos['resultados_del_ensayo'][2][0][7]))
    canvas.drawString(494, 395, str(datos['resultados_del_ensayo'][2][0][8]))
    canvas.drawString(522, 395, str(datos['resultados_del_ensayo'][2][0][9]))

    canvas.line(60, 392, 550, 392)  ## horizontal0-13
    canvas.drawString(65, 382, 'Humedad promedio w (%)')
    canvas.drawString(280, 382, str(datos['resultados_del_ensayo'][3][0]))
    canvas.drawString(340, 382, str(datos['resultados_del_ensayo'][3][1]))
    canvas.drawString(395, 382, str(datos['resultados_del_ensayo'][3][2]))
    canvas.drawString(450, 382, str(datos['resultados_del_ensayo'][3][3]))
    canvas.drawString(510, 382, str(datos['resultados_del_ensayo'][3][4]))

    canvas.line(60, 379, 550, 379)  ## horizontal0-13
    canvas.drawString(65, 369, 'Peso unitario seco yd kN/m3')
    canvas.drawString(280, 369, str(datos['resultados_del_ensayo'][4][0]))
    canvas.drawString(340, 369, str(datos['resultados_del_ensayo'][4][1]))
    canvas.drawString(395, 369, str(datos['resultados_del_ensayo'][4][2]))
    canvas.drawString(450, 369, str(datos['resultados_del_ensayo'][4][3]))
    canvas.drawString(510, 369, str(datos['resultados_del_ensayo'][4][4]))

    canvas.line(60, 366, 550, 366)  ## horizontal0-13
    canvas.drawString(320, 356, 'Peso unitario seco max yd kN/m3')
    canvas.drawString(510, 356, str(datos['resultados_del_ensayo'][5][0]))
    canvas.line(318, 353, 550, 353)  ## horizontal0-13
    canvas.drawString(320, 343, 'Contenido de humedad optimo w (%)')
    canvas.drawString(510, 343, str(datos['resultados_del_ensayo'][5][1]))
    canvas.line(318, 340, 550, 340)  ## horizontal0-13

    # # imagen ensayo
    canvas.drawImage("static/" + datos['direccion_de_grafico'], 80, 205, width=200, height=160)  # izquierda, abajo

    # observaciones
    canvas.drawString(80, 150, 'D. OBSERVACIONES')
    canvas.line(60, 140, 550, 140)  ## horizontal abajo9
    linea7 = 480
    # FIRMAS
    canvas.drawString(70, 95, 'Firma del jefe de carrera')
    canvas.drawString(420, 95, 'Firma del tecnico')
    canvas.line(puntoAx, puntoY - linea7 - 110, puntoMedio - 90, puntoY - linea7 - 110)
    canvas.line(puntoMedio + 80, puntoY - linea7 - 110, puntoBx, puntoY - linea7 - 110)

    # DATOS ACREDITACION
    linea8y = 70
    canvas.drawString(90, linea8y - 10, 'ELABORADO POR')
    canvas.drawString(260, linea8y - 10, 'REVISADO POR')
    canvas.drawString(420, linea8y - 10, 'APROBADO POR')

    canvas.line(puntoAx, linea8y, puntoBx, linea8y)
    linea8y = linea8y - 15
    canvas.line(puntoAx, linea8y, puntoBx, linea8y)
    linea8y = linea8y - 25
    canvas.line(puntoAx, linea8y, puntoBx, linea8y)
    canvas.line(puntoAx, linea8y + 40, puntoAx, linea8y)  # vertical
    canvas.line(puntoBx, linea8y + 40, puntoBx, linea8y)  # vertical
    canvas.line(puntoMedio - 90, linea8y + 40, puntoMedio - 90, linea8y)  # vertical
    canvas.line(puntoMedio + 90, linea8y + 40, puntoMedio + 90, linea8y)  # vertical

    # FIN COPIAR

    canvas.save()
    pdf_out = output.getvalue()

    output.close()
    filename = 'proctor_estandar_aashto.pdf'
    response = make_response(pdf_out)
    response.headers['Content-Disposition'] = "attachment; filename"
    response.mimetype = 'application/pdf'
    # return response
    return send_file(filename, as_attachment=False)




###################################### RPCONO_DE_ARENA ASTM ########################################################
def reporte_cono_de_arena2(datos_cono_astm):
    datos=datos_cono_astm[1]
    output = cStringIO.StringIO()
    canvas = Canvas("cono_de_arena_astm.pdf", pagesize=letter)
    canvas.setLineWidth(.3)
    canvas.setFont('Helvetica', 10)

    canvas.line(60, 760, 550, 760)  # punto x1, y1 , x2, y2 #HORIZONTAL
    canvas.line(60, 760, 60, 700)  # VERTICAL
    canvas.line(60, 700, 550, 700)  # HORIZONTAL
    canvas.line(550, 760, 550, 700)  # VERTICAL
    canvas.line(190, 760, 190, 700)  # VERTICAL
    canvas.line(400, 760, 400, 700)  # VERTICAL
    # CAJETIN PEQUENO
    canvas.line(400, 745, 550, 745)  # HORIZONTAL
    canvas.line(400, 730, 550, 730)  # HORIZONTAL
    canvas.line(400, 715, 550, 715)  # HORIZONTAL
    canvas.line(470, 760, 470, 715)  # VERTICAL

    canvas.drawImage("static/img/emi.jpeg", 70, 710, width=115, height=40)

    # TITULO
    frame1 = Frame(190, 700, 210, 60, showBoundary=1)  # Frame(movX,movY,margenAncho,mrgenAlto)
    bodyStyle = ParagraphStyle('normal', fontSize=24, leading=28, spaceBefore=30, alignment=TA_CENTER)
    s = datos_cono_astm[0]
    story = [Paragraph(s, bodyStyle)]
    story_inframe = KeepInFrame(210, 1 * inch, story)
    frame1.addFromList([story_inframe], canvas)
    # interlineado=740

    # DATOS
    posx = 410
    canvas.setFont('Helvetica', 10)
    canvas.drawString(posx, 750, 'Codigo:')
    canvas.drawString(posx, 735, 'Aprobacion:')
    canvas.drawString(posx, 720, 'Version:')
    canvas.drawString(posx + 70, 750, 'C5102-0')
    canvas.drawString(posx + 70, 735, 'Aprobado')
    canvas.drawString(posx + 70, 720, 'Version 1.1')
    canvas.drawString(posx + 30, 703, 'Página 1 de 1')

    # SEGUNDA CAJETILLA
    puntoAx = 60
    puntoBx = 550
    puntoY = 698
    puntoMedio = (puntoAx + puntoBx) / 2

    canvas.line(60, 680, 550,
                680)  # horizontal arriba (largohacialaIZQUIERDA ,arribaIZQ , largo de la linea hacia la derecha ,arribaDER)
    canvas.setFont('Helvetica', 12)
    canvas.drawString(235, 665, 'A. DATOS GENRALES')  # (# ,  arriba , #)
    canvas.line(60, 680, 60,
                568)  # vertical iquierdo  (mover linea hacia derecha punto arriba, linea hacia arriba, mover linea hacia derecha punto abajo)
    canvas.line(550, 680, 550, 568)  # vertical DERECHO
    canvas.line(60, 661, 550, 661)  ## horizontal abajo
    # primero
    canvas.setFont('Helvetica', 9)
    canvas.drawString(160, 651, 'Proyecto')
    canvas.line(60, 649, 550, 649)  ## horizontal abajo2
    canvas.line(300, 660, 300, 568)  # vertical2 MEDIO
    canvas.drawString(400, 651, 'Fecha')
    canvas.setFont('Helvetica', 12)
    canvas.drawString(70, 633, datos['datos_generales'][0])
    canvas.drawString(310, 633, datos['datos_generales'][7])
    canvas.line(60, 630, 550, 630)  ## horizontal abajo3
    # segundo
    canvas.setFont('Helvetica', 9)
    canvas.drawString(160, 620, 'Ubicacion')
    canvas.drawString(400, 620, 'Laboratista')
    canvas.line(60, 618, 550, 618)  ## horizontal abajo4
    canvas.line(60, 599, 550, 599)  ## horizontal abajo5
    canvas.setFont('Helvetica', 12)
    canvas.drawString(70, 602, datos['datos_generales'][1])
    canvas.drawString(310, 602, datos['datos_generales'][4])

    # tercero
    canvas.setFont('Helvetica', 9)
    canvas.drawString(120, 589, 'Descripcion De La Muestra')
    canvas.drawString(380, 589, 'Tipo De Muestra')
    canvas.line(60, 587, 550, 587)  ## horizontal abajo6
    canvas.line(60, 568, 550, 568)  ## horizontal abajo7
    canvas.setFont('Helvetica', 12)
    canvas.drawString(70, 571, datos['datos_generales'][2])
    canvas.drawString(310, 571, datos['datos_generales'][3])

    # # tabla calculos
    for i in range(34):
        canvas.line(60, 560 - i * 13, 550, 560 - i * 13)  ## horizontal

    canvas.line(60, 560, 60, 131)  # vertical iquierdo
    canvas.line(550, 560, 550, 131)  # vertical DERECHO
    # ****************** datos tecnicos ********************************
    canvas.line(480, 547, 480, 404)  # vertical DERECHO medio1
    canvas.line(410, 547, 410, 404)  # vertical DERECHO medio2
    canvas.line(340, 547, 340, 404)  # vertical DERECHO medio3
    canvas.line(270, 547, 270, 404)  # vertical DERECHO medio4
    # **************** contenido de humedad **************************
    canvas.line(480, 391, 480, 326)  # vertical DERECHO medio1
    canvas.line(410, 391, 410, 326)  # vertical DERECHO medio2
    canvas.line(340, 391, 340, 326)  # vertical DERECHO medio3
    canvas.line(270, 391, 270, 326)  # vertical DERECHO medio4

    # ************** densidad ***************************************
    canvas.line(480, 313, 480, 131)  # vertical DERECHO medio1
    canvas.line(410, 313, 410, 131)  # vertical DERECHO medio2
    canvas.line(340, 313, 340, 131)  # vertical DERECHO medio3
    canvas.line(270, 313, 270, 131)  # vertical DERECHO medio4

    canvas.setFont('Helvetica', 9)
    canvas.drawString(260, 550, 'B. DATOS TECNICOS')

    # ****************** titulos ***********************************
    canvas.drawString(65, 538, 'Numero de solicitud')
    canvas.drawString(65, 524, 'Fecha solicitada')
    canvas.drawString(65, 510, 'Material procedente')
    canvas.drawString(65, 497, 'Progresiva')
    canvas.drawString(65, 484, 'Lado')
    canvas.drawString(65, 471, 'Tramo ejecutado inicio')
    canvas.drawString(65, 458, 'Tramo ejecutado final')
    canvas.drawString(65, 445, 'Fecha de ejecución')
    canvas.drawString(65, 432, 'Capa')
    canvas.drawString(65, 419, 'Progresisva del ensayo')
    canvas.drawString(65, 406, 'Lado')
    # ***************** datos 1 ********************************************
    canvas.drawString(295, 538, str(datos['datos_muestra_laboratorio'][0][0][0]))
    canvas.drawString(275, 524, str(datos['datos_muestra_laboratorio'][0][0][1]))
    canvas.drawString(271, 510, str(datos['datos_muestra_laboratorio'][0][0][2]))
    canvas.drawString(275, 497, str(datos['datos_muestra_laboratorio'][0][0][3]) + '+' + str(
        datos['datos_muestra_laboratorio'][0][0][4]))
    canvas.drawString(275, 484, str(datos['datos_muestra_laboratorio'][0][0][5]))
    canvas.drawString(275, 471, str(datos['datos_muestra_laboratorio'][0][0][6]) + '+' + str(
        datos['datos_muestra_laboratorio'][0][0][7]))
    canvas.drawString(275, 458, str(datos['datos_muestra_laboratorio'][0][0][8]) + '+' + str(
        datos['datos_muestra_laboratorio'][0][0][9]))
    canvas.drawString(275, 445, str(datos['datos_muestra_laboratorio'][0][0][10]))
    canvas.drawString(275, 432, str(datos['datos_muestra_laboratorio'][0][0][11]))
    canvas.drawString(275, 419, str(datos['datos_muestra_laboratorio'][0][0][12]) + '+' + str(
        datos['datos_muestra_laboratorio'][0][0][13]))
    canvas.drawString(275, 406, str(datos['datos_muestra_laboratorio'][0][0][14]))

    # ***************** datos 2 ********************************************
    canvas.drawString(355, 538, str(datos['datos_muestra_laboratorio'][0][1][0]))
    canvas.drawString(345, 524, str(datos['datos_muestra_laboratorio'][0][1][1]))
    canvas.drawString(342, 510, str(datos['datos_muestra_laboratorio'][0][1][2]))
    canvas.drawString(345, 497, str(datos['datos_muestra_laboratorio'][0][1][3]) + '+' + str(
        datos['datos_muestra_laboratorio'][0][1][4]))
    canvas.drawString(345, 484, str(datos['datos_muestra_laboratorio'][0][1][5]))
    canvas.drawString(345, 471, str(datos['datos_muestra_laboratorio'][0][1][6]) + '+' + str(
        datos['datos_muestra_laboratorio'][0][1][7]))
    canvas.drawString(345, 458, str(datos['datos_muestra_laboratorio'][0][1][8]) + '+' + str(
        datos['datos_muestra_laboratorio'][0][1][9]))
    canvas.drawString(345, 445, str(datos['datos_muestra_laboratorio'][0][1][10]))
    canvas.drawString(345, 432, str(datos['datos_muestra_laboratorio'][0][1][11]))
    canvas.drawString(345, 419, str(datos['datos_muestra_laboratorio'][0][1][12]) + '+' + str(
        datos['datos_muestra_laboratorio'][0][1][13]))
    canvas.drawString(345, 406, str(datos['datos_muestra_laboratorio'][0][1][14]))
    # **************************************************************************


    # ***************** datos 3 ********************************************
    canvas.drawString(430, 538, str(datos['datos_muestra_laboratorio'][0][2][0]))
    canvas.drawString(415, 524, str(datos['datos_muestra_laboratorio'][0][2][1]))
    canvas.drawString(412, 510, str(datos['datos_muestra_laboratorio'][0][2][2]))
    canvas.drawString(415, 497, str(datos['datos_muestra_laboratorio'][0][2][3]) + '+' + str(
        datos['datos_muestra_laboratorio'][0][2][4]))
    canvas.drawString(415, 484, str(datos['datos_muestra_laboratorio'][0][2][5]))
    canvas.drawString(415, 471, str(datos['datos_muestra_laboratorio'][0][2][6]) + '+' + str(
        datos['datos_muestra_laboratorio'][0][2][7]))
    canvas.drawString(415, 458, str(datos['datos_muestra_laboratorio'][0][2][8]) + '+' + str(
        datos['datos_muestra_laboratorio'][0][2][9]))
    canvas.drawString(415, 445, str(datos['datos_muestra_laboratorio'][0][2][10]))
    canvas.drawString(415, 432, str(datos['datos_muestra_laboratorio'][0][2][11]))
    canvas.drawString(415, 419, str(datos['datos_muestra_laboratorio'][0][2][12]) + '+' + str(
        datos['datos_muestra_laboratorio'][0][2][13]))
    canvas.drawString(415, 406, str(datos['datos_muestra_laboratorio'][0][2][14]))
    # **************************************************************************


    # ***************** datos 4 ********************************************
    canvas.drawString(495, 538, str(datos['datos_muestra_laboratorio'][0][3][0]))
    canvas.drawString(485, 524, str(datos['datos_muestra_laboratorio'][0][3][1]))
    canvas.drawString(482, 510, str(datos['datos_muestra_laboratorio'][0][3][2]))
    canvas.drawString(485, 497, str(datos['datos_muestra_laboratorio'][0][3][3]) + '+' + str(
        datos['datos_muestra_laboratorio'][0][3][4]))
    canvas.drawString(485, 484, str(datos['datos_muestra_laboratorio'][0][3][5]))
    canvas.drawString(485, 471, str(datos['datos_muestra_laboratorio'][0][3][6]) + '+' + str(
        datos['datos_muestra_laboratorio'][0][3][7]))
    canvas.drawString(485, 458, str(datos['datos_muestra_laboratorio'][0][3][8]) + '+' + str(
        datos['datos_muestra_laboratorio'][0][3][9]))
    canvas.drawString(485, 445, str(datos['datos_muestra_laboratorio'][0][3][10]))
    canvas.drawString(485, 432, str(datos['datos_muestra_laboratorio'][0][3][11]))
    canvas.drawString(485, 419, str(datos['datos_muestra_laboratorio'][0][3][12]) + '+' + str(
        datos['datos_muestra_laboratorio'][0][3][13]))
    canvas.drawString(485, 406, str(datos['datos_muestra_laboratorio'][0][3][14]))
    # **************************************************************************

    # **************************************************************************

    canvas.drawString(250, 393, 'C. CONTENIDO DE HUMEDAD')
    canvas.drawString(65, 380, 'Numero de contenedor')
    canvas.drawString(65, 367, 'Masa recipiente (g) Mr')
    canvas.drawString(65, 354, 'Masa del contenedor + suelo humedo (g) Mw+r')
    canvas.drawString(65, 341, 'Masa del contenedor + suelo seco (g) Md+r')
    canvas.drawString(65, 328, 'Contenido de humedad w(%)')

    # ***************************** datos humedad 1**********************************
    canvas.drawString(295, 380, str(datos['datos_muestra_laboratorio'][1][0][0][0]))
    canvas.drawString(280, 367, str(datos['datos_muestra_laboratorio'][1][0][0][1]))
    canvas.drawString(280, 354, str(datos['datos_muestra_laboratorio'][1][0][0][2]))
    canvas.drawString(280, 341, str(datos['datos_muestra_laboratorio'][1][0][0][3]))
    canvas.drawString(280, 328, str(datos['resultados_del_ensayo'][0][0]))

    # ********************************************************************************

    # ***************************** datos humedad 2 **********************************
    canvas.drawString(365, 380, str(datos['datos_muestra_laboratorio'][1][0][1][0]))
    canvas.drawString(350, 367, str(datos['datos_muestra_laboratorio'][1][0][1][1]))
    canvas.drawString(350, 354, str(datos['datos_muestra_laboratorio'][1][0][1][2]))
    canvas.drawString(350, 341, str(datos['datos_muestra_laboratorio'][1][0][1][3]))
    canvas.drawString(350, 328, str(datos['resultados_del_ensayo'][0][1]))

    # ********************************************************************************


    # ***************************** datos humedad 3 **********************************
    canvas.drawString(430, 380, str(datos['datos_muestra_laboratorio'][1][0][2][0]))
    canvas.drawString(420, 367, str(datos['datos_muestra_laboratorio'][1][0][2][1]))
    canvas.drawString(420, 354, str(datos['datos_muestra_laboratorio'][1][0][2][2]))
    canvas.drawString(420, 341, str(datos['datos_muestra_laboratorio'][1][0][2][3]))
    canvas.drawString(420, 328, str(datos['resultados_del_ensayo'][0][1]))

    # ********************************************************************************

    # ***************************** datos humedad 4 **********************************
    canvas.drawString(500, 380, str(datos['datos_muestra_laboratorio'][1][0][3][0]))
    canvas.drawString(490, 367, str(datos['datos_muestra_laboratorio'][1][0][3][1]))
    canvas.drawString(490, 354, str(datos['datos_muestra_laboratorio'][1][0][3][2]))
    canvas.drawString(490, 341, str(datos['datos_muestra_laboratorio'][1][0][3][3]))
    canvas.drawString(490, 328, str(datos['resultados_del_ensayo'][0][1]))

    # ********************************************************************************

    canvas.drawString(280, 315, 'D. DENSIDAD')
    canvas.drawString(65, 302, 'Pozo')
    canvas.drawString(65, 289, 'Profundidad')
    canvas.drawString(65, 276, 'Peso unitario de la arena')
    canvas.drawString(65, 263, 'Peso del frasco + arena (antes del ensayo)')
    canvas.drawString(65, 250, 'Peso del frasco + arena (despues del ensayo)')
    canvas.drawString(65, 237, 'Peso de la arena (hoyo + cono)')
    canvas.drawString(65, 224, 'Volumen de cono y hoyo')
    canvas.drawString(65, 211, 'Volumen en el cono')
    canvas.drawString(65, 198, 'Volumen del hoyo')
    canvas.drawString(65, 185, 'Peso de la muestra humeda del hoyo')
    canvas.drawString(65, 172, 'Densidad seca aparente del suelo')
    canvas.drawString(65, 159, 'Densidad maxima de laboratorio (proctor)')
    canvas.drawString(65, 146, 'Grado de compactacion')
    canvas.drawString(65, 133, 'Grado de compactacion de especificacion')

    # ********************************  DENSIDAD RESULTADO 1 ******************************
    canvas.drawString(295, 302, str(datos['datos_muestra_laboratorio'][1][1][0][7]))
    canvas.drawString(280, 289, str(datos['datos_muestra_laboratorio'][1][1][0][2]))
    canvas.drawString(280, 276, str(datos['datos_muestra_laboratorio'][1][1][0][0]))
    canvas.drawString(280, 263, str(datos['datos_muestra_laboratorio'][1][1][0][4]))
    canvas.drawString(280, 250, str(datos['datos_muestra_laboratorio'][1][1][0][5]))
    canvas.drawString(280, 237, str(datos['resultados_del_ensayo'][1][0][0]))
    canvas.drawString(280, 224, str(datos['resultados_del_ensayo'][1][0][1]))
    canvas.drawString(280, 211, str(datos['datos_muestra_laboratorio'][1][1][0][1]))
    canvas.drawString(280, 198, str(datos['resultados_del_ensayo'][1][0][2]))
    canvas.drawString(280, 185, str(datos['datos_muestra_laboratorio'][1][1][0][6]))
    canvas.drawString(280, 172, str(datos['resultados_del_ensayo'][1][0][3]))
    canvas.drawString(280, 159, str(datos['resultados_del_ensayo'][1][0][4]))
    canvas.drawString(280, 146, str(datos['resultados_del_ensayo'][1][0][5]))
    canvas.drawString(280, 133, str(datos['resultados_del_ensayo'][1][0][6]))
    # **************************************************************************************

    # ********************************  DENSIDAD RESULTADO 2 ******************************
    canvas.drawString(365, 302, str(datos['datos_muestra_laboratorio'][1][1][1][7]))
    canvas.drawString(350, 289, str(datos['datos_muestra_laboratorio'][1][1][1][2]))
    canvas.drawString(350, 276, str(datos['datos_muestra_laboratorio'][1][1][1][0]))
    canvas.drawString(350, 263, str(datos['datos_muestra_laboratorio'][1][1][1][4]))
    canvas.drawString(350, 250, str(datos['datos_muestra_laboratorio'][1][1][1][5]))
    canvas.drawString(350, 237, str(datos['resultados_del_ensayo'][1][1][0]))
    canvas.drawString(350, 224, str(datos['resultados_del_ensayo'][1][1][1]))
    canvas.drawString(350, 211, str(datos['datos_muestra_laboratorio'][1][1][1][1]))
    canvas.drawString(350, 198, str(datos['resultados_del_ensayo'][1][1][2]))
    canvas.drawString(350, 185, str(datos['datos_muestra_laboratorio'][1][1][1][6]))
    canvas.drawString(350, 172, str(datos['resultados_del_ensayo'][1][1][3]))
    canvas.drawString(350, 159, str(datos['resultados_del_ensayo'][1][1][4]))
    canvas.drawString(350, 146, str(datos['resultados_del_ensayo'][1][1][5]))
    canvas.drawString(350, 133, str(datos['resultados_del_ensayo'][1][1][6]))
    # **************************************************************************************



    # ********************************  DENSIDAD RESULTADO 3 ******************************
    canvas.drawString(430, 302, str(datos['datos_muestra_laboratorio'][1][1][2][7]))
    canvas.drawString(420, 289, str(datos['datos_muestra_laboratorio'][1][1][2][2]))
    canvas.drawString(420, 276, str(datos['datos_muestra_laboratorio'][1][1][2][0]))
    canvas.drawString(420, 263, str(datos['datos_muestra_laboratorio'][1][1][2][4]))
    canvas.drawString(420, 250, str(datos['datos_muestra_laboratorio'][1][1][2][5]))
    canvas.drawString(420, 237, str(datos['resultados_del_ensayo'][1][2][0]))
    canvas.drawString(420, 224, str(datos['resultados_del_ensayo'][1][2][1]))
    canvas.drawString(420, 211, str(datos['datos_muestra_laboratorio'][1][1][2][1]))
    canvas.drawString(420, 198, str(datos['resultados_del_ensayo'][1][2][2]))
    canvas.drawString(420, 185, str(datos['datos_muestra_laboratorio'][1][1][2][6]))
    canvas.drawString(420, 172, str(datos['resultados_del_ensayo'][1][2][3]))
    canvas.drawString(420, 159, str(datos['resultados_del_ensayo'][1][2][4]))
    canvas.drawString(420, 146, str(datos['resultados_del_ensayo'][1][2][5]))
    canvas.drawString(420, 133, str(datos['resultados_del_ensayo'][1][2][6]))
    # **************************************************************************************



    # ********************************  DENSIDAD RESULTADO 4 ******************************
    canvas.drawString(500, 302, str(datos['datos_muestra_laboratorio'][1][1][3][7]))
    canvas.drawString(490, 289, str(datos['datos_muestra_laboratorio'][1][1][3][2]))
    canvas.drawString(490, 276, str(datos['datos_muestra_laboratorio'][1][1][3][0]))
    canvas.drawString(490, 263, str(datos['datos_muestra_laboratorio'][1][1][3][4]))
    canvas.drawString(490, 250, str(datos['datos_muestra_laboratorio'][1][1][3][5]))
    canvas.drawString(490, 237, str(datos['resultados_del_ensayo'][1][3][0]))
    canvas.drawString(490, 224, str(datos['resultados_del_ensayo'][1][3][1]))
    canvas.drawString(490, 211, str(datos['datos_muestra_laboratorio'][1][1][3][1]))
    canvas.drawString(490, 198, str(datos['resultados_del_ensayo'][1][3][2]))
    canvas.drawString(490, 185, str(datos['datos_muestra_laboratorio'][1][1][3][6]))
    canvas.drawString(490, 172, str(datos['resultados_del_ensayo'][1][3][3]))
    canvas.drawString(490, 159, str(datos['resultados_del_ensayo'][1][3][4]))
    canvas.drawString(490, 146, str(datos['resultados_del_ensayo'][1][3][5]))
    canvas.drawString(490, 133, str(datos['resultados_del_ensayo'][1][3][6]))
    # **************************************************************************************

    # observaciones
    canvas.drawString(58, 117, 'D. OBSERVACIONES')
    canvas.line(60, 115, 550, 115)  ## horizontal abajo9
    linea7 = 499
    # FIRMAS
    canvas.drawString(70, 78, 'Firma del jefe de carrera')
    canvas.drawString(420, 78, 'Firma del tecnico')
    canvas.line(puntoAx, puntoY - linea7 - 110, puntoMedio - 90, puntoY - linea7 - 110)
    canvas.line(puntoMedio + 80, puntoY - linea7 - 110, puntoBx, puntoY - linea7 - 110)

    # DATOS ACREDITACION
    linea8y = 70
    canvas.drawString(90, linea8y - 10, 'ELABORADO POR')
    canvas.drawString(260, linea8y - 10, 'REVISADO POR')
    canvas.drawString(420, linea8y - 10, 'APROBADO POR')

    canvas.line(puntoAx, linea8y, puntoBx, linea8y)
    linea8y = linea8y - 15
    canvas.line(puntoAx, linea8y, puntoBx, linea8y)
    linea8y = linea8y - 25
    canvas.line(puntoAx, linea8y, puntoBx, linea8y)
    canvas.line(puntoAx, linea8y + 40, puntoAx, linea8y)  # vertical
    canvas.line(puntoBx, linea8y + 40, puntoBx, linea8y)  # vertical
    canvas.line(puntoMedio - 90, linea8y + 40, puntoMedio - 90, linea8y)  # vertical
    canvas.line(puntoMedio + 90, linea8y + 40, puntoMedio + 90, linea8y)  # vertical

    # FIN COPIAR

    canvas.save()
    pdf_out = output.getvalue()

    output.close()
    filename = 'cono_de_arena_astm.pdf'
    response = make_response(pdf_out)
    response.headers['Content-Disposition'] = "attachment; filename"
    response.mimetype = 'application/pdf'
    # return response

    return send_file(filename, as_attachment=False)





def reporte_indice_de_soporte_astm(datos_CBR):
    datos=datos_CBR[1]

    # output = cStringIO.StringIO()
    canvas = Canvas("indice_de_soporte_CBR.pdf", pagesize=letter)
    canvas.setLineWidth(.3)
    canvas.setFont('Helvetica', 10)

    canvas.line(60, 760, 550, 760)  # punto x1, y1 , x2, y2 #HORIZONTAL
    canvas.line(60, 760, 60, 700)  # VERTICAL
    canvas.line(60, 700, 550, 700)  # HORIZONTAL
    canvas.line(550, 760, 550, 700)  # VERTICAL
    canvas.line(190, 760, 190, 700)  # VERTICAL
    canvas.line(400, 760, 400, 700)  # VERTICAL
    # CAJETIN PEQUENO
    canvas.line(400, 745, 550, 745)  # HORIZONTAL
    canvas.line(400, 730, 550, 730)  # HORIZONTAL
    canvas.line(400, 715, 550, 715)  # HORIZONTAL
    canvas.line(470, 760, 470, 715)  # VERTICAL
    canvas.drawImage("static/img/emi.jpeg", 70, 710, width=115, height=40)

    # TITULO
    frame1 = Frame(190, 700, 210, 60, showBoundary=1)  # Frame(movX,movY,margenAncho,mrgenAlto)
    bodyStyle = ParagraphStyle('normal', fontSize=24, leading=28, spaceBefore=30, alignment=TA_CENTER)
    s = datos_CBR[0]
    story = [Paragraph(s, bodyStyle)]
    story_inframe = KeepInFrame(210, 1 * inch, story)
    frame1.addFromList([story_inframe], canvas)
    # interlineado=740

    # DATOS
    posx = 410
    canvas.setFont('Helvetica', 10)
    canvas.drawString(posx, 750, 'Codigo:')
    canvas.drawString(posx, 735, 'Aprobacion:')
    canvas.drawString(posx, 720, 'Version:')
    canvas.drawString(posx + 70, 750, 'C5117-9')
    canvas.drawString(posx + 70, 735, 'Aprobado')
    canvas.drawString(posx + 70, 720, 'Version 1.1')
    canvas.drawString(posx + 30, 703, 'Página 1 de 2')

    # SEGUNDA CAJETILLA
    puntoAx = 60
    puntoBx = 550
    puntoY = 698
    puntoMedio = (puntoAx + puntoBx) / 2

    canvas.line(60, 680, 550,
                680)  # horizontal arriba (largohacialaIZQUIERDA ,arribaIZQ , largo de la linea hacia la derecha ,arribaDER)
    canvas.setFont('Helvetica', 12)
    canvas.drawString(235, 665, 'A. DATOS GENRALES')  # (# ,  arriba , #)
    canvas.line(60, 680, 60,
                568)  # vertical iquierdo  (mover linea hacia derecha punto arriba, linea hacia arriba, mover linea hacia derecha punto abajo)
    canvas.line(550, 680, 550, 568)  # vertical DERECHO
    canvas.line(60, 661, 550, 661)  ## horizontal abajo
    # primero
    canvas.setFont('Helvetica', 9)
    canvas.drawString(160, 651, 'Proyecto')
    canvas.line(60, 649, 550, 649)  ## horizontal abajo2
    canvas.line(300, 660, 300, 568)  # vertical2 MEDIO
    canvas.drawString(400, 651, 'Fecha')
    canvas.setFont('Helvetica', 12)
    canvas.drawString(70, 633, datos['datos_generales'][0])
    canvas.drawString(310, 633, datos['datos_generales'][7])
    canvas.line(60, 630, 550, 630)  ## horizontal abajo3
    # segundo
    canvas.setFont('Helvetica', 9)
    canvas.drawString(160, 620, 'Ubicacion')
    canvas.drawString(400, 620, 'Laboratista')
    canvas.line(60, 618, 550, 618)  ## horizontal abajo4
    canvas.line(60, 599, 550, 599)  ## horizontal abajo5
    canvas.setFont('Helvetica', 12)
    canvas.drawString(70, 602, datos['datos_generales'][1])
    canvas.drawString(310, 602, datos['datos_generales'][4])

    # tercero
    canvas.setFont('Helvetica', 9)
    canvas.drawString(120, 589, 'Descripcion De La Muestra')
    canvas.drawString(380, 589, 'Tipo De Muestra')
    canvas.line(60, 587, 550, 587)  ## horizontal abajo6
    canvas.line(60, 568, 550, 568)  ## horizontal abajo7
    canvas.setFont('Helvetica', 12)
    canvas.drawString(70, 571, datos['datos_generales'][2])
    canvas.drawString(310, 571, datos['datos_generales'][3])

    # # tabla calculos
    for i in range(12):
        canvas.line(60, 560 - i * 13, 550, 560 - i * 13)  ## horizontal

    canvas.line(60, 560, 60, 184)  # vertical IZQUIERDO
    canvas.line(550, 560, 550, 184)  # vertical DERECHO
    # ****************** datos tecnicos ********************************
    canvas.line(240, 547, 240, 430)  # vertical DERECHO medio1
    canvas.line(343.33, 547, 343.33, 430)  # vertical DERECHO medio2
    canvas.line(446.33, 547, 446.33, 430)  # vertical DERECHO medio3
    # intermedios
    canvas.line(291.66, 508, 291.66, 430)  # vertical1
    canvas.line(394.99, 508, 394.99, 430)  # vertical2
    canvas.line(497.99, 508, 497.99, 430)  # vertical3

    # **************** contenido de dato humedades de compactacion y ebebimiento **************************
    # cabecera pequeña
    canvas.line(60, 397, 550, 397)
    canvas.line(240, 407, 550, 407)
    for i in range(9):
        canvas.line(60, 384 - i * 13, 550, 384 - i * 13)  ## horizontal

    canvas.line(240, 417, 240, 293)  # vertical DERECHO medio1
    canvas.line(343.33, 417, 343.33, 293)  # vertical DERECHO medio2
    canvas.line(446.33, 417, 446.33, 293)  # vertical DERECHO medio3
    # intermedios
    canvas.line(291.66, 417, 291.66, 293)  # vertical1
    canvas.line(394.99, 417, 394.99, 293)  # vertical2
    canvas.line(497.99, 417, 497.99, 293)  # vertical3
    # mas medio pequenos
    canvas.line(265.83, 407, 265.83, 319)  # vertical1
    canvas.line(317.49, 407, 317.49, 319)  # vertical2
    canvas.line(369.16, 407, 369.16, 319)  # vertical3
    canvas.line(420.82, 407, 420.82, 319)  # vertical4
    canvas.line(472.16, 407, 472.16, 319)  # vertical5
    canvas.line(523.82, 407, 523.82, 319)  # vertical6

    # ************** determinacion de la expancion ***************************************
    canvas.line(60, 250, 550, 250)  ## horizontal

    for i in range(5):
        canvas.line(60, 236 - i * 13, 550, 236 - i * 13)  ## horizontal

    canvas.line(240, 280, 240, 184)  # vertical DERECHO medio1
    canvas.line(343.33, 280, 343.33, 184)  # vertical DERECHO medio2
    canvas.line(446.33, 280, 446.33, 184)  # vertical DERECHO medio3
    # intermedios 0
    canvas.line(155, 280, 155, 184)  # vertical DERECHO medio1
    # intermedios 1
    canvas.line(274.44, 280, 274.44, 184)  # vertical DERECHO medio1
    canvas.line(308.88, 280, 308.88, 184)  # vertical DERECHO medio1
    # intermedios 2
    canvas.line(377.77, 280, 377.77, 184)  # vertical DERECHO medio1
    canvas.line(412.21, 280, 412.21, 184)  # vertical DERECHO medio1
    # intermedios 3
    canvas.line(480.77, 280, 480.77, 184)  # vertical DERECHO medio1
    canvas.line(515.21, 280, 515.21, 184)  # vertical DERECHO medio1

    canvas.setFont('Helvetica', 9)
    canvas.drawString(230, 550, 'B. COMPACTACIÓN DE LA MUESTRA')

    # ****************** titulos ***********************************
    canvas.drawString(65, 538, 'Molde N°')
    canvas.drawString(65, 524, 'N° de capas')
    canvas.drawString(65, 510, 'N° de golpes por capa')
    canvas.drawString(65, 497, 'Condición de la muestra')
    canvas.drawString(65, 484, 'Peso hum. de la muestra + molde (gr)')
    canvas.drawString(65, 471, 'Peso del molde (gr)')
    canvas.drawString(65, 458, 'Peso humedo de la muestra (gr)')
    canvas.drawString(65, 445, 'volumen de la muestra (cm3)')
    canvas.drawString(65, 432, 'Densidad humedad de la muestra (gr/cm3)')
    # ***************** datos 1 ********************************************
    canvas.drawString(290, 538, str(datos['datos_muestra_laboratorio'][5][0]))
    canvas.drawString(290, 524, str(datos['datos_muestra_laboratorio'][5][3]))
    canvas.drawString(288, 510, str(datos['datos_muestra_laboratorio'][5][6]))
    canvas.setFont('Helvetica', 7)
    canvas.drawString(243, 497, 'Antes embeb')
    canvas.drawString(292, 497, 'Despues embeb')
    canvas.setFont('Helvetica', 9)
    canvas.drawString(245, 484, str(datos['datos_muestra_laboratorio'][0][0][0][0]))
    canvas.drawString(295, 484, str(datos['datos_muestra_laboratorio'][0][0][1][0]))
    canvas.drawString(245, 471, str(datos['datos_muestra_laboratorio'][0][0][0][1]))
    canvas.drawString(295, 471, str(datos['datos_muestra_laboratorio'][0][0][0][1]))
    canvas.drawString(245, 458, str(datos['resultados_del_ensayo'][0][0][0]))
    canvas.drawString(295, 458, str(datos['resultados_del_ensayo'][0][1][0]))
    canvas.drawString(245, 445, str(datos['datos_muestra_laboratorio'][0][0][0][2]))
    canvas.drawString(295, 445, str(datos['datos_muestra_laboratorio'][0][0][0][2]))
    canvas.drawString(245, 432, str(datos['resultados_del_ensayo'][0][0][1]))
    canvas.drawString(295, 432, str(datos['resultados_del_ensayo'][0][1][1]))

    # # ***************** datos 2 ********************************************
    canvas.drawString(395, 538, str(datos['datos_muestra_laboratorio'][5][1]))
    canvas.drawString(395, 524, str(datos['datos_muestra_laboratorio'][5][4]))
    canvas.drawString(392, 510, str(datos['datos_muestra_laboratorio'][5][7]))
    canvas.setFont('Helvetica', 7)
    canvas.drawString(348, 497, 'Antes embeb')
    canvas.drawString(395, 497, 'Despues embeb')
    canvas.setFont('Helvetica', 9)
    canvas.drawString(348, 484, str(datos['datos_muestra_laboratorio'][0][1][0][0]))
    canvas.drawString(399, 484, str(datos['datos_muestra_laboratorio'][0][1][1][0]))
    canvas.drawString(348, 471, str(datos['datos_muestra_laboratorio'][0][1][0][1]))
    canvas.drawString(399, 471, str(datos['datos_muestra_laboratorio'][0][1][0][1]))
    canvas.drawString(348, 458, str(datos['resultados_del_ensayo'][0][2][0]))
    canvas.drawString(399, 458, str(datos['resultados_del_ensayo'][0][2][0]))
    canvas.drawString(348, 445, str(datos['datos_muestra_laboratorio'][0][1][0][2]))
    canvas.drawString(399, 445, str(datos['datos_muestra_laboratorio'][0][1][0][2]))
    canvas.drawString(348, 432, str(datos['resultados_del_ensayo'][0][2][1]))
    canvas.drawString(399, 432, str(datos['resultados_del_ensayo'][0][3][1]))

    # # **************************************************************************
    #
    #
    # # ***************** datos 3 ********************************************
    canvas.drawString(495, 538, str(datos['datos_muestra_laboratorio'][5][2]))
    canvas.drawString(495, 524, str(datos['datos_muestra_laboratorio'][5][5]))
    canvas.drawString(492, 510, str(datos['datos_muestra_laboratorio'][5][8]))
    canvas.setFont('Helvetica', 7)
    canvas.drawString(450, 497, 'Antes embeb')
    canvas.drawString(499, 497, 'Despues embeb')
    canvas.setFont('Helvetica', 9)
    canvas.drawString(450, 484, str(datos['datos_muestra_laboratorio'][0][2][0][0]))
    canvas.drawString(501, 484, str(datos['datos_muestra_laboratorio'][0][2][1][0]))
    canvas.drawString(450, 471, str(datos['datos_muestra_laboratorio'][0][2][0][1]))
    canvas.drawString(501, 471, str(datos['datos_muestra_laboratorio'][0][2][0][1]))
    canvas.drawString(450, 458, str(datos['resultados_del_ensayo'][0][4][0]))
    canvas.drawString(501, 458, str(datos['resultados_del_ensayo'][0][5][0]))
    canvas.drawString(450, 445, str(datos['datos_muestra_laboratorio'][0][2][0][2]))
    canvas.drawString(501, 445, str(datos['datos_muestra_laboratorio'][0][2][0][2]))
    canvas.drawString(450, 432, str(datos['resultados_del_ensayo'][0][4][1]))
    canvas.drawString(501, 432, str(datos['resultados_del_ensayo'][0][5][1]))

    # **************************************************************************

    # **************************************************************************

    canvas.drawString(220, 419, 'C. HUMEDADES DE COMPACTACIÓN Y EMBEBIMIENTO')
    canvas.drawString(120, 404, 'HUMEDAD')
    canvas.setFont('Helvetica', 6.5)
    # primera
    canvas.drawString(240.8, 409, 'De compactacion')
    canvas.drawString(293.5, 409, 'Despues embeb.')
    canvas.drawString(242, 400, 'Inferior')
    canvas.drawString(266.5, 400, 'Superior')
    # -------------------------------------
    canvas.drawString(294, 400, 'Inferior')
    canvas.drawString(318, 400, 'Superior')
    # segundo
    canvas.drawString(344, 409, 'De compactacion')
    canvas.drawString(396.5, 409, 'Despues embeb.')
    canvas.drawString(346, 400, 'Inferior')
    canvas.drawString(369.5, 400, 'Superior')
    canvas.drawString(398, 400, 'Inferior')
    canvas.drawString(421.2, 400, 'Superior')
    # tercero
    canvas.drawString(447, 409, 'De compactacion')
    canvas.drawString(499.5, 409, 'Despues embeb.')
    canvas.drawString(449, 400, 'Inferior')
    canvas.drawString(472.6, 400, 'Superior')
    canvas.drawString(501, 400, 'Inferior')
    canvas.drawString(524.5, 400, 'Superior')
    canvas.setFont('Helvetica', 9)
    canvas.drawString(65, 387, 'Recipiente N°')
    canvas.drawString(65, 374, 'Masa del contenedor + suelo humedo (gr)')
    canvas.drawString(65, 361, 'Masa del contenedor + suelo seco (g)')
    canvas.drawString(65, 348, 'Masa del agua')
    canvas.drawString(65, 335, 'Masa recipiente (gr)')
    canvas.drawString(65, 322, 'Masa del suelo seco (gr)')
    canvas.drawString(65, 309, 'PROMEDIO % DE HUMEDAD')
    canvas.drawString(65, 296, 'Densidad seca probeta (gr/cm3)')

    # ***************************** datos dato 1**********************************
    canvas.drawString(250, 387, str(datos['datos_muestra_laboratorio'][1][0][0][0][3]))
    canvas.drawString(275, 387, str(datos['datos_muestra_laboratorio'][1][0][0][1][3]))
    canvas.drawString(299, 387, str(datos['datos_muestra_laboratorio'][1][0][1][0][3]))
    canvas.drawString(325, 387, str(datos['datos_muestra_laboratorio'][1][0][1][1][3]))
    canvas.drawString(350, 387, str(datos['datos_muestra_laboratorio'][1][1][0][0][3]))
    canvas.drawString(375, 387, str(datos['datos_muestra_laboratorio'][1][1][0][1][3]))
    canvas.drawString(400, 387, str(datos['datos_muestra_laboratorio'][1][1][1][0][3]))
    canvas.drawString(425, 387, str(datos['datos_muestra_laboratorio'][1][1][1][1][3]))
    canvas.drawString(455, 387, str(datos['datos_muestra_laboratorio'][1][2][0][0][3]))
    canvas.drawString(480, 387, str(datos['datos_muestra_laboratorio'][1][2][0][1][3]))
    canvas.drawString(505, 387, str(datos['datos_muestra_laboratorio'][1][2][1][0][3]))
    canvas.drawString(530, 387, str(datos['datos_muestra_laboratorio'][1][2][1][1][3]))
    #
    # # ***************************** datos dato 2 **********************************
    canvas.drawString(241, 374, str(datos['datos_muestra_laboratorio'][1][0][0][0][1]))
    canvas.drawString(267, 374, str(datos['datos_muestra_laboratorio'][1][0][0][1][1]))
    canvas.drawString(293, 374, str(datos['datos_muestra_laboratorio'][1][0][1][0][1]))
    canvas.drawString(319, 374, str(datos['datos_muestra_laboratorio'][1][0][1][1][1]))
    canvas.drawString(345, 374, str(datos['datos_muestra_laboratorio'][1][1][0][0][1]))
    canvas.drawString(370, 374, str(datos['datos_muestra_laboratorio'][1][1][0][1][1]))
    canvas.drawString(396, 374, str(datos['datos_muestra_laboratorio'][1][1][1][0][1]))
    canvas.drawString(422, 374, str(datos['datos_muestra_laboratorio'][1][1][1][1][1]))
    canvas.drawString(447, 374, str(datos['datos_muestra_laboratorio'][1][2][0][0][1]))
    canvas.drawString(473, 374, str(datos['datos_muestra_laboratorio'][1][2][0][1][1]))
    canvas.drawString(499, 374, str(datos['datos_muestra_laboratorio'][1][2][1][0][1]))
    canvas.drawString(525, 374, str(datos['datos_muestra_laboratorio'][1][2][1][1][1]))

    # # ***************************** datos dato 3 **********************************
    canvas.drawString(241, 361, str(datos['datos_muestra_laboratorio'][1][0][0][0][2]))
    canvas.drawString(267, 361, str(datos['datos_muestra_laboratorio'][1][0][0][1][2]))
    canvas.drawString(293, 361, str(datos['datos_muestra_laboratorio'][1][0][1][0][2]))
    canvas.drawString(319, 361, str(datos['datos_muestra_laboratorio'][1][0][1][1][2]))
    canvas.drawString(345, 361, str(datos['datos_muestra_laboratorio'][1][1][0][0][2]))
    canvas.drawString(370, 361, str(datos['datos_muestra_laboratorio'][1][1][0][1][2]))
    canvas.drawString(396, 361, str(datos['datos_muestra_laboratorio'][1][1][1][0][2]))
    canvas.drawString(422, 361, str(datos['datos_muestra_laboratorio'][1][1][1][1][2]))
    canvas.drawString(447, 361, str(datos['datos_muestra_laboratorio'][1][2][0][0][2]))
    canvas.drawString(473, 361, str(datos['datos_muestra_laboratorio'][1][2][0][1][2]))
    canvas.drawString(499, 361, str(datos['datos_muestra_laboratorio'][1][2][1][0][2]))
    canvas.drawString(525, 361, str(datos['datos_muestra_laboratorio'][1][2][1][1][2]))
    # #********************************************************************************
    # # ***************************** datos dato 4 masa del agua **********************************
    canvas.drawString(241, 348, str(datos['resultados_del_ensayo'][0][0][3][1][0]))
    canvas.drawString(267, 348, str(datos['resultados_del_ensayo'][0][0][3][1][1]))
    canvas.drawString(293, 348, str(datos['resultados_del_ensayo'][0][1][3][1][0]))
    canvas.drawString(319, 348, str(datos['resultados_del_ensayo'][0][1][3][1][1]))
    canvas.drawString(345, 348, str(datos['resultados_del_ensayo'][0][2][3][1][0]))
    canvas.drawString(370, 348, str(datos['resultados_del_ensayo'][0][2][3][1][1]))
    canvas.drawString(396, 348, str(datos['resultados_del_ensayo'][0][3][3][1][0]))
    canvas.drawString(422, 348, str(datos['resultados_del_ensayo'][0][3][3][1][1]))
    canvas.drawString(447, 348, str(datos['resultados_del_ensayo'][0][4][3][1][0]))
    canvas.drawString(473, 348, str(datos['resultados_del_ensayo'][0][4][3][1][1]))
    canvas.drawString(499, 348, str(datos['resultados_del_ensayo'][0][5][3][1][0]))
    canvas.drawString(525, 348, str(datos['resultados_del_ensayo'][0][5][3][1][1]))
    # #********************************************************************************
    # # ***************************** datos dato 4 masa del recipiente **********************************
    canvas.drawString(241, 335, str(datos['datos_muestra_laboratorio'][1][0][0][0][0]))
    canvas.drawString(267, 335, str(datos['datos_muestra_laboratorio'][1][0][0][1][0]))
    canvas.drawString(293, 335, str(datos['datos_muestra_laboratorio'][1][0][1][0][0]))
    canvas.drawString(319, 335, str(datos['datos_muestra_laboratorio'][1][0][1][1][0]))
    canvas.drawString(345, 335, str(datos['datos_muestra_laboratorio'][1][1][0][0][0]))
    canvas.drawString(370, 335, str(datos['datos_muestra_laboratorio'][1][1][0][1][0]))
    canvas.drawString(396, 335, str(datos['datos_muestra_laboratorio'][1][1][1][0][0]))
    canvas.drawString(422, 335, str(datos['datos_muestra_laboratorio'][1][1][1][1][0]))
    canvas.drawString(447, 335, str(datos['datos_muestra_laboratorio'][1][2][0][0][0]))
    canvas.drawString(473, 335, str(datos['datos_muestra_laboratorio'][1][2][0][1][0]))
    canvas.drawString(499, 335, str(datos['datos_muestra_laboratorio'][1][2][1][0][0]))
    canvas.drawString(525, 335, str(datos['datos_muestra_laboratorio'][1][2][1][1][0]))
    # #********************************************************************************

    # # ***************************** datos dato 4 masa del suelo seco **********************************
    canvas.drawString(241, 322, str(datos['resultados_del_ensayo'][0][0][3][2][0]))
    canvas.drawString(267, 322, str(datos['resultados_del_ensayo'][0][0][3][2][1]))
    canvas.drawString(293, 322, str(datos['resultados_del_ensayo'][0][1][3][2][0]))
    canvas.drawString(319, 322, str(datos['resultados_del_ensayo'][0][1][3][2][1]))
    canvas.drawString(345, 322, str(datos['resultados_del_ensayo'][0][2][3][2][0]))
    canvas.drawString(370, 322, str(datos['resultados_del_ensayo'][0][2][3][2][1]))
    canvas.drawString(396, 322, str(datos['resultados_del_ensayo'][0][3][3][2][0]))
    canvas.drawString(422, 322, str(datos['resultados_del_ensayo'][0][3][3][2][1]))
    canvas.drawString(447, 322, str(datos['resultados_del_ensayo'][0][4][3][2][0]))
    canvas.drawString(473, 322, str(datos['resultados_del_ensayo'][0][4][3][2][1]))
    canvas.drawString(499, 322, str(datos['resultados_del_ensayo'][0][5][3][2][0]))
    canvas.drawString(525, 322, str(datos['resultados_del_ensayo'][0][5][3][2][1]))
    # #********************************************************************************
    # # ***************************** datos dato 4 humedad promedio **********************************
    canvas.drawString(250, 309, str(datos['resultados_del_ensayo'][0][0][3][0][0]))
    canvas.drawString(302, 309, str(datos['resultados_del_ensayo'][0][1][3][0][0]))
    canvas.drawString(354, 309, str(datos['resultados_del_ensayo'][0][2][3][0][0]))
    canvas.drawString(405, 309, str(datos['resultados_del_ensayo'][0][3][3][0][0]))
    canvas.drawString(456, 309, str(datos['resultados_del_ensayo'][0][4][3][0][0]))
    canvas.drawString(508, 309, str(datos['resultados_del_ensayo'][0][5][3][0][0]))
    # #********************************************************************************
    # # ***************************** datos dato 4 dencidad seca probeta **********************************
    canvas.drawString(250, 296, str(datos['resultados_del_ensayo'][0][0][2]))
    canvas.drawString(302, 296, str(datos['resultados_del_ensayo'][0][1][2]))
    canvas.drawString(354, 296, str(datos['resultados_del_ensayo'][0][2][2]))
    canvas.drawString(405, 296, str(datos['resultados_del_ensayo'][0][3][2]))
    canvas.drawString(456, 296, str(datos['resultados_del_ensayo'][0][4][2]))
    canvas.drawString(508, 296, str(datos['resultados_del_ensayo'][0][5][2]))
    # #********************************************************************************

    canvas.drawString(260, 282, 'D. DETERMINACION DE LA EXPANCIÓN')
    canvas.drawString(93, 260, 'Fecha')
    canvas.drawString(185, 260, 'Hora')
    # cab 1
    canvas.drawString(242, 268, 'Lectura')
    canvas.drawString(243, 260, 'Extens')
    canvas.drawString(278, 270, 'Increm')
    canvas.drawString(279, 262, 'Altura')
    canvas.drawString(280, 255, '(mm)')
    canvas.drawString(320, 268, '%')
    canvas.setFont('Helvetica', 7)
    canvas.drawString(310, 260, 'Expansion')
    # cab 2
    canvas.setFont('Helvetica', 9)
    canvas.drawString(345, 268, 'Lectura')
    canvas.drawString(346, 260, 'Extens')
    canvas.drawString(380, 270, 'Increm')
    canvas.drawString(381, 262, 'Altura')
    canvas.drawString(382, 255, '(mm)')
    canvas.drawString(422, 268, '%')
    canvas.setFont('Helvetica', 7)
    canvas.drawString(413, 260, 'Expansion')
    # cab 3
    canvas.setFont('Helvetica', 9)
    canvas.drawString(448, 268, 'Lectura')
    canvas.drawString(449, 260, 'Extens')
    canvas.drawString(484, 270, 'Increm')
    canvas.drawString(486, 262, 'Altura')
    canvas.drawString(487, 255, '(mm)')
    canvas.drawString(525, 268, '%')
    canvas.setFont('Helvetica', 7)
    canvas.drawString(516, 260, 'Expansion')
    canvas.setFont('Helvetica', 9)
    # ---------------FECHA------------------------------------------------
    canvas.drawString(83, 240, str(datos['datos_muestra_laboratorio'][2][0][0][0]))
    canvas.drawString(83, 226, str(datos['datos_muestra_laboratorio'][2][0][0][1]))
    canvas.drawString(83, 213, str(datos['datos_muestra_laboratorio'][2][0][0][2]))
    canvas.drawString(83, 200, str(datos['datos_muestra_laboratorio'][2][0][0][3]))
    canvas.drawString(83, 186, str(datos['datos_muestra_laboratorio'][2][0][0][4]))
    # ---------------HORA--------------------------------------------------------
    canvas.drawString(175, 240, str(datos['datos_muestra_laboratorio'][2][0][1][0]))
    canvas.drawString(175, 226, str(datos['datos_muestra_laboratorio'][2][0][1][1]))
    canvas.drawString(175, 213, str(datos['datos_muestra_laboratorio'][2][0][1][2]))
    canvas.drawString(175, 200, str(datos['datos_muestra_laboratorio'][2][0][1][3]))
    canvas.drawString(175, 186, str(datos['datos_muestra_laboratorio'][2][0][1][4]))
    # ---------------LECTURA EXTEND 1--------------------------------------------------------
    canvas.drawString(248, 240, str(datos['datos_muestra_laboratorio'][2][1][0][0]))
    canvas.drawString(248, 226, str(datos['datos_muestra_laboratorio'][2][1][0][1]))
    canvas.drawString(248, 213, str(datos['datos_muestra_laboratorio'][2][1][0][2]))
    canvas.drawString(248, 200, str(datos['datos_muestra_laboratorio'][2][1][0][3]))
    canvas.drawString(248, 186, str(datos['datos_muestra_laboratorio'][2][1][0][4]))

    # --------------INCREMENT ALTURA MM 1-------------------------------------------------------
    canvas.drawString(280, 240, str(datos['resultados_del_ensayo'][1][0][0][0]))
    canvas.drawString(280, 226, str(datos['resultados_del_ensayo'][1][0][0][1]))
    canvas.drawString(280, 213, str(datos['resultados_del_ensayo'][1][0][0][2]))
    canvas.drawString(280, 200, str(datos['resultados_del_ensayo'][1][0][0][3]))
    canvas.drawString(280, 186, str(datos['resultados_del_ensayo'][1][0][0][4]))
    # -------------- EXPANSION % 1-------------------------------------------------------
    canvas.drawString(315, 240, str(datos['resultados_del_ensayo'][1][0][0][0]))
    canvas.drawString(315, 226, str(datos['resultados_del_ensayo'][1][0][0][1]))
    canvas.drawString(315, 213, str(datos['resultados_del_ensayo'][1][0][0][2]))
    canvas.drawString(315, 200, str(datos['resultados_del_ensayo'][1][0][0][3]))
    canvas.drawString(315, 186, str(datos['resultados_del_ensayo'][1][0][0][4]))
    # ***********************************************************************************************
    # ---------------LECTURA EXTEND 2--------------------------------------------------------
    canvas.drawString(349, 240, str(datos['datos_muestra_laboratorio'][2][1][0][0]))
    canvas.drawString(349, 226, str(datos['datos_muestra_laboratorio'][2][1][0][1]))
    canvas.drawString(349, 213, str(datos['datos_muestra_laboratorio'][2][1][0][2]))
    canvas.drawString(349, 200, str(datos['datos_muestra_laboratorio'][2][1][0][3]))
    canvas.drawString(349, 186, str(datos['datos_muestra_laboratorio'][2][1][0][4]))

    # --------------INCREMENT ALTURA MM 2-------------------------------------------------------
    canvas.drawString(383, 240, str(datos['resultados_del_ensayo'][1][0][0][0]))
    canvas.drawString(383, 226, str(datos['resultados_del_ensayo'][1][0][0][1]))
    canvas.drawString(383, 213, str(datos['resultados_del_ensayo'][1][0][0][2]))
    canvas.drawString(383, 200, str(datos['resultados_del_ensayo'][1][0][0][3]))
    canvas.drawString(383, 186, str(datos['resultados_del_ensayo'][1][0][0][4]))
    # -------------- EXPANSION % 2-------------------------------------------------------
    canvas.drawString(415, 240, str(datos['resultados_del_ensayo'][1][0][0][0]))
    canvas.drawString(415, 226, str(datos['resultados_del_ensayo'][1][0][0][1]))
    canvas.drawString(415, 213, str(datos['resultados_del_ensayo'][1][0][0][2]))
    canvas.drawString(415, 200, str(datos['resultados_del_ensayo'][1][0][0][3]))
    canvas.drawString(415, 186, str(datos['resultados_del_ensayo'][1][0][0][4]))
    # ***********************************************************************************************

    # ---------------LECTURA EXTEND 3--------------------------------------------------------
    canvas.drawString(451, 240, str(datos['datos_muestra_laboratorio'][2][1][0][0]))
    canvas.drawString(451, 226, str(datos['datos_muestra_laboratorio'][2][1][0][1]))
    canvas.drawString(451, 213, str(datos['datos_muestra_laboratorio'][2][1][0][2]))
    canvas.drawString(451, 200, str(datos['datos_muestra_laboratorio'][2][1][0][3]))
    canvas.drawString(451, 186, str(datos['datos_muestra_laboratorio'][2][1][0][4]))

    # --------------INCREMENT ALTURA MM 3-------------------------------------------------------
    canvas.drawString(488, 240, str(datos['resultados_del_ensayo'][1][0][0][0]))
    canvas.drawString(488, 226, str(datos['resultados_del_ensayo'][1][0][0][1]))
    canvas.drawString(488, 213, str(datos['resultados_del_ensayo'][1][0][0][2]))
    canvas.drawString(488, 200, str(datos['resultados_del_ensayo'][1][0][0][3]))
    canvas.drawString(488, 186, str(datos['resultados_del_ensayo'][1][0][0][4]))
    # -------------- EXPANSION % 3-------------------------------------------------------
    canvas.drawString(518, 240, str(datos['resultados_del_ensayo'][1][0][0][0]))
    canvas.drawString(518, 226, str(datos['resultados_del_ensayo'][1][0][0][1]))
    canvas.drawString(518, 213, str(datos['resultados_del_ensayo'][1][0][0][2]))
    canvas.drawString(518, 200, str(datos['resultados_del_ensayo'][1][0][0][3]))
    canvas.drawString(518, 186, str(datos['resultados_del_ensayo'][1][0][0][4]))
    # ***********************************************************************************************
    # #**************************************************************************************


    # observaciones
    canvas.drawString(58, 150, 'D. OBSERVACIONES')
    canvas.line(60, 130, 550, 130)  ## horizontal abajo9
    linea7 = 499
    # FIRMAS
    canvas.drawString(90, 78, 'Firma del jefe de carrera')
    canvas.drawString(450, 78, 'Firma del tecnico')
    canvas.line(puntoAx, puntoY - linea7 - 110, puntoMedio - 90, puntoY - linea7 - 110)
    canvas.line(puntoMedio + 80, puntoY - linea7 - 110, puntoBx, puntoY - linea7 - 110)

    # DATOS ACREDITACION
    linea8y = 70
    canvas.drawString(90, linea8y - 10, 'ELABORADO POR')
    canvas.drawString(260, linea8y - 10, 'REVISADO POR')
    canvas.drawString(420, linea8y - 10, 'APROBADO POR')

    canvas.line(puntoAx, linea8y, puntoBx, linea8y)
    linea8y = linea8y - 15
    canvas.line(puntoAx, linea8y, puntoBx, linea8y)
    linea8y = linea8y - 25
    canvas.line(puntoAx, linea8y, puntoBx, linea8y)
    canvas.line(puntoAx, linea8y + 40, puntoAx, linea8y)  # vertical
    canvas.line(puntoBx, linea8y + 40, puntoBx, linea8y)  # vertical
    canvas.line(puntoMedio - 90, linea8y + 40, puntoMedio - 90, linea8y)  # vertical
    canvas.line(puntoMedio + 90, linea8y + 40, puntoMedio + 90, linea8y)  # vertical

    #####-------------------------------  segunda hoja ------------------------------------########################
    canvas.showPage()

    output = cStringIO.StringIO()
    canvas.setLineWidth(.3)
    canvas.setFont('Helvetica', 10)
    canvas.line(60, 760, 550, 760)  # punto x1, y1 , x2, y2 #HORIZONTAL
    canvas.line(60, 760, 60, 700)  # VERTICAL
    canvas.line(60, 700, 550, 700)  # HORIZONTAL
    canvas.line(550, 760, 550, 700)  # VERTICAL
    canvas.line(190, 760, 190, 700)  # VERTICAL
    canvas.line(400, 760, 400, 700)  # VERTICAL
    # CAJETIN PEQUENO
    canvas.line(400, 745, 550, 745)  # HORIZONTAL
    canvas.line(400, 730, 550, 730)  # HORIZONTAL
    canvas.line(400, 715, 550, 715)  # HORIZONTAL
    canvas.line(470, 760, 470, 715)  # VERTICAL
    canvas.drawImage("static/img/emi.jpeg", 70, 710, width=115, height=40)

    # TITULO
    frame1 = Frame(190, 700, 210, 60, showBoundary=1)  # Frame(movX,movY,margenAncho,mrgenAlto)
    bodyStyle = ParagraphStyle('normal', fontSize=24, leading=28, spaceBefore=30, alignment=TA_CENTER)
    s = datos_CBR[0]
    story = [Paragraph(s, bodyStyle)]
    story_inframe = KeepInFrame(210, 1 * inch, story)
    frame1.addFromList([story_inframe], canvas)
    # interlineado=740

    # DATOS
    posx = 410
    canvas.setFont('Helvetica', 10)
    canvas.drawString(posx, 750, 'Codigo:')
    canvas.drawString(posx, 735, 'Aprobacion:')
    canvas.drawString(posx, 720, 'Version:')
    canvas.drawString(posx + 70, 750, 'C5117-9')
    canvas.drawString(posx + 70, 735, 'Aprobado')
    canvas.drawString(posx + 70, 720, 'Version 1.1')
    canvas.drawString(posx + 30, 703, 'Página 2 de 2')


    # ---------- cuerpo ---------------------------------------------------------
    if len(datos['resultados_del_ensayo'][2][3]) == 12:
        t = 490
    else:
        t = 529
    canvas.line(60, 685, 60, t)  # vertical IZQUIERDO
    canvas.line(550, 685, 550, t)  # vertical DERECHO
    # CABECERA
    canvas.line(60, 685, 550, 685)  #
    canvas.line(60, 645, 550, 645)  #
    canvas.line(60, 667, 240, 667)  # linea de peentracion
    canvas.line(291.5, 667, 343.5, 667)  # linea de precion mpa1
    canvas.line(395, 667, 446.5, 667)  # linea de precion mpa2
    canvas.line(498, 667, 550, 667)  # linea de precion mpa3
    # lineas
    canvas.line(240, 685, 240, t)  # vertical DERECHO medio1
    canvas.line(343.33, 685, 343.33, t)  # vertical DERECHO medio2
    canvas.line(446.33, 685, 446.33, t)  # vertical DERECHO medio3
    # intermedias de pentracion
    canvas.line(120, 667, 120, t)  # vertical DERECHO medio1
    canvas.line(180, 667, 180, t)  # vertical DERECHO medio2

    # intermedias
    canvas.line(291.66, 685, 291.66, t)  # vertical DERECHO medio1
    canvas.line(394.99, 685, 394.99, t)  # vertical DERECHO medio2
    canvas.line(497.99, 685, 497.99, t)  # vertical DERECHO medio3
    canvas.setFont('Helvetica', 10)
    canvas.drawString(112, 672, 'PENETRACIÓN')
    canvas.setFont('Helvetica', 9)
    canvas.drawString(63, 653, 'Tiempo (min)')
    canvas.drawString(128, 653, 'Pulgadas')
    canvas.drawString(186, 653, 'Centimetros')
    canvas.drawString(247, 670, 'Lectura')
    canvas.drawString(255, 655, 'Dial')
    canvas.setFont('Helvetica', 8)
    canvas.drawString(292.5, 675, 'Presion (Mpa)')
    canvas.setFont('Helvetica', 9)
    canvas.drawString(297, 655, 'Calculada')
    ##**** 2 *******************************
    canvas.drawString(352, 670, 'Lectura')
    canvas.drawString(360, 655, 'Dial')
    canvas.setFont('Helvetica', 8)
    canvas.drawString(395.5, 675, 'Presion (Mpa)')
    canvas.setFont('Helvetica', 9)
    canvas.drawString(400, 655, 'Calculada')
    ##**** 3 *******************************
    canvas.drawString(455, 670, 'Lectura')
    canvas.drawString(463, 655, 'Dial')
    canvas.setFont('Helvetica', 8)
    canvas.drawString(499, 675, 'Presion (Mpa)')
    canvas.setFont('Helvetica', 9)
    canvas.drawString(503, 655, 'Calculada')
    canvas.setFont('Helvetica', 9)
    a = 635

    for i in range(len(datos['resultados_del_ensayo'][2][3])):
        canvas.line(60, 633 - i * 13, 550, 633 - i * 13)  ## horizontal
        canvas.drawString(69, a - i * 13, str(datos['resultados_del_ensayo'][2][3][i]))  # tiempo
        canvas.drawString(128, a - i * 13, str(datos['resultados_del_ensayo'][2][4][i]))  # pul
        canvas.drawString(188, a - i * 13, str(datos['resultados_del_ensayo'][2][5][i]))  # centimetro
        canvas.drawString(248, a - i * 13, str(datos['datos_muestra_laboratorio'][3][0][i]))  # lectura dial 1
        canvas.drawString(297, a - i * 13, str(datos['resultados_del_ensayo'][2][0][0][i]))  # calculada1
        canvas.drawString(350, a - i * 13, str(datos['datos_muestra_laboratorio'][3][1][i]))  # lectura dial 2
        canvas.drawString(400, a - i * 13, str(datos['resultados_del_ensayo'][2][0][1][i]))  # calculada2
        canvas.drawString(455, a - i * 13, str(datos['datos_muestra_laboratorio'][3][2][i]))  # lectura dial 3
        canvas.drawString(503, a - i * 13, str(datos['resultados_del_ensayo'][2][0][2][i]))  # calculada3


    canvas.drawImage("static/" + datos['direccion_de_grafico'][0], 50, 355, width=300, height=140)  # izquierda, abajo


    canvas.drawImage("static/" + datos['direccion_de_grafico'][1], 330, 355, width=250, height=140)  # izquierda, abajo

    # ---------------------------------------------------------------------------




    # observaciones
    canvas.drawString(58, 150, 'D. OBSERVACIONES')
    canvas.line(60, 130, 550, 130)  ## horizontal abajo9
    linea7 = 499
    # FIRMAS
    canvas.drawString(90, 78, 'Firma del jefe de carrera')
    canvas.drawString(450, 78, 'Firma del tecnico')
    canvas.line(puntoAx, puntoY - linea7 - 110, puntoMedio - 90, puntoY - linea7 - 110)
    canvas.line(puntoMedio + 80, puntoY - linea7 - 110, puntoBx, puntoY - linea7 - 110)

    # DATOS ACREDITACION
    linea8y = 70
    canvas.drawString(90, linea8y - 10, 'ELABORADO POR')
    canvas.drawString(260, linea8y - 10, 'REVISADO POR')
    canvas.drawString(420, linea8y - 10, 'APROBADO POR')

    canvas.line(puntoAx, linea8y, puntoBx, linea8y)
    linea8y = linea8y - 15
    canvas.line(puntoAx, linea8y, puntoBx, linea8y)
    linea8y = linea8y - 25
    canvas.line(puntoAx, linea8y, puntoBx, linea8y)
    canvas.line(puntoAx, linea8y + 40, puntoAx, linea8y)  # vertical
    canvas.line(puntoBx, linea8y + 40, puntoBx, linea8y)  # vertical
    canvas.line(puntoMedio - 90, linea8y + 40, puntoMedio - 90, linea8y)  # vertical
    canvas.line(puntoMedio + 90, linea8y + 40, puntoMedio + 90, linea8y)  # vertical

    # FIN COPIAR
    canvas.save()
    pdf_out = output.getvalue()

    output.close()

    canvas.showPage()

    filename = 'indice_de_soporte_CBR.pdf'
    response = make_response(pdf_out)
    response.headers['Content-Disposition'] = "attachment; filename"
    response.mimetype = 'application/pdf'
    # return response
    return send_file(filename, as_attachment=False)
############################  REPORTE_CORTE DIRECTO GEOTECNIA ##############################################3

def reporte_corte_directo_astm_geotecnia(datos_corte):

    datos=datos_corte[1]
    canvas = Canvas("corte_directo_geotecnia.pdf", pagesize=letter)
    canvas.setLineWidth(.3)
    canvas.setFont('Helvetica', 10)

    canvas.line(60, 760, 550, 760)  # punto x1, y1 , x2, y2 #HORIZONTAL
    canvas.line(60, 760, 60, 700)  # VERTICAL
    canvas.line(60, 700, 550, 700)  # HORIZONTAL
    canvas.line(550, 760, 550, 700)  # VERTICAL
    canvas.line(190, 760, 190, 700)  # VERTICAL
    canvas.line(400, 760, 400, 700)  # VERTICAL
    # CAJETIN PEQUENO
    canvas.line(400, 745, 550, 745)  # HORIZONTAL
    canvas.line(400, 730, 550, 730)  # HORIZONTAL
    canvas.line(400, 715, 550, 715)  # HORIZONTAL
    canvas.line(470, 760, 470, 715)  # VERTICAL

    canvas.drawImage("static/img/emi.jpeg", 70, 710, width=115, height=40)

    # TITULO
    frame1 = Frame(190, 700, 210, 60, showBoundary=1)  # Frame(movX,movY,margenAncho,mrgenAlto)
    bodyStyle = ParagraphStyle('normal', fontSize=24, leading=28, spaceBefore=30, alignment=TA_CENTER)
    s = datos_corte[0]
    story = [Paragraph(s, bodyStyle)]
    story_inframe = KeepInFrame(210, 1 * inch, story)
    frame1.addFromList([story_inframe], canvas)
    # interlineado=740

    # DATOS
    posx = 410
    canvas.setFont('Helvetica', 10)
    canvas.drawString(posx, 750, 'Codigo:')
    canvas.drawString(posx, 735, 'Aprobacion:')
    canvas.drawString(posx, 720, 'Version:')
    canvas.drawString(posx + 70, 750, 'C5117-9')
    canvas.drawString(posx + 70, 735, 'Aprobado')
    canvas.drawString(posx + 70, 720, 'Version 1.1')
    canvas.drawString(posx + 30, 703, 'Página 1 de 2')

    # SEGUNDA CAJETILLA
    puntoAx = 60
    puntoBx = 550
    puntoY = 698
    puntoMedio = (puntoAx + puntoBx) / 2

    canvas.line(60, 680, 550,
                680)  # horizontal arriba (largohacialaIZQUIERDA ,arribaIZQ , largo de la linea hacia la derecha ,arribaDER)
    canvas.setFont('Helvetica', 12)
    canvas.drawString(235, 665, 'A. DATOS GENRALES')  # (# ,  arriba , #)
    canvas.line(60, 680, 60,
                568)  # vertical iquierdo  (mover linea hacia derecha punto arriba, linea hacia arriba, mover linea hacia derecha punto abajo)
    canvas.line(550, 680, 550, 568)  # vertical DERECHO
    canvas.line(60, 661, 550, 661)  ## horizontal abajo
    # primero
    canvas.setFont('Helvetica', 9)
    canvas.drawString(160, 651, 'Proyecto')
    canvas.line(60, 649, 550, 649)  ## horizontal abajo2
    canvas.line(300, 660, 300, 568)  # vertical2 MEDIO
    canvas.drawString(400, 651, 'Fecha')
    canvas.setFont('Helvetica', 12)
    canvas.drawString(70, 633, datos['datos_generales'][0])
    canvas.drawString(310, 633, datos['datos_generales'][7])
    canvas.line(60, 630, 550, 630)  ## horizontal abajo3
    # segundo
    canvas.setFont('Helvetica', 9)
    canvas.drawString(160, 620, 'Ubicacion')
    canvas.drawString(400, 620, 'Laboratista')
    canvas.line(60, 618, 550, 618)  ## horizontal abajo4
    canvas.line(60, 599, 550, 599)  ## horizontal abajo5
    canvas.setFont('Helvetica', 12)
    canvas.drawString(70, 602, datos['datos_generales'][1])
    canvas.drawString(310, 602, datos['datos_generales'][4])

    # tercero
    canvas.setFont('Helvetica', 9)
    canvas.drawString(120, 589, 'Descripcion De La Muestra')
    canvas.drawString(380, 589, 'Tipo De Muestra')
    canvas.line(60, 587, 550, 587)  ## horizontal abajo6
    canvas.line(60, 568, 550, 568)  ## horizontal abajo7
    canvas.setFont('Helvetica', 12)
    canvas.drawString(70, 571, datos['datos_generales'][2])
    canvas.drawString(310, 571, datos['datos_generales'][3])

    # ****************** datos tecnicos ********************************
    canvas.line(200, 560, 200, 482)  # vertical DERECHO medio1
    canvas.line(420, 560, 420, 482)  # vertical DERECHO medio2
    # intermedios
    canvas.line(311, 547, 311, 482)  # vertical DERECHO medio2
    canvas.line(368, 547, 368, 482)  # vertical DERECHO medio2

    canvas.setFont('Helvetica', 9)
    canvas.drawString(230, 550, 'DIMENSIONES DE LA CAJA DE CORTE')
    for i in range(7):
        canvas.line(200, 560 - i * 13, 420, 560 - i * 13)  ## horizontal

        # ****************** titulos ***********************************
    canvas.drawString(204, 538, 'Dimensión interior 1')
    canvas.drawString(204, 524, 'Dimensión interior 2')
    canvas.drawString(204, 510, 'Area inicial de probeta')
    canvas.drawString(204, 497, 'Altura incial de la probeta')
    canvas.drawString(204, 484, 'Volumen de la muestra')

    # #***************** datos 1 ********************************************
    canvas.drawString(320, 538, str(datos['datos_muestra_laboratorio'][1][0]))
    canvas.drawString(385, 538, 'cm')
    canvas.drawString(320, 524, str(datos['datos_muestra_laboratorio'][1][1]))
    canvas.drawString(385, 524, 'cm')
    canvas.drawString(320, 510, str(datos['resultados_del_ensayo'][3][0]))
    canvas.drawString(385, 510, 'cm')
    canvas.drawString(320, 497, str(datos['datos_muestra_laboratorio'][1][2]))
    canvas.drawString(385, 497, 'cm2')
    canvas.drawString(320, 484, str(datos['resultados_del_ensayo'][3][1]))
    canvas.drawString(385, 484, 'cm3')

    # ********************************** propiedades de la muestra *************
    canvas.drawString(230, 468, 'DIMENSIONES DE LA CAJA DE CORTE')
    canvas.drawString(65, 455, 'Esfuerzo Normal:')
    canvas.drawString(220, 455, str(datos['datos_muestra_laboratorio'][2][1][0]) + ' ' + 'KN/m2')

    canvas.drawString(310, 455, 'Carga Normal:')
    canvas.drawString(465, 455, str(datos['datos_muestra_laboratorio'][2][0][0]) + ' ' + 'KN/m2')

    # cabecera
    canvas.drawString(82, 442, 'Dx (mm)')
    canvas.drawString(158, 442, 'Lectura Dy')
    canvas.drawString(245, 442, 'Dy (mm)')
    canvas.drawString(308, 442, 'Lectura de Fuerza')
    canvas.drawString(393, 442, 'Area Modificada')
    canvas.drawString(473, 442, 'Esfuerzo Cortante')

    if len(datos['datos_muestra_laboratorio'][0][0][0]) == 11:
        largo = 296
    else:
        largo = 309

    canvas.line(60, 478, 60, largo)  # vertical IZQUIERDO
    canvas.line(550, 478, 550, largo)  # vertical DERECHO
    # parte de la cabezera
    canvas.line(60, 478, 550, 478)
    canvas.line(60, 465, 550, 465)
    canvas.line(60, 452, 550, 452)
    canvas.line(60, 439, 550, 439)

    # intermedios
    canvas.line(141.66, 452, 141.66, largo)
    canvas.line(223.32, 452, 223.32, largo)
    canvas.line(304.98, 465, 304.98, largo)
    canvas.line(386.64, 452, 386.64, largo)
    canvas.line(468.3, 452, 468.3, largo)
    a = 429

    for i in range(len(datos['datos_muestra_laboratorio'][0][0][0])):
        canvas.line(60, 426 - i * 13, 550, 426 - i * 13)  ## horizontal
        canvas.drawString(69, a - i * 13, str(datos['datos_muestra_laboratorio'][0][0][0][i]))
        canvas.drawString(150, a - i * 13, str(datos['datos_muestra_laboratorio'][0][0][1][i]))
        canvas.drawString(230, a - i * 13, str(datos['resultados_del_ensayo'][0][0][i]))
        canvas.drawString(312, a - i * 13, str(datos['datos_muestra_laboratorio'][0][0][2][i]))
        canvas.drawString(393, a - i * 13, str(datos['resultados_del_ensayo'][1][0][i]))
        canvas.drawString(473, a - i * 13, str(datos['resultados_del_ensayo'][2][0][i]))

    # *******************************  TABLA DE MUESTRA NUERO 2 **************************************************

    # cabecera 2
    if len(datos['datos_muestra_laboratorio'][0][1][0]) == 11:
        largo2 = 134
    else:
        largo2 = 147

    canvas.line(60, 303, 60, largo2)  # vertical IZQUIERDO
    canvas.line(550, 303, 550, largo2)  # vertical DERECHO
    canvas.line(60, 303, 550, 303)
    canvas.line(60, 290, 550, 290)
    canvas.line(60, 277, 550, 277)
    # intermedios
    canvas.line(141.66, 290, 141.66, largo2)
    canvas.line(223.32, 290, 223.32, largo2)
    canvas.line(304.98, 303, 304.98, largo2)
    canvas.line(386.64, 290, 386.64, largo2)
    canvas.line(468.3, 290, 468.3, largo2)

    canvas.drawString(65, 293, 'Esfuerzo Normal:')
    canvas.drawString(220, 293, str(datos['datos_muestra_laboratorio'][2][1][1]) + ' ' + 'KN/m2')

    canvas.drawString(310, 293, 'Carga Normal:')
    canvas.drawString(465, 293, str(datos['datos_muestra_laboratorio'][2][0][1]) + ' ' + 'KN/m2')

    # cabecera2
    canvas.drawString(82, 280, 'Dx (mm)')
    canvas.drawString(158, 280, 'Lectura Dy')
    canvas.drawString(245, 280, 'Dy (mm)')
    canvas.drawString(308, 280, 'Lectura de Fuerza')
    canvas.drawString(393, 280, 'Area Modificada')
    canvas.drawString(473, 280, 'Esfuerzo Cortante')

    b = 267
    for i in range(len(datos['datos_muestra_laboratorio'][0][1][0])):
        canvas.line(60, 264 - i * 13, 550, 264 - i * 13)  ## horizontal
        canvas.drawString(69, b - i * 13, str(datos['datos_muestra_laboratorio'][0][1][0][i]))
        canvas.drawString(150, b - i * 13, str(datos['datos_muestra_laboratorio'][0][1][1][i]))
        canvas.drawString(230, b - i * 13, str(datos['resultados_del_ensayo'][0][1][i]))
        canvas.drawString(312, b - i * 13, str(datos['datos_muestra_laboratorio'][0][1][2][i]))
        canvas.drawString(393, b - i * 13, str(datos['resultados_del_ensayo'][1][1][i]))
        canvas.drawString(473, b - i * 13, str(datos['resultados_del_ensayo'][2][1][i]))

    # # observaciones
    # canvas.drawString(58, 150, 'D. OBSERVACIONES')
    # canvas.line(60, 130, 550, 130)  ## horizontal abajo9
    linea7 = 499
    # # FIRMAS
    canvas.drawString(90, 78, 'Firma del jefe de carrera')
    canvas.drawString(450, 78, 'Firma del tecnico')
    canvas.line(puntoAx, puntoY - linea7 - 110, puntoMedio - 90, puntoY - linea7 - 110)
    canvas.line(puntoMedio + 80, puntoY - linea7 - 110, puntoBx, puntoY - linea7 - 110)

    # DATOS ACREDITACION
    linea8y = 70
    canvas.drawString(90, linea8y - 10, 'ELABORADO POR')
    canvas.drawString(260, linea8y - 10, 'REVISADO POR')
    canvas.drawString(420, linea8y - 10, 'APROBADO POR')

    canvas.line(puntoAx, linea8y, puntoBx, linea8y)
    linea8y = linea8y - 15
    canvas.line(puntoAx, linea8y, puntoBx, linea8y)
    linea8y = linea8y - 25
    canvas.line(puntoAx, linea8y, puntoBx, linea8y)
    canvas.line(puntoAx, linea8y + 40, puntoAx, linea8y)  # vertical
    canvas.line(puntoBx, linea8y + 40, puntoBx, linea8y)  # vertical
    canvas.line(puntoMedio - 90, linea8y + 40, puntoMedio - 90, linea8y)  # vertical
    canvas.line(puntoMedio + 90, linea8y + 40, puntoMedio + 90, linea8y)  # vertical

    #####-------------------------------  segunda hoja ------------------------------------########################
    canvas.showPage()

    output = cStringIO.StringIO()
    canvas.setLineWidth(.3)
    canvas.setFont('Helvetica', 10)
    canvas.line(60, 760, 550, 760)  # punto x1, y1 , x2, y2 #HORIZONTAL
    canvas.line(60, 760, 60, 700)  # VERTICAL
    canvas.line(60, 700, 550, 700)  # HORIZONTAL
    canvas.line(550, 760, 550, 700)  # VERTICAL
    canvas.line(190, 760, 190, 700)  # VERTICAL
    canvas.line(400, 760, 400, 700)  # VERTICAL
    canvas.drawImage("static/img/emi.jpeg", 70, 710, width=115, height=40)
    # CAJETIN PEQUENO
    canvas.line(400, 745, 550, 745)  # HORIZONTAL
    canvas.line(400, 730, 550, 730)  # HORIZONTAL
    canvas.line(400, 715, 550, 715)  # HORIZONTAL
    canvas.line(470, 760, 470, 715)  # VERTICAL

    # TITULO
    frame1 = Frame(190, 700, 210, 60, showBoundary=1)  # Frame(movX,movY,margenAncho,mrgenAlto)
    bodyStyle = ParagraphStyle('normal', fontSize=24, leading=28, spaceBefore=30, alignment=TA_CENTER)
    s = datos_corte[0]
    story = [Paragraph(s, bodyStyle)]
    story_inframe = KeepInFrame(210, 1 * inch, story)
    frame1.addFromList([story_inframe], canvas)
    # interlineado=740

    # DATOS
    posx = 410
    canvas.setFont('Helvetica', 10)
    canvas.drawString(posx, 750, 'Codigo:')
    canvas.drawString(posx, 735, 'Aprobacion:')
    canvas.drawString(posx, 720, 'Version:')
    canvas.drawString(posx + 70, 750, 'C5117-9')
    canvas.drawString(posx + 70, 735, 'Aprobado')
    canvas.drawString(posx + 70, 720, 'Version 1.1')
    canvas.drawString(posx + 30, 703, 'Página 2 de 2')
    # ---------- cuerpo ---------------------------------------------------------


    # *******************************  TABLA DE MUESTRA NUERO 3 **************************************************

    # cabecera 3
    canvas.setFont('Helvetica', 9)
    if len(datos['datos_muestra_laboratorio'][0][2][0]) == 11:
        largo2 = 511
    else:
        largo2 = 524

    canvas.line(60, 680, 60, largo2)  # vertical IZQUIERDO
    canvas.line(550, 680, 550, largo2)  # vertical DERECHO
    canvas.line(60, 680, 550, 680)
    canvas.line(60, 667, 550, 667)
    canvas.line(60, 654, 550, 654)
    # intermedios
    canvas.line(141.66, 667, 141.66, largo2)
    canvas.line(223.32, 667, 223.32, largo2)
    canvas.line(304.98, 680, 304.98, largo2)
    canvas.line(386.64, 667, 386.64, largo2)
    canvas.line(468.3, 667, 468.3, largo2)

    canvas.drawString(65, 670, 'Esfuerzo Normal:')
    canvas.drawString(220, 670, str(datos['datos_muestra_laboratorio'][2][1][0]) + ' ' + 'KN/m2')

    canvas.drawString(310, 670, 'Carga Normal:')
    canvas.drawString(465, 670, str(datos['datos_muestra_laboratorio'][2][0][2]) + ' ' + 'KN/m2')

    # cabecera2
    canvas.drawString(82, 657, 'Dx (mm)')
    canvas.drawString(158, 657, 'Lectura Dy')
    canvas.drawString(245, 657, 'Dy (mm)')
    canvas.drawString(308, 657, 'Lectura de Fuerza')
    canvas.drawString(393, 657, 'Area Modificada')
    canvas.drawString(473, 657, 'Esfuerzo Cortante')

    c = 644
    for i in range(len(datos['datos_muestra_laboratorio'][0][2][0])):
        canvas.line(60, 641 - i * 13, 550, 641 - i * 13)  ## horizontal
        canvas.drawString(69, c - i * 13, str(datos['datos_muestra_laboratorio'][0][2][0][i]))
        canvas.drawString(150, c - i * 13, str(datos['datos_muestra_laboratorio'][0][2][1][i]))
        canvas.drawString(230, c - i * 13, str(datos['resultados_del_ensayo'][0][2][i]))
        canvas.drawString(312, c - i * 13, str(datos['datos_muestra_laboratorio'][0][2][2][i]))
        canvas.drawString(393, c - i * 13, str(datos['resultados_del_ensayo'][1][2][i]))
        canvas.drawString(473, c - i * 13, str(datos['resultados_del_ensayo'][2][2][i]))


    canvas.drawImage("static/" + datos['direccion_de_grafico'][0], 50, 355, width=300, height=140)  # izquierda, abajo


    canvas.drawImage("static/" + datos['direccion_de_grafico'][1], 325, 355, width=250, height=140)  # izquierda, abajo

    canvas.drawImage("static/" + datos['direccion_de_grafico'][2], 180, 212, width=250, height=140)  # izquierda, abajo

    # ---------------------------------------------------------------------------




    # observaciones
    canvas.drawString(58, 150, 'D. OBSERVACIONES')
    canvas.line(60, 130, 550, 130)  ## horizontal abajo9
    linea7 = 499
    # FIRMAS
    canvas.drawString(90, 78, 'Firma del jefe de carrera')
    canvas.drawString(450, 78, 'Firma del tecnico')
    canvas.line(puntoAx, puntoY - linea7 - 110, puntoMedio - 90, puntoY - linea7 - 110)
    canvas.line(puntoMedio + 80, puntoY - linea7 - 110, puntoBx, puntoY - linea7 - 110)

    # DATOS ACREDITACION
    linea8y = 70
    canvas.drawString(90, linea8y - 10, 'ELABORADO POR')
    canvas.drawString(260, linea8y - 10, 'REVISADO POR')
    canvas.drawString(420, linea8y - 10, 'APROBADO POR')

    canvas.line(puntoAx, linea8y, puntoBx, linea8y)
    linea8y = linea8y - 15
    canvas.line(puntoAx, linea8y, puntoBx, linea8y)
    linea8y = linea8y - 25
    canvas.line(puntoAx, linea8y, puntoBx, linea8y)
    canvas.line(puntoAx, linea8y + 40, puntoAx, linea8y)  # vertical
    canvas.line(puntoBx, linea8y + 40, puntoBx, linea8y)  # vertical
    canvas.line(puntoMedio - 90, linea8y + 40, puntoMedio - 90, linea8y)  # vertical
    canvas.line(puntoMedio + 90, linea8y + 40, puntoMedio + 90, linea8y)  # vertical

    # FIN COPIAR
    canvas.save()
    pdf_out = output.getvalue()

    output.close()

    canvas.showPage()

    filename = 'corte_directo_geotecnia.pdf'
    response = make_response(pdf_out)
    response.headers['Content-Disposition'] = "attachment; filename"
    response.mimetype = 'application/pdf'
    # return response
    return send_file(filename, as_attachment=False)



# ##################################  SOLICITUD DE USO DE LABORATORIO ######################################


def reporte_solicitud_de_uso_de_laboratorio(datos_uso_lab):

    datos=datos_uso_lab[1]

    output = cStringIO.StringIO()
    canvas = Canvas("uso_de_laboratorio.pdf", pagesize=letter)
    canvas.setLineWidth(.3)
    canvas.setFont('Helvetica', 10)

    canvas.saveState()
    # canvas = canvas.Canvas(self.nombrePDF, pagesize=letter)
    canvas.setLineWidth(.3)
    canvas.setFont('Helvetica', 10)

    canvas.line(60, 760, 550, 760)  # punto x1, y1 , x2, y2 #HORIZONTAL
    canvas.line(60, 760, 60, 700)  # VERTICAL
    canvas.line(60, 700, 550, 700)  # HORIZONTAL
    canvas.line(550, 760, 550, 700)  # VERTICAL
    canvas.line(190, 760, 190, 700)  # VERTICAL
    canvas.line(400, 760, 400, 700)  # VERTICAL
    # CAJETIN PEQUENO
    canvas.line(400, 745, 550, 745)  # HORIZONTAL
    canvas.line(400, 730, 550, 730)  # HORIZONTAL
    canvas.line(400, 715, 550, 715)  # HORIZONTAL
    canvas.line(470, 760, 470, 715)  # VERTICAL
    # Inseratmos la imagen en el documento
    # canvas.drawImage('emi.jpeg', -50, 500)#Imagen estatica
    canvas.drawImage("static/img/emi.jpeg", 70, 710, width=115, height=40)

    # TITULO
    frame1 = Frame(190, 700, 210, 60, showBoundary=1)  # Frame(movX,movY,margenAncho,mrgenAlto)
    bodyStyle = ParagraphStyle('normal', fontSize=20, leading=28, spaceBefore=30, alignment=TA_CENTER)
    s = datos_uso_lab[0]
    story = [Paragraph(s, bodyStyle)]
    story_inframe = KeepInFrame(210, 1 * inch, story)
    frame1.addFromList([story_inframe], canvas)
    # interlineado=740

    # DATOS
    posx = 410
    canvas.setFont('Helvetica', 10)
    canvas.drawString(posx, 750, 'Codigo:')
    canvas.drawString(posx, 735, 'Aprobacion:')
    canvas.drawString(posx, 720, 'Version:')
    canvas.drawString(posx + 70, 750, 'C5117-9')
    canvas.drawString(posx + 70, 735, 'Aprobado')
    canvas.drawString(posx + 70, 720, 'Version 1.1')
    canvas.drawString(posx + 30, 703, 'Página 1 de 1')

    # SEGUNDA CAJETILLA
    puntoAx = 60
    puntoBx = 550

    puntoY = 698
    canvas.line(puntoAx, puntoY, puntoBx, puntoY)
    canvas.line(puntoAx, puntoY - 20, puntoBx, puntoY - 20)
    canvas.setFont('Helvetica', 8)
    canvas.drawString(puntoAx + 3, puntoY - 8, 'Unidad administrativa:')
    canvas.drawString(puntoAx + 3, puntoY - 17, 'Direccion Nacional de Investigacion Ciencia y Tecnologia')

    puntoMedio = (puntoAx + puntoBx) / 2

    canvas.line(puntoMedio, puntoY, puntoMedio, puntoY - 20)  # vertical
    canvas.drawString(puntoMedio + 3, puntoY - 8, 'Area Responsable:')
    canvas.drawString(puntoMedio + 3, puntoY - 17, 'Normalizacion de Laboratorios y Registro')
    canvas.line(puntoAx, puntoY - 35, puntoBx, puntoY - 35)
    canvas.setFont('Helvetica-Bold', 9)
    canvas.drawString(puntoMedio - 70, puntoY - 30, 'REQUERIMIENTOS DE LABORATORIO')
    canvas.line(puntoAx, puntoY, puntoAx, puntoY - 35)  # vertical
    canvas.line(puntoBx, puntoY, puntoBx, puntoY - 35)  # vertical

    # siguiente cajetilla
    cajetin_pequeno = 150
    canvas.line(puntoAx, puntoY - 37, puntoBx, puntoY - 37)  #
    canvas.line(puntoAx, puntoY - 46, puntoBx, puntoY - 46)  #
    canvas.line(puntoAx, puntoY - 64, puntoBx, puntoY - 64)  #
    canvas.line(puntoAx, puntoY - 37, puntoAx, puntoY - 64)  # vertical
    canvas.line(puntoBx, puntoY - 37, puntoBx, puntoY - 64)  # vertical
    canvas.line(puntoBx - cajetin_pequeno, puntoY - 37, puntoBx - cajetin_pequeno, puntoY - 64)  # vertical
    canvas.setFont('Helvetica', 8)
    canvas.drawString(puntoAx + 130, puntoY - 45, 'Nombre del solictante')
    canvas.drawString(puntoAx + 410, puntoY - 45, 'C.I.')
    # datos
    canvas.setFont('Helvetica', 10)
    canvas.drawString(puntoAx + 100, puntoY - 60, datos['nombre'])
    canvas.drawString(puntoAx + 390, puntoY - 60, datos['ci'])

    # Siguiente cajetin
    division = 150
    canvas.line(puntoAx, puntoY - 67, puntoBx, puntoY - 67)  #
    canvas.line(puntoAx, puntoY - 76, puntoBx, puntoY - 76)  #
    canvas.line(puntoAx, puntoY - 94, puntoBx, puntoY - 94)  #
    canvas.line(puntoAx, puntoY - 67, puntoAx, puntoY - 94)  # vertical
    canvas.line(puntoBx, puntoY - 67, puntoBx, puntoY - 94)  # vertical
    canvas.line(puntoAx + division, puntoY - 67, puntoAx + division, puntoY - 94)  # vertical
    canvas.line(puntoBx - division, puntoY - 67, puntoBx - division, puntoY - 94)  # vertical
    canvas.setFont('Helvetica', 8)
    canvas.drawString(puntoAx + 60, puntoY - 75, 'Carrera')
    canvas.drawString(puntoAx + 220, puntoY - 75, 'Asignatura')
    canvas.drawString(puntoAx + 400, puntoY - 75, 'Semestre')
    # datos
    canvas.setFont('Helvetica', 10)
    canvas.drawString(puntoAx + 30, puntoY - 90, datos['carrera'])
    canvas.drawString(puntoAx + 190, puntoY - 90, datos['asignatura'])
    canvas.drawString(puntoAx + 400, puntoY - 90, datos['semestre'])

    # Sigueinte Cajetilla
    cajetin_pequeno = 150
    canvas.line(puntoAx, puntoY - 97, puntoBx, puntoY - 97)  #
    canvas.line(puntoAx, puntoY - 106, puntoBx, puntoY - 106)  #
    canvas.line(puntoAx, puntoY - 124, puntoBx, puntoY - 124)  #
    canvas.line(puntoAx, puntoY - 97, puntoAx, puntoY - 124)  # vertical
    canvas.line(puntoBx, puntoY - 97, puntoBx, puntoY - 124)  # vertical
    canvas.line(puntoBx - cajetin_pequeno, puntoY - 97, puntoBx - cajetin_pequeno, puntoY - 124)  # vertical
    canvas.setFont('Helvetica', 8)
    canvas.drawString(puntoAx + 130, puntoY - 105, 'Practica de Laboratorio')
    canvas.drawString(puntoAx + 380, puntoY - 105, 'Fecha de la Solicitud')
    # datos
    canvas.setFont('Helvetica', 10)
    canvas.drawString(puntoAx + 140 - len(datos['practica_laboratorio']), puntoY - 120,
                      datos['practica_laboratorio'])
    canvas.drawString(puntoAx + 380, puntoY - 120, datos['fecha_solicitud'])

    # TABLAS MATERIALES
    linea = 140
    canvas.drawString(puntoAx + 3, puntoY - linea + 3, 'MATERIALES')

    lista_materiales = [datos['materiales'][0], datos['materiales'][1], datos['materiales'][2],
                        datos['materiales'][3], datos['materiales'][4], datos['materiales'][5],
                        datos['materiales'][6], datos['materiales'][7]]
    cont = 0
    for i in range(5):
        canvas.line(puntoAx, puntoY - linea, puntoBx, puntoY - linea)
        if i <= 3:
            canvas.drawString(puntoAx + 5, puntoY - linea - 13, lista_materiales[cont])
            canvas.drawString(puntoMedio + 5, puntoY - linea - 13, lista_materiales[cont + 1])
            if i <= 2:
                cont = cont + 2
        linea = linea + 20

    canvas.line(puntoMedio, puntoY - 140, puntoMedio, puntoY - linea + 20)  # vertical
    canvas.line(puntoAx, puntoY - 140, puntoAx, puntoY - linea + 20)  # vertical
    canvas.line(puntoBx, puntoY - 140, puntoBx, puntoY - linea + 20)  # vertical

    # TABLAS EQUIPOS
    linea1 = linea - 20
    canvas.drawString(puntoAx + 3, puntoY - linea1 - 17, 'EQUIPOS')

    lista_equipos = [datos['equipos'][0], datos['equipos'][1], datos['equipos'][2],
                     datos['equipos'][3]]
    cont = 0
    for y in range(4):
        canvas.line(puntoAx, puntoY - linea1, puntoBx, puntoY - linea1)
        if y <= 1:
            canvas.drawString(puntoAx + 5, puntoY - linea1 - 33, lista_equipos[cont])
            canvas.drawString(puntoMedio + 5, puntoY - linea1 - 33, lista_equipos[cont + 1])
            if y < 1:
                cont = cont + 2
        linea1 = linea1 + 20
    canvas.line(puntoMedio, puntoY - linea, puntoMedio, puntoY - linea1 + 20)  # vertical
    canvas.line(puntoAx, puntoY - linea, puntoAx, puntoY - linea1 + 20)  # vertical
    canvas.line(puntoBx, puntoY - linea, puntoBx, puntoY - linea1 + 20)  # vertical

    linea2 = linea1 - 20
    canvas.drawString(puntoAx + 3, puntoY - linea2 - 17, 'REACTIVOS')
    lista_reactivos = [datos['reactivos'][0], datos['reactivos'][1], datos['reactivos'][2],
                       datos['reactivos'][3], datos['reactivos'][4], datos['reactivos'][5],
                       datos['reactivos'][6], datos['reactivos'][7]]
    cont = 0
    for z in range(6):
        canvas.line(puntoAx, puntoY - linea2, puntoBx, puntoY - linea2)
        if z <= 3:
            canvas.drawString(puntoAx + 5, puntoY - linea2 - 33, lista_reactivos[cont])
            canvas.drawString(puntoMedio + 5, puntoY - linea2 - 33, lista_reactivos[cont + 1])
            if z <= 2:
                cont = cont + 2
        linea2 = linea2 + 20
    canvas.line(puntoMedio, puntoY - linea1, puntoMedio, puntoY - linea2 + 20)  # vertical
    canvas.line(puntoAx, puntoY - linea1, puntoAx, puntoY - linea2 + 20)  # vertical
    canvas.line(puntoBx, puntoY - linea1, puntoBx, puntoY - linea2 + 20)  # vertical

    # PRESTAMO
    linea3 = linea2 - 20
    canvas.setFont('Helvetica-Bold', 8)
    canvas.drawString(puntoAx + 3, puntoY - linea3 - 17, 'PRESTAMO')
    canvas.setFont('Helvetica', 8)

    # HORA
    canvas.drawString(puntoMedio - 120, puntoY - linea3 - 17, 'Hora:')
    canvas.line(puntoMedio - 100, puntoY - linea3 - 5, puntoMedio - 30, puntoY - linea3 - 5)
    canvas.line(puntoMedio - 100, puntoY - linea3 - 23, puntoMedio - 30, puntoY - linea3 - 23)
    canvas.line(puntoMedio - 100, puntoY - linea3 - 5, puntoMedio - 100, puntoY - linea3 - 23)  # vertical
    canvas.line(puntoMedio - 30, puntoY - linea3 - 5, puntoMedio - 30, puntoY - linea3 - 23)  # vertical
    canvas.drawString(puntoMedio - 90, puntoY - linea3 - 17, datos['hora_uso_laboratorio'])
    # FECHA
    canvas.drawString(puntoMedio + 25, puntoY - linea3 - 17, 'Fecha:')
    canvas.line(puntoMedio + 50, puntoY - linea3 - 5, puntoMedio + 170, puntoY - linea3 - 5)
    canvas.line(puntoMedio + 50, puntoY - linea3 - 23, puntoMedio + 170, puntoY - linea3 - 23)
    canvas.line(puntoMedio + 50, puntoY - linea3 - 5, puntoMedio + 50, puntoY - linea3 - 23)  # vertical
    canvas.line(puntoMedio + 170, puntoY - linea3 - 5, puntoMedio + 170, puntoY - linea3 - 23)  # vertical
    canvas.drawString(puntoMedio + 80, puntoY - linea3 - 17, datos['fecha_uso_laboratorio'])
    # OBSERVACIONES
    linea4 = linea3 + 25
    canvas.drawString(puntoMedio - 230, puntoY - linea4 - 20, 'OBSERVACIONES:')
    canvas.line(puntoMedio - 150, puntoY - linea4 - 5, puntoBx, puntoY - linea4 - 5)
    canvas.line(puntoMedio - 150, puntoY - linea4 - 35, puntoBx, puntoY - linea4 - 35)
    canvas.line(puntoMedio - 150, puntoY - linea4 - 5, puntoMedio - 150, puntoY - linea4 - 35)  # vertical
    canvas.line(puntoBx, puntoY - linea4 - 5, puntoBx, puntoY - linea4 - 35)  # vertical
    # FUNCION ACOMODAR TEXTO
    frame2 = Frame(puntoMedio - 150, puntoY - linea4 - 35, 395, 30, showBoundary=1,
                   topPadding=0)  # Frame(movX,movY,margenAncho,mrgenAlto)
    bodyStyle2 = ParagraphStyle('normal', fontSize=10, leading=10, spaceBefore=30)
    s2 = datos['observaciones']
    story2 = [Paragraph(s2, bodyStyle2)]
    story_inframe2 = KeepInFrame(395, 1 * inch, story2)
    frame2.addFromList([story_inframe2], canvas)
    # FIN FUNCION

    # FIRMAS
    linea5 = linea4 + 60
    canvas.drawString(puntoAx + 45, puntoY - linea5 - 13, 'Firma del solicitante')
    canvas.drawString(puntoMedio + 130, puntoY - linea5 - 13, 'Firma del encargado')
    canvas.line(puntoAx, puntoY - linea5, puntoMedio - 90, puntoY - linea5)
    canvas.line(puntoMedio + 80, puntoY - linea5, puntoBx, puntoY - linea5)
    # DEVOLUCIONES
    linea6 = linea5
    canvas.setFont('Helvetica-Bold', 8)
    canvas.drawString(puntoAx + 3, puntoY - linea6 - 35, 'DEVOLUCION')
    canvas.setFont('Helvetica', 8)
    # HORA
    canvas.drawString(puntoMedio - 120, puntoY - linea6 - 35, 'Hora:')
    canvas.line(puntoMedio - 100, puntoY - linea6 - 22, puntoMedio - 30, puntoY - linea6 - 22)
    canvas.line(puntoMedio - 100, puntoY - linea6 - 40, puntoMedio - 30, puntoY - linea6 - 40)
    canvas.line(puntoMedio - 100, puntoY - linea6 - 22, puntoMedio - 100, puntoY - linea6 - 40)  # vertical
    canvas.line(puntoMedio - 30, puntoY - linea6 - 22, puntoMedio - 30, puntoY - linea6 - 40)  # vertical
    canvas.drawString(puntoMedio - 90, puntoY - linea6 - 35, '...')
    # #FECHA
    canvas.drawString(puntoMedio + 25, puntoY - linea6 - 35, 'Fecha:')
    canvas.line(puntoMedio + 50, puntoY - linea6 - 22, puntoMedio + 170, puntoY - linea6 - 22)
    canvas.line(puntoMedio + 50, puntoY - linea6 - 40, puntoMedio + 170, puntoY - linea6 - 40)
    canvas.line(puntoMedio + 50, puntoY - linea6 - 22, puntoMedio + 50, puntoY - linea6 - 40)  # vertical
    canvas.line(puntoMedio + 170, puntoY - linea6 - 22, puntoMedio + 170, puntoY - linea6 - 40)  # vertical
    canvas.drawString(puntoMedio + 80, puntoY - linea6 - 35, '...')
    # OBSERVACIONES
    linea7 = linea6
    canvas.drawString(puntoMedio - 230, puntoY - linea7 - 65, 'OBSERVACIONES:')
    canvas.line(puntoMedio - 150, puntoY - linea7 - 50, puntoBx, puntoY - linea7 - 50)
    canvas.line(puntoMedio - 150, puntoY - linea7 - 80, puntoBx, puntoY - linea7 - 80)
    canvas.line(puntoMedio - 150, puntoY - linea7 - 50, puntoMedio - 150, puntoY - linea7 - 80)  # vertical
    canvas.line(puntoBx, puntoY - linea7 - 50, puntoBx, puntoY - linea7 - 80)  # vertical

    # FUNCION ACOMODAR TEXTO
    frame2 = Frame(puntoMedio - 150, puntoY - linea7 - 80, 395, 30, showBoundary=1,
                   topPadding=0)  # Frame(movX,movY,margenAncho,mrgenAlto)
    bodyStyle2 = ParagraphStyle('normal', fontSize=10, leading=10, spaceBefore=30)
    s2 = "Se devolvio todo"
    story2 = [Paragraph(s2, bodyStyle2)]
    story_inframe2 = KeepInFrame(395, 1 * inch, story2)  # (primer parametro ancho del texto)
    frame2.addFromList([story_inframe2], canvas)
    # FIN FUNCION

    # FIRMAS
    canvas.drawString(puntoAx + 45, puntoY - linea7 - 120, 'Firma del solicitante')
    canvas.drawString(puntoMedio + 130, puntoY - linea7 - 120, 'Firma del encargado')
    canvas.line(puntoAx, puntoY - linea7 - 110, puntoMedio - 90, puntoY - linea7 - 110)
    canvas.line(puntoMedio + 80, puntoY - linea7 - 110, puntoBx, puntoY - linea7 - 110)
    # DATOS ACREDITACION
    linea8y = puntoY - linea7 - 130
    canvas.drawString(puntoAx + 35, linea8y - 10, 'ELABORADO POR')
    canvas.drawString(puntoAx + 210, linea8y - 10, 'REVISADO POR')
    canvas.drawString(puntoAx + 380, linea8y - 10, 'APROBADO POR')

    canvas.line(puntoAx, linea8y, puntoBx, linea8y)
    linea8y = linea8y - 15
    canvas.line(puntoAx, linea8y, puntoBx, linea8y)
    linea8y = linea8y - 25
    canvas.line(puntoAx, linea8y, puntoBx, linea8y)
    canvas.line(puntoAx, linea8y + 40, puntoAx, linea8y)  # vertical
    canvas.line(puntoBx, linea8y + 40, puntoBx, linea8y)  # vertical
    canvas.line(puntoMedio - 90, linea8y + 40, puntoMedio - 90, linea8y)  # vertical
    canvas.line(puntoMedio + 90, linea8y + 40, puntoMedio + 90, linea8y)  # vertical
    # RECOMENDACIONES
    x = linea8y + 112
    canvas.drawString(puntoAx + 3, puntoY - linea7 - 185, 'RECOMENDACIONES')
    canvas.line(puntoAx, puntoY - linea7 - x, puntoBx, puntoY - linea7 - x)
    canvas.line(puntoAx, puntoY - linea7 - 188, puntoBx, puntoY - linea7 - 188)
    canvas.line(puntoAx, puntoY - linea7 - 225, puntoBx, puntoY - linea7 - 225)
    canvas.line(puntoAx, puntoY - linea7 - x, puntoAx, puntoY - linea7 - 225)  # Vertical
    canvas.line(puntoBx, puntoY - linea7 - x, puntoBx, puntoY - linea7 - 225)  # Vertical
    canvas.setFont('Helvetica', 8)
    canvas.drawString(puntoAx + 3, puntoY - linea7 - 200,
                      'Este formulario debe ser entregado al Encargado de Laboratorio con 45 horas de anticipacion a la realizacion de la practica.')
    canvas.drawString(puntoAx + 3, puntoY - linea7 - 210,
                      'El solicitante y el Encargado deben verificar en detalle los insumos al momento de la entrega y devolucion. La firma de este documento,')
    canvas.drawString(puntoAx + 3, puntoY - linea7 - 220,
                      'por parte del solicitante, avala la conformidad y lo hace responsable por danos o el hurto de los materiales y equipos solicitados')

    # FIN COPIAR

    canvas.save()
    pdf_out = output.getvalue()

    output.close()
    filename = 'uso_de_laboratorio.pdf'
    response = make_response(pdf_out)
    response.headers['Content-Disposition'] = "attachment; filename"
    response.mimetype = 'application/pdf'
    # return response
    return send_file(filename, as_attachment=False)


# ################################# REPORTE_SOLICITUD_DE PRETAMO DE EQUIPOS ##################################


def solicitud_de_prestamo_de_equipos_de_laboratorio(datos_equipos):
    datos=datos_equipos[1]

    output = cStringIO.StringIO()
    canvas = Canvas("prestamo_de_equipos.pdf", pagesize=letter)
    canvas.setLineWidth(.3)
    canvas.setFont('Helvetica', 10)

    canvas.saveState()
    # canvas = canvas.Canvas(self.nombrePDF, pagesize=letter)
    canvas.setLineWidth(.3)
    canvas.setFont('Helvetica', 10)

    canvas.line(60, 760, 550, 760)  # punto x1, y1 , x2, y2 #HORIZONTAL
    canvas.line(60, 760, 60, 700)  # VERTICAL
    canvas.line(60, 700, 550, 700)  # HORIZONTAL
    canvas.line(550, 760, 550, 700)  # VERTICAL
    canvas.line(190, 760, 190, 700)  # VERTICAL
    canvas.line(400, 760, 400, 700)  # VERTICAL
    # CAJETIN PEQUENO
    canvas.line(400, 745, 550, 745)  # HORIZONTAL
    canvas.line(400, 730, 550, 730)  # HORIZONTAL
    canvas.line(400, 715, 550, 715)  # HORIZONTAL
    canvas.line(470, 760, 470, 715)  # VERTICAL
    # Inseratmos la imagen en el documento
    # canvas.drawImage('emi.jpeg', -50, 500)#Imagen estatica
    canvas.drawImage("static/img/emi.jpeg", 70, 710, width=115, height=40)
    # TITULO
    # Modificar texto
    frame1 = Frame(190, 700, 210, 60, showBoundary=1)  # Frame(movX,movY,margenAncho,mrgenAlto)
    bodyStyle = ParagraphStyle('normal', fontSize=24, leading=28, spaceBefore=30, alignment=TA_CENTER)
    s = datos_equipos[0]
    story = [Paragraph(s, bodyStyle)]
    story_inframe = KeepInFrame(210, 1 * inch, story)
    frame1.addFromList([story_inframe], canvas)
    #

    # DATOS
    posx = 410
    canvas.setFont('Helvetica', 10)
    canvas.drawString(posx, 750, 'Codigo:')
    canvas.drawString(posx, 735, 'Aprobacion:')
    canvas.drawString(posx, 720, 'Version:')
    canvas.drawString(posx + 70, 750, 'C5117-9')
    canvas.drawString(posx + 70, 735, 'Aprobado')
    canvas.drawString(posx + 70, 720, 'Version 1.1')

    # SEGUNDA CAJETILLA
    puntoAx = 60
    puntoBx = 550

    puntoY = 698
    canvas.line(puntoAx, puntoY, puntoBx, puntoY)
    canvas.line(puntoAx, puntoY - 20, puntoBx, puntoY - 20)
    canvas.setFont('Helvetica', 8)
    canvas.drawString(puntoAx + 3, puntoY - 8, 'Unidad administrativa:')
    canvas.drawString(puntoAx + 3, puntoY - 17, 'Direccion Nacional de Investigacion Ciencia y Tecnologia')

    puntoMedio = (puntoAx + puntoBx) / 2

    canvas.line(puntoMedio, puntoY, puntoMedio, puntoY - 20)  # vertical
    canvas.drawString(puntoMedio + 3, puntoY - 8, 'Area Responsable:')
    canvas.drawString(puntoMedio + 3, puntoY - 17, 'Normalizacion de Laboratorios y Registro')
    canvas.line(puntoAx, puntoY - 35, puntoBx, puntoY - 35)
    canvas.setFont('Helvetica-Bold', 9)
    canvas.drawString(puntoMedio - 70, puntoY - 30, 'REQUERIMIENTOS DE LABORATORIO')
    canvas.line(puntoAx, puntoY, puntoAx, puntoY - 35)  # vertical
    canvas.line(puntoBx, puntoY, puntoBx, puntoY - 35)  # vertical

    # siguiente cajetilla
    cajetin_pequeno = 150
    canvas.line(puntoAx, puntoY - 37, puntoBx, puntoY - 37)  #
    canvas.line(puntoAx, puntoY - 46, puntoBx, puntoY - 46)  #
    canvas.line(puntoAx, puntoY - 64, puntoBx, puntoY - 64)  #
    canvas.line(puntoAx, puntoY - 37, puntoAx, puntoY - 64)  # vertical
    canvas.line(puntoBx, puntoY - 37, puntoBx, puntoY - 64)  # vertical
    canvas.line(puntoBx - cajetin_pequeno, puntoY - 37, puntoBx - cajetin_pequeno, puntoY - 64)  # vertical
    canvas.setFont('Helvetica', 8)
    canvas.drawString(puntoAx + 130, puntoY - 45, 'Nombre del solictante')
    canvas.drawString(puntoAx + 410, puntoY - 45, 'C.I.')
    # datos
    canvas.setFont('Helvetica', 10)
    canvas.drawString(puntoAx + 100, puntoY - 60, datos['nombre'])
    canvas.drawString(puntoAx + 390, puntoY - 60, datos['ci'])

    # Siguiente cajetin
    division = 150
    canvas.line(puntoAx, puntoY - 67, puntoBx, puntoY - 67)  #
    canvas.line(puntoAx, puntoY - 76, puntoBx, puntoY - 76)  #
    canvas.line(puntoAx, puntoY - 94, puntoBx, puntoY - 94)  #
    canvas.line(puntoAx, puntoY - 67, puntoAx, puntoY - 94)  # vertical
    canvas.line(puntoBx, puntoY - 67, puntoBx, puntoY - 94)  # vertical
    canvas.line(puntoAx + division, puntoY - 67, puntoAx + division, puntoY - 94)  # vertical
    canvas.line(puntoBx - division, puntoY - 67, puntoBx - division, puntoY - 94)  # vertical
    # canvas.setFont('Helvetica', 8)
    canvas.drawString(puntoAx + 60, puntoY - 75, 'Carrera:')
    canvas.drawString(puntoAx + 210, puntoY - 75, 'Sala de trabajo:')
    canvas.drawString(puntoAx + 400, puntoY - 75, 'Asignatura:')
    # datos
    canvas.setFont('Helvetica', 10)
    canvas.drawString(puntoAx + 30, puntoY - 90, datos['carrera'])
    canvas.drawString(puntoAx + 190, puntoY - 90, datos['sala_de_trabajo'])
    canvas.drawString(puntoAx + 350, puntoY - 90, datos['asignatura'])

    # Sigueinte Cajetilla
    # cajetin_pequeno=150
    canvas.drawString(puntoAx + 3, puntoY - 105, 'Proposito de uso de equipos(s):')
    canvas.line(puntoAx, puntoY - 110, puntoBx, puntoY - 110)  #
    canvas.line(puntoAx, puntoY - 143, puntoBx, puntoY - 143)  #

    canvas.line(puntoAx, puntoY - 110, puntoAx, puntoY - 143)  # vertical
    canvas.line(puntoBx, puntoY - 110, puntoBx, puntoY - 143)  # vertical

    # FUNCION ACOMODAR TEXTO
    frame2 = Frame(puntoAx, puntoY - 143, 490, 33, showBoundary=1,
                   topPadding=0)  # Frame(movX,movY,margenAncho,mrgenAlto)
    bodyStyle2 = ParagraphStyle('normal', fontSize=10, leading=10, spaceBefore=30)
    s2 = datos['proposito_uso_de_equipo']
    story2 = [Paragraph(s2, bodyStyle2)]
    story_inframe2 = KeepInFrame(490, 1 * inch, story2)
    frame2.addFromList([story_inframe2], canvas)
    # FIN FUNCION

    # TABLAS MATERIALES
    linea = 160
    canvas.drawString(puntoAx + 3, puntoY - linea + 3, 'Equipos solicitados:')

    lista_equipos = [datos['equipos'][0], datos['equipos'][1], datos['equipos'][2],
                     datos['equipos'][3], datos['equipos'][4], datos['equipos'][5],
                     datos['equipos'][6],
                     datos['equipos'][7], datos['equipos'][8], datos['equipos'][9], "Equipos K",
                     "Equipos L", "Equipos M", "Equipos N"]
    cont = 0
    for i in range(8):
        canvas.line(puntoAx, puntoY - linea, puntoBx, puntoY - linea)
        if i <= 6:
            canvas.drawString(puntoAx + 5, puntoY - linea - 10, lista_equipos[cont])
            canvas.drawString(puntoMedio + 5, puntoY - linea - 10, lista_equipos[cont + 1])
            if i <= 5:
                cont = cont + 2
        linea = linea + 20

    canvas.line(puntoMedio, puntoY - 160, puntoMedio, puntoY - linea + 20)  # vertical
    canvas.line(puntoAx, puntoY - 160, puntoAx, puntoY - linea + 20)  # vertical
    canvas.line(puntoBx, puntoY - 160, puntoBx, puntoY - linea + 20)  # vertical

    # PRESTAMO
    linea3 = 400 - 20
    canvas.setFont('Helvetica-Bold', 8)
    canvas.drawString(puntoAx + 3, puntoY - linea3 - 17, 'PRESTAMO')
    canvas.setFont('Helvetica', 8)

    # HORA
    canvas.drawString(puntoMedio - 120, puntoY - linea3 - 17, 'Hora:')
    canvas.line(puntoMedio - 100, puntoY - linea3 - 5, puntoMedio - 30, puntoY - linea3 - 5)
    canvas.line(puntoMedio - 100, puntoY - linea3 - 23, puntoMedio - 30, puntoY - linea3 - 23)
    canvas.line(puntoMedio - 100, puntoY - linea3 - 5, puntoMedio - 100, puntoY - linea3 - 23)  # vertical
    canvas.line(puntoMedio - 30, puntoY - linea3 - 5, puntoMedio - 30, puntoY - linea3 - 23)  # vertical
    canvas.drawString(puntoMedio - 90, puntoY - linea3 - 17, datos['hora_uso_de_equipo'])
    # FECHA
    canvas.drawString(puntoMedio + 25, puntoY - linea3 - 17, 'Fecha:')
    canvas.line(puntoMedio + 50, puntoY - linea3 - 5, puntoMedio + 170, puntoY - linea3 - 5)
    canvas.line(puntoMedio + 50, puntoY - linea3 - 23, puntoMedio + 170, puntoY - linea3 - 23)
    canvas.line(puntoMedio + 50, puntoY - linea3 - 5, puntoMedio + 50, puntoY - linea3 - 23)  # vertical
    canvas.line(puntoMedio + 170, puntoY - linea3 - 5, puntoMedio + 170, puntoY - linea3 - 23)  # vertical
    canvas.drawString(puntoMedio + 80, puntoY - linea3 - 17, datos['fecha_uso_de_equipo'])
    # OBSERVACIONES
    linea4 = linea3 + 25
    canvas.drawString(puntoMedio - 230, puntoY - linea4 - 20, 'OBSERVACIONES:')
    canvas.line(puntoMedio - 150, puntoY - linea4 - 5, puntoBx, puntoY - linea4 - 5)
    canvas.line(puntoMedio - 150, puntoY - linea4 - 35, puntoBx, puntoY - linea4 - 35)
    canvas.line(puntoMedio - 150, puntoY - linea4 - 5, puntoMedio - 150, puntoY - linea4 - 35)  # vertical
    canvas.line(puntoBx, puntoY - linea4 - 5, puntoBx, puntoY - linea4 - 35)  # vertical

    # FUNCION ACOMODAR TEXTO
    frame2 = Frame(puntoMedio - 150, puntoY - linea4 - 35, 395, 30, showBoundary=1,
                   topPadding=0)  # Frame(movX,movY,margenAncho,mrgenAlto)
    bodyStyle2 = ParagraphStyle('normal', fontSize=10, leading=10, spaceBefore=30)
    s2 = datos['observaciones']
    print "s2", s2
    print type(datos['observaciones'])
    story2 = [Paragraph(s2, bodyStyle2)]
    story_inframe2 = KeepInFrame(395, 1 * inch, story2)
    frame2.addFromList([story_inframe2], canvas)
    # FIN FUNCION

    # FIRMAS
    linea5 = linea4 + 60
    canvas.drawString(puntoAx + 45, puntoY - linea5 - 13, 'Firma del solicitante')
    canvas.drawString(puntoMedio + 130, puntoY - linea5 - 13, 'Firma del encargado')
    canvas.line(puntoAx, puntoY - linea5, puntoMedio - 90, puntoY - linea5)
    canvas.line(puntoMedio + 80, puntoY - linea5, puntoBx, puntoY - linea5)
    # DEVOLUCIONES
    linea6 = linea5
    canvas.setFont('Helvetica-Bold', 8)
    canvas.drawString(puntoAx + 3, puntoY - linea6 - 35, 'DEVOLUCION')
    canvas.setFont('Helvetica', 8)
    # HORA
    canvas.drawString(puntoMedio - 120, puntoY - linea6 - 35, 'Hora:')
    canvas.line(puntoMedio - 100, puntoY - linea6 - 22, puntoMedio - 30, puntoY - linea6 - 22)
    canvas.line(puntoMedio - 100, puntoY - linea6 - 40, puntoMedio - 30, puntoY - linea6 - 40)
    canvas.line(puntoMedio - 100, puntoY - linea6 - 22, puntoMedio - 100, puntoY - linea6 - 40)  # vertical
    canvas.line(puntoMedio - 30, puntoY - linea6 - 22, puntoMedio - 30, puntoY - linea6 - 40)  # vertical
    canvas.drawString(puntoMedio - 90, puntoY - linea6 - 35, '...')
    # #FECHA
    canvas.drawString(puntoMedio + 25, puntoY - linea6 - 35, 'Fecha:')
    canvas.line(puntoMedio + 50, puntoY - linea6 - 22, puntoMedio + 170, puntoY - linea6 - 22)
    canvas.line(puntoMedio + 50, puntoY - linea6 - 40, puntoMedio + 170, puntoY - linea6 - 40)
    canvas.line(puntoMedio + 50, puntoY - linea6 - 22, puntoMedio + 50, puntoY - linea6 - 40)  # vertical
    canvas.line(puntoMedio + 170, puntoY - linea6 - 22, puntoMedio + 170, puntoY - linea6 - 40)  # vertical
    canvas.drawString(puntoMedio + 80, puntoY - linea6 - 35, '...')
    # OBSERVACIONES
    linea7 = linea6
    canvas.drawString(puntoMedio - 230, puntoY - linea7 - 65, 'OBSERVACIONES:')
    canvas.line(puntoMedio - 150, puntoY - linea7 - 50, puntoBx, puntoY - linea7 - 50)
    canvas.line(puntoMedio - 150, puntoY - linea7 - 80, puntoBx, puntoY - linea7 - 80)
    canvas.line(puntoMedio - 150, puntoY - linea7 - 50, puntoMedio - 150, puntoY - linea7 - 80)  # vertical
    canvas.line(puntoBx, puntoY - linea7 - 50, puntoBx, puntoY - linea7 - 80)  # vertical

    # FUNCION ACOMODAR TEXTO
    frame2 = Frame(puntoMedio - 150, puntoY - linea7 - 80, 395, 30, showBoundary=1,
                   topPadding=0)  # Frame(movX,movY,margenAncho,mrgenAlto)
    bodyStyle2 = ParagraphStyle('normal', fontSize=10, leading=10, spaceBefore=30)
    s2 = "Se devolvio todo como tenia q ser todo tranquilo y positivo papu genial"
    story2 = [Paragraph(s2, bodyStyle2)]
    story_inframe2 = KeepInFrame(395, 1 * inch, story2)  # (primer parametro ancho del texto)
    frame2.addFromList([story_inframe2], canvas)
    # FIN FUNCION

    # FIRMAS
    canvas.drawString(puntoAx + 45, puntoY - linea7 - 120, 'Firma del solicitante')
    canvas.drawString(puntoMedio + 130, puntoY - linea7 - 120, 'Firma del encargado')
    canvas.line(puntoAx, puntoY - linea7 - 110, puntoMedio - 90, puntoY - linea7 - 110)
    canvas.line(puntoMedio + 80, puntoY - linea7 - 110, puntoBx, puntoY - linea7 - 110)
    # DATOS ACREDITACION
    linea8y = puntoY - linea7 - 130
    canvas.drawString(puntoAx + 35, linea8y - 10, 'ELABORADO POR')
    canvas.drawString(puntoAx + 210, linea8y - 10, 'REVISADO POR')
    canvas.drawString(puntoAx + 380, linea8y - 10, 'APROBADO POR')

    canvas.line(puntoAx, linea8y, puntoBx, linea8y)
    linea8y = linea8y - 15
    canvas.line(puntoAx, linea8y, puntoBx, linea8y)
    linea8y = linea8y - 25
    canvas.line(puntoAx, linea8y, puntoBx, linea8y)
    canvas.line(puntoAx, linea8y + 40, puntoAx, linea8y)  # vertical
    canvas.line(puntoBx, linea8y + 40, puntoBx, linea8y)  # vertical
    canvas.line(puntoMedio - 90, linea8y + 40, puntoMedio - 90, linea8y)  # vertical
    canvas.line(puntoMedio + 90, linea8y + 40, puntoMedio + 90, linea8y)  # vertical
    # RECOMENDACIONES
    x = linea8y + 112
    canvas.drawString(puntoAx + 3, puntoY - linea7 - 185, 'RECOMENDACIONES')
    canvas.line(puntoAx, puntoY - linea7 - x, puntoBx, puntoY - linea7 - x)
    canvas.line(puntoAx, puntoY - linea7 - 188, puntoBx, puntoY - linea7 - 188)
    canvas.line(puntoAx, puntoY - linea7 - 225, puntoBx, puntoY - linea7 - 225)
    canvas.line(puntoAx, puntoY - linea7 - x, puntoAx, puntoY - linea7 - 225)  # Vertical
    canvas.line(puntoBx, puntoY - linea7 - x, puntoBx, puntoY - linea7 - 225)  # Vertical
    canvas.setFont('Helvetica', 8)

    canvas.drawString(puntoAx + 3, puntoY - linea7 - 200,
                      'El solicitante y el encargado deben verificar en detalle los equipos al momento de la entrega y recepcion.')
    canvas.drawString(puntoAx + 3, puntoY - linea7 - 210,
                      'La firma de este documento avala la conformidad y lo hace responsable por danos o el hurto de los equipos solicitados.')

    # FIN COPIAR

    canvas.save()
    pdf_out = output.getvalue()

    output.close()
    filename = 'prestamo_de_equipos.pdf'
    response = make_response(pdf_out)
    response.headers['Content-Disposition'] = "attachment; filename"
    response.mimetype = 'application/pdf'
    # return response
    return send_file(filename, as_attachment=False)





if __name__=='__main__':
    # app.run(debug=True)
    app.run(debug=True,host='0.0.0.0') #para el celular ip:5000

