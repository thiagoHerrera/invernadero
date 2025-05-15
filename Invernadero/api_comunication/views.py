from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render 
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from users.models import Parameters


@api_view(['POST'])
def sensors(request):
    temperatura = request.data.get('temperatura')
    humedad = request.data.get('humedad')
    humedad_suelo = request.data.get('humedad_suelo')
    luz = request.data.get('luz')

    if temperatura is None or humedad is None or humedad_suelo is None or luz is None:
        return Response({'error': 'Faltan datos'}, status=status.HTTP_400_BAD_REQUEST)

    # Guardar en la base de datos
    Parameters.objects.create(
        hume=humedad,
        hume_floor=humedad_suelo,
        temperature=temperatura
    )
    acciones = {
        'riego' : 0,
        'ventiladores' : 0,
        'tiempo' : 5000,
        'mensaje': 'Datos guardados correctamente'
    }
    
    if temperatura > 28:
        acciones['ventiladores'] = 1
    if humedad_suelo < 40:
        acciones['riego'] = 1
        
def get_latest_parameters(request):
    ultimo = Parameters.objects.last()
    if ultimo is None:
        return Response({'error': 'No hay datos disponibles'}, status=status.HTTP_404_NOT_FOUND)

    data = {
        'temperatura': ultimo.temperature,
        'humedad': ultimo.hume,
        'humedad_suelo': ultimo.hume_floor,
    }

    return render(request, 'index.html', data)



