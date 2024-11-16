#!/bin/bash

echo "🚀 Starting FITB_AI initial setup..."

# Start PostgreSQL container
echo "📦 Starting PostgreSQL container..."
docker-compose up -d
if [ $? -ne 0 ]; then
    echo "❌ Failed to start PostgreSQL container"
    exit 1
fi

# Wait for PostgreSQL to be ready
echo "⏳ Waiting for PostgreSQL to be ready..."
sleep 5  # Give PostgreSQL time to initialize

# Check if container is running
if ! docker ps | grep -q fitb_ai_db; then
    echo "❌ PostgreSQL container is not running"
    exit 1
fi
echo "✅ PostgreSQL is running"

# Navigate to Django project directory
cd ../src

# Create and apply migrations
echo "🔄 Creating migrations..."
uv run manage.py makemigrations
if [ $? -ne 0 ]; then
    echo "❌ Failed to create migrations"
    exit 1
fi

echo "🔄 Applying migrations..."
uv run manage.py migrate
if [ $? -ne 0 ]; then
    echo "❌ Failed to apply migrations"
    exit 1
fi

# Create superuser
echo "👤 Creating superuser..."
uv run manage.py createsuperuser

echo "✅ Setup complete! You can now start the application"