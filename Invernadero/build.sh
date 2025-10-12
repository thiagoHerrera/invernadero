#!/usr/bin/env bash
# Build script para Render

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