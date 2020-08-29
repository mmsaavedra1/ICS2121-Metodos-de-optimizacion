__author__ = "Moises Saavedra Caceres"
__email__ = "mmsaavedra1@ing.puc.cl"


# Modulos nativos de python
import numpy as np
import time
import scipy.optimize

# Modulo creado por usuario
from parametros import *

# Se crea un decorador (googlear) del tipo timer para testear el tiempo
# de ejecucion del programa
def timer(funcion):
    def inner(*args, **kwargs):

        inicio = time.time()
        resultado = funcion(*args, **kwargs)
        final = round(time.time() - inicio, 3)
        print("\nTiempo de ejecucion total: {}[s]".format(final))

        return resultado
    return inner


def evaluar_funcion_gradiente(Q, c, x, funcion_objetivo, gradiente_objetivo):
    """
    Esta funcion va creando el paso de cada iteracion. Ocupando la teoría
    estudiada. Retorna el valor de la funcion, su gradiente y su hessiano, evaluados en xi
    para la iteracion i.
    """

    alpha = 10

    # Evaluacion de la funcion a optimizar, gradiente y hessiano con el x, y sus factores asociados.
    funcion_objetivo_evaluada = funcion_objetivo(x, Q, c, alpha)
    gradiente_evaluado = gradiente_objetivo(x, Q, c, alpha)

    return funcion_objetivo_evaluada, gradiente_evaluado


def funcion_enunciado(lambda_, Q, c, x, alpha, direccion_descenso):
    """
    Funcion original evaluada en: x + lambda*direccion_descenso
    """
    m, n = Q.shape

    # Se actualiza el valor de x
    x = x + lambda_*direccion_descenso

    return (0.5 * np.dot(np.transpose(x), np.dot(Q,x)) + np.dot(np.transpose(c), x) + alpha*(5 - x[n-1])**4)[0][0]


def funcion_enunciado(lambda_, Q, c, x, alpha, direccion_descenso):
    """
    Funcion original evaluada en: x + lambda*direccion_descenso
    """
    m, n = Q.shape

    # Se actualiza el valor de x
    x = x + lambda_*direccion_descenso

    return (0.5 * np.dot(np.transpose(x), np.dot(Q,x)) + np.dot(np.transpose(c), x) + alpha*(5 - x[n-1])**4)[0][0]

@timer
def gradiente(Q, c, x0, epsilon, iteracion_maxima, funcion_objetivo, gradiente_objetivo):
    """
    Esta funcion es una aplicacion del metodo del gradiente, la que
    va a ir devolviendo valor objetivo, gradiente actual.

    Su entrada posee:
    - Q : matriz cuadrada que constituye la funcion definida
    - c : vector asociado que constituye la funcion definida
    - x0 : punto inicial de prueba
    - epsilon : error/ tolerancia deseada
    - iteracion_maxima : numero maximo de iteraciones

    Su retorno (salida) es:
    - valor : valor de la funcion evaluada en x en la iteracion actual
    - x : solucion en la que se alcanza el valor objetivo
    - R : matriz con la informacion de cada iteracion. Es una fila por iteracion
          y esta constituida por:
          - Numero de iteracion
          - valor
          - norma del gradiente
          - paso (lambda)
    """
    # 1º paso del algoritmo: Se definen los parametros iniciales
    iteracion = 0
    stop = False
    x = x0
    alpha = 10

    # Se prepara el output del codigo para en cada iteracion
    # entregar la informacion correspondiente
    print("\n\n*********      METODO DE GRADIENTE      **********\n")
    print("ITERACION     VALOR OBJ      NORMA        LAMBDA")

    # Se inicia el ciclo para las iteraciones maximas seteadas por el usuario
    while (stop == False) and (iteracion <= iteracion_maxima):

        # 2º paso del algoritmo: Se obtiene la informacion para determinar
        # el valor de la direccion de descenso
        [valor_funcion, valor_gradiente] = evaluar_funcion_gradiente(Q, c, x, funcion_objetivo, gradiente_objetivo)
        direccion_descenso = -valor_gradiente

        # 3º paso del algoritmo: Se analiza el criterio de parada
        norma = np.linalg.norm(valor_gradiente, 2)

        if norma <= epsilon:
            stop = True
        else:
        # 4º paso del algoritmo: Se busca el peso (lambda) optimo
            # Se definen las dimensiones
            [m, n] = Q.shape

            # Se resuelve el subproblema de lambda
            lambda_ = scipy.optimize.fminbound(funcion_enunciado, 0, 10, args=(Q, c, x, alpha, direccion_descenso))

        # La rutina del gradiente muestra en pantalla para cada iteracion:
        # nº de iteracion, valor de la funcion evaluada en el x de la iteracion,
        # la norma del gradiente y el valor de peso de lambda
        retorno_en_pantalla = [iteracion, valor_funcion, norma, lambda_]
        print(f"{retorno_en_pantalla[0]: ^12d}{retorno_en_pantalla[1][0][0]: ^12f} {retorno_en_pantalla[2]: ^12f} {retorno_en_pantalla[3]: ^12f}")

        # 5º paso del algoritmo: Se actualiza el valor de x para la siguiente
        # iteracion del algoritmo
        x = x + lambda_*direccion_descenso
        iteracion += 1

    return retorno_en_pantalla

if __name__ == '__main__':
    # Creacion de funcion objetivo, gradiente y hessiano
    def funcion_objetivo(x, Q, c, alpha):
        """
        Como argumentos, se aconseja colocar todos los valores constantes que tiene la funcion.
        Después, en la ejecución de la rutina de Newton se da un valor a dichos argumentos.
        """
        funcion = 0.5 * np.dot(np.transpose(x), np.dot(Q,x)) + np.dot(np.transpose(c), x) + alpha*(5 - x[n-1])**4
        return funcion


    def gradiente_objetivo(x, Q, c, alpha):
        """
        Como argumentos, se aconseja colocar todos los valores constantes que tiene la funcion.
        Después, en la ejecución de la rutina de Newton se da un valor a dichos argumentos.
        """

        # Dimensiones de la matriz ingresada
        n, _ = Q.shape

        # Se crean las variables que ayudan a definir la funcion principal
        # para este caso el vector que solo posee valor en coordenada n
        # y la matriz que posee valor en coordenada en fila m y coordenada n
        # ademas del valor del real alpha 
        # (evaluacion de los argumentos de la funcion definidas debajo delif __name__ == '__name__')

        vector_canonico = np.zeros((n, 1))
        vector_canonico[n-1][0] = 1

        gradiente = np.dot(Q, x) + c + vector_canonico * (-4*alpha*(5-x[n-1])**3)

        return gradiente
    

    # Se crean siempre los mismos numeros aleatorios
    # Borrar ambos seed si se desea lo contrario
    random.seed(0)
    np.random.seed(0)

    # Testeo de Newton, primero se generan datos para la funcion
    n = 4
    Q, c = generar_datos(n) # Se importa del modulo parametros

    # Se ocupa el vector de "unos" como punto de inicio
    # (notar el salto que pega) de la iteracion 1 a la 2 el valor objetivo
    # -- Queda a tu eleccion que vector ingresar como solucion para la iteracion 1 --
    x0 = np.ones((n, 1))

    # Error asociado 10% este caso
    epsilon = 0.1

    # Maximo de iteraciones (para que no quede un loop infinito)
    iteracion_maxima = 5

    gradiente(Q, c, x0, epsilon, iteracion_maxima, funcion_objetivo, gradiente_objetivo)
