# -*- coding: utf-8 -*-
__author__ = "Moises Saavedra Caceres & Jorge Vera"
__email__ = "mmsaavedra1@ing.puc.cl"


# Modulos nativos de python
import numpy as np
import time
import scipy.optimize

# Modulo creado por nosotros (parametros.py)
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

def subrutina(vars, X, Y):
    """
    Esta funcion debe retornar el valor de la funcion, su gradiente segun
    la iteracion estudiada.
    """
    # Dimensiones de la matriz ingresada
    m, k = (55, 5)

    """  IMPLEMENTADO  """
    # Se crean las variables que ayudan a definir la funcion principal
    # para este caso el vector que solo posee valor en coordenada n
    # y la matriz que posee valor en coordenada en fila m y coordenada n
    # ademas del valor del real alpha

    var_alfa = vars[:5]
    var_beta = vars[5:]
    # Funcion a calcular
    funcion_objetivo = 0

    suma_i = 0
    for i in range(0, m):
        suma_j = 0
        for j in range(0, k):
            suma_j += var_beta[j]*(X[i][j]**var_alfa[j])
        suma_i += (suma_j - Y[i])**2

    funcion_objetivo = suma_i/(2*m)
    """  IMPLEMENTADO  """


    return funcion_objetivo[0]

"""  IMPLEMENTADO  """
global soluciones
soluciones = list()

def graficar(xk):
    """
    Se almancenan los valores en xk para cada iteracion para luego ser graficados
    """
    soluciones.append(xk)

 
def calcular_convergencia(x, x_optimo):
    limites = list()

    for i in range(1, len(x)):
        x_k = x[i]
        x_k_menos_1 = x[i-1]
        norma_numerador = np.linalg.norm(x_k - x_optimo, 2)
        norma_denominador = np.linalg.norm(x_k_menos_1 - x_optimo, 2)
        limite = norma_numerador/norma_denominador
        limites.append(limite)

    iteraciones = range(1, len(x))

    import matplotlib
    import matplotlib.pyplot as plt


    fig, ax = plt.subplots()
    ax.plot(iteraciones, limites)

    ax.set(xlabel='Iteracion', ylabel='Error de soluciones',
        title='[BFGS] Convergencia de las soluciones')
    ax.grid()

    fig.savefig("[BFGS] Convergencia de las soluciones.png")
    plt.show()

"""  IMPLEMENTADO  """


if __name__ == '__main__':
    # Testeo de BFGS, primero se generan datos para la funcion


    # Se ocupa el vector de "unos" como punto de inicio
    # (notar el salto que pega) de la iteracion 1 a la 2 el valor objetivo
    # -- Queda a tu eleccion que vector ingresar como solucion para la iteracion 1 --

    """  IMPLEMENTADO  """
    # Matriz rescatada de Excel
    X, Y = importar_excel()
    X = np.array(X)/100000
    Y = np.array(Y)/100000

    x0 = np.ones((10, 1))

    res = scipy.optimize.minimize(subrutina, x0, (X,Y), method='BFGS', options={'gtol': 1e-3, 'disp': False}, callback=graficar)
    calcular_convergencia(soluciones, res.x)
    """  IMPLEMENTADO  """
