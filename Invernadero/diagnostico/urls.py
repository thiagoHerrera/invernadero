# diagnostico/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('subir/', views.subir_imagen, name='subir_imagen'),
]
