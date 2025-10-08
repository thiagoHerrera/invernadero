# Importación de la función path para definir rutas en Django
from django.urls import path

# Importación de las vistas que se van a asociar a las rutas
from .views import sensors, get_latest_parameters, parameters_history, parameters_stats, configuracion, actuadores_manual

# Endpoints de la API
urlpatterns = [
    # Ruta para recibir datos de sensores (temperatura, humedad, etc.)
    # Método HTTP esperado: POST
    # Vista asociada: sensors
    path('parameters/', sensors, name='parameters'),

    # Ruta para obtener el último conjunto de datos registrados
    # Método HTTP esperado: GET
    # Vista asociada: get_latest_parameters
    path('parameters/latest/', get_latest_parameters, name='get_latest_parameters'),

    # Ruta para obtener las últimas N mediciones
    path('parameters/history/', parameters_history, name='parameters_history'),

    # Ruta para obtener estadísticas diarias
    path('parameters/stats/', parameters_stats, name='parameters_stats'),

    # Ruta para configuración de umbrales
    path('configuracion/', configuracion, name='configuracion'),

    # Ruta para actuadores manuales
    path('actuadores/manual/', actuadores_manual, name='actuadores_manual'),
]
