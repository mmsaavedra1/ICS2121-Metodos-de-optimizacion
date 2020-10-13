#!/usr/bin/python

from gurobipy import *
import numpy as np
import scipy.linalg

from leerExcel import importar_excel


def timer(funcion):
    """
    Se crea un decorador (googlear) del tipo timer para testear el tiempo
    de ejecucion del programa
    """
    def inner(*args, **kwargs):

        inicio = time.time()
        resultado = funcion(*args, **kwargs)
        final = round(time.time() - inicio, 3)
        print("\nTiempo de ejecucion total: {}[s]".format(final))

        return resultado
    return inner

def FW(A, b, rho, iteracion_maxima):
    """
    Esta funcion recibe como input una matriz A y un vector b. Se busca resolver
    el problema de regulacion L1 con un parametro rho, en la formulación
    auxiliar para usar el algoritmo de Frank-Wolfe.

    Su entrada posee:
        - A : Matriz de m muestras (filas) de cada variable n (columnas).
        - b : Matriz de m muestras obtenidas que depende de las n variables.
        - rho: Escalar que limita ||x||_1.
        - iteracion_maxima : Numero maximo de iteraciones a realizar.

    Su salida es:
        - valor_optimo : Valor optimo del problema a minimizar.
        - xk : Vector solucion del problema de k iteraciones."""

    # Se setean las dimensiones
    m, n = A.shape
    N = range(n)
    
    norma_b = np.linalg.norm(b)

    # Se crea ek modelo lineal y se setean las variables y restricciones
    
    fw = Model("PL auxiliar de Frank-Wolfe")
    
    fw.setParam(GRB.Param.OutputFlag, 0)
    
    # variables
    y = fw.addVars(N,lb=-GRB.INFINITY,ub=GRB.INFINITY)
    z = fw.addVars(N,lb=0,ub=GRB.INFINITY)
    
    # Restricciones
    fw.addConstr(quicksum(z[j] for j in N) <= rho)
    fw.addConstrs((-z[j] <= y[j]) for j in N)
    fw.addConstrs((y[j] <= z[j]) for j in N)
    
    # Se setean las condiciones iniciales, junto a los vectores que almacenand
    # informacion de la iteracion k, k-1, k-2, respectivamente.
    xk = np.zeros((n, 1))


    # La sucesion thetak se setea simplemente como 1 y se modifica en cada iteración (ver el código))
    thetak = 1


    # Se calcula el valor optimo actual en la iteracion 0
    valor_optimo = np.linalg.norm(np.dot(A, xk) - b)**2


    # Se despliega el mensaje en pantalla
    print("\n\n**********    METODO FISTA    *********\n")
    print("ITERACION     VALOR OBJ      ERROR AJUSTE  ||x||_1")

    errores = list()

    # Se comienza el ciclo de iteraciones
    for iteracion in range(iteracion_maxima):
        # Se determina el gradiente en la iteración actual.

        grad =  2*np.dot(np.transpose(A), np.dot(A, xk) - b) 

        # Se actualiza la función objetivo del problema lineal
        fw.setObjective(sum((grad[j,0]*y[j]) for j in N), GRB.MINIMIZE)
        # Se resuelve
        fw.optimize()
        # 5º Se actualiza la sucesion thetak 

        thetak = 2/(2+iteracion)

        # Se actualiza el punto solución actual
        
        for j in N:
            xk[j] = xk[j] + thetak*(y[j].X - xk[j])
            
        # 6º Se actualiza el valor objetivo
        valor_optimo = np.linalg.norm(np.dot(A, xk) - b)**2

        # 7º Se calcula el error (segun norma infito de b) para mostrar en pantalla.
        error = np.linalg.norm(np.dot(A, xk) - b)/norma_b
        errores.append(error)

        # Se calcula ||xk||_1 
        n1 = np.linalg.norm(xk, 1)
        

         # La rutina FW muestra en pantalla para cada iteracion:
        # nº de iteracion, valor de la funcion evaluada en el x de la iteracion,
        #  error y angulo formado por las soluciones.
        retorno_en_pantalla = [iteracion, valor_optimo, error, n1]
#        print(f"{retorno_en_pantalla[0]: ^12d}{retorno_en_pantalla[1]: ^12f} {retorno_en_pantalla[2]: ^12f} {retorno_en_pantalla[3]: ^12f}")
        print("%12.6f %12.6f %12.6f %12.6f" % (retorno_en_pantalla[0],retorno_en_pantalla[1],retorno_en_pantalla[2],retorno_en_pantalla[3]))

    return xk, errores

if __name__ == '__main__':
    # Esto es para que simepre se generen los mismos numeros aleatorios
    np.random.seed(1000)

    rho = 1000
    iteracion_maxima = 1000
    
    # Esta rutina tiene que ser reemplazada si se quiere leer 
    # datos externos.
    #A, b = generar_datos(300, 1500)
    A, b = importar_excel()
    
    xsol, errores = FW(np.array(A), np.array(b), rho, iteracion_maxima)
    
    import matplotlib
    import matplotlib.pyplot as plt


    fig, ax = plt.subplots()
    ax.plot(range(iteracion_maxima), errores)

    ax.set(xlabel='Iteracion', ylabel='Error',
        title='Análisis de convergencia del error')
    ax.grid()

    fig.savefig("[FW] Convergencia del error.png")
    plt.show()
