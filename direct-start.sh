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

# Configure ALLOWED_HOSTS dynamically for Render
if [ -n "$RENDER_EXTERNAL_URL" ]; then
    # Extract domain from Render URL (remove https://)
    RENDER_DOMAIN=$(echo $RENDER_EXTERNAL_URL | sed 's|https://||')
    export ALLOWED_HOSTS="$RENDER_DOMAIN,localhost,127.0.0.1"
    echo "ALLOWED_HOSTS configured: $ALLOWED_HOSTS"
else
    # Fallback for other platforms
    export ALLOWED_HOSTS="localhost,127.0.0.1,0.0.0.0"
    echo "ALLOWED_HOSTS fallback: $ALLOWED_HOSTS"
fi

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