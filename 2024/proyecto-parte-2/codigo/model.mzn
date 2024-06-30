
% Número de trabajadores
int: num_workers;

% Número de tareas
int: num_tasks;

% Número de niveles de especialización
int: num_levels;

% Presupuesto total
int: P;

% Máximo de tareas por trabajador
int: N;

% Costo fijo de asignar al trabajador i a la tarea j
array[1..num_workers, 1..num_tasks] of int: fixed_cost;

% Costo por unidad de tiempo del trabajador i para la tarea j
array[1..num_workers, 1..num_tasks] of int: time_cost;

% Tiempo necesario para completar cada tarea j
array[1..num_tasks] of int: task_time;

% Tiempo máximo que cada trabajador i puede ser asignado
array[1..num_workers] of int: max_worker_time;

% Nivel de especialización de cada trabajador i
array[1..num_workers] of int: worker_level;

% Nivel de especialización requerido por cada tarea j
array[1..num_tasks] of int: task_level;

% Variables de decisión: x[i, j] indica si el trabajador i está asignado a la tarea j
array[1..num_workers, 1..num_tasks] of var 0..1: x;

% Variables auxiliares: tiempo que cada trabajador i dedica a la tarea j
array[1..num_workers, 1..num_tasks] of var 0..max(task_time): y;

% Restricciones

% 1. Presupuesto total
constraint sum(i in 1..num_workers, j in 1..num_tasks)(x[i, j] * fixed_cost[i, j]) <= P;

% 2. Máximo de tareas por trabajador
constraint forall(i in 1..num_workers)(sum(j in 1..num_tasks)(x[i, j]) <= N);

% 3. Tiempo máximo de trabajo por trabajador
constraint forall(i in 1..num_workers)(sum(j in 1..num_tasks)(y[i, j]) <= max_worker_time[i]);

% 4. Completar todas las tareas
constraint forall(j in 1..num_tasks)(sum(i in 1..num_workers)(y[i, j]) >= task_time[j]);

% 5. Límite de trabajadores por tarea
constraint forall(j in 1..num_tasks)(sum(i in 1..num_workers)(x[i, j]) <= ceil(2.0 / 3.0 * num_workers));

% 6. Nivel de especialización adecuado
constraint forall(i in 1..num_workers, j in 1..num_tasks)(
    x[i, j] = 1 -> worker_level[i] >= task_level[j]
);

% 7. Consistencia entre asignación y tiempo
constraint forall(i in 1..num_workers, j in 1..num_tasks)(
    x[i, j] = 1 -> y[i, j] > 0
);

constraint forall(i in 1..num_workers, j in 1..num_tasks)(
    y[i, j] > 0 -> x[i, j] = 1
);

% 8. Sobrecualificación y costos totales
var int: overqual_costs = sum(i in 1..num_workers, j in 1..num_tasks)(
    x[i, j] * max(0, worker_level[i] - task_level[j])
);

var int: total_fixed_costs = sum(i in 1..num_workers, j in 1..num_tasks)(x[i, j] * fixed_cost[i, j]);
var int: total_time_costs = sum(i in 1..num_workers, j in 1..num_tasks)(y[i, j] * time_cost[i, j]);

var int: total_cost = total_fixed_costs + total_time_costs + overqual_costs;

solve minimize total_cost;

% Salida
output [
    "Asignaciones: ",
    ", Trabajador -> Tareas",
    concat([ show(i) ++ ": " ++ show([j | j in 1..num_tasks where fix(x[i,j]) == 1]) ++ "\n" | i in 1..num_workers ]),
    ", Costo total: ", show(total_cost),
    ", Costos fijos: ", show(total_fixed_costs),
    ", Costos por unidad de tiempo: ", show(total_time_costs),
    ", Costos por sobrecalificación: ", show(overqual_costs),
];
