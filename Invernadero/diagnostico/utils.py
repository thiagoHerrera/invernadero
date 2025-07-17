import requests
import base64

API_KEY = "P4kCJ4jg5YOzsOqljbCpwkBirpZACWV1EJD8wzfWM8HuSGwZYX"

def diagnosticar_planta(imagen_path):
    with open(imagen_path, "rb") as f:
        imagen_base64 = base64.b64encode(f.read()).decode("utf-8")
    
    payload = {
        "api_key": API_KEY,
        "images": [imagen_base64],
        "modifiers": ["crops_fast", "similar_images"],
        "plant_details": ["disease", "description", "treatment"]
    }
    res = requests.post("https://api.plant.id/v2/health_assessment", json=payload)
    print(res.json())  # Para depurar
    data = res.json()
    res = requests.post("https://api.plant.id/v2/health_assessment", json=payload)
    return res.json()
