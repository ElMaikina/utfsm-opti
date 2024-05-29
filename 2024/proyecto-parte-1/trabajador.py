# Al crear un Trabajador se le asignan sus restricciones
# y el arreglo de Tiempo por Tarea (txt) que le indica 
# cuanto tiempo le toma cada tarea

# Los parametros se asignaran aleatoriamente 
# desde el Generador
class Trabajador:
    def __init__(self, esp, cxut, cf, txt):
        self.especializacion = esp
        self.costo_unidad_tiempo = cxut
        self.costo_fijo = cf
        self.tiempo_por_tarea = txt
