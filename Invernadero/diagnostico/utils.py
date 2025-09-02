import requests
import base64

API_KEY = "P4kCJ4jg5YOzsOqljbCpwkBirpZACWV1EJD8wzfWM8HuSGwZYX"

# Diccionario local con info de enfermedades
ENFERMEDADES_INFO = {
    "Leotiomycetes": {
        "descripcion": "Hongo fitopatógeno (por ejemplo Botrytis) que causa moho gris y podredumbre blanda en hojas, flores y tallos.",
        "tratamiento": "Eliminar el tejido infectado, mejorar la ventilación y aplicar fungicidas orgánicos (purín de ortiga o cola de caballo)."
    },
    "Oidium": {
        "descripcion": "Enfermedad fúngica conocida como oídio o cenicilla que genera manchas blancas polvorientas sobre las hojas.",
        "tratamiento": "Poda y retiro de las zonas afectadas, y aplicación de azufre en polvo o tratamientos ecológicos como infusión de ajo o purines."
    },
    "Fungi": {
        "descripcion": "Infección fúngica general que provoca necrosis, manchas foliares y pudrición en raíces o tallos.",
        "tratamiento": "Eliminar tejido enfermo, reducir la humedad ambiental y usar fungicidas naturales (purín de ortiga, cola de caballo) como preventivos."
    },
    "downy mildew": {
        "descripcion": "Enfermedad por mildiu que causa manchas amarillas en el haz de la hoja y moho blanco en el envés.",
        "tratamiento": "Cortar partes infectadas, asegurar buena ventilación y aplicar fungicidas naturales (azufre, purín de ortiga o cola de caballo)."
    },
    "rust": {
        "descripcion": "Enfermedad de la roya que produce puntos o ampollas anaranjadas en el envés de las hojas.",
        "tratamiento": "Podar las áreas infectadas y aplicar fungicidas caseros como cola de caballo o purín de ortiga sobre las hojas afectadas."
    },
    "Insecta": {
        "descripcion": "Plaga de insectos chupadores (pulgones, mosca blanca, etc.) que extraen savia y provocan hojas amarillas y marchitas.",
        "tratamiento": "Tratar con jabón potásico o insecticidas ecológicos suaves, eliminar manualmente los insectos y fomentar depredadores naturales como mariquitas."
    },
    "Abiotic": {
        "descripcion": "Problema abiótico: daños por factores ambientales (riego, luz, nutrientes, temperatura) sin patógeno presente.",
        "tratamiento": "Corregir el estrés ajustando riego, luz, temperatura y fertilización según las necesidades de la planta."
    }
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
