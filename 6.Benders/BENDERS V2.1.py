#
#  Código para Descomposición de Benders V2
#
# Autor: Moisés Saavedra
# Modificaciones y comentarios adicionales: Jorge Vera
#

from gurobipy import *
import numpy
import time

# Se setea que opcion de resolucion ocupar
opcion = int(input("Ingresa 0 para no ocupar Benders, \ncualquier otra tecla para usar Benders: "))
if opcion == 0:
    no_benders = True
else:
    no_benders = False


######################################
#   Invencion de parametros base     #
######################################

numpy.random.seed(1)

#Numero de depositos
n = 30
N = range(n)
NITERACIONES = 100


# Parametros
q = numpy.random.randint(400000, 1000000, (n,n))
c = numpy.random.randint(400,500, (n,n))
s = numpy.random.randint(1000, 2000, n)
d = numpy.random.randint(1000, 2000, (n,n))

########################################
#  Opimiza deterministico equivalente  #
# (modelo resuleto sin ocupar BENDERS) #
########################################
if no_benders:
    deterministico = Model()
    deterministico.Params.Threads = 1

    # Generacion de variables
    x = deterministico.addVars(N, N, vtype=GRB.CONTINUOUS, lb=0)
    y = deterministico.addVars(N, N, vtype=GRB.CONTINUOUS, lb=0)

    # Generacion de restricciones
    R1 = deterministico.addConstrs(
        (quicksum(x[ii, jj] for jj in N if jj!=ii) <= s[ii]) for ii in N
    )

    R2 = deterministico.addConstrs(
        (quicksum(y[ii, jj] for jj in N if jj!=ii) <= s[ii] + quicksum(x[ll, ii] for ll in N if ll!=ii) - quicksum(x[ii, ll] for ll in N if ll!=ii)) for ii in N
    )

    R3 = deterministico.addConstrs(
        (y[ii, jj] <= d[ii][jj]) for ii in N for jj in N if jj!=ii
    )

    # Generacion de funcion objetivo
    deterministico.setObjective(
        quicksum(quicksum(q[ii][jj]*y[ii,jj] - c[ii][jj]*x[ii,jj] for jj in N if jj!=ii) for ii in N),
        GRB.MAXIMIZE
    )

    # Optimiza el equivalente
    inicio = time.time()
    deterministico.update()
    deterministico.optimize()
    final = time.time()

    print("Valor objetivo - Tiempo de resolucion ")
    print(deterministico.objVal, "   -   ", deterministico.Runtime)

else:
    ########################################
    #   Inicia  Descomposicion Benders
    #########################################

    # Define problema maestro
    maestro = Model()
    maestro.Params.OutputFlag = 0

    # Generacion de variables
    xm = maestro.addVars(N, N, vtype=GRB.CONTINUOUS, lb=0)
    theta = maestro.addVar(vtype=GRB.CONTINUOUS)

    # Generacion de restricciones
    R1m = maestro.addConstrs(
        (quicksum(xm[i,j] for j in N if j!=i) <= s[i]) for i in N
    )
    # Esta restricción es artifical, solo para excluir las variables x(i,i)
    R2m = maestro.addConstrs(
        (xm[i,i] == 0) for i in N
    )

    # Generacion de funcion objetivo
    # En la primera iteración necesitamos el maestro como problema en variables x, sin theta.
    # Esto produce una solución factible para la primera etapa, para poder iniciar el ciclo.
    #

    # Generacion de funcion objetivo
    maestro.setObjective(
        - quicksum(quicksum(c[i,j]*xm[i,j] for j in N if j!=i) for i in N),
        GRB.MINIMIZE
    )

    


    # *********************************************************************************

    ##### Definicion de subproblema ####
    # 
    # En este caso el problema satélite se usa en forma primal directamente.
    # Entonces, lo que se usa en la iteración son las VARIABLES DUALES del satélite, esas
    # generan el corte.
    #
    subproblema = Model()
    subproblema.Params.OutputFlag = 0

    # Generacion de variables
    ysub = subproblema.addVars(N, N, vtype=GRB.CONTINUOUS, lb=0)

    # Generacion de restricciones
    R1sub = subproblema.addConstrs(
        (quicksum(ysub[i,j] for j in N if j!=i) <= 0) for i in N
    )

    R2sub = subproblema.addConstrs(
        (ysub[i,j] <= d[i,j]) for i in N for j in N if j!=i
    )

    # Esta restricción es artifical, solo para excluir las variables ysub(i,i)
    R3sub = subproblema.addConstrs(
        (ysub[i,i] == 0) for i in N
    )

    # Genera funcion objetivo
    subproblema.setObjective(
        quicksum(quicksum(q[i,j]*ysub[i,j] for j in N if j!=i) for i in N),
        GRB.MAXIMIZE
    )

    subproblema.update()

    ##################################
    #         Ciclo Benders          #
    ##################################

    print("")
    print("---------- CICLOS BENDERS-------------")
    print("")
    print("Ciclo - Master - Subproblema")
    inicio = time.time()
    contador = 0
    lista = []

    # Se inician las iteracion controladas
    FOold = 0
    while contador <= NITERACIONES:
        contador += 1

        # Resuelve el modelo maestro
        maestro.update()
        maestro.optimize()

        # Se crean las variables duales para cada iteracion asociada
        pi_R1 = numpy.zeros((n))
        pi_R2 = numpy.zeros((n, n))

        # Actualizacion de restricciones segun lo calculado en el maestro
        for i in N:
            R1sub[i].rhs = (s[i] + sum((xm[j,i].X - xm[i,j].X) for j in N if j!=i))

        # Optimizacion del subproblema satélite.
        # Recordar que se resuleve el primal en las variables y directamente.        subproblema.update()
        subproblema.optimize()

        # Acumula el valor en la FO
        FO = maestro.objVal
        print(contador, "/", maestro.objVal, "/", subproblema.objVal)
        lista.append(FO)

        # Condicion de quiebre de BENDERE
#        if 0.001 >= abs(1-(FO)/(FO + 0.1)):
#            print("**** Termino por convergencia ****")
#            break

        # Se cargan las variables duales
        for i in N:
            pi_R1[i] = R1sub[i].Pi
        for i in N:
            for j in N:
                if j!=i: pi_R2[i,j] = R2sub[i,j].Pi

       
        # Si es factible agrega corte de optimalidad
        maestro.addConstr(
            quicksum(s[i] * pi_R1[i] for i in N)
            + quicksum(quicksum(xm[l, i] * pi_R1[i] for l in N if i != l) for i in N)
            - quicksum(quicksum(xm[i, n] * pi_R1[i] for n in N if i != n) for i in N)
            + quicksum(quicksum(d[i, j] * pi_R2[i, j] for j in N if i != j) for i in N) >= theta
        )

        maestro.setObjective(
        theta + quicksum(quicksum(-c[i,j]*xm[i,j] for j in N if j!=i) for i in N),
        GRB.MAXIMIZE
        )

    final = time.time()
    print("")
    print(" Tiempo de ejecucion:", (final - inicio))