#!/usr/bin/env bash
# Build script para Render

set -o errexit

echo "Instalando dependencias..."
pip install -r requirements.txt

echo "Ejecutando migraciones..."
# Crear migraciones para todas las apps
python manage.py makemigrations users
python manage.py makemigrations Verificacion2FA
python manage.py makemigrations Authentication
python manage.py makemigrations api_comunication
python manage.py makemigrations Windows
python manage.py makemigrations diagnostico
python manage.py makemigrations

# Ejecutar migraciones
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