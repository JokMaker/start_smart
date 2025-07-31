#!/usr/bin/env bash
# Render build script

set -o errexit  # exit on error

# Install dependencies
pip install -r requirements.txt

# Initialize database
python -c "
try:
    from db_setup import setup_database
    setup_database()
    print('Database setup completed')
except Exception as e:
    print(f'Database setup failed: {e}')
    # Create basic tables manually
    import sqlite3
    conn = sqlite3.connect('startsmart.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        name TEXT NOT NULL,
        user_type TEXT NOT NULL,
        bio TEXT,
        skills TEXT,
        location TEXT,
        resume_filename TEXT,
        portfolio_url TEXT,
        profile_image TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        last_login TIMESTAMP,
        is_active INTEGER DEFAULT 1
    )''')
    conn.commit()
    conn.close()
    print('Manual database creation completed')
"

# Add demo jobs for video
python add_jobs_for_video.py

echo "Build completed successfully"
