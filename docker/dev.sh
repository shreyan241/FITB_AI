#!/bin/bash

echo "🚀 Starting FITB_AI development server..."

# Start PostgreSQL container if not running
if ! docker ps | grep -q fitb_ai_db; then
    echo "📦 Starting PostgreSQL container..."
    docker-compose up -d
    sleep 5
fi

# Navigate to Django project directory
cd ../src

# Start development server using Uvicorn
echo "🔄 Starting Django development server with Uvicorn..."
uv run uvicorn backend.asgi:application --reload --host 0.0.0.0 --port 8000