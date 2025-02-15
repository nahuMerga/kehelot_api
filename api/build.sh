#!/usr/bin/env bash

set -o errexit  # Exit on error
set -o pipefail  # Exit on first failed command in a pipeline
set -o nounset  # Prevent using unset variables
set -o xtrace  # Debugging: Print commands before running them

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
gunicorn your_project.wsgi:application --bind 0.0.0.0:$PORT --workers 3
