from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from users.models import Parameters

@login_required
def home(request):
    return render(request, 'home.html')

def landing(request):
    return render(request, 'landing.html')

def equipo(request):
    return render(request, 'equipos.html')

def contacto(request):
    return render(request, 'contacto.html')

def funciones(request):
    return render(request, 'funciones.html')

def info(request):
    return render(request, 'info.html')

def historialcultivo(request):
    ultimo = Parameters.objects.last()

    if ultimo is None:
        return render(request, 'estadisticas.html', {
            'temperatura': 'No disponible',
            'humedad': 'No disponible',
            'humedad_suelo': 'No disponible',
        })

    data = {
        'temperatura': ultimo.temperature,
        'humedad': ultimo.hume,
        'humedad_suelo': ultimo.hume_floor,
    }

    return render(request, 'historial-cultivo.html', data)


