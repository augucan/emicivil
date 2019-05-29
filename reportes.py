# -*- coding: utf-8 -*-
from arrow import *  # utcnow, get
from reportlab import *
# from reportlab import PermissionError
from reportlab.lib.units import inch, mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle, Frame, KeepInFrame, PageBreak
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.lib.colors import black, purple, white, blue,gray
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter,A4,landscape
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle


from flask_pymongo import PyMongo
from flask import Flask
# from  pymongo  import  MongoClient
import os

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'civil_emi'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/civil_emi'  # taller_grado_civil
mongo = PyMongo(app)


# ======================= CLASE reportePDF =========================

class reportePDF(object):



    def __init__(self, titulo, cabecera, datos, nombrePDF):
        print '1'
        super(reportePDF, self).__init__()
        self.titulo = titulo
        self.cabecera = cabecera
        print "dtossss",datos
        self.datos = datos
        self.nombrePDF = nombrePDF
        self.estilos = getSampleStyleSheet()

    # @staticmethod
    def pagina_uno(self,canvas, archivoPDF):
        print '2'

        canvas.saveState()
        estilos = getSampleStyleSheet()

        alineacion = ParagraphStyle(name="alineacion", alignment=TA_RIGHT, fontSize=7,
                                    parent=estilos["Normal"])

        # Encabezado
        # FORMATO CAJETILLA
        valorY = 780
        valorY2 = 720
        canvas.line(50, valorY, 560, valorY)  # punto x1, y1 , x2, y2 #HORIZONTAL
        canvas.line(50, valorY, 50, valorY2)  # VERTICAL
        canvas.line(50, valorY2, 560, valorY2)  # HORIZONTAL
        canvas.line(560, valorY, 560, valorY2)  # VERTICAL
        canvas.line(190, valorY, 190, valorY2)  # VERTICAL
        canvas.line(400, valorY, 400, valorY2)  # VERTICAL
        # CAJETIN PEQUENO
        altura_aux = 20
        canvas.line(400, 745 + altura_aux, 560, 745 + altura_aux)  # HORIZONTAL
        canvas.line(400, 730 + altura_aux, 560, 730 + altura_aux)  # HORIZONTAL
        canvas.line(400, 715 + altura_aux, 560, 715 + altura_aux)  # HORIZONTAL
        canvas.line(465, 760 + altura_aux, 465, 715 + altura_aux)  # VERTICAL
        canvas.drawImage('static/img/emi.jpeg', 65, 730, width=115, height=40)

        canvas.setFont('Helvetica', 10)
        canvas.drawString(407, 750 + altura_aux, 'Codigo:')
        canvas.drawString(407, 735 + altura_aux, 'Aprobacion:')
        canvas.drawString(407, 720 + altura_aux, 'Version:')
        # Datos
        canvas.setFont('Helvetica', 8)
        canvas.drawString(480, 750 + altura_aux, 'C5117-9')
        canvas.drawString(480, 720 + altura_aux, 'Version 1.1')

        canvas.setFont('Helvetica', 14)
        frame1 = Frame(190, 720, 210, 60, showBoundary=1)  # Frame(movX,movY,margenAncho,mrgenAlto)
        bodyStyle = ParagraphStyle('normal', fontSize=16, leading=20, spaceBefore=10, alignment=TA_CENTER)
        s = self.titulo
        story = [Paragraph(s, bodyStyle)]
        story_inframe = KeepInFrame(280, 1 * inch, story)
        frame1.addFromList([story_inframe], canvas)
        # fin

        fecha = utcnow().to("local").format("dddd, DD / MMMM / YYYY", locale="es")
        fechaReporte = fecha.replace("-", "de")

        encabezadoFecha = Paragraph(fechaReporte, alineacion)
        anchura, altura = encabezadoFecha.wrap(archivoPDF.width, archivoPDF.topMargin)
        encabezadoFecha.drawOn(canvas, archivoPDF.leftMargin - 6, 750)  # PARA CAMBIAR LA ALTURA DE LA FECHA

        # Pie de pagina
        piePagina = Paragraph("Reporte generado ingenieria civi.", estilos["Normal"])
        anchura, altura = piePagina.wrap(archivoPDF.width, archivoPDF.bottomMargin)
        piePagina.drawOn(canvas, archivoPDF.leftMargin, 1 * mm + (0.2 * inch))


        px3 = 50
        px4 = 560
        canvas.line(px3, 80, px4, 80)  # punto x1, y1 , x2, y2 #HORIZONTAL
        canvas.line(px3, 35, px4, 35)  # punto x1, y1 , x2, y2 #HORIZONTAL
        canvas.line(px3, 80, px3, 35)  # VERTICAL
        canvas.line(px3, 70, px4, 70)  # HORIZONTAL
        canvas.line(px4, 80, px4, 35)  # VERTICAL
        canvas.line(220, 80, 220, 35)  # VERTICAL
        canvas.line(390, 80, 390, 35)  # VERTICAL
        # DATOS ACREDITACION
        canvas.setFont('Helvetica', 8)
        canvas.drawString(px3 + 40, 72, 'ELABORADO POR')
        canvas.drawString(px3 + 220, 72, 'REVISADO POR')
        canvas.drawString(px3 + 380, 72, 'APROBADO POR')
        # Suelta el lienzo
        canvas.restoreState()

    # @staticmethod
    def _encabezadoPiePagina(self, canvas, archivoPDF):
        print '3'
        canvas.saveState()
        estilos = getSampleStyleSheet()

        alineacion = ParagraphStyle(name="alineacion", alignment=TA_RIGHT, fontSize=7,
                                    parent=estilos["Normal"])

        # Encabezado
        # FORMATO CAJETILLA
        valorY = 780
        valorY2 = 720
        canvas.line(50, valorY, 560, valorY)  # punto x1, y1 , x2, y2 #HORIZONTAL
        canvas.line(50, valorY, 50, valorY2)  # VERTICAL
        canvas.line(50, valorY2, 560, valorY2)  # HORIZONTAL
        canvas.line(560, valorY, 560, valorY2)  # VERTICAL
        canvas.line(190, valorY, 190, valorY2)  # VERTICAL
        canvas.line(400, valorY, 400, valorY2)  # VERTICAL
        # CAJETIN PEQUENO
        altura_aux = 20
        canvas.line(400, 745 + altura_aux, 560, 745 + altura_aux)  # HORIZONTAL
        canvas.line(400, 730 + altura_aux, 560, 730 + altura_aux)  # HORIZONTAL
        canvas.line(400, 715 + altura_aux, 560, 715 + altura_aux)  # HORIZONTAL
        canvas.line(465, 760 + altura_aux, 465, 715 + altura_aux)  # VERTICAL
        canvas.drawImage("static/img/emi.jpeg", 65, 730, width=115, height=40)

        canvas.setFont('Helvetica', 10)
        canvas.drawString(410, 750 + altura_aux, 'Codigo:')
        canvas.drawString(407, 735 + altura_aux, 'Aprobacion:')
        canvas.drawString(407, 720 + altura_aux, 'Version:')
        # Datos
        canvas.setFont('Helvetica', 8)
        canvas.drawString(480, 750 + altura_aux, 'C5117-9')
        canvas.drawString(480, 720 + altura_aux, 'Version 1.1')

        canvas.setFont('Helvetica', 14)
        frame1 = Frame(190, 720, 210, 60, showBoundary=1)  # Frame(movX,movY,margenAncho,mrgenAlto)
        bodyStyle = ParagraphStyle('normal', fontSize=16, leading=10, spaceBefore=10, alignment=TA_CENTER)
        s = self.titulo
        story = [Paragraph(s, bodyStyle)]
        story_inframe = KeepInFrame(280, 1 * inch, story)
        frame1.addFromList([story_inframe], canvas)
        # fin

        fecha = utcnow().to("local").format("dddd, DD / MMMM / YYYY", locale="es")
        fechaReporte = fecha.replace("-", "de")

        encabezadoFecha = Paragraph(fechaReporte, alineacion)
        anchura, altura = encabezadoFecha.wrap(archivoPDF.width, archivoPDF.topMargin)
        encabezadoFecha.drawOn(canvas, archivoPDF.leftMargin - 6, 750)  # PARA CAMBIAR LA ALTURA DE LA FECHA

        # Pie de pagina
        piePagina = Paragraph("Reporte generado por ingenieria civil.", estilos["Normal"])
        anchura, altura = piePagina.wrap(archivoPDF.width, archivoPDF.bottomMargin)
        piePagina.drawOn(canvas, archivoPDF.leftMargin, 1 * mm + (0.2 * inch))
        # Suelta el lienzo
        canvas.restoreState()

    def convertirDatos(self):
        print '4'
        """Convertir la lista de diccionarios a una lista de listas para crear
           la tabla PDF."""

        estiloEncabezado = ParagraphStyle(name="estiloEncabezado", alignment=TA_LEFT,
                                          fontSize=8, textColor=white,
                                          fontName="Helvetica-Bold",
                                          parent=self.estilos["Normal"])

        estiloNormal = self.estilos["Normal"]
        estiloNormal.alignment = TA_LEFT
        estiloNormal.fontSize = 8 #cambiar tamano de la letra del contenido

        claves, nombres = zip(*[[k, n] for k, n in self.cabecera])

        encabezado = [Paragraph(nombre, estiloEncabezado) for nombre in nombres]
        nuevosDatos = [tuple(encabezado)]

        for dato in self.datos:
            nuevosDatos.append([Paragraph(str(dato[clave]), estiloNormal) for clave in claves])

        return nuevosDatos
    def Exportar(self):
        print '5'
        """Exportar los datos a un archivo PDF."""

        alineacionTitulo = ParagraphStyle(name="centrar", alignment=TA_CENTER, fontSize=13,
                                          leading=20, textColor=white,
                                          parent=self.estilos["Heading1"])

        self.ancho, self.alto = letter

        convertirDatos = self.convertirDatos()

        tabla = Table(convertirDatos, colWidths=(self.ancho - 100) / len(self.cabecera)+ 5, hAlign="CENTER")
        tabla.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), gray),
            ("ALIGN", (0, 0), (0, -1), "LEFT"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),  # Texto centrado y alineado a la izquierda
            ("INNERGRID", (0, 0), (-1, -1), 0.50, black),  # Lineas internas
            ("BOX", (0, 0), (-1, -1), 0.25, black),  # Linea (Marco) externa
            #('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ]))

        historia = []
        historia.append(Paragraph(self.titulo, alineacionTitulo))
        historia.append(Spacer(1, 0.16 * inch))
        historia.append(tabla)

        archivoPDF = SimpleDocTemplate(self.nombrePDF, leftMargin=50, rightMargin=50, pagesize=letter,
                                       title="Reportes PDF", author="jhon")

        try:
            archivoPDF.build(historia, onFirstPage=self.pagina_uno,
                             onLaterPages=self._encabezadoPiePagina,
                             canvasmaker=numeracionPaginas)

            # +------------------------------------+
            return True
            # +------------------------------------+
        #except PermissionErro:
        except True:
            # +--------------------------------------------+
            return False
            # +--------------------------------------------+


# ================== CLASE numeracionPaginas =======================

class numeracionPaginas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        print '6'
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        print '7'
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        print '8'
        #Agregar informacion de la pagina a cada pagina (pagina x de y)
        numeroPaginas = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(numeroPaginas)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, conteoPaginas):
        print '9'
        self.setFont('Helvetica', 10)
        self.drawRightString(180 * mm, 250 * mm + (0.2 * inch),
                             "Pagina {} de {}".format(self._pageNumber, conteoPaginas))


        # ===================== FUNCIoN generarReporte =====================
