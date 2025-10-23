from django import template
from django.utils import timezone
from datetime import datetime
import pytz

register = template.Library()

@register.filter
def format_api_date(value):
    """
    Formatea fechas que vienen del API y las convierte al timezone de Buenos Aires
    """
    if not value:
        return "No disponible"
    
    try:
        # Timezone de Buenos Aires
        buenos_aires_tz = pytz.timezone('America/Argentina/Buenos_Aires')
        
        # Si es una cadena, intentar parsearla
        if isinstance(value, str):
            # Manejar diferentes formatos de fecha ISO
            if 'T' in value:
                # Formato ISO con T
                if value.endswith('Z'):
                    value = value[:-1] + '+00:00'
                elif '+' not in value and '-' not in value[-6:]:
                    value = value + '+00:00'
                
                dt = datetime.fromisoformat(value)
            else:
                # Intentar parsear otros formatos
                dt = datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
                dt = pytz.UTC.localize(dt)
            
            # Convertir a timezone de Buenos Aires
            if dt.tzinfo is None:
                dt = pytz.UTC.localize(dt)
            
            buenos_aires_dt = dt.astimezone(buenos_aires_tz)
            return buenos_aires_dt.strftime("%d/%m/%Y %H:%M:%S")
        
        # Si ya es un objeto datetime
        elif isinstance(value, datetime):
            if value.tzinfo is None:
                value = pytz.UTC.localize(value)
            
            buenos_aires_dt = value.astimezone(buenos_aires_tz)
            return buenos_aires_dt.strftime("%d/%m/%Y %H:%M:%S")
        
        else:
            return str(value)
            
    except (ValueError, TypeError, AttributeError) as e:
        # En caso de error, intentar mostrar el valor original
        return str(value)

@register.filter
def buenos_aires_time(parameter_obj):
    """
    Usa el método del modelo para obtener la fecha en Buenos Aires
    """
    try:
        if hasattr(parameter_obj, 'get_buenos_aires_time'):
            ba_time = parameter_obj.get_buenos_aires_time()
            return ba_time.strftime("%d/%m/%Y %H:%M:%S")
        else:
            return format_api_date(parameter_obj)
    except Exception:
        return "Fecha no disponible"