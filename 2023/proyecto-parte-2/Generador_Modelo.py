import pandas as pd
import minizinc
import ast
import time

def calcular_costos_transporte(bodegas, tiendas):
    costos_transporte = []
    for i in range(len(bodegas)):
        costos_bodega = []
        for j in range(len(tiendas)):
            distancia = ((bodegas.loc[i, "Coordenada_x"] - tiendas.loc[j, "Coordenada_x"])**2 +
                         (bodegas.loc[i, "Coordenada_y"] - tiendas.loc[j, "Coordenada_y"])**2)**0.5
            costo_transporte = 1.25 * distancia
            costo_transporte = int(costo_transporte)
            costos_bodega.append(costo_transporte)
        costos_transporte.append(costos_bodega)
    return costos_transporte

# Leer los datos de los archivos CSV
bodegas = pd.read_csv('bodegas.csv')
tiendas = pd.read_csv('tiendas.csv')

# Convertir las coordenadas a listas de números
bodegas["Coordenadas"] = bodegas["Coordenadas"].apply(ast.literal_eval)
tiendas["Coordenadas"] = tiendas["Coordenadas"].apply(ast.literal_eval)

# Dividir las coordenadas en dos columnas separadas
bodegas[["Coordenada_x", "Coordenada_y"]] = pd.DataFrame(bodegas["Coordenadas"].to_list(), index=bodegas.index)
tiendas[["Coordenada_x", "Coordenada_y"]] = pd.DataFrame(tiendas["Coordenadas"].to_list(), index=tiendas.index)

# Calcular los costos de transporte
costo_transporte = calcular_costos_transporte(bodegas, tiendas)

# Crear el modelo MiniZinc
modelo = minizinc.Model()
modelo.add_string("""
% Declaración de parámetros
int: num_bodegas;
int: num_tiendas;
array[1..num_bodegas] of int: costo_instalacion;
array[1..num_bodegas, 1..num_tiendas] of float: costo_transporte;
array[1..num_bodegas] of int: capacidad_bodegas;  % Capacidad de cada bodega
int: limite_emisiones;  % Límite de emisiones
array[1..num_bodegas] of int: emisiones;

% Variables de decisión
array[1..num_bodegas] of var 0..1: bodegas_seleccionadas;
array[1..num_bodegas, 1..num_tiendas] of var 0..1: bodegas_satisfacen_tiendas;

% Restricciones
constraint forall(i in 1..num_tiendas)(
    sum(j in 1..num_bodegas)(bodegas_satisfacen_tiendas[j, i]) = 1
);
constraint forall(i in 1..num_bodegas)(
    sum(j in 1..num_tiendas)(bodegas_satisfacen_tiendas[i, j]) <= bodegas_seleccionadas[i] * num_tiendas
);
% Cada bodega debe satisfacer una cantidad de tiendas igual o menor a su capacidad
constraint forall(i in 1..num_bodegas)(
    sum(j in 1..num_tiendas)(bodegas_satisfacen_tiendas[i, j]) <= capacidad_bodegas[i]
);
% Restricción de emisiones
constraint sum(i in 1..num_bodegas, j in 1..num_tiendas)(
    bodegas_satisfacen_tiendas[i, j] * emisiones[i]
) <= limite_emisiones;

% Función objetivo
var float: costo_total = 
    sum(i in 1..num_bodegas)(costo_instalacion[i] * bodegas_seleccionadas[i]) +
    sum(i in 1..num_bodegas, j in 1..num_tiendas)(costo_transporte[i, j] * bodegas_satisfacen_tiendas[i, j]);

% Resolución
solve minimize costo_total;


""")

costo_transporte = calcular_costos_transporte(bodegas, tiendas)
# Crear una instancia del modelo con los datos

instancia = minizinc.Instance(minizinc.Solver.lookup("coin-bc"), modelo)
instancia["num_bodegas"] = len(bodegas)
instancia["num_tiendas"] = len(tiendas)
instancia["costo_instalacion"] = list(bodegas["Costo"])
instancia["emisiones"] = list(bodegas["Emision"])
instancia["costo_transporte"] = costo_transporte
instancia["limite_emisiones"] = 500 * len(tiendas)
instancia["capacidad_bodegas"] = list(bodegas["Capacidad"])


# Resolver la instancia y obtener la solución
inicio = time.time()
solucion = instancia.solve()
fin = time.time()
print(solucion)
print(fin-inicio)
