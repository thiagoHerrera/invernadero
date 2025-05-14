from django.shortcuts import render

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
# Create your views here.
