import requests
import matplotlib.pyplot as plt
import numpy as np
import ctypes
import json
import os

#https://documents.worldbank.org/en/publication/documents-reports/api

##  Obtiene los datos del Índice GINI de la API mediante GET.
#   @return year años
#   @return value valores del índice
def get_data():
    response = requests.get(
        "https://api.worldbank.org/v2/en/country/ARG/indicator/SI.POV.GINI?format=json&date=2000:2025"
    )

    if response.ok:
        data = response.json()
        results = data[1]  # El segundo elemento contiene los datos

        year = []
        value = []
        for entry in results:
            if entry['value'] is not None:
                year.append(entry['date'])
                value.append(entry['value'])
            else:
                year.append(entry['date'])
                value.append(0)

        year = np.flip(np.array(year, dtype=float))
        value = np.flip(np.array(value, dtype=float))

        return year, value
    else:
        print("Error al obtener los datos:", response.status_code)
        return None, None

##  Wrapper de la función en C.
#   @param input Puntero flotante a un array de entrada.
#   @param output Puntero Entero a un array de salida.
#   @param length Longitud del arreglo.
def convertion(input:float, output:int, length:int):
    return convertion_c.convertion(input, output, length)

# Cargar la librería compartida
lib_path = os.path.join(os.path.dirname(__file__), 'convertion.so')
convertion_c = ctypes.CDLL(lib_path)

convertion_c.convertion.argtypes = (
    ctypes.POINTER(ctypes.c_float),  # float* input
    ctypes.POINTER(ctypes.c_int),    # int* output
    ctypes.c_int                     # int length
)
convertion_c.convertion.restype = ctypes.c_void_p

year, value = get_data()

length = len(value)
input_array = (ctypes.c_float * length)(*value)
output_array = (ctypes.c_int * length)()

convertion(input_array, output_array, len(value))
value_c = np.ctypeslib.as_array(output_array)

plt.plot(year, value_c, marker='o', label='Gini Index')
plt.title('Índice de Gini en Argentina (2011-2025)')
plt.xlabel('Año')
plt.grid(True)
plt.yticks(np.arange(0, 60, 1))
plt.ylim(30,60)
plt.ylabel('Índice de Gini')
plt.legend()
plt.xticks(rotation=45)
plt.show()