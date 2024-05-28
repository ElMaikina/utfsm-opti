import random
import sys

def generate_instance(num_workers, num_tasks, P, N):
    # Generar costos fijos y costos por sobrecalificación aleatoriamente
    cost = [[random.randint(1, 10) for _ in range(num_tasks)] for _ in range(num_workers)]
    overqualification_cost = [random.randint(1, 5) for _ in range(num_workers)]

    # Crear el archivo de datos .dzn
    with open("data.dzn", "w") as f:
        f.write(f"num_workers = {num_workers};\n")
        f.write(f"num_tasks = {num_tasks};\n")
        f.write(f"P = {P};\n")
        f.write(f"N = {N};\n")
        
        f.write("cost = [|")
        for i in range(num_workers):
            f.write(",".join(map(str, cost[i])))
            if i < num_workers - 1:
                f.write("|")
        f.write("|];\n")
        
        f.write("overqualification_cost = [")
        f.write(",".join(map(str, overqualification_cost)))
        f.write("];\n")

# Funcion principal
if __name__ == '__main__':
    
    # Valores de N a evaluar
    N = [1, 2, 3, 4]

    # Cantidad de instancias
    cant_instancias = 15

    I = [ \
        [10, 19], \
        [20, 29], \
        [30, 39], \
        [40, 49], \
        [50, 60], \
        [80, 104], \
        [105, 129], \
        [130, 154], \
        [155, 179], \
        [180, 205], \
        [300, 359], \
        [360, 419], \
        [420, 479], \
        [480, 539], \
        [540, 600] \
    ]

    J = [ \
        [5, 7], \
        [8, 12], \
        [13, 18], \
        [19, 23], \
        [24, 30], \
        [30, 44], \
        [45, 59], \
        [60, 74], \
        [75, 89], \
        [90, 105], \
        [100, 139], \
        [140, 179], \
        [180, 219], \
        [220, 259], \
        [260, 300] \
    ]
    # Rango de nivel de especializacion
    esp_worker_min = 1
    esp_worker_max = 8
    esp_worker_mod = 8
    
    # Rango de nivel de especializacion
    esp_task_min = 1
    esp_task_max = 8
    esp_task_mod = 8

    # Tiempo disponible por trabajador
    time_disp_min = 300
    time_disp_max = 450

    for n in N:
        match n:

            # Establece los tiempos disponibles a partir de la seccion
            # de Creacion de Parametros en el PDF
            case 1:
                time_disp_min = 300
                time_disp_max = 450
            case 2:
                time_disp_min = 400
                time_disp_max = 550
            case 3:
                time_disp_min = 500
                time_disp_max = 650
            case 4:
                time_disp_min = 600
                time_disp_max = 750
        
        # Muestra por pantalla el N actual
        print("Calculando para N = " + str(n))

        # Para cada N genera un I y J
        for i in range(cant_instancias):
            print("Rangos para I = " + str(I[i]))
            print("Rangos para J = " + str(J[i]))

            # Obtener valores a partir de los rangos obtenidos

            # Modificar para que tome los valores generados
            generate_instance(5, 10, 100, 3)

    sys.exit()