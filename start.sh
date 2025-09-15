#!/bin/bash

# Exit on error
set -e

# Print environment for debugging
echo "Starting Django application..."
echo "DJANGO_ENV: $DJANGO_ENV"
echo "DEBUG: $DEBUG"
echo "PORT: $PORT"

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