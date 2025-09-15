#!/bin/bash
set -e

echo "=== Direct Django Deployment Script ==="
echo "Environment: $DJANGO_ENV"
echo "Debug: $DEBUG"
echo "Port: $PORT"

# Install dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Set production environment
export DJANGO_ENV=production
export DEBUG=False

# Create necessary directories
mkdir -p Invernadero/staticfiles
mkdir -p Invernadero/media

# Navigate to Django project
cd Invernadero

# Run database migrations
echo "Running database migrations..."
python3 manage.py migrate --verbosity=1

# Collect static files
echo "Collecting static files..."
python3 manage.py collectstatic --noinput --clear --verbosity=1

# Create superuser if needed (optional)
echo "Checking for superuser..."
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='admin').exists() or None" | python3 manage.py shell || echo "No superuser created"

# Start Gunicorn server
echo "Starting Gunicorn server on port $PORT..."
exec gunicorn invernadero.wsgi:application \
  --bind 0.0.0.0:$PORT \
  --workers 2 \
  --threads 2 \
  --timeout 30 \
  --access-logfile - \
  --error-logfile - \
  --log-level info