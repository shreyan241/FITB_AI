#!/bin/bash

echo "🚀 Starting FITB_AI..."

# Start PostgreSQL container
echo "📦 Starting PostgreSQL container..."
docker-compose up -d
if [ $? -ne 0 ]; then
    echo "❌ Failed to start PostgreSQL container"
    exit 1
fi

# Wait for PostgreSQL to be ready
echo "⏳ Waiting for PostgreSQL to be ready..."
for i in {1..30}; do
    if docker exec fitb_ai_db pg_isready > /dev/null 2>&1; then
        echo "✅ PostgreSQL is ready"
        break
    fi
    echo "Waiting... ($i/30)"
    sleep 2
done

# Check if container is running
if ! docker ps | grep -q fitb_ai_db; then
    echo "❌ PostgreSQL container is not running"
    exit 1
fi
echo "✅ PostgreSQL is running"

# Navigate to Django project directory
cd ../src

# Make migrations for any model changes
echo "🔄 Checking for model changes..."
uv run manage.py makemigrations
if [ $? -ne 0 ]; then
    echo "❌ Failed to make migrations"
    exit 1
fi
echo "✅ Migrations created successfully"

# Apply any pending migrations
echo "🔄 Applying migrations..."
uv run manage.py migrate
if [ $? -ne 0 ]; then
    echo "❌ Failed to apply migrations"
    exit 1
fi
echo "✅ Database migrations complete"

# Collect static files if needed
echo "🔄 Collecting static files..."
uv run manage.py collectstatic --noinput
if [ $? -ne 0 ]; then
    echo "❌ Failed to collect static files"
    exit 1
fi
echo "✅ Static files collected"

echo "✅ Startup complete! You can now start the application"