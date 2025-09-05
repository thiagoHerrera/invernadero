from django.urls import path
from .views import landing, home, equipo, contacto, funciones, info, historialcultivo


urlpatterns = [
    path('', landing, name="landing"),
    path('home/', home, name='home'),
    path('equipos/', equipo, name="equipos"),
    path('contacto/', contacto, name="contacto"),
    path('funciones/', funciones, name="funciones"),
    path('informacion/', info, name="info"),
    path('historialcultivo/', historialcultivo, name='historialcultivo'),

]