# Importación de decoradores y clases de DRF (Django REST Framework)
from rest_framework.decorators import api_view, permission_classes  # Para declarar vistas basadas en funciones que aceptan solicitudes HTTP
from rest_framework.response import Response    # Para enviar respuestas HTTP con datos en formato JSON
from rest_framework import status               # Para usar códigos de estado HTTP estandarizados
from rest_framework.permissions import AllowAny

# Importaciones de Django
from django.shortcuts import render             # (No se utiliza en este archivo pero se importa por defecto)
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
import logging
import json
from datetime import datetime

# Importación del modelo Parameters desde la app users
from users.models import Parameters, Configuration
from .serializers import ParametersSerializer, ConfigurationSerializer


@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def sensors(request):
    """
    Vista que recibe datos de sensores desde un cliente (por ejemplo, un microcontrolador),
    los guarda en la base de datos y devuelve acciones sugeridas como respuesta.
    """
    try:
        # Parsear datos JSON del cuerpo de la solicitud
        if hasattr(request, 'data') and request.data:
            data = request.data
        else:
            # Fallback para datos raw
            try:
                data = json.loads(request.body.decode('utf-8'))
            except (json.JSONDecodeError, UnicodeDecodeError):
                return JsonResponse({
                    'error': 'Formato de datos inválido. Se esperaba JSON.'
                }, status=400)
        
        # Extraer y validar datos requeridos
        required_fields = ['temperatura', 'humedad', 'humedad_suelo', 'luz']
        missing_fields = [field for field in required_fields if field not in data or data[field] is None]
        
        if missing_fields:
            return JsonResponse({
                'error': f'Faltan campos requeridos: {", ".join(missing_fields)}'
            }, status=400)
        
        # Convertir y validar tipos de datos
        try:
            temperatura = float(data['temperatura'])
            humedad = float(data['humedad'])
            humedad_suelo = float(data['humedad_suelo'])
            luz = float(data['luz'])
        except (ValueError, TypeError):
            return JsonResponse({
                'error': 'Los valores deben ser numéricos'
            }, status=400)
        
        # Validar rangos lógicos
        if not (-50 <= temperatura <= 100):
            return JsonResponse({'error': 'Temperatura fuera de rango (-50 a 100°C)'}, status=400)
        if not (0 <= humedad <= 100):
            return JsonResponse({'error': 'Humedad fuera de rango (0 a 100%)'}, status=400)
        if not (0 <= humedad_suelo <= 100):
            return JsonResponse({'error': 'Humedad del suelo fuera de rango (0 a 100%)'}, status=400)
        if not (0 <= luz <= 100):
            return JsonResponse({'error': 'Luz fuera de rango (0 a 100%)'}, status=400)
        
        # Obtener configuración o usar valores por defecto
        config = Configuration.objects.first()
        temp_threshold = config.temp_max if config else 28.0
        hume_floor_threshold = config.hum_min if config else 40.0
        
        # Lógica de control automático
        riego = humedad_suelo < hume_floor_threshold
        ventiladores = temperatura > temp_threshold
        
        # Comandos manuales (opcional)
        if 'comando_riego' in data and data['comando_riego'] is not None:
            riego = bool(int(data['comando_riego']))
        if 'comando_ventiladores' in data and data['comando_ventiladores'] is not None:
            ventiladores = bool(int(data['comando_ventiladores']))
        
        # Guardar en base de datos
        param = Parameters.objects.create(
            hume=humedad,
            hume_floor=humedad_suelo,
            temperature=temperatura,
            light=luz,
            riego=riego,
            ventiladores=ventiladores,
            timestamp=timezone.now()
        )
        
        # Respuesta estructurada
        response_data = {
            "sensores": {
                "temperatura": temperatura,
                "humedad": humedad,
                "humedad_suelo": humedad_suelo,
                "luz": luz
            },
            "acciones": {
                "riego": int(riego),
                "ventiladores": int(ventiladores),
                "tiempo": 5000
            },
            "mensaje": "Datos guardados correctamente",
            "timestamp": param.timestamp.isoformat() + 'Z'
        }
        
        return JsonResponse(response_data, status=201)
        
    except Exception as e:
        return JsonResponse({
            'error': 'Error interno del servidor',
            'details': str(e)
        }, status=500)


@permission_classes([AllowAny])
@api_view(['GET'])
def get_latest_parameters(request):
    """
    Vista que obtiene el último registro guardado en la base de datos
    y lo devuelve como respuesta.

    Método permitido: GET
    
    Respuesta:
    Un diccionario con los últimos valores de temperatura, humedad, humedad del suelo, luz, riego, ventiladores.
    """
    # Obtener el último registro ingresado en el modelo Parameters
    ultimo = Parameters.objects.order_by('-id').first()
    
    if ultimo is None:
        # Si no hay datos en la base de datos, se devuelve un error 404
        return Response({'error': 'No hay datos disponibles'}, status=status.HTTP_404_NOT_FOUND)

    # Crear un diccionario con los datos del último registro
    data = {
        'temperatura': ultimo.temperature,
        'humedad': ultimo.hume,
        'humedad_suelo': ultimo.hume_floor,
        'luz': ultimo.light,
        'riego': ultimo.riego,
        'ventiladores': ultimo.ventiladores,
    }

    # Devolver los datos como respuesta HTTP
    return Response(data, status=status.HTTP_200_OK)


@permission_classes([AllowAny])
@api_view(['GET'])
def parameters_history(request):
    """
    Vista que devuelve las últimas N mediciones.
    Parámetro: limit (default 10)
    """
    limit = int(request.GET.get('limit', 10))
    params = Parameters.objects.order_by('-id')[:limit]
    serializer = ParametersSerializer(params, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@permission_classes([AllowAny])
@api_view(['GET'])
def parameters_stats(request):
    """
    Vista que devuelve promedios diarios de temperatura y humedad.
    """
    from django.db.models import Avg
    from django.db.models.functions import TruncDate

    stats = Parameters.objects.annotate(
        date=TruncDate('timestamp')
    ).values('date').annotate(
        avg_temperature=Avg('temperature'),
        avg_humidity=Avg('hume')
    ).order_by('-date')

    data = list(stats)
    return Response(data, status=status.HTTP_200_OK)


@permission_classes([AllowAny])
@api_view(['GET', 'PUT'])
def configuracion(request):
    """
    Vista para obtener o actualizar umbrales.
    """
    config = Configuration.objects.first()
    if not config:
        return Response({'error': 'No hay configuración disponible'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ConfigurationSerializer(config)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        serializer = ConfigurationSerializer(config, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@permission_classes([AllowAny])
@api_view(['POST'])
def actuadores_manual(request):
    """
    Vista para forzar encendido/apagado manual de riego o ventiladores.
    Crea un nuevo registro con las acciones especificadas.
    """
    logger = logging.getLogger(__name__)

    riego = request.data.get('riego')
    ventiladores = request.data.get('ventiladores')

    if riego is None or ventiladores is None:
        return Response({'error': 'Faltan datos: riego y ventiladores requeridos'}, status=status.HTTP_400_BAD_REQUEST)

    # Obtener el último registro para copiar sensores
    ultimo = Parameters.objects.order_by('-id').first()
    if not ultimo:
        return Response({'error': 'No hay datos previos'}, status=status.HTTP_400_BAD_REQUEST)

    # Crear nuevo registro con acciones manuales
    param = Parameters.objects.create(
        hume=ultimo.hume,
        hume_floor=ultimo.hume_floor,
        temperature=ultimo.temperature,
        light=ultimo.light,
        riego=bool(int(riego)),
        ventiladores=bool(int(ventiladores)),
        timestamp=timezone.now()
    )

    logger.info(f"Acciones manuales: riego={param.riego}, ventiladores={param.ventiladores}")

    return Response({'mensaje': 'Acciones manuales aplicadas'}, status=status.HTTP_201_CREATED)
