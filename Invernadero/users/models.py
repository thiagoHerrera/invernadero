from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Parameters(models.Model):
    hume = models.FloatField()  # humedad
    hume_floor = models.FloatField()  # humedad_suelo
    temperature = models.FloatField()
    light = models.FloatField(default=0)
    riego = models.BooleanField(default=False)  # acción de riego
    ventiladores = models.BooleanField(default=False)  # acción de ventiladores
    timestamp = models.DateTimeField()

    class Meta:
        ordering = ['-id']


class GrenHouse(models.Model):
    nombre = models.CharField(max_length=100)
    id_user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_parameters = models.ForeignKey(Parameters, on_delete=models.CASCADE)


class Configuration(models.Model):
    temp_threshold = models.FloatField(default=28.0)  # umbral temperatura para ventiladores
    hume_floor_threshold = models.FloatField(default=40.0)  # umbral humedad suelo para riego
    light_threshold = models.FloatField(default=500.0)  # umbral luz si necesario