from dataclasses import dataclass
import random
from typing import Literal

# Clases

@dataclass
class Instancia:
    """Parámetros de la instancia"""
    num_workers: tuple[int, int]
    num_tasks: tuple[int, int]
    size: Literal['small', 'medium', 'large']

    def get_values(self) -> tuple[int, int]:
        """Devuelve una tupla con la cantidad de trabajadores y tareas de la instancia
        generada aleatoriamente con los rangos definidos en la instancia."""
        num_workers = random.randint(self.num_workers[0], self.num_workers[1])
        num_tasks = random.randint(self.num_tasks[0], self.num_tasks[1])
        return num_workers, num_tasks


@dataclass
class Task:
    """Clase Tarea"""
    index: int
    especializacion: int
    required_time: int


@dataclass
class Worker:
    """Clase Trabajador"""
    index: int
    especializacion: int
    costo_unidad_tiempo: int
    costo_fijo: list[int]
    sobrecalificacion_por_tarea: list[int]
    costo_por_sobrecalificacion: int
    tiempo_por_tarea: list[int]


# Constantes
N = 2  # Definido por el enunciado

instancias = [
    Instancia((10, 19), (5, 7), 'small'),
    Instancia((20, 29), (8, 12), 'small'),
    Instancia((30, 39), (13, 18), 'small'),
    Instancia((40, 49), (19, 23), 'small'),
    Instancia((50, 60), (24, 30), 'small'),
    Instancia((80, 104), (30, 44), 'medium'),
    Instancia((105, 129), (45, 59), 'medium'),
    Instancia((130, 154), (60, 74), 'medium'),
    Instancia((155, 179), (75, 89), 'medium'),
    Instancia((180, 205), (90, 105), 'medium'),
    Instancia((300, 359), (100, 139), 'large'),
    Instancia((360, 419), (140, 179), 'large'),
    Instancia((420, 479), (180, 219), 'large'),
    Instancia((480, 539), (220, 259), 'large'),
    Instancia((540, 600), (260, 300), 'large')
]

ESPECIALIZACION_WORKER = (1, 8, 8)
ESPECIALIZACION_TASK = (1, 8, 1)

WORKER_DISP_TIME = (400, 550, 10)  # Dependiente de N
TIME_PER_TASK = (30, 400, 10)  # Dependiente de N

WORKER_COST_RANGES = {
    1: (5, 10),
    2: (10, 15),
    3: (15, 20),
    4: (20, 25),
    5: (25, 30),
    6: (30, 35),
    7: (35, 40),
    8: (40, 45)
}


def get_worker_cost_per_time(specialization: int) -> int:
    """Obtener costo por unidad tiempo de un trabajador"""
    return random.randint(WORKER_COST_RANGES[specialization][0],
                          WORKER_COST_RANGES[specialization][1])


def get_budget(num_workers: int) -> int:
    """El presupuesto P debe tomar un número entre dos tercios del número de trabajadores
    por 10000 y cuatro quintos del número de trabajadores por 10000."""
    return random.randint(num_workers * 2 // 3 * 10_000, num_workers * 4 // 5 * 10_000)


def create_task(i: int) -> Task:
    """Crea una tarea con valores aleatorios."""
    especializacion = int(random.triangular(*ESPECIALIZACION_TASK))

    time_min, time_max, time_step = TIME_PER_TASK
    tiempo_por_tarea = random.randint(time_min // time_step, time_max // time_step) * time_step

    return Task(index=i,
                especializacion=especializacion,
                required_time=tiempo_por_tarea)

def create_worker(i: int, tasks: list[Task]) -> Worker:
    """Crea un trabajador con valores aleatorios."""
    especializacion = int(random.triangular(*ESPECIALIZACION_WORKER))

    costo_unidad_tiempo = get_worker_cost_per_time(especializacion)

    costo_fijo = [random.randint(4_000, 8_000)
                  for task in tasks]

    sobrecalificacion_por_tarea = [especializacion - task.especializacion
                                   for task in tasks]

    costo_por_sobrecalificacion = random.randint(10_000, 20_000)

    time_min, time_max, time_step = WORKER_DISP_TIME
    tiempo_por_tarea = [random.randint(time_min // time_step, time_max // time_step) * time_step
                        for _ in range(N)]

    return Worker(index=i,
                  especializacion=especializacion,
                  costo_unidad_tiempo=costo_unidad_tiempo,
                  costo_fijo=costo_fijo,
                  sobrecalificacion_por_tarea=sobrecalificacion_por_tarea,
                  costo_por_sobrecalificacion=costo_por_sobrecalificacion,
                  tiempo_por_tarea=tiempo_por_tarea)

def generate_instance(num_workers: int, num_tasks: int, *, file_name: str):
    """Genera una instancia con la cantidad de trabajadores y tareas especificadas."""
    print(f"Generando instancia con {num_workers} "
          f"trabajadores y {num_tasks} tareas")
    budget = get_budget(num_workers)

    tasks = [create_task(i)
             for i in range(num_tasks)]

    workers = [create_worker(i, tasks)
               for i in range(num_workers)]

    # Crear el archivo de datos .dzn
    with open(file_name, "w", encoding="utf-8") as f:
        f.write(f"num_workers = {num_workers};\n")
        f.write(f"num_tasks = {num_tasks};\n")
        f.write(f"P = {budget};\n")
        f.write(f"N = {N};\n")

        f.write("cost = [|")
        f.write("|".join(",".join(str(cost)
                                  for cost in worker.costo_fijo)
                         for worker in workers))
        f.write("|];\n")

        f.write("overqualification_cost = [|")
        f.write("|".join(",".join(str(worker.costo_por_sobrecalificacion)
                                  for _ in range(num_tasks))
                         for worker in workers))
        f.write("|];\n")


# Funcion principal
if __name__ == '__main__':
    # Muestra por pantalla el N actual
    print(f"Calculando con {N=}")

    for instancia in instancias:
        print()
        print(instancia)
        i, j = instancia.get_values()
        generate_instance(i,
                          j,
                          file_name=f"data_{instancia.size}_{i}-{j}.dzn")
