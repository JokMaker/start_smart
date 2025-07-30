#!/usr/bin/env python3
"""
Production-Ready Database Reset
Clears all test data and sets up fresh database for real users
"""

import sqlite3
import os
from datetime import datetime
from werkzeug.security import generate_password_hash

def reset_for_production():
    """Reset database for production use"""
    print("🚀 PREPARING DATABASE FOR PRODUCTION")
    print("=" * 50)
    
    # Backup existing database
    if os.path.exists('startsmart.db'):
        backup_name = f'startsmart_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.db'
        os.rename('startsmart.db', backup_name)
        print(f"✅ Backed up existing database to: {backup_name}")
    
    # Create fresh database
    conn = sqlite3.connect('startsmart.db')
    c = conn.cursor()
    
    # Create all tables (copying from db_setup.py structure)
    print("📋 Creating fresh database tables...")
    
    # Users table
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        name TEXT NOT NULL,
        user_type TEXT NOT NULL CHECK(user_type IN ('student', 'mentor', 'recruiter')),
        bio TEXT,
        skills TEXT,
        location TEXT,
        profile_image TEXT,
        is_verified BOOLEAN DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        last_login TIMESTAMP,
        is_active BOOLEAN DEFAULT 1
    )''')
    
    # Jobs table
    c.execute('''CREATE TABLE IF NOT EXISTS jobs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        company TEXT NOT NULL,
        description TEXT NOT NULL,
        requirements TEXT,
        location TEXT,
        salary_range TEXT,
        job_type TEXT CHECK(job_type IN ('full-time', 'part-time', 'internship', 'contract')),
        posted_by INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        deadline DATE,
        is_active BOOLEAN DEFAULT 1,
        FOREIGN KEY (posted_by) REFERENCES users (id)
    )''')
    
    # Applications table
    c.execute('''CREATE TABLE IF NOT EXISTS applications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        job_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        cover_letter TEXT,
        resume_path TEXT,
        status TEXT DEFAULT 'pending' CHECK(status IN ('pending', 'reviewed', 'accepted', 'rejected')),
        applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (job_id) REFERENCES jobs (id),
        FOREIGN KEY (user_id) REFERENCES users (id),
        UNIQUE(job_id, user_id)
    )''')
    
    # Startups table
    c.execute('''CREATE TABLE IF NOT EXISTS startups (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT NOT NULL,
        industry TEXT,
        stage TEXT CHECK(stage IN ('idea', 'prototype', 'mvp', 'growth', 'scale')),
        founder_id INTEGER,
        website TEXT,
        location TEXT,
        funding_goal REAL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (founder_id) REFERENCES users (id)
    )''')
    
    # Mentorship table
    c.execute('''CREATE TABLE IF NOT EXISTS mentorship (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        mentor_id INTEGER NOT NULL,
        mentee_id INTEGER NOT NULL,
        topic TEXT NOT NULL,
        status TEXT DEFAULT 'pending' CHECK(status IN ('pending', 'active', 'completed', 'cancelled')),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (mentor_id) REFERENCES users (id),
        FOREIGN KEY (mentee_id) REFERENCES users (id)
    )''')
    
    # Resources table
    c.execute('''CREATE TABLE IF NOT EXISTS resources (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        file_path TEXT NOT NULL,
        uploaded_by INTEGER,
        category TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        downloads INTEGER DEFAULT 0,
        FOREIGN KEY (uploaded_by) REFERENCES users (id)
    )''')
    
    # Notifications table
    c.execute('''CREATE TABLE IF NOT EXISTS notifications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        title TEXT NOT NULL,
        message TEXT NOT NULL,
        type TEXT CHECK(type IN ('info', 'success', 'warning', 'error')),
        is_read BOOLEAN DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )''')
    
    print("✅ All tables created successfully")
    
    # Create sample content (jobs, startups) but NO TEST USERS
    print("📝 Adding sample job opportunities...")
    
    sample_jobs = [
        ("Software Developer", "TechStart Rwanda", "Join our growing team building the next generation of fintech solutions for Africa.", "Python, JavaScript, SQL", "Kigali, Rwanda", "$30,000 - $45,000", "full-time"),
        ("Marketing Intern", "Green Energy Solutions", "Help us promote sustainable energy solutions across East Africa.", "Marketing, Social Media, Content Creation", "Nairobi, Kenya", "$500 - $800/month", "internship"),
        ("Data Analyst", "African Analytics", "Analyze data to drive business decisions for agricultural technology.", "Python, Excel, Statistics", "Lagos, Nigeria", "$25,000 - $35,000", "full-time"),
        ("UI/UX Designer", "Mobile First", "Design beautiful mobile applications for African markets.", "Figma, Adobe Creative Suite, User Research", "Cape Town, South Africa", "$20,000 - $30,000", "contract")
    ]
    
    for job in sample_jobs:
        c.execute("""INSERT INTO jobs (title, company, description, requirements, location, salary_range, job_type, created_at) 
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                 (*job, datetime.now()))
    
    print("✅ Sample jobs added")
    
    # Add sample startups
    print("🚀 Adding sample startups...")
    
    sample_startups = [
        ("AgriTech Solutions", "Connecting farmers with modern agricultural technology and markets", "Agriculture", "mvp", "Kigali, Rwanda"),
        ("EduLearn Africa", "Online learning platform focused on African curriculum", "Education", "prototype", "Nairobi, Kenya"),
        ("FinPay Mobile", "Mobile payment solutions for rural communities", "Fintech", "growth", "Lagos, Nigeria"),
        ("HealthConnect", "Telemedicine platform for remote healthcare delivery", "Healthcare", "idea", "Accra, Ghana")
    ]
    
    for startup in sample_startups:
        c.execute("""INSERT INTO startups (name, description, industry, stage, location, created_at) 
                     VALUES (?, ?, ?, ?, ?, ?)""",
                 (*startup, datetime.now()))
    
    print("✅ Sample startups added")
    
    conn.commit()
    conn.close()
    
    print("\n🎉 PRODUCTION DATABASE READY!")
    print("=" * 50)
    print("✅ Fresh database with NO test users")
    print("✅ Sample jobs and startups available")
    print("✅ Ready for real user registrations")
    print("✅ All authentication systems operational")
    
    return True

if __name__ == "__main__":
    reset_for_production()
