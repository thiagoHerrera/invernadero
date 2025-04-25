from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


@api_view(['POST'])
def sensors(request):
    """
    Recibe datos en JSON de los sensores y responde con confirmación.
    """
    #obtener valores del JSON
    sensor1 = request.data.get('sensor1')
    sensor2 = request.data.get('sensor2')
    sensor3 = request.data.get('sensor3')

    #ver que los valores no esten vacios
    if sensor1 is None or sensor2 is None or sensor3 is None:
        #responde con el codigo 400
        return Response({'error': 'Faltan datos de sensores'}, status=status.HTTP_400_BAD_REQUEST)

    #responder a la esp32
    return Response({'mensaje': 'Datos recibidos correctamente'}, status=status.HTTP_200_OK)
    

