#!/usr/bin/env python3
"""
Script para probar la API del invernadero
"""
import requests
import json

# URL del servidor
url = "https://floracore.onrender.com/api/parameters/"

# Datos de prueba (similares a los que envía el Arduino)
test_data = {
    "temperatura": 26.8,
    "humedad": 78.0,
    "humedad_suelo": 100.0,
    "luz": 100.0
}

print("Probando API del invernadero...")
print(f"URL: {url}")
print(f"Datos: {json.dumps(test_data, indent=2)}")

try:
    # Enviar solicitud POST
    response = requests.post(
        url, 
        json=test_data,
        headers={'Content-Type': 'application/json'},
        timeout=10
    )
    
    print(f"\nCódigo de respuesta: {response.status_code}")
    print(f"Headers de respuesta: {dict(response.headers)}")
    
    if response.text:
        print(f"Respuesta del servidor:")
        try:
            response_json = response.json()
            print(json.dumps(response_json, indent=2))
        except json.JSONDecodeError:
            print(f"Respuesta no es JSON válido: {response.text}")
    else:
        print("Respuesta vacía")
        
except requests.exceptions.RequestException as e:
    print(f"Error en la solicitud: {e}")
except Exception as e:
    print(f"Error inesperado: {e}")