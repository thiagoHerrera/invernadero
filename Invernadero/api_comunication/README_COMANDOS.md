# Sistema Optimizado de Control de Invernadero

## Descripción
Sistema centralizado que controla riego, ventiladores y foco desde el servidor. El microcontrolador recibe comandos cada 10 segundos.

## Arquitectura Optimizada

### Microcontrolador (ESP32)
- Envía datos de sensores cada 10 segundos
- Recibe y ejecuta comandos del servidor
- Control completamente centralizado

### Servidor (Django)
- Lógica automática basada en sensores
- Comandos manuales con prioridad
- Estado persistente en base de datos

## Endpoints

### 1. Datos de Sensores (usado por microcontrolador)
**URL:** `/api/parameters/`  
**Método:** `POST`

**Entrada:**
```json
{
    "temperatura": 25.5,
    "humedad": 60.0,
    "humedad_suelo": 35.0,
    "luz": 80.0
}
```

**Respuesta:**
```json
{
    "sensores": {
        "temperatura": 25.5,
        "humedad": 60.0,
        "humedad_suelo": 35.0,
        "luz": 80.0
    },
    "acciones": {
        "riego": 1,
        "ventiladores": 0,
        "foco": 1,
        "tiempo": 5000
    },
    "mensaje": "Datos guardados correctamente",
    "timestamp": "2024-01-15T10:30:00.000Z"
}
```

### 2. Comandos Manuales
**URL:** `/api/actuadores/manual/`  
**Método:** `POST`

```json
{
    "riego": true,
    "ventiladores": false,
    "foco": true
}
```

### 3. Estado Actual
**URL:** `/api/parameters/latest/`  
**Método:** `GET`

### 4. Interfaz Web
**URL:** `/api/comandos/`  
**Método:** `GET`

## Lógica Automática
- **Riego**: ON si humedad_suelo < 40%
- **Ventiladores**: ON si temperatura > 28°C  
- **Foco**: ON si luz < 50%

## Comandos Manuales
- Tienen prioridad sobre lógica automática
- Se aplican una sola vez
- Luego vuelve al modo automático

## Código Arduino Optimizado
```cpp
// Función principal que recibe comandos del servidor
void aplicarAcciones(int riego, int ventiladores, int foco) {
  digitalWrite(PIN_RIEGO, riego ? HIGH : LOW);
  digitalWrite(PIN_VENTILADORES, ventiladores ? HIGH : LOW);
  digitalWrite(PIN_FOCO, foco ? HIGH : LOW);
}

// Loop optimizado - envío cada 10 segundos
static unsigned long lastSend = 0;
if (millis() - lastSend > 10000 || datosCambiaron(currentData, lastSentData)) {
  enviarDatos(currentData);
  lastSend = millis();
}
```

## Características
- ✅ Control centralizado desde servidor
- ✅ Estado en tiempo real en interfaz web
- ✅ Persistencia en base de datos
- ✅ Lógica automática inteligente
- ✅ Comandos manuales prioritarios
- ✅ Comunicación optimizada cada 10s
- ✅ Interfaz web responsiva

## Uso
1. **Automático**: El sistema funciona solo basado en sensores
2. **Manual**: Usar `/api/comandos/` para control directo
3. **Monitoreo**: Estado en tiempo real en la interfaz web