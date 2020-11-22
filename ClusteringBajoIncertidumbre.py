#encoding:utf-8
import numpy as np
import random
import matplotlib.pyplot as plt
import pandas as pd
import math
import csv
import tkinter
import time
from heapq import nsmallest
from PIL import Image, ImageTk

def findCircle(x1, y1, x2, y2, x3, y3): #FUNCION OBTENIDA DE https://www.geeksforgeeks.org/equation-of-circle-when-three-points-on-the-circle-are-given/
    x12 = x1 - x2;  
    x13 = x1 - x3;  
  
    y12 = y1 - y2;  
    y13 = y1 - y3;  
  
    y31 = y3 - y1;  
    y21 = y2 - y1;  
  
    x31 = x3 - x1;  
    x21 = x2 - x1;  
  
    # x1^2 - x3^2  
    sx13 = pow(x1, 2) - pow(x3, 2);  
  
    # y1^2 - y3^2  
    sy13 = pow(y1, 2) - pow(y3, 2);  
  
    sx21 = pow(x2, 2) - pow(x1, 2);  
    sy21 = pow(y2, 2) - pow(y1, 2);  
  
    f = (((sx13) * (x12) + (sy13) * 
          (x12) + (sx21) * (x13) + 
          (sy21) * (x13)) // (2 * 
          ((y31) * (x12) - (y21) * (x13)))); 
              
    g = (((sx13) * (y12) + (sy13) * (y12) + 
          (sx21) * (y13) + (sy21) * (y13)) // 
          (2 * ((x31) * (y12) - (x21) * (y13))));  
  
    c = (-pow(x1, 2) - pow(y1, 2) - 
         2 * g * x1 - 2 * f * y1);  
  
    # eqn of circle be x^2 + y^2 + 2*g*x + 2*f*y + c = 0  
    # where centre is (h = -g, k = -f) and  
    # radius r as r^2 = h^2 + k^2 - c  
    h = -g;  
    k = -f;  
    sqr_of_r = h * h + k * k - c;  
  
    # r is the radius  
    r = round(math.sqrt(sqr_of_r), 5);  
  
    print("Centro = (", h, ", ", k, ")");  
    print("Radio = ", r);  

    return h, k, r

def nuevasCircunferencias(puntosTotales, puntosPorCluster, gradosPorCluster, n_clusters): #Le daré el conjunto de puntos que pertenecen a esa circunferencia, tras ello usaré los 3 puntos con mejor grado de pertenencia para calcular el nuevo radio, y el centro será la media de todos los puntos
    #Este algoritmo estará basado en findCircle, k-medias, y mi propia lógica
    
    #Por cada Circunferencia, voy a calcular su nuevo radio y centro
    
    x = [] #Lista con las variables X de cada centro
    y = [] #Lista con las variables Y de cada centro
    r = [] #Lista con los radios de cada centro
    
    for i in range(n_clusters): #Recorro cada cluster
        
        puntos = puntosPorCluster[i] #Obtengo los puntos de ese cluster
        grados = gradosPorCluster[i] #Obtengo los grados de ese cluster
        
        #BUSCANDO EL NUEVO CENTRO
        
        sumX = 0 
        sumY = 0
        
        for j in range(0, len(puntos)):
            
            punto = puntos[j]
            
            sumX = punto[0] + sumX
            sumY = punto[1] + sumY
            
            
        nuevoCentroX = sumX/len(puntos)
        nuevoCentroY = sumY/len(puntos)
        
        x.append(nuevoCentroX)
        y.append(nuevoCentroY)
        
        print("El nuevo centro de la circunferencia", i+1, "es: (", x[i], ",", y[i], ")")
        
        #BUSCANDO EL NUEVO RADIO   
            #PROBAR CON TODOS LOS PUNTOS DEL CLUSTER, EN VEZ DE 3 Aleatorios
        p = 3
        
        if len(puntos) < 3:
            p = len(puntos)

        tresPuntos = random.sample(puntos, p) #cojo tres puntos aleatorios, ya que con los tres mejores puntos el algoritmo se quedaba pillado en algunos puntos
        
        distanciaDePuntoACentro = 0
        
        for j in range(0, len(tresPuntos)):
            
            punto = tresPuntos[j]
            
            varX = punto[0]
            varY = punto[1]
            
            distanciaDePuntoACentro = math.sqrt(((x[i] - varX)*(x[i] - varX)) + ((y[i] - varY)*(y[i] - varY))) + distanciaDePuntoACentro
                       
        nuevoRadio = distanciaDePuntoACentro/len(tresPuntos) 
        
        #distanciaDePuntoACentro = 0
        
        #for j in range(0, len(puntos)):  
         
            #punto = puntos[j]
            #varX = punto[0]
            #varY = punto[1]
            
            #distanciaDePuntoACentro = math.sqrt(((x[i] - varX)*(x[i] - varX)) + ((y[i] - varY)*(y[i] - varY))) + distanciaDePuntoACentro
            
        #nuevoRadio = distanciaDePuntoACentro/len(puntos)   
            
        r.append(nuevoRadio)
        
        print("El nuevo radio de la circunferencia", i+1, "es:", r[i])
        
        print("------------------------------------------------------------------------------------")
    
    return x, y, r

def nuevasCircunferenciasV2(puntosPorCluster):
    #Algoritmo basado en uno de internete jejej https://goodcalculators.com/best-fit-circle-least-squares-calculator/
    
    x = [] #Valores de las X de los centros
    y = [] #Valores de las Y de los centros
    r = [] #Valores de los radios 
    
    #Por cada cluster:
    
    #[Σ(xi^2)  Σ(xi*yi) Σxi] * [A] = Σ(xi*(xi^2 + yi^2))
    #[Σ(xi*yi) Σ(yi^2)  Σyi] * [B] = Σ(yi*(xi^2 + yi^2))
    #[Σxi      Σyi       n ] * [C] = Σ(xi^2 + yi^2)
    
    #xCentro = A/2
    #yCentro = B/2
    #r = (raiz(4*C + A^2 + B^2))/2
    
    for i in range(0, len(puntosPorCluster)): #Recorro cada cluster
        
        puntos = puntosPorCluster[i] #Obtengo los puntos de ese cluster
           
        n = len(puntosPorCluster)       #n      
        q = 0                #Σ(xi^2)       
        e = 0                        #Σxi        
        w = 0                #Σ(yi^2)        
        t = 0                        #Σyi
        u = 0                    #Σ(xi*yi)     
        v = 0                  #Σ(xi*(xi^2 + yi^2))    
        p = 0                  #Σ(yi*(yi^2 + yi^2))    
        z = 0                         #Σ(xi^2 + yi^2)
         
        for j in range(0, len(puntos)): #Recorro cada punto del cluster
            
            punto = puntos[j]
            
            varX = punto[0]
            varY = punto[1]
            
            e = e + varX                                              #Σxi
            t = t + varY                                              #Σyi
            q = q + pow(varX, 2)                      #Σ(xi^2)
            w = w + pow(varY, 2)                      #Σ(yi^2)
            u = u + varX*varY                                 #Σ(xi*yi)
            v = v + (varX*(pow(varX, 2) + pow(varY, 2)))  #Σ(xi*(xi^2 + yi^2))
            p = p + (varY*(pow(varX, 2) + pow(varY, 2)))  #Σ(yi*(yi^2 + yi^2))
            z = z + (pow(varX, 2) + pow(varY, 2))                       #Σ(xi^2 + yi^2)
              
        #Resolviendo la matriz
        
        matrizA = np.matrix([[q, u, e],[u, w, t],[e, t, n]])
        matrizB = np.matrix([[v],[p],[z]])
        
        ABC = (matrizA**-1)*matrizB
        
        #A = float(ABC[0])
        #B = float(ABC[1])
        #C = float(ABC[2])
        
        
        sumX = 0 
        sumY = 0
        
        for g in range(0, len(puntos)):
            
            punto = puntos[g]
            
            sumX = punto[0] + sumX
            sumY = punto[1] + sumY
            
            
        nuevoCentroX = sumX/len(puntos)
        nuevoCentroY = sumY/len(puntos)
        
        x.append(nuevoCentroX)
        y.append(nuevoCentroY)
        
        #BUSCANDO EL NUEVO RADIO
        
        #xCentro = A/2
        #yCentro = B/2
        
        A = nuevoCentroX*2
        B = nuevoCentroY*2
        C = nuevoCentroX*nuevoCentroX + nuevoCentroY*nuevoCentroY - nuevoCentroX*A + B*nuevoCentroY
        
        #r = (raiz(4*C + A^2 + B^2))/2
        
        
        
        nuevoRadio = math.sqrt( (4*C + pow(A, 2) + pow(B, 2) ) )/2
        
        r.append(nuevoRadio)
        
        
        
    return x, y, r
    
def nuevasCircunferenciasV3(puntosPorCluster):
    
    x = [] #Valores de las X de los centros
    y = [] #Valores de las Y de los centros
    r = [] #Valores de los radios
    
    for i in range(0, len(puntosPorCluster)): #Recorro cada cluster
        
        puntos = puntosPorCluster[i] #Obtengo los puntos de ese cluster
        
        punto1, punto2 = random.sample(puntos, 2) #Cojo dos puntos aleatorios
        
        x1 = punto1[0]
        y1 = punto1[1]

        x2 = punto2[0]
        y2 = punto2[1]
        
        distanciasP1 = []
        distanciasP2 = []
        
        for j in range(0, len(puntos)):
               
            punto = puntos[j]
            
            varX = punto[0]
            varY = punto[1]
            
            distanciaDePuntoAP1 = math.sqrt(((x1 - varX)*(x1 - varX)) + ((y1 - varY)*(y1 - varY)))
            distanciaDePuntoAP2 = math.sqrt(((x2 - varX)*(x2 - varX)) + ((y2 - varY)*(y2 - varY)))
            
            distanciasP1.append(distanciaDePuntoAP1)
            distanciasP2.append(distanciaDePuntoAP2)
        
        #Busco los mas alejados
        
        indexP3 = distanciasP1.index(max(distanciasP1))
        indexP4 = distanciasP2.index(max(distanciasP2))
            
        punto3 = puntos[indexP3]
        punto4 = puntos[indexP4]
        
        x3 = punto3[0]
        y3 = punto3[1]

        x4 = punto4[0]
        y4 = punto4[1]
        
        #Quiero cojer dos puntos aleatorios, cojer sus puntos mas alejados (en el cluster) y trazar dos rectas entre el punto y su mas alejado
        #Tras esto calculo sus perpendicularer y veo donde se cortan, para escojer el nuevo centro
        
        
        #1-3
        medio13X = (x1+x3)/2
        medio13Y = (y1+y3)/2
        
        pendiente13 = (y3-y1)/(x2-x1)
        
        pendientePerp13 = -1/pendiente13
        
        #recta = y -y1 = m(x -x1) -> y = mX - mx1 + y1
        
        #2-4
        medio24X = (x2+x4)/2
        medio24Y = (y2+y4)/2
        
        pendiente24 = (y4-y2)/(x4-x2)
        
        pendientePerp24 = -1/pendiente24
             
        #punto de corte
        
        numerador =  medio24Y + pendientePerp13*medio13X + medio13Y - pendientePerp24*medio24X
        denominador = pendientePerp13 - pendientePerp24
        
        newX = numerador/denominador
        newY = pendientePerp13*newX - pendientePerp13*medio13X + medio13Y
        
        x.append(newX)
        y.append(newY)
        
        #BUSCANDO EL NUEVO RADIO   
        
        p = 3
        
        if len(puntos) < 3:
            p = len(puntos)

        tresPuntos = random.sample(puntos, p) #cojo tres puntos aleatorios, ya que con los tres mejores puntos el algoritmo se quedaba pillado en algunos puntos
        
        distanciaDePuntoACentro = 0
        
        for j in range(0, len(tresPuntos)):
            
            punto = tresPuntos[j]
            
            varX = punto[0]
            varY = punto[1]
            
            distanciaDePuntoACentro = math.sqrt(((x[i] - varX)*(x[i] - varX)) + ((y[i] - varY)*(y[i] - varY))) + distanciaDePuntoACentro
                       
        nuevoRadio = distanciaDePuntoACentro/len(tresPuntos)   
            
        r.append(nuevoRadio)
           
    return x, y, r

def nuevasCircunferenciasV4(puntosTotales, puntosPorCluster, gradosPorCluster, n_clusters): #Le daré el conjunto de puntos que pertenecen a esa circunferencia, tras ello usaré los 3 puntos con mejor grado de pertenencia para calcular el nuevo radio, y el centro será la media de todos los puntos
    #Este algoritmo estará basado en findCircle, k-medias, y mi propia lógica
    
    #Por cada Circunferencia, voy a calcular su nuevo radio y centro
    
    x = [] #Lista con las variables X de cada centro
    y = [] #Lista con las variables Y de cada centro
    r = [] #Lista con los radios de cada centro
    
    for i in range(n_clusters): #Recorro cada cluster
        
        puntos = puntosPorCluster[i] #Obtengo los puntos de ese cluster
        grados = gradosPorCluster[i] #Obtengo los grados de ese cluster
        
        #BUSCANDO EL NUEVO CENTRO
        
        punto1, punto3 = random.sample(puntos, 2) #Cojo dos puntos aleatorios
        
        x1 = punto1[0]
        y1 = punto1[1]

        distanciasP1 = []
        
        for j in range(0, len(puntos)):
               
            punto = puntos[j]
            
            varX = punto[0]
            varY = punto[1]
            
            distanciaDePuntoAP1 = math.sqrt(((x1 - varX)*(x1 - varX)) + ((y1 - varY)*(y1 - varY)))
        
            distanciasP1.append(distanciaDePuntoAP1)
              
        #Busco los mas alejados
        
        indexP2 = distanciasP1.index(max(distanciasP1)) #Punto más alejado
         
        punto2 = puntos[indexP2]
      
        x2 = punto2[0]
        y2 = punto2[1]
        
        newX = (x1+x2)/2
        newY = (y1+y2)/2
        
        xe = round(newX, 1)
        ye = round(newY, 1)
  
        x.append(xe)
        y.append(ye)
        

        #BUSCANDO EL NUEVO RADIO   
            #PROBAR CON TODOS LOS PUNTOS DEL CLUSTER, EN VEZ DE 3 Aleatorios
        p = 3
        
        if len(puntos) < 3:
            p = len(puntos)

        tresPuntos = random.sample(puntos, p) #cojo tres puntos aleatorios, ya que con los tres mejores puntos el algoritmo se quedaba pillado en algunos puntos
        
        distanciaDePuntoACentro = 0
        
        for j in range(0, len(tresPuntos)):
            
            punto = tresPuntos[j]
            
            varX = punto[0]
            varY = punto[1]
            
            distanciaDePuntoACentro = math.sqrt(((x[i] - varX)*(x[i] - varX)) + ((y[i] - varY)*(y[i] - varY))) + distanciaDePuntoACentro
                       
        nuevoRadio = distanciaDePuntoACentro/len(tresPuntos) 
            
        ra = round(nuevoRadio, 1)    
            
        r.append(ra)
        
        
        print("El nuevo centro de la circunferencia", i+1, "es:", x[i], ",", y[i])
        print("El nuevo radio de la circunferencia", i+1, "es:", r[i])
        
        print("------------------------------------------------------------------------------------")
    
    return x, y, r
    
def calculaGradosPertenencias(puntosTotales, x, y, radios, n_clusters):
    
    gradosPertenenciaPorPuntosNORMALIZADOS = []    
    puntosPorCluster = [] #Cada elemento de esta lista será una lista con varios puntos, los puntos del cluster 1 serán del index 0, etc.
    gradosPorCluster = []
    
    for i in range(0, len(puntosTotales)): #Recorremos todos los puntos
        
        punto = puntosTotales.values[i] #Obtenemos el valor del punto en el índice 'i'
        
        varX = punto[0]
        varY = punto[1]
        
        gradosPertenencia = [] #grados de pertenencia del punto en cuestion
        gradosPertenenciaNormalizados = [] #grados de pertenencia NORMALIZADOS del punto en cuestion
        
        #Ahora hay que calcular la distancia del 'punto' a los centros de los cluster
        
        for j in range(n_clusters): #En vez de dos deberá ser el nº de clusters RECORRO EL NÚMERO DE CLUSTERS
            
                distanciaDePuntoACentro = math.sqrt(((x[j] - varX)*(x[j] - varX)) + ((y[j] - varY)*(y[j] - varY)))
                
                distanciaDePuntoACircunferencia =  abs(distanciaDePuntoACentro - radios[j])
                
                gradosPertenencia.append(distanciaDePuntoACircunferencia)
                
                        
        #Normalizamos los valores
        
        denominador = sum(gradosPertenencia) + 0.00000000000000000000000000000000000000000000000001
        
        for l in range(0, len(gradosPertenencia)):
            
            numerador = gradosPertenencia[l]/denominador

            gradosPertenenciaNormalizados.append(numerador)           
           
        #El punto pertenece al círculo con grado de menor valor      
        minpos = gradosPertenenciaNormalizados.index(min(gradosPertenenciaNormalizados))         
    
        gradosPertenenciaPorPuntosNORMALIZADOS.append(gradosPertenenciaNormalizados)
        
    print("dsfsdfsdfs",gradosPertenenciaPorPuntosNORMALIZADOS)

    for i in range(n_clusters): #Recorro cada cluster, y comparo cada grado de cada punto y lo añado o no si pertenece a ese cluster
        
        puntosPertenecientesAlCluster = []
        gradosDeLosPuntosPertenecientesAlCluster = []
        
        for j in range(0, len(gradosPertenenciaPorPuntosNORMALIZADOS)):
            
            gradosDelPuntoJ = gradosPertenenciaPorPuntosNORMALIZADOS[j]
           
            if gradosDelPuntoJ.index(min(gradosDelPuntoJ)) == i:
                puntosPertenecientesAlCluster.append(puntosTotales.values[j])
                gradosDeLosPuntosPertenecientesAlCluster.append(min(gradosDelPuntoJ))
                
                
        if len(puntosPertenecientesAlCluster) < 3: #Si algun cluster se queda sin puntos, le asigno sus 3 mejores puntos AHORA OBLIGO A QUE TENGA 3 CIRCULOS JEJ
            
            gradosDelClusterN = []   
            
            for u in range(0, len(gradosPertenenciaPorPuntosNORMALIZADOS)):
                
                tuplaDeGrados = gradosPertenenciaPorPuntosNORMALIZADOS[u]
                
                gradosDelClusterN.append(tuplaDeGrados[i])
                  
            
            print("ESTOY SIN PUNTOS JKEJE", gradosDelClusterN)
            
            tresMejoresDeN = nsmallest(2, gradosDelClusterN)
            peor = max(gradosDelClusterN)
            
            gradosDeLosPuntosPertenecientesAlCluster.append(tresMejoresDeN[0])
            gradosDeLosPuntosPertenecientesAlCluster.append(tresMejoresDeN[1])
            gradosDeLosPuntosPertenecientesAlCluster.append(peor)
            
            print("MIS TRES MEJORES JEJ", tresMejoresDeN)
            
            indPuntos = []
            
            for o in range(0, 2):
                
                for v in range(0, len(gradosPertenenciaPorPuntosNORMALIZADOS)):
                
                    gradosDelPuntoV = gradosPertenenciaPorPuntosNORMALIZADOS[v]
                
                    if tresMejoresDeN[o] in  gradosDelPuntoV:
                        
                        indPuntos.append(v)
                        
                    
            
            print("Indice de los puntos", indPuntos)
            
            for h in range(0, 2):
                
                index = indPuntos[h] 
            
                puntosPertenecientesAlCluster.append(puntosTotales.values[index])
            
            
            #Como tercero cojo el que peor 
            
            for v in range(0, len(gradosPertenenciaPorPuntosNORMALIZADOS)):
                
                gradosDelPuntoV = gradosPertenenciaPorPuntosNORMALIZADOS[v]
            
                if peor in gradosDelPuntoV:
                    
                    puntosPertenecientesAlCluster.append(puntosTotales.values[v])
            
        puntosPorCluster.append(puntosPertenecientesAlCluster) 
        gradosPorCluster.append(gradosDeLosPuntosPertenecientesAlCluster)
    
    
    print("Lista de Puntos separados por Cluster:", puntosPorCluster)
    
    print("------------------------------------------------------------------------------------")
    
    return puntosPorCluster, gradosPorCluster
    
def inicializacion(n_clusters, url_datos): #Inicializa los circulos según un número de cluster predeterminado
    
    with open(url_datos, newline='') as f:
    
        puntosCSV = csv.reader(f)
        puntos = list(puntosCSV)
        
    x = []
    y = []
    radios = []    
        
    n = n_clusters*3
        
    puntosNecesarios = random.sample(puntos, n) #Obtengo 6 puntos aleatorios
    
    
    for i in range (0, n_clusters):
        
        puntoA = puntosNecesarios[0]
        puntoB = puntosNecesarios[1]
        puntoC = puntosNecesarios[2]
     
        x1, y1, r1 = findCircle(float(puntoA[0]), float(puntoA[1]), float(puntoB[0]), float(puntoB[1]), float(puntoC[0]), float(puntoC[1])) 
        
        puntosNecesarios.pop(0)
        puntosNecesarios.pop(0)
        puntosNecesarios.pop(0)
        
        x.append(x1) 
        y.append(y1)
        radios.append(r1)
    
    print("------------------------------------------------------------------------------------")
    
    return x, y, radios
    
def representacionGrafica(x, y, radios, puntosPorCluster):  #Hay que dar los centros y los radios 

    fig = plt.figure(figsize = (6,6))

    ax = fig.add_subplot()
    ax.set_xlabel('X', fontsize = 15)
    ax.set_ylabel('Y', fontsize = 15)
    ax.set_xlim(-2,28)
    ax.set_ylim(-2,28)
    ax.set_title('Círculos', fontsize = 20)
    
    colores = ["r", "b", "g", "y", "p"]
    
    for i in range(0, len(radios)):
        
        varX = x[i]
        varY = y[i]
        
        puntosDelCluster = puntosPorCluster[i]
        color = colores[i]
        
        #Dibujando la circunferencia
        ax.scatter(x = varX, y = varY, c=color, s = 15)
        circle1 = plt.Circle((varX,varY), radios[i], color= color, fill= False)
        ax.add_artist(circle1)
        
        #Dibujando los puntos del cluster pertenecientes a esa circunferencia
        for j in range(0, len(puntosDelCluster)):
            punto = puntosDelCluster[j]
            ax.scatter(punto[0], y = punto[1],c=color, s = 5)
             
    plt.grid()
    plt.show()
     
def buscandoAproximarLasCircunferencias(n_cluster, url_datos): #Calculo del grado de pertenencia inicial y muestra gráfica
    
    time1 = time.time() #Iniciamos el tiempo de ejecución de la función
    
    x, y, radios = inicializacion(n_cluster, url_datos)

    puntosCSV = pd.read_csv(url_datos, header=None, names=['X', 'Y'])
    
    valorParada = 0.019 #Valor que mejor me aproxima los ejemplos proporcionados
    
    sumGradosTotal = 10 #Para los ejemplos de una circunferencia
    
    counter = 1
    
    max_interacciones = 3000 #Para que no se eternice
    
    
    while (sumGradosTotal > valorParada) and (max_interacciones > counter):
        
        print("Ciclo", counter)
        print("========")
        
        condicion = True
        
        counter = counter + 1
        
        puntosPorCluster, gradosPorCluster = calculaGradosPertenencias(puntosCSV, x, y, radios, n_cluster)
        
        #CONDICIÓN DE PARADA
        for i in range(n_cluster):
            
            mediaGradosCluster = sum(gradosPorCluster[i])/(len(gradosPorCluster[i])) #F1
            
            sumGradosTotal =  sumGradosTotal + mediaGradosCluster #F1
            
            print("Cluster", i, ":", mediaGradosCluster)
            
        sumGradosTotal = sumGradosTotal/len(gradosPorCluster) #Esta es la media de grados juntando todos los cluster #F1
        
        if(n_cluster) == 1:
            
            sumGradosTotal = sumGradosTotal - 1
            valorParada = 10
        
        print("Valor de Condición de parada:", sumGradosTotal)
        print("------------------------------------------------------------------------------------")
        
        #x, y, radios = nuevasCircunferencias(puntosCSV, puntosPorCluster, gradosPorCluster, n_cluster)
        #x, y, radios = nuevasCircunferenciasV2(puntosPorCluster)
        #x, y, radios = nuevasCircunferenciasV3(puntosPorCluster)
        x, y, radios = nuevasCircunferenciasV4(puntosCSV, puntosPorCluster, gradosPorCluster, n_cluster)
       
        #representacionGrafica(x, y, radios, puntosPorCluster)

    print("Solución encontrada en el ciclo:", counter - 1)
    
    time2 = time.time() #Paramos el tiempo de ejecución
    print('Tiempo en encontrar la solución:', round(((time2-time1)), 2), "segundos.")
    representacionGrafica(x, y, radios, puntosPorCluster)
    
def generadorDeEjemplosEspecificos(nombre, n_clusters, centrosJuntos, radiosJuntos, n_min, n_max, ruido): #Genera ejemplo
    
    #EN LA ENTRADA DE RADIOS Y CENTROS SOLO SE PERMITEN NUMEROS ENTEROS
    #ES OBLIGATORIO SEGUIR EL PATRON: "(x,y), (x1,y1), (x2, y2)..." PARA LA ENTRADA DE CENTROS
    
    centros = centrosJuntos.split(", ")
    radios = radiosJuntos.split(", ")
    
    x = [] #Aqui almacenaré el valor de las X de los puntos
    y = [] #Aqui almacenaré el valor de las Y de los puntos

    for i in range(0, int(n_clusters)):
        
        #Obtengo el centro y el radio del cluster i   
        centro = centros[i]
     
        #Un poco basto pero no tengo mucho conocimiento sobre python
        centro = centro.replace(',','')
        centro = centro.replace(')','')
        centro = centro.replace('(','')
        
        r0 = radios[i]  
        x0 = centro[0]
        y0 = centro[1]
        
        numPuntosPorCluster = random.randint(int(n_min), int(n_max)) #Número de puntos por cluster
        
        #Obteniendo los puntos
        
        for i2 in range(0, numPuntosPorCluster):
            
            angulo = random.randint(0, 360) #Ángulo aleatorio
            
            varX = int(x0) + int(r0)*math.cos(angulo) #Valor de la X será el coseno del angulo por el radio
            varY = int(y0) + int(r0)*math.sin(angulo) #Valor de la Y será el seno del angulo por el radio
        
            x.append(round(varX, 1)) #Redondeo los valores con un decimal
            y.append(round(varY, 1))
                      
        #Representación de ruido
        
        if ruido == True:
        
            puntosDeRuido = round((numPuntosPorCluster/5), 0) #Establezco el nº de ruido como la quinta parte de los puntos del cluster
        
            print(puntosDeRuido)
        
            for i3 in range (0, int(puntosDeRuido)):
            
                valorDeRuido = random.uniform(-1.5, 1.5)
            
                while abs(valorDeRuido) < 0.5:                        #Me aseguro que el valor de ruido será mayor de 0.5
                    valorDeRuido = random.uniform(-1.5, 1.5)
            
                angulo = random.randint(0, 360) #Ángulo aleatorio
            
                varX = int(x0) + int(r0)*math.cos(angulo) + valorDeRuido #Valor de la X
                varY = int(y0) + int(r0)*math.sin(angulo) + valorDeRuido #Valor de la Y
        
                x.append(round(varX, 1)) #Redondeo los valores con un decimal
                y.append(round(varY, 1))
           
    #Representacion de los datos generados    
    
    fig = plt.figure(figsize = (6,6))

    ax = fig.add_subplot()
    ax.set_xlabel('X', fontsize = 15)
    ax.set_ylabel('Y', fontsize = 15)
    ax.set_xlim(-20,20)
    ax.set_ylim(-20,20)
    ax.set_title('Puntos', fontsize = 20)
     
    for i4 in range(0, len(x)):
       
        ax.scatter(x[i4], y = y[i4], c="black", s = 20)
             
    plt.grid()
    
    nombreFinal = nombre + ".csv"
    
    try:
        ejemplo = open(nombreFinal, "x") #Generamos el archivo en la raiz del proyecto  
    except FileExistsError:
        tkinter.messagebox.showerror("¡Error!", "¡Ya hay un archivo con ese nombre!") #Error si ya existe
    else:
        
        #Escribimos los puntos en el archivo
    
        for i5 in range(0, len(x)):
        
            if i5 != 0:
                ejemplo.write("\n")
        
            ejemplo.write(str(x[i5]))
            ejemplo.write(", ")
            ejemplo.write(str(y[i5]))
        
        ejemplo.close

        plt.show()

def generadorDeEjemplosAleatorios(nombre, n_clusters, n_min, n_max, ruido): #Genera ejemplo
    
    x = [] #Aqui almacenaré el valor de las X de los puntos
    y = [] #Aqui almacenaré el valor de las Y de los puntos

    for i in range(0, int(n_clusters)):
        
        r0 = random.randint(1, 10) 
        x0 = random.uniform(-10, 10)
        y0 = random.uniform(-10, 10)
        
        numPuntosPorCluster = random.randint(int(n_min), int(n_max)) #Número de puntos por cluster
        
        #Obteniendo los puntos
        
        for i2 in range(0, numPuntosPorCluster):
            
            angulo = random.randint(0, 360) #Ángulo aleatorio
            
            varX = int(x0) + int(r0)*math.cos(angulo) #Valor de la X será el coseno del angulo por el radio
            varY = int(y0) + int(r0)*math.sin(angulo) #Valor de la Y será el seno del angulo por el radio
        
            x.append(round(varX, 1)) #Redondeo los valores con un decimal
            y.append(round(varY, 1))
                      
        #Representación de ruido
        
        if ruido == True:
        
            puntosDeRuido = round((numPuntosPorCluster/5), 0) #Establezco el nº de ruido como la quinta parte de los puntos del cluster
        
            print(puntosDeRuido)
        
            for i3 in range (0, int(puntosDeRuido)):
            
                valorDeRuido = random.uniform(-1.5, 1.5)
            
                while abs(valorDeRuido) < 0.5:                        #Me aseguro que el valor de ruido será mayor de 0.5
                    valorDeRuido = random.uniform(-1.5, 1.5)
            
                angulo = random.randint(0, 360) #Ángulo aleatorio
            
                varX = int(x0) + int(r0)*math.cos(angulo) + valorDeRuido #Valor de la X
                varY = int(y0) + int(r0)*math.sin(angulo) + valorDeRuido #Valor de la Y
        
                x.append(round(varX, 1)) #Redondeo los valores con un decimal
                y.append(round(varY, 1))
           
    #Representacion de los datos generados    
    
    fig = plt.figure(figsize = (6,6))

    ax = fig.add_subplot()
    ax.set_xlabel('X', fontsize = 15)
    ax.set_ylabel('Y', fontsize = 15)
    ax.set_xlim(-20,20)
    ax.set_ylim(-20,20)
    ax.set_title('Puntos', fontsize = 20)
     
    for i4 in range(0, len(x)):
       
        ax.scatter(x[i4], y = y[i4], c="black", s = 20)
             
    plt.grid()
    
    nombreFinal = nombre + ".csv"
    
    try:
        ejemplo = open(nombreFinal, "x") #Generamos el archivo en la raiz del proyecto  
    except FileExistsError:
        tkinter.messagebox.showerror("¡Error!", "¡Ya hay un archivo con ese nombre!") #Error si ya existe
    else:
        
        #Escribimos los puntos en el archivo
    
        for i5 in range(0, len(x)):
        
            if i5 != 0:
                ejemplo.write("\n")
        
            ejemplo.write(str(x[i5]))
            ejemplo.write(", ")
            ejemplo.write(str(y[i5]))
        
        ejemplo.close

        plt.show()   
        


#ESTILO Y REPRESENTACIÓN
#=======================

def ventana_principal():
    
    ventanaPrincipal = tkinter.Tk()
    ventanaPrincipal.geometry("450x450")
    ventanaPrincipal.config(bg='#CFF9FF')
    ventanaPrincipal.title("Clustering Bajo Incertidumbre") 
    
    image = Image.open('fondo.png')
    photo_image = ImageTk.PhotoImage(image)
    label = tkinter.Label(ventanaPrincipal, image = photo_image, bg='#CFF9FF')
    
    button = tkinter.Button(text="Aproximar Circunferencias",  command=ventana_aproximar)
    button.config(bg="#8DE9F5", activebackground="#BCF7FF", font=('MV Boli', '13'), height = 2, width = 25)
    button.pack(side=tkinter.TOP, anchor=tkinter.NW, padx = 40, pady=20)
    
    button2 = tkinter.Button(text="Generar Ejemplo",  command=ventana_generador)
    button2.config(bg="#8DE9F5", activebackground="#BCF7FF", font=('MV Boli', '13'), height = 2, width = 25)
    button2.pack(side=tkinter.TOP, anchor=tkinter.NW, padx=40)
    
    label.pack()
    
    ventanaPrincipal.mainloop()
    
def ventana_aproximar():  
    
    def abrirArchivo():
        fichero.config(state = 'normal', bg= "#B9F0A1")
        
        if len(fichero.get()) != 0:  #Limpiamos el entry con los datos del archivo anterior si se decide cambiar de archivo antes de comenzar
            fichero.delete(0, 'end')
            
        archivoDatos = tkinter.filedialog.askopenfilename(initialdir = "/", title = "Selecciona un archivo '.csv'", filetype = (("csv", "*.csv"), ("All Files", "*.*")))
        fichero.insert(0, archivoDatos)
        fichero.config(state = 'readonly')
     
    def aceptar(event):
           
        if len(numeroDeClusters.get()) == 0 or len(fichero.get()) == 0: #Comprobando si se han introducido los datos
            
            tkinter.messagebox.showwarning("¡Cuidado!", "¡Has olvidado introducir el nº de clusters o el archivo de datos!")    
            
        else:
            try:
                int(numeroDeClusters.get()) #Comprobando si el numero de cluster introducido es un numero entero   
            except ValueError:
                tkinter.messagebox.showerror("¡Error!", "¡Has introducido un valor incorrecto como nº de clusters!")      
            else:  
                
                mensaje = "El nº de clusters introducidos es: '" + numeroDeClusters.get() + "'" + "\nLa ruta selecionada es: '" + fichero.get() + "'" + "\n\nRecuerda que si selecciona un valor de clusters que no se adecúa a los datos el proceso podría eternizarse. \n \n ¿Estás seguro de que desea continuar?"
                
                if tkinter.messagebox.askokcancel("¿Estás seguro?", mensaje): #Si aceptamos, finalmente ejecutamos la aproximación de circunferencias
                
                    buscandoAproximarLasCircunferencias(int(numeroDeClusters.get()), str(fichero.get()))
             
    ventanaAprox = tkinter.Tk()
    ventanaAprox.title("Aproximar Circunferencias")    
    ventanaAprox.geometry("590x250")
    ventanaAprox.config(bg='#DEFFCF')
    
    mensaje = tkinter.Text(ventanaAprox, background="#B9F0A1", font=("Gabriola", 10,))
    mensaje.insert(tkinter.INSERT, "RECUERDA: Para el número de circunferencias deberá \n introducir un número entero, mientras que para los \n datos de entrada deberá seleccionar un archivo: '.csv'.")
    mensaje.config(width = 45, height = 3, state='disabled')
    mensaje.grid(row=3, column = 0)
    
    tkinter.Label(ventanaAprox, text = "Número de circunferencias:", font = "Gabriola 16 bold", padx = 25, pady = 10, bg = "#DEFFCF").grid(row=0)
    tkinter.Label(ventanaAprox, text = "Datos de entrada:", font = "Gabriola 16 bold", padx = 20, pady = 10, bg = "#DEFFCF",).grid(row=1)
    
    tkinter.Label(ventanaAprox, pady =12, bg = "#DEFFCF",).grid(row=2) #Espacio
    
    numeroDeClusters = tkinter.Entry(ventanaAprox)
    fichero = tkinter.Entry(ventanaAprox) 
    
    numeroDeClusters.config(width = 26, bg= "#B9F0A1")
    fichero.config(width = 26, state ='readonly', readonlybackground = "#B9F0A1") 
    
    numeroDeClusters.grid(row=0, column=1)
    fichero.grid(row=1, column=1) 
    
    numeroDeClusters.bind("<Return>", aceptar)
    fichero.bind("<Return>", aceptar)
     
    #Sube tu archivo
     
    tkinter.Label(ventanaAprox, padx =12, bg = "#DEFFCF",).grid(row=1, column = 2) #Espacio
    
    botonSubeArchivo = tkinter.Button(ventanaAprox, text = "Buscar archivo", font=('MV Boli', '10'), bg="#98D37E", activebackground="#B9F0A1", command = abrirArchivo, padx = 10).grid(row = 1, column = 3) 
    botonAceptar = tkinter.Button(ventanaAprox, text = "Comenzar", font=('MV Boli', '10'), bg="#FFAC54", activebackground="#FFD1A0", command = lambda: aceptar("<Return>"), padx = 10).grid(row = 0, column = 3) 
    
def ventana_generador():
    
    def select():
        
        print(chks.get())
             
        if chks.get() == True:
            chks.set(False)
            
        else:
            chks.set(True)   
            
        print(chks.get())     
    
    def generar(event):
        
        cenBool = False
        radBool = False
        ruido = False 
        
        print(chks.get())
        print(nombre.get())    
            
        if len(str(radios.get())) != 0:
            radBool = True 
            
        if len(str(centros.get())) != 0:
            cenBool = True  
        
        #Check valores necesarios
        
        if len(numeroDeClusters.get()) == 0 or len(numeroMinPuntos.get()) == 0 or len(numeroMaxPuntos.get()) == 0 or len(nombre.get()) == 0: #Comprobando si se han introducido los datos         
            return tkinter.messagebox.showwarning("¡Cuidado!", "¡Has olvidado introducir el nombre, el nº de clusters o el rango de puntos!")
             
        #Check nombre max 60 caracteres
        if len(nombre.get()) > 60:         
            return tkinter.messagebox.showwarning("¡Cuidado!", "¡El nombre no puede superar 60 caracteres!")
            
        #Check valores integer
        try:
            int(numeroDeClusters.get())
            int(numeroMinPuntos.get())
            int(numeroMaxPuntos.get())  
        except ValueError:
            tkinter.messagebox.showerror("¡Error!", "¡Has introducido un valor incorrecto en el nº de circunferencias, mínimo de puntos o máximo de puntos, recuerda que deben ser números enteros!")
        
        #Check min < max   
        if int(numeroMinPuntos.get()) > int(numeroMaxPuntos.get()):
            return tkinter.messagebox.showwarning("¡Cuidado!", "¡El mínimo de puntos no puede superar al máximo de puntos!")
        
        #Check min distinto de 0
        if int(numeroMinPuntos.get()) == 0:
            return tkinter.messagebox.showwarning("¡Cuidado!", "¡El mínimo de puntos no puede ser igual a 0!")
               
        #Check radio+centros
        if (radBool == False and cenBool == True) or (radBool == True and cenBool == False) :
            return tkinter.messagebox.showwarning("¡Cuidado!", "¡Si introduces centros debes introducir radios y viceversa!")
        
        #if radios And centros --> Check datos en int DE LOCOS
         
        #if radios And centros --> Check radioSize = centroSize = nClusters MAL
        if len(str(centros.get())) !=  len(str(radios.get())):
            return tkinter.messagebox.showerror("¡Error!", "¡El número de radios debe ser igual al número de centros y al número de circunferencias!")
            
        #if radios And centros --> Check patron radios and centros  LEL
            
        if (radBool == False and cenBool == False):
    
            generadorDeEjemplosAleatorios(str(nombre.get()), int(numeroDeClusters.get()), int(numeroMinPuntos.get()), int(numeroMaxPuntos.get()), chks)
        else:    
            generadorDeEjemplosEspecificos(str(nombre.get()), int(numeroDeClusters.get()), str(centros.get()), str(radios.get()), int(numeroMinPuntos.get()), int(numeroMaxPuntos.get()), chks)
    
    ventanaGen = tkinter.Tk()
    ventanaGen.title("Generador de Ejemplos")    
    ventanaGen.geometry("612x450")
    ventanaGen.config(bg='#FFD1A0')
     
    #Títulos
    
    chks = tkinter.BooleanVar()
       
    tkinter.Label(ventanaGen, text = "Nombre:", anchor= "e", font = "Gabriola 16 bold", bg='#FFD1A0', width = 30).grid(row=1)
    tkinter.Label(ventanaGen, text = "Número de circunferencias:", anchor= "e", font = "Gabriola 16 bold", bg='#FFD1A0', width = 30).grid(row=2)
    tkinter.Label(ventanaGen, text = "Número mínimo de puntos por cluster:", anchor= "e", font = "Gabriola 16 bold", bg='#FFD1A0', width = 30).grid(row=3)
    tkinter.Label(ventanaGen, text = "Número máximo de puntos por cluster:", anchor= "e", font = "Gabriola 16 bold", bg='#FFD1A0', width = 30).grid(row=4) 
    checky = tkinter.Checkbutton(ventanaGen, text = "Aplicar ruido", variable = chks,  font = "Gabriola 16 bold", bg='#FFD1A0', activebackground="#FFD1A0", selectcolor = "#FFB96F", command= select)
    tkinter.Label(ventanaGen, text = "Centros (Opcional):", anchor= "e", font = "Gabriola 16 bold", bg='#FFD1A0', width = 30).grid(row=7)
    tkinter.Label(ventanaGen, text = "Radios (Opcional):", anchor= "e", font = "Gabriola 16 bold", bg='#FFD1A0', width = 30).grid(row=8)
    
    tkinter.Label(ventanaGen, text = "ej: '(x1,y1), (x2,y2)...'", font = "Arial 10", bg = "#FFD1A0", fg = "grey").grid(row=7, column = 4)
    tkinter.Label(ventanaGen, text = "ej: 'r1, r2, r3, r4, r5...'", font = "Arial 10", bg = "#FFD1A0", fg = "grey").grid(row=8, column = 4)
  
    #Entradas
    
    nombre = tkinter.Entry(ventanaGen, bg= "#FFB96F") 
    numeroDeClusters = tkinter.Entry(ventanaGen, bg= "#FFB96F") 
    numeroMinPuntos = tkinter.Entry(ventanaGen, bg= "#FFB96F") 
    numeroMaxPuntos = tkinter.Entry(ventanaGen, bg= "#FFB96F")  
    centros = tkinter.Entry(ventanaGen, bg= "#FFB96F")  
    radios = tkinter.Entry(ventanaGen, bg= "#FFB96F")
    
    nombre.grid(row = 1, column = 2)
    numeroDeClusters.grid(row = 2, column = 2)  
    numeroMinPuntos.grid(row = 3, column = 2)  
    numeroMaxPuntos.grid(row = 4, column = 2)  
    centros.grid(row = 7, column =2)  
    radios.grid(row = 8, column =2) 
    checky.grid(row=5, column = 2)  
    
    nombre.bind("<Return>", generar)
    numeroDeClusters.bind("<Return>", generar)
    numeroMinPuntos.bind("<Return>", generar)
    numeroMaxPuntos.bind("<Return>", generar)
    centros.bind("<Return>", generar)
    radios.bind("<Return>", generar)
    checky.bind("<Return>", generar)  
    
    #Generar
    
    botonAceptar = tkinter.Button(ventanaGen, text = "Generar", font=('MV Boli', '10'), bg="#98D37E", activebackground="#B9F0A1", command = lambda: generar("<Return>"), padx = 10).grid(row = 10, column = 2) 
    
    #Espacios en blanco
    
    tkinter.Label(ventanaGen, bg = "#FFD1A0").grid(row=9)
    tkinter.Label(ventanaGen, bg = "#FFD1A0", width = 5).grid(column=1)
    tkinter.Label(ventanaGen, bg = "#FFD1A0").grid(row=6)
    tkinter.Label(ventanaGen, bg = "#FFD1A0").grid(row=0)
       
if __name__ == "__main__":
    #probando()
    #ventana_principal()
    buscandoAproximarLasCircunferencias(3, "C:/Users/Rafa/git/ClusteringBajoIncertidumbreIA/puntos2.csv")
    
   
    