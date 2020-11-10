from gurobipy import *
import numpy as np


def resolver_problema_generacion_columnas(tamano_items, tamano_materia_prima, demanda, error):
    """Funcion que ejecuta el algoritmo"""

    # 1º Se crea un patron de corte inicial ineficiente ( recordar que
    # no importa la solucion inicial, ya que no altera el tiempo de resolucion)

    patron = []
    m = len(tamano_items)

    for i, tamano in enumerate(tamano_items):
        pat = [0]*m
        pat[i] = int(tamano_materia_prima/tamano)
        patron.append(pat)

    # 2º Se genera el objeto y x_jiables necesarias para el ProblemaMaestro
    iteracion = 0
    K = len(patron)
    maestro = Model("Problema maestro")

    # 2.1º Se crea un diccionario donde la llave es el subindice de la variable X
    # y el valor es la variable de gurobi
    x = {}
    for k in range(K):
        # obj=1 indica que el a_ijiciente que le acompaña en la F.O. es 1
        x[k] = maestro.addVar(obj=1.0, vtype=GRB.INTEGER, name="x[%d]"%k)
    maestro.update()
    maestro.Params.OutputFlag = 0

    # 2.2º Se crea un diccrionario con las restricciones donde la llave es el subindice de
    # la restriccion de demanda asociada
    ordenes={}
    for i in range(m):
        a_ij = [patron[k][i] for k in range(K) if patron[k][i] > 0]
        x_j = [x[k] for k in range(K) if patron[k][i] > 0]
        ordenes[i] = maestro.addConstr(LinExpr(a_ij, x_j), ">", demanda[i], name="Orden de demanda[%d]"%i)
    maestro.update()

    # 3º Comienza el algoritmo
    while True:
        # 3.1º Se optimiza el problema maestro relajado
        iteracion +=1
        print("\n\nIteración:", iteracion)
        maestro_relajado = maestro.relax()
        maestro_relajado.optimize()
        print("Objetivo del maestro relajado:", maestro_relajado.ObjVal)

        # 3.2ª Se almacenan las variables duales para luego ser ocupadas
        # en el subproblema y se define este problema, cabe recordar que es un
        # problema de tipo knapsack y este se maximiza.
        pi = [c.Pi for c in maestro_relajado.getConstrs()]
        sub_problema = Model("Subproblema")
        sub_problema.ModelSense = -1

        # 3.3º Se crea un diccionario donde la llave es el subindice de la variable y
        # y el valor es la variable de gurobi
        y = {}
        for i in range(m):
            y[i] = sub_problema.addVar(obj=pi[i], lb=0, ub=demanda[i], vtype=GRB.INTEGER, name="y[%d]"%i)
        sub_problema.update()

        # 3.4º Se agrega la restriccion de capacidad asociada al problema dual
        L = LinExpr(tamano_items, [y[i] for i in range(m)])
        sub_problema.addConstr(L, "<", tamano_materia_prima, name="Tamaño materia prima")
        sub_problema.update()

        # 3.5º Se resuelve el subproblema
        sub_problema.Params.OutputFlag = 0
        sub_problema.optimize()

        print ("Objetivo del subproblema:", sub_problema.ObjVal)

        # 3.6º Se termina el problema si no hay mas columnas
        if sub_problema.ObjVal < 1+error: # break if no more columns
            break

        # 3.7º Si no se generan un nuevo patron de corte

        pat = [int(y[i].X+0.5) for i in y]
        patron.append(pat)

        # 3.8º Se agregan las nuevas columnas al problema maestro
        col = Column()
        for i in range(m):
            if patron[K][i] > 0:
                col.addTerms(patron[K][i], ordenes[i])

        # 3.9º Como se agrega una nueva columna se debe agregar una nueva variables asociada
        x[K] = maestro.addVar(obj=1, vtype=GRB.INTEGER, name="x[%d]"%K, column=col)
        maestro.update()
        K += 1

        print("Fin de la generacion de columnas")

        # 4º Se resueve el maestro nuevamente pero ocupando el maestro NO relajando
        # es decir se resuelve el problema entero.
        maestro.optimize()
        print("\n\n Valor objetivo final del problema:", maestro.ObjVal)
        print("Patrones:")
        for k in x:
            if x[k].X > error:
                print ("Patron:", k,)
                print ("\tTamaños:",)
                print ([tamano_items[i] for i in range(m) if patron[k][i]>0 for j in range(patron[k][i])],)
                print ("--> %d Rollos" % int(x[k].X+.5))

        # 5º Retornamos los rollos de materia cortados (Lo esperado del problema)
        rollos = []
        for k in x:
            for j in range(int(x[k].X + .5)):
                rollos.append(sorted([tamano_items[i] for i in range(m) if patron[k][i]>0 for j in range(patron[k][i])]))
        rollos.sort()
        return rollos


if __name__ == '__main__':

    np.random.seed(1)

    tamano_items = list()
    demanda = list()

    # Valores que se pueden modificar
    cantidad_de_piezas = 100
    tamano_materia_prima = 110
    valor_minimo_demanda = 10
    valor_maximo_demanda = 50
    error = 1.e-6

    for iter in range(5):
        tamano_items.append(np.random.randint(tamano_materia_prima))
        demanda.append(np.random.randint(valor_minimo_demanda, valor_maximo_demanda))

    rollos = resolver_problema_generacion_columnas(tamano_items, tamano_materia_prima, demanda)
