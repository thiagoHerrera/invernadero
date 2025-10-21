# 🚀 Despliegue en Render - FloraCore

## ❌ Problema Identificado

El error `no such table: auth_user` ocurre porque **las migraciones no se ejecutaron en producción**.

## ✅ Solución Implementada

### 1. Script de Build Automático
Creé `build.sh` que se ejecuta automáticamente en cada despliegue:

```bash
#!/usr/bin/env bash
set -o errexit

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar migraciones
python manage.py migrate

# Crear superusuario
python manage.py shell -c "..."

# Recopilar archivos estáticos
python manage.py collectstatic --noinput
```

### 2. Configuración de Producción
Actualicé `settings.py` para:
- ✅ Soporte PostgreSQL automático
- ✅ Configuración de archivos estáticos
- ✅ WhiteNoise para servir archivos
- ✅ Variables de entorno

### 3. Dependencias Corregidas
Recreé `requirements.txt` con:
- Django 5.2.7
- PostgreSQL (psycopg2-binary)
- Gunicorn
- WhiteNoise
- Todas las dependencias necesarias

## 🔧 Configuración en Render

### Variables de Entorno Requeridas:
```
DEBUG=False
DATABASE_URL=(automático con PostgreSQL)
```

### Build Command:
```
./build.sh
```

### Start Command:
```
gunicorn invernadero.wsgi:application
```

## 📁 Archivos Creados/Modificados

1. ✅ `build.sh` - Script de build automático
2. ✅ `requirements.txt` - Dependencias corregidas
3. ✅ `settings.py` - Configuración de producción
4. ✅ `render.yaml` - Configuración de Render
5. ✅ `deploy_render.py` - Script de despliegue

## 🚀 Pasos para Desplegar

### En Render Dashboard:

1. **Conectar Repositorio**
   - Conecta tu repo de GitHub

2. **Configurar Build**
   - Build Command: `./build.sh`
   - Start Command: `gunicorn invernadero.wsgi:application`

3. **Agregar Base de Datos**
   - Crear PostgreSQL database
   - Render conectará automáticamente via `DATABASE_URL`

4. **Variables de Entorno**
   ```
   DEBUG=False
   ```

5. **Deploy**
   - Render ejecutará automáticamente las migraciones

## 🔍 Verificación

Después del despliegue, verifica:

1. ✅ Migraciones aplicadas
2. ✅ Superusuario creado (admin/floracore2025)
3. ✅ Archivos estáticos servidos
4. ✅ Base de datos PostgreSQL funcionando

## 🚨 Solución Inmediata

Si el sitio ya está desplegado pero con error:

1. **Forzar Redeploy** en Render Dashboard
2. O **Ejecutar manualmente**:
   ```bash
   python manage.py migrate
   ```

## 📊 Estado Esperado

Después del despliegue correcto:
- ✅ Todas las tablas creadas
- ✅ Usuario admin disponible
- ✅ Sitio funcionando en https://floracore.onrender.com
- ✅ Sin errores de base de datos

## 🔄 Próximos Despliegues

El script `build.sh` se ejecutará automáticamente en cada push, aplicando:
- Nuevas migraciones
- Actualizaciones de dependencias
- Recopilación de archivos estáticos

¡El problema de migraciones está resuelto para siempre! 🎉