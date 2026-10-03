#!/bin/bash

set -e

echo "                                                 "
echo "================================================="
echo "Collecting static files..."
echo "================================================="
echo "                                                 "
python manage.py collectstatic --noinput

echo "                                                 "
echo "================================================="
echo "Applying migrations to database..."
echo "================================================="
echo "                                                 "
python manage.py migrate

echo "                                                 "
echo "================================================="
echo "Creating default superuser..."
echo "================================================="
echo "                                                 "
python manage.py createsuperuser --no-input || true

echo "                                                 "
echo "================================================="
echo "Running celery worker on the background..."
echo "================================================="
echo "                                                 "
celery -A core.tasks.emails worker --loglevel=info &

echo "                                                 "
echo "================================================="
echo "Running backend..."
echo "================================================="
echo "                                                 "
exec gunicorn core.wsgi:application --bind 0.0.0.0:${PORT:-8000}

