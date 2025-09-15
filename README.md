# Invernadero

Sistema de monitoreo inteligente para invernaderos con autenticación 2FA, API REST y análisis de imágenes.

## 🚀 Despliegue en Render

### Prerrequisitos

1. Cuenta en [Render](https://render.com)
2. Repositorio Git con este código

### Configuración del Despliegue

1. **Conectar el repositorio:**
   - Ve a Render Dashboard
   - Click en "New" → "Web Service"
   - Conecta tu repositorio de Git

2. **Configuración automática:**
   - Render detectará automáticamente el `render.yaml`
   - Se creará la base de datos PostgreSQL automáticamente
   - Las variables de entorno se configurarán automáticamente

3. **Variables de entorno adicionales (opcionales):**
   - Si necesitas configurar email, agrega estas variables en Render:
     - `EMAIL_HOST_USER`: tu-email@gmail.com
     - `EMAIL_HOST_PASSWORD`: tu-contraseña-app

### Archivos de Configuración

- `render.yaml`: Configuración del servicio web y base de datos
- `start.sh`: Script de inicio que ejecuta migraciones y collectstatic
- `requirements.txt`: Dependencias de Python para producción
- `.env.example`: Ejemplo de variables de entorno

### Configuración de Settings

El proyecto usa configuración modular:
- `settings/base.py`: Configuración común
- `settings/production.py`: Configuración para producción
- `settings/development.py`: Configuración para desarrollo

La variable `DJANGO_ENV` determina qué configuración usar:
- `production`: Para despliegue en Render
- `development`: Para desarrollo local

### Base de Datos

- **Desarrollo**: SQLite (incluido en el repositorio)
- **Producción**: PostgreSQL (creado automáticamente por Render)

### Comandos Importantes

```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar migraciones
python Invernadero/manage.py migrate

# Recopilar archivos estáticos
python Invernadero/manage.py collectstatic --noinput

# Ejecutar servidor de desarrollo
python Invernadero/manage.py runserver
```

### URLs Importantes

- **Aplicación**: `https://tu-app.onrender.com`
- **Admin**: `https://tu-app.onrender.com/admin/`

### Características

- ✅ Autenticación de usuarios con 2FA
- ✅ API REST completa
- ✅ Análisis de imágenes para diagnóstico de plantas
- ✅ Dashboard administrativo
- ✅ Sistema de notificaciones
- ✅ Optimización de imágenes
- ✅ Servidor de archivos estáticos optimizado

### Tecnologías

- **Backend**: Django 5.2.6
- **Base de Datos**: PostgreSQL (producción) / SQLite (desarrollo)
- **Autenticación**: Django OTP + 2FA
- **API**: Django REST Framework
- **Archivos Estáticos**: WhiteNoise
- **Servidor WSGI**: Gunicorn
- **Despliegue**: Render

### Desarrollo Local

1. Clona el repositorio
2. Crea entorno virtual: `python -m venv venv`
3. Activa entorno: `source venv/bin/activate`
4. Instala dependencias: `pip install -r requirements.txt`
5. Ejecuta migraciones: `cd Invernadero && python manage.py migrate`
6. Ejecuta servidor: `python manage.py runserver`

### 🚨 Solución de Problemas de Despliegue

Si encuentras el error `"py: command not found"` en Render:

#### Opción 1: Recrear el Servicio
1. Elimina el servicio web actual en Render
2. Crea un nuevo servicio web conectando el mismo repositorio
3. Render debería detectar automáticamente `render.yaml`

#### Opción 2: Configuración Manual
Si Render no detecta `render.yaml`, configura manualmente:
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `bash start.sh`

#### Opción 3: Usar Script Alternativo
- Usa `render-deploy.yaml` en lugar de `render.yaml`
- O usa `render-manual.sh` como start command: `bash render-manual.sh`

#### Verificación
Después de aplicar cualquier solución:
1. Revisa los logs en Render Dashboard
2. Verifica que las variables de entorno estén configuradas
3. Confirma que la base de datos PostgreSQL esté conectada

### Contribución

1. Fork el proyecto
2. Crea una rama para tu feature
3. Commit tus cambios
4. Push a la rama
5. Abre un Pull Request

### Licencia

Este proyecto está bajo la Licencia MIT.