# Importación de la función path para definir rutas en Django
from django.urls import path

# Importación de las vistas que se van a asociar a las rutas
from .views import sensors, get_latest_parameters

# Endpoints de la API
urlpatterns = [
    # Ruta para recibir datos de sensores (temperatura, humedad, etc.)
    # Método HTTP esperado: POST
    # Vista asociada: sensors
    # Nombre interno de la ruta: 'sensors'
    path('sensors/', sensors, name='sensors'),

    # Ruta para obtener el último conjunto de datos registrados
    # Método HTTP esperado: GET
    # Vista asociada: get_latest_parameters
    # Nombre interno de la ruta: 'get_latest_parameters'
    path('getLast/', get_latest_parameters, name='get_latest_parameters'),
]
