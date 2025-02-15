#!/usr/bin/env bash

set -o errexit  # Exit on error


echo "🚀 Starting deployment..."

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Run database migrations
python manage.py migrate --no-input

# Collect static files
python manage.py collectstatic --no-input

# Start Gunicorn server using the dynamic PORT environment variable
python manage.py runserver
