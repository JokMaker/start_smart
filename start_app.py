#!/usr/bin/env python3
"""
Simple test runner to diagnose and fix StartSmart issues
"""
import os
import sys
import sqlite3
from datetime import datetime
from werkzeug.security import generate_password_hash

def create_database():
    """Create database with test users"""
    print("🔧 Creating fresh database...")
    
    # Remove existing database
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
        stage TEXT DEFAULT 'Early Stage',
        founder_id INTEGER NOT NULL,
        website TEXT,
        logo TEXT,
        founded_date DATE,
        location TEXT,
        created_at TIMESTAMP NOT NULL,
        FOREIGN KEY (founder_id) REFERENCES users (id)
    )''')
    
    # Create applications table
    c.execute('''CREATE TABLE IF NOT EXISTS applications (
        id INTEGER PRIMARY KEY,
        user_id INTEGER NOT NULL,
        job_id INTEGER NOT NULL,
        status TEXT DEFAULT 'pending' CHECK(status IN ('pending', 'accepted', 'rejected')),
        applied_at TIMESTAMP NOT NULL,
        cover_letter TEXT,
        FOREIGN KEY (user_id) REFERENCES users (id),
        FOREIGN KEY (job_id) REFERENCES jobs (id),
        UNIQUE(user_id, job_id)
    )''')
    
    # Create mentorship table
    c.execute('''CREATE TABLE IF NOT EXISTS mentorship (
        id INTEGER PRIMARY KEY,
        mentor_id INTEGER NOT NULL,
        mentee_id INTEGER NOT NULL,
        topic TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'pending' CHECK(status IN ('pending', 'accepted', 'rejected', 'completed')),
        message TEXT,
        created_at TIMESTAMP NOT NULL,
        FOREIGN KEY (mentor_id) REFERENCES users (id),
        FOREIGN KEY (mentee_id) REFERENCES users (id)
    )''')
    
    # Create notifications table
    c.execute('''CREATE TABLE IF NOT EXISTS notifications (
        id INTEGER PRIMARY KEY,
        user_id INTEGER NOT NULL,
        title TEXT NOT NULL,
        message TEXT NOT NULL,
        type TEXT NOT NULL,
        is_read BOOLEAN DEFAULT 0,
        created_at TIMESTAMP NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )''')
    
    # Create resources table
    c.execute('''CREATE TABLE IF NOT EXISTS resources (
        id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        description TEXT NOT NULL,
        category TEXT NOT NULL,
        file_url TEXT,
        external_url TEXT,
        uploaded_by INTEGER NOT NULL,
        view_count INTEGER DEFAULT 0,
        created_at TIMESTAMP NOT NULL,
        FOREIGN KEY (uploaded_by) REFERENCES users (id)
    )''')
    
    print("✅ Database tables created")
    
    # Create test users
    test_users = [
        ('j.kur@alustudent.com', 'password123', 'John Kur', 'student'),
        ('mentor@example.com', 'mentor123', 'Jane Mentor', 'mentor'),
        ('recruiter@company.com', 'recruiter123', 'Bob Recruiter', 'recruiter')
    ]
    
    for email, password, name, user_type in test_users:
        password_hash = generate_password_hash(password)
        c.execute("""INSERT INTO users (email, password, name, user_type, created_at) 
                     VALUES (?, ?, ?, ?, ?)""",
                 (email, password_hash, name, user_type, datetime.now()))
        print(f"👤 Created user: {name} ({email})")
    
    # Create sample job
    c.execute("""INSERT INTO jobs (title, company, description, location, salary, 
                 job_type, posted_by, created_at, application_url, requirements, is_active)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
             ('Software Developer Intern', 'TechCorp', 
              'Join our development team as an intern to gain hands-on experience.', 
              'Kigali, Rwanda', '$500/month', 'internship', 4, datetime.now(),
              'https://techcorp.com/apply', 'Python, JavaScript, Git', 1))
    
    # Create sample startup
    c.execute("""INSERT INTO startups (name, description, industry, stage, founder_id, 
                 website, location, created_at)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
             ('EduTech Solutions', 'Revolutionizing education through technology',
              'Education Technology', 'Early Stage', 1, 'https://edutech.rw', 'Kigali, Rwanda',
              datetime.now()))
    
    conn.commit()
    conn.close()
    
    print("✅ Database initialization completed!")
    print("\n📋 Available Test User Credentials:")
    print("Student: j.kur@alustudent.com / password123")
    print("Mentor: mentor@example.com / mentor123")
    print("Recruiter: recruiter@company.com / recruiter123")
    print("\n💡 Note: Admin users can be created manually through registration")
    return True

def main():
    print("🚀 StartSmart Diagnostic and Fix Tool")
    print("=" * 50)
    
    # Step 1: Initialize fresh database
    print("\n1️⃣ Initializing fresh database...")
    try:
        create_database()
        print("✅ Database initialized successfully")
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # Step 2: Test Flask app import
    print("\n2️⃣ Testing Flask application...")
    try:
        from app import app
        print("✅ Flask app imports successfully")
    except Exception as e:
        print(f"❌ Flask app import failed: {e}")
        return
    
    # Step 3: Start the application
    print("\n3️⃣ Starting the application...")
    print("🌐 Visit: http://localhost:5000")
    print("📋 Test credentials: j.kur@alustudent.com / password123")
    print("� Or register as student, mentor, or recruiter")
    print("�🛑 Press Ctrl+C to stop the server")
    print("\n✅ All missing routes have been added:")
    print("   - ai_job_matches (/ai-job-matches)")
    print("   - job_map (/job-map)")
    print("   - mentorship_calendar (/mentorship-calendar)")
    
    try:
        # Initialize database before starting
        from app import init_db
        init_db()
        app.run(debug=True, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\n👋 Server stopped")
    except Exception as e:
        print(f"❌ Failed to start server: {e}")

if __name__ == "__main__":
    main()
