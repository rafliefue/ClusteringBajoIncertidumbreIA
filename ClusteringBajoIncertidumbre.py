#encoding:utf-8

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

def redondearCircunferencias(x, y, radios):
    
    xRed = []
    yRed = []
    radiosRed = []
    
    for i in range (0, len(radios)):
        newX = round(x[i], 1)
        newY = round(y[i], 1)
        newRadio = round(radios[i], 1)
        
        xRed.append(newX)
        yRed.append(newY)
        radiosRed.append(newRadio)
    
    return xRed, yRed, radiosRed 

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
    ax.set_xlim(-5,27)
    ax.set_ylim(-5,27)
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
    
    valorParada = 0.019
    
    sumGradosTotal = 10 #F1
    
    counter = 1
    
    
    while sumGradosTotal > valorParada:
        
        print("Ciclo", counter)
        print("========")
        
        condicion = True
        
        counter = counter + 1
        
        puntosPorCluster, gradosPorCluster = calculaGradosPertenencias(puntosCSV, x, y, radios, n_cluster)
        
        #CONDICIÓN DE PARADA
        for i in range(n_cluster):
            
            mediaGradosCluster = sum(gradosPorCluster[i])/(len(gradosPorCluster[i])) #F1
            
            sumGradosTotal =  sumGradosTotal + mediaGradosCluster #F1
          
        sumGradosTotal = sumGradosTotal/len(gradosPorCluster) #Esta es la media de grados juntando todos los cluster #F1
        
        if(n_cluster) == 1:
            
            sumGradosTotal = sumGradosTotal - 1
            valorParada = 10
        
        print("Valor de Condición de parada:", sumGradosTotal)
        print("------------------------------------------------------------------------------------")
        
        x, y, radios = nuevasCircunferencias(puntosCSV, puntosPorCluster, gradosPorCluster, n_cluster)
       
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
        
        isOk = True
           
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
    
    ventanaGen = tkinter.Tk()
    ventanaGen.title("Generador de Ejemplos")    
    ventanaGen.geometry("450x450")
    ventanaGen.config(bg='#FFD1A0')
    
    contenedor1 = tkinter.Label(ventanaGen, width = 64, height = 15, bg = "#FFD1A0").grid(row=0) #Para generar ejemplos aleatorios
    contenedor2 = tkinter.Label(ventanaGen, width = 64, height = 15, bg = "#FFBE79").grid(row=1) #Para generar ejemplos con solución conocida
    
    
      
    
    
    
       
if __name__ == "__main__":
    ventana_principal()
    #buscandoAproximarLasCircunferencias(3, 'C:/Users/Rafa/git/ClusteringBajoIncertidumbreIA/puntos3.csv')
    #generadorDeEjemplosEspecificos("ejemplo1",2,"(9,7), (2,6)","2, 4",5,20,False)
   
    