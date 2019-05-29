# coding=utf-8 mostrar_roles
from reportes import reportePDF
from suelos import ensayo
# from flask_pymongo import PyMongo
import pymongo
from flask import Flask,session,jsonify
from flask_mail import Mail,Message
import bcrypt
import time
import os
import requests
import numpy
app=Flask(__name__)

#CONFIGURACION ENVIO EMAIL reporte_formulario_solicitud_laboratorio
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'civilemicbba@gmail.com'
app.config['MAIL_PASSWORD'] = 'EsCuElAMILITARiNgEnIeRiA-civil68'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail=Mail(app)



#FIN CONFIGURACION

mongo = pymongo.MongoClient("mongodb://Carlosc13:Familia123@cluster0-shard-00-00-9oxf8.mongodb.net:27017,cluster0-shard-00-01-9oxf8.mongodb.net:27017,cluster0-shard-00-02-9oxf8.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true") #instanciar conexion con MongoDB
db = mongo["civil_emi"]

# app.config['MONGO_DBNAME'] = 'civil_emi'
# app.config['MONGO_URI'] = 'mongodb://localhost:27017/civil_emi'
# mongo = PyMongo(app)


class controler:


    def __init__(self):
        pass


    def ingresar_alsistema(self, nombre,password):
        empleados = db['empleados']
        login_user = empleados.find_one({'username': nombre})


        if login_user and bcrypt.hashpw(password.encode('utf-8'), login_user['password'].encode('utf-8')) == login_user['password'].encode('utf-8') and login_user['estado'].encode('utf-8')=='Habilitado':
            session['username'] = login_user['cargo'].encode('utf-8')
            session['roles'] = login_user['rol'].encode('utf-8')
            session['datos_sol_lab']=login_user
            session['tipo']=login_user['tipo'].encode('utf-8')
            session['cedula'] = login_user['ci'].encode('utf-8')
            rolesss=db['rol_user']
            privilegios = rolesss.find_one({'rol': session['roles']})
            session['rol'] = privilegios['privilegios']
            return True
        else:
            login_user2 = empleados.find_one({'email': nombre})
            if login_user2 and bcrypt.hashpw(password.encode('utf-8'), login_user2['password'].encode('utf-8')) == login_user2['password'].encode('utf-8') and login_user2['estado'].encode('utf-8')=='Habilitado':
                session['username'] = login_user2['cargo'].encode('utf-8')
                session['roles'] = login_user2['rol'].encode('utf-8')
                session['tipo'] = login_user2['tipo'].encode('utf-8')
                session['cedula'] = login_user2['ci'].encode('utf-8')
                session['datos_sol_lab'] = login_user2
                rolesss=db['rol_user']
                privilegios = rolesss.find_one({'rol': session['roles']})
                session['rol'] = privilegios['privilegios']
                return True
            else:

                estudiantes = db['estudiantes']
                login_estudiante = estudiantes.find_one({'username': nombre})



                if login_estudiante and bcrypt.hashpw(password.encode('utf-8'), login_estudiante['password'].encode('utf-8')) == login_estudiante['password'].encode('utf-8') and login_estudiante['estado'].encode('utf-8')=='Habilitado':
                    session['username'] = login_estudiante['nombres'].encode('utf-8')
                    session['roles'] = login_estudiante['rol'].encode('utf-8')
                    session['cedula'] = login_estudiante['ci'].encode('utf-8')
                    session['tipo'] = login_estudiante['tipo'].encode('utf-8')
                    session['datos_sol_lab'] = login_estudiante
                    rolesss=db['rol_user']
                    privilegios = rolesss.find_one({'rol': session['roles']})
                    session['rol'] = privilegios['privilegios']
                    return True
                else:
                    return False




                    
#******************************* EMPLEADO **********************************************************************************************************************************
    def crear_empleado(self,nombre_usuario,contrasena,rol,estado,nombre,apellido,ci,especialidad,email,cargo,ff):
        empleados = db['empleados']
        if empleados.find_one({'_id': 1}) is None:
            id_max = 1

        else:
            id_max = self.buscar_id_max(empleados)
        existing_user = empleados.find_one({'username' : nombre_usuario}) # consulta a la base de datos para ver si existe el usuario en la basa de datos
        existing_user2 = empleados.find_one({'ci' : ci}) # consulta a la base de datos para ver si existe el usuario en la basa de datos
        if existing_user is None and existing_user2 is None: # si el usuario no existe en la bae de datos entra
            #MICROSERVICES USERS
            url = 'https://emi-civil-microservicios-user.herokuapp.com/registrar_empleado/' + nombre_usuario + ',' + contrasena + ',' + rol + ',' + estado + ',' + nombre + ',' + apellido + ',' + ci + ',' + especialidad + ',' + email + ',' + cargo + ',' + time.strftime("%Y-%m-%d") + ',' + ff + ',' + str(id_max)
            valores = requests.post(url)
            dato = valores.json()
            return dato['respuesta']
        else:
            return False


    def mostrar_empleado(self):
        empleado_completo=[]
        empleados = db['empleados']
        list_empleados = empleados.find()
        for i in list_empleados:
            user = []
            v1 = i["_id"]
            v2 = i["username"]
            v4 = i["rol"]
            v5 = i["estado"]
            v6 = i["nombres"]
            v7 = i["apellidos"]
            v8 = i["especialidad"]
            v9 = i["ci"]
            v10 = i["email"]
            v11 = i["cargo"]
            v12 = i["fecha_inicio"]
            v13 = i["fecha_baja"]
            v14 = i["password"]
            user.append(v1)
            user.append(v2)
            user.append(v4)
            user.append(v5)
            user.append(v6)
            user.append(v7)
            user.append(v8)
            user.append(v9)
            user.append(v10)
            user.append(v11)
            user.append(v12)
            user.append(v13)
            user.append(v14)
            empleado_completo.append(tuple(user))
        return tuple(empleado_completo)

    def actualizar_empleado(self,id,nombre_usuario,contrasena,rol,estado,nombre,apellido,ci,especialidad,email,cargo,ff):
        empleados = db['empleados']
        if id=='1':
            return False
        else:

           if empleados.find_one({'password': contrasena}):# entra cuando la contraseña igual XD
               contrasena='1'


           existing_user = empleados.find_one({'username': nombre_usuario,'password': contrasena,"rol": rol, "estado": estado, "nombres": nombre, "apellidos": apellido, "especialidad": especialidad, "email": email, "cargo": cargo, "fecha_baja": ff})  # consulta a la base de datos para ver si existe el usuario en la basa de datos
           existing_user2 = empleados.find_one({'ci': ci})
           if existing_user is None:  # si el usuario no existe en la bae de datos entra
                #MICROSERVICIOS USERS
                url = 'https://emi-civil-microservicios-user.herokuapp.com/editar_empleado/' + str(id) + ',' + nombre_usuario + ',' + contrasena + ',' + rol + ',' + estado + ',' + nombre + ',' + apellido + ',' + ci + ',' + especialidad + ',' + email + ',' + cargo + ',' + ff
                # url = 'https://emi-labcivil-users.herokuapp.com/editar_empleado/' + str(id) + ',' + nombre_usuario + ',' + contrasena + ',' + rol + ',' + estado + ',' + nombre + ',' + apellido + ',' + ci + ',' + especialidad + ',' + email + ',' + cargo + ',' + ff
                valores = requests.post(url)
                dato = valores.json()
                return dato['respuesta']

           else:
              return False




    def eliminar_empleado(self,id):
        if id=='1':
            return False
        else:
            url = 'https://emi-civil-microservicios-user.herokuapp.com/eliminar_empleado/' + str(id)
            valores = requests.post(url)
            dato = valores.json()
            return dato['respuesta']



    def reporte_empleado(self):
        coleccion = db['empleados']  # conectar con las colecciones
        titulo = "LISTA DE EMPLEADOS"
        cabecera = (("_id", "Codigo"), ("username", "Usuario"), ("rol", "Rol"), ("estado", "Estado"), ("nombres", "Nombres"),
        ("apellidos", "Apellidos"), ("especialidad", "Especialidad"), ("ci", "Ci"), ("email", "Email"),)
        nombrepdf=session['cedula']+"empelado"+"reporte.pdf"
        return self.reportes_tablas(coleccion,titulo,cabecera,nombrepdf)

#************************************************************* EMPLEADO FIN  ******************************************************
  




#************************************************************* ESTUDIANTES  ******************************************************
  
    
    def crear_estudiante(self,nombre_usuario,contrasena,rol,semestre,nombre,apellido,ci,codigo,correo,estado):
        estudiantes = db['estudiantes']
        if nombre_usuario == 'Administrador' or nombre_usuario == 'administrador':
            return False
        else:
            if estudiantes.find_one({'_id' : 1}) is None:
                id_max = 1
            else:
                id_max = self.buscar_id_max(estudiantes)
            existing_user = estudiantes.find_one({'username' : nombre_usuario}) # consulta a la base de datos para ver si existe el usuario en la basa de datos
            existing_user2 = estudiantes.find_one({'ci': ci})
            if existing_user is None and existing_user2 is None: # si el usuario no existe en la bae de datos entra

                msg = Message('ESCUELA MILITAR DE INGENIERIA', sender='civilemicbba@gmail.com',
                              recipients=[correo])
                msg.body = 'Querido usuari@ : ' + '' + nombre + '' + ' su user es : ' + "su codigo de estudiante" + ' y su password es : ' + contrasena + ' '  + ' ' + "con el podra ingresar al sistema" + ''
                mail.send(msg)
                #MICROSERVICIOS ESTUDIANTE
                url = 'https://emi-civil-microservicios-user.herokuapp.com/registrar_estudiante/' + nombre_usuario + ',' + contrasena + ',' + rol + ',' + semestre + ',' + nombre + ',' + apellido + ',' + ci + ',' + codigo + ',' + correo + ','+ str(id_max) + ',' + estado
                valores = requests.post(url)
                dato = valores.json()
                return dato['respuesta']
            else:
                return False



    def actualizar_estudiante(self,id,rol,semestre,nombre,apellido,ci,codigo,correo,estado):
        estudiantes = db['estudiantes']

        existing_user = estudiantes.find_one({"rol": rol, "semestre": semestre,"nombres": nombre, "apellidos": apellido,"correo": correo,"estado": estado})  # consulta a la base de datos para ver si existe el usuario en la basa de datos
        existing_user1 = estudiantes.find_one({'codigo': codigo})
        existing_user2 = estudiantes.find_one({'ci': ci})

        if existing_user is None:
                # MICROSERVICIOS ESTUDIANTE
            url = 'https://emi-civil-microservicios-user.herokuapp.com/editar_estudiante/'+ str(id) + ',' + rol + ',' + semestre + ',' + nombre + ',' + apellido + ',' + ci + ',' + codigo + ',' + correo + ',' + estado
            # url = 'https://emi-labcivil-users.herokuapp.com/editar_estudiante/'+ str(id) + ',' + rol + ',' + semestre + ',' + nombre + ',' + apellido + ',' + ci + ',' + codigo + ',' + correo
            valores = requests.post(url)

            dato = valores.json()
            return dato['respuesta']

        if existing_user1 is None:
                # MICROSERVICIOS ESTUDIANTE
            url = 'https://emi-civil-microservicios-user.herokuapp.com/editar_estudiante/'+ str(id) + ',' + rol + ',' + semestre + ',' + nombre + ',' + apellido + ',' + ci + ',' + codigo + ',' + correo + ',' + estado

            valores = requests.post(url)

            dato = valores.json()
            return dato['respuesta']

        if existing_user2 is None:
                # MICROSERVICIOS ESTUDIANTE
            url = 'https://emi-civil-microservicios-user.herokuapp.com/editar_estudiante/'+ str(id) + ',' + rol + ',' + semestre + ',' + nombre + ',' + apellido + ',' + ci + ',' + codigo + ',' + correo + ',' + estado

            valores = requests.post(url)

            dato = valores.json()
            return dato['respuesta']




        else:
            return False




    def mostrar_estudiante(self):
        estudiante_completo=[]
        estudiantes = db['estudiantes']
        list_estudiantes = estudiantes.find()
        for i in list_estudiantes:
            user = []
            v1 = i["_id"]
            v2 = i["username"]
            v3 = i["password"]
            v4 = i["rol"]
            v5 = i["semestre"]
            v6 = i["nombres"]
            v7 = i["apellidos"]
            v8 = i["ci"]
            v9 = i["codigo"]
            v10 = i["email"]
            v11 = i["estado"]
            user.append(v1)
            user.append(v2)
            user.append(v3)
            user.append(v4)
            user.append(v5)
            user.append(v6)
            user.append(v7)
            user.append(v8)
            user.append(v9)
            user.append(v10)
            user.append(v11)
            estudiante_completo.append(tuple(user))
        return tuple(estudiante_completo)


    def eliminar_estudiante(self,id):
        estudiantes = db['estudiantes']
        url = 'https://emi-civil-microservicios-user.herokuapp.com/eliminar_estudiante/' + str(id)
        valores = requests.post(url)
        dato = valores.json()
        return dato['respuesta']


    def reporte_estudiante(self):
        coleccion = db['estudiantes']  # conectar con las colecciones
        titulo = "LISTA DE ESTUDIANTES"
        cabecera = (("_id", "Codigo"),
                    ("username", "Usuario"),
                    ("rol", "Rol"),
                    ("semestre", "Semestre"),
                    ("nombres", "Nombres"),
                    ("apellidos", "Apellidos"),
                    ("ci", "Ci"),
                    ("codigo", "Codigo"),)
        nombrepdf = session['cedula'] + "estudiante" + "reporte.pdf"
        return self.reportes_tablas(coleccion,titulo,cabecera,nombrepdf)

# ************************************************************* ESTUDIANTES FIN  ******************************************************






# ************************************************************* ADMINISTRAR ROLES INICIO  ******************************************************

    def crear_rol(self,rol_usuario,privilegios):
        rol = db['rol_user']
        if rol.find_one({'_id' : 1}) is None:
            id_max = 1
        else:
            id_max = self.buscar_id_max(rol)
        existing_rol_user = rol.find_one({'rol' : rol_usuario}) # consulta a la base de datos para ver si existe el usuario en la basa de datos
        if existing_rol_user is None : # si el usuario no existe en la bae de datos entra
            self.guardar_rol(rol_usuario,id_max,privilegios)
            return True
        else:
            return False


    def guardar_rol(self,rol_usuario,id_max,privilegios):
        rol = db['rol_user']

        almacenar = {
            '_id': id_max,
            'rol':rol_usuario,
            'privilegios':privilegios
        }
        rol.insert(almacenar)
        return True

    def mostrar_roles(self):
        rol_completo=[]
        roles = db['rol_user']
        list_roles = roles.find()
        for i in list_roles:
            rol = []
            v1 = i["_id"]
            v2 = i["rol"]
            v3 = i["privilegios"]
            rol.append(v1)
            rol.append(v2)
            rol.append(v3)
            rol_completo.append(tuple(rol))
        return tuple(rol_completo)

    def actualizar_roles(self,id,rol,privilegios):

        if id== "1":
            return False
        else:
            roles = db['rol_user']
            existing_user = roles.find_one({'rol': rol,"privilegios": privilegios})  # consulta a la base de datos para ver si existe el usuario en la basa de datos
            if existing_user is None:
                roles.update({"_id": {"$eq": float(id)}}, {"$set": {"rol": rol,"privilegios": privilegios}},upsert=False, multi=False)
                response = {'respuesta': "Modificado"}
                return jsonify(response)
            else:
                return False

    def eliminar_rol(self,id):
        if id =="1":
            return False
        else:
            rol = db['rol_user']
            rol.remove({'_id': float(id)})
            return True

# ************************************************************* ADMINISTRAR ROLES FIN  ******************************************************




# ************************************************************* ADMINISTRAR CLIENTES FIN  ******************************************************
    def crear_cliente(self, nombre_cliente,apellido_cliente,ci_cliente,email_cliente,telefono_cliente):
        clientes = db['clientes']
        if nombre_cliente == 'Administrador' or nombre_cliente == 'administrador':
            return False

        else:
            if clientes.find_one({'_id': 1}) is None:
                id_max = 1
            else:
                id_max = self.buscar_id_max(clientes)
            existing_user = clientes.find_one({'ci_cliente': ci_cliente})  # consulta a la base de datos para ver si existe el usuario en la basa de datos
            if existing_user is None:  # si el usuario no existe en la bae de datos entra

                return self.guardar_cliente(nombre_cliente,apellido_cliente,ci_cliente,email_cliente,telefono_cliente,id_max)

            else:
                return False
    #
    def guardar_cliente(self,nombre_cliente,apellido_cliente,ci_cliente,email_cliente,telefono_cliente,id_max):
        clientes = db['clientes']
        almacenar = {'_id': id_max,'nombres_cliente':nombre_cliente,'apellidos_cliente':apellido_cliente,'ci_cliente':ci_cliente,'email_cliente': email_cliente,'telefono_cliente': telefono_cliente}
        clientes.insert(almacenar)
        response = {'respuesta': "Creado"}
        return jsonify(response)

    def mostrar_clientes(self):
        clientes_completo=[]
        clientes = db['clientes']
        list_clientes = clientes.find()
        for i in list_clientes:
            client = []
            v1 = i["_id"]
            v2 = i["nombres_cliente"]
            v4 = i["apellidos_cliente"]
            v5 = i["ci_cliente"]
            v6 = i["email_cliente"]
            v7 = i["telefono_cliente"]
            client.append(v1)
            client.append(v2)
            client.append(v4)
            client.append(v5)
            client.append(v6)
            client.append(v7)
            clientes_completo.append(tuple(client))
        return tuple(clientes_completo)

    def actualizar_cliente(self,id,nombre_cliente,apellido_cliente,ci_cliente,email_cliente,telefono_cliente):#*********************** pendiente la contasena ******************************************
        clientes = db['clientes']
        if nombre_cliente == 'Administrador' or nombre_cliente == 'administrador':
            return False

        else:
            existing_user = clientes.find_one({'nombres_cliente': nombre_cliente, "apellidos_cliente":apellido_cliente,"ci_cliente": ci_cliente, "email_cliente": email_cliente,"telefono_cliente": telefono_cliente})  # consulta a la base de datos para ver si existe el usuario en la basa de datos
            if existing_user is None:
                clientes.update({"_id": {"$eq": int(id)}}, {"$set": {"nombres_cliente": nombre_cliente, "apellidos_cliente": apellido_cliente, "ci_cliente": ci_cliente, "email_cliente": email_cliente, "telefono_cliente": telefono_cliente}},
                                    upsert=False, multi=False)
                response = {'respuesta': "Modificado"}
                return jsonify(response)
            else:
                return False

    def eliminar_cliente(self,id):
        clientes = db['clientes']
        clientes.remove({'_id': int(id)})
        return True

    def reporte_cliente(self):
        coleccion = db['clientes']  # conectar con las colecciones
        titulo = "LISTA DE CLIENTES"
        cabecera = (("_id", "Nro registro"),
                    ("nombres_cliente", "Nombres"),
                    ("apellidos_cliente", "Apellidos"),
                    ("ci_cliente", "Ci"),
                    ("email_cliente", "Email"),
                    ("telefono_cliente", "Telefono"),)
        nombrepdf = session['cedula'] + "clientes" + "reporte.pdf"
        return self.reportes_tablas(coleccion,titulo,cabecera,nombrepdf)


# ************************************************************* ADMINISTRAR CLIENTES FIN  ******************************************************

#**************************************************** ADMINIDTRAR SOLICITUD TRABAJO EXTERNO INICIO  ********************************

    def crear_solicitud_trabajo_externo(self,**kwargs):
        solicitu_trabajo = db['solicitud_trabajo_externo']

        if solicitu_trabajo.find_one({'_id': 1}) is None:
            kwargs['_id']=1
        else:
            kwargs['_id'] = self.buscar_id_max(solicitu_trabajo)

        existing_user = solicitu_trabajo.find_one({'solicitante': kwargs['solicitante']})  # consulta a la base de datos para ver si existe el usuario en la basa de datos
        if existing_user is None:  # si el usuario no existe en la bae de datos entra
                return solicitu_trabajo.insert(kwargs)
        else:
            return False

    def mostrar_solicitu_trabajo_esterno(self):
        solicitu_trab_completo=[]
        stexterno = db['solicitud_trabajo_externo']
        list_solicitud_trab = stexterno.find()
        for i in list_solicitud_trab:
            solicitud_tra = []
            v1 = i["_id"]
            v2 = i["solicitante"]
            v4 = i["laboratista"]
            v5 = i["descripcion_muestra"]
            v6 = i["ubicacion"]
            v7 = i["proyecto"]
            v8 = i["jefe_de_carrera"]
            v9 = i["tipo_muestra"]
            v10 = i["fecha_ensayo"]
            v11 = i["fecha_entrega"]
            v12 = i["fecha_muestreo"]
            v13 = i["codigo"]
            v14 = i["ensayos_solicitados"]
            solicitud_tra.append(v1)
            solicitud_tra.append(v2)
            solicitud_tra.append(v4)
            solicitud_tra.append(v5)
            solicitud_tra.append(v6)
            solicitud_tra.append(v7)
            solicitud_tra.append(v8)
            solicitud_tra.append(v9)
            solicitud_tra.append(v10)
            solicitud_tra.append(v11)
            solicitud_tra.append(v12)
            solicitud_tra.append(v13)
            solicitud_tra.append(v14)
            solicitu_trab_completo.append(tuple(solicitud_tra))
        return tuple(solicitu_trab_completo)


    def actualizar_solicitud_trabajo_externo(self,**kwargs):#*********************** pendiente la contasena ******************************************
        solicitud_trab = db['solicitud_trabajo_externo']

        #{'tipo_muestra': u'Distubada', '_id': u'1', 'laboratista': u'Administrador', 'descripcion_muestra': u'Arcilla Disperciva', 'fecha_ensayo': u'2019-02-28', 'fecha_entrega': u'2019-03-03', 'fecha_muestreo': u'2019-03-21', 'ubicacion': u'Veintitr\xe9s De Marzo', 'proyecto': u'Prueba Uno', 'solicitante': u'Diego Armando', 'codigo': u'2123424', 'estado': u'Bueno', 'jefe_de_carrera': u'Coronel Morron'}
        existing_user = solicitud_trab.find_one({'tipo_muestra': kwargs['tipo_muestra'], "laboratista":kwargs['laboratista'],"descripcion_muestra": kwargs['descripcion_muestra'], "fecha_ensayo": kwargs['fecha_ensayo'],"fecha_entrega": kwargs['fecha_entrega'], "fecha_muestreo": kwargs['fecha_muestreo'], "ubicacion": kwargs['ubicacion'], "proyecto": kwargs['proyecto'], "solicitante": kwargs['solicitante'], "codigo": kwargs['codigo'], "estado": kwargs['estado'], "jefe_de_carrera": kwargs['jefe_de_carrera']})  # consulta a la base de datos para ver si existe el usuario en la basa de datos
        if existing_user is None:
            solicitud_trab.update({"_id": {"$eq": int(kwargs['_id'])}}, {"$set": {'tipo_muestra': kwargs['tipo_muestra'], "laboratista":kwargs['laboratista'],"descripcion_muestra": kwargs['descripcion_muestra'], "fecha_ensayo": kwargs['fecha_ensayo'],"fecha_entrega": kwargs['fecha_entrega'], "fecha_muestreo": kwargs['fecha_muestreo'], "ubicacion": kwargs['ubicacion'], "proyecto": kwargs['proyecto'], "solicitante": kwargs['solicitante'], "codigo": kwargs['codigo'], "estado": kwargs['estado'], "jefe_de_carrera": kwargs['jefe_de_carrera']}},upsert=False, multi=False)
            response = {'respuesta': "Modificado"}
            return jsonify(response)
        else:
            return False

    def eliminar_solicitud_trabajo_externo(self,id):
        solicitud_trab = db['solicitud_trabajo_externo']
        solicitud_trab.remove({'_id': int(id)})
        return True


    def reporte_solicitud_trabajo_externo(self):

        coleccion = db['solicitud_trabajo_externo']  # conectar con las colecciones
        titulo = "LISTA DE SOLICITUDES DE TRABAJO"
        cabecera = (("_id", "Nro registro"),
                    ("solicitante", "Solicitante"),
                    ("laboratista", "Laboratista"),
                    ("descripcion_muestra", "Descripcion muestra"),
                    ("ubicacion", "Ubicacion"),
                    ("jefe_de_carrera", "Jefe de carrera"),
                    ("fecha_entrega", "Fecha entrega"),)
        nombrepdf = session['cedula'] + "solicitud_tabajo_externo" + "reporte.pdf"
        return self.reportes_tablas(coleccion,titulo,cabecera,nombrepdf)
#----------------------------------------------------ADMINISTRAR SOLICITU TRABAJO EXTERNO FIN ------------------------------------







    def guardar_solicitud_laboratorio(self,**kwargs):
        solicitud = db['solicitudes_de_laboratorio']
        diccionario=kwargs


        if solicitud.find_one({'_id': 1}) is None:

            diccionario['_id']=1

        else:
            id_max = self.buscar_id_max(solicitud)
            diccionario['_id'] = id_max

        solicitud.insert(diccionario)
        return True

    def retorna_datos_select_dinamico(self,dato):
        equipos = []
        equipos_laboratorio = db['equipos_laboratorio']
        equipo = equipos_laboratorio.find({"$and": [{"ensayo_utilizado": {"$eq": dato}}, {"tipo_equipo": {"$eq": 'Equipos'}}]})

        for a in equipo:
            equipos.append(a['nombre_activo'])
        return equipos

    def retorna_datos_select_materiales(self,dato):
        materiales = []
        materiales_laboratorio = db['materiales_laboratorio']
        material = materiales_laboratorio.find({"$and": [{"ensayo_utilizado": {"$eq": dato}}, {"tipo_equipo": {"$eq": 'Materiales'}}]})

        for a in material:
            materiales.append(a['nombre_activo'])
        return materiales


    def retorna_datos_select_reactivos(self,dato):
        reactivos = []
        reactivos_laboratorio = db['reactivos_laboratorio']
        reactivo = reactivos_laboratorio.find({"$and": [{"ensayo_utilizado": {"$eq": dato}}, {"tipo_equipo": {"$eq": 'Reactivos'}}]})
        for a in reactivo:
            reactivos.append(a['nombre_activo'])
        return reactivos


    def mostrar_solicitudes_laboratorio(self):
        solicitudes_completo=[]
        solicitudes = db['solicitudes_de_laboratorio']
        list_solicitudes = solicitudes.find()
        for i in list_solicitudes:
            solicitud = []
            v1 = i["_id"]
            v2 = i["nombre"]
            v3 = i["semestre"]
            v4 = i["ci"]
            v5 = i["correo_electronico"]
            v6 = i["fecha_solicitud"]
            v7 = i["fecha_uso_laboratorio"]
            v8 = i["hora_uso_laboratorio"]
            v9 = i["estado"]
            v10 = i["observaciones"]
            solicitud.append(v1)
            solicitud.append(v2)
            solicitud.append(v3)
            solicitud.append(v4)
            solicitud.append(v5)
            solicitud.append(v6)
            solicitud.append(v7)
            solicitud.append(v8)
            solicitud.append(v9)
            solicitud.append(v10)
            solicitudes_completo.append(tuple(solicitud))
        return tuple(solicitudes_completo)

    def enviar_correo_de_aceptacion(self,id_dato):
        solicitudes = db['solicitudes_de_laboratorio']
        if self.registrar_solicitudes_aceptadas_de_uso_laboratorios(id_dato,solicitudes):
            solicitudes.update({"_id": {"$eq": float(id_dato)}}, {"$set": {"estado": "aceptado"}}, upsert=False, multi=False)
            datos_solicitudes = solicitudes.find_one({'_id': float(id_dato)})
            msg = Message('Solicitud de Laboratorio', sender='civilemicbba@gmail.com', recipients=[datos_solicitudes['correo_electronico']])
            msg.body = 'Estudiante : '+''+datos_solicitudes['nombre']+''+' se confirmo la '+ 'hora ' + datos_solicitudes['hora_uso_laboratorio'] +' y la '+ ' Fecha ' + datos_solicitudes['fecha_uso_laboratorio'] + '' + " para el uso del laboratorio" + ''
            mail.send(msg)
            return True
        else:
            return False

    def registrar_solicitudes_aceptadas_de_uso_laboratorios(self,id,solicitudes):
        solicitudes_de_uso = db['solicitudes_aceptadas_de_uso_laboratorio']
        solicitud_aceptada = solicitudes.find_one({'_id': float(id)})
        if solicitudes_de_uso.find_one({'_id': 1}) is None:
            solicitud_aceptada['_id'] = 1
        else:
            id_max = self.buscar_id_max(solicitudes_de_uso)
            solicitud_aceptada['_id'] = id_max

        solicitudes_de_uso.insert(solicitud_aceptada)
        return True



    def enviar_correo_de_rechazo(self, id_dato):
        solicitudes = db['solicitudes_de_laboratorio']
        datos_solicitudes = solicitudes.find_one({'_id': float(id_dato)})
        msg = Message('Solicitud de Laboratorio', sender='civilemicbba@gmail.com',
                      recipients=[datos_solicitudes['correo_electronico']])
        msg.body = 'Estudiante : ' + '' + datos_solicitudes['nombre'] + '' + ' se rechazo la ' + 'hora ' + \
                   datos_solicitudes['hora_uso_laboratorio'] + ' y la ' + ' Fecha ' + datos_solicitudes[
                       'fecha_uso_laboratorio'] + '' + " para el uso del laboratorio ya que la fecha y la hora no estara disponible el laboratorio" + ''
        mail.send(msg)
        solicitudes.remove({'_id': float(id_dato)})
        return True

    def observaciones_solocitud_laboratorio(self,id,observaciones):
        observacionessolici = db['solicitudes_de_laboratorio']
        existing_observaciones = observacionessolici.find_one({'observaciones': observaciones})  # consulta a la base de datos para ver si existe el usuario en la basa de datos
        if existing_observaciones is None:
            observacionessolici.update({"_id": {"$eq": float(id)}}, {"$set": {"observaciones": observaciones}}, upsert=False, multi=False)
            response = {'respuesta': "Modificado"}
            return jsonify(response)
        else:
            return False

    def eliminar_solicitud_laboratorio(self,id):
        eliminar_solici = db['solicitudes_de_laboratorio']
        eliminar_solici.remove({'_id': float(id)})
        return True


    def reporte_solicitud_laboratorio(self):
        coleccion = db['solicitudes_aceptadas_de_uso_laboratorio']  # conectar con las colecciones
        titulo = "LISTA DE SOLICITUDES DE LABORATORIO"
        cabecera = (("_id", "Nro"),
                    ("fecha_uso_laboratorio", "Fecha solicitud"),
                    ("hora_uso_laboratorio", "Hora"),
                    ("solicitante", "Solicitante"),
                    ("nombre", "Nombre"),
                    ("asignatura", "Asignatura"),
                    ("practica_laboratorio", "Practica de laboratorio"),
                    ("semestre", "Semestre"),)
        nombrepdf = session['cedula'] + "solicitudlab" + "reporte.pdf"
        return self.reportes_tablas(coleccion,titulo,cabecera,nombrepdf)


    def reporte_formulario_solicitud_laboratorio(self,b):
        coleccion = db['solicitudes_de_laboratorio']  #conectar con las colecciones
        datos_solicitud = coleccion.find_one({"_id": int(b)})
        nombrepdf='uso_de_laboratorio' + session['cedula'] + ".pdf"
        return ['USO DE LABORATORIO', datos_solicitud, nombrepdf]





    def registrar_equipos(self,nombreactivo,codanterior,codactivo,estadoactivo,fechacompra,descripcionactivo,ensayo_utilizado):
        if ensayo_utilizado[0]:
            ensayo_utilizado[0]="Contenido De H.(Astm D2216)"
        if ensayo_utilizado[1]:
            ensayo_utilizado[1]="Granulometría (Astm D422)"
        if ensayo_utilizado[2]:
            ensayo_utilizado[2]="Granulometría (Aashto T-27)"
        if ensayo_utilizado[3]:
            ensayo_utilizado[3]="Limites De C. (Astm D4318)"
        if ensayo_utilizado[4]:
            ensayo_utilizado[4]="Limites De C. (Aashto T-89)"
        if ensayo_utilizado[5]:
            ensayo_utilizado[5]="Limite De Contracción (Astm D427)"
        if ensayo_utilizado[6]:
            ensayo_utilizado[6]="Proctor Modificado (Astm D1557)"
        if ensayo_utilizado[7]:
            ensayo_utilizado[7]="Proctor Modificado (Aashto T-180)"
        if ensayo_utilizado[8]:
            ensayo_utilizado[8]="Proctor Estándar (Aashto T-99)"
        if ensayo_utilizado[9]:
            ensayo_utilizado[9]="Cono De Arena (Astm D1556-64)"
        if ensayo_utilizado[10]:
            ensayo_utilizado[10]="Gravedad Especifica (Astm D854-02)"
        if ensayo_utilizado[11]:
            ensayo_utilizado[11]="Hidrometría (Astm D422-63)"
        if ensayo_utilizado[12]:
            ensayo_utilizado[12]="Doble Hidrometría (Astm D422-6)"
        if ensayo_utilizado[13]:
            ensayo_utilizado[13]="Permeabilidad De Carga C. (Astm D2434)"
        if ensayo_utilizado[14]:
            ensayo_utilizado[14]="Permeabilidad De Carga V. (Astm)"
        if ensayo_utilizado[15]:
            ensayo_utilizado[15]="Cbr (Astm D1883-99)"
        if ensayo_utilizado[16]:
            ensayo_utilizado[16]="Cbr (Aashto T-193)"
        if ensayo_utilizado[17]:
            ensayo_utilizado[17]="Consolidación Unidimensional (Astm D2435-96)"
        if ensayo_utilizado[18]:
            ensayo_utilizado[18]="Corte Directo (Astm D3080-98)"
        if ensayo_utilizado[19]:
            ensayo_utilizado[19]="Cono Dinámico De P. (Dcp)"



        equipos_laboratorio = db['equipos_laboratorio']
        if equipos_laboratorio.find_one({'_id': 1}) is None:
            id_max = 1

        else:
            id_max = self.buscar_id_max(equipos_laboratorio)
            
        existing_user = equipos_laboratorio.find_one({'codigo_activo' : codactivo}) # consulta a la base de datos para ver si existe el usuario en la basa de datos
        existing_user2 = equipos_laboratorio.find_one({'codigo_anterior' : codanterior}) # consulta a la base de datos para ver si existe el usuario en la basa de datos
        if existing_user is None and existing_user2 is None: # si el usuario no existe en la bae de datos entra
            self.guardar_equipos(nombreactivo,codanterior,codactivo,estadoactivo,fechacompra,descripcionactivo,ensayo_utilizado,id_max)
            return True
        else:
            return False

    def guardar_equipos(self,nombreactivo,codanterior,codactivo,estadoactivo,fechacompra,descripcionactivo,ensayo_utilizado,id_max):
        equipos_laboratorio = db['equipos_laboratorio']


        almacenar = {
            '_id': id_max,
            'nombre_activo':nombreactivo.title(),
            'codigo_anterior': codanterior,
            'codigo_activo': codactivo,
            'estado_activo': estadoactivo.title(),
            'fecha_compra': fechacompra,
            'tipo_equipo': "Equipos",
            'descripcion_activo': descripcionactivo.title(),
            'ensayo_utilizado' :ensayo_utilizado
        }
        equipos_laboratorio.insert(almacenar)

        response = {
            'respuesta': "Guardado"
        }

        return jsonify(response)

    def mostrar_equipos_laboratorio(self):
        lista_equipos=[]
        equipos = db['equipos_laboratorio']
        list_equipos = equipos.find()
        for i in list_equipos:
            equipos_lab = []
            v1 = i["_id"]
            v2 = i["nombre_activo"]
            v3 = i["codigo_anterior"]
            v4 = i["codigo_activo"]
            v5 = i["descripcion_activo"]
            v6 = i["estado_activo"]
            v7 = i["fecha_compra"]
            v8 = i["ensayo_utilizado"]
            equipos_lab.append(v1)
            equipos_lab.append(v2)
            equipos_lab.append(v3)
            equipos_lab.append(v4)
            equipos_lab.append(v5)
            equipos_lab.append(v6)
            equipos_lab.append(v7)
            equipos_lab.append(v8)
            lista_equipos.append(tuple(equipos_lab))
        return tuple(lista_equipos)


    def actualizar_equipos(self,id,nombreactivo,codanterior,codactivo,estadoactivo,fechacompra,descripcionactivo,ensayo_utilizado):
        equipos_laboratorio = db['equipos_laboratorio']

        if ensayo_utilizado[0]:
            ensayo_utilizado[0]="Contenido De H.(Astm D2216)"
        if ensayo_utilizado[1]:
            ensayo_utilizado[1]="Granulometría (Astm D422)"
        if ensayo_utilizado[2]:
            ensayo_utilizado[2]="Granulometría (Aashto T-27)"
        if ensayo_utilizado[3]:
            ensayo_utilizado[3]="Limites De C. (Astm D4318)"
        if ensayo_utilizado[4]:
            ensayo_utilizado[4]="Limites De C. (Aashto T-89)"
        if ensayo_utilizado[5]:
            ensayo_utilizado[5]="Limite De Contracción (Astm D427)"
        if ensayo_utilizado[6]:
            ensayo_utilizado[6]="Proctor Modificado (Astm D1557)"
        if ensayo_utilizado[7]:
            ensayo_utilizado[7]="Proctor Modificado (Aashto T-180)"
        if ensayo_utilizado[8]:
            ensayo_utilizado[8]="Proctor Estándar (Aashto T-99)"
        if ensayo_utilizado[9]:
            ensayo_utilizado[9]="Cono De Arena (Astm D1556-64)"
        if ensayo_utilizado[10]:
            ensayo_utilizado[10]="Gravedad Especifica (Astm D854-02)"
        if ensayo_utilizado[11]:
            ensayo_utilizado[11]="Hidrometría (Astm D422-63)"
        if ensayo_utilizado[12]:
            ensayo_utilizado[12]="Doble Hidrometría (Astm D422-6)"
        if ensayo_utilizado[13]:
            ensayo_utilizado[13]="Permeabilidad De Carga C. (Astm D2434)"
        if ensayo_utilizado[14]:
            ensayo_utilizado[14]="Permeabilidad De Carga V. (Astm)"
        if ensayo_utilizado[15]:
            ensayo_utilizado[15]="Cbr (Astm D1883-99)"
        if ensayo_utilizado[16]:
            ensayo_utilizado[16]="Cbr (Aashto T-193)"
        if ensayo_utilizado[17]:
            ensayo_utilizado[17]="Consolidación Unidimensional (Astm D2435-96)"
        if ensayo_utilizado[18]:
            ensayo_utilizado[18]="Corte Directo (Astm D3080-98)"
        if ensayo_utilizado[19]:
            ensayo_utilizado[19]="Cono Dinámico De P. (Dcp)"



        existing_user = equipos_laboratorio.find_one({'nombre_activo': nombreactivo, "codigo_anterior": codanterior, "codigo_activo": codactivo, "estado_activo": estadoactivo, "fecha_compra": fechacompra, "descripcion_activo": descripcionactivo,"ensayo_utilizado":ensayo_utilizado})  # consulta a la base de datos para ver si existe el usuario en la basa de datos
        if existing_user is None:  # si el usuario no existe en la bae de datos entra
            equipos_laboratorio.update({"_id": {"$eq": float(id)}}, {"$set": {'nombre_activo': nombreactivo, "codigo_anterior": codanterior, "codigo_activo": codactivo, "estado_activo": estadoactivo, "fecha_compra": fechacompra, "descripcion_activo": descripcionactivo,"ensayo_utilizado":ensayo_utilizado}},
                            upsert=False, multi=False)
            response = {
                'respuesta': "Modificado"
            }
            # return True
            return jsonify(response)
        else:
            return False

    def eliminar_gloval(self,id):
        eliminar = db['equipos_laboratorio']
        eliminar.remove({'_id': float(id)})
        return True

    def mostrar_lista_equipos(self):#revisar
        lista_equipos=[]
        equipos = db['equipos_laboratorio']
        list_equipos = equipos.find()
        for i in list_equipos:
            v1 = i["nombre_activo"]
            lista_equipos.append(v1)
        return  lista_equipos

    def reporte_equipos(self):
        coleccion = db['equipos_laboratorio']  # conectar con las colecciones
        titulo = "LISTA DE EQUIPOS DE LABORATORIO"
        cabecera = (("_id", "Nro items"),
                    ("nombre_activo", "Nombre"),
                    ("codigo_anterior", "Codigo Anterior"),
                    ("codigo_activo", "Codigo Activo"),
                    ("descripcion_activo", "Descripcion del activo"),
                    ("estado_activo", "Estado Activo"),
                    ("fecha_compra", "Fecha de Compra"),)
        nombrepdf = session['cedula'] + "equipos" + "reporte.pdf"
        return self.reportes_tablas(coleccion,titulo,cabecera,nombrepdf)




    def reporte_formulario_solicitud_equipos(self,b):
        coleccion = db['solicitudes_de_equipos']  # conectar con las colecciones
        datos_solicitud = coleccion.find_one({"_id": int(b)})
        nombrepdf = 'uso_de_laboratorio' + session['cedula'] + ".pdf"
        return ['PRESTAMO DE EQUIPOS', datos_solicitud, nombrepdf]

 




#******************************************sggggggggggggggggggggggggggtgadrhehtm***************************************************
    def registrar_materiales(self,nombreactivo,fecharegistro,descripcionactivo,ensayo_utilizado):
        if ensayo_utilizado[0]:
            ensayo_utilizado[0] = "Contenido De H.(Astm D2216)"
        if ensayo_utilizado[1]:
            ensayo_utilizado[1] = "Granulometría (Astm D422)"
        if ensayo_utilizado[2]:
            ensayo_utilizado[2] = "Granulometría (Aashto T-27)"
        if ensayo_utilizado[3]:
            ensayo_utilizado[3] = "Limites De C. (Astm D4318)"
        if ensayo_utilizado[4]:
            ensayo_utilizado[4] = "Limites De C. (Aashto T-89)"
        if ensayo_utilizado[5]:
            ensayo_utilizado[5] = "Limite De Contracción (Astm D427)"
        if ensayo_utilizado[6]:
            ensayo_utilizado[6] = "Proctor Modificado (Astm D1557)"
        if ensayo_utilizado[7]:
            ensayo_utilizado[7] = "Proctor Modificado (Aashto T-180)"
        if ensayo_utilizado[8]:
            ensayo_utilizado[8] = "Proctor Estándar (Aashto T-99)"
        if ensayo_utilizado[9]:
            ensayo_utilizado[9] = "Cono De Arena (Astm D1556-64)"
        if ensayo_utilizado[10]:
            ensayo_utilizado[10] = "Gravedad Especifica (Astm D854-02)"
        if ensayo_utilizado[11]:
            ensayo_utilizado[11] = "Hidrometría (Astm D422-63)"
        if ensayo_utilizado[12]:
            ensayo_utilizado[12] = "Doble Hidrometría (Astm D422-6)"
        if ensayo_utilizado[13]:
            ensayo_utilizado[13] = "Permeabilidad De Carga C. (Astm D2434)"
        if ensayo_utilizado[14]:
            ensayo_utilizado[14] = "Permeabilidad De Carga V. (Astm)"
        if ensayo_utilizado[15]:
            ensayo_utilizado[15] = "Cbr (Astm D1883-99)"
        if ensayo_utilizado[16]:
            ensayo_utilizado[16] = "Cbr (Aashto T-193)"
        if ensayo_utilizado[17]:
            ensayo_utilizado[17] = "Consolidación Unidimensional (Astm D2435-96)"
        if ensayo_utilizado[18]:
            ensayo_utilizado[18] = "Corte Directo (Astm D3080-98)"
        if ensayo_utilizado[19]:
            ensayo_utilizado[19] = "Cono Dinámico De P. (Dcp)"

        materiales_laboratorio = db['materiales_laboratorio']
        if materiales_laboratorio.find_one({'_id': 1}) is None:
            id_max = 1

        else:
            id_max = self.buscar_id_max(materiales_laboratorio)

        existing_user = materiales_laboratorio.find_one({'nombre_activo': nombreactivo})  # consulta a la base de datos para ver si existe el usuario en la basa de datos

        if existing_user is None:  # si el usuario no existe en la bae de datos entra
            self.guardar_materiales(nombreactivo,fecharegistro,descripcionactivo,ensayo_utilizado,id_max,materiales_laboratorio)
            return True
        else:
            return False

    def guardar_materiales(self,nombreactivo,fecharegistro,descripcionactivo,ensayo_utilizado,id_max,materiales_laboratorio):
        # equipos_laboratorio = db['equipos_laboratorio']

        almacenar = {
            '_id': id_max,
            'nombre_activo': nombreactivo.title(),
            'tipo_equipo': "Materiales",
            'descripcion_activo': descripcionactivo.title(),
            'ensayo_utilizado': ensayo_utilizado,
            'fecha_registro': fecharegistro
        }
        materiales_laboratorio.insert(almacenar)

        response = {
            'respuesta': "Guardado"
        }

        return jsonify(response)




    def mostrar_materiales_laboratorio(self):
        lista_equipos=[]
        materiales = db['materiales_laboratorio']
        list_materiales = materiales.find()
        for i in list_materiales:
            equipos_lab = []
            v1 = i["_id"]
            v2 = i["nombre_activo"]
            v3 = i["fecha_registro"]
            v4 = i["ensayo_utilizado"]
            v5 = i["descripcion_activo"]
            equipos_lab.append(v1)
            equipos_lab.append(v2)
            equipos_lab.append(v3)
            equipos_lab.append(v4)
            equipos_lab.append(v5)
            lista_equipos.append(tuple(equipos_lab))
        return tuple(lista_equipos)



    def actualizar_materiales(self,id,nombreactivo,descripcionactivo,ensayo_utilizado):
        materiales_laboratorio = db['materiales_laboratorio']

        if ensayo_utilizado[0]:
            ensayo_utilizado[0]="Contenido De H.(Astm D2216)"
        if ensayo_utilizado[1]:
            ensayo_utilizado[1]="Granulometría (Astm D422)"
        if ensayo_utilizado[2]:
            ensayo_utilizado[2]="Granulometría (Aashto T-27)"
        if ensayo_utilizado[3]:
            ensayo_utilizado[3]="Limites De C. (Astm D4318)"
        if ensayo_utilizado[4]:
            ensayo_utilizado[4]="Limites De C. (Aashto T-89)"
        if ensayo_utilizado[5]:
            ensayo_utilizado[5]="Limite De Contracción (Astm D427)"
        if ensayo_utilizado[6]:
            ensayo_utilizado[6]="Proctor Modificado (Astm D1557)"
        if ensayo_utilizado[7]:
            ensayo_utilizado[7]="Proctor Modificado (Aashto T-180)"
        if ensayo_utilizado[8]:
            ensayo_utilizado[8]="Proctor Estándar (Aashto T-99)"
        if ensayo_utilizado[9]:
            ensayo_utilizado[9]="Cono De Arena (Astm D1556-64)"
        if ensayo_utilizado[10]:
            ensayo_utilizado[10]="Gravedad Especifica (Astm D854-02)"
        if ensayo_utilizado[11]:
            ensayo_utilizado[11]="Hidrometría (Astm D422-63)"
        if ensayo_utilizado[12]:
            ensayo_utilizado[12]="Doble Hidrometría (Astm D422-6)"
        if ensayo_utilizado[13]:
            ensayo_utilizado[13]="Permeabilidad De Carga C. (Astm D2434)"
        if ensayo_utilizado[14]:
            ensayo_utilizado[14]="Permeabilidad De Carga V. (Astm)"
        if ensayo_utilizado[15]:
            ensayo_utilizado[15]="Cbr (Astm D1883-99)"
        if ensayo_utilizado[16]:
            ensayo_utilizado[16]="Cbr (Aashto T-193)"
        if ensayo_utilizado[17]:
            ensayo_utilizado[17]="Consolidación Unidimensional (Astm D2435-96)"
        if ensayo_utilizado[18]:
            ensayo_utilizado[18]="Corte Directo (Astm D3080-98)"
        if ensayo_utilizado[19]:
            ensayo_utilizado[19]="Cono Dinámico De P. (Dcp)"



        existing_user = materiales_laboratorio.find_one({'nombre_activo': nombreactivo, "descripcion_activo": descripcionactivo,"ensayo_utilizado":ensayo_utilizado})  # consulta a la base de datos para ver si existe el usuario en la basa de datos
        if existing_user is None:  # si el usuario no existe en la bae de datos entra
            materiales_laboratorio.update({"_id": {"$eq": float(id)}}, {"$set": {'nombre_activo': nombreactivo, "descripcion_activo": descripcionactivo,"ensayo_utilizado":ensayo_utilizado}},
                            upsert=False, multi=False)
            response = {
                'respuesta': "Modificado"
            }
            # return True
            return jsonify(response)
        else:
            return False

    def eliminar_materiales(self, id):
        eliminar = db['materiales_laboratorio']
        eliminar.remove({'_id': float(id)})
        return True



    def reporte_materiales(self):
        coleccion = db['materiales_laboratorio']  # conectar con las colecciones
        titulo = "LISTA DE MATERIALES DE LABORATORIO"
        cabecera = (("_id", "Nro items"),
                    ("nombre_activo", "Nombre"),
                    ("descripcion_activo", "Descripcion del activo"),
                    ("fecha_registro", "Fecha de Registro"),)
        nombrepdf = session['cedula'] + "materiales" + "reporte.pdf"
        return self.reportes_tablas(coleccion,titulo,cabecera,nombrepdf)
#**************************sggsb***********srjhdjtyjtyyyhyjuhuyyyyyyyyyy**************************************************************************







#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    def registrar_reactivos(self,nombreactivo,fecha_vencimiento, fecharegistro,ensayo_utilizado):
        if ensayo_utilizado[0]:
            ensayo_utilizado[0] = "Contenido De H.(Astm D2216)"
        if ensayo_utilizado[1]:
            ensayo_utilizado[1] = "Granulometría (Astm D422)"
        if ensayo_utilizado[2]:
            ensayo_utilizado[2] = "Granulometría (Aashto T-27)"
        if ensayo_utilizado[3]:
            ensayo_utilizado[3] = "Limites De C. (Astm D4318)"
        if ensayo_utilizado[4]:
            ensayo_utilizado[4] = "Limites De C. (Aashto T-89)"
        if ensayo_utilizado[5]:
            ensayo_utilizado[5] = "Limite De Contracción (Astm D427)"
        if ensayo_utilizado[6]:
            ensayo_utilizado[6] = "Proctor Modificado (Astm D1557)"
        if ensayo_utilizado[7]:
            ensayo_utilizado[7] = "Proctor Modificado (Aashto T-180)"
        if ensayo_utilizado[8]:
            ensayo_utilizado[8] = "Proctor Estándar (Aashto T-99)"
        if ensayo_utilizado[9]:
            ensayo_utilizado[9] = "Cono De Arena (Astm D1556-64)"
        if ensayo_utilizado[10]:
            ensayo_utilizado[10] = "Gravedad Especifica (Astm D854-02)"
        if ensayo_utilizado[11]:
            ensayo_utilizado[11] = "Hidrometría (Astm D422-63)"
        if ensayo_utilizado[12]:
            ensayo_utilizado[12] = "Doble Hidrometría (Astm D422-6)"
        if ensayo_utilizado[13]:
            ensayo_utilizado[13] = "Permeabilidad De Carga C. (Astm D2434)"
        if ensayo_utilizado[14]:
            ensayo_utilizado[14] = "Permeabilidad De Carga V. (Astm)"
        if ensayo_utilizado[15]:
            ensayo_utilizado[15] = "Cbr (Astm D1883-99)"
        if ensayo_utilizado[16]:
            ensayo_utilizado[16] = "Cbr (Aashto T-193)"
        if ensayo_utilizado[17]:
            ensayo_utilizado[17] = "Consolidación Unidimensional (Astm D2435-96)"
        if ensayo_utilizado[18]:
            ensayo_utilizado[18] = "Corte Directo (Astm D3080-98)"
        if ensayo_utilizado[19]:
            ensayo_utilizado[19] = "Cono Dinámico De P. (Dcp)"

        reactivos_laboratorio = db['reactivos_laboratorio']
        if reactivos_laboratorio.find_one({'_id': 1}) is None:
            id_max = 1

        else:
            id_max = self.buscar_id_max(reactivos_laboratorio)

        existing_user = reactivos_laboratorio.find_one({'nombre_activo': nombreactivo})  # consulta a la base de datos para ver si existe el usuario en la basa de datos

        if existing_user is None:  # si el usuario no existe en la bae de datos entra
            self.guardar_reactivos(nombreactivo,fecha_vencimiento, fecharegistro,ensayo_utilizado,id_max,reactivos_laboratorio)
            return True
        else:
            return False

    def guardar_reactivos(self,nombreactivo,fecha_vencimiento, fecharegistro,ensayo_utilizado,id_max,reactivos_laboratorio):

        almacenar = {
            '_id': id_max,
            'nombre_activo': nombreactivo.title(),
            'tipo_equipo': "Reactivos",
            'fecha_vencimiento': fecha_vencimiento,
            'ensayo_utilizado': ensayo_utilizado,
            'fecha_registro': fecharegistro
        }
        reactivos_laboratorio.insert(almacenar)

        response = {
            'respuesta': "Guardado"
        }

        return jsonify(response)

    def mostrar_reactivos_laboratorio(self):
        lista_equipos=[]
        reactivos = db['reactivos_laboratorio']
        list_reactivos = reactivos.find()
        for i in list_reactivos:
            equipos_lab = []
            v1 = i["_id"]
            v2 = i["nombre_activo"]
            v3 = i["fecha_vencimiento"]
            v4 = i["ensayo_utilizado"]
            v5 = i["fecha_registro"]

            equipos_lab.append(v1)
            equipos_lab.append(v2)
            equipos_lab.append(v3)
            equipos_lab.append(v4)
            equipos_lab.append(v5)
            lista_equipos.append(tuple(equipos_lab))
        return tuple(lista_equipos)

    def actualizar_reactivos(self,id, nombreactivo, fechavencimiento, ensayo_utilizado):
        reactivos_laboratorio = db['reactivos_laboratorio']

        if ensayo_utilizado[0]:
            ensayo_utilizado[0]="Contenido De H.(Astm D2216)"
        if ensayo_utilizado[1]:
            ensayo_utilizado[1]="Granulometría (Astm D422)"
        if ensayo_utilizado[2]:
            ensayo_utilizado[2]="Granulometría (Aashto T-27)"
        if ensayo_utilizado[3]:
            ensayo_utilizado[3]="Limites De C. (Astm D4318)"
        if ensayo_utilizado[4]:
            ensayo_utilizado[4]="Limites De C. (Aashto T-89)"
        if ensayo_utilizado[5]:
            ensayo_utilizado[5]="Limite De Contracción (Astm D427)"
        if ensayo_utilizado[6]:
            ensayo_utilizado[6]="Proctor Modificado (Astm D1557)"
        if ensayo_utilizado[7]:
            ensayo_utilizado[7]="Proctor Modificado (Aashto T-180)"
        if ensayo_utilizado[8]:
            ensayo_utilizado[8]="Proctor Estándar (Aashto T-99)"
        if ensayo_utilizado[9]:
            ensayo_utilizado[9]="Cono De Arena (Astm D1556-64)"
        if ensayo_utilizado[10]:
            ensayo_utilizado[10]="Gravedad Especifica (Astm D854-02)"
        if ensayo_utilizado[11]:
            ensayo_utilizado[11]="Hidrometría (Astm D422-63)"
        if ensayo_utilizado[12]:
            ensayo_utilizado[12]="Doble Hidrometría (Astm D422-6)"
        if ensayo_utilizado[13]:
            ensayo_utilizado[13]="Permeabilidad De Carga C. (Astm D2434)"
        if ensayo_utilizado[14]:
            ensayo_utilizado[14]="Permeabilidad De Carga V. (Astm)"
        if ensayo_utilizado[15]:
            ensayo_utilizado[15]="Cbr (Astm D1883-99)"
        if ensayo_utilizado[16]:
            ensayo_utilizado[16]="Cbr (Aashto T-193)"
        if ensayo_utilizado[17]:
            ensayo_utilizado[17]="Consolidación Unidimensional (Astm D2435-96)"
        if ensayo_utilizado[18]:
            ensayo_utilizado[18]="Corte Directo (Astm D3080-98)"
        if ensayo_utilizado[19]:
            ensayo_utilizado[19]="Cono Dinámico De P. (Dcp)"



        existing_user = reactivos_laboratorio.find_one({'nombre_activo': nombreactivo, "fecha_vencimiento": fechavencimiento,"ensayo_utilizado":ensayo_utilizado})  # consulta a la base de datos para ver si existe el usuario en la basa de datos
        if existing_user is None:  # si el usuario no existe en la bae de datos entra
            reactivos_laboratorio.update({"_id": {"$eq": float(id)}}, {"$set": {'nombre_activo': nombreactivo, "fecha_vencimiento": fechavencimiento,"ensayo_utilizado":ensayo_utilizado}},
                            upsert=False, multi=False)
            response = {
                'respuesta': "Modificado"
            }
            # return True
            return jsonify(response)
        else:
            return False

    def eliminar_reactivos(self, id):
        eliminar = db['reactivos_laboratorio']
        eliminar.remove({'_id': float(id)})
        return True

    def reporte_reactivos(self):
        coleccion = db['reactivos_laboratorio']  # conectar con las colecciones
        titulo = "LISTA DE REACTIVOS DE LABORATORIO"
        cabecera = (("_id", "Nro items"),
                    ("nombre_activo", "Nombre"),
                    ("fecha_vencimiento", "Fecha de Vencimiento"),
                    ("fecha_registro", "Fecha de Registro"),)
        nombrepdf = session['cedula'] + "reactivos" + "reporte.pdf"
        return self.reportes_tablas(coleccion,titulo,cabecera,nombrepdf)
#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////












    def guardar_solicitud_de_equipos(self,**kwargs):
        solicitud = db['solicitudes_de_equipos']
        if solicitud.find_one({'_id': 1}) is None:

            kwargs['_id'] = 1

        else:
            id_max = self.buscar_id_max(solicitud)
            kwargs['_id'] = id_max

        solicitud.insert(kwargs)
        return True

    def mostrar_solicitudes_equipo(self):
        solicitudes_completo = []
        solicitudes = db['solicitudes_de_equipos']
        list_solicitudes = solicitudes.find()
        for i in list_solicitudes:
            solicitud = []
            v1 = i["_id"]
            v2 = i["nombre"]
            v3 = i["asignatura"]
            v4 = i["ci"]
            v5 = i["correo_electronico"]
            v6 = i["fecha_solicitud"]
            v7 = i["fecha_uso_de_equipo"]
            v8 = i["hora_uso_de_equipo"]
            v9 = i["estado"]
            v10 = i["observaciones"]
            solicitud.append(v1)
            solicitud.append(v2)
            solicitud.append(v3)
            solicitud.append(v4)
            solicitud.append(v5)
            solicitud.append(v6)
            solicitud.append(v7)
            solicitud.append(v8)
            solicitud.append(v9)
            solicitud.append(v10)
            solicitudes_completo.append(tuple(solicitud))
        return tuple(solicitudes_completo)




    def enviar_correo_de_aceptacion_solicitud_equipo(self,id_dato):
        solicitudes = db['solicitudes_de_equipos']
        if self.registrar_solicitudes_aceptadas_de_uso_equipos(id_dato,solicitudes):
            solicitudes.update({"_id": {"$eq": float(id_dato)}}, {"$set": {"estado": "aceptado"}}, upsert=False, multi=False)
            datos_solicitudes = solicitudes.find_one({'_id': float(id_dato)})
            msg = Message('Solicitud de Equipos', sender='civilemicbba@gmail.com', recipients=[datos_solicitudes['correo_electronico']])
            msg.body = 'Querido usuari@ : '+''+datos_solicitudes['nombre']+''+' se confirmo la '+ 'hora ' + datos_solicitudes['hora_uso_de_equipo'] +' y la '+ ' Fecha ' + datos_solicitudes['fecha_uso_de_equipo'] + '' + " para el uso de los equipos" + ''
            mail.send(msg)
            return True
        else:
            return False

    def registrar_solicitudes_aceptadas_de_uso_equipos(self,id,solicitudes):
        solicitudes_de_uso = db['solicitudes_aceptadas_de_uso_equipos']
        solicitud_aceptada = solicitudes.find_one({'_id': float(id)})
        if solicitudes_de_uso.find_one({'_id': 1}) is None:
            solicitud_aceptada['_id'] = 1
        else:
            id_max = self.buscar_id_max(solicitudes_de_uso)
            solicitud_aceptada['_id'] = id_max

        solicitudes_de_uso.insert(solicitud_aceptada)
        return True

    def enviar_correo_de_rechazo_solicitud_equipo(self, id_dato):
        solicitudes = db['solicitudes_de_equipos']
        datos_solicitudes = solicitudes.find_one({'_id': float(id_dato)})
        msg = Message('Solicitud de Equipos', sender='civilemicbba@gmail.com',
                      recipients=[datos_solicitudes['correo_electronico']])
        msg.body = 'Querido usuari@ : ' + '' + datos_solicitudes['nombre'] + '' + ' se rechazo la ' + 'hora ' + \
                   datos_solicitudes['hora_uso_de_equipo'] + ' y la ' + ' Fecha ' + datos_solicitudes[
                       'fecha_uso_de_equipo'] + '' + " para el uso de los equipos ya que la fecha y la hora no estara disponible los equipos" + ''
        mail.send(msg)
        solicitudes.remove({'_id': float(id_dato)})
        return True

    def observaciones_solocitud_equipos(self,id,observaciones):
        observacionessolici = db['solicitudes_de_equipos']
        existing_observaciones = observacionessolici.find_one({'observaciones': observaciones})  # consulta a la base de datos para ver si existe el usuario en la basa de datos
        if existing_observaciones is None:
            observacionessolici.update({"_id": {"$eq": float(id)}}, {"$set": {"observaciones": observaciones}}, upsert=False, multi=False)
            response = {'respuesta': "Modificado"}
            return jsonify(response)
        else:
            return False

    def eliminar_solicitud_equipos(self,id):
        eliminar_solici = db['solicitudes_de_equipos']
        eliminar_solici.remove({'_id': float(id)})
        return True

    def reporte_solicitud_equipos(self):
        coleccion = db['solicitudes_aceptadas_de_uso_equipos']  # conectar con las colecciones
        titulo = "LISTA DE SOLICITUDES DE EQUIPOS"
        cabecera = (("_id", "Codigo"),
                    ("nombre", "Nombre"),
                    ("carrera", "Carrera"),
                    ("asignatura", "Asignatura"),
                    ("ci", "Ci"),
                    ("correo_electronico", "Correo"),
                    ("fecha_uso_de_equipo", "Fecha solicitud"),
                    ("hora_uso_de_equipo", "Hora"),)
        nombrepdf = session['cedula'] + "solicitud_equipo" + "reporte.pdf"
        return self.reportes_tablas(coleccion, titulo, cabecera,nombrepdf)


#***************************************************************************************************************************************
    def reportes_tablas(self,coleccion,titulo, cabecera,nombrePDF):
        datos = coleccion.find()  # dato impoetante
        reporte = reportePDF(titulo, cabecera, datos, nombrePDF).Exportar()
        os.system(nombrePDF)
        return nombrePDF


    def lista_roles(self):
        rol=[]
        roles = db['rol_user']
        list_roles = roles.find()
        for i in list_roles:
            R1 = i["rol"]
            rol.append(R1)
        return rol


    def buscar_id_max(self,nombre_coleccion):
        ids = []
        cursor3 = nombre_coleccion.find()
        for i in cursor3:
            ids.append(i["_id"])
        return (max(ids) + 1)

    def usuario_maximo(self,nombre_coleccion):
        ids = []
        cursor3 = nombre_coleccion.find({'ci':{'$in':[session['cedula']]}})
        for i in cursor3:
            ids.append(i["_id"])
        return (max(ids))


    #******************************** ENSAYOS ************************************************************************


    #--------------------------------- CONTENIDO DE HUMEDAD ----------------------------------------------------------

    def calculo_contenido_humedad(self,**kwargs):
        muestra1=[kwargs['datos_muestra_laboratorio'][3],kwargs['datos_muestra_laboratorio'][4],kwargs['datos_muestra_laboratorio'][5]]
        muestra2 = [kwargs['datos_muestra_laboratorio'][6], kwargs['datos_muestra_laboratorio'][7],kwargs['datos_muestra_laboratorio'][8]]
        muestra3 = [kwargs['datos_muestra_laboratorio'][9], kwargs['datos_muestra_laboratorio'][10],kwargs['datos_muestra_laboratorio'][11]]
        contenido_humedad = db['ensayo_contenido_de_humedad']
        sueloss = db['ensayos_de_suelos']

        datos=[muestra1,muestra2,muestra3]
        if sueloss.find_one({'_id': 1}) is None:kwargs['_id'] = 1
        else:
            id_max = self.buscar_id_max(sueloss)
            kwargs['_id'] = id_max

        calculo_contenido_H=ensayo().calculo_contenido_humedad(datos,"humedad")
        if calculo_contenido_H[0]==1:
            return calculo_contenido_H
        else:
            kwargs['resultados_del_ensayo']=calculo_contenido_H
            suelos_genral={'datos_generales':kwargs['datos_generales'],'ensayo':kwargs['ensayo'],'_id':kwargs['_id']}
            contenido_humedad.insert(kwargs)
            sueloss.insert(suelos_genral)
        return [None]


    def modificar_calculo_contenido_humedad(self,**kwargs):
        contenido_humedad = db['ensayo_contenido_de_humedad']
        sueloss = db['ensayos_de_suelos']
        existing_user = contenido_humedad.find_one(kwargs)  # consulta a la base de datos para ver si existe el usuario en la basa de datos
        if existing_user is None:
            muestra1 = [kwargs['datos_muestra_laboratorio'][3], kwargs['datos_muestra_laboratorio'][4],
                        kwargs['datos_muestra_laboratorio'][5]]
            muestra2 = [kwargs['datos_muestra_laboratorio'][6], kwargs['datos_muestra_laboratorio'][7],
                        kwargs['datos_muestra_laboratorio'][8]]
            muestra3 = [kwargs['datos_muestra_laboratorio'][9], kwargs['datos_muestra_laboratorio'][10],
                        kwargs['datos_muestra_laboratorio'][11]]

            datos=[muestra1, muestra2, muestra3]

            calculo_contenido_H = ensayo().calculo_contenido_humedad(datos,"humedad")
            if calculo_contenido_H[0] == 1:
                return calculo_contenido_H
            else:
                contenido_humedad.update({"_id": {"$eq": int(kwargs['_id'])}}, {"$set":{"datos_generales":kwargs['datos_generales'],"datos_muestra_laboratorio":kwargs['datos_muestra_laboratorio'],"resultados_del_ensayo":calculo_contenido_H}}, upsert=False, multi=False)
                sueloss.update({"_id": {"$eq": int(kwargs['_id'])}}, {"$set":{"datos_generales":kwargs['datos_generales']}}, upsert=False, multi=False)


        return [None]



    def mostrar_datos_contenido_humedad(self):
        ensayo_contenido_humedad = db['ensayo_contenido_de_humedad']
        id_max=self.usuario_maximo(ensayo_contenido_humedad)
        listasss = ensayo_contenido_humedad.find_one({'_id': id_max})
        return listasss

    def reporte_contenido_de_humedad(self,b):
        coleccion = db['ensayo_contenido_de_humedad']  #conectar con las colecciones
        datos_solicitud = coleccion.find_one({'_id': int(b)})
        nombrepdf=session['cedula']+"contenido_humedad"+".pdf"
        return [datos_solicitud['ensayo'],datos_solicitud,nombrepdf]

# *********************************************************************************************************************



#********************************************* GRANULOMETRIA **********************************************************
    def calculo_granulometrico(self,**kwargs):
        granulometria = db['ensayo_granulometria_astm']
        sueloss = db['ensayos_de_suelos']

        if sueloss.find_one({'_id': 1}) is None:kwargs['_id'] = 1
        else:
            id_max = self.buscar_id_max(sueloss)
            kwargs['_id'] = id_max

        masa_retenida=[kwargs['datos_muestra_laboratorio'][4],kwargs['datos_muestra_laboratorio'][5],kwargs['datos_muestra_laboratorio'][6],kwargs['datos_muestra_laboratorio'][7],kwargs['datos_muestra_laboratorio'][8],kwargs['datos_muestra_laboratorio'][9],kwargs['datos_muestra_laboratorio'][10],kwargs['datos_muestra_laboratorio'][11],kwargs['datos_muestra_laboratorio'][12],kwargs['datos_muestra_laboratorio'][13],kwargs['datos_muestra_laboratorio'][14],kwargs['datos_muestra_laboratorio'][15],kwargs['datos_muestra_laboratorio'][16],kwargs['datos_muestra_laboratorio'][17]]

        g=ensayo().granulometria(kwargs['datos_muestra_laboratorio'][0],kwargs['datos_muestra_laboratorio'][2],kwargs['datos_muestra_laboratorio'][1],kwargs['datos_muestra_laboratorio'][3],masa_retenida,kwargs['_id'],kwargs['usuario'],kwargs['ci'])
        if g[0] ==1:
            return g
        else:
            graficos = []
            graficos.append(g.pop())
            if kwargs['datos_muestra_laboratorio'][18]=='seleccionar':
                graficos.append('ninguno1')
                g.append(['ninguno', 'ninguno'])
            else:
                C=ensayo().clasificacion_suelos_astm(g[5][12],g[6][12], g[5][7],g[8][0],g[8][1],kwargs['datos_muestra_laboratorio'][19],kwargs['datos_muestra_laboratorio'][18],kwargs['_id'],kwargs['usuario'],kwargs['ci'])
                if C==None:
                    graficos.append('ninguno1')
                    g.append(['ninguno', 'ninguno'])
                else:
                    graficos.append(C.pop(0))
                    g.append(C)

            suelos_genral={'datos_generales':kwargs['datos_generales'],'ensayo':kwargs['ensayo'],'_id':kwargs['_id']}
            kwargs['direccion_de_grafico']=graficos
            kwargs['resultados_del_ensayo'] = g
            granulometria.insert(kwargs)
            sueloss.insert(suelos_genral)
        return [None]



    def modificar_calculo_granulometrico(self,**kwargs):
        granulometria = db['ensayo_granulometria_astm']
        sueloss = db['ensayos_de_suelos']

        masa_retenida=[kwargs['datos_muestra_laboratorio'][4],kwargs['datos_muestra_laboratorio'][5],kwargs['datos_muestra_laboratorio'][6],kwargs['datos_muestra_laboratorio'][7],kwargs['datos_muestra_laboratorio'][8],kwargs['datos_muestra_laboratorio'][9],kwargs['datos_muestra_laboratorio'][10],kwargs['datos_muestra_laboratorio'][11],kwargs['datos_muestra_laboratorio'][12],kwargs['datos_muestra_laboratorio'][13],kwargs['datos_muestra_laboratorio'][14],kwargs['datos_muestra_laboratorio'][15],kwargs['datos_muestra_laboratorio'][16],kwargs['datos_muestra_laboratorio'][17]]

        g=ensayo().granulometria(kwargs['datos_muestra_laboratorio'][0],kwargs['datos_muestra_laboratorio'][2],kwargs['datos_muestra_laboratorio'][1],kwargs['datos_muestra_laboratorio'][3],masa_retenida,kwargs['_id'],kwargs['usuario'],kwargs['ci'])
        if g[0] ==1:
            return g
        else:
            graficos = []
            graficos.append(g.pop())
            if kwargs['datos_muestra_laboratorio'][18] == 'seleccionar':
                graficos.append('ninguno1')
                g.append(['ninguno', 'ninguno'])
            else:
                C=ensayo().clasificacion_suelos_astm(g[5][12],g[6][12], g[5][7],g[8][0],g[8][1],kwargs['datos_muestra_laboratorio'][19],kwargs['datos_muestra_laboratorio'][18],kwargs['_id'],kwargs['usuario'],kwargs['ci'])
                if C == None:
                    graficos.append('ninguno1')
                    g.append(['ninguno', 'ninguno'])
                else:
                    graficos.append(C.pop(0))
                    g.append(C)


            direccion_grafico = kwargs['direccion_de_grafico'] = graficos
            granulometria.update({"_id": {"$eq": int(kwargs['_id'])}}, {
                "$set": {"datos_generales": kwargs['datos_generales'],
                         "datos_muestra_laboratorio": kwargs['datos_muestra_laboratorio'], "resultados_del_ensayo": g,
                         "direccion_de_grafico": direccion_grafico}}, upsert=False, multi=False)
            sueloss.update({"_id": {"$eq": int(kwargs['_id'])}}, {"$set":{"datos_generales":kwargs['datos_generales']}}, upsert=False, multi=False)


        return [None]



    def mostrar_datos_granulometria(self):
        granulometria = db['ensayo_granulometria_astm']
        id_max = self.usuario_maximo(granulometria)
        listasss = granulometria.find_one({'_id': id_max})
        return listasss





    def reporte_granulometria_astm(self,b):
        coleccion = db['ensayo_granulometria_astm']  #conectar con las colecciones
        datos_solicitud = coleccion.find_one({'_id': int(b)})
        nombrepdf="granulometria_astm"+ session['cedula']+".pdf"
        return [datos_solicitud['ensayo'], datos_solicitud, nombrepdf]


#-----------------------------------------------------------------------------------------------------------------------


#*************************************** LIMITES DE CONSISTENCIA *******************************************************
    def calculo_limites_de_consistencia_astm(self,**kwargs):
        limites = db['ensayo_limites_de_consistencia_astm']
        sueloss = db['ensayos_de_suelos']
        if sueloss.find_one({'_id': 1}) is None:kwargs['_id'] = 1
        else:
            id_max = self.buscar_id_max(sueloss)
            kwargs['_id'] = id_max
        L=ensayo().Calculo_limite_liquido(kwargs['datos_muestra_laboratorio'][1],kwargs['datos_muestra_laboratorio'][2],kwargs['_id'],kwargs['usuario'],kwargs['ci'],'ll_astm')
        if L[0]==1:
            return L
        else:
            suelos_genral={'datos_generales':kwargs['datos_generales'],'ensayo':kwargs['ensayo'],'_id':kwargs['_id']}
            kwargs['direccion_de_grafico'] = L[0][4].pop()
            kwargs['resultados_del_ensayo'] = L
            limites.insert(kwargs)
            sueloss.insert(suelos_genral)
        return [None]


    def modificar_calculo_limites_astm(self,**kwargs):
        limites = db['ensayo_limites_de_consistencia_astm']
        sueloss = db['ensayos_de_suelos']
        L = ensayo().Calculo_limite_liquido(kwargs['datos_muestra_laboratorio'][1],kwargs['datos_muestra_laboratorio'][2], kwargs['_id'], kwargs['usuario'],kwargs['ci'],'ll_astm')
        if L[0] == 1:
            return L
        else:
            kwargs['direccion_de_grafico'] = L[0][4].pop()
            direccion_grafico=kwargs['direccion_de_grafico']
            limites.update({"_id": {"$eq": int(kwargs['_id'])}}, {"$set": {"datos_generales": kwargs['datos_generales'],"datos_muestra_laboratorio": kwargs['datos_muestra_laboratorio'], "resultados_del_ensayo": L,"direccion_de_grafico": direccion_grafico}}, upsert=False, multi=False)
            sueloss.update({"_id": {"$eq": int(kwargs['_id'])}}, {"$set":{"datos_generales":kwargs['datos_generales']}}, upsert=False, multi=False)
        return [None]


    def mostrar_datos_limites_astm(self):
        limites = db['ensayo_limites_de_consistencia_astm']
        id_max = self.usuario_maximo(limites)
        listasss = limites.find_one({'_id': id_max})
        return listasss

    def lista_limite_liquido(self):
        LL = []
        roles = db['ensayo_limites_de_consistencia_astm']
        list_LL = roles.find()
        for i in list_LL:
            lista = []
            R1 = i["resultados_del_ensayo"][0][4][0][0]
            R2 =i["resultados_del_ensayo"][2]
            lista.append(R1)
            lista.append(R2)
            LL.append(lista)
        return LL


    def reporte_limite_de_consistencia_astm(self,b):
        coleccion = db['ensayo_limites_de_consistencia_astm']  #conectar con las colecciones
        datos_solicitud = coleccion.find_one({'_id': int(b)})
        nombrepdf="limite_de_consistencia_astm"+ session['cedula']+".pdf"
        return [datos_solicitud['ensayo'],datos_solicitud,nombrepdf]


#----------------------------------------------------------------------------------------------------------------------


#****************************************** proctor astm **************************************************************
    def calculo_proctor_modificado_astm(self,**kwargs):
        proctor_astm = db['ensayo_proctor_modificado_astm']
        sueloss = db['ensayos_de_suelos']
        if sueloss.find_one({'_id': 1}) is None:
            kwargs['_id'] = 1
        else:
            id_max = self.buscar_id_max(sueloss)
            kwargs['_id'] = id_max

        P=ensayo().proctor_modificado_astm(kwargs['datos_muestra_laboratorio'][0],kwargs['datos_muestra_laboratorio'][1],kwargs['datos_muestra_laboratorio'][2],kwargs['datos_muestra_laboratorio'][4],kwargs['_id'], kwargs['usuario'],kwargs['ci'],"proctor",'proctor_astm')
        if P[0]==1:
            return P
        else:
            suelos_genral={'datos_generales':kwargs['datos_generales'],'ensayo':kwargs['ensayo'],'_id':kwargs['_id']}
            kwargs['datos_muestra_laboratorio'][0].pop(4)
            kwargs['datos_muestra_laboratorio'][0].append(P.pop(6))
            kwargs['direccion_de_grafico'] = P[5].pop(2)
            kwargs['resultados_del_ensayo'] = P
            proctor_astm.insert(kwargs)
            sueloss.insert(suelos_genral)
        return [None]


    def modificar_calculo_proctor_modificado_astm(self,**kwargs):
        proctor_astm = db['ensayo_proctor_modificado_astm']
        sueloss = db['ensayos_de_suelos']

        P=ensayo().proctor_modificado_astm(kwargs['datos_muestra_laboratorio'][0],kwargs['datos_muestra_laboratorio'][1],kwargs['datos_muestra_laboratorio'][2],kwargs['datos_muestra_laboratorio'][4],kwargs['_id'], kwargs['usuario'],kwargs['ci'],"proctor",'proctor_astm')
        if P[0]==1:
            return P
        else:
            kwargs['datos_muestra_laboratorio'][0].pop(4)
            kwargs['datos_muestra_laboratorio'][0].append(P.pop(6))
            kwargs['direccion_de_grafico'] = P[5].pop(2)
            proctor_astm.update({"_id": {"$eq": int(kwargs['_id'])}}, {"$set": {"datos_generales": kwargs['datos_generales'],"datos_muestra_laboratorio": kwargs['datos_muestra_laboratorio'], "resultados_del_ensayo": P,"direccion_de_grafico": kwargs['direccion_de_grafico']}}, upsert=False, multi=False)
            sueloss.update({"_id": {"$eq": int(kwargs['_id'])}}, {"$set":{"datos_generales":kwargs['datos_generales']}}, upsert=False, multi=False)
        return [None]


    def mostrar_datos_proctor_astm(self):
        proctor_astm = db['ensayo_proctor_modificado_astm']
        id_max = self.usuario_maximo(proctor_astm)
        listasss = proctor_astm.find_one({'_id': id_max})
        return listasss


    def reporte_proctor_modificado_astm(self,b):
        coleccion = db['ensayo_proctor_modificado_astm']  #conectar con las colecciones
        datos_solicitud = coleccion.find_one({'_id': int(b)})
        nombrepdf="proctor_modificado_astm"+ session['cedula']+".pdf"
        return [datos_solicitud['ensayo'], datos_solicitud, nombrepdf]
#----------------------------------------------------------------------------------------------------------------------


#****************************************  LIMITES DE CONSISTENCIA AASHTO *********************************************
    def calculo_limites_de_consistencia_aashto(self,**kwargs):
        limites = db['ensayo_limites_de_consistencia_aashto']
        sueloss = db['ensayos_de_suelos']
        if sueloss.find_one({'_id': 1}) is None:kwargs['_id'] = 1
        else:
            id_max = self.buscar_id_max(sueloss)
            kwargs['_id'] = id_max
        L=ensayo().Calculo_limite_liquido(kwargs['datos_muestra_laboratorio'][1],kwargs['datos_muestra_laboratorio'][2],kwargs['_id'],kwargs['usuario'],kwargs['ci'],'ll_aashto')
        if L[0]==1:
            return L
        else:
            suelos_genral={'datos_generales':kwargs['datos_generales'],'ensayo':kwargs['ensayo'],'_id':kwargs['_id']}
            kwargs['direccion_de_grafico'] = L[0][4].pop()
            kwargs['resultados_del_ensayo'] = L
            print "dato=",kwargs
            limites.insert(kwargs)
            sueloss.insert(suelos_genral)
        return [None]


    def modificar_calculo_limites_aashto(self,**kwargs):
        limites = db['ensayo_limites_de_consistencia_aashto']
        sueloss = db['ensayos_de_suelos']
        L = ensayo().Calculo_limite_liquido(kwargs['datos_muestra_laboratorio'][1],kwargs['datos_muestra_laboratorio'][2], kwargs['_id'], kwargs['usuario'],kwargs['ci'],'ll_aashto')
        if L[0] == 1:
            return L
        else:
            kwargs['direccion_de_grafico'] = L[0][4].pop()
            direccion_grafico=kwargs['direccion_de_grafico']
            limites.update({"_id": {"$eq": int(kwargs['_id'])}}, {"$set": {"datos_generales": kwargs['datos_generales'],"datos_muestra_laboratorio": kwargs['datos_muestra_laboratorio'], "resultados_del_ensayo": L,"direccion_de_grafico": direccion_grafico}}, upsert=False, multi=False)
            sueloss.update({"_id": {"$eq": int(kwargs['_id'])}}, {"$set":{"datos_generales":kwargs['datos_generales']}}, upsert=False, multi=False)
        return [None]


    def mostrar_datos_limites_aashto(self):
        limites = db['ensayo_limites_de_consistencia_aashto']
        id_max = self.usuario_maximo(limites)
        listasss = limites.find_one({'_id': id_max})
        return listasss

    def lista_limite_liquido_aashto(self):
        LL = []
        roles = db['ensayo_limites_de_consistencia_aashto']
        list_LL = roles.find()
        for i in list_LL:
            lista = []
            R1 = i["resultados_del_ensayo"][0][4][0][0]
            R2 =i["resultados_del_ensayo"][2]
            lista.append(R1)
            lista.append(R2)
            LL.append(lista)
        return LL





    def reporte_limite_de_consistencia_aashto(self,b):
        coleccion = db['ensayo_limites_de_consistencia_aashto']  #conectar con las colecciones
        datos_solicitud = coleccion.find_one({'_id': int(b)})
        nombrepdf="limite_de_consistencia_astm"+ session['cedula']+".pdf"
        return [datos_solicitud['ensayo'], datos_solicitud, nombrepdf]


#----------------------------------------------------------------------------------------------------------------------



#****************************************** proctor AASHTO **************************************************************
    def calculo_proctor_modificado_aashto(self,**kwargs):
        proctor_astm = db['ensayo_proctor_modificado_aashto']
        sueloss = db['ensayos_de_suelos']
        if sueloss.find_one({'_id': 1}) is None:
            kwargs['_id'] = 1
        else:
            id_max = self.buscar_id_max(sueloss)
            kwargs['_id'] = id_max

        P=ensayo().proctor_modificado_astm(kwargs['datos_muestra_laboratorio'][0],kwargs['datos_muestra_laboratorio'][1],kwargs['datos_muestra_laboratorio'][2],kwargs['datos_muestra_laboratorio'][4],kwargs['_id'], kwargs['usuario'],kwargs['ci'],"proctor",'proctor_aashto')
        if P[0]==1:
            return P
        else:
            suelos_genral={'datos_generales':kwargs['datos_generales'],'ensayo':kwargs['ensayo'],'_id':kwargs['_id']}
            kwargs['datos_muestra_laboratorio'][0].pop(4)
            kwargs['datos_muestra_laboratorio'][0].append(P.pop(6))
            kwargs['direccion_de_grafico'] = P[5].pop(2)
            kwargs['resultados_del_ensayo'] = P
            proctor_astm.insert(kwargs)
            sueloss.insert(suelos_genral)
        return [None]


    def modificar_calculo_proctor_modificado_aashto(self,**kwargs):
        proctor_aashto = db['ensayo_proctor_modificado_aashto']
        sueloss = db['ensayos_de_suelos']

        P=ensayo().proctor_modificado_astm(kwargs['datos_muestra_laboratorio'][0],kwargs['datos_muestra_laboratorio'][1],kwargs['datos_muestra_laboratorio'][2],kwargs['datos_muestra_laboratorio'][4],kwargs['_id'], kwargs['usuario'],kwargs['ci'],"proctor",'proctor_aashto')
        if P[0]==1:
            return P
        else:
            kwargs['datos_muestra_laboratorio'][0].pop(4)
            kwargs['datos_muestra_laboratorio'][0].append(P.pop(6))
            kwargs['direccion_de_grafico'] = P[5].pop(2)
            proctor_aashto.update({"_id": {"$eq": int(kwargs['_id'])}}, {"$set": {"datos_generales": kwargs['datos_generales'],"datos_muestra_laboratorio": kwargs['datos_muestra_laboratorio'], "resultados_del_ensayo": P,"direccion_de_grafico": kwargs['direccion_de_grafico']}}, upsert=False, multi=False)
            sueloss.update({"_id": {"$eq": int(kwargs['_id'])}}, {"$set":{"datos_generales":kwargs['datos_generales']}}, upsert=False, multi=False)
        return [None]


    def mostrar_datos_proctor_aashto(self):
        proctor_aashto = db['ensayo_proctor_modificado_aashto']
        id_max = self.usuario_maximo(proctor_aashto)
        listasss = proctor_aashto.find_one({'_id': id_max})
        return listasss


    def reporte_proctor_modificado_aashto(self,b):
        coleccion = db['ensayo_proctor_modificado_aashto']  #conectar con las colecciones
        datos_solicitud = coleccion.find_one({'_id': int(b)})
        nombrepdf="proctor_modificado_aashto"+ session['cedula']+".pdf"
        return [datos_solicitud['ensayo'], datos_solicitud, nombrepdf]
#----------------------------------------------------------------------------------------------------------------------










#****************************************** proctor AASHTO ESTANDAR  **************************************************************
    def calculo_proctor_estandar_aashto(self,**kwargs):

        proctor_estandar = db['ensayo_proctor_estandar_aashto']
        sueloss = db['ensayos_de_suelos']
        if sueloss.find_one({'_id': 1}) is None:
            kwargs['_id'] = 1
        else:
            id_max = self.buscar_id_max(sueloss)
            kwargs['_id'] = id_max

        P=ensayo().proctor_modificado_astm(kwargs['datos_muestra_laboratorio'][0],kwargs['datos_muestra_laboratorio'][1],kwargs['datos_muestra_laboratorio'][2],kwargs['datos_muestra_laboratorio'][4],kwargs['_id'], kwargs['usuario'],kwargs['ci'],"proctor",'proctor_estandar_aashto')
        if P[0]==1:
            return P
        else:
            suelos_genral={'datos_generales':kwargs['datos_generales'],'ensayo':kwargs['ensayo'],'_id':kwargs['_id']}
            kwargs['datos_muestra_laboratorio'][0].pop(4)
            kwargs['datos_muestra_laboratorio'][0].append(P.pop(6))
            kwargs['direccion_de_grafico'] = P[5].pop(2)
            kwargs['resultados_del_ensayo'] = P
            proctor_estandar.insert(kwargs)
            sueloss.insert(suelos_genral)
        return [None]


    def Modelo_modificar_proctor_estandar_aashto(self,**kwargs):
        proctor_aashto = db['ensayo_proctor_estandar_aashto']
        sueloss = db['ensayos_de_suelos']

        P=ensayo().proctor_modificado_astm(kwargs['datos_muestra_laboratorio'][0],kwargs['datos_muestra_laboratorio'][1],kwargs['datos_muestra_laboratorio'][2],kwargs['datos_muestra_laboratorio'][4],kwargs['_id'], kwargs['usuario'],kwargs['ci'],"proctor",'proctor_estandar_aashto')
        if P[0]==1:
            return P
        else:
            kwargs['datos_muestra_laboratorio'][0].pop(4)
            kwargs['datos_muestra_laboratorio'][0].append(P.pop(6))
            kwargs['direccion_de_grafico'] = P[5].pop(2)
            proctor_aashto.update({"_id": {"$eq": int(kwargs['_id'])}}, {"$set": {"datos_generales": kwargs['datos_generales'],"datos_muestra_laboratorio": kwargs['datos_muestra_laboratorio'], "resultados_del_ensayo": P,"direccion_de_grafico": kwargs['direccion_de_grafico']}}, upsert=False, multi=False)
            sueloss.update({"_id": {"$eq": int(kwargs['_id'])}}, {"$set":{"datos_generales":kwargs['datos_generales']}}, upsert=False, multi=False)
        return [None]


    def mostrar_datos_proctor_estandar_aashto(self):
        proctor_aashto = db['ensayo_proctor_estandar_aashto']
        id_max = self.usuario_maximo(proctor_aashto)
        listasss = proctor_aashto.find_one({'_id': id_max})
        return listasss


    def reporte_proctor_estandar_aashto(self,b):
        coleccion = db['ensayo_proctor_estandar_aashto']  #conectar con las colecciones
        datos_solicitud = coleccion.find_one({'_id': int(b)})
        nombrepdf="proctor_estandar_aashto"+ session['cedula']+".pdf"
        return [datos_solicitud['ensayo'], datos_solicitud, nombrepdf]
# #----------------------------------------------------------------------------------------------------------------------


#******************************** LISTA PROCTOR ***********************************************
    def lista_proctor_astm(self):
        prctor_astm = []
        roles = db['ensayo_proctor_modificado_astm']
        list_LL = roles.find()
        for i in list_LL:
            R1 = i["resultados_del_ensayo"][5][0]
            prctor_astm.append(R1)
        return prctor_astm

    def lista_proctor_modificado_aashto(self):
        prctor_astm = []
        roles = db['ensayo_proctor_modificado_aashto']
        list_LL = roles.find()
        for i in list_LL:
            R1 = i["resultados_del_ensayo"][5][0]
            prctor_astm.append(R1)
        return prctor_astm


    def lista_proctor_estandar_aashto(self):
        prctor_astm = []
        roles = db['ensayo_proctor_estandar_aashto']
        list_LL = roles.find()
        for i in list_LL:
            R1 = i["resultados_del_ensayo"][5][0]
            prctor_astm.append(R1)
        return prctor_astm

    def lista_total_proctor(self):
        total=self.lista_proctor_astm()+self.lista_proctor_modificado_aashto()+self.lista_proctor_estandar_aashto()
        return list(set(total))


#********************************************* GRANULOMETRIA **********************************************************
    def calculo_granulometrico_aashto(self,**kwargs):
        granulometria = db['ensayo_granulometria_aashto']
        sueloss = db['ensayos_de_suelos']

        if sueloss.find_one({'_id': 1}) is None:kwargs['_id'] = 1
        else:
            id_max = self.buscar_id_max(sueloss)
            kwargs['_id'] = id_max

        g=ensayo().granulometria_aashto(kwargs['datos_muestra_laboratorio'][0],kwargs['datos_muestra_laboratorio'][1],kwargs['datos_muestra_laboratorio'][2],kwargs['datos_muestra_laboratorio'][3],kwargs['datos_muestra_laboratorio'][4],kwargs['_id'],kwargs['usuario'],kwargs['ci'])
        if g[0] ==1:
            return g
        else:
            suelos_genral = {'datos_generales': kwargs['datos_generales'], 'ensayo': kwargs['ensayo'],'_id': kwargs['_id']}
            kwargs['direccion_de_grafico'] = g.pop()
            kwargs['resultados_del_ensayo'] = g
            granulometria.insert(kwargs)
            sueloss.insert(suelos_genral)
        return [None]


    def modificar_calculo_granulometrico_aashto(self,**kwargs):
        granulometria = db['ensayo_granulometria_aashto']
        sueloss = db['ensayos_de_suelos']

        g=ensayo().granulometria_aashto(kwargs['datos_muestra_laboratorio'][0],kwargs['datos_muestra_laboratorio'][1],kwargs['datos_muestra_laboratorio'][2],kwargs['datos_muestra_laboratorio'][3],kwargs['datos_muestra_laboratorio'][4],kwargs['_id'],kwargs['usuario'],kwargs['ci'])
        if g[0] ==1:
            return g
        else:
            kwargs['direccion_de_grafico'] = g.pop()
            granulometria.update({"_id": {"$eq": int(kwargs['_id'])}}, {"$set": {"datos_generales": kwargs['datos_generales'],"datos_muestra_laboratorio": kwargs['datos_muestra_laboratorio'], "resultados_del_ensayo": g,"direccion_de_grafico": kwargs['direccion_de_grafico']}}, upsert=False, multi=False)
            sueloss.update({"_id": {"$eq": int(kwargs['_id'])}}, {"$set":{"datos_generales":kwargs['datos_generales']}}, upsert=False, multi=False)


        return [None]



    def mostrar_datos_granulometria_aashto(self):
        granulometria = db['ensayo_granulometria_aashto']
        id_max = self.usuario_maximo(granulometria)
        listasss = granulometria.find_one({'_id': id_max})
        return listasss

    def reporte_granulometria_aashto(self,b):
        coleccion = db['ensayo_granulometria_aashto']  #conectar con las colecciones
        datos_solicitud = coleccion.find_one({'_id': int(b)})
        nombrepdf="granulometria_aashto"+ session['cedula']+".pdf"
        return [datos_solicitud['ensayo'], datos_solicitud, nombrepdf]


# #-----------------------------------------------------------------------------------------------------------------------

# *************************************** LIMITE DE CONTRACCION *********************************************************
    def calculo_limite_de_contraccion_astm(self,**kwargs):
        limite_contraccion = db['ensayo_limite_de_contraccion_astm']
        sueloss = db['ensayos_de_suelos']
        datos_adicionales_de_ensayo=db['datos_adicionales_de_ensayos']
        datos_ad = datos_adicionales_de_ensayo.find_one({'_id': int(1)})



        if sueloss.find_one({'_id': 1}) is None:
            kwargs['_id'] = 1
        else:
            id_max = self.buscar_id_max(sueloss)
            kwargs['_id'] = id_max

        limite_de_contraccion=ensayo().calculo_limite_de_contraccion(kwargs['datos_muestra_laboratorio'],datos_ad['densidad_H2O'])

        if limite_de_contraccion[0]==1:
            return limite_de_contraccion
        else:
            kwargs['resultados_del_ensayo']=limite_de_contraccion
            suelos_genral={'datos_generales':kwargs['datos_generales'],'ensayo':kwargs['ensayo'],'_id':kwargs['_id']}
            limite_contraccion.insert(kwargs)
            sueloss.insert(suelos_genral)
        return [None]

    def mostrar_datos_limite_de_contraccion(self):
        ensayo_limite_contraccion = db['ensayo_limite_de_contraccion_astm']
        id_max = self.usuario_maximo(ensayo_limite_contraccion)
        listasss = ensayo_limite_contraccion.find_one({'_id': id_max})
        return listasss



    def modificar_calculo_limite_de_contraccion(self,**kwargs):
        limite_c = db['ensayo_limite_de_contraccion_astm']
        sueloss = db['ensayos_de_suelos']
        datos_adicionales_de_ensayo = db['datos_adicionales_de_ensayos']
        datos_ad = datos_adicionales_de_ensayo.find_one({'_id': int(1)})

        limite_contraccion = ensayo().calculo_limite_de_contraccion(kwargs['datos_muestra_laboratorio'],datos_ad['densidad_H2O'])
        if limite_contraccion[0] == 1:
            return limite_contraccion
        else:
            limite_c.update({"_id": {"$eq": int(kwargs['_id'])}}, {"$set":{"datos_generales":kwargs['datos_generales'],"datos_muestra_laboratorio":kwargs['datos_muestra_laboratorio'],"resultados_del_ensayo":limite_contraccion}}, upsert=False, multi=False)
            sueloss.update({"_id": {"$eq": int(kwargs['_id'])}}, {"$set":{"datos_generales":kwargs['datos_generales']}}, upsert=False, multi=False)

        return [None]


    def reporte_limite_de_contraccion_astm(self,b):
        coleccion = db['ensayo_limite_de_contraccion_astm']  #conectar con las colecciones
        datos_solicitud = coleccion.find_one({'_id': int(b)})
        nombrepdf=session['cedula']+"limite_de_contraccion_astm"+".pdf"
        return [datos_solicitud['ensayo'], datos_solicitud, nombrepdf]


#-----------------------------------------------------------------------------------------------------------------------



#************************************** CONO DE ARENA ASTM ************************************************************
    def calculo_cono_de_arena_astm(self, **kwargs):
        cono_arena_astm = db['ensayo_cono_de_arena_astm']
        sueloss = db['ensayos_de_suelos']

        if sueloss.find_one({'_id': 1}) is None:kwargs['_id'] = 1
        else:
            id_max = self.buscar_id_max(sueloss)
            kwargs['_id'] = id_max

        Cono=ensayo().calculo_cono_de_arena(kwargs['datos_muestra_laboratorio'][1])
        if Cono[0] ==1:
            return Cono
        else:
            suelos_genral = {'datos_generales': kwargs['datos_generales'], 'ensayo': kwargs['ensayo'],'_id': kwargs['_id']}
            kwargs['resultados_del_ensayo'] = Cono
            print kwargs
            cono_arena_astm.insert(kwargs)
            sueloss.insert(suelos_genral)
        return [None]

    def mostrar_cono_de_arena_astm(self):
        ensayo_cono_arena_astm = db['ensayo_cono_de_arena_astm']
        id_max = self.usuario_maximo(ensayo_cono_arena_astm)
        listasss = ensayo_cono_arena_astm.find_one({'_id': id_max})
        return listasss


    def modificar_calculo_cono_de_arena_astm(self,**kwargs):
        ensayo_cono_arena_astm = db['ensayo_cono_de_arena_astm']
        sueloss = db['ensayos_de_suelos']
        datos_adicionales_de_ensayo = db['datos_adicionales_de_ensayos']
        datos_ad = datos_adicionales_de_ensayo.find_one({'_id': int(1)})

        cono_arena_astm = ensayo().calculo_cono_de_arena(kwargs['datos_muestra_laboratorio'][1])
        if cono_arena_astm[0] == 1:
            return cono_arena_astm
        else:
            ensayo_cono_arena_astm.update({"_id": {"$eq": int(kwargs['_id'])}}, {"$set":{"datos_generales":kwargs['datos_generales'],"datos_muestra_laboratorio":kwargs['datos_muestra_laboratorio'],"resultados_del_ensayo":cono_arena_astm}}, upsert=False, multi=False)
            sueloss.update({"_id": {"$eq": int(kwargs['_id'])}}, {"$set":{"datos_generales":kwargs['datos_generales']}}, upsert=False, multi=False)
        return [None]



    def reporte_cono_de_arena_astm(self,b):
        coleccion = db['ensayo_cono_de_arena_astm']  #conectar con las colecciones
        datos_solicitud = coleccion.find_one({'_id': int(b)})
        nombrepdf=session['cedula']+"cono_de_arena_astm"+".pdf"
        return [datos_solicitud['ensayo'], datos_solicitud, nombrepdf]
#-----------------------------------------------------------------------------------------------------------------------




#************************************** CBR ASTM ************************************************************
    def calculo_CBR_astm(self, **kwargs):
        cbr_astm = db['ensayo_CBR_astm']
        geotecniaa = db['ensayos_de_geotecnia']
        datos_adicionales_de_ensayo = db['datos_adicionales_de_ensayos']
        datos_ad = datos_adicionales_de_ensayo.find_one({'_id': int(1)})

        if geotecniaa.find_one({'_id': 1}) is None:kwargs['_id'] = 1
        else:
            id_max = self.buscar_id_max(geotecniaa)
            kwargs['_id'] = id_max
        cbr=ensayo().calculo_ensayo_CBR(kwargs['datos_muestra_laboratorio'][0],kwargs['datos_muestra_laboratorio'][1],kwargs['datos_muestra_laboratorio'][2][1],kwargs['datos_muestra_laboratorio'][3],datos_ad[kwargs['datos_muestra_laboratorio'][4]],kwargs['usuario'],kwargs['ci'],kwargs['_id'],'cbr_astm')
        if cbr[0] ==1:
            return cbr
        else:

            geotecnia_genral = {'datos_generales': kwargs['datos_generales'], 'ensayo': kwargs['ensayo'],'_id': kwargs['_id']}
            kwargs['direccion_de_grafico']=cbr[2][2].pop(1)
            kwargs['resultados_del_ensayo'] = cbr
            print "dato=",kwargs
            cbr_astm.insert(kwargs)
            geotecniaa.insert(geotecnia_genral)
        return [None]

    def mostrar_indice_de_soporte_cbr_astm(self):
        cbr = db['ensayo_CBR_astm']
        id_max = self.usuario_maximo(cbr)
        listasss = cbr.find_one({'_id': id_max})
        return listasss


    def modificar_calculo_cbr_astm(self,**kwargs):
        cbr_astm = db['ensayo_CBR_astm']
        geotecniaa = db['ensayos_de_geotecnia']
        datos_adicionales_de_ensayo = db['datos_adicionales_de_ensayos']
        datos_ad = datos_adicionales_de_ensayo.find_one({'_id': int(1)})

        cbr=ensayo().calculo_ensayo_CBR(kwargs['datos_muestra_laboratorio'][0],kwargs['datos_muestra_laboratorio'][1],kwargs['datos_muestra_laboratorio'][2][1],kwargs['datos_muestra_laboratorio'][3],datos_ad[kwargs['datos_muestra_laboratorio'][4]],kwargs['usuario'],kwargs['ci'],kwargs['_id'],'cbr_astm')
        if cbr[0] ==1:
            return cbr
        else:
            kwargs['direccion_de_grafico'] = cbr[2][2].pop(1)
            cbr_astm.update({"_id": {"$eq": int(kwargs['_id'])}}, {"$set": {"datos_generales": kwargs['datos_generales'],"datos_muestra_laboratorio": kwargs['datos_muestra_laboratorio'], "resultados_del_ensayo": cbr,"direccion_de_grafico": kwargs['direccion_de_grafico']}}, upsert=False, multi=False)
            geotecniaa.update({"_id": {"$eq": int(kwargs['_id'])}}, {"$set":{"datos_generales":kwargs['datos_generales']}}, upsert=False, multi=False)
        return [None]



    def reporte_indice_de_soporte_cbr_astm(self,b):
        coleccion = db['ensayo_CBR_astm']  #conectar con las colecciones
        datos_solicitud = coleccion.find_one({'_id': int(b)})
        nombrepdf=session['cedula']+"indice_de_soporte_CBR_ASTM"+".pdf"
        return [datos_solicitud['ensayo'], datos_solicitud, nombrepdf]
# #-----------------------------------------------------------------------------------------------------------------------





#************************************** CORTE DIRECTO ASTM ************************************************************
    def calculo_corte_directo_astm(self, **kwargs):
        corte_dir = db['ensayo_corte_directo_astm']
        geotecniaa = db['ensayos_de_geotecnia']

        if geotecniaa.find_one({'_id': 1}) is None:kwargs['_id'] = 1
        else:
            id_max = self.buscar_id_max(geotecniaa)
            kwargs['_id'] = id_max
        C_Directo=ensayo().ensayo_corte_directo(kwargs['datos_muestra_laboratorio'][0],kwargs['datos_muestra_laboratorio'][1],kwargs['datos_muestra_laboratorio'][2],kwargs['_id'],kwargs['usuario'],kwargs['ci'])
        if C_Directo[0] ==1:
            return C_Directo
        else:

            suelos_genral = {'datos_generales': kwargs['datos_generales'], 'ensayo': kwargs['ensayo'],'_id': kwargs['_id']}
            kwargs['direccion_de_grafico']=C_Directo.pop()
            kwargs['resultados_del_ensayo'] = C_Directo
            corte_dir.insert(kwargs)
            geotecniaa.insert(suelos_genral)
        return [None]

    def mostrar_corte_directo_astm(self):
        corte_d = db['ensayo_corte_directo_astm']
        id_max = self.usuario_maximo(corte_d)
        listasss = corte_d.find_one({'_id': id_max})
        return listasss


    def modificar_calculo_corte_directo_astm(self,**kwargs):
        corte_dir = db['ensayo_corte_directo_astm']
        geotecniaa = db['ensayos_de_geotecnia']


        C_Directo=ensayo().ensayo_corte_directo(kwargs['datos_muestra_laboratorio'][0],kwargs['datos_muestra_laboratorio'][1],kwargs['datos_muestra_laboratorio'][2],kwargs['_id'],kwargs['usuario'],kwargs['ci'])
        if C_Directo[0] ==1:
            return C_Directo
        else:
            kwargs['direccion_de_grafico'] = C_Directo.pop()
            corte_dir.update({"_id": {"$eq": int(kwargs['_id'])}}, {"$set": {"datos_generales": kwargs['datos_generales'],"datos_muestra_laboratorio": kwargs['datos_muestra_laboratorio'], "resultados_del_ensayo": C_Directo,"direccion_de_grafico": kwargs['direccion_de_grafico']}}, upsert=False, multi=False)
            geotecniaa.update({"_id": {"$eq": int(kwargs['_id'])}}, {"$set":{"datos_generales":kwargs['datos_generales']}}, upsert=False, multi=False)
        return [None]



    def reporte_corte_directo_geotecnia(self,b):
        coleccion = db['ensayo_corte_directo_astm']  #conectar con las colecciones
        datos_solicitud = coleccion.find_one({'_id': int(b)})
        nombrepdf=session['cedula']+"corte_directo_geotecnia"+".pdf"
        return [datos_solicitud['ensayo'], datos_solicitud, nombrepdf]
# # #-----------------------------------------------------------------------------------------------------------------------



# ************************************* ENSAYOS GENRAL DE GEOTECNIA   *************************************************
    def mostrar_lista_de_ensayos_de_geotecnia(self):
        solicitudes_completo = []
        solicitudes = db['ensayos_de_geotecnia']
        list_solicitudes = solicitudes.find()
        for i in list_solicitudes:
            solicitud = []
            v1 = i["_id"]
            v2 = i["ensayo"]
            v3 = i["datos_generales"][4]
            v4 = i["datos_generales"][5]
            v5 = i["datos_generales"][1]
            v6 = i["datos_generales"][2]
            v7 = i["datos_generales"][6]
            v8 = i["datos_generales"][7]

            solicitud.append(v1)
            solicitud.append(v2)
            solicitud.append(v3)
            solicitud.append(v4)
            solicitud.append(v5)
            solicitud.append(v6)
            solicitud.append(v7)
            solicitud.append(v8)
            solicitudes_completo.append(tuple(solicitud))
        return tuple(solicitudes_completo)


    def eliminar_lista_ensayos_geotecnia(self,id):
        geotecniaa = db['ensayos_de_geotecnia']
        ensayo_suelos = geotecniaa.find_one({'_id': int(id)})
        GEOTECNIA = ensayo_suelos['ensayo']

        if GEOTECNIA=='INDICE DE SOPORTE CALIFORNIA CBR (ASTM D1883-99)'.decode('utf-8').strip():
            CBR = db['ensayo_CBR_astm']
            CBR.remove({'_id': int(id)})
            geotecniaa.remove({'_id': int(id)})
            return True
        else:
            if GEOTECNIA == 'CORTE DIRECTO (ASTM D3080)':
                CORTE_dir = db['ensayo_corte_directo_astm']
                CORTE_dir.remove({'_id': int(id)})
                geotecniaa.remove({'_id': int(id)})
                return True

        return False









#**********************************************************************************************************************







#-------------------------------------- ENSAYOS EN GNERAL DE SUELOS ---------------------------------------------------
#
    def mostrar_lista_de_ensayos_de_suelos(self):
        solicitudes_completo = []
        solicitudes = db['ensayos_de_suelos']
        list_solicitudes = solicitudes.find()
        for i in list_solicitudes:
            solicitud = []
            v1 = i["_id"]
            v2 = i["ensayo"]
            v3 = i["datos_generales"][4]
            v4 = i["datos_generales"][5]
            v5 = i["datos_generales"][1]
            v6 = i["datos_generales"][2]
            v7 = i["datos_generales"][6]
            v8 = i["datos_generales"][7]

            solicitud.append(v1)
            solicitud.append(v2)
            solicitud.append(v3)
            solicitud.append(v4)
            solicitud.append(v5)
            solicitud.append(v6)
            solicitud.append(v7)
            solicitud.append(v8)
            solicitudes_completo.append(tuple(solicitud))
        return tuple(solicitudes_completo)




#--------------------------------------- FIN --------------------------------------------------------------------------
    def eliminar_lista_ensayos_suelos(self,id):
        sueloss = db['ensayos_de_suelos']
        ensayo_suelos = sueloss.find_one({'_id': int(id)})
        ENSUELO = ensayo_suelos['ensayo']

        if ENSUELO=="CONTENIDO DE HUMEDAD (ASTM D2216)":
            contenido_humedad = db['ensayo_contenido_de_humedad']
            contenido_humedad.remove({'_id': int(id)})
            sueloss.remove({'_id': int(id)})
            return True
        else:
            if ENSUELO == "LIMITES DE CONSISTENCIA (ASTM D4318)":
                limites = db['ensayo_limites_de_consistencia_astm']
                limites.remove({'_id': int(id)})
                sueloss.remove({'_id': int(id)})
                return True
            else:
                if ENSUELO == "GRANULOMETRIA (ASTM D422)":
                    granulometria = db['ensayo_granulometria_astm']
                    granulometria.remove({'_id': int(id)})
                    sueloss.remove({'_id': int(id)})
                    return True
                else:
                    if ENSUELO == "COMPACTACION PROCTOR MODIFICADO (ASTM D1557)":
                        proctor_astm = db['ensayo_proctor_modificado_astm']
                        proctor_astm.remove({'_id': int(id)})
                        sueloss.remove({'_id': int(id)})
                        return True
                    else:
                        if ENSUELO == "LIMITES DE CONSISTENCIA (AASHTO T-89)":
                            limites_aashto = db['ensayo_limites_de_consistencia_aashto']
                            limites_aashto.remove({'_id': int(id)})
                            sueloss.remove({'_id': int(id)})
                            return True
                        else:
                            if ENSUELO == "COMPACTACION PROCTOR MODIFICADO (AASHTO T-180)":
                                proctor_aashto = db['ensayo_proctor_modificado_aashto']
                                proctor_aashto.remove({'_id': int(id)})
                                sueloss.remove({'_id': int(id)})
                                return True
                            else:
                                if ENSUELO == "COMPACTACION PROCTOR ESTANDAR (AASHTO T-99)":
                                    proctor_aashto = db['ensayo_proctor_estandar_aashto']
                                    proctor_aashto.remove({'_id': int(id)})
                                    sueloss.remove({'_id': int(id)})
                                    return True
                                else:
                                    if ENSUELO == 'GRANULOMETRIA (AASHTO T-27)':
                                        granulometria_aashto = db['ensayo_granulometria_aashto']
                                        granulometria_aashto.remove({'_id': int(id)})
                                        sueloss.remove({'_id': int(id)})
                                        return True
                                    else:
                                        if ENSUELO == 'LIMITE DE CONTRACCIÓN (ASTM D427)'.decode('utf-8').strip():
                                            limite_contraccion = db['ensayo_limite_de_contraccion_astm']
                                            limite_contraccion.remove({'_id': int(id)})
                                            sueloss.remove({'_id': int(id)})
                                            return True
                                        else:
                                            if ENSUELO == 'CONO DE ARENA (ASTM D1556-64)'.decode('utf-8').strip():
                                                cono_arena = db['ensayo_cono_de_arena_astm']
                                                cono_arena.remove({'_id': int(id)})
                                                sueloss.remove({'_id': int(id)})
                                                return True


        return True