# Solución para Problemas de Despliegue en Render

## Problemas Identificados

### 1. Error de Base de Datos: `no such table: auth_user`
**Causa**: Las migraciones no se ejecutaron correctamente en Render.

### 2. CSS no se carga en login, register y recuperar contraseña
**Causa**: Configuración incorrecta de archivos estáticos con WhiteNoise.

## Soluciones Implementadas

### 1. Configuración de Base de Datos Mejorada

**Archivo**: `settings.py`
- Habilitado `STATICFILES_STORAGE` para WhiteNoise
- Configurado `DEBUG` basado en variable de entorno

### 2. Script de Build Mejorado

**Archivo**: `build.sh`
```bash
#!/usr/bin/env bash
set -o errexit

echo "Instalando dependencias..."
pip install -r requirements.txt

echo "Ejecutando migraciones..."
python manage.py makemigrations
python manage.py migrate --run-syncdb

echo "Creando superusuario..."
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(is_superuser=True).exists():
    User.objects.create_superuser('admin', 'admin@floracore.com', 'floracore2025')
    print('Superusuario creado')
else:
    print('Superusuario ya existe')
"

echo "Recopilando archivos estáticos..."
python manage.py collectstatic --noinput --clear

echo "Build completado exitosamente"
```

### 3. Requirements.txt Corregido

**Archivo**: `requirements.txt`
- Corregido formato corrupto
- Agregado `gunicorn==23.0.0`
- Mantenidas todas las dependencias necesarias

### 4. Configuración de Render Mejorada

**Archivo**: `render.yaml`
```yaml
services:
  - type: web
    name: floracore
    env: python
    buildCommand: "chmod +x build.sh && ./build.sh"
    startCommand: "gunicorn invernadero.wsgi:application --bind 0.0.0.0:$PORT"
    envVars:
      - key: DEBUG
        value: "False"
      - key: DJANGO_SETTINGS_MODULE
        value: "invernadero.settings"
      - key: PYTHONPATH
        value: "/opt/render/project/src/Invernadero"
```

## Pasos para Redesplegar

### 1. Hacer Commit de los Cambios
```bash
git add .
git commit -m "Fix: Configurar base de datos PostgreSQL y solucionar CSS"
git push origin main
```

### 2. En Render Dashboard

#### Opción A: Usar render.yaml (Recomendado)
1. El archivo `render.yaml` creará automáticamente:
   - Servicio web `floracore`
   - Base de datos PostgreSQL `floracore-db`
   - Conexión automática entre ambos

#### Opción B: Configuración Manual
1. Crear base de datos PostgreSQL:
   - New > PostgreSQL
   - Name: `floracore-db`
   - Plan: Free
2. Crear/actualizar servicio web:
   - Conectar al repositorio
   - Environment: Python 3
   - Build Command: `./build.sh`
   - Start Command: `gunicorn invernadero.wsgi:application`

### 3. Variables de Entorno (si usas configuración manual)
- `DEBUG=False`
- `DJANGO_SETTINGS_MODULE=invernadero.settings`
- `DATABASE_URL` (se conecta automáticamente desde la BD PostgreSQL)

### 4. Monitorear el Deploy
- Revisa los logs de build para errores
- Verifica que las migraciones se ejecuten correctamente
- Confirma que los archivos estáticos se recopilen

## Archivos Estáticos - Estructura Esperada

```
Invernadero/
├── static/                 # Archivos estáticos globales
├── users/static/          # CSS de login, register, password reset
│   ├── css/
│   │   ├── login.css
│   │   ├── register.css
│   │   └── password_reset.css
│   └── img/
└── staticfiles/           # Generado por collectstatic (no versionar)
```

## Verificación Post-Despliegue

### 1. Verificar Base de Datos
- Accede a `/admin/` y verifica que puedas hacer login
- Usuario: `admin`
- Contraseña: `floracore2025`

### 2. Verificar CSS
- Ve a `/users/signin/`
- Verifica que el CSS se cargue correctamente
- Inspecciona elementos para confirmar que los estilos se aplican

### 3. Verificar Funcionalidad
- Prueba login/logout
- Prueba registro de usuarios
- Prueba recuperación de contraseña

## Comandos de Diagnóstico

Si sigues teniendo problemas, puedes usar estos comandos en el shell de Render:

```bash
# Verificar migraciones
python manage.py showmigrations

# Verificar archivos estáticos
python manage.py collectstatic --dry-run

# Verificar configuración
python manage.py check --deploy
```

## Notas Importantes

1. **WhiteNoise**: Ahora está correctamente configurado para servir archivos estáticos
2. **Migraciones**: Se ejecutan con `--run-syncdb` para crear tablas faltantes
3. **Debug**: Deshabilitado en producción
4. **Archivos Estáticos**: Se limpian y recopilan en cada deploy

## Contacto de Emergencia

Si los problemas persisten:
1. Revisa los logs de Render en tiempo real
2. Verifica que todos los archivos se hayan subido correctamente
3. Confirma que las variables de entorno estén configuradas
4. Considera hacer un redeploy completo desde cero si es necesario