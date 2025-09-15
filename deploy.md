# 🚀 Guía de Despliegue - Sistema Invernadero

## 📋 Información General

**Proyecto**: Sistema de Monitoreo Inteligente para Invernaderos
**Framework**: Django 5.2.6
**Plataforma de Despliegue**: Render
**Base de Datos**: PostgreSQL (producción) / SQLite (desarrollo)

## 👥 Equipo Responsable

- **Desarrollador Principal**: [Tu Nombre]
- **Fecha de Creación**: Diciembre 2024
- **Versión**: 1.0.0

---

## 📁 Estructura del Proyecto

```
invernadero/
├── Invernadero/                    # Proyecto Django principal
│   ├── invernadero/               # Configuración del proyecto
│   │   ├── settings/              # Configuración modular
│   │   │   ├── __init__.py
│   │   │   ├── base.py            # Configuración común
│   │   │   ├── production.py      # Configuración producción
│   │   │   └── development.py     # Configuración desarrollo
│   │   ├── settings.py            # Punto de entrada
│   │   ├── urls.py
│   │   ├── wsgi.py
│   │   └── asgi.py
│   ├── users/                     # App de usuarios
│   ├── Authentication/            # App de autenticación
│   ├── Verificacion2FA/           # App de 2FA
│   ├── api_comunication/          # App de API
│   ├── diagnostico/               # App de diagnóstico
│   ├── Windows/                   # App de interfaz
│   ├── db.sqlite3                 # Base de datos desarrollo
│   ├── manage.py
│   └── start.bat                  # Script Windows (legacy)
├── requirements.txt               # Dependencias Python
├── render.yaml                   # Configuración Render
├── start.sh                      # Script de inicio
├── .env.example                  # Variables de entorno ejemplo
├── .gitignore                    # Archivos ignorados
├── README.md                     # Documentación general
└── deploy.md                     # Esta guía
```

---

## 🔧 Prerrequisitos

### Para Desarrollo Local
- **Python**: 3.8 o superior
- **Git**: Para control de versiones
- **Virtualenv**: Para entornos virtuales

### Para Despliegue en Producción
- **Cuenta en Render**: [render.com](https://render.com)
- **Repositorio Git**: GitHub, GitLab o Bitbucket
- **Credenciales de Email**: Para notificaciones (opcional)

### Conocimientos Requeridos
- Python y Django
- Bases de datos SQL
- Git y control de versiones
- Conceptos básicos de despliegue web

---

## 🛠️ Configuración de Desarrollo Local

### 1. Clonar el Repositorio
```bash
git clone [URL_DEL_REPOSITORIO]
cd invernadero
```

### 2. Crear Entorno Virtual
```bash
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 3. Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar Base de Datos
```bash
cd Invernadero
python manage.py migrate
```

### 5. Crear Superusuario (Opcional)
```bash
python manage.py createsuperuser
```

### 6. Ejecutar Servidor de Desarrollo
```bash
python manage.py runserver
```

**URL de Desarrollo**: http://127.0.0.1:8000

---

## 🚀 Proceso de Despliegue en Render

### Paso 1: Preparar el Repositorio
1. Asegúrate de que todos los cambios estén commiteados
2. Verifica que `.gitignore` excluya archivos sensibles
3. Sube el código a tu repositorio Git

### Paso 2: Crear Servicio en Render
1. Ve a [render.com](https://render.com) y accede a tu cuenta
2. Haz clic en **"New"** → **"Web Service"**
3. Conecta tu repositorio Git
4. Configura el servicio:

#### Configuración del Servicio Web
- **Name**: invernadero (o el nombre que prefieras)
- **Runtime**: Python 3
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `sh start.sh`

### Paso 3: Configurar Base de Datos
Render creará automáticamente una base de datos PostgreSQL. Las variables de entorno se configurarán automáticamente gracias al `render.yaml`.

### Paso 4: Variables de Entorno Adicionales
En el dashboard de Render, agrega estas variables si son necesarias:

```bash
# Email Configuration (Opcional)
EMAIL_HOST_USER=tu-email@gmail.com
EMAIL_HOST_PASSWORD=tu-app-password
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True

# Otras configuraciones personalizadas
DJANGO_SETTINGS_MODULE=invernadero.settings.production
```

### Paso 5: Desplegar
1. Haz clic en **"Create Web Service"**
2. Render comenzará el proceso de construcción automático
3. El despliegue tomará aproximadamente 5-10 minutos

---

## ⚙️ Configuración de Variables de Entorno

### Variables Automáticas (Configuradas por Render)
- `DJANGO_ENV`: production
- `SECRET_KEY`: Generada automáticamente
- `DEBUG`: false
- `ALLOWED_HOSTS`: URL de tu app en Render
- `DB_NAME`: Nombre de la base de datos
- `DB_USER`: Usuario de la base de datos
- `DB_PASSWORD`: Contraseña de la base de datos
- `DB_HOST`: Host de la base de datos
- `DB_PORT`: Puerto de la base de datos

### Variables Manuales (Opcionales)
```bash
# Email
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=tu-email@gmail.com
EMAIL_HOST_PASSWORD=tu-app-password

# Otras
TIME_ZONE=America/Mexico_City
LANGUAGE_CODE=es-mx
```

---

## 🔍 Verificación del Despliegue

### 1. Verificar que la App esté Ejecutándose
- Ve a la URL proporcionada por Render
- Deberías ver la página principal del sistema

### 2. Verificar Base de Datos
- Accede al admin: `https://tu-app.onrender.com/admin/`
- Intenta crear un usuario o verificar datos existentes

### 3. Verificar API
- Prueba endpoints de la API: `https://tu-app.onrender.com/api/`

### 4. Verificar Archivos Estáticos
- Verifica que CSS, JS e imágenes se carguen correctamente

---

## 🐛 Solución de Problemas Comunes

### Error: "py: command not found"
**Síntomas**: Render ejecuta `py manage.py runserver` y falla porque `py` no existe
**Solución**:
1. **Verifica que Render use `render.yaml`**:
   - Asegúrate de que `render.yaml` esté en la raíz del repositorio
   - Si Render no lo detecta, elimina el servicio y crea uno nuevo
   - O usa `render-deploy.yaml` como alternativa

2. **Configuración manual en Render**:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `bash start.sh`
   - Asegúrate de que `start.sh` tenga permisos de ejecución

3. **Variables de entorno requeridas**:
   - `DJANGO_ENV=production`
   - `DEBUG=False`
   - Configurar base de datos PostgreSQL

### Error: "Build Failed"
**Síntomas**: El despliegue falla durante la construcción
**Solución**:
1. Verifica que `requirements.txt` esté correcto
2. Asegúrate de que `start.sh` tenga permisos de ejecución
3. Revisa los logs de construcción en Render

### Error: "Database Connection Failed"
**Síntomas**: Error al conectar con PostgreSQL
**Solución**:
1. Verifica que las variables de DB sean correctas
2. Asegúrate de que la base de datos esté creada
3. Revisa las credenciales en el dashboard de Render

### Error: "Static Files Not Loading"
**Síntomas**: CSS/JS no se cargan en producción
**Solución**:
1. Verifica que `collectstatic` se ejecute en `start.sh`
2. Confirma que WhiteNoise esté configurado correctamente
3. Revisa que `STATIC_ROOT` esté definido

### Error: "500 Internal Server Error"
**Síntomas**: Error del servidor en producción
**Solución**:
1. Revisa los logs de la aplicación en Render
2. Verifica configuración de `DEBUG=False`
3. Confirma que `SECRET_KEY` esté configurada
4. Revisa configuración de `ALLOWED_HOSTS`

---

## 📊 Monitoreo y Mantenimiento

### Logs de Aplicación
- En Render Dashboard → Service → Logs
- Revisa errores y mensajes importantes

### Base de Datos
- Accede vía Render Dashboard → Database
- Monitorea uso y conexiones

### Rendimiento
- Monitorea tiempos de respuesta
- Revisa uso de CPU y memoria
- Considera upgrade de plan si es necesario

### Backups
- Render hace backups automáticos de la base de datos
- Configura backups adicionales si es crítico

---

## 🔄 Actualizaciones y Despliegues

### Proceso de Actualización
1. **Desarrollo Local**:
   ```bash
   git checkout -b feature/nueva-funcionalidad
   # Realiza cambios
   git commit -m "Nueva funcionalidad"
   git push origin feature/nueva-funcionalidad
   ```

2. **Testing**:
   - Prueba localmente
   - Verifica que no haya errores
   - Revisa compatibilidad con producción

3. **Merge y Despliegue**:
   ```bash
   git checkout main
   git merge feature/nueva-funcionalidad
   git push origin main
   ```
   - Render detectará el push y redeployará automáticamente

### Rollback
Si hay problemas con una actualización:
1. Ve al dashboard de Render
2. Selecciona el commit anterior
3. Haz rollback desde la interfaz

---

## 📝 Comandos Útiles

### Desarrollo Local
```bash
# Activar entorno virtual
source venv/bin/activate

# Ejecutar servidor
cd Invernadero && python manage.py runserver

# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Recopilar archivos estáticos
python manage.py collectstatic

# Ejecutar tests
python manage.py test
```

### Producción (Render)
```bash
# Ver logs
render logs --service-id [SERVICE_ID]

# Reiniciar servicio
render restart --service-id [SERVICE_ID]

# Ver variables de entorno
render env list --service-id [SERVICE_ID]
```

---

## ✅ Checklist de Despliegue

### Pre-Despliegue
- [ ] Código commiteado y pusheado
- [ ] Variables de entorno configuradas
- [ ] `.gitignore` actualizado
- [ ] `requirements.txt` correcto
- [ ] `render.yaml` configurado

### Durante Despliegue
- [ ] Servicio web creado en Render
- [ ] Base de datos PostgreSQL creada
- [ ] Build exitoso
- [ ] Migraciones aplicadas
- [ ] Archivos estáticos recopilados

### Post-Despliegue
- [ ] Aplicación accesible en la URL
- [ ] Admin panel funcionando
- [ ] API endpoints respondiendo
- [ ] Archivos estáticos cargando
- [ ] Base de datos conectada
- [ ] Email funcionando (si configurado)

### Verificación Final
- [ ] Crear usuario de prueba
- [ ] Probar funcionalidades principales
- [ ] Verificar logs sin errores
- [ ] Performance aceptable

---

## 📞 Contactos y Soporte

**Desarrollador Principal**: [Tu Nombre]
**Email**: [tu-email@ejemplo.com]
**Repositorio**: [URL del repositorio]

Para soporte técnico:
1. Revisa esta documentación
2. Consulta los logs de Render
3. Revisa issues en el repositorio
4. Contacta al equipo de desarrollo

---

## 🔒 Consideraciones de Seguridad

### Producción
- `DEBUG = False`
- `SECRET_KEY` segura y única
- `ALLOWED_HOSTS` configurado correctamente
- HTTPS habilitado
- Headers de seguridad activados

### Base de Datos
- Credenciales seguras
- Conexiones limitadas
- Backups regulares

### Variables Sensibles
- Nunca commiteadas al repositorio
- Configuradas únicamente en Render
- Rotadas periódicamente

---

*Esta documentación se actualiza con cada cambio significativo en el proceso de despliegue. Última actualización: Diciembre 2024*