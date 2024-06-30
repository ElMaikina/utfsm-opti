# pylint: disable=missing-module-docstring, missing-function-docstring, missing-class-docstring, line-too-long
from dataclasses import dataclass
from threading import Thread
import random
import time
from typing import Literal
import minizinc

from generator import generate_model_and_data

class CodeTimer:
    def __init__(self, name):
        self.name = name
        self.start_time = None
        self.end_time = None
        self._thread = Thread(target=self.debug)

    def debug(self):
        SLEEP_TIME = 15
        time.sleep(SLEEP_TIME)
        while self.end_time is None:
            print(f"Elapsed time '{self.name}': {self.elapsed_time // 1000:.0f} seconds")
            time.sleep(SLEEP_TIME)

    def start(self):
        self.start_time = time.time()
        self._thread.start()

    def stop(self):
        self._thread.join()
        self.end_time = time.time()

    @property
    def elapsed_time(self):
        if self.start_time is None:
            return None
        if self.end_time is None:
            return (time.time() - self.start_time)*1000
        return (self.end_time - self.start_time)*1000

    __enter__ = start
    def __exit__(self, exc_type, exc_value, traceback):
        self.stop()
        print(f"{self.name} elapsed time: {self.elapsed_time:.2f} ms")

@dataclass
class Instancia:
    """Parámetros de la instancia"""
    workers_range: tuple[int, int]
    tasks_range: tuple[int, int]
    size: Literal['small', 'medium', 'large']

    timer: CodeTimer = None

    _num_workers: int | None = None
    _num_tasks: int | None = None
    _budget: int | None = None

    def __post_init__(self):
        self.timer = CodeTimer(f"Instancia {self.size} {self.num_workers} trabajadores, {self.num_tasks} tareas")

    @property
    def num_workers(self) -> int:
        if self._num_workers is None:
            self._num_workers = random.randint(self.workers_range[0], self.workers_range[1])
        return self._num_workers

    @property
    def num_tasks(self) -> int:
        if self._num_tasks is None:
            self._num_tasks = random.randint(self.tasks_range[0], self.tasks_range[1])
        return self._num_tasks

    @property
    def budget(self) -> int:
        if self._budget is None:
            self._budget = random.randint(10_000 * self.num_workers * 2 // 3,
                                          10_000 * self.num_workers * 4 // 5)
        return self._budget

def solve_optimization(instancia: Instancia):
    generate_model_and_data(
        num_workers=instancia.num_workers,
        num_tasks=instancia.num_tasks,
        num_levels=8,
        P=instancia.budget,
        N=2,
    )

    # Crear un modelo MiniZinc
    model = minizinc.Model()
    model.add_file("model.mzn")
    model.add_file("data.dzn")

    # Crear una instancia del solucionador MiniZinc
    solver = minizinc.Solver.lookup("com.google.ortools.sat")

    # Resolver el modelo
    instance = minizinc.Instance(solver, model)

    with instancia.timer:
        result = instance.solve(processes=1000)

    # Imprimir los resultados
    print(f"x = {result['x']}")
    print(f"y = {result['y']}")

    return result


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

def print_as_csv():
    print("Tamaño, Trabajadores, Tareas, presupuesto, Tiempo de ejecución")
    for instancia in instancias:
        if instancia.timer.end_time is None:
            break
        print(instancia.size, end=", ")
        print(instancia.num_workers, end=", ")
        print(instancia.num_tasks, end=", ")
        print(instancia.budget, end=", ")
        print(instancia.timer.elapsed_time)

def main():
    try:
        for i, instancia in enumerate(instancias):
            print("\n"*2)
            print(f"Instancia {i+1}: {instancia.size} {instancia.num_workers} trabajadores, {instancia.num_tasks} tareas")

            t = solve_optimization(instancia)

            print(f"Tiempo de ejecución instancia tamaño {instancia.size} {i+1}: {t:.2f} ms\n\n")
            print()
            print_as_csv()
    except KeyboardInterrupt:
        print("Interrumpido por el usuario")
    finally:
        print_as_csv()

if __name__ == "__main__":
    main()
