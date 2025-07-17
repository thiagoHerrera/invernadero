from django.shortcuts import render
from .utils import diagnosticar_planta
import os
from django.conf import settings

def subir_imagen(request):
    resultado = None
    diseases = []

    if request.method == 'POST' and request.FILES.get('foto'):
        imagen = request.FILES['foto']
        ruta_imagen = os.path.join(settings.MEDIA_ROOT, imagen.name)

        # Crear la carpeta media si no existe
        os.makedirs(os.path.dirname(ruta_imagen), exist_ok=True)

        with open(ruta_imagen, 'wb+') as destino:
            for chunk in imagen.chunks():
                destino.write(chunk)

        resultado = diagnosticar_planta(ruta_imagen)
        if resultado and "health_assessment" in resultado:
            diseases = resultado.get("health_assessment", {}).get("diseases", [])

    return render(request, 'subir_imagen.html', {'resultado': resultado, 'diseases': diseases})