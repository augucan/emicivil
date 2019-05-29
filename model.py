# from flask_proyecto.controller.controller import controler

from controller import controler

class Modelo:

    def __init__(self):
        pass


    def modelo_login(self,nombre,password):
        return controler().ingresar_alsistema(nombre,password)

    def Modelo_empleado (self,nombre_usuario,contrasena,rol,estado,nombre,apellido,ci,especialidad,email,cargo,ff):
        return controler().crear_empleado(nombre_usuario, contrasena, rol, estado, nombre, apellido, ci, especialidad,
                                          email, cargo, ff)
    def Modelo_mostrar_empleado(self):
        return controler().mostrar_empleado()
    def lista_roles(self):
        return controler().lista_roles()

    def Modelo_actualizar_empleado(self,id,nombre_usuario,contrasena,rol,estado,nombre,apellido,ci,especialidad,email,cargo,ff):
        return controler().actualizar_empleado(id,nombre_usuario,contrasena,rol,estado,nombre,apellido,ci,especialidad,email,cargo,ff)
    def Modelo_eliminar(self,id):
        return controler().eliminar_empleado(id)
    def Modelo_reporte_empleado(self):
        return controler().reporte_empleado()

    def Modelo_estudiante(self,nombre_usuario,contrasena,rol,semestre,nombre,apellido,ci,codigo,correo,estado):
        return controler().crear_estudiante(nombre_usuario,contrasena,rol,semestre,nombre,apellido,ci,codigo,correo,estado)
    def Modelo_mostrar_estudiante(self):
        return controler().mostrar_estudiante()
    def Modelo_actualizar_estudiante(self,id,rol,semestre,nombre,apellido,ci,codigo,correo,estado):
        return controler().actualizar_estudiante(id,rol,semestre,nombre,apellido,ci,codigo,correo,estado)
    def Modelo_eliminar_estudiante(self,id):
        return controler().eliminar_estudiante(id)
    def Modelo_reporte_estudiante(self):
        return controler().reporte_estudiante()




    def Modelo_rol(self,rol_usuario,privilegios):
        return controler().crear_rol(rol_usuario,privilegios)
    def Modelo_mostrar_roles(self):
        return controler().mostrar_roles()
    def Modelo_actualizar_roles(self,id,rol,privilegios):
        return controler().actualizar_roles(id,rol,privilegios)
    def Modelo_eliminar_rol(self,id):
        return controler().eliminar_rol(id)



    def Modelo_clientes(self, nombre_cliente,apellido_cliente,ci_cliente,email_cliente,telefono_cliente):
        return controler().crear_cliente(nombre_cliente,apellido_cliente,ci_cliente,email_cliente,telefono_cliente)
    def Modelo_mostrar_clientes(self):
        return controler().mostrar_clientes()
    def Modelo_actualizar_cliente(self,id,nombre_cliente,apellido_cliente,ci_cliente,email_cliente,telefono_cliente):
        return controler().actualizar_cliente(id,nombre_cliente,apellido_cliente,ci_cliente,email_cliente,telefono_cliente)
    def Modelo_eliminar_cliente(self,id):
        return controler().eliminar_cliente(id)
    def Modelo_reporte_cliente(self):
        return controler().reporte_cliente()
#-----------------------------------------------------------------------------------------------------------------------
    def Modelo_solicitud_trabajo_externo(self, **kwargs):
        return controler().crear_solicitud_trabajo_externo(**kwargs)
    def Modelo_mostrar_solicitud_trabajo_externo(self):
        return controler().mostrar_solicitu_trabajo_esterno()
    def Modelo_actualizar_actualizar_solicitud_trabajo_externo(self,**kwargs):
        return controler().actualizar_solicitud_trabajo_externo(**kwargs)
    def Modelo_eliminar_solicitud_trabajo_externo(self,id):
        return controler().eliminar_solicitud_trabajo_externo(id)
    def Modelo_reporte_solicitud_trabajo_externo(self):
        return controler().reporte_solicitud_trabajo_externo()



    def Modelo_solicitud_laboratorio(self,**kwargs):
        return controler().guardar_solicitud_laboratorio(**kwargs)
    def Modelo_select_dinamico(self,dato):
        return controler().retorna_datos_select_dinamico(dato)
    def Modelo_select_materiales(self,dato):
        return controler().retorna_datos_select_materiales(dato)
    def Modelo_select_reactivos(self,dato):
        return controler().retorna_datos_select_reactivos(dato)
    def Modelo_mostrar_solicitudes_laboratorio(self):
        return controler().mostrar_solicitudes_laboratorio()
    def Modelo_aceptacion_solicitud(self,id):
        return controler().enviar_correo_de_aceptacion(id)
    def Modelo_rechazo_de_solicitud(self,id):
        return controler().enviar_correo_de_rechazo(id)
    def Modelo_observaciones(self,id,observaciones):
        return controler().observaciones_solocitud_laboratorio(id,observaciones)
    def Modelo_eliminar_solicitudes_lab(self,id):
        return controler().eliminar_solicitud_laboratorio(id)
    def Modelo_reporte_solicitud_laboratorio(self):
        return controler().reporte_solicitud_laboratorio()
    def Modelo_reporte_formulario_solicitud_laboratorio(self,b):
        return controler().reporte_formulario_solicitud_laboratorio(b)



    def Modelo_registrar_equipos(self,nombreactivo,codanterior,codactivo,estadoactivo,fechacompra,descripcionactivo,ensayo_utilizado):
        return controler().registrar_equipos(nombreactivo,codanterior,codactivo,estadoactivo,fechacompra,descripcionactivo,ensayo_utilizado)
    def Modelo_mostrar_equipos(self):
        return controler().mostrar_equipos_laboratorio()
    def Modelo_actualizar_equipos(self,id,nombreactivo,codanterior,codactivo,estadoactivo,fechacompra,descripcionactivo,ensayo_utilizado):
        return controler().actualizar_equipos(id,nombreactivo,codanterior,codactivo,estadoactivo,fechacompra,descripcionactivo,ensayo_utilizado)
    def Modelo_eliminar_global(self,id):
        return controler().eliminar_gloval(id)
    def Modelo_mostrar_lista(self):
        return controler().mostrar_lista_equipos()
    def Modelo_reporte_equipos(self):
        return controler().reporte_equipos()



    def Modelo_registrar_materiales(self,nombreactivo,fecharegistro,descripcionactivo,ensayo_utilizado):
        return controler().registrar_materiales(nombreactivo,fecharegistro,descripcionactivo,ensayo_utilizado)
    def Modelo_mostrar_materiales(self):
        return controler().mostrar_materiales_laboratorio()
    def Modelo_actualizar_materiales(self,id,nombreactivo,descripcionactivo,ensayo_utilizado):
        return controler().actualizar_materiales(id,nombreactivo,descripcionactivo,ensayo_utilizado)
    def Modelo_eliminar_materiales(self,id):
        return controler().eliminar_materiales(id)
    # def Modelo_mostrar_lista(self):
    #     return controler().mostrar_lista_equipos()
    def Modelo_reporte_materiales(self):
        return controler().reporte_materiales()




    #//////////////////////////////////////////////////

    def Modelo_registrar_reactivos(self, nombreactivo,fecha_vencimiento, fecharegistro,ensayo_utilizado):
        return controler().registrar_reactivos(nombreactivo,fecha_vencimiento, fecharegistro,ensayo_utilizado)

    def Modelo_mostrar_reactivos(self):
        return controler().mostrar_reactivos_laboratorio()

    def Modelo_actualizar_reactivos(self, id, nombreactivo, fechavencimiento, ensayo_utilizado):
        return controler().actualizar_reactivos(id, nombreactivo, fechavencimiento, ensayo_utilizado)

    def Modelo_eliminar_reactivo(self, id):
        return controler().eliminar_reactivos(id)
    #     # def Modelo_mostrar_lista(self):
    #     #     return controler().mostrar_lista_equipos()
    def Modelo_reporte_reactivos(self):
        return controler().reporte_reactivos()




    def Modelo_solicitud_de_equipos(self,**kwargs):
        return controler().guardar_solicitud_de_equipos(**kwargs)
    def Modelo_mostrar_solicitudes_equipos(self):
        return controler().mostrar_solicitudes_equipo()
    def Modelo_aceptacion_solicitud_equipo(self,id):
        return controler().enviar_correo_de_aceptacion_solicitud_equipo(id)
    def Modelo_rechazo_de_solicitud_equipos(self,id):
        return controler().enviar_correo_de_rechazo_solicitud_equipo(id)
    def Modelo_observaciones_solicitud_equipos(self,id,observaciones):
        return controler().observaciones_solocitud_equipos(id,observaciones)
    def Modelo_eliminar_solicitudes_equipos(self,id):
        return controler().eliminar_solicitud_equipos(id)
    def Modelo_reporte_solicitud_equipos(self):
        return controler().reporte_solicitud_equipos()
    def Modelo_reporte_formulario_solicitud_equipos(self,b):
        return controler().reporte_formulario_solicitud_equipos(b)


# ******************************************* ENSAYOS******************************************************************


# ******************************************* CONTENIDO DE HUMEDAD ****************************************************
    def Modelo_calculo_contenido_humedad(self,**kwargs):
        return controler().calculo_contenido_humedad(**kwargs)
    def Modelo_modificar_calculo_contenido_humedad(self,**kwargs):
        return controler().modificar_calculo_contenido_humedad(**kwargs)
    def Modelo_mostrar_datos_contenido_humedad(self):
        return controler().mostrar_datos_contenido_humedad()
    def Modelo_reporte_contenido_humedad(self,b):
        return controler().reporte_contenido_de_humedad(b)
# *********************************************************************************************************************


# ******************************************* GRANULOMETRIA ASTM ****************************************************
    def Modelo_granulometria(self,**kwargs):
        return controler().calculo_granulometrico(**kwargs)
    def Modelo_modificar_calculo_granulometria(self,**kwargs):
        return controler().modificar_calculo_granulometrico(**kwargs)
    def Modelo_mostrar_datos_granulometria(self):
        return controler().mostrar_datos_granulometria()
    def Modelo_lista_limite_liquido(self):
        return controler().lista_limite_liquido()
    def Modelo_reporte_granulometria_astm(self,b):
        return controler().reporte_granulometria_astm(b)
# *********************************************************************************************************************



# ******************************************* LIMIMTES DE CONSISTENCIA ASTM *******************************************
    def Modelo_limites_de_consistencia_astm(self,**kwargs):
        return controler().calculo_limites_de_consistencia_astm(**kwargs)
    def Modelo_modificar_calculo_limites_astm(self,**kwargs):
        return controler().modificar_calculo_limites_astm(**kwargs)
    def Modelo_mostrar_datos_limites_astm(self):
        return controler().mostrar_datos_limites_astm()
    def Modelo_reporte_limite_de_consistencia_astm_d4318(self,b):
        return controler().reporte_limite_de_consistencia_astm(b)
# # ********************************************************************************************************************




#********************************************** PROCTOR MODIFICADO ASTM ************************************************
    def Modelo_calculo_proctor_modificado_astm(self,**kwargs):
        return controler().calculo_proctor_modificado_astm(**kwargs)
    def Modelo_modificar_proctor_modificado_astm(self,**kwargs):
        return controler().modificar_calculo_proctor_modificado_astm(**kwargs)
    def Modelo_mostrar_datos_proctor_astm(self):
        return controler().mostrar_datos_proctor_astm()
    def Modelo_reporte_proctor_modificado_astm(self,b):
        return controler().reporte_proctor_modificado_astm(b)
#***********************************************************************************************************************




# ******************************************* LIMIMTES DE CONSISTENCIA AASHTO *******************************************
    def Modelo_limites_de_consistencia_aashto(self,**kwargs):
        return controler().calculo_limites_de_consistencia_aashto(**kwargs)
    def Modelo_modificar_calculo_limites_aashto(self,**kwargs):
        return controler().modificar_calculo_limites_aashto(**kwargs)
    def Modelo_mostrar_datos_limites_aashto(self):
        return controler().mostrar_datos_limites_aashto()
    def Modelo_reporte_limite_de_consistencia_aashto_t89(self,b):
        return controler().reporte_limite_de_consistencia_aashto(b)
# # ********************************************************************************************************************

#********************************************** PROCTOR MODIFICADO AASHTO ************************************************
    def Modelo_calculo_proctor_modificado_aashto(self,**kwargs):
        return controler().calculo_proctor_modificado_aashto(**kwargs)
    def Modelo_modificar_proctor_modificado_aashto(self,**kwargs):
        return controler().modificar_calculo_proctor_modificado_aashto(**kwargs)
    def Modelo_mostrar_datos_proctor_aashto(self):
        return controler().mostrar_datos_proctor_aashto()
    def Modelo_reporte_proctor_modificado_aashto(self,b):
        return controler().reporte_proctor_modificado_aashto(b)
#***********************************************************************************************************************


#********************************************** PROCTOR MODIFICADO AASHTO ************************************************
    def Modelo_calculo_proctor_estandar_aashto(self,**kwargs):
        return controler().calculo_proctor_estandar_aashto(**kwargs)
    def Modelo_modificar_proctor_estandar_aashto(self,**kwargs):
        return controler().Modelo_modificar_proctor_estandar_aashto(**kwargs)
    def Modelo_mostrar_datos_proctor_estandar_aashto(self):
        return controler().mostrar_datos_proctor_estandar_aashto()
    def Modelo_reporte_proctor_estandar_aashto(self,b):
        return controler().reporte_proctor_estandar_aashto(b)
#***********************************************************************************************************************

# ******************************************* GRANULOMETRIA AASHTO ****************************************************
    def Modelo_granulometria_aashto(self,**kwargs):
        return controler().calculo_granulometrico_aashto(**kwargs)
    def Modelo_modificar_calculo_granulometria_aashto(self,**kwargs):
        return controler().modificar_calculo_granulometrico_aashto(**kwargs)
    def Modelo_mostrar_datos_granulometria_aashto(self):
        return controler().mostrar_datos_granulometria_aashto()
    def Modelo_lista_limite_liquido_aashto(self):
        return controler().lista_limite_liquido_aashto()
    def Modelo_reporte_granulometria_aashto(self,b):
        return controler().reporte_granulometria_aashto(b)
# *********************************************************************************************************************

# ******************************************* LIMITE DE CONTRACCION ****************************************************
    def Modelo_calculo_limite_de_contraccion_astm(self,**kwargs):
        return controler().calculo_limite_de_contraccion_astm(**kwargs)
    def Modelo_modificar_calculo_limite_de_contraccion(self,**kwargs):
        return controler().modificar_calculo_limite_de_contraccion(**kwargs)
    def Modelo_mostrar_datos_limite_de_contraccion(self):
        return controler().mostrar_datos_limite_de_contraccion()
    def Modelo_reporte_limite_de_contraccion_astm(self,b):
        return controler().reporte_limite_de_contraccion_astm(b)
# *********************************************************************************************************************



#******************************************** CONO DE ARENA ASTM *****************************************************
    def Modelo_calculo_cono_de_arena(self,**kwargs):
        return controler().calculo_cono_de_arena_astm(**kwargs)
    def Modelo_lista_proctor_densidad_maxima(self):
        return controler().lista_total_proctor()
    def Modelo_mostrar_datos_cono_de_arena_astm(self):
        return controler().mostrar_cono_de_arena_astm()
    def Modelo_modificar_calculo_cono_de_arena_astm(self, **kwargs):
        return controler().modificar_calculo_cono_de_arena_astm(**kwargs)
    def Modelo_reporte_cono_de_arena_astm(self, b):
        return controler().reporte_cono_de_arena_astm(b)
#*********************************************************************************************************************

#*********************************** LISTA DE ENSAYOS DE SUELOS ********************************************************
    def Modelo_mostrar_lista_de_ensayos_de_suelos(self):
        return controler().mostrar_lista_de_ensayos_de_suelos()

    def Modelo_reporte_lista_ensayos_suelos(self,b):
        return controler().reporte_lista_ensayos_suelos(b)

    def Modelo_eliminar_lista_ensayos_suelos(self,id):
        return controler().eliminar_lista_ensayos_suelos(id)
#***********************************************************************************************************************




########################################## ensayos geotecnia ########################################################

# ******************************************** INDICE DE SOPORTE CBR ASTM *****************************************************
    def Modelo_calculo_CBR_astm(self, **kwargs):
        return controler().calculo_CBR_astm(**kwargs)

    def Modelo_mostrar_datos_indice_de_soporte_cbr_astm(self):
        return controler().mostrar_indice_de_soporte_cbr_astm()

    def Modelo_modificar_calculo_cbr_astm(self, **kwargs):
        return controler().modificar_calculo_cbr_astm(**kwargs)

    def Modelo_reporte_indice_de_soporte_cbr_astm(self, b):
        return controler().reporte_indice_de_soporte_cbr_astm(b)
# *********************************************************************************************************************


# ******************************************** CORTE DIRECTO ASTM *****************************************************
    def Modelo_calculo_corte_directo_astm(self, **kwargs):
        return controler().calculo_corte_directo_astm(**kwargs)

    def Modelo_mostrar_corte_directo_astm(self):
        return controler().mostrar_corte_directo_astm()

    def Modelo_modificar_calculo_corte_directo_astm(self, **kwargs):
        return controler().modificar_calculo_corte_directo_astm(**kwargs)

    def Modelo_reporte_corte_directo_geotecnia(self, b):
        return controler().reporte_corte_directo_geotecnia(b)
# ***********************************************************************************************************************
#*********************************** LISTA DE ENSAYOS DE SUELOS ********************************************************
    def Modelo_mostrar_lista_de_ensayos_de_geotecnia(self):
        return controler().mostrar_lista_de_ensayos_de_geotecnia()

#
    def Modelo_eliminar_lista_ensayos_geotecnia(self,id):
        return controler().eliminar_lista_ensayos_geotecnia(id)
#***********************************************************************************************************************

######################################################################################################################