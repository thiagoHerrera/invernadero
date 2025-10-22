# API de Comandos Manuales - Invernadero

## Descripción
Esta API permite enviar comandos manuales que serán aplicados al microcontrolador en su próxima comunicación con el endpoint `/api/parameters/`.

## Cómo funciona
1. El microcontrolador envía datos de sensores a `/api/parameters/` (POST)
2. El servidor responde con acciones automáticas O comandos manuales pendientes
3. Los comandos manuales se aplican una sola vez y luego se limpian
4. El microcontrolador lee la respuesta y aplica las acciones

## Endpoints

### 1. Establecer Comandos Manuales
**URL:** `/api/actuadores/manual/`  
**Método:** `POST`  
**Content-Type:** `application/json`

#### Parámetros de entrada:
```json
{
    "riego": true/false,           // Opcional: activar/desactivar riego
    "ventiladores": true/false     // Opcional: activar/desactivar ventiladores
}
```

#### Respuesta exitosa (200):
```json
{
    "mensaje": "Comandos manuales establecidos",
    "comandos": {
        "riego": true,
        "ventiladores": false
    },
    "timestamp": "2024-01-15T10:30:00.000Z"
}
```

### 2. Respuesta del Microcontrolador (automática)
**URL:** `/api/parameters/` (usado por el microcontrolador)  
**Método:** `POST`

El microcontrolador recibe esta respuesta que incluye comandos manuales si están pendientes:

```json
{
    "sensores": {
        "temperatura": 25.5,
        "humedad": 60.0,
        "humedad_suelo": 35.0,
        "luz": 80.0
    },
    "acciones": {
        "riego": 1,        // 1 = ON, 0 = OFF
        "ventiladores": 0,
        "tiempo": 5000
    },
    "mensaje": "Datos guardados correctamente",
    "timestamp": "2024-01-15T10:30:00.000Z"
}
```

### 3. Interfaz Web
**URL:** `/api/comandos/`  
**Método:** `GET`

Interfaz web para enviar comandos manuales desde el navegador.

## Ejemplos de uso

### Activar riego manualmente:
```bash
curl -X POST http://localhost:8000/api/actuadores/manual/ \
  -H "Content-Type: application/json" \
  -d '{"riego": true}'
```

### Desactivar ventiladores:
```bash
curl -X POST http://localhost:8000/api/actuadores/manual/ \
  -H "Content-Type: application/json" \
  -d '{"ventiladores": false}'
```

### Desde JavaScript:
```javascript
const response = await fetch('/api/actuadores/manual/', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({
        riego: true,
        ventiladores: false
    })
});

const data = await response.json();
console.log(data);
```

## Flujo de trabajo
1. **Usuario envía comando manual** → `/api/actuadores/manual/`
2. **Comando se almacena** en memoria del servidor
3. **Microcontrolador envía datos** → `/api/parameters/`
4. **Servidor responde** con comando manual (si existe) o lógica automática
5. **Microcontrolador aplica** las acciones recibidas
6. **Comando manual se limpia** automáticamente

## Notas importantes
- Los comandos manuales tienen **prioridad** sobre la lógica automática
- Cada comando manual se aplica **una sola vez**
- Si no hay comandos manuales, se aplica la lógica automática:
  - Riego: ON si humedad_suelo < 40%
  - Ventiladores: ON si temperatura > 28°C
- Compatible con el código Arduino existente
- Los valores booleanos aceptan: `true/false`, `1/0`, `"on"/"off"`, `"yes"/"no"`, `"activar"`