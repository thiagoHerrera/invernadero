import requests
import json
import time
import random

# URL del endpoint
url = "http://127.0.0.1:8000/api/parameters/"

# Simular datos de sensores
def generate_sensor_data():
    return {
        "temperatura": round(random.uniform(18, 30), 1),
        "humedad": round(random.uniform(50, 80), 1),
        "humedad_suelo": round(random.uniform(30, 70), 1),
        "luz": round(random.uniform(60, 95), 1)
    }

# Enviar datos
data = generate_sensor_data()
print(f"Enviando datos: {data}")

try:
    response = requests.post(url, json=data)
    print(f"Status: {response.status_code}")
    print(f"Respuesta: {response.json()}")
except Exception as e:
    print(f"Error: {e}")