from django.shortcuts import render
from .utils import diagnosticar_planta
import os
from django.conf import settings

def subir_imagen(request):
    resultado = None
    primera_disease = None
    imagen_url = None  # inicializar siempre para evitar errores

    if request.method == 'POST' and request.FILES.get('foto'):
        imagen = request.FILES['foto']
        ruta_imagen = os.path.join(settings.MEDIA_ROOT, imagen.name)

        # Crear la carpeta media si no existe
        os.makedirs(os.path.dirname(ruta_imagen), exist_ok=True)

        # Guardar la imagen
        with open(ruta_imagen, 'wb+') as destino:
            for chunk in imagen.chunks():
                destino.write(chunk)

        # Diagnosticar la planta
        resultado = diagnosticar_planta(ruta_imagen)
        if resultado and "health_assessment" in resultado:
            diseases = resultado.get("health_assessment", {}).get("diseases", [])
            if diseases:
                primera_disease = diseases[0]  # Tomamos solo la primera enfermedad

        # Construir URL pública de la imagen
        imagen_url = os.path.join(settings.MEDIA_URL, imagen.name)

    return render(request, 'subir_imagen.html', {
        'resultado': resultado,
        'disease': primera_disease,
        'imagen_url': imagen_url  # siempre definida
    })
