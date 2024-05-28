import minizinc

def solve_optimization():
    # Crear un modelo MiniZinc
    model = minizinc.Model()
    model.add_file("assignment_model.mzn")
    model.add_file("data.dzn")

    # Crear una instancia del solucionador MiniZinc
    gecode = minizinc.Solver.lookup("gecode")

    # Resolver el modelo
    with minizinc.Instance(gecode, model) as instance:
        result = instance.solve()

    # Imprimir los resultados
    print(f"x = {result['x']}")
    print(f"total_cost = {result['total_cost']}")

if __name__ == "__main__":
    solve_optimization()
