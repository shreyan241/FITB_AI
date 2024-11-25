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
sleep 10  # Give PostgreSQL time to initialize

# Test database connection
echo "🔄 Testing database connection..."
max_attempts=30
counter=0
while ! docker exec fitb_ai_db pg_isready -U fitb_ai_user -d fitb_ai_db > /dev/null 2>&1; do
    counter=$((counter + 1))
    if [ $counter -eq $max_attempts ]; then
        echo "❌ Database failed to start"
        exit 1
    fi
    echo "Waiting for database... ($counter/$max_attempts)"
    sleep 1
done

echo "✅ PostgreSQL is running and accepting connections"

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