import requests
import base64

API_KEY = "eA0XzW9oJlnezexYI1I9Ehfgq5gBTD4codNoquzM2Cm7y8Qwji"  # reemplazá con la clave válida

ENFERMEDADES_INFO = {
    "Leotiomycetes": {
        "descripcion": "Hongo fitopatógeno (ej: Botrytis) que causa moho gris y podredumbre blanda.",
        "tratamiento": "Eliminar tejido infectado, ventilar mejor y aplicar fungicidas orgánicos."
    },
    "Oidium": {
        "descripcion": "Oídio o cenicilla, genera manchas blancas polvorientas.",
        "tratamiento": "Poda, retiro de hojas enfermas y aplicación de azufre en polvo."
    },
    "Fungi": {
        "descripcion": "Infección fúngica general con necrosis y pudrición.",
        "tratamiento": "Eliminar tejido enfermo, reducir humedad y aplicar fungicidas naturales."
    },
    "downy mildew": {
        "descripcion": "Mildiu con manchas amarillas y moho blanco en el envés.",
        "tratamiento": "Cortar partes infectadas, buena ventilación y fungicidas naturales."
    },
    "rust": {
        "descripcion": "Roya con ampollas anaranjadas en hojas.",
        "tratamiento": "Podar áreas infectadas y aplicar cola de caballo o purín de ortiga."
    },
    "Insecta": {
        "descripcion": "Plaga de insectos chupadores (pulgones, mosca blanca).",
        "tratamiento": "Tratar con jabón potásico o insecticidas ecológicos suaves."
    },
    "Abiotic": {
        "descripcion": "Daños por factores ambientales (riego, luz, nutrientes).",
        "tratamiento": "Corregir riego, luz y fertilización según necesidad."
    },
    "Senescence": {
    "descripcion": "Proceso natural de envejecimiento de la planta, que provoca amarillamiento y caída de hojas viejas.",
    "tratamiento": "No requiere tratamiento, ya que es un ciclo normal. Solo retirar hojas secas y mantener condiciones óptimas de riego y nutrientes."
    },
    "dead plant": {
    "descripcion": "La planta está muerta o en un estado irreversible de deterioro.",
    "tratamiento": "No existe tratamiento posible. Se recomienda retirar la planta y reemplazarla por una nueva, revisando previamente las condiciones del entorno."
    }

}


def diagnosticar_planta(imagen_path):
    with open(imagen_path, "rb") as f:
        imagen_base64 = base64.b64encode(f.read()).decode("utf-8")

    url = "https://api.plant.id/v2/health_assessment"

    headers = {
        "Content-Type": "application/json",
        "Api-Key": API_KEY   # ✅ ahora la API se autentica por header
    }

    payload = {
        "images": [imagen_base64],
        "modifiers": ["crops_fast", "similar_images"],
        "plant_details": ["disease", "description", "treatment"]
    }

    res = requests.post(url, headers=headers, json=payload)

    if res.status_code != 200:
        return {
            "health_assessment": {
                "diseases": [{
                    "name": "Error en diagnóstico",
                    "description": {"short": f"No se pudo procesar la respuesta: {res.text}"},
                    "treatment": {"chemical": "Revisar conexión o API key", "biological": ""}
                }]
            }
        }

    data = res.json()

    # Enriquecer con info local
    diseases = data.get("health_assessment", {}).get("diseases", [])
    for disease in diseases:
        nombre = disease.get("name", "Desconocida")
        info_local = ENFERMEDADES_INFO.get(nombre, {})
        if not disease.get("description"):
            disease["description"] = {"short": info_local.get("descripcion", "Descripción no disponible.")}
        if not disease.get("treatment"):
            disease["treatment"] = {"chemical": info_local.get("tratamiento", "No disponible"), "biological": ""}

    return data
