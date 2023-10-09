#!/bin/bash

echo "Starting entrypoint.sh..."

# wait for PSQL server to start
sleep 10

# Generate new migration files
echo "Generating new migration files..."
python3 manage.py makemigrations

# Apply database migrations
echo "Applying database migrations..."
python3 manage.py migrate

# collect static files
python3 manage.py collectstatic --no-input

# Start the Django development server
echo "Starting Django development server..."
python3 manage.py runserver 0.0.0.0:8000
