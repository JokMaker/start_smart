import sqlite3
import os
from datetime import datetime
from werkzeug.security import generate_password_hash

def setup_database():
    """
    Set up the StartSmart database with all required tables based on the SRS document.
    """
    print("Setting up StartSmart database...")
    
    # Create database connection
    conn = sqlite3.connect('startsmart.db')
    c = conn.cursor()
    
    # Users table - Core user information and authentication
    c.execute('''CREATE TABLE IF NOT EXISTS users (
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
    
    # Jobs table - Job listings posted by recruiters
    c.execute('''CREATE TABLE IF NOT EXISTS jobs (
        id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        company TEXT NOT NULL,
        description TEXT NOT NULL,
        location TEXT NOT NULL,
        salary TEXT,
        job_type TEXT NOT NULL CHECK(job_type IN ('full-time', 'part-time', 'internship', 'contract', 'remote', 'hybrid')),
        posted_by INTEGER NOT NULL,
        created_at TIMESTAMP NOT NULL,
        application_url TEXT,
        requirements TEXT NOT NULL,
        benefits TEXT,
        deadline DATE,
        is_active BOOLEAN DEFAULT 1,
        FOREIGN KEY (posted_by) REFERENCES users (id)
    )''')
    
    # Applications table - Job applications submitted by students
    c.execute('''CREATE TABLE IF NOT EXISTS applications (
        id INTEGER PRIMARY KEY,
        job_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        status TEXT NOT NULL DEFAULT 'pending' CHECK(status IN ('pending', 'reviewed', 'shortlisted', 'rejected', 'hired')),
        cover_letter TEXT,
        applied_at TIMESTAMP NOT NULL,
        updated_at TIMESTAMP,
        FOREIGN KEY (job_id) REFERENCES jobs (id),
        FOREIGN KEY (user_id) REFERENCES users (id)
    )''')
    
    # Startups table - Startup ventures listed by students or mentors
    c.execute('''CREATE TABLE IF NOT EXISTS startups (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        description TEXT NOT NULL,
        industry TEXT,
        stage TEXT CHECK(stage IN ('idea', 'prototype', 'early-stage', 'growth', 'established')),
        founder_id INTEGER NOT NULL,
        logo_image TEXT,
        website_url TEXT,
        funding_status TEXT,
        team_size INTEGER DEFAULT 1,
        created_at TIMESTAMP NOT NULL,
        FOREIGN KEY (founder_id) REFERENCES users (id)
    )''')
    
    # Startup Team Members - For tracking team members of startups
    c.execute('''CREATE TABLE IF NOT EXISTS startup_members (
        id INTEGER PRIMARY KEY,
        startup_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        role TEXT NOT NULL,
        joined_at TIMESTAMP NOT NULL,
        FOREIGN KEY (startup_id) REFERENCES startups (id),
        FOREIGN KEY (user_id) REFERENCES users (id),
        UNIQUE(startup_id, user_id)
    )''')
    
    # Mentorship table - Mentorship connections between mentors and students
    c.execute('''CREATE TABLE IF NOT EXISTS mentorship (
        id INTEGER PRIMARY KEY,
        mentor_id INTEGER NOT NULL,
        mentee_id INTEGER NOT NULL,
        topic TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'pending' CHECK(status IN ('pending', 'accepted', 'rejected', 'completed')),
        message TEXT,
        created_at TIMESTAMP NOT NULL,
        updated_at TIMESTAMP,
        FOREIGN KEY (mentor_id) REFERENCES users (id),
        FOREIGN KEY (mentee_id) REFERENCES users (id)
    )''')
    
    # Mentorship Sessions - For tracking individual mentorship sessions
    c.execute('''CREATE TABLE IF NOT EXISTS mentorship_sessions (
        id INTEGER PRIMARY KEY,
        mentorship_id INTEGER NOT NULL,
        session_date TIMESTAMP NOT NULL,
        duration INTEGER, -- in minutes
        notes TEXT,
        status TEXT NOT NULL DEFAULT 'scheduled' CHECK(status IN ('scheduled', 'completed', 'cancelled')),
        FOREIGN KEY (mentorship_id) REFERENCES mentorship (id)
    )''')
    
    # Resources table - Educational resources and materials
    c.execute('''CREATE TABLE IF NOT EXISTS resources (
        id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        description TEXT NOT NULL,
        category TEXT NOT NULL,
        file_url TEXT,
        external_url TEXT,
        uploaded_by INTEGER NOT NULL,
        created_at TIMESTAMP NOT NULL,
        view_count INTEGER DEFAULT 0,
        FOREIGN KEY (uploaded_by) REFERENCES users (id)
    )''')
    
    # Events table - Workshops, webinars, and networking events
    c.execute('''CREATE TABLE IF NOT EXISTS events (
        id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        description TEXT NOT NULL,
        event_type TEXT NOT NULL CHECK(event_type IN ('workshop', 'webinar', 'networking', 'conference', 'other')),
        location TEXT,
        is_virtual BOOLEAN DEFAULT 0,
        event_date TIMESTAMP NOT NULL,
        duration INTEGER, -- in minutes
        organizer_id INTEGER NOT NULL,
        max_participants INTEGER,
        created_at TIMESTAMP NOT NULL,
        FOREIGN KEY (organizer_id) REFERENCES users (id)
    )''')
    
    # Event Registrations - For tracking event participants
    c.execute('''CREATE TABLE IF NOT EXISTS event_registrations (
        id INTEGER PRIMARY KEY,
        event_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        registration_date TIMESTAMP NOT NULL,
        attendance_status TEXT DEFAULT 'registered' CHECK(attendance_status IN ('registered', 'attended', 'no-show')),
        FOREIGN KEY (event_id) REFERENCES events (id),
        FOREIGN KEY (user_id) REFERENCES users (id),
        UNIQUE(event_id, user_id)
    )''')
    
    # Notifications table - System notifications for users
    c.execute('''CREATE TABLE IF NOT EXISTS notifications (
        id INTEGER PRIMARY KEY,
        user_id INTEGER NOT NULL,
        message TEXT NOT NULL,
        notification_type TEXT NOT NULL,
        related_id INTEGER, -- ID of related entity (job, application, etc.)
        is_read BOOLEAN DEFAULT 0,
        created_at TIMESTAMP NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )''')
    
    # Skills table - For standardized skill tags
    c.execute('''CREATE TABLE IF NOT EXISTS skills (
        id INTEGER PRIMARY KEY,
        name TEXT UNIQUE NOT NULL,
        category TEXT
    )''')
    
    # User Skills - Many-to-many relationship between users and skills
    c.execute('''CREATE TABLE IF NOT EXISTS user_skills (
        id INTEGER PRIMARY KEY,
        user_id INTEGER NOT NULL,
        skill_id INTEGER NOT NULL,
        proficiency_level TEXT CHECK(proficiency_level IN ('beginner', 'intermediate', 'advanced', 'expert')),
        FOREIGN KEY (user_id) REFERENCES users (id),
        FOREIGN KEY (skill_id) REFERENCES skills (id),
        UNIQUE(user_id, skill_id)
    )''')
    
    # Job Skills - Many-to-many relationship between jobs and required skills
    c.execute('''CREATE TABLE IF NOT EXISTS job_skills (
        id INTEGER PRIMARY KEY,
        job_id INTEGER NOT NULL,
        skill_id INTEGER NOT NULL,
        is_required BOOLEAN DEFAULT 1,
        FOREIGN KEY (job_id) REFERENCES jobs (id),
        FOREIGN KEY (skill_id) REFERENCES skills (id),
        UNIQUE(job_id, skill_id)
    )''')
    
    # Create admin user if it doesn't exist
    c.execute("SELECT COUNT(*) FROM users WHERE user_type = 'admin'")
    if c.fetchone()[0] == 0:
        admin_password = generate_password_hash('admin123')
        c.execute("INSERT INTO users (email, password, name, user_type, created_at) VALUES (?, ?, ?, ?, ?)",
                 ('admin@startsmart.com', admin_password, 'System Administrator', 'admin', datetime.now()))
    
    # Insert sample skills
    sample_skills = [
        ('Python', 'Programming'),
        ('JavaScript', 'Programming'),
        ('HTML/CSS', 'Web Development'),
        ('React', 'Web Development'),
        ('Node.js', 'Web Development'),
        ('SQL', 'Database'),
        ('Project Management', 'Business'),
        ('Marketing', 'Business'),
        ('Data Analysis', 'Data Science'),
        ('Machine Learning', 'Data Science'),
        ('UI/UX Design', 'Design'),
        ('Graphic Design', 'Design'),
        ('Content Writing', 'Communication'),
        ('Public Speaking', 'Communication'),
        ('Leadership', 'Soft Skills'),
        ('Teamwork', 'Soft Skills'),
        ('Problem Solving', 'Soft Skills')
    ]
    
    for skill in sample_skills:
        try:
            c.execute("INSERT INTO skills (name, category) VALUES (?, ?)", skill)
        except sqlite3.IntegrityError:
            # Skill already exists
            pass
    
    conn.commit()
    conn.close()
    print("Database setup complete!")

if __name__ == "__main__":
    setup_database()