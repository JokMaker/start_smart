#!/usr/bin/env python3
"""
Fresh Database Setup Script for StartSmart
This script creates a completely new database with proper schema alignment
"""

import sqlite3
import os
from datetime import datetime
from werkzeug.security import generate_password_hash

def delete_old_database():
    """Delete the existing database file"""
    db_path = 'startsmart.db'
    if os.path.exists(db_path):
        os.remove(db_path)
        print(f"✅ Deleted old database: {db_path}")
    else:
        print(f"ℹ️ No existing database found at: {db_path}")

def create_fresh_database():
    """Create a completely fresh database with proper schema"""
    print("🔧 Creating fresh database with proper schema...")
    
    conn = sqlite3.connect('startsmart.db')
    c = conn.cursor()
    
    # Users table with proper schema
    c.execute('''CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        name TEXT NOT NULL,
        user_type TEXT NOT NULL CHECK (user_type IN ('student', 'mentor', 'recruiter', 'admin')),
        phone TEXT,
        location TEXT,
        bio TEXT,
        skills TEXT,
        profile_image TEXT DEFAULT 'default-profile.jpg',
        linkedin_url TEXT,
        github_url TEXT,
        portfolio_url TEXT,
        is_active INTEGER DEFAULT 1,
        email_verified INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        last_login TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # Jobs table with salary_range column (not salary)
    c.execute('''CREATE TABLE jobs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        company TEXT NOT NULL,
        description TEXT NOT NULL,
        location TEXT,
        salary_range TEXT,
        job_type TEXT NOT NULL CHECK (job_type IN ('full-time', 'part-time', 'internship', 'contract', 'remote', 'hybrid')),
        posted_by INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        application_url TEXT,
        requirements TEXT,
        benefits TEXT,
        deadline DATE,
        is_active INTEGER DEFAULT 1,
        views INTEGER DEFAULT 0,
        FOREIGN KEY (posted_by) REFERENCES users (id)
    )''')
    
    # Startups table with founder column (text, not founder_id)
    c.execute('''CREATE TABLE startups (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT,
        industry TEXT,
        founder TEXT NOT NULL,
        website TEXT,
        location TEXT,
        funding_stage TEXT,
        team_size INTEGER,
        logo_url TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # Applications table
    c.execute('''CREATE TABLE applications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        job_id INTEGER NOT NULL,
        status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'reviewed', 'shortlisted', 'rejected', 'accepted')),
        applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        cover_letter TEXT,
        relevant_experience TEXT,
        portfolio_url TEXT,
        recruiter_notes TEXT,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id),
        FOREIGN KEY (job_id) REFERENCES jobs (id),
        UNIQUE(user_id, job_id)
    )''')
    
    # Skills table
    c.execute('''CREATE TABLE skills (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL,
        category TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # User skills junction table
    c.execute('''CREATE TABLE user_skills (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        skill_id INTEGER NOT NULL,
        proficiency_level TEXT CHECK (proficiency_level IN ('beginner', 'intermediate', 'advanced', 'expert')),
        FOREIGN KEY (user_id) REFERENCES users (id),
        FOREIGN KEY (skill_id) REFERENCES skills (id),
        UNIQUE(user_id, skill_id)
    )''')
    
    # Job skills junction table
    c.execute('''CREATE TABLE job_skills (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        job_id INTEGER NOT NULL,
        skill_id INTEGER NOT NULL,
        required_level TEXT CHECK (required_level IN ('beginner', 'intermediate', 'advanced', 'expert')),
        FOREIGN KEY (job_id) REFERENCES jobs (id),
        FOREIGN KEY (skill_id) REFERENCES skills (id),
        UNIQUE(job_id, skill_id)
    )''')
    
    # Mentorship table
    c.execute('''CREATE TABLE mentorship (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        mentor_id INTEGER NOT NULL,
        mentee_id INTEGER NOT NULL,
        subject TEXT,
        message TEXT,
        status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'accepted', 'declined', 'completed')),
        session_date TIMESTAMP,
        session_duration INTEGER,
        meeting_url TEXT,
        notes TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (mentor_id) REFERENCES users (id),
        FOREIGN KEY (mentee_id) REFERENCES users (id)
    )''')
    
    # Notifications table
    c.execute('''CREATE TABLE notifications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        message TEXT NOT NULL,
        notification_type TEXT DEFAULT 'general',
        related_id INTEGER,
        is_read INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )''')
    
    # Resources table
    c.execute('''CREATE TABLE resources (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        category TEXT,
        file_url TEXT,
        external_url TEXT,
        uploaded_by INTEGER,
        view_count INTEGER DEFAULT 0,
        download_count INTEGER DEFAULT 0,
        is_active INTEGER DEFAULT 1,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (uploaded_by) REFERENCES users (id)
    )''')
    
    # Password reset tokens table
    c.execute('''CREATE TABLE password_reset_tokens (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        token TEXT UNIQUE NOT NULL,
        expires_at TIMESTAMP NOT NULL,
        used INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )''')
    
    # Events table
    c.execute('''CREATE TABLE events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        event_type TEXT,
        location TEXT,
        event_date TIMESTAMP,
        organizer_id INTEGER,
        max_participants INTEGER,
        registration_deadline TIMESTAMP,
        is_active INTEGER DEFAULT 1,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (organizer_id) REFERENCES users (id)
    )''')
    
    conn.commit()
    print("✅ Database schema created successfully!")
    return conn

def add_demo_users(conn):
    """Add demo users for testing"""
    print("👥 Adding demo users...")
    
    c = conn.cursor()
    
    # Demo admin user
    admin_password = generate_password_hash("admin123", method='pbkdf2:sha256')
    c.execute("""INSERT INTO users (email, password, name, user_type, bio, created_at) 
                 VALUES (?, ?, ?, ?, ?, ?)""",
              ("admin@startsmart.com", admin_password, "Admin User", "admin", 
               "Platform administrator", datetime.now()))
    
    # Demo student user
    student_password = generate_password_hash("student123", method='pbkdf2:sha256')
    c.execute("""INSERT INTO users (email, password, name, user_type, location, skills, bio, created_at) 
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
              ("student@example.com", student_password, "Alice Johnson", "student", 
               "Nairobi, Kenya", "Python, JavaScript, React", 
               "Computer Science student passionate about software development", datetime.now()))
    
    # Demo recruiter user
    recruiter_password = generate_password_hash("recruiter123", method='pbkdf2:sha256')
    c.execute("""INSERT INTO users (email, password, name, user_type, location, bio, created_at) 
                 VALUES (?, ?, ?, ?, ?, ?, ?)""",
              ("recruiter@techcorp.com", recruiter_password, "Bob Williams", "recruiter", 
               "Lagos, Nigeria", "Senior Talent Acquisition Specialist at TechCorp", datetime.now()))
    
    # Demo mentor user
    mentor_password = generate_password_hash("mentor123", method='pbkdf2:sha256')
    c.execute("""INSERT INTO users (email, password, name, user_type, location, skills, bio, created_at) 
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
              ("mentor@startup.co", mentor_password, "Dr. Sarah Chen", "mentor", 
               "Cape Town, South Africa", "Product Management, Entrepreneurship, AI", 
               "Serial entrepreneur and startup mentor with 15+ years experience", datetime.now()))
    
    conn.commit()
    print("✅ Demo users added successfully!")

def add_demo_startups(conn):
    """Add demo startups"""
    print("🏢 Adding demo startups...")
    
    c = conn.cursor()
    
    startups = [
        ("TechNova Solutions", "AI-powered logistics platform for African markets", 
         "Technology", "John Kemboi", "https://technova.com", "Nairobi, Kenya", "Series A", 25),
        ("GreenAgri Tech", "Sustainable farming solutions using IoT and data analytics", 
         "Agriculture", "Amina Hassan", "https://greenagri.tech", "Accra, Ghana", "Seed", 12),
        ("FinanceFlow", "Digital banking platform for SMEs across Africa", 
         "Fintech", "David Ochieng", "https://financeflow.app", "Lagos, Nigeria", "Series B", 45)
    ]
    
    for startup in startups:
        c.execute("""INSERT INTO startups (name, description, industry, founder, website, location, funding_stage, team_size, created_at) 
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                  (*startup, datetime.now()))
    
    conn.commit()
    print("✅ Demo startups added successfully!")

def add_demo_jobs(conn):
    """Add demo jobs with proper salary_range column"""
    print("💼 Adding demo jobs...")
    
    c = conn.cursor()
    
    # Get the recruiter ID (Bob Williams)
    c.execute("SELECT id FROM users WHERE email = 'recruiter@techcorp.com'")
    recruiter_id = c.fetchone()[0]
    
    jobs = [
        ("Software Developer", "TechCorp Solutions", 
         "We are looking for a passionate software developer to join our growing team...", 
         "Nairobi, Kenya", "$40,000 - $60,000", "full-time", 
         "Experience with Python, JavaScript, and modern web frameworks", 
         "Health insurance, flexible hours, remote work options"),
        
        ("Data Analyst Intern", "DataInsights Ltd", 
         "Exciting internship opportunity for students passionate about data science...", 
         "Lagos, Nigeria", "$1,000 - $2,000 monthly", "internship", 
         "Knowledge of Python, SQL, and statistical analysis", 
         "Mentorship, training programs, potential full-time offer"),
        
        ("Frontend Developer", "WebCraft Agency", 
         "Join our creative team building amazing user experiences...", 
         "Cape Town, South Africa", "$35,000 - $50,000", "full-time", 
         "React, Vue.js, TypeScript, responsive design", 
         "Creative environment, learning budget, team events"),
        
        ("Product Manager", "InnovateTech", 
         "Lead product development for our mobile applications...", 
         "Kigali, Rwanda", "$50,000 - $70,000", "full-time", 
         "Product management experience, agile methodologies", 
         "Equity options, leadership development, international exposure")
    ]
    
    for job in jobs:
        c.execute("""INSERT INTO jobs (title, company, description, location, salary_range, job_type, 
                     requirements, benefits, posted_by, created_at, is_active) 
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                  (*job, recruiter_id, datetime.now(), 1))
    
    conn.commit()
    print("✅ Demo jobs added successfully!")

def add_demo_skills(conn):
    """Add demo skills"""
    print("🛠️ Adding demo skills...")
    
    c = conn.cursor()
    
    skills = [
        ("Python", "Programming"),
        ("JavaScript", "Programming"),
        ("React", "Frontend"),
        ("Node.js", "Backend"),
        ("SQL", "Database"),
        ("Data Analysis", "Analytics"),
        ("Project Management", "Management"),
        ("UI/UX Design", "Design"),
        ("Machine Learning", "AI/ML"),
        ("Digital Marketing", "Marketing")
    ]
    
    for skill in skills:
        c.execute("INSERT INTO skills (name, category, created_at) VALUES (?, ?, ?)",
                  (*skill, datetime.now()))
    
    conn.commit()
    print("✅ Demo skills added successfully!")

def verify_database(conn):
    """Verify the database schema and data"""
    print("🔍 Verifying database setup...")
    
    c = conn.cursor()
    
    # Check table structure
    tables = ['users', 'jobs', 'startups', 'applications', 'skills']
    for table in tables:
        c.execute(f"SELECT COUNT(*) FROM {table}")
        count = c.fetchone()[0]
        print(f"  - {table}: {count} records")
    
    # Verify column names in jobs table
    c.execute("PRAGMA table_info(jobs)")
    job_columns = [row[1] for row in c.fetchall()]
    print(f"  - jobs table columns: {job_columns}")
    
    # Verify column names in startups table
    c.execute("PRAGMA table_info(startups)")
    startup_columns = [row[1] for row in c.fetchall()]
    print(f"  - startups table columns: {startup_columns}")
    
    print("✅ Database verification complete!")

def main():
    """Main function to set up fresh database"""
    print("🚀 Starting fresh database setup for StartSmart...")
    print("=" * 50)
    
    try:
        # Step 1: Delete old database
        delete_old_database()
        
        # Step 2: Create fresh database with proper schema
        conn = create_fresh_database()
        
        # Step 3: Add demo data
        add_demo_users(conn)
        add_demo_startups(conn)
        add_demo_jobs(conn)
        add_demo_skills(conn)
        
        # Step 4: Verify setup
        verify_database(conn)
        
        conn.close()
        
        print("=" * 50)
        print("🎉 Fresh database setup completed successfully!")
        print("\nDemo user credentials:")
        print("  Admin: admin@startsmart.com / admin123")
        print("  Student: student@example.com / student123")
        print("  Recruiter: recruiter@techcorp.com / recruiter123")
        print("  Mentor: mentor@startup.co / mentor123")
        print("\n✅ Ready to test registration and login!")
        
    except Exception as e:
        print(f"❌ Error during database setup: {e}")
        return False
    
    return True

if __name__ == "__main__":
    main()
