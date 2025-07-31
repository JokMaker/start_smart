#!/usr/bin/env bash
# Render build script

set -o errexit  # exit on error

# Install dependencies
pip install -r requirements.txt

# Emergency database setup for authentication
echo "Setting up database and demo users..."
python emergency_db_fix.py

# Add demo jobs
echo "Adding demo jobs..."
python add_jobs_for_video.py

echo "Build completed successfully"
