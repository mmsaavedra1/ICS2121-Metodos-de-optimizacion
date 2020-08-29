__author__ = "Moises Saavedra Caceres"
__email__ = "mmsaavedra1@ing.puc.cl"

# Modulos nativos de python
import random
import numpy as np
import scipy

# Modulos creados por usuario
from parametros import *


# Se crean funciones matematicas necesarias para este script
def funcion_enunciado(Q, c, x):
    """
    Funcion original vista en clases
    """

    # Se setean las dimension
    m, n = Q.shape

    # Este es el de la funcion del enunciado - NO EL DEL LINESEARCH
    alpha_ = 10

    return (0.5 * np.dot(np.transpose(x), np.dot(Q,x)) + np.dot(np.transpose(c), x) + alpha_*(5 - x[n-1])**4)[0][0]

def gradiente_enunciado(Q, c, x):
    """
    Gradiente de la funcion vista en clases
    """

    # Se setean las dimension
    m, n = Q.shape

    # Este es el de la funcion del enunciado - NO EL DEL LINESEARCH
    alpha_ = 10

    # Se crean las variables que ayudan a definir la funcion principal
    # para este caso el vector que solo posee valor en coordenada n
    vector_canonico = np.zeros((n, 1))
    vector_canonico[n-1][0] = 1

    return np.dot(Q, x) + c + vector_canonico * (-4*alpha_*(5-x[n-1])**3)

def phi(Q, c, x, alpha, direccion_descenso):
    return funcion_enunciado(Q, c, x+alpha*direccion_descenso)

def phi_derivado(Q, c, x, alpha, direccion_descenso):
    return np.dot(np.transpose(direccion_descenso), gradiente_enunciado(Q, c, x + alpha*direccion_descenso))


# Algoritmos de backtracking
def line_search_algoritmo(Q, c, x_k, direccion_descenso_k, maximo_iteraciones, c1=1e-4, c2=0.9, imprimir_avance=True):
    """
    En lugar de calcular: min f(xk + alpha*direccion_descensok) s.a alpha >= 0
    se parte con un intervalo largo y este se va acortando (backtracking).
    En la practica esto es un parte de la optimizacion temporal y
    costo computacional que implica el line search.

    PD: No ocupa el algoritmo de "backtracking"
    aprendido en introduccion a la programacion :)

    Funcion que recibe como parametros:
        - Q : Matriz definida por enunciado.
        - c : vector definido por enunciado.
        - x_k : vetor solucion de la iteracion actual del metodo usado.
        - direccion_descenso_k : direccion de descenso de la iteracion actual
        del metodo usado.
        - maximo_iteraciones : numero maximo de iteraciones hechas en el backtracking
        - c1 : peso de la condicion de Armijo.
        - c2 : peso de la condion de Wolfe.

    Luego, esta funcion retorna como parametros:
        - alpha_actual : incognita buscada
    """


    # Se obtienen las dimensiones del arreglo
    m, n = x_k.shape

    # Seteamos los parametros iniciales constantes
    alpha_0 = 0
    alpha_max = 50
    phi_0 = phi(Q, c, x_k, 0, direccion_descenso_k)
    phi_derivado_0 = phi_derivado(Q, c, x_k, 0, direccion_descenso_k)

    # Seteamos los parametros que iran mutando con el tiempo
    alpha_actual = random.uniform(alpha_0, alpha_max)
    alpha_anterior = 0
    iteracion_actual = 1
    phi_anterior = 0

    # Se comienza el loop del algoritmo
    while iteracion_actual <= maximo_iteraciones:

        if iteracion_actual > 1:
            phi_anterior = phi_actual

        # Se evaluar phi(alpha_actual)
        phi_actual = phi(Q, c, x_k, alpha_actual, direccion_descenso_k)

        # 1º criterio de parada
        if (phi_actual > phi_0 + c1*alpha_actual*phi_derivado_0) or (phi_actual >= phi_anterior and iteracion_actual > 1):
            return zoom(Q, c, x_k, direccion_descenso_k, alpha_anterior, alpha_actual, imprimir_avance)

        # Se evalua phi_derivado(alpha_actual)
        phi_derivado_actual = phi_derivado(Q, c, x_k, alpha_actual, direccion_descenso_k)

        # 2º criterio de parada
        if np.abs(phi_derivado_actual) <= -c2*phi_derivado_0:
            return alpha_actual

        # 3º criterio de parada
        if phi_derivado_actual >= 0:
            return zoom(Q, c, x_k, direccion_descenso_k, alpha_actual, alpha_anterior, imprimir_avance)

        # Si no cumple ningun criterio de parada se actualiza el mundo
        alpha_anterior = alpha_actual
        alpha_actual = np.random(alpha_anterior, alpha_max)
        iteracion_actual += 1

def zoom(Q, c, x_k, direccion_descenso_k, alpha_low, alpha_high, imprimir_avance, c1=1e-4, c2=0.9):
    """
    Funcion que interpola los valores de alpha para encontrar valor razonable
    alpha a retornar.

    Funcion que recibe como parametros:
        - alpha_low : cota minima de interpolacion
        - alpha_high : cota maxima de interpolacion

    Luego, esta funcion retorna como parametros:
        - alpha : incognita buscada
    """

    # Se setan los valores importantes
    phi_0 = phi(Q, c, x_k, 0, direccion_descenso_k)
    phi_derivado_0 = phi_derivado(Q, c, x_k, 0, direccion_descenso_k)
    iteracion_actual = 1

    if imprimir_avance == True:
        print("\n\n*********        INICIO  BACKTRACKING        **********")
        print("           ITERACION               LAMBDA")

    while True:

        # Actualiza en pantalla el ultimo valor encontrado

        alpha_actual = random.uniform(alpha_low, alpha_high)

        if imprimir_avance == True:
            print(f"{iteracion_actual: ^32d} {alpha_actual: ^12f}")

        # Se calculan los valores de phi y phi_derivado evaluados en
        # el alpha de la iteracion actual.
        phi_actual = phi(Q, c, x_k, alpha_actual, direccion_descenso_k)

        if (phi_actual > phi_0 + c1*alpha_actual*phi_derivado_0) or (phi_actual >= phi(Q, c, x_k, alpha_low, direccion_descenso_k)):
            alpha_high = alpha_actual

        else:

            phi_derivado_actual = phi_derivado(Q, c, x_k, alpha_actual, direccion_descenso_k)
            if np.abs(phi_derivado_actual) <= -c2*phi_derivado_0:

                if imprimir_avance == True:
                    print("*********           FIN BACKTRACKING        **********\n\n")
                return alpha_actual

            if phi_derivado_actual*(alpha_high - alpha_low) >= 0:
                alpha_high = alpha_low

            alpha_low = alpha_actual

        iteracion_actual += 1

if __name__ == '__main__':

    # Mismos datos siempre
    np.random.seed(1)

    # Testeo de Line search, primero se generan datos para la funcion
    n = 4
    Q, c = generar_datos(n)

    # Se ocupa el vector de "unos" como punto de inicio
    # (notar el salto que pega) de la iteracion 1 a la 2 el valor objetivo
    # -- Queda a tu eleccion que vector ingresar como solucion para la iteracion 1 --
    x0 = np.random.rand(n, 1)

    # Se crea una direccion de descenso para el Testeo
    direccion_descenso = - gradiente_enunciado(Q, c, x0)

    # Se realiza un llamada a la subrutina de line search
    line_search_algoritmo(Q, c, x0, direccion_descenso, 100)
