import requests
import matplotlib.pyplot as plt
import numpy as np
import ctypes
import json

#https://documents.worldbank.org/en/publication/documents-reports/api

response = requests.get(
    "https://api.worldbank.org/v2/en/country/ARG/indicator/SI.POV.GINI?format=json&date=2000:2025"
)

if response.ok:
    data = response.json()
    results = data[1]  # El segundo elemento contiene los datos

    year = []
    value = []
    for entry in results:
        year.append(entry['date'])
        value.append(entry['value'])
    year = np.flip(np.array(year))
    value = np.flip(np.array(value))

    plt.plot(year, value, marker='o', label='Gini Index')
    plt.title('Índice de Gini en Argentina (2011-2025)')
    plt.xlabel('Año')
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.show()
else:
    print("Error al obtener los datos:", response.status_code)
