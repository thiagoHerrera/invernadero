# Importación de decoradores y clases de DRF (Django REST Framework)
from rest_framework.decorators import api_view, permission_classes  # Para declarar vistas basadas en funciones que aceptan solicitudes HTTP
from rest_framework.response import Response    # Para enviar respuestas HTTP con datos en formato JSON
from rest_framework import status               # Para usar códigos de estado HTTP estandarizados
from rest_framework.permissions import AllowAny

# Importaciones de Django
from django.shortcuts import render             # (No se utiliza en este archivo pero se importa por defecto)
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
import logging
from datetime import datetime

# Importación del modelo Parameters desde la app users
from users.models import Parameters, Configuration
from .serializers import ParametersSerializer, ConfigurationSerializer


@csrf_exempt
@permission_classes([AllowAny])
@api_view(['POST'])  # Solo permite solicitudes HTTP POST
def sensors(request):
    """
    Vista que recibe datos de sensores desde un cliente (por ejemplo, un microcontrolador o app móvil),
    los guarda en la base de datos y devuelve acciones sugeridas como respuesta.

    Datos esperados en el cuerpo del POST:
    - temperatura
    - humedad
    - humedad_suelo
    - luz
    - comando_riego (opcional)
    - comando_ventiladores (opcional)

    Respuesta:
    JSON completo con sensores, acciones, mensaje y timestamp.
    """
    logger = logging.getLogger(__name__)

    # Se extraen los valores enviados desde el cliente
    temperatura = request.data.get('temperatura')
    humedad = request.data.get('humedad')
    humedad_suelo = request.data.get('humedad_suelo')
    luz = request.data.get('luz')

    # Validación: verificar que todos los valores requeridos estén presentes
    if temperatura is None or humedad is None or humedad_suelo is None or luz is None:
        return Response({'error': 'Faltan datos'}, status=status.HTTP_400_BAD_REQUEST)

    # Obtener configuración de umbrales
    config = Configuration.objects.first()
    if not config:
        config = Configuration.objects.create()

    # Lógica automática: activar ventiladores si la temperatura supera el umbral
    riego = False
    ventiladores = False

    if float(temperatura) > config.temp_threshold:
        ventiladores = True

    if float(humedad_suelo) < config.hume_floor_threshold:
        riego = True

    # Comandos manuales enviados desde el frontend (sobrescriben lógica automática)
    comando_riego = request.data.get('comando_riego')
    comando_ventiladores = request.data.get('comando_ventiladores')

    if comando_riego is not None:
        riego = bool(int(comando_riego))
        logger.info("Se accionó el riego manualmente")

    if comando_ventiladores is not None:
        ventiladores = bool(int(comando_ventiladores))
        logger.info("Se accionó el ventilador manualmente")

    # Guardar los datos en la base de datos usando el modelo Parameters
    param = Parameters.objects.create(
        hume=float(humedad),
        hume_floor=float(humedad_suelo),
        temperature=float(temperatura),
        light=float(luz),
        riego=riego,
        ventiladores=ventiladores,
        timestamp=timezone.now()
    )

    # Respuesta JSON completa
    response_data = {
        "sensores": {
            "temperatura": float(temperatura),
            "humedad": float(humedad),
            "humedad_suelo": float(humedad_suelo),
            "luz": float(luz)
        },
        "acciones": {
            "riego": int(riego),
            "ventiladores": int(ventiladores),
            "tiempo": 5000
        },
        "mensaje": "Datos guardados correctamente",
        "timestamp": param.timestamp.isoformat() + 'Z'
    }

    # Se devuelve la respuesta con las acciones a realizar
    return Response(response_data, status=status.HTTP_201_CREATED)


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
        config = Configuration.objects.create()

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
