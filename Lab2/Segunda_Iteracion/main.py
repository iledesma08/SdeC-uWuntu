import requests
import matplotlib.pyplot as plt
import numpy as np
import os
from msl.loadlib import LoadLibrary
from msl.loadlib import Client64

class MainC(Client64):
    def __init__(self):
        lib_path = os.path.join(os.path.dirname(__file__), 'main_c.so')
        super().__init__(lib_path)

    def convertion(self, input_array):
        length = len(input_array)
        int_array = self.request32('convertion', input_array.astype(np.float32), length)
        return np.array(int_array, dtype=np.int32)

##
# Fetches the GINI index
def get_data():
    response = requests.get(
        "https://api.worldbank.org/v2/en/country/ARG/indicator/SI.POV.GINI?format=json&date=2000:2025"
    )

    if response.ok:
        data = response.json()
        results = data[1]
        year = []
        value = []

        for entry in results:
            year.append(entry['date'])
            value.append(entry['value'] if entry['value'] is not None else 0)

        return np.flip(np.array(year, dtype=float)), np.flip(np.array(value, dtype=float))
    else:
        print("Failed to fetch data:", response.status_code)
        return None, None

# Usar la clase para convertir valores
main_c = MainC()

# Fetch and convert
year, value = get_data()
value_c = main_c.convertion(value)

# Plotting
plt.plot(year, value_c, marker='o', label='Gini Index (converted)')
plt.title('Gini Index in Argentina (2000–2025)')
plt.xlabel('Year')
plt.grid(True)
plt.legend()
plt.xticks(rotation=45)
plt.ylim(30, 60)
plt.yticks(np.arange(30, 60, 1))
plt.show()
