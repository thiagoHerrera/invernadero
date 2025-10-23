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

# Variables globales para control manual persistente
comandos_manuales = {'riego': None, 'ventiladores': None, 'foco': None}
modo_manual = {'riego': False, 'ventiladores': False, 'foco': False}
estados_manuales = {'riego': False, 'ventiladores': True, 'foco': True}  # Estados cuando están en manual

@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def sensors(request):
    """
    Vista que recibe datos de sensores desde un cliente (por ejemplo, un microcontrolador),
    los guarda en la base de datos y devuelve acciones sugeridas como respuesta.
    """
    global comandos_manuales
    
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
        
        # Convertir y validar tipos de datos (acepta números y cadenas)
        def convert_to_float(value, field_name):
            if isinstance(value, (int, float)):
                return float(value)
            elif isinstance(value, str):
                try:
                    return float(value.strip())
                except ValueError:
                    raise ValueError(f"El campo '{field_name}' debe ser un número válido")
            else:
                raise ValueError(f"El campo '{field_name}' debe ser un número o cadena numérica")
        
        try:
            temperatura = convert_to_float(data['temperatura'], 'temperatura')
            humedad = convert_to_float(data['humedad'], 'humedad')
            humedad_suelo = convert_to_float(data['humedad_suelo'], 'humedad_suelo')
            luz = convert_to_float(data['luz'], 'luz')
        except ValueError as e:
            return JsonResponse({
                'error': str(e)
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
        
        # Valores por defecto para control automático
        temp_threshold = 28.0
        hume_floor_threshold = 40.0
        
        # Aplicar comandos manuales y activar modo manual persistente
        if comandos_manuales['riego'] is not None:
            modo_manual['riego'] = True
            estados_manuales['riego'] = comandos_manuales['riego']
            comandos_manuales['riego'] = None
            
        if comandos_manuales['ventiladores'] is not None:
            modo_manual['ventiladores'] = True
            estados_manuales['ventiladores'] = comandos_manuales['ventiladores']
            comandos_manuales['ventiladores'] = None
            
        if comandos_manuales['foco'] is not None:
            modo_manual['foco'] = True
            estados_manuales['foco'] = comandos_manuales['foco']
            comandos_manuales['foco'] = None
        
        # Determinar estados finales
        riego = estados_manuales['riego'] if modo_manual['riego'] else (humedad_suelo < hume_floor_threshold)
        ventiladores = estados_manuales['ventiladores'] if modo_manual['ventiladores'] else (temperatura > 24.0)
        foco = estados_manuales['foco'] if modo_manual['foco'] else True
        
        # Guardar en base de datos
        param = Parameters.objects.create(
            hume=humedad,
            hume_floor=humedad_suelo,
            temperature=temperatura,
            light=luz,
            riego=riego,
            ventiladores=ventiladores,
            foco=foco,
            timestamp=timezone.now()
        )
        
        # Respuesta estructurada compatible con el microcontrolador
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
                "foco": int(foco),
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
        'foco': ultimo.foco,
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
        serializer = ConfigurationSerializer(config, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def actuadores_manual(request):
    """
    Vista para establecer comandos manuales que serán aplicados
    en la próxima respuesta al microcontrolador.
    """
    global comandos_manuales
    
    try:
        data = request.data if hasattr(request, 'data') and request.data else json.loads(request.body.decode('utf-8'))
        
        def convert_to_bool(value):
            if isinstance(value, bool):
                return value
            elif isinstance(value, (int, float)):
                return bool(int(value))
            elif isinstance(value, str):
                value = value.strip().lower()
                return value in ['true', '1', 'on', 'yes', 'activar']
            return False
        
        # Establecer comandos manuales
        if 'riego' in data:
            comandos_manuales['riego'] = convert_to_bool(data['riego'])
        if 'ventiladores' in data:
            comandos_manuales['ventiladores'] = convert_to_bool(data['ventiladores'])
        if 'foco' in data:
            comandos_manuales['foco'] = convert_to_bool(data['foco'])
        
        return JsonResponse({
            'mensaje': 'Comandos manuales establecidos',
            'comandos': comandos_manuales,
            'timestamp': timezone.now().isoformat() + 'Z'
        }, status=200)
        
    except Exception as e:
        return JsonResponse({
            'error': 'Error procesando comandos',
            'details': str(e)
        }, status=500)


@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def modo_automatico(request):
    """
    Vista para volver al modo automático.
    """
    global modo_manual
    
    modo_manual = {'riego': False, 'ventiladores': False, 'foco': False}
    
    return JsonResponse({
        'mensaje': 'Modo automático activado',
        'timestamp': timezone.now().isoformat() + 'Z'
    }, status=200)


@permission_classes([AllowAny])
def comandos_manual_view(request):
    """
    Vista para mostrar la interfaz web de comandos manuales.
    """
    return render(request, 'comandos_manual.html')