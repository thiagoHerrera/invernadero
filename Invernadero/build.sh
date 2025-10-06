#!/usr/bin/env bash
# Build script para Render

set -o errexit

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar migraciones
python manage.py migrate

# Crear superusuario si no existe
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(is_superuser=True).exists():
    User.objects.create_superuser('admin', 'admin@floracore.com', 'floracore2025')
    print('Superusuario creado')
"

# Recopilar archivos estáticos
python manage.py collectstatic --noinput