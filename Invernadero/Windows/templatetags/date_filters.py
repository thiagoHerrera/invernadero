from django import template
from django.utils import timezone
from datetime import datetime

register = template.Library()

@register.filter
def buenos_aires_time(parameter_obj):
    """
    Convierte la fecha del objeto a timezone de Buenos Aires usando Django
    """
    try:
        if hasattr(parameter_obj, 'timestamp'):
            # Usar timezone de Django para convertir a Buenos Aires
            # Django maneja automáticamente la conversión si USE_TZ=True
            local_time = timezone.localtime(parameter_obj.timestamp)
            return local_time.strftime("%d/%m/%Y %H:%M:%S")
        else:
            return "Fecha no disponible"
    except Exception:
        return "Fecha no disponible"