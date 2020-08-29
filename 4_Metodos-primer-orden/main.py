__author__ = "Moises Saavedra Caceres"
__email__ = "mmsaavedra1@ing.puc.cl"

# Se importan los script de ambos metodos para compararlos
from LASSO.LASSO import *
from LASSOACELERADO.LASSO_FISTA import *

# Se importan los modulos creados por el usuario
from parametros import *

# Esto es para que simepre se generen los mismos numeros aleatorios
np.random.seed(1000)

# Esto es aprueba de errores de singularidad
while True:
    try:
        # Setea las dimensiones deseadas
        A, b = generar_datos(30, 100)
        # Se generan los valores de error e iteraciones
        numero_iteraciones = 100
        error = 10

        # Se prueba la singularidad (NO HACER CASO A ESTA LINEA)
        prueba = np.linalg.inv(A)

    except:
        print("¡Error de singularidad!")

    finally:
        # Se corre el programa
        LASSO(A, b, error, numero_iteraciones)
        print("\n{}\n".format("*"*50))
        LASSO_FISTA(A, b, error, numero_iteraciones)
        break
