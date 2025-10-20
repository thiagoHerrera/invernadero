#!/usr/bin/env python3
"""
Script para probar la API del invernadero localmente
"""
import requests
import json
import sys

def test_api_endpoint(url, data):
    """Prueba un endpoint de la API"""
    print(f"Probando: {url}")
    print(f"Datos: {json.dumps(data, indent=2)}")
    
    try:
        response = requests.post(
            url,
            json=data,
            headers={
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            timeout=10
        )
        
        print(f"Código de respuesta: {response.status_code}")
        print(f"Headers: {dict(response.headers)}")
        
        if response.text:
            print("Respuesta:")
            try:
                response_json = response.json()
                print(json.dumps(response_json, indent=2))
                return True
            except json.JSONDecodeError:
                print(f"Respuesta no es JSON válido:")
                print(response.text[:500])  # Primeros 500 caracteres
                return False
        else:
            print("Respuesta vacía")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"Error en la solicitud: {e}")
        return False

def main():
    # Datos de prueba similares a los del Arduino
    test_data = {
        "temperatura": 26.8,
        "humedad": 78.0,
        "humedad_suelo": 100.0,
        "luz": 100.0
    }
    
    # URLs a probar
    urls = [
        "https://floracore.onrender.com/api/parameters/",
        "http://localhost:8000/api/parameters/"  # Para pruebas locales
    ]
    
    success_count = 0
    for url in urls:
        print("=" * 60)
        if test_api_endpoint(url, test_data):
            success_count += 1
        print()
    
    print(f"Pruebas exitosas: {success_count}/{len(urls)}")
    return success_count > 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)