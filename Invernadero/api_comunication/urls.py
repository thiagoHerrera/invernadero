from django.urls import path
from .views import sensors, get_latest_parameters
#enpoints de la api
urlpatterns = [
    path('sensors/', sensors, name='sensors'),
    path('getLast/', get_latest_parameters, name='get_latest_parameters'),
]
