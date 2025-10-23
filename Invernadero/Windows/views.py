from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from api_comunication.views import get_latest_parameters as api_latest, parameters_history as api_history, parameters_stats as api_stats
from django.http import HttpRequest
from django.http.request import QueryDict

def home(request):
    return render(request, 'landing.html')

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

@login_required
def get_latest_parameters(request):
    # Obtener datos del endpoint latest
    latest_request = HttpRequest()
    latest_request.method = 'GET'
    latest_response = api_latest(latest_request)
    
    # Obtener historial (últimas 10 mediciones)
    history_request = HttpRequest()
    history_request.method = 'GET'
    history_request.GET = QueryDict('limit=10')
    history_response = api_history(history_request)
    
    # Obtener estadísticas diarias
    stats_request = HttpRequest()
    stats_request.method = 'GET'
    stats_response = api_stats(stats_request)
    
    # Procesar datos
    context = {
        'temperatura': 'No disponible',
        'humedad': 'No disponible',
        'humedad_suelo': 'No disponible',
        'luz': 'No disponible',
        'riego': 'No disponible',
        'ventiladores': 'No disponible',
        'foco': 'No disponible',
        'history_data': [],
        'stats_data': []
    }
    
    # Procesar datos del latest
    if latest_response.status_code == 200:
        latest_data = latest_response.data
        context.update({
            'temperatura': latest_data.get('temperatura', 'No disponible'),
            'humedad': latest_data.get('humedad', 'No disponible'),
            'humedad_suelo': latest_data.get('humedad_suelo', 'No disponible'),
            'luz': latest_data.get('luz', 'No disponible'),
            'riego': 'Activo' if latest_data.get('riego') else 'Inactivo',
            'ventiladores': 'Activo' if latest_data.get('ventiladores') else 'Inactivo',
            'foco': 'Activo' if latest_data.get('foco') else 'Inactivo'
        })
    
    # Procesar datos del historial
    if history_response.status_code == 200:
        context['history_data'] = history_response.data
    
    # Procesar datos de estadísticas
    if stats_response.status_code == 200:
        context['stats_data'] = stats_response.data
    
    return render(request, 'estadisticas.html', context)
