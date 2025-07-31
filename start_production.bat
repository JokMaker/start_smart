@echo off
REM StartSmart Production Startup Script for Windows

echo 🚀 Starting StartSmart Production Server...

REM Create necessary directories
echo 📁 Creating directories...
if not exist "backups" mkdir backups
if not exist "logs" mkdir logs
if not exist "static\uploads" mkdir static\uploads

REM Create backup before starting
echo 💾 Creating database backup...
python backup_system.py

REM Check if .env file exists
if not exist ".env" (
    echo ⚠️  Warning: .env file not found. Using default settings.
    echo 📝 Please create .env file with production settings.
)

REM Set production environment
set FLASK_ENV=production

REM Start the application
echo 🌟 Starting Flask application...
python app.py

pause
