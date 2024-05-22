import random

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

# Ejemplo de uso
generate_instance(5, 10, 100, 3)