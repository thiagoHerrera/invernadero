# Importación de decoradores y clases de DRF (Django REST Framework)
from rest_framework.decorators import api_view  # Para declarar vistas basadas en funciones que aceptan solicitudes HTTP
from rest_framework.response import Response    # Para enviar respuestas HTTP con datos en formato JSON
from rest_framework import status               # Para usar códigos de estado HTTP estandarizados

# Importaciones de Django
from django.shortcuts import render             # (No se utiliza en este archivo pero se importa por defecto)

# Importación del modelo Parameters desde la app users
from users.models import Parameters


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
    Un diccionario con instrucciones sobre riego y ventilación.
    """
    # Se extraen los valores enviados desde el cliente
    temperatura = request.data.get('temperatura')
    humedad = request.data.get('humedad')
    humedad_suelo = request.data.get('humedad_suelo')
    luz = request.data.get('luz')

    # Validación: verificar que todos los valores requeridos estén presentes
    if temperatura is None or humedad is None or humedad_suelo is None or luz is None:
        return Response({'error': 'Faltan datos'}, status=status.HTTP_400_BAD_REQUEST)

    # Guardar los datos en la base de datos usando el modelo Parameters
    Parameters.objects.create(
        hume=humedad,
        hume_floor=humedad_suelo,
        temperature=temperatura
    )

    # Diccionario con acciones a tomar por el sistema (ej. riego y ventiladores)
    acciones = {
        'riego': 0,
        'ventiladores': 0,
        'tiempo': 5000,  # Tiempo en milisegundos para mantener activa la acción
        'mensaje': 'Datos guardados correctamente'
    }
    
    # Lógica automática: activar ventiladores si la temperatura supera los 28°C
    if temperatura > 28:
        acciones['ventiladores'] = 1

    # Activar riego si la humedad del suelo es menor a 40%
    if humedad_suelo < 40:
        acciones['riego'] = 1

    # Comandos manuales enviados desde el frontend (sobrescriben lógica automática)
    comando_riego = request.data.get('comando_riego')
    comando_ventiladores = request.data.get('comando_ventiladores')

    if comando_riego is not None:
        acciones['riego'] = int(comando_riego)
        print("se acciono el riego")

    if comando_ventiladores is not None:
        acciones['ventiladores'] = int(comando_ventiladores)
        print("se acciono ventilador")

    # Se devuelve la respuesta con las acciones a realizar
    return Response(acciones, status=status.HTTP_201_CREATED)


def get_latest_parameters(request):
    """
    Vista que obtiene el último registro guardado en la base de datos
    y lo devuelve como respuesta.

    Método permitido: GET (no está decorado con @api_view, pero se asume uso interno o mediante configuración)
    
    Respuesta:
    Un diccionario con los últimos valores de temperatura, humedad y humedad del suelo.
    """
    # Obtener el último registro ingresado en el modelo Parameters
    ultimo = Parameters.objects.last()
    
    if ultimo is None:
        # Si no hay datos en la base de datos, se devuelve un error 404
        return Response({'error': 'No hay datos disponibles'}, status=status.HTTP_404_NOT_FOUND)

    # Crear un diccionario con los datos del último registro
    data = {
        'temperatura': ultimo.temperature,
        'humedad': ultimo.hume,
        'humedad_suelo': ultimo.hume_floor,
    }

    # Devolver los datos como respuesta HTTP
    return Response(data, status=status.HTTP_200_OK)
