import requests
import base64

API_KEY = "P4kCJ4jg5YOzsOqljbCpwkBirpZACWV1EJD8wzfWM8HuSGwZYX"

# Diccionario local con info de enfermedades
ENFERMEDADES_INFO = {
    "Leotiomycetes": {
        "descripcion": "Es un hongo fitopatógeno que afecta hojas y tallos...",
        "tratamiento": "Aplicar fungicidas adecuados, mejorar ventilación..."
    },
    "Oidium": {
        "descripcion": "Conocido como oídio o cenicilla, provoca manchas blancas...",
        "tratamiento": "Eliminar hojas afectadas y aplicar azufre o bicarbonato..."
    },
    "Abiotic": {
        "descripcion": "Problema abiótico: no hay infección, solo estrés ambiental.",
        "tratamiento": "Revisar riego, luz, temperatura y nutrientes de la planta."
    }
    # Agregá más enfermedades según tu necesidad
}

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
    data = res.json()

    # Procesamos las enfermedades detectadas
    diseases = data.get("health_assessment", {}).get("diseases", [])
    for disease in diseases:
        nombre = disease.get("name", "Desconocida")

        # Rellenar descripción y tratamiento desde diccionario local si no vienen
        info_local = ENFERMEDADES_INFO.get(nombre, {})
        disease["description"] = disease.get("description") or {"short": info_local.get("descripcion", "Descripción no disponible.")}
        disease["treatment"] = disease.get("treatment") or {"chemical": info_local.get("tratamiento", "No disponible"), "biological": ""}

    return data
