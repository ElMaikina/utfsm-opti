# Funcion encargada de generar el modelo compatible en MiniZinc
def generate_mzn_model(num_trabajadores, num_tareas, presupuesto, max_tareas):
    filename="generated_model.mzn"
    model = """
    % Modelo de asignación de tareas a trabajadores

    int: num_workers; % Número de trabajadores
    int: num_tasks; % Número de tareas
    int: P; % Presupuesto total
    int: N; % Máximo de tareas por trabajador

    % Costos de asignación por tarea y trabajador
    array[1..num_workers, 1..num_tasks] of int: cost;

    % Costos por sobrecalificación por trabajador
    array[1..num_workers] of int: overqualification_cost;

    % Variables de decisión
    array[1..num_workers, 1..num_tasks] of var 0..1: x;

    % Restricciones
    constraint sum(i in 1..num_workers, j in 1..num_tasks)(x[i,j] * cost[i,j]) <= P;
    constraint forall(i in 1..num_workers)(sum(j in 1..num_tasks)(x[i,j]) <= N);

    % Asegurarse de que todos los costos se contabilizan
    var int: fixed_costs = sum(i in 1..num_workers, j in 1..num_tasks)(x[i,j] * cost[i,j]);
    var int: overqual_costs = sum(i in 1..num_workers)(overqualification_cost[i] * sum(j in 1..num_tasks)(x[i,j]));

    % Función objetivo: Minimizar el costo total
    var int: total_cost = fixed_costs + overqual_costs;

    solve minimize total_cost;

    % Salida
    output [
        "Asignaciones:\\n",
        "Trabajador -> Tareas\\n",
        concat([ show(i) ++ ": " ++ show([j | j in 1..num_tasks where fix(x[i,j]) == 1]) ++ "\\n" | i in 1..num_workers ]),
        "Costo total: ", show(total_cost), "\\n",
        "Costos fijos: ", show(fixed_costs), "\\n",
        "Costos por sobrecalificación: ", show(overqual_costs), "\\n"
    ];
    """

    with open(filename, "w") as f:
        f.write(model)
    
    print(f"Modelo MiniZinc generado y guardado en {filename}")

# Ejemplo de uso
generate_mzn_model()
