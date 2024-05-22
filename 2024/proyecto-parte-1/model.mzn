% assignment_model.mzn

int: num_workers; % Número de trabajadores
int: num_tasks; % Número de tareas
int: P; % Presupuesto total
int: N; % Máximo de tareas por trabajador

array[1..num_workers, 1..num_tasks] of int: cost; % Costo fijo por tarea
array[1..num_workers] of int: overqualification_cost; % Costo por sobrecalificación

% Variables de decisión
array[1..num_workers, 1..num_tasks] of var 0..1: x; % x[i,j] indica si el trabajador i realiza la tarea j

% Restricciones
constraint sum(i in 1..num_workers, j in 1..num_tasks)(x[i,j] * cost[i,j]) <= P; % Restricción de presupuesto
constraint forall(i in 1..num_workers)(sum(j in 1..num_tasks)(x[i,j]) <= N); % Restricción de máximo de tareas por trabajador

% Función objetivo: Minimizar el costo total
var int: total_cost = sum(i in 1..num_workers, j in 1..num_tasks)(x[i,j] * cost[i,j])
                    + sum(i in 1..num_workers)(overqualification_cost[i] * sum(j in 1..num_tasks)(x[i,j]));

solve minimize total_cost;

% Salida
output ["x=\(x)\n", "total_cost=\(total_cost)\n"];