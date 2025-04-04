import ctypes
import requests
import json

response = requests.get("https://api.worldbank.org/v2/en/country/all/indicator/SI.POV.GINI?format=json&date=2011:2020&per_page=32500&page=1&country=%22Argentina%22")
if response:
    print("Response received successfully.")
    data = response.json()
    print(data[1][0])
else:
    print("Failed to retrieve data.")
