from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import pytz

# Create your models here.
class Parameters(models.Model):
    hume = models.CharField(max_length=20)
    hume_floor = models.CharField(max_length=20)
    temperature = models.CharField(max_length=20)
    light = models.CharField(max_length=20, default="0")
    riego = models.BooleanField(default=False)
    ventiladores = models.BooleanField(default=False)
    foco = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def get_buenos_aires_time(self):
        """Retorna el timestamp convertido al timezone de Buenos Aires"""
        buenos_aires_tz = pytz.timezone('America/Argentina/Buenos_Aires')
        if self.timestamp.tzinfo is None:
            utc_time = pytz.UTC.localize(self.timestamp)
        else:
            utc_time = self.timestamp
        return utc_time.astimezone(buenos_aires_tz)
    
    class Meta:
        ordering = ['-timestamp']


class GrenHouse(models.Model):
    nombre = models.CharField(max_length=100)
    id_user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_parameters = models.ForeignKey(Parameters, on_delete=models.CASCADE)

class Configuration(models.Model):
    temp_min = models.FloatField(default=20.0)
    temp_max = models.FloatField(default=25.0)
    hum_min = models.FloatField(default=60.0)
    hum_max = models.FloatField(default=80.0)
    light_hours = models.IntegerField(default=12)
    auto_watering = models.BooleanField(default=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)