#encoding:utf-8
import random
import matplotlib.pyplot as plt
import pandas as pd
import math
import csv
from heapq import nsmallest

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
  
    print("Centre = (", h, ", ", k, ")");  
    print("Radius = ", r);  

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

        punto1, punto2, punto3 = random.sample(puntos, 3) #cojo tres puntos aleatorios, ya que con los tres mejores puntos el algoritmo se quedaba pillado en algunos puntos
        
        tresPuntos = []
        
        tresPuntos.append(punto1)
        tresPuntos.append(punto2)
        tresPuntos.append(punto3)

        distanciaDePuntoACentro = 0
        
        for j in range(0, 3):
            
            punto = tresPuntos[j]
            
            varX = punto[0]
            varY = punto[1]
            
            distanciaDePuntoACentro = math.sqrt(((x[i] - varX)*(x[i] - varX)) + ((y[i] - varY)*(y[i] - varY))) + distanciaDePuntoACentro
                       
        nuevoRadio = distanciaDePuntoACentro/len(tresPuntos)        
                  
        r.append(nuevoRadio)
        
        print("El nuevo radio de la circunferencia", i+1, "es: (", r[i])
        
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
        
        for j in range(2): #En vez de dos deberá ser el nº de clusters RECORRO EL NÚMERO DE CLUSTERS
            
                distanciaDePuntoACentro = math.sqrt(((x[j] - varX)*(x[j] - varX)) + ((y[j] - varY)*(y[j] - varY)))
                
                distanciaDePuntoACircunferencia =  abs(distanciaDePuntoACentro - radios[j])
                
                gradosPertenencia.append(distanciaDePuntoACircunferencia)
                
                        
        #Normalizamos los valores
        
        denominador = sum(gradosPertenencia)
        
        for l in range(0, len(gradosPertenencia)):
            
            numerador = gradosPertenencia[l]/denominador

            gradosPertenenciaNormalizados.append(numerador)           
           
        #El punto pertenece al círculo con grado de menor valor      
        minpos = gradosPertenenciaNormalizados.index(min(gradosPertenenciaNormalizados))         
    
        gradosPertenenciaPorPuntosNORMALIZADOS.append(gradosPertenenciaNormalizados)
        

    for i in range(2): #Recorro cada cluster, y comparo cada grado de cada punto y lo añado o no si pertenece a ese cluster
        
        puntosPertenecientesAlCluster = []
        gradosDeLosPuntosPertenecientesAlCluster = []
        
        for j in range(0, len(gradosPertenenciaPorPuntosNORMALIZADOS)):
            
            gradosDelPuntoJ = gradosPertenenciaPorPuntosNORMALIZADOS[j]
           
            if gradosDelPuntoJ.index(min(gradosDelPuntoJ)) == i:
                puntosPertenecientesAlCluster.append(puntosTotales.values[j])
                gradosDeLosPuntosPertenecientesAlCluster.append(min(gradosDelPuntoJ))

        puntosPorCluster.append(puntosPertenecientesAlCluster) 
        gradosPorCluster.append(gradosDeLosPuntosPertenecientesAlCluster)
    
    
    return puntosPorCluster, gradosPorCluster
    

def inicializacion(n_clusters): #Inicializa los circulos según un número de cluster predeterminado
    
    with open('puntos.csv', newline='') as f:
    
        puntosCSV = csv.reader(f)
        puntos = list(puntosCSV)
        
        
    puntoA, puntoB, puntoC, puntoD, puntoE, puntoF = random.sample(puntos, 6) #Obtengo 6 puntos aleatorios
     
    x1, y1, r1 = findCircle(float(puntoA[0]), float(puntoA[1]), float(puntoB[0]), float(puntoB[1]), float(puntoC[0]), float(puntoC[1])) #Circunferencia1
    x2, y2, r2 = findCircle(float(puntoD[0]), float(puntoD[1]), float(puntoE[0]), float(puntoE[1]), float(puntoF[0]), float(puntoF[1])) #Circunferencia2
    
    x = []
    y = []
    radios = []
    
    x.append(x1)
    x.append(x2)
    y.append(y1)
    y.append(y2)
    
    radios.append(r1)
    radios.append(r2)
    
    print("------------------------------------------------------------------------------------")
    
    return x, y, radios
    
     
def representacionGrafica(x, y, radios):  #Hay que dar los centros y los radios 

    puntosCSV = pd.read_csv('puntos.csv', header=None, names=['X', 'Y'])
    
    fig = plt.figure(figsize = (6,6))

    ax = fig.add_subplot()
    ax.set_xlabel('X', fontsize = 15)
    ax.set_ylabel('Y', fontsize = 15)
    ax.set_xlim(-5,15)
    ax.set_ylim(-5,15)
    ax.set_title('Círculos', fontsize = 20)
    
    
    for i in range(0, 2):
        
        varX = x[i]
        varY = y[i]
        
        circle1 = plt.Circle((varX,varY), radios[i], color='r', fill= False)
        ax.scatter(x = varX, y = varY, s = 5)
        ax.scatter(puntosCSV.X, y = puntosCSV.Y,c='b', s = 20)
        
        ax.add_artist(circle1)
    
    plt.grid()
    plt.show()
     

def buscandoAproximarLasCircunferencias(): #Calculo del grado de pertenencia inicial y muestra gráfica
    
    x, y, radios = inicializacion(1)

    puntosCSV = pd.read_csv('puntos.csv', header=None, names=['X', 'Y'])
    
    for i in range(20):
        
        print("LOOP")
        
        p1, p2 = calculaGradosPertenencias(puntosCSV, x, y, radios, 2)
    
        x, y, radios = nuevasCircunferencias(puntosCSV, p1, p2, 2)
    
        representacionGrafica(x, y, radios)
    
    
if __name__ == "__main__":

    buscandoAproximarLasCircunferencias()