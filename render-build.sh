#!/usr/bin/env bash
# Render build script

set -o errexit  # exit on error

# Install dependencies
pip install -r requirements.txt

# Simple database initialization that definitely works
python -c "
import sqlite3
import os
from datetime import datetime

print('🚨 CREATING DATABASE FOR RENDER...')

# Remove old database
if os.path.exists('startsmart.db'):
    os.remove('startsmart.db')

conn = sqlite3.connect('startsmart.db')
c = conn.cursor()

# Create users table
c.execute('''CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    name TEXT NOT NULL,
    user_type TEXT NOT NULL DEFAULT 'student',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active INTEGER DEFAULT 1,
    profile_picture TEXT,
    bio TEXT,
    location TEXT,
    phone TEXT,
    website TEXT,
    linkedin TEXT,
    skills TEXT,
    experience TEXT,
    education TEXT
)''')

# Create jobs table
c.execute('''CREATE TABLE jobs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    company TEXT NOT NULL,
    description TEXT NOT NULL,
    location TEXT,
    salary TEXT,
    job_type TEXT DEFAULT 'full-time',
    posted_by INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deadline DATE,
    requirements TEXT,
    benefits TEXT,
    application_url TEXT,
    is_active INTEGER DEFAULT 1,
    FOREIGN KEY (posted_by) REFERENCES users (id)
)''')

# Create applications table  
c.execute('''CREATE TABLE applications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    job_id INTEGER,
    user_id INTEGER,
    status TEXT DEFAULT 'pending',
    applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    cover_letter TEXT,
    resume_url TEXT,
    FOREIGN KEY (job_id) REFERENCES jobs (id),
    FOREIGN KEY (user_id) REFERENCES users (id)
)''')

conn.commit()
conn.close()
print('✅ DATABASE CREATED SUCCESSFULLY')
"

# Add demo jobs
echo "Adding demo jobs..."
python add_jobs_for_video.py

echo "Build completed successfully"
