from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Parameters(models.Model):
    hume = models.CharField(max_length=20)
    hume_floor = models.CharField(max_length=20)
    temperature = models.CharField(max_length=20)
    light = models.CharField(max_length=20)
    
class GrenHouse(models.Model):
    nombre = models.CharField(max_length=100)
    id_user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_parameters = models.ForeignKey(Parameters, on_delete=models.CASCADE)