#!/bin/sh
set -e

DB_HOST="${POSTGRES_HOST:-db}"
DB_PORT="${POSTGRES_PORT:-5432}"

echo "Waiting for Postgres at $DB_HOST:$DB_PORT..."
until nc -z "$DB_HOST" "$DB_PORT"; do
    echo "Postgres not ready yet..."
    sleep 1
done

echo "Running Django setup..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

echo "Starting Gunicorn..."
exec gunicorn tuzmore.wsgi:application \
    --bind 0.0.0.0:8000 \ 
    --workers=4 \
    --timeout=120