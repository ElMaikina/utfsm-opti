import matplotlib.pyplot as plt
import numpy as np
import random
import math
import time
from tabulate import tabulate
import csv

# Clase que contiene los atributos de Bodega
class Bodega:
    def __init__(self, capacidad, costo, coord, emision):
        self.capacidad = capacidad
        self.costo = costo
        self.coord = coord
        self.emision = emision

    def __str__(self):
        return f"Bodega - capacidad: {self.capacidad}, costo: {self.costo}, coordenadas: {self.coord}, emision: {self.emision}"

    def to_csv(self):
        return [self.capacidad, self.costo, self.coord, self.emision]

# Clase que contiene los atributos de Tienda
class Tienda:
    def __init__(self, coord):
        self.coord = coord

    def __str__(self):
        return f"Tienda - coordenadas: {self.coord}"

    def to_csv(self):
        return [self.coord]

# Revisa si se encuentra en las zonas interiores
def esta_en_celeste(x, y):
    if x in range(225, 375) and y in range(225, 375):
        return True
    return False

def esta_en_verde(x, y):
    if x in range(100, 500) and y in range(100, 500):
        return True
    return False

# Genera todas las coordenadas posibles
def generar_todas_las_coordenadas_bodegas():
    arreglo_coordenadas_totales = []
    for x in range(600):
        for y in range(600):
            if esta_en_celeste(x, y):
                continue
            arreglo_coordenadas_totales.append([x,y])

    return arreglo_coordenadas_totales

# Genera todas las coordenadas posibles
def generar_todas_las_coordenadas_tiendas():
    arreglo_coordenadas_totales = []
    for x in range(225, 375):
        for y in range(225, 375):
            arreglo_coordenadas_totales.append([x,y])

    return arreglo_coordenadas_totales

# Obtiene el costo de transporte
def costo_de_instalacion(x, y):
    if x in range(100, 500) and y in range(100, 500):
        return int(random.randint(1500,4000))
    return int(random.randint(1000,1500))

# Obtiene la emision por operacion
def emision_de_operacion():
    return random.randint(20,70)

# Costo dependiendo del color de la zona
def costo_zona_celeste():
    return int(random.randint(1000,1500))

def costo_zona_verde():
    return int(random.randint(1500,4000))

# Capacidad dependiendo del color de la zona
def funcion_capacidad(J):
    return int(random.randint(2, int(J/2)))

# Capacidad dependiendo del color de la zona
def funcion_emision():
    return int(random.randint(20, 70))

# Distancia desde la tienda a la bodega
def distancia(C_tiendas,C_bodegas):
    x1,y1 = C_tiendas
    x2,y2 = C_bodegas
    distancia = math.sqrt((x2-x1)**2+(y2-y1)**2)
    return round(distancia,2)




# Funcion principal del programa
if __name__ == '__main__':

    seed_value = 69
    random.seed(seed_value)

    I_inf = [5, 8, 13, 19, 24, 32, 39, 46, 54, 66, 72, 82, 92, 102, 112]
    I_sup = [7, 12, 18, 23, 30, 38, 45, 53, 65, 72, 81, 91, 101, 111, 131]

    J_inf = [6, 10, 20, 30, 40, 50, 65, 80, 95, 110, 125, 145, 165, 185, 205]
    J_sup = [10, 20, 30, 40, 50, 65, 80, 95, 110, 125, 145, 165,185 ,205 ,225]

    cada_cinco =0
    iteraciones =15

    print(f"Habra un total de {iteraciones} iteraciones...\n")
    # time.sleep(2)
    indice =0

    arreglo_coordenadas_totales_tiendas = generar_todas_las_coordenadas_tiendas()
    arreglo_coordenadas_totales_bodegas = generar_todas_las_coordenadas_bodegas()

    bodegas = []
    tiendas = []
    selec = 14
    while indice < iteraciones:

        bodegas = []
        tiendas = []
        if cada_cinco == 5:
            seed_value +=1
            cada_cinco =0
            random.seed(seed_value)
            print("\n----------------\n")

        I = random.randint(I_inf[indice], I_sup[indice])
        J = random.randint(J_inf[indice], J_sup[indice])

        # Genera el costo por zona aleatoriamente
        costo_celeste = costo_zona_celeste()
        costo_verde = costo_zona_verde()
        print(f"Costo por zona celeste: {costo_celeste}")
        print(f"Costo por zona verde: {costo_verde}")
        print(f"La emision maxima sera: {500 * J}")
        print(f"I: {I}")
        print(f"J: {J}")

        arreglo_tiendas = []
        cantidad_tiendas = J
        j =0
        while j < J:
            tienda = Tienda(random.choice(arreglo_coordenadas_totales_tiendas))
            arreglo_tiendas.append(tienda)
            tiendas.append(tienda) # Agrega la tienda a la lista de tiendas justo después de crearla
            j +=1

        print(f"\nCoordenas de las tiendas:")
        for tienda in arreglo_tiendas:
            print(tienda)


        arreglo_bodegas = []
        i=0
        while i < I:
            x,y= random.choice(arreglo_coordenadas_totales_bodegas)
            bodega = Bodega(funcion_capacidad(J), costo_de_instalacion(x,y), [x,y], funcion_emision())
            arreglo_bodegas.append(bodega)
            bodegas.append(bodega) # Agrega la bodega a la lista de bodegas justo después de crearla
            i +=1

        print(f"\nCoordenas de las bodegas:")
        for bodega in arreglo_bodegas:
            print(bodega)

        distancias_f=[]
        i=1
        for tienda in arreglo_tiendas:
            distancias=[]
            ac="J"+str(i)
            distancias.append(ac)
            for bodega in arreglo_bodegas:
                cordenas_t=tienda.coord
                cordenas_b=bodega.coord
                distancias.append(distancia(cordenas_t,cordenas_b))
            i +=1
            distancias_f.append(distancias)

        H=[" "]

        i=1
        while i<= len(arreglo_bodegas):
            H.append(("I"+str(i)))
            i +=1


        print("\nDistancias:\n")
        print(tabulate(distancias_f , headers=H))

        if selec == indice:
            with open('bodegas.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Capacidad", "Costo", "Coordenadas", "Emision"])
                for bodega in bodegas:
                    writer.writerow(bodega.to_csv())

            with open('tiendas.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Coordenadas"])
                for tienda in tiendas:
                    writer.writerow(tienda.to_csv())

        
    
        
        indice +=1
        cada_cinco +=1
        # time.sleep(1)




