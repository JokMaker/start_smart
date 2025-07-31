#!/bin/bash
# StartSmart Production Startup Script

echo "🚀 Starting StartSmart Production Server..."

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p backups
mkdir -p logs
mkdir -p static/uploads

# Create backup before starting
echo "💾 Creating database backup..."
python backup_system.py

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  Warning: .env file not found. Using default settings."
    echo "📝 Please create .env file with production settings."
fi

# Set production environment
export FLASK_ENV=production
export PYTHONPATH=$PYTHONPATH:$(pwd)

# Start the application
echo "🌟 Starting Flask application..."
python app.py
