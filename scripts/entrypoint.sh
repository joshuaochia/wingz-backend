#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $DB_HOST $DB_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

exec "$@"

# 🚫 Skip migrations in dev
if [ "$DJANGO_ENV" != "dev" ]; then
    echo "Running migrations..."
    python manage.py migrate --noinput
else
    echo "Skipping migrations (dev mode)"
fi

# STATICFILES HANDLING
if [ "$DJANGO_ENV" != "dev" ]; then
    echo "Preparing static files..."
    mkdir -p "$APP_HOME/staticfiles"
    python manage.py collectstatic --noinput --clear
else
    echo "Skipping collectstatic (dev mode)"
fi

if [ "$QCLUSTER" = "true" ]; then
    echo "Starting Django Q cluster..."
    exec python manage.py qcluster
elif [ "$DJANGO_ENV" = "dev" ]; then
    echo "Starting dev env..."
    exec python manage.py runserver 0.0.0.0:8000
else
    echo "Starting Gunicorn web server..."
    exec gunicorn app.wsgi:application --bind 0.0.0.0:8000
fi