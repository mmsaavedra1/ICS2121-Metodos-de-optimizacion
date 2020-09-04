# -*- coding: utf-8 -*-
__author__ = "Moises Saavedra Caceres"
__email__ = "mmsaavedra1@ing.puc.cl"


# Modulos nativos de python
import numpy as np
import numdifftools as nd
import time
from scipy.optimize import fminbound



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


""" IMPLEMENTADO """
def funcion_linesearch(_lambda, X, Y, variables, direccion_descenso):
    variables = variables + _lambda*direccion_descenso
    return sum([(variables[j+5]*(X[i][j]**variables[j]) - Y[i])**2 for i in range(55) for j in range(5)])/2*55
""" IMPLEMENTADO """


def subrutina(X, Y, var_alfa, var_beta):
    """
    Esta funcion va creando el paso de cada iteracion. Ocupando la teoría
    estudiada. Retorna el valor de la funcion, su gradiente y su hessiano segun
    la iteracion estudiada.
    """

    """ IMPLEMENTADO """
    # Se crean las variables que ayudan a definir la funcion principal
    # para este caso el vector que solo posee valor en coordenada n
    # y la matriz que posee valor en coordenada en fila m y coordenada n
    # ademas del valor del real alpha


    # Funcion a calcular
    variables = np.concatenate((var_alfa, var_beta))
    funcion_objetivo = lambda variables: sum([(variables[j+5]*(X[i][j]**variables[j]) - Y[i])**2 for i in range(55) for j in range(5)])/(2*55)
    valor_funcion_objetivo = funcion_objetivo(variables)

    # Calcular gradiente con metodos numericos
    gradiente = nd.Gradient(funcion_objetivo)
    valor_gradiente = gradiente(variables)

    # Calcular newton con metodos numericos
    hessiano = nd.Hessian(funcion_objetivo)
    valor_hessiano = hessiano(variables)
    """ IMPLEMENTADO """

    return valor_funcion_objetivo, valor_gradiente, valor_hessiano


@timer
def newton(X, Y, var_alfa_inicial, var_beta_inicial, epsilon, iteracion_maxima):
    """
    Esta funcion es una aplicacion del metodo de Newton, la que
    va a ir devolviendo valor objetivo, gradiente actual y Hessiano.
    """
    # 1º paso del algoritmo: Se definen los parametros iniciales
    iteracion = 0
    stop = False
    var_alfa = var_alfa_inicial
    var_beta = var_beta_inicial

    """ IMPLEMENTADO """
    error = []
    iteraciones = []
    """ IMPLEMENTADO """


    # Se prepara el output del codigo para en cada iteracion
    # entregar la informacion correspondiente
    print("\n\n*********       METODO DE NEWTON      **********\n")
    print("ITERACION     VALOR OBJ      NORMA        LAMBDA")

    # Se inicia el ciclo para las iteraciones maximas seteadas por el usuario
    while (stop == False) and (iteracion <= iteracion_maxima):

        # 2º paso del algoritmo: Se obtiene la informacion para determinar
        # el valor de la direccion de descenso
        [valor, gradiente, hessiano] = subrutina(X, Y, var_alfa, var_beta)
        direccion_descenso = np.dot(-np.linalg.inv(hessiano), gradiente)

        # 3º paso del algoritmo: Se analiza el criterio de parada
        norma = np.linalg.norm(gradiente, ord=2)
        error.append(norma)

        if norma <= epsilon:
            stop = True
        else:
        # 4º paso del algoritmo: Se busca el peso (lambda) optimo
            """ IMPLEMENTADO + funcion_linesearch arriba"""
            variables = np.concatenate((var_alfa, var_beta))
            lambda_ = fminbound(funcion_linesearch, 0, 1, args=(X, Y, variables, direccion_descenso))
            """ IMPLEMENTADO + funcion_linesearch arriba"""

        # La rutina de Newton muestra en pantalla para cada iteracion:
        # nº de iteracion, valor de la funcion evaluada en el x de la iteracion,
        # la norma del gradiente y el valor de peso de lambda
        retorno_en_pantalla = [iteracion, valor, norma, lambda_]
#       Nota de J. Vera: Esta forma de "print" requiere Python 3.6 
#        print(f"{retorno_en_pantalla[0]: ^12d}{retorno_en_pantalla[1][0][0]: ^12f} {retorno_en_pantalla[2]: ^12f} {retorno_en_pantalla[3]: ^12f}")

        print("%12.6f %12.6f %12.6f %12.6f" % (retorno_en_pantalla[0],retorno_en_pantalla[1], retorno_en_pantalla[2], retorno_en_pantalla[3]))

        # 5º paso del algoritmo: Se actualiza el valor de x para la siguiente
        # iteracion del algoritmo
        """ IMPLEMENTADO """
        var_alfa = var_alfa + (lambda_/110)*direccion_descenso[:5]
        var_beta = var_beta + (lambda_/110)*direccion_descenso[5:]
        iteracion += 1
        iteraciones.append(iteracion)
        """ IMPLEMENTADO """
    
    """ IMPLEMENTADO """
    import matplotlib
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots()
    ax.plot(iteraciones, error)

    ax.set(xlabel='Iteracion', ylabel='Error',
        title='Análisis de convergencia del error')
    ax.grid()

    fig.savefig("[Newton] Convergencia del error.png")
    plt.show()
    """ IMPLEMENTADO """

    return retorno_en_pantalla