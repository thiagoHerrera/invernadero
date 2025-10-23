# Códigos Arduino para Sistema de Invernadero

## Versiones Disponibles

### 1. `codigo_tesis.ino` - Versión GitHub Codespaces
- **URL**: `https://fantastic-xylophone-4jwvw4jpxj792q66v-8000.app.github.dev/api/parameters/`
- **Problema**: GitHub Codespaces requiere autenticación (error 401)
- **Uso**: Solo para desarrollo en Codespaces con autenticación

### 2. `codigo_tesis_local.ino` - Versión Local HTTP
- **URL**: `http://localhost:8000/api/parameters/`
- **Protocolo**: HTTP (sin SSL)
- **Uso**: Testing local en red privada
- **Estado**: ✅ Funciona correctamente

### 3. `codigo_tesis_produccion.ino` - Versión Producción
- **URL**: `https://floracore.onrender.com/api/parameters/`
- **Protocolo**: HTTPS con SSL
- **Uso**: Producción real con servidor Render
- **Estado**: ✅ Recomendado para uso real

## Características Comunes

### Sensores Soportados
- **DHT11**: Temperatura y humedad ambiente (Pin 4)
- **Sensor de humedad de suelo**: Analógico (Pin 34)
- **Sensor de luz**: LDR analógico (Pin 35)

### Actuadores Controlados
- **Riego**: Relé en Pin 26
- **Ventiladores**: Relé en Pin 27  
- **Foco/Luz**: Relé en Pin 25

### Comunicación
- **Frecuencia**: Cada 10 segundos o cuando hay cambios significativos
- **Formato**: JSON con datos de sensores
- **Respuesta**: JSON con acciones para actuadores

### Lógica Automática (Servidor)
- **Riego**: ON si humedad_suelo < 40%
- **Ventiladores**: ON si temperatura > 28°C
- **Foco**: ON si luz < 50%

### Comandos Manuales
- Tienen prioridad sobre lógica automática
- Se aplican una sola vez
- Controlados desde interfaz web `/api/comandos/`

## Estructura de Comunicación

### Datos Enviados (Arduino → Servidor)
```json
{
    "temperatura": 25.5,
    "humedad": 60.0,
    "humedad_suelo": 35.0,
    "luz": 80.0
}
```

### Respuesta Recibida (Servidor → Arduino)
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

## Configuración WiFi
```cpp
const char* ssid = "Cereza";
const char* password = "robotica25";
```

## Recomendación de Uso

1. **Desarrollo Local**: Usar `codigo_tesis_local.ino`
2. **Producción**: Usar `codigo_tesis_produccion.ino`
3. **GitHub Codespaces**: Requiere configuración adicional de autenticación

## Monitoreo Serial
- Baudrate: 115200
- Logs detallados de sensores, comunicación y actuadores
- Información de conexión WiFi y errores