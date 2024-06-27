import random

def main() -> int:
    # Parametros del modelo
    D = 0 # Cantidad de trabajadores
    C = 0 # Cantidad de tareas
    P = 0 # Presupuesto total

    # Matrices que contienen los costos asociados
    F = generar_costo_fijo(D, C) # Costo fijo por trabajador en cada tarea
    U = generar_costo_unit(D, C) # Costo unitario por hora para trabajador en cada tarea
    E = generar_nivel_esp(D, C) # Nivel de especializacion de trabajador en cada tarea
    T = generar_nivel_min(D, C) # Nivel minimo de especializacion en cada tarea

    # Arreglo de datos tanto para trabajadores como por tarea
    H = generar_cant_horas(C) # Horas minimas a cumplir por tarea
    M = generar_tareas_max(D) # Cantidad de tareas maximas por trabajador
    O = generar_costo_sobre(D) # Costo de sobrecalificacion por tarea


    return 0

if __name__ == '__main__':
    sys.exit(main())  # next section explains the use of sys.exit
