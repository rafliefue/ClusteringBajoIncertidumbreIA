#encoding:utf-8
import random
import matplotlib.pyplot as plt
import pandas as pd
import math
import csv

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


def inicializacion(): #Inicializa los circulos
    
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
     

def buscandoAproximarLasCircunferencias(): #Calculo del grado de pertenencia inicial y muestra gr�fica
    
    x, y, radios = inicializacion()

    puntosCSV = pd.read_csv('puntos.csv', header=None, names=['X', 'Y'])
    
    gradosPertenenciaPorPuntos = []
    
    for i in range(0, len(puntosCSV)):
        
        punto = puntosCSV.values[i] #Obtenemos el valor del punto en el �ndice 'i'
        
        varX = punto[0]
        varY = punto[1]
        
        gradosPertenencia = [] #grados de pertenencia del punto en cuestion
        gradosPertenenciaNormalizados = []
        
        #Ahora hay que calcular la distancia del 'punto' a los centros de los cluster
        
        for j in range(2): #En vez de dos deber�a ser el n� de clusters
            
                centroCluster = []
                centroCluster.append(x[j])
                centroCluster.append(y[j])
                
                distanciaDePuntoACentro = math.sqrt(((x[j] - varX)*(x[j] - varX)) + ((y[j] - varY)*(y[j] - varY)))
                
                distanciaDePuntoACircunferencia =  abs(distanciaDePuntoACentro - radios[j])
                
                
                gradosPertenencia.append(distanciaDePuntoACircunferencia)
                
                
                print("Distancia del punto:",i + 1,"a la circunferencia:",j + 1, distanciaDePuntoACircunferencia)
                
                
        print("Grados de Pertenencia del punto", punto, ":", gradosPertenencia)  
        
        #Normalizamos los valores
        
        denominador = sum(gradosPertenencia)
        
        for l in range(0, len(gradosPertenencia)):
            
            numerador = gradosPertenencia[l]/denominador

            gradosPertenenciaNormalizados.append(numerador)
            
            
        print("Grados de Pertenencia NORMALIZADOS del punto", punto, ":", gradosPertenenciaNormalizados)   
              
        #El punto pertenece al c�rculo con grado de menor valor      
        minpos = gradosPertenenciaNormalizados.index(min(gradosPertenenciaNormalizados))    
             
        print("El punto:", punto, "pertenece a la circunferencia:", minpos + 1)
         
        print("------------------------------------------------------------------------------------")
    
        gradosPertenenciaPorPuntos.append(gradosPertenenciaNormalizados)
        
    print("TODOS LOS GRADOS DE PERTENENCIA NORMALIZADOS POR PUNTOS:", gradosPertenenciaPorPuntos)

    representacionGrafica(x, y, radios)  
    
    print("SEGUNDA ITERACCI�N")
    
    

#AHORA HAY QUE REALIZAR N VECES UN ALGORITMO QUE APROXIME EL CENTRO A LOS PUNTOS


if __name__ == "__main__":

    buscandoAproximarLasCircunferencias()