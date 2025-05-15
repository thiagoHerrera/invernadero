from django.urls import path
from .views import landing, home, equipo, contacto, funciones, info, estadisticas, get_latest_parameters,perfil, planta , notificaciones


urlpatterns = [
    path('', landing, name="landing"),
    path('home/', home, name='home'),
    path('equipos/', equipo, name="equipos"),
    path('contacto/', contacto, name="contacto"),
    path('funciones/', funciones, name="funciones"),
    path('informacion/', info, name="info"),
    path('estadisticas/', get_latest_parameters, name='estadisticas'),
    path('perfil/', perfil, name='perfil'),
    path('planta/',planta, name="planta"),
    path('notificaciones/',notificaciones, name="notificaciones"),

]