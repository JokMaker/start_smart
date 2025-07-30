#!/usr/bin/env python3
"""
Database initialization and user creation script for StartSmart
"""
import sqlite3
import os
from datetime import datetime
from werkzeug.security import generate_password_hash

def initialize_database():
    """Initialize database with proper schema"""
    print("🔧 Initializing StartSmart database...")
    
    # Remove existing database to start fresh
    if os.path.exists('startsmart.db'):
        os.remove('startsmart.db')
        print("📁 Removed existing database")
    
    # Create new database
    conn = sqlite3.connect('startsmart.db')
    c = conn.cursor()
    
    # Create users table
    c.execute('''CREATE TABLE users (
        id INTEGER PRIMARY KEY,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        name TEXT NOT NULL,
        user_type TEXT NOT NULL CHECK(user_type IN ('student', 'mentor', 'recruiter', 'admin')),
        bio TEXT,
        skills TEXT,
        location TEXT,
        resume_file TEXT,
        profile_image TEXT,
        created_at TIMESTAMP NOT NULL,
        last_login TIMESTAMP
    )''')
    
    # Create jobs table
    c.execute('''CREATE TABLE jobs (
        id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        company TEXT NOT NULL,
        description TEXT NOT NULL,
        location TEXT NOT NULL,
        salary TEXT,
        job_type TEXT NOT NULL,
        posted_by INTEGER NOT NULL,
        created_at TIMESTAMP NOT NULL,
        application_url TEXT,
        requirements TEXT NOT NULL,
        benefits TEXT,
        deadline DATE,
        is_active BOOLEAN DEFAULT 1,
        FOREIGN KEY (posted_by) REFERENCES users (id)
    )''')
    
    # Create startups table
    c.execute('''CREATE TABLE startups (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        description TEXT NOT NULL,
        industry TEXT NOT NULL,
        founder_id INTEGER NOT NULL,
        website TEXT,
        logo TEXT,
        founded_date DATE,
        location TEXT,
        created_at TIMESTAMP NOT NULL,
        FOREIGN KEY (founder_id) REFERENCES users (id)
    )''')
    
    print("✅ Database tables created")
    
    # Create test users
    test_users = [
        {
            'email': 'j.kur@alustudent.com',
            'password': 'password123',
            'name': 'John Kur',
            'user_type': 'student'
        },
        {
            'email': 'admin@startsmart.com',
            'password': 'admin123',
            'name': 'Admin User',
            'user_type': 'admin'
        },
        {
            'email': 'mentor@example.com',
            'password': 'mentor123',
            'name': 'Jane Mentor',
            'user_type': 'mentor'
        },
        {
            'email': 'recruiter@company.com',
            'password': 'recruiter123',
            'name': 'Bob Recruiter',
            'user_type': 'recruiter'
        }
    ]
    
    for user_data in test_users:
        password_hash = generate_password_hash(user_data['password'])
        c.execute("""INSERT INTO users (email, password, name, user_type, created_at) 
                     VALUES (?, ?, ?, ?, ?)""",
                 (user_data['email'], password_hash, user_data['name'], 
                  user_data['user_type'], datetime.now()))
        print(f"👤 Created user: {user_data['name']} ({user_data['email']})")
    
    # Create sample job
    c.execute("""INSERT INTO jobs (title, company, description, location, salary, 
                 job_type, posted_by, created_at, application_url, requirements, is_active)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
             ('Software Developer Intern', 'TechCorp', 
              'Join our development team as an intern to gain hands-on experience.', 
              'Kigali, Rwanda', '$500/month', 'internship', 4, datetime.now(),
              'https://techcorp.com/apply', 'Python, JavaScript, Git', 1))
    
    # Create sample startup
    c.execute("""INSERT INTO startups (name, description, industry, founder_id, 
                 website, location, created_at)
                 VALUES (?, ?, ?, ?, ?, ?, ?)""",
             ('EduTech Solutions', 'Revolutionizing education through technology',
              'Education Technology', 1, 'https://edutech.rw', 'Kigali, Rwanda',
              datetime.now()))
    
    conn.commit()
    conn.close()
    
    print("✅ Database initialization completed!")
    print("\n📋 Test User Credentials:")
    print("Student: j.kur@alustudent.com / password123")
    print("Admin: admin@startsmart.com / admin123")
    print("Mentor: mentor@example.com / mentor123")
    print("Recruiter: recruiter@company.com / recruiter123")

if __name__ == "__main__":
    initialize_database()
