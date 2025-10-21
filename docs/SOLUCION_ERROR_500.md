# Solución al Error 500 - "InvalidInput"

## Problema Identificado
El ESP32 estaba recibiendo un error HTTP 500 con el mensaje "InvalidInput" al intentar enviar datos al servidor Django. El error se debía a varios factores:

1. **Respuesta HTML en lugar de JSON**: El servidor devolvía páginas de error HTML en lugar de respuestas JSON válidas
2. **Falta de validación robusta**: El servidor no manejaba correctamente datos malformados
3. **Configuración CORS faltante**: Problemas de CORS que podían causar errores
4. **Manejo de errores insuficiente**: Tanto en Arduino como en Django

## Soluciones Implementadas

### 1. Mejoras en el Servidor Django (`api_comunication/views.py`)

- **Validación robusta de datos**: Verificación de tipos y rangos de valores
- **Manejo de errores mejorado**: Try-catch comprehensivo con logging
- **Respuestas JSON consistentes**: Uso de `JsonResponse` para garantizar formato JSON
- **Validación de rangos lógicos**: Verificar que los valores estén en rangos esperados

```python
# Validar rangos lógicos
if not (-50 <= temperatura <= 100):
    return JsonResponse({'error': 'Temperatura fuera de rango (-50 a 100°C)'}, status=400)
```

### 2. Configuración CORS (`settings.py`)

- **Agregado django-cors-headers**: Para manejar solicitudes cross-origin
- **Configuración de headers permitidos**: Accept, Content-Type, etc.
- **Métodos HTTP permitidos**: POST, GET, OPTIONS, etc.

```python
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_HEADERS = ['accept', 'content-type', 'authorization', ...]
```

### 3. Mejoras en el Código Arduino (`codigo_tesis.ino`)

- **JSON más robusto**: Uso de ArduinoJson para crear JSON válido
- **Validación de respuestas**: Verificar que la respuesta sea JSON antes de parsear
- **Manejo de errores mejorado**: Detectar respuestas HTML vs JSON
- **Headers HTTP adicionales**: User-Agent, Accept, etc.

```cpp
// Verificar si la respuesta parece ser JSON
if (response.startsWith("{") && response.endsWith("}")) {
    // Parsear JSON
} else {
    Serial.println("Error: Respuesta no es JSON válido");
}
```

### 4. Herramientas de Diagnóstico

- **Script de prueba Python** (`test_local_api.py`): Para probar la API
- **Script de diagnóstico Arduino** (`diagnostico_arduino.ino`): Para diagnosticar conectividad
- **Requirements.txt actualizado**: Con todas las dependencias necesarias

## Archivos Modificados

1. `/Invernadero/api_comunication/views.py` - Vista principal mejorada
2. `/Invernadero/invernadero/settings.py` - Configuración CORS y DRF
3. `/Invernadero/requirements.txt` - Dependencias actualizadas
4. `/Invernadero/codigo_tesis.ino` - Código Arduino mejorado

## Archivos Nuevos

1. `/test_local_api.py` - Script de prueba de API
2. `/diagnostico_arduino.ino` - Script de diagnóstico
3. `/SOLUCION_ERROR_500.md` - Este documento

## Pasos para Implementar

1. **Actualizar el servidor Django**:
   ```bash
   pip install -r requirements.txt
   python manage.py migrate
   python manage.py runserver
   ```

2. **Probar la API**:
   ```bash
   python test_local_api.py
   ```

3. **Cargar el código mejorado al ESP32**:
   - Usar el archivo `codigo_tesis.ino` actualizado
   - O usar `diagnostico_arduino.ino` para diagnóstico

4. **Verificar logs**:
   - Monitorear el Serial Monitor del Arduino
   - Revisar logs del servidor Django

## Resultados Esperados

- ✅ Respuestas JSON válidas del servidor
- ✅ Manejo robusto de errores
- ✅ Comunicación estable ESP32 ↔ Servidor
- ✅ Logs informativos para debugging
- ✅ Validación de datos de entrada

## Troubleshooting

Si persisten los problemas:

1. Usar el script de diagnóstico Arduino
2. Verificar conectividad WiFi y DNS
3. Probar la API con el script Python
4. Revisar logs del servidor Django
5. Verificar que el servidor esté desplegado correctamente en Render