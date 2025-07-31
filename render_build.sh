#!/bin/bash
# Build script for Render deployment

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Setting up database..."
python -c "
try:
    from app import init_db
    init_db()
    print('Database initialized successfully')
except Exception as e:
    print(f'Database init error: {e}')
    # Manual database setup
    import sqlite3
    conn = sqlite3.connect('startsmart.db')
    c = conn.cursor()
    
    # Create essential tables
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        name TEXT NOT NULL,
        user_type TEXT NOT NULL,
        bio TEXT,
        location TEXT,
        skills TEXT,
        profile_image TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        last_login TIMESTAMP,
        is_active INTEGER DEFAULT 1
    )''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS jobs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        company TEXT NOT NULL,
        description TEXT NOT NULL,
        location TEXT NOT NULL,
        salary TEXT,
        job_type TEXT NOT NULL,
        posted_by INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        application_url TEXT,
        is_active INTEGER DEFAULT 1,
        requirements TEXT,
        benefits TEXT,
        deadline TEXT
    )''')
    
    conn.commit()
    conn.close()
    print('Manual database setup completed')
"

echo "Build completed successfully!"