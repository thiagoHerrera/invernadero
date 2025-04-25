from django.urls import path
from .views import sensors
#enpoints de la api
urlpatterns = [
    path('sensors/', sensors, name='sensors'),
]
