from django.shortcuts import render
from django.contrib.auth.decorators import login_required

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

def estadisticas(request):
    return render(request, 'estadisticas.html')
# Create your views here.
