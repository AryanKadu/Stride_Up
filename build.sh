#!/bin/bash
# Build script for Render deployment

echo "Running migrations..."
python manage.py migrate

echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

# Create superuser from env vars (if set). No hardcoded credentials.
# Set DJANGO_SUPERUSER_USERNAME, DJANGO_SUPERUSER_PASSWORD, DJANGO_SUPERUSER_EMAIL
# in Render's Environment tab to enable this.
if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ]; then
    echo "Creating superuser from environment variables..."
    python manage.py createsuperuser --noinput || echo "Superuser already exists, skipping."
else
    echo "Skipping superuser creation (DJANGO_SUPERUSER_* env vars not set)."
fi

echo "Build completed!" 