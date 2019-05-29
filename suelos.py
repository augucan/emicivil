# -*- coding: utf-8 -*-


from copy import deepcopy
import numpy
from matplotlib import pyplot as grafico
from math import pi
from fractions import Fraction




# plotly.tools.set_credentials_file(username='Carlosc13', api_key='KI1HaRwXbP7QectILvC0')

class ensayo:
    def __init__(self):
        self.y=[]
        self.dencidad=[]

    def calculo_contenido_humedad(self,total1,estado):
        resultados = []
        resta1=[]
        resta2=[]
        contenido_humedad = []
        self.inicio = len(total1)
        w = 0
        total = 0
        b = 0
        f = 0
        for i in range(len(total1)):

            if (float(total1[i][2]) - float(total1[i][0]))==0:
                return [1,"error divicion entre cero (0)"+str(i+1)]
            else:
                w = ((float(total1[i][1]) - float(total1[i][2])) / (float(total1[i][2]) - float(total1[i][0]))) * 100
                resta1.append(round(float(total1[i][1]) - float(total1[i][2]),2))
                resta2.append(round(float(total1[i][2]) - float(total1[i][0]),2))
                if w<0:
                    return [1,"error del ensayo contenido humedad resultados negativos revisar datos incuerentes en la fila Nro :"+" "+str(i+1)]

            total = total + w
            if i == 0:
                b = w
            if i == self.inicio - 1:
                f = w

            if estado=="humedad":
                resultados.append(round(w, 2))
            if estado=="proctor":
                contenido_humedad.append(round(w, 2))

        print "total=",total
        print "self inicio",self.inicio
        tot = total / self.inicio
        a = (100 * abs(b - f)) / tot

        print tot,"sobrepasa lo== 7.8"
        if tot > 7.8:

            return [1,"Porecentaje de humedad total "+" " +str(round(tot,2))+"%"+"  "+" "+"El calculo del ensayo sobre pasa los valores de la desviacion establecida  Revisar Contenido de Humedad"]
        else:

            if estado=="proctor":
                resultados.append(contenido_humedad)
                resultados.append(resta1)
                resultados.append(resta2)
                return resultados
            else:
                resultados.append(round(tot,2))
                resultados.append(resta1[0])
                resultados.append(resta1[1])
                resultados.append(resta1[2])
                resultados.append(resta2[0])
                resultados.append(resta2[1])
                resultados.append(resta2[2])
                return resultados

#***********************************************************************************************************************




#********************************** GRANULOMETRIA **********************************************************************
    def granulometria(self,MR,masamuestra,MR2,masameteriseco,masa_retenida,id,usuario,cedula):
        self.tamiz=['3"','2"','1"','3/4"','1/2"','3/8"','1/4"','°4','°10','°30','°50','°100','°200','Bandeja']
        self.diametro=[76.200,50.800,25.400,19.100,12.700,9.500,6.400,4.750,2.000,0.600,0.300,0.150,0.075,0.000]
        bandera=0
        masa_retenida_acumulada=[]
        porcentaje_retenido=[]
        porcentaje_que_pasa=[]
        D10=0
        D30=0
        D60=0
        grava=0
        finos=0
        suma = 0
        suma_ms_ret = 0

        mas_muestra_seca=round(float(masamuestra)-float(MR),2)
        masa_seca_material_grueso=round(float(masameteriseco)-float(MR2),2)
        suma_material_fino=round(mas_muestra_seca-masa_seca_material_grueso,2)


        for a in range(len(self.tamiz)):
            if (len(self.tamiz)-1)==a:
                suma=suma + float(masa_retenida[a])+suma_material_fino
                masa_retenida_acumulada.append(round(suma,2))
            else:
                suma=suma + float(masa_retenida[a])
                masa_retenida_acumulada.append(round(suma,2))

        for c in range(len(self.tamiz)):
            suma2=(masa_retenida_acumulada[c]*100.0)/(masa_retenida_acumulada[len(self.tamiz)-1])
            porcentaje_retenido.append(round(suma2,2))
            porcentaje_que_pasa.append(round(100-porcentaje_retenido[c],2))
            suma_ms_ret = suma_ms_ret + float(masa_retenida[c])




        desface=((masa_seca_material_grueso - suma_ms_ret) * 100) / masa_seca_material_grueso
        if desface>2:
            return [1,desface]
        else:
            direccion_grafico=self.grafica_granulometria(self.diametro,porcentaje_que_pasa,id,usuario,cedula)
            self.diametro.append(0.0)
            porcentaje_que_pasa.append(0.0)
            vector_original = porcentaje_que_pasa
            diametros = self.diametro
            vector_auxiliar_polar = deepcopy(vector_original)
            vector_auxiliar_polar.append(60)
            vector_auxiliar_polar.append(30)
            vector_auxiliar_polar.append(10)
            vector_auxiliar_polar.sort(reverse=True)

            for i in range(len(vector_auxiliar_polar)):
                if vector_auxiliar_polar[i] == 60:
                    for a in range(len(vector_original)):
                        if vector_original[a] == vector_auxiliar_polar[i - 1]:

                            D60 = self.polarizacion(vector_auxiliar_polar[i - 1],
                                                    vector_auxiliar_polar[i + 1],
                                                    diametros[a],
                                                    diametros[a + 1], 60)

                if vector_auxiliar_polar[i] == 30:
                    for a in range(len(vector_original)):
                        if vector_original[a] == vector_auxiliar_polar[i - 1]:

                            D30 = self.polarizacion(vector_auxiliar_polar[i - 1], vector_auxiliar_polar[i + 1],diametros[a],diametros[a + 1], 30)

                if vector_auxiliar_polar[i] == 10:
                    if vector_auxiliar_polar[i + 1] == 0:
                        bandera = 1
                    else:
                        for a in range(len(vector_original)):
                            if vector_original[a] == vector_auxiliar_polar[i - 1]:

                                D10 = self.polarizacion(vector_auxiliar_polar[i - 1],
                                                        vector_auxiliar_polar[i + 1],
                                                        diametros[a],
                                                        diametros[a + 1], 10)

            for i in range(len(self.tamiz)):
                if self.tamiz[i] == '°4':
                    grava = round(porcentaje_retenido[i],2)
                if self.tamiz[i] == '°200':
                    finos = round(porcentaje_que_pasa[i],2)

            if bandera == 1:
                D10 = 0
                Cc = 0
                Cu = 0
            else:
                Cc = (D30 ** 2 / (D10 * D60))
                Cu = (D60 / D10)

            masa_retenida.append(suma_ms_ret)
            return [[mas_muestra_seca,masa_seca_material_grueso,suma_material_fino],self.tamiz,self.diametro,masa_retenida,masa_retenida_acumulada,porcentaje_retenido,porcentaje_que_pasa,[D60,D30,D10],[round(Cc, 2),round(Cu, 2)],[grava,finos,round(100-finos-grava, 2)],direccion_grafico]






    def polarizacion(self, pasa1, pasa2, diametro1, diametro2, D):
        x = abs(((pasa1 - D) / (pasa1 - pasa2)) * (diametro1 - diametro2) - diametro1)
        return round(x, 2)

    def grafica_granulometria(self, diametro, porcentaje_que_pasa,id,usuario,cedula):
        diametro.pop()
        porcentaje_que_pasa.pop()
        fig1 = grafico.figure()
        grafico.plot(diametro,porcentaje_que_pasa, marker='o', color='b')
        grafico.gca().invert_xaxis()
        grafico.grid(True)
        grafico.xscale('log')
        grafico.ylabel("% QUE PASA")
        grafico.xlabel("DIAMETRO DE PARTICULAS mm")
        png = '.png'
        fig1.savefig('static/img/granulometria/' + "granulometria" +str (id) +str(usuario) +str(cedula))
        return 'img/granulometria/' + "granulometria" +str (id) +str(usuario) +str(cedula)+png




    def clasificacion_suelos_astm(self,retenido200,floqpasa200,retenido4,coeficiente_uniformidad,coeficiente_gradacion,indice_plasticidad,limite_liquido,id,usuario,cedula):

        resultado_clasificacion=[]
        xa = numpy.loadtxt("clasificacionX.txt")


        atterberg=0
        ya = []
        xu = numpy.arange(16, 76)
        yu = []

        for i in xa:
            a = round(0.73 * (i - 20), 2)
            ya.append(a)

        for i in xu:
            a = 0.9 * (i - 9)
            yu.append(a)

        fig2 = grafico.figure()
        grafico.plot(xa, ya, 'b-')
        grafico.plot(xu, yu, 'b--', c='r')
        grafico.scatter(float(limite_liquido),indice_plasticidad)#Y X
        grafico.grid(True)
        grafico.legend(['linea A','linea U'])
        grafico.xlabel("Limite Liquido(LL)")
        grafico.ylabel("Indice de Plasticidad(IP)")
        png = '.png'
        fig2.savefig('static/img/clasificacion astm/'+"clasificacion_suelos"  + str(id) + str(usuario))
        save_grafico='img/clasificacion astm/'+"clasificacion_suelos" + str(id) + str(usuario)+ png


        if float(limite_liquido) > 25:
            for z in range(len(xa)):
                if float(limite_liquido) == xa[z]:
                    if indice_plasticidad>ya[z]:
                        atterberg = 1
                    else:
                        atterberg = 0

        else:
            atterberg = 1
        SF=retenido200-retenido4
        Gf = retenido4
        sfdivgf = SF/Gf


        resultado_clasificacion.append(save_grafico)
        

        if retenido200>50:
            if retenido4>0.5:
                if floqpasa200<5 and coeficiente_uniformidad>=4 and coeficiente_gradacion<=3 and 1<=coeficiente_gradacion:
                    sigla="GW"


                    if SF<15:
                        resultado_clasificacion.append(sigla)
                        resultado_clasificacion.append("Grava bien gradada")
                        return resultado_clasificacion
                    if SF>=15:
                        resultado_clasificacion.append(sigla)
                        resultado_clasificacion.append("Grava bien gradada con arena")
                        return resultado_clasificacion


                if floqpasa200<5 and coeficiente_uniformidad<4 or coeficiente_gradacion>3 and coeficiente_gradacion<1:
                    sigla="GP"


                    if SF<15:
                        resultado_clasificacion.append(sigla)
                        resultado_clasificacion.append("Grava pobremente gradada")
                        return resultado_clasificacion
                    if SF>=15:
                        resultado_clasificacion.append(sigla)
                        resultado_clasificacion.append("Grava pobremente gradada con arena")
                        return resultado_clasificacion

                if floqpasa200>12 and indice_plasticidad<4 or atterberg==0:
                    sigla="GM"


                    if SF<15:
                        resultado_clasificacion.append(sigla)
                        resultado_clasificacion.append("Grava limosa")
                        return resultado_clasificacion
                    if SF>=15:
                        resultado_clasificacion.append(sigla)
                        resultado_clasificacion.append("Grava limosa con arena")
                        return resultado_clasificacion

                if floqpasa200>12 and indice_plasticidad>7 and atterberg==1:
                    sigla = "GC"

                    if SF<15:
                        resultado_clasificacion.append(sigla)
                        resultado_clasificacion.append("Grava arcillosa")
                        return resultado_clasificacion
                    if SF>=15:
                        resultado_clasificacion.append(sigla)
                        resultado_clasificacion.append("Grava arcilloza con arena")
                        return resultado_clasificacion

                if floqpasa200>12 and float(limite_liquido)<50 and indice_plasticidad<=7 and 4<=indice_plasticidad and atterberg==1:
                    sigla="GC-GM"

                    if SF<15:
                        resultado_clasificacion.append(sigla)
                        resultado_clasificacion.append("Grava limo arcillosa")
                        return resultado_clasificacion

                    if SF>=15:
                        resultado_clasificacion.append(sigla)
                        resultado_clasificacion.append("Grava limo arcillosa con arena")
                        return resultado_clasificacion


                if 5<=floqpasa200 and floqpasa200<=12 and floqpasa200<5 and indice_plasticidad<4 or atterberg==0:

                    sigla="GW-GM"


                    if SF<15:
                        resultado_clasificacion.append(sigla)
                        resultado_clasificacion.append("Grava bien gradada con limo")
                        return resultado_clasificacion
                    if SF>=15:
                        resultado_clasificacion.append(sigla)
                        resultado_clasificacion.append("Grava bien gradada con limo y arena")
                        return resultado_clasificacion


                if 5<=floqpasa200 and floqpasa200<=12 and floqpasa200<5 and indice_plasticidad>7 and atterberg==1:
                    print "Cumple los criterios de degradacion de GW y los criterios de plasticidad de GC"
                    sigla="GW-GC"


                    if SF<15:
                        resultado_clasificacion.append(sigla)
                        resultado_clasificacion.append("Grava bien gradada con arcilla")
                        return resultado_clasificacion
                    if SF>=15:
                        resultado_clasificacion.append(sigla)
                        resultado_clasificacion.append("Grava bien gradada con arcilla y arena")
                        return resultado_clasificacion

                if 5<=floqpasa200 and floqpasa200<=12 and floqpasa200<5 and indice_plasticidad<4 or atterberg==0:
                    sigla="GP-GM"


                    if SF<15:
                        resultado_clasificacion.append(sigla)
                        resultado_clasificacion.append("Grava pobremente gradada con limo")
                        return resultado_clasificacion
                    if SF>=15:
                        resultado_clasificacion.append(sigla)
                        resultado_clasificacion.append("Grava pobremente gradada con limo y arena")
                        return resultado_clasificacion


                if 5<=floqpasa200 and floqpasa200<=12 and floqpasa200<5 and indice_plasticidad>7 and atterberg==1:
                    sigla="GP-GC"

                    if SF<15:
                        resultado_clasificacion.append(sigla)
                        resultado_clasificacion.append("Grava pobremente gradada con arcilla")
                        return resultado_clasificacion
                    if SF>=15:
                        resultado_clasificacion.append(sigla)
                        resultado_clasificacion.append("Grava pobremente gradada con arcilla y arena")
                        return resultado_clasificacion



            if retenido4<=0.5:
                if floqpasa200<5 and coeficiente_uniformidad>=6 and coeficiente_gradacion>=1 and coeficiente_gradacion<=3:
                    sigla="SW"

                    if SF<15:
                        resultado_clasificacion.append(sigla)
                        resultado_clasificacion.append("Arena bien gradada")
                        return resultado_clasificacion
                    if SF>=15:
                        resultado_clasificacion.append(sigla)
                        resultado_clasificacion.append("Arena bien gradada con grava")
                        return resultado_clasificacion

                if floqpasa200<5 and coeficiente_uniformidad>=4 or coeficiente_gradacion>3 and coeficiente_gradacion<1:
                    sigla = "SP"

                    if SF<15:
                        resultado_clasificacion.append(sigla)
                        resultado_clasificacion.append("Arena pobremente gradada")
                        return resultado_clasificacion
                    if SF>=15:
                        resultado_clasificacion.append(sigla)
                        resultado_clasificacion.append("Arena pobremente gradada con grava")
                        return resultado_clasificacion

                if floqpasa200>12 and indice_plasticidad>7 or atterberg==0:
                    sigla = "SM"

                    if SF<15:
                        resultado_clasificacion.append(sigla)
                        resultado_clasificacion.append("Arena limosa")
                        return resultado_clasificacion
                    if SF>=15:
                        resultado_clasificacion.append(sigla)
                        resultado_clasificacion.append("Arena limosa con grava")
                        return resultado_clasificacion

                if floqpasa200>12 and indice_plasticidad>7 and atterberg==1:
                    sigla = "SC"

                    if SF < 15:
                        resultado_clasificacion.append(sigla)
                        resultado_clasificacion.append("Arena arcillosa")
                        return resultado_clasificacion
                    if SF >= 15:
                        resultado_clasificacion.append(sigla)
                        resultado_clasificacion.append("Arena arcillosa con grava")
                        return resultado_clasificacion

                if floqpasa200>12 and float(limite_liquido)<50 and indice_plasticidad>=4 and indice_plasticidad<=7 and atterberg==1:
                    sigla = "SC-SM"

                    if SF < 15:
                        resultado_clasificacion.append(sigla)
                        resultado_clasificacion.append("Arena limosa arcillosa")
                        return resultado_clasificacion
                    if SF >= 15:
                        resultado_clasificacion.append(sigla)
                        resultado_clasificacion.append("Arena limosa arcillosa con grava")
                        return resultado_clasificacion

                if floqpasa200>=5 and floqpasa200<=12 and floqpasa200<5 and indice_plasticidad<4 or atterberg==0:
                    sigla = "SW-SM"

                    if SF < 15:
                        resultado_clasificacion.append(sigla)
                        resultado_clasificacion.append("Arena bien gradada con limo")
                        return resultado_clasificacion
                    if SF >= 15:
                        resultado_clasificacion.append(sigla)
                        resultado_clasificacion.append("Arena bien gradada con limo y grava")
                        return resultado_clasificacion


                if floqpasa200>=5 and floqpasa200<=12 and floqpasa200<5 and indice_plasticidad>7 and atterberg==1:
                    #print "Cumple los criterios de gradacion de SW y los criterios de plasticidad de SC"
                    sigla = "SW-SC"

                    if SF < 15:
                        resultado_clasificacion.append(sigla)
                        resultado_clasificacion.append("Arena bien gradada con arcilla")
                        return resultado_clasificacion

                    if SF >= 15:
                        resultado_clasificacion.append(sigla)
                        resultado_clasificacion.append("Arena bien gradada con arcilla y grava")
                        return resultado_clasificacion


                if floqpasa200>=5 and floqpasa200<=12 and floqpasa200<5 and indice_plasticidad<4 or atterberg==0:
                    #print "Cumple los criterios de gradacion de SP y los criterios de plasticidad de SM"
                    sigla = "SP-SM"

                    if SF < 15:
                        resultado_clasificacion.append(sigla)
                        resultado_clasificacion.append("Arena pobremente gradada con limo")
                        return resultado_clasificacion

                    if SF >= 15:
                        resultado_clasificacion.append(sigla)
                        resultado_clasificacion.append("Arena pobremente gradada con limo y grava")
                        return resultado_clasificacion


                if floqpasa200>=5 and floqpasa200<=12 and floqpasa200<5 and indice_plasticidad>7 and atterberg==1:
                    #print "Cumple los criterios de gradacion de SP y los criterios de plasticidad de SC"
                    sigla = "Sp-SC"


                    if SF < 15:
                        resultado_clasificacion.append(sigla)
                        resultado_clasificacion.append("Arena pobremente gradada con arcilla")
                        return resultado_clasificacion
                    if SF >= 15:
                        resultado_clasificacion.append(sigla)
                        resultado_clasificacion.append("Arena pobremente gradada con arcilla y grava")
                        return resultado_clasificacion





        if retenido200<=50:
            if float(limite_liquido)<50:
                if indice_plasticidad<4 or atterberg==0:
                    sigla = "ML"


                    if retenido200<15:
                        resultado_clasificacion.append(sigla)
                        resultado_clasificacion.append("Limo")
                        return resultado_clasificacion
                    if retenido200>=15 and retenido200<=29 and sfdivgf>=1:
                        resultado_clasificacion.append(sigla)
                        resultado_clasificacion.append("Limo con arena")
                        return resultado_clasificacion
                    if retenido200>=15 and retenido200<=29 and sfdivgf<1:
                        resultado_clasificacion.append(sigla)
                        resultado_clasificacion.append("Limo con grava")
                        return resultado_clasificacion

                    if retenido200>=30 and sfdivgf>=1 and Gf<15:
                        resultado_clasificacion.append(sigla)
                        resultado_clasificacion.append("Limo arenoso")
                        return resultado_clasificacion

                    if retenido200>=30 and sfdivgf>=1 and Gf>=15:
                        resultado_clasificacion.append(sigla)
                        resultado_clasificacion.append("Limo arenoso con grava")
                        return resultado_clasificacion

                    if retenido200>=30 and sfdivgf<1 and SF<15:
                        resultado_clasificacion.append(sigla)
                        resultado_clasificacion.append("Limo gravoso")
                        return resultado_clasificacion

                    if retenido200>=30 and sfdivgf<1 and Gf>=15:
                        resultado_clasificacion.append(sigla)
                        resultado_clasificacion.append("Limo gravoso con arena")
                        return resultado_clasificacion




                if indice_plasticidad>7 and atterberg==1:
                    sigla = "CL"


                    if retenido200<15:
                        resultado_clasificacion.append(sigla)
                        resultado_clasificacion.append("Arcilla magra")
                        return resultado_clasificacion
                    if retenido200>=15 and retenido200<=29:
                        if sfdivgf>=1:
                            resultado_clasificacion.append(sigla)
                            resultado_clasificacion.append("Arcilla magra con arena")
                            return resultado_clasificacion

                        if sfdivgf<1:
                            resultado_clasificacion.append(sigla)
                            resultado_clasificacion.append("arcilla magra con grava")
                            return resultado_clasificacion

                    if retenido200>=30:
                        if sfdivgf>=1 and Gf<15:
                            resultado_clasificacion.append(sigla)
                            resultado_clasificacion.append("Arcilla magra arenosa")
                            return resultado_clasificacion

                        if sfdivgf>=1 and Gf>=15:
                            resultado_clasificacion.append(sigla)
                            resultado_clasificacion.append("Arcilla magra arenosa con grava")
                            return resultado_clasificacion

                        if sfdivgf<1 and SF<15:
                            resultado_clasificacion.append(sigla)
                            resultado_clasificacion.append("Arcilla magra gravosa")
                            return resultado_clasificacion

                        if sfdivgf<1 and SF>= 15:
                            resultado_clasificacion.append(sigla)
                            resultado_clasificacion.append("Arcilla magra gravosa con arena")
                            return resultado_clasificacion



                if indice_plasticidad>=4 and indice_plasticidad<=7 and atterberg==1:
                    sigla = "CL-ML"


                    if retenido200<15:
                        resultado_clasificacion.append(sigla)
                        resultado_clasificacion.append("Arcilla limosa")
                        return resultado_clasificacion

                    if retenido200>=15 and retenido200<=29 and sfdivgf>=1:
                        resultado_clasificacion.append(sigla)
                        resultado_clasificacion.append("Arcilla limosa con arena")
                        return resultado_clasificacion

                    if retenido200>=15 and retenido200<=29 and sfdivgf<1:
                        resultado_clasificacion.append(sigla)
                        resultado_clasificacion.append("Arcilla limosa con grava")
                        return resultado_clasificacion

                    if retenido200>=30 and sfdivgf>=1 and Gf<15:
                        resultado_clasificacion.append(sigla)
                        resultado_clasificacion.append("Arcilla limosa arenosa")
                        return resultado_clasificacion

                    if retenido200>=30 and sfdivgf>=1 and Gf>=15:
                        resultado_clasificacion.append(sigla)
                        resultado_clasificacion.append("Arcilla limosa arenosa con grava")
                        return resultado_clasificacion

                    if retenido200>=30 and sfdivgf<1 and SF<15:
                        resultado_clasificacion.append(sigla)
                        resultado_clasificacion.append("Arcilla limosa gravosa")
                        return resultado_clasificacion

                    if retenido200>=30 and sfdivgf<1 and SF>=15:
                        resultado_clasificacion.append(sigla)
                        resultado_clasificacion.append("Arcilla limosa gravosa con arena")
                        return resultado_clasificacion




            if float(limite_liquido)>=50:
                if atterberg==0:
                    sigla = "MH"


                    if retenido200<15:
                        resultado_clasificacion.append(sigla)
                        resultado_clasificacion.append("Limo elastico")
                        return resultado_clasificacion

                    if retenido200 >= 15 and retenido200 <= 29 and sfdivgf >= 1:
                        resultado_clasificacion.append(sigla)
                        resultado_clasificacion.append("Limo elastico con arena")
                        return resultado_clasificacion

                    if retenido200 >= 15 and retenido200 <= 29 and sfdivgf < 1:
                        resultado_clasificacion.append(sigla)
                        resultado_clasificacion.append("Limo elastico con grava")
                        return resultado_clasificacion

                    if retenido200>=30 and sfdivgf>=1 and Gf<15:
                        resultado_clasificacion.append(sigla)
                        resultado_clasificacion.append("Limo elastico arenoso")
                        return resultado_clasificacion

                    if retenido200>=30 and sfdivgf>=1 and Gf>=15:
                        resultado_clasificacion.append(sigla)
                        resultado_clasificacion.append("Limo elastico arenoso con grava")
                        return resultado_clasificacion

                    if retenido200>=30 and sfdivgf<1 and SF<15:
                        resultado_clasificacion.append(sigla)
                        resultado_clasificacion.append("Limo elastico gravoso")
                        return resultado_clasificacion

                    if retenido200>=30 and sfdivgf<1 and SF>=15:
                        resultado_clasificacion.append(sigla)
                        resultado_clasificacion.append("Limo elastico gravoso con arena")
                        return resultado_clasificacion




                if atterberg==1:
                    sigla = "CH"


                    if retenido200<15:
                        resultado_clasificacion.append(sigla)
                        resultado_clasificacion.append("Arcilla grasa")
                        return resultado_clasificacion

                    if retenido200 >= 15 and retenido200 <= 29 and sfdivgf >= 1:
                        resultado_clasificacion.append(sigla)
                        resultado_clasificacion.append("Arcilla grasa con arena")
                        return resultado_clasificacion

                    if retenido200 >= 15 and retenido200 <= 29 and sfdivgf < 1:
                        resultado_clasificacion.append(sigla)
                        resultado_clasificacion.append("Arcilla grasa con grava")
                        return resultado_clasificacion

                    if retenido200>=30 and sfdivgf>=1 and Gf<15:
                        resultado_clasificacion.append(sigla)
                        resultado_clasificacion.append("Arcilla grasa arenosa")
                        return resultado_clasificacion

                    if retenido200>=30 and sfdivgf>=1 and Gf>=15:
                        resultado_clasificacion.append(sigla)
                        resultado_clasificacion.append("Arcilla grasa arenosa con grava")
                        return resultado_clasificacion

                    if retenido200>=30 and sfdivgf<1 and SF<15:
                        resultado_clasificacion.append(sigla)
                        resultado_clasificacion.append("Arcilla grasa gravosa")
                        return resultado_clasificacion

                    if retenido200>=30 and sfdivgf<1 and SF>=15:
                        resultado_clasificacion.append(sigla)
                        resultado_clasificacion.append("Arcilla grasa gravosa con arena")
                        return resultado_clasificacion


#------------------------------------------------------------------------------------------------------------------------

    




#************************************************ LIMITES DE CONSISTENCIA ASTM *****************************************
    def Calculo_Limite_plastico(self,total1):
        resultados = []
        masa_agua = []
        masa_suelo_seco = []
        w = 0
        total = 0
        b = 0
        f = 0
        for i in range(len(total1)):
            w = ((float(total1[i][1]) - float(total1[i][2])) / (float(total1[i][2]) - float(total1[i][0]))) * 100
            masa_agua.append(round((float(total1[i][1]) - float(total1[i][2])), 2))
            masa_suelo_seco.append(round((float(total1[i][2]) - float(total1[i][0])), 2))
            total = total + w
            if i == 0:
                b = w
            if i == len(total1) - 1:
                f = w

            if round(w,2)<0:
                mensaje = "Contenido de humedad negativa del ensayo limite plastico error en la Muestra Nro :" + " " + str(i + 1)
                return ["error", mensaje]
            else:
                resultados.append(round(w, 2))

        tot = total / len(total1)
        return [resultados, masa_agua, masa_suelo_seco, round(sum(resultados) / len(total1), 2)]



    def Calculo_limite_liquido(self,muestras,limite_plastico,id,usuario,cedula,tiipo_ensayo):
        masa_agua = []
        masa_suelo_seco = []
        w = 0
        total = 0
        b = 0
        f = 0
        x = 0
        vec = []
        cal_humedad = []
        reacomodar = []
        terminado = [0, 0, 0]
        for i in range(len(muestras)):
            if (float(muestras[i][3]) - float(muestras[i][0]))==0:
                return [1,"division entre 0"]
            else:

                w = ((float(muestras[i][2]) - float(muestras[i][3])) / (float(muestras[i][3]) - float(muestras[i][0]))) * 100
                masa_agua.append(round((float(muestras[i][2]) - float(muestras[i][3])), 2))
                masa_suelo_seco.append(round((float(muestras[i][3]) - float(muestras[i][0])), 2))
            total = total + w
            if i == 0:
                b = w
            if i == len(muestras) - 1:
                f = w
            # calculo de golpes
            if tiipo_ensayo == 'll_astm':
                if float(muestras[i][1]) < 15 or float(muestras[i][1]) > 36:
                    return [1,"Valores fuera de rangos Valor de Golpes"]
                else:
                    vec.append(float(muestras[i][1]))
            else:
                vec.append(float(muestras[i][1]))

            if float(round(w, 2))<0:
                mensaje="Contenido de humedad negativa del ensayo limite liquido error en la Muestra Nro :"+" "+str(i+1)
                return [1, mensaje]
            else:
                cal_humedad.append(float(round(w, 2)))

        tot = total / len(muestras)
        a = (100 * abs(b - f)) / tot

        vec.sort()
        if tiipo_ensayo=='ll_astm':
            if len(vec) < 3:
                return [1,"Error de ensayo"]
            else:
                if float(vec[0]) > 14 and float(vec[0]) < 26 and float(vec[0]):
                    terminado[0] = float(vec[0])
                if float(vec[1]) > 19 and float(vec[1]) < 31 and float(vec[1]):
                    terminado[1] = float(vec[1])
                if float(vec[2]) > 24 and float(vec[2]) < 36 and float(vec[2]):
                    terminado[2] = float(vec[2])
                if 0 in terminado:
                    return [1,"Error de ensayo,Valor de Golpes"]
                else:
                    for i in range(len(muestras)):
                        if cal_humedad[i] == max(cal_humedad):
                            reacomodar.append(vec[0])
                        if cal_humedad[i] == min(cal_humedad):
                            reacomodar.append(vec[len(muestras) - 1])
                        if cal_humedad[i] != max(cal_humedad) and cal_humedad[i] != min(cal_humedad):
                            reacomodar.append(vec[1])
        else:
            reacomodar=vec

        a = [[cal_humedad, reacomodar, masa_agua, masa_suelo_seco, self.regresion(reacomodar, cal_humedad,id,usuario,cedula,tiipo_ensayo)],
             self.Calculo_Limite_plastico(limite_plastico)]
        if a[1][0]=="error":
            return [1,a[1][1]]
        else:
            a.append(round(a[0][4][0][0] - a[1][3], 2))
            return a


#*--------------------------------------------------- GRAFICO LIMITES DE CONSISTENCIA ASTM ------------------------------
    def regresion(self, numero_de_golpes, porcentaje_de_humedad,id,usuario,cedula,tipo_ll):

        entrenamiento = numpy.array([numero_de_golpes, porcentaje_de_humedad]).transpose()
        self.y = entrenamiento[:, 1]
        m, n = entrenamiento.shape
        aux = numpy.ones((self.y.shape[0], n))
        aux[:, 1] = entrenamiento[:, 0]
        self.X = aux
        self.Theta = numpy.zeros(2)
        self.ecNormal()
        return self.graficarConjunto(id,usuario,cedula,tipo_ll)

    def ecNormal(self):
        self.Theta = self.Theta.reshape(2, 1)
        self.Theta = numpy.linalg.pinv(self.X.transpose().dot(self.X)).dot(self.X.transpose().dot(self.y))

    def graficarConjunto(self,id,usuario,cedula,tipo_ll):
        if True:
            fig3 = grafico.figure()
            grafico.scatter(self.X[:, 1], self.y, color="b")
            grafico.plot(self.X[:, 1], self.X.dot(self.Theta.transpose()))
            # *********************************************************************************************************
            y = self.ecualinearecta(self.X[:, 1], self.X.dot(self.Theta.transpose()))
            # *********************************************************************************************************
            grafico.scatter(25, y[0], color="orange")
            grafico.plot(25, y[0], color="orange")


        grafico.ylabel("CONTENIDO DE HUMEDAD (%)")
        grafico.xlabel("Nro DE GOLPES")

        if tipo_ll=='corte_directo':
            grafico.ylabel("ESFUERZO DE CORTE Kpa")
            grafico.xlabel("ESFUERZO NORMAL Kpa")

        grafico.grid(True)
        png = '.png'
        if tipo_ll=='corte_directo':
            fig3.savefig('static/img/corte directo astm/' + "corte_directoF3" + str(id))
            return ['img/corte directo astm/' + "corte_directoF3" + str(id) + png,y]
        if tipo_ll=='ll_astm':
            fig3.savefig("static/img/limites C astm/"+ "limite_liquido" + str(id) + str(usuario) + str(cedula))
            return [y,'img/limites C astm/'+ "limite_liquido" + str(id) + str(usuario) + str(cedula) + png]
        else:
            fig3.savefig("static/img/limites C aashto/" + "limite_liquido_aashto" + str(id) + str(usuario) + str(cedula))
            return [y, 'img/limites C aashto/' + "limite_liquido_aashto" + str(id) + str(usuario) + str(cedula) + png]
    def ecualinearecta(self, x, y):
        n = len(x)
        sumx = sum(x)
        sumy = sum(y)
        sumxy = sum(x * y)
        sumx = sum(x)
        sumx2 = sum(x * x)
        promx = sumx / n
        promy = sumy / n
        m = (sumx * sumy - n * sumxy) / (sumx ** 2 - n * sumx2)
        b = promy - m * promx
        self.Y1 = m * 25 + b
        return [round(self.Y1,2),str(round(m, 4)) +" "+ "X"+" " + "+"+" " + str(round(b, 3))]
#-----------------------------------------------------------------------------------------------------------------------





#************************************** PROCTOR MODIFICADO ASTM *******************************************************

    def proctor_modificado_astm(self,datos,peso_molde_suelo,peso_molde,humedad,id,usuario,ci,estado,ensayo_proc):
        peso_humedo_suelo = []
        peso_unitario_humedo = []
        peso_molde_mas_suelo = []
        peso_unitario_seco = []
        gravedad = datos[1]
        if float(datos[4]) == 0:
            volumen = round((round(((pi * (float(datos[2]) ** 2) * float(datos[3])) / 4), 2)) / 10 ** 3, 2)
        else:
            volumen = datos[4]

        ########PESO UNITARIO

        for i in range(len(peso_molde_suelo)):
            peso_molde_mas_suelo.append(float(peso_molde_suelo[i]))
            dato_peso_humedo = float(peso_molde_suelo[i]) - float(peso_molde[i])
            if float(volumen)==0:
                return [1,"division entre cero introdusca volumen mayor a 0"]
            dato_peso_unitario = (dato_peso_humedo * float(gravedad)) / float(volumen)

            peso_humedo_suelo.append(round(dato_peso_humedo, 2))
            peso_unitario_humedo.append(round(dato_peso_unitario, 2))

            # CONDICION

        if peso_molde_mas_suelo[0] == max(peso_molde_mas_suelo):
            return [1,"No se cumple la condicion de curvatura"]

        if peso_molde_mas_suelo[-1] == max(peso_molde_mas_suelo):
            return [1,"No se cumple la condicion de curvatura"]
        else:

            ########CONTENIDO HUMEDAD
            resultado = self.calculo_contenido_humedad(humedad, estado)
            if resultado[0]==1:
                return [1,resultado[1]]
            par = []
            inpar = []
            for i in range(len(humedad)):
                if i % 2 == 0:
                    par.append(i)
                else:
                    if i % 2 != 0:
                        inpar.append(i)
            humeda_promedio = []
            for x in range(len(peso_molde_suelo)):
                ph = round((resultado[0][par[x]] + resultado[0][inpar[x]]) / 2, 2)
                humeda_promedio.append(ph)
                dato_y = peso_unitario_humedo[x] / (1 + (ph / 100))
                peso_unitario_seco.append(round(dato_y, 2))


            return [peso_humedo_suelo, peso_unitario_humedo, resultado, humeda_promedio, peso_unitario_seco,
                    self.graficar_proctor(humeda_promedio, peso_unitario_seco, id, usuario, ci,ensayo_proc),volumen]




    def graficar_proctor(self,x,y,id,usuario,ci,esayo_proctor):
        z = numpy.polyfit(x, y, 3)
        f = numpy.poly1d(z)

        x_new = numpy.linspace(x[0], x[-1], 50)
        y_new = f(x_new)

        for i in range(len(y_new)):
            if max(y_new) == y_new[i]:
                ym = round(y_new[i], 2)
                xm = round(x_new[i], 2)

        fig4 = grafico.figure()
        grafico.plot(x, y, 'o', x_new, y_new)
        grafico.scatter(xm, ym, c='r')
        grafico.ylabel("DENSIDAD SECO (gr)")
        grafico.xlabel("CONTENIDO DE HUMEDAD (%)")
        grafico.grid(True)
        png = '.png'
        if esayo_proctor =='proctor_astm':
            fig4.savefig('static/img/proctor modificado astm/' + "proctor_mod_astm" + str(id) + str(usuario))
            save_grafico = 'img/proctor modificado astm/' + "proctor_mod_astm" + str(id) + str(usuario) + png
        else:
            if esayo_proctor=='proctor_aashto':
                fig4.savefig('static/img/proctor modificado aashto/' + "proctor_mod_aashto" + str(id) + str(usuario))
                save_grafico = 'img/proctor modificado aashto/' + "proctor_mod_aashto" + str(id) + str(usuario) + png
            else:
                if esayo_proctor == 'proctor_estandar_aashto':
                    fig4.savefig('static/img/proctor estandar aashto/' + "proctor_estandar_aashto" + str(id) + str(usuario))
                    save_grafico = 'img/proctor estandar aashto/' + "proctor_estandar_aashto" + str(id) + str(usuario) + png

        return [ym, xm, save_grafico]


    def granulometria_aashto(self,datos,tam,ret,peso_retmain,LL,id,usuario,ci):

        datos_resultados=[]
        peso_agua_PA=float(datos[0])-float(datos[1])
        datos_resultados.append(round(peso_agua_PA,2))
        peso_suelo_PS=float(datos[1])-float(datos[2])
        datos_resultados.append(round(peso_suelo_PS,2))
        porcentajehumedad=round(((float(datos[0])-float(datos[1]))*100)/(float(datos[1])-float(datos[2])),2)
        datos_resultados.append(round(porcentajehumedad,2))


        tamiz = []
        tamanomm = []
        pesoretenido = []
        retenidoacumuladoGrs=[]
        porcentajetot=[]
        porcentajequepasa=[]
        suma=0


        for i in range(len(tam)):
            t=tam[i]
            t1=Fraction(t)
            if t1==4:
                tm=4.75
            if t1!=4:
                tm=round(25.44*t1,2)
            tamiz.append(t)
            if i==0:
                tamanomm.append(0)
            else:
                tamanomm.append(tm)




        for i in ret:
            pesoretenido.append(float(i))
        agregadogrueso =sum(pesoretenido)
        datos_resultados.append(round(agregadogrueso,2))
        pasa_Nro4_Mh=float(datos[3]) - agregadogrueso
        datos_resultados.append(round(pasa_Nro4_Mh,2))
        pasaNro4seco = round(((float(datos[3]) - agregadogrueso) * 100) / (100 + porcentajehumedad), 2)
        datos_resultados.append(round(pasaNro4seco,2))
        muestratotalseca =round ((agregadogrueso + pasaNro4seco),2)
        datos_resultados.append(round(muestratotalseca,2))


        for i in range(len(tam)):
            suma = suma + pesoretenido[i]
            retenidoacumuladoGrs.append(suma)
            porcen =(retenidoacumuladoGrs[i] * 100) / float(muestratotalseca)
            porcentajetot.append(round(porcen,2))
            loquepasa = 100 - porcentajetot[i]
            porcentajequepasa.append(round(loquepasa,2))


        tamiz2=['10','40','200']
        tamanoenmm2=[2,0.425,0.075]
        retenido2=peso_retmain
        retenidoGR2=[]
        retenidoacumuladoporcentaje2=[]
        porcentajemortero=[]
        porcentajequepasatotal2=[]
        quepasa1=deepcopy(porcentajequepasa)
        a=quepasa1.pop(-1)
        suma2=0
        contador2=0


        pasaNro10seco=round((float(datos[4])*100)/(100+porcentajehumedad),2)
        datos_resultados.append(round(pasaNro10seco,2))


        for i in range(3):
            suma2 = suma2 + float(retenido2[i])
            retenidoGR2.append(round(suma2,2))
            porcentaje = round((retenidoGR2[i] * 100) / float(pasaNro10seco), 2)
            retenidoacumuladoporcentaje2.append(porcentaje)
            mortero=100-retenidoacumuladoporcentaje2[i]
            porcentajemortero.append(round(mortero,2))
            totalloquepasa=((porcentajemortero[i]*a)/100)
            porcentajequepasatotal2.append(round(totalloquepasa,2))


        porcentajetot_2_copia=deepcopy(porcentajetot)
        tamanomm_2_copia=deepcopy(tamanomm)
        tamiz2_2_copia=deepcopy(tamiz2)
        porcentajequepasa_2_copia=deepcopy(porcentajequepasa)
        for i in range(3):
            xp = tamanoenmm2[i]
            tamanomm_2_copia.append(xp)
            yp = porcentajequepasatotal2[i]
            porcentajequepasa_2_copia.append(yp)
            tZ=tamiz2_2_copia.pop(0)
            tamiz.append(tZ)
            por=retenidoacumuladoporcentaje2[i]
            porcentajetot_2_copia.append(por)


        bandera=0
        vector_original = porcentajequepasa_2_copia
        diametros = tamanomm_2_copia
        vector_auxiliar_polar = deepcopy(vector_original)
        vector_auxiliar_polar.append(60)
        vector_auxiliar_polar.append(30)
        vector_auxiliar_polar.append(10)
        vector_auxiliar_polar.sort(reverse=True)


        for i in range(len(vector_auxiliar_polar)):
            if vector_auxiliar_polar[i] == 60:

                for a in range(len(vector_original)):
                    if vector_original[a] == vector_auxiliar_polar[i - 1]:

                        D60 =round( self.polarizacion(vector_auxiliar_polar[i - 1],vector_auxiliar_polar[i + 1],diametros[a],diametros[a + 1], 60),2)
            if vector_auxiliar_polar[i] == 30:
                for a in range(len(vector_original)):
                    if vector_original[a] == vector_auxiliar_polar[i - 1]:

                        if a==len(diametros)-1:
                            D30=0
                        else:
                            D30 =round(self.polarizacion(vector_auxiliar_polar[i - 1], vector_auxiliar_polar[i + 1],diametros[a],diametros[a + 1], 30),2)
            if vector_auxiliar_polar[i] == 10:

                # if vector_auxiliar_polar[i + 1] == 0:
                if i == len(vector_auxiliar_polar)-1:
                        bandera = 1
                        D10=0
                else:
                    for a in range(len(vector_original)):
                        if vector_original[a] == vector_auxiliar_polar[i - 1]:
                            D10 = round(self.polarizacion(vector_auxiliar_polar[i - 1],vector_auxiliar_polar[i + 1],diametros[a],diametros[a + 1], 10),2)

        for i in range(len(tamiz)):
            if tamiz[i] == '4':
                grava = porcentajetot_2_copia[i]
            if tamiz[i] == '200':
                finos = porcentajequepasa_2_copia[i]

        Grava =round(grava, 2)
        Arena =round(100 - finos - grava, 2)
        Finos =round(finos, 2)
        if bandera == 0:
            Cc =round ((D30 ** 2 / (D10 * D60)),2)
            Cu = round((D60 / D10),2)
        else:
            Cc=0
            Cu=0

        if LL[0]!='seleccionar':
            clasificacion= self.clasificacionAASHTO(porcentajequepasatotal2[0],porcentajequepasatotal2[1],porcentajequepasatotal2[2],float(LL[0]),float(LL[1]))
        else:
            clasificacion='ninguno'
        datos_graficos=self.graficagranulometriaAASHTO(tamanomm_2_copia,porcentajequepasa_2_copia,id,usuario,ci)
        return [datos_resultados,[D60,D30,D10],[Cc,Cu],[Grava,Arena,Finos],[retenidoacumuladoGrs,porcentajetot,tamanomm,porcentajequepasa],[retenidoGR2,retenidoacumuladoporcentaje2,porcentajemortero,tamanoenmm2,porcentajequepasatotal2,tamiz2],clasificacion,datos_graficos]



    def graficagranulometriaAASHTO(self,x1,y1,id,usuario,ci):
        x1.pop(0)
        y1.pop(0)
        fig5 = grafico.figure()
        grafico.scatter(x1, y1, marker='o', color='b')
        grafico.plot(x1, y1, marker='o', color='b')
        grafico.gca().invert_xaxis()
        grafico.grid(True)
        grafico.xscale('log')
        grafico.ylabel("% QUE PASA")
        grafico.xlabel("DIAMETRO DE PARTICULAS mm")
        png = '.png'
        fig5.savefig('static/img/granulometria aashto/' + "granulometria_aashto" + str(id) + str(ci))
        return 'img/granulometria aashto/' + "granulometria_aashto" +str (id) +str(ci)+png


#********************************CLASIFICACION DE SUELOS AASHTO* INICIO *****************************************


    def clasificacionAASHTO(self,pasanumero10,pasanumero40,pasanumero200,limiteliquido,indiceplasticidad):
        if pasanumero200<=35:

            if pasanumero10 <= 50 and pasanumero40 <= 30 and pasanumero200 <= 15 and indiceplasticidad<=7:
                ig=(pasanumero200-35)*(0.2+0.005*(limiteliquido-40))+0.01*(pasanumero200-15)*(indiceplasticidad-10)
                if ig < 0:
                    ig=0
                return "A-1-a"+"("+str(int(round(ig,0)))+")"
            else:

                if pasanumero40<=50 and pasanumero200<=25:
                    if indiceplasticidad=="NP":
                        indiceplasticidad=0
                    ig = (pasanumero200 - 35) * (0.2 + 0.005 * (limiteliquido - 40)) + 0.01 * (pasanumero200 - 15) * (
                    indiceplasticidad - 10)
                    if ig < 0:
                        ig=0
                    return "A-1-b"+ "("+str(int(round(ig,0)))+ ")"
                else:

                    if pasanumero40>=51 and pasanumero200<=10 and indiceplasticidad=="NP":
                        indiceplasticidad=0
                        ig = (pasanumero200 - 35) * (0.2 + 0.005 * (limiteliquido - 40)) + 0.01 * (pasanumero200 - 15) * (
                        indiceplasticidad - 10)
                        if ig < 0:
                            ig=0
                        return "A-3"+ "("+ str(int(round(ig,0)))+ ")"
                    else:

                        if pasanumero200<=35 and limiteliquido<=40 and indiceplasticidad<=10 and indiceplasticidad>0 and limiteliquido>0:
                            ig = (pasanumero200 - 35) * (0.2 + 0.005 * (limiteliquido - 40)) + 0.01 * (pasanumero200 - 15) * (
                                indiceplasticidad - 10)
                            if ig < 0:
                                ig=0
                            return "A-2-4"+ "("+ str(int(round(ig,0)))+ ")"
                        else:

                            if pasanumero200<=35 and limiteliquido>=41 and indiceplasticidad <=10 and indiceplasticidad>0:
                                ig = (pasanumero200 - 35) * (0.2 + 0.005 * (limiteliquido - 40)) + 0.01 * (pasanumero200 - 15) * (
                                    indiceplasticidad - 10)
                                if ig < 0:
                                    ig=0
                                return "A-2-5"+ "("+ str(int(round(ig,0)))+ ")"
                            else:

                                if pasanumero200<=35 and limiteliquido<=40 and indiceplasticidad>=11 and limiteliquido>0:
                                    ig = 0.01*(pasanumero200-15)*(indiceplasticidad-10)
                                    if ig < 0:
                                        ig=0
                                    return "A-2-6"+ "("+ str(int(round(ig,0)))+ ")"
                                else:

                                    if pasanumero200<=35 and limiteliquido>=41 and indiceplasticidad>=11:

                                        ig = 0.01 * (pasanumero200 - 15) * (indiceplasticidad - 10)
                                        if ig < 0:
                                            ig=0
                                        return "A-2-7"+ "("+str(int(round(ig,0)))+ ")"

        else:

            if pasanumero200>35:

                    if pasanumero200>=36 and limiteliquido<=40 and indiceplasticidad<=10 and limiteliquido>0 and indiceplasticidad>0:
                        ig = (pasanumero200 - 35) * (0.2 + 0.005 * (limiteliquido - 40)) + 0.01 * (pasanumero200 - 15) * (
                            indiceplasticidad - 10)
                        if ig < 0:
                            ig=0
                        return "A-4"+ "("+ str(int(round(ig,0)))+ ")"
                    else:

                        if pasanumero200>=36 and limiteliquido>=41 and indiceplasticidad<=10 and indiceplasticidad>0:
                            ig = (pasanumero200 - 35) * (0.2 + 0.005 * (limiteliquido - 40)) + 0.01 * (pasanumero200 - 15) * (
                                indiceplasticidad - 10)
                            if ig < 0:
                                ig=0
                            return "A-5"+ "("+ str(int(round(ig,0)))+ ")"
                        else:


                            if pasanumero200>=36 and limiteliquido<=40 and indiceplasticidad>=11 and limiteliquido>0:
                                ig = (pasanumero200 - 35) * (0.2 + 0.005 * (limiteliquido - 40)) + 0.01 * (pasanumero200 - 15) * (
                                    indiceplasticidad - 10)
                                if ig < 0:
                                    ig=0
                                return "A-6"+ "("+ str(int(round(ig,0)))+ ")"
                            else:


                                if pasanumero200>=36 and limiteliquido>=41 and indiceplasticidad>=11:
                                    ig = (pasanumero200 - 35) * (0.2 + 0.005 * (limiteliquido - 40)) + 0.01 * (pasanumero200 - 15) * (
                                        indiceplasticidad - 10)
                                    if ig < 0:
                                        ig=0
                                    return "A-7"+ "("+ str(int(round(ig,0)))+ ")"
                                else:

                                    if pasanumero200>=36 and limiteliquido>=41 and indiceplasticidad>=11 and indiceplasticidad<=limiteliquido-30 and indiceplasticidad>0:
                                        ig = (pasanumero200 - 35) * (0.2 + 0.005 * (limiteliquido - 40)) + 0.01 * (pasanumero200 - 15) * (
                                            indiceplasticidad - 10)
                                        if ig < 0:
                                            ig=0
                                        return "A-7-5a"+ "("+ str(int(round(ig,0)))+ ")"

                                    else:

                                        if pasanumero200>=36 and limiteliquido>=41 and indiceplasticidad>=11 and indiceplasticidad>limiteliquido-30:
                                            ig = (pasanumero200 - 35) * (0.2 + 0.005 * (limiteliquido - 40)) + 0.01 * (pasanumero200 - 15) * (
                                                indiceplasticidad - 10)
                                            if ig < 0:
                                                ig=0
                                            return "A-7-6b"+ "("+ str(int(round(ig,0)))+ ")"
                                        else:
                                            return "NO existe clasificacion"


#********************************CLASIFICACION DE SUELOS AASHTO* FIN *****************************************





#***************************** LIMITE DE CONTRACCION *******************************************************************
    def calculo_limite_de_contraccion(self,datos,H2O):

        volumen_inicial_del_recipiente=round(float(datos[1])/float(datos[0]),2)
        temperatura_del_agua=self.Densidad_H2O(float(datos[6]),H2O)
        Masa_de_la_muestra_humeda=round(float(datos[3])-float(datos[2]),2)
        Masa_de_la_muestra_seca=round(float(datos[4])-float(datos[2]),2)
        volumen_de_mercurio_desplazado=round((float(datos[5])/float(datos[0])),2)
        contenido_humedad_inicial=round(((Masa_de_la_muestra_humeda-Masa_de_la_muestra_seca)/Masa_de_la_muestra_seca)*100,2)
        cambio_en_el_contenido_de_humedad=round((((volumen_inicial_del_recipiente-volumen_de_mercurio_desplazado)/Masa_de_la_muestra_seca)*100)*temperatura_del_agua,2)
        limite_de_contraccion=round(contenido_humedad_inicial-cambio_en_el_contenido_de_humedad,2)
        indice_de_contraccion=round((Masa_de_la_muestra_seca/(volumen_de_mercurio_desplazado*temperatura_del_agua)),2)
        return [volumen_inicial_del_recipiente,Masa_de_la_muestra_humeda,Masa_de_la_muestra_seca,volumen_de_mercurio_desplazado,contenido_humedad_inicial,cambio_en_el_contenido_de_humedad,limite_de_contraccion,indice_de_contraccion]

    def Densidad_H2O(self,t,densidad_H2O):
        temperatura = []
        densidadagua = 0
        for i in range(len(densidad_H2O)):
            temperatura.append(i)
            if i == t:
                densidadagua = float(densidad_H2O[i])
                return densidadagua

            if i == 100 and densidadagua == 0 and t <= 100:
                temperatura.append(t)
                temperatura.sort()
                for x in range(len(temperatura)):
                    if temperatura[x] == t:
                        return self.polarizacion(temperatura[x - 1], temperatura[x + 1],densidad_H2O[temperatura[x - 1]],densidad_H2O[temperatura[x + 1]], t)

                break
#-----------------------------------------------------------------------------------------------------------------------




# **************************************** CONO DE ARENA ASTM **********************************************************

    def calculo_cono_de_arena(self,datos):
        contenido_humedad=[]
        resultados=[]
        for i in range(len(datos[0])):
            if float(datos[3]) == 1:
                if datos[4][2]==0:
                    return [1,'error division entre cero']
                else:
                    densidad = (float(datos[4][1]) - float(datos[4][0])) / float(datos[4][2])
                    if densidad ==0:
                        return [1, 'error division entre cero']

            else:
                if float(datos[3]) == 2:
                    densidad = datos[1][i][0]

            volumen_en_el_cono = datos[1][i][1]
            densidad_maxima_proctor = datos[2]

            w =round(((float(datos[0][i][2]) - float(datos[0][i][3])) / (float(datos[0][i][3]) - float(datos[0][i][1]))) * 100,2)
            contenido_humedad.append(w)
            grado_de_compactacion_de_especificacion = datos[1][i][3]
            peso_del_frasco_mas_arena_antes=datos[1][i][4]
            peso_del_frasco_mas_arena_despues = datos[1][i][5]
            peso_de_la_arena_hoyo_mas_cono=round(float(peso_del_frasco_mas_arena_antes)-float(peso_del_frasco_mas_arena_despues),2)#valor de arena que queda
            volumen_de_cono_y_hoyo=round((float(peso_de_la_arena_hoyo_mas_cono)/float(densidad)),2)
            volumen_del_hoyo=round(float(volumen_de_cono_y_hoyo)-float(volumen_en_el_cono),2)
            peso_de_la_muestra_humeda_del_hoyo=datos[1][i][6]
            densidad_seca=round(float(peso_de_la_muestra_humeda_del_hoyo)/float(volumen_del_hoyo),2)
            densidad_aparente=round(densidad_seca/(1+(w/100)),2)
            grado_de_compactacion=round((densidad_aparente*100)/float(densidad_maxima_proctor),2)
            if grado_de_compactacion>=float(grado_de_compactacion_de_especificacion):
                estado= "aceptado"
            else:
                estado= "rechazado"
            resultados.append([peso_de_la_arena_hoyo_mas_cono,volumen_de_cono_y_hoyo,volumen_del_hoyo,densidad_aparente,densidad_maxima_proctor,grado_de_compactacion,grado_de_compactacion_de_especificacion,estado])
        return [contenido_humedad,resultados]

#-----------------------------------------------------------------------------------------------------------------------







#*****************************************   ENSAYO CBR ****************************************************************

    def calculo_ensayo_CBR(self,compactacion,humedad,expansion,lectura_dial,abaco_cbr,usuario,ci,id,tip_ensayo):
        resutado_total_cbr=[]
        for i in range(len(compactacion)):
            for j in range(2):

                if j ==0:
                    antes=[]
                    pesoMoldegr=float(compactacion[i][j][1])
                    pesoHumedoMuestra = round(float(compactacion[i][j][0]) - float(compactacion[i][j][1]), 3)
                    antes.append(pesoHumedoMuestra)
                    calculoVolumen=2
                    if calculoVolumen==1:
                        self.calculo_volumen(101.65,116.4)
                    else:
                        volumenMuestra = float(compactacion[i][j][2])

                        dencidad1=round(pesoHumedoMuestra/volumenMuestra,3)
                        self.dencidad.append(dencidad1)
                        antes.append(dencidad1)
                        h=self.calculo_contenido_humedad_CBR(humedad[i][j],"cbr")
                        if h[0]==1:
                            return [1,' error de calculo antes de enbebimineto'+' '+'fila Nro :'+str(j+1)+' '+h[1]]
                        densidad_seca_proveta=round((dencidad1 / (1 + (h[0][0] / 100))),3)
                        antes.append(densidad_seca_proveta)
                        antes.append(h)

                if j==1:
                    despues=[]
                    pesoHumedoMuestra2 =round(float(compactacion[i][j][0]) - pesoMoldegr,3)
                    despues.append(pesoHumedoMuestra2)
                    dencidad2=round(pesoHumedoMuestra2/volumenMuestra,3)
                    despues.append(dencidad2)
                    h = self.calculo_contenido_humedad_CBR(humedad[i][j], "cbr")
                    if h[0]==1:
                        return [1,' error de calculo despues de enbebimineto'+' '+'fila Nro :'+str(j+1)+' '+h[1]]
                    densidad_seca_proveta_despues= round((dencidad2 / (1 + (h[0][0] / 100))), 3)
                    despues.append(densidad_seca_proveta_despues)
                    despues.append(h)
                    despues.append(volumenMuestra)
            resutado_total_cbr.append(antes)
            resutado_total_cbr.append(despues)
        return [resutado_total_cbr,self.expansion(expansion),self.esfuerzo(lectura_dial,abaco_cbr,usuario,ci,id,tip_ensayo)]

    def expansion(self,exp):
        resultado_total_expansion=[]
        datos_dia = []
        contador_datos = 4
        datos_expansion = []
        for i in range(len(exp)):
            for j in range(len(exp[i])):
                datos_dia.append(exp[i][j])
            for x in range(5):
                expansion = round(((float(datos_dia[contador_datos]) - float(exp[i][0])) / 116.4) * 100,2)
                datos_expansion.append(expansion)
                contador_datos = contador_datos - 1
                incremento_altura = []
                porcentaje_expansion = []
                muestras=[]
            for y in range(5):


                incremento_altura.append(float(exp[i][y])/100)
                porcentaje_expansion.append(round(datos_expansion.pop(), 2))

            muestras.append(incremento_altura)
            muestras.append(porcentaje_expansion)
            resultado_total_expansion.append(muestras)
        return resultado_total_expansion



    def calculo_volumen(self,diametro,altura):
        volumen = round((round(((pi * (float(diametro) ** 2) * float(altura)) / 4), 2)) / 10 ** 3, 2)
        return volumen


    def esfuerzo(self,lectura_dial,abaco_cbr,usuario,ci,id,tip_ensayo):
        abaco_cbrdato=[]
        resultado_final=[]
        datos_abaco_total=[]
        area = (pi * (49.6** 2)) / 4
        area_convertida = (area / 10 ** 2) / 100 ** 2
        if len(lectura_dial[2])<=9:
            penetracion =[0,0.5,1.0,1.5,2.0,2.5,3.0,3.5,4.0]
            pulgadas=[0,0.025,0.050,0.075,0.100,0.125,0.150,0.175,0.200]
            centimetros=[0,0.63,1.27,1.90,2.54,3.18,3.81,4.45,5.08]
        else:
            penetracion = [0,0.65,1.25,1.90,2.5,3,3.5,4.40,5.0,7.5,10,12.5]  # x
            pulgadas = [0, 0.025, 0.050, 0.075, 0.100, 0.125, 0.150, 0.175, 0.200,0,0,0]
            centimetros = [0, 0.63, 1.27, 1.90, 2.54, 3.18, 3.81, 4.45, 5.08,0,0,0]
        vector_presion = []
        for i in range(len(lectura_dial)):
            presion_por_muestra=[]
            dato_abaco=[]
            for j in range(len(lectura_dial[0])):
                datos_labo = int(lectura_dial[i][j])
                dato_abaco.append(round(abaco_cbr[datos_labo], 4))
                presion =round( dato_abaco[j] / area_convertida,2)
                presion_por_muestra.append(presion)
            vector_presion.append(presion_por_muestra)
            datos_abaco_total.append(dato_abaco)


        resultado_final.append(datos_abaco_total)
        resultado_final.append(vector_presion)
        resultado_final.append(self.grafica_cbr(penetracion,vector_presion[0],vector_presion[1],vector_presion[2],usuario,ci,id,tip_ensayo))
        resultado_final.append(penetracion)
        resultado_final.append(pulgadas)
        resultado_final.append(centimetros)
        return resultado_final

    def grafica_cbr(self,x,y,y2,y3,usuario,ci,id,tip_ensayo):
        ecuaciones_cbr=[]

        z = numpy.polyfit(x, y, 3)
        f = numpy.poly1d(z)
        z2 = numpy.polyfit(x, y2, 3)
        f2 = numpy.poly1d(z2)
        z3 = numpy.polyfit(x, y3, 3)
        f3 = numpy.poly1d(z3)

        # calculate new x's and y's
        x_new = numpy.linspace(x[0], x[-1], 50)
        y_new = f(x_new)
        y_new2 = f2(x_new)
        y_new3 = f3(x_new)
        A = f(2.54)
        B = f2(2.54)
        C = f3(2.54)
        grafica1=[A,B,C]
        A1 = f(5.08)
        B1 = f2(5.08)
        C1 = f3(5.08)
        grafica2= [A1, B1, C1]
        fig6 = grafico.figure()
        grafico.plot(x, y, 'o', x_new, y_new)
        grafico.plot(x, y2, 'o', x_new, y_new2)
        grafico.plot(x, y3, 'o', x_new, y_new3)
        grafico.grid(True)
        grafico.ylabel("PRESION (Mpa)")
        grafico.xlabel("PENETRACION")
        png = '.png'
        if tip_ensayo =='cbr_astm':
            fig6.savefig('static/img/indice de soporte cbr astm/' + "indice_de_soporte_astm" + str(id) + str(ci))
            fig_cbr1 = 'img/indice de soporte cbr astm/' + "indice_de_soporte_astm" +str (id) +str(ci)+png
        else:
            fig6.savefig('static/img/indice de soporte cbr aashto/' + "indice_de_soporte_aashto" + str(id) + str(ci))
            fig_cbr1 = 'img/indice de soporte cbr aashto/' + "indice_de_soporte_aashto" + str(id) + str(ci) + png



#*********************segundo grafico************************

        m8 = numpy.polyfit(grafica1, self.dencidad,3)
        f8 = numpy.poly1d(m8)
        x_nuevo = numpy.linspace(grafica1[0], grafica1[-1],50)
        y_nuevo = f8(x_nuevo)
        m9 = numpy.polyfit(grafica2, self.dencidad, 3)
        f9 = numpy.poly1d(m9)
        x_nuevo1 = numpy.linspace(grafica2[0], grafica2[-1],50)
        y_nuevo1 = f9(x_nuevo1)
        fig7 = grafico.figure()
        grafico.plot(grafica1,self.dencidad,'o',x_nuevo,y_nuevo)
        grafico.plot(grafica2, self.dencidad,'o', x_nuevo1,y_nuevo1)
        grafico.grid(True)
        grafico.xlabel("% CBR")

        ecuaciones_cbr.append(str(f))
        ecuaciones_cbr.append(str(f2))
        ecuaciones_cbr.append(str(f3))
        png = '.png'
        if tip_ensayo =='cbr_astm':
            fig7.savefig('static/img/indice de soporte cbr astm/' + "indice_de_soporte_fig2_astm" + str(id) + str(ci))
            fig_cbr2 = 'img/indice de soporte cbr astm/' + "indice_de_soporte_fig2_astm" +str (id) +str(ci)+png
        else:
            fig7.savefig('static/img/indice de soporte cbr aashto/' + "indice_de_soporte_fig2_aashto" + str(id) + str(ci))
            fig_cbr2 = 'img/indice de soporte cbr aashto/' + "indice_de_soporte_fig2_aashto" + str(id) + str(ci) + png

        return [ecuaciones_cbr ,[fig_cbr1,fig_cbr2]]


    def calculo_contenido_humedad_CBR(self,total1,estado):
        resultados = []
        contenido_humedad=[]
        resta1=[]
        resta2=[]
        self.inicio = len(total1)
        w = 0
        total = 0
        b = 0
        f = 0
        for i in range(len(total1)):

            if (float(total1[i][2]) - float(total1[i][0]))==0:
                return [1, "error divicion entre cero (0)" + str(i + 1)]
            else:
                w = ((float(total1[i][1]) - float(total1[i][2])) / (float(total1[i][2]) - float(total1[i][0]))) * 100
                resta1.append(round(float(total1[i][1]) - float(total1[i][2]),2))
                resta2.append(round(float(total1[i][2]) - float(total1[i][0]),2))
                if w<0:
                    return [1,"error del ensayo contenido humedad resultados negativos revisar datos incuerentes en la fila Nro :"+" "+str(i+1)]

            total = total + w
            if i == 0:
                b = w
            if i == self.inicio - 1:
                f = w
            if estado=="humedad":
                resultados.append(round(w, 2))
            if estado=="proctor":
                contenido_humedad.append(round(w, 2))

        tot = total / self.inicio
        a = (100 * abs(b - f)) / tot
        if tot > 100:
            print "por que putas entrooo"
            return [1,"Porecentaje de humedad total "+" " +str(round(tot,2))+"%"+"  "+" "+"El calculo del ensayo sobre pasa los valores de la desviacion establecida  Revisar Contenido de Humedad"]
        else:

            if estado=="proctor":
                resultados.append(contenido_humedad)
                resultados.append(resta1)
                resultados.append(resta2)
                return resultados
            else:
                if estado=="cbr":
                    ch_total = []
                    ch_total.append(round(tot,2))
                    resultados.append(ch_total)
                    resultados.append(resta1)
                    resultados.append(resta2)
                    return resultados

                else:
                    resultados.append(round(tot,2))
                    resultados.append(resta1[0])
                    resultados.append(resta1[1])
                    resultados.append(resta1[2])
                    resultados.append(resta2[0])
                    resultados.append(resta2[1])
                    resultados.append(resta2[2])
                    return resultados
#-----------------------------------------------------------------------------------------------------------------------

#********************************************* CORTE DIRECTO INICIO ***************************************************

    def ensayo_corte_directo(self, datos, dimension_interior, regrecion,id,usuario,cedula):
        dy_total = []
        area_modificada_total = []
        esfuerzo_cortante_total = []
        dimencion_de_la_caja_De_corte = [float(dimension_interior[0]) * float(dimension_interior[1]), (
        float(dimension_interior[0]) * float(dimension_interior[1]) * float(dimension_interior[2]))]

        for i in range(len(datos)):
            dy = []
            area_modificada = []
            esfuerzo_cortante = []
            for j in range(len(datos[i][0])):
                dy_resultado = ((float(datos[i][1][j]) - float(datos[i][1][0])) * 0.001 * 25.4)
                dy.append(round(dy_resultado, 2))
                area_modificada_resultado = round(
                    float(dimension_interior[1]) * ((float(dimension_interior[0]) - dy_resultado / 10)), 2)
                area_modificada.append(area_modificada_resultado)
                esfuerzo_cortante_resultado = round((float(datos[i][2][j]) / (area_modificada_resultado / 10000)), 2)
                esfuerzo_cortante.append(esfuerzo_cortante_resultado)
            dy_total.append(dy)
            area_modificada_total.append(area_modificada)
            esfuerzo_cortante_total.append(esfuerzo_cortante)

        a = [[datos[0][0], datos[1][0], datos[2][0]]]
        b = [[esfuerzo_cortante_total[0], esfuerzo_cortante_total[1], esfuerzo_cortante_total[2]],
             [dy_total[0], dy_total[1], dy_total[2]]]
        grafica1=self.grafica_corte_directo(a, b,id,usuario,cedula)
        grafica2=self.regresion(regrecion[0], regrecion[1],id,usuario,cedula,'corte_directo')
        grafica1.append(grafica2[0])
        grafica1.append(grafica2[1])
        return [dy_total,area_modificada_total,esfuerzo_cortante_total,dimencion_de_la_caja_De_corte,grafica1]

    def grafica_corte_directo(self, diametro, porcentaje_que_pasa,id,usuario,ci):

        fig8 = grafico.figure()
        for i in range(3):

            grafico.plot(diametro[0][i], porcentaje_que_pasa[0][i], marker='o')
        grafico.grid(True)
        grafico.ylabel("Esfuerzo de corte")
        grafico.xlabel("Deformacion Horizontal (mm)")
        png = '.png'
        fig8.savefig('static/img/corte directo astm/' + "corte_directoF1" + str(id) + str(ci))
        figura8= 'img/corte directo astm/' + "corte_directoF1" + str(id) + str(ci) + png

        fig9 = grafico.figure()
        for i in range(3):

            grafico.plot(diametro[0][i], porcentaje_que_pasa[1][i], marker='o')

        grafico.grid(True)
        grafico.ylabel("Deformacion vertical (mm)")
        grafico.xlabel("Deformacion hprizotal (mm)")
        png = '.png'
        fig9.savefig('static/img/corte directo astm/' + "corte_directoF2" + str(id) + str(ci))
        figura9 = 'img/corte directo astm/' + "corte_directoF2" + str(id) + str(ci) + png
        return [figura8,figura9]
