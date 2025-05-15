from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from users.models import Parameters

@login_required
def home(request):
    return render(request, 'post-login/home.html')

def landing(request):
    return render(request, 'pre-login/landing.html')

def equipo(request):
    return render(request, 'pre-login/equipos.html')

def contacto(request):
    return render(request, 'pre-login/contacto.html')

def funciones(request):
    return render(request, 'pre-login/funciones.html')

def info(request):
    return render(request, 'pre-login/info.html')

def estadisticas(request):
    return render(request, 'post-login/estadisticas.html')
# Create your views here.

def perfil(request):
    return render(request, 'post-login/perfil.html')

def planta(request):
    return render(request, 'post-login/mi_planta.html')

def notificaciones(request):
    return render(request, 'post-login/notificaciones.html')



def get_latest_parameters(request):
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

    return render(request, 'post-login/estadisticas.html', data)
