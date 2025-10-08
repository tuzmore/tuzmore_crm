#!/bin/sh
set -e

echo "=========================================="
echo "🚀 Starting Tuzmore Django Application"
echo "=========================================="

# Ensure DATABASE_URL is set
if [ -z "$DATABASE_URL" ]; then
    echo "❌ ERROR: DATABASE_URL environment variable not set!"
    exit 1
fi

# Optional: wait for PostgreSQL to be ready
echo "Checking database connection..."
until python manage.py check --database default; do
    echo "⏳ Database not ready yet, waiting..."
    sleep 3
done

echo "✅ Database is ready!"

# Run migrations
echo "Applying database migrations..."
python manage.py migrate --noinput

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

# Start Gunicorn
echo "Starting Gunicorn server..."
exec gunicorn tuzmore.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 4 \
    --timeout 120
