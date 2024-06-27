import random

















def generate_model_and_data(num_workers, num_tasks, num_levels, P, N, model_filename="assignment_model.mzn", data_filename="data.dzn"):
    # Generar el modelo MiniZinc
    with open(model_filename, "w") as f:
        f.write("""
% Modelo de asignación de trabajadores a tareas

int: num_workers; % Número de trabajadores
int: num_tasks; % Número de tareas
int: num_levels; % Número de niveles de especialización
int: P; % Presupuesto total
int: N; % Máximo de tareas por trabajador
float: max_worker_fraction = 2/3; % Máximo de trabajadores asignados a una sola tarea (en fracción)

% Matriz de costos fijos por asignación (trabajador i a tarea j)
array[1..num_workers, 1..num_tasks] of int: fixed_cost;

% Matriz de costos por unidad de tiempo (trabajador i a tarea j)
array[1..num_workers, 1..num_tasks] of int: time_cost;

% Tiempo necesario para completar cada tarea
array[1..num_tasks] of int: task_time;

% Tiempo máximo que cada trabajador puede ser asignado
array[1..num_workers] of int: max_worker_time;

% Niveles de especialización de los trabajadores (nivel de cada trabajador)
array[1..num_workers] of int: worker_level;

% Niveles de especialización requeridos por las tareas (nivel de cada tarea)
array[1..num_tasks] of int: task_level;

% Variables de decisión: x[i,j] indica si el trabajador i es asignado a la tarea j
array[1..num_workers, 1..num_tasks] of var 0..1: x;

% Variables auxiliares: tiempo asignado de cada trabajador a cada tarea
array[1..num_workers, 1..num_tasks] of var 0..task_time[j]: y;

% Restricciones

% Todos los costos fijos de asignación no pueden superar el presupuesto
constraint sum(i in 1..num_workers, j in 1..num_tasks)(x[i,j] * fixed_cost[i,j]) <= P;

% Restricción de que cada trabajador no puede realizar más de N tareas
constraint forall(i in 1..num_workers)(sum(j in 1..num_tasks)(x[i,j]) <= N);

% Restricción de tiempo máximo de cada trabajador
constraint forall(i in 1..num_workers)(sum(j in 1..num_tasks)(y[i,j]) <= max_worker_time[i]);

% Cada tarea debe ser completada completamente por uno o más trabajadores
constraint forall(j in 1..num_tasks)(sum(i in 1..num_workers)(y[i,j]) >= task_time[j]);

% No más de dos tercios de los trabajadores pueden estar asignados a una sola tarea
constraint forall(j in 1..num_tasks)(
    sum(i in 1..num_workers)(x[i,j]) <= ceil(max_worker_fraction * num_workers)
);

% Asignación permitida sólo si el trabajador tiene el nivel de especialización adecuado o superior
constraint forall(i in 1..num_workers, j in 1..num_tasks)(
    x[i,j] = 1 -> worker_level[i] >= task_level[j]
);

% Si un trabajador es asignado a una tarea, el tiempo asignado debe ser mayor que cero
constraint forall(i in 1..num_workers, j in 1..num_tasks)(
    x[i,j] = 1 -> y[i,j] > 0
);

% Costos por sobrecalificación
var int: overqual_costs = sum(i in 1..num_workers, j in 1..num_tasks)(
    x[i,j] * max(0, worker_level[i] - task_level[j])
);

% Costos totales fijos y de tiempo
var int: total_fixed_costs = sum(i in 1..num_workers, j in 1..num_tasks)(x[i,j] * fixed_cost[i,j]);
var int: total_time_costs = sum(i in 1..num_workers, j in 1..num_tasks)(y[i,j] * time_cost[i,j]);

% Función objetivo: Minimizar el costo total (fijo y por unidad de tiempo)
var int: total_cost = total_fixed_costs + total_time_costs + overqual_costs;

solve minimize total_cost;

% Salida
output [
    "Asignaciones:\\n",
    "Trabajador -> Tareas\\n",
    concat([ show(i) ++ ": " ++ show([j | j in 1..num_tasks where fix(x[i,j]) == 1]) ++ "\\n" | i in 1..num_workers ]),
    "Costo total: ", show(total_cost), "\\n",
    "Costos fijos: ", show(total_fixed_costs), "\\n",
    "Costos por unidad de tiempo: ", show(total_time_costs), "\\n",
    "Costos por sobrecalificación: ", show(overqual_costs), "\\n"
];
""")

    print(f"Modelo MiniZinc generado y guardado en {model_filename}")

    # Generar los datos de la instancia
    worker_level = [random.randint(1, num_levels) for _ in range(num_workers)]
    task_level = [random.randint(1, num_levels) for _ in range(num_tasks)]
    fixed_cost = [[random.randint(1, 20) for _ in range(num_tasks)] for _ in range(num_workers)]
    time_cost = [[random.randint(1, 10) for _ in range(num_tasks)] for _ in range(num_workers)]
    task_time = [random.randint(10, 50) for _ in range(num_tasks)]
    max_worker_time = [random.randint(30, 100) for _ in range(num_workers)]

    # Crear el archivo de datos .dzn
    with open(data_filename, "w") as f:
        f.write(f"num_workers = {num_workers};\n")
        f.write(f"num_tasks = {num_tasks};\n")
        f.write(f"num_levels = {num_levels};\n")
        f.write(f"P = {P};\n")
        f.write(f"N = {N};\n")

        f.write("worker_level = [")
        f.write(", ".join(map(str, worker_level)))
        f.write("];\n")

        f.write("task_level = [")
        f.write(", ".join(map(str, task_level)))
        f.write("];\n")

        f.write("fixed_cost = array2d(1..num_workers, 1..num_tasks, [")
        for i in range(num_workers):
            for j in range(num_tasks):
                f.write(f"{fixed_cost[i][j]}")
                if i < num_workers - 1 or j < num_tasks - 1:
                    f.write(", ")
        f.write("]);\n")

        f.write("time_cost = array2d(1..num_workers, 1..num_tasks, [")
        for i in range(num_workers):
            for j in range(num_tasks):
                f.write(f"{time_cost[i][j]}")
                if i < num_workers - 1 or j < num_tasks - 1:
                    f.write(", ")
        f.write("]);\n")

        f.write("task_time = [")
        f.write(", ".join(map(str, task_time)))
        f.write("];\n")

        f.write("max_worker_time = [")
        f.write(", ".join(map(str, max_worker_time)))
        f.write("];\n")

    print(f"Datos de instancia generados y guardados en {data_filename}")


#generate_model_and_data(5, 8, 5, 300, 3)

# Uso del generador
