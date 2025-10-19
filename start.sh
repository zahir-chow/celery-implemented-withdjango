#!/bin/bash
set -e

# Set Django settings module explicitly
export DJANGO_SETTINGS_MODULE=async_demo.settings_production

# Wait for database to be ready
echo "Waiting for database..."
python manage.py migrate --noinput

# Ensure staticfiles directory exists
mkdir -p staticfiles

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

# Start the application
echo "Starting application..."
exec gunicorn async_demo.wsgi:application \
    --bind 0.0.0.0:${PORT:-8000} \
    --workers 3 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile -
