#!/bin/bash

# Exit on error
set -e

# Print environment for debugging
echo "Starting Django application..."
echo "DJANGO_ENV: $DJANGO_ENV"
echo "DEBUG: $DEBUG"
echo "PORT: $PORT"

# Configure ALLOWED_HOSTS dynamically for Render
if [ -n "$RENDER_EXTERNAL_URL" ]; then
    # Extract domain from Render URL (remove https://)
    RENDER_DOMAIN=$(echo $RENDER_EXTERNAL_URL | sed 's|https://||')
    export ALLOWED_HOSTS="$RENDER_DOMAIN"
    echo "ALLOWED_HOSTS configured: $ALLOWED_HOSTS"
fi

# Change to the correct directory
cd Invernadero || exit 1

# Run migrations
echo "Running database migrations..."
python3 manage.py migrate

# Collect static files
echo "Collecting static files..."
python3 manage.py collectstatic --noinput --clear

# Start Gunicorn server
echo "Starting Gunicorn server..."
exec gunicorn invernadero.wsgi:application --bind 0.0.0.0:$PORT --log-level info