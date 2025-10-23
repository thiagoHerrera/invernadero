from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from users.models import Parameters
from django.db.models import Avg
from django.db.models.functions import TruncDate

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
    
    try:
        # Obtener el último registro
        latest = Parameters.objects.order_by('-id').first()
        if latest:
            context.update({
                'temperatura': latest.temperature,
                'humedad': latest.hume,
                'humedad_suelo': latest.hume_floor,
                'luz': latest.light,
                'riego': 'Activo' if latest.riego else 'Inactivo',
                'ventiladores': 'Activo' if latest.ventiladores else 'Inactivo',
                'foco': 'Activo' if latest.foco else 'Inactivo'
            })
        
        # Obtener historial (últimas 10 mediciones)
        history_data = Parameters.objects.order_by('-id')[:10]
        context['history_data'] = history_data
        

        
        # Obtener estadísticas diarias (convertir CharField a Float para promedios)
        from django.db.models import Case, When, FloatField
        from django.db.models.functions import Cast
        
        try:
            stats = Parameters.objects.annotate(
                date=TruncDate('timestamp'),
                temp_float=Cast('temperature', FloatField()),
                hume_float=Cast('hume', FloatField())
            ).values('date').annotate(
                avg_temperature=Avg('temp_float'),
                avg_humidity=Avg('hume_float')
            ).order_by('-date')[:7]  # Últimos 7 días
            
            context['stats_data'] = list(stats)
        except Exception:
            # Si hay error con la conversión, usar lista vacía
            context['stats_data'] = []
            
    except Exception as e:
        # En caso de error, mantener los valores por defecto
        pass
    
    return render(request, 'estadisticas.html', context)
