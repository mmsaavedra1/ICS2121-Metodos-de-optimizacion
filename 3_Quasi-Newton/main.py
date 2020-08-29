__author__ = "Moises Saavedra Caceres"
__email__ = "mmsaavedra1@ing.puc.cl"


from quasi_newton import *
from newton import *

#Una vez que se tienen los modulos creados, deben crear en el archivo main las funciones que
#se desean estudiar y analizar.
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


def hessiano_objetivo(x, Q, alpha):
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

    matriz_canonica = np.zeros((n,n))
    matriz_canonica[n-1][n-1] = 1

    hessiano = Q + matriz_canonica * (12*alpha*(5-x[n-1])**2)

    return hessiano

 

#####################  Correr algoritmo para las funciones definidas #####################

# Este comando genera los valores aleatorios para cada ejecucion
np.random.seed(1)


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
iteracion_maxima = 200

quasinewton_BFGS(Q, c, x0, epsilon, iteracion_maxima, funcion_objetivo, gradiente_objetivo)
newton(Q, c, x0, epsilon, iteracion_maxima, funcion_objetivo, gradiente_objetivo, hessiano_objetivo)
