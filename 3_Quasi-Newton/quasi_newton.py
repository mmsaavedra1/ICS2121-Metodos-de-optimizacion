__author__ = "Moises Saavedra Caceres"
__email__ = "mmsaavedra1@ing.puc.cl"


# Modulos nativos de python
import numpy as np
import scipy.linalg
import scipy.optimize
import random
import time


# Modulos creados por usuario
from parametros import *


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


def funcion_enunciado(lambda_, Q, c, x, alpha, direccion_descenso):
    """
    Funcion original evaluada en: x + lambda*direccion_descenso
    """
    m, n = Q.shape

    # Se actualiza el valor de x
    x = x + lambda_*direccion_descenso

    return (0.5 * np.dot(np.transpose(x), np.dot(Q,x)) + np.dot(np.transpose(c), x) + alpha*(5 - x[n-1])**4)[0][0]


# Se genera el algoritmo de quasi newton mediante BFGS
@timer
def quasinewton_BFGS(Q, c, x0, epsilon, iteracion_maxima, funcion_objetivo, gradiente_objetivo):
    """
    Esta funcion es una aplicacion del metodo de Newton, la que
    va a ir devolviendo valor objetivo, gradiente actual y Hessiano.

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

    # 1º paso: Se definen los parametros iniciales
    m, n = x0.shape
    iteracion = 0
    stop = False
    alpha = 10

    # Se necesitan valores actuales y anteriores
    xk = x0
    gradientek = -gradiente_objetivo(xk, Q, c, alpha)
    Bk = np.identity(m)
    Bk_inversa = np.linalg.inv(Bk)

    # Solo una vez se "calcula" la inversa del hessiano (para este caso B0 es la I)
    direccion_descenso = -np.dot(Bk_inversa, gradientek)

    # Se prepara el output del codigo para en cada iteracion
    # entregar la informacion correspondiente
    print("\n\n*********       METODO DE QUASI NEWTON      **********\n")
    print("ITERACION     VALOR OBJ      NORMA        LAMBDA")

    # Se inicial el ciclo para las iteracion maximas seteadas por el usuario
    while (stop == False) and (iteracion <= iteracion_maxima):
        # 2º paso: Se obtiene la direccion de descenso
        direccion_descenso = -np.dot(Bk_inversa, gradientek)

        # 3º paso del algoritmo: Se analiza el criterio de parada
        norma = np.linalg.norm(gradientek, ord=2)

        if norma <= epsilon:
            stop = True
        else:
            # 4º paso: Se realiza LINESEARCH, para efectos de simplicidad se ocupara
            # el modulo scipy, tambien puedes implementar el subido a siding, pero
            # eso requiere que modifiques el codigo.
            lambda_ = scipy.optimize.fminbound(funcion_enunciado, 0, 10, args=(Q, c, xk, alpha, direccion_descenso))

            # 5º paso: se setea un parametro de la ecuacion de la secante
            sk = lambda_*direccion_descenso

            # 6º paso: se actualiza el valor de xk
            xk_anterior = xk
            xk = xk_anterior + sk

            # 7º paso: se setea un parametro de la ecuacion de la secante
            gradientek_anterior = gradientek
            gradientek = -gradiente_objetivo(xk, Q, c, alpha)
            yk = gradientek - gradientek_anterior


            # 8º paso: se actualiza el valor del hessiano aproximado
            Bk_anterior = Bk
            Bk = Bk_anterior + np.dot(yk, np.transpose(yk))/np.dot(np.transpose(yk),sk) - np.dot(Bk_anterior, np.dot(np.dot(sk, np.transpose(sk)), np.transpose(Bk_anterior)))/np.dot(np.transpose(sk), np.dot(Bk_anterior, sk))

            # 9º paso: se calcula la inversa mediante aproximacion
            Bk_inversa_anterior = Bk_inversa
            Bk_inversa = Bk_inversa_anterior + (np.dot(np.transpose(sk), yk) + np.dot(np.transpose(yk),np.dot(Bk_inversa_anterior, yk)))*np.dot(sk, np.transpose(sk))/(np.dot(np.transpose(sk), yk)**2) - (np.dot(Bk_inversa_anterior, np.dot(yk, np.transpose(sk))) + np.dot(sk, np.dot(np.transpose(yk), Bk_inversa_anterior)))/np.dot(np.transpose(sk), yk)

        # La rutina de Newton muestra en pantalla para cada iteracion:
        # nº de iteracion, valor de la funcion evaluada en el x de la iteracion,
        # la norma del gradiente y el valor de peso de lambda
        valor = funcion_objetivo(xk, Q, c, alpha)
        retorno_en_pantalla = [iteracion, valor, norma, lambda_]

        print(f"{retorno_en_pantalla[0]: ^12d}{retorno_en_pantalla[1]: ^12f} {retorno_en_pantalla[2]: ^12f} {retorno_en_pantalla[3]: ^12f}")

        # Siguiente iteracion del algoritmo
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
        return funcion[0][0]


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
    
    # Este comando genera los valores aleatorios para cada ejecucion
    np.random.seed(1)

    # Testeo de Newton, primero se generan datos para la funcion
    n = 4
    Q, c = generar_datos(n)

    # Se ocupa el vector de "unos" como punto de inicio
    # (notar el salto que pega) de la iteracion 1 a la 2 el valor objetivo
    # -- Queda a tu eleccion que vector ingresar como solucion para la iteracion 1 --
    x0 = np.ones((n, 1))

    # Error asociado 10% este caso
    epsilon = 0.1

    # Maximo de iteraciones (para que no quede un loop infinito)
    iteracion_maxima = 200

    quasinewton_BFGS(Q, c, x0, epsilon, iteracion_maxima, funcion_objetivo, gradiente_objetivo)
