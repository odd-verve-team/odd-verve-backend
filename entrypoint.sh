#!/bin/bash

set -e

echo "================================================="
echo "Collecting static files..."
echo "================================================="
python manage.py collectstatic --noinput

echo "================================================="
echo "Apply migrations to database..."
echo "================================================="
python manage.py migrate

echo "================================================="
echo "Creating default superuser..."
echo "================================================="
python manage.py createsuperuser --no-input || true

echo "================================================="
echo "Running celery worker on the background..."
echo "================================================="
celery -A core.tasks.emails worker --loglevel=info &

echo "================================================="
echo "Running backend..."
echo "================================================="
exec gunicorn core.wsgi:application --bind 0.0.0.0:8000
