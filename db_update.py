import sqlite3
from datetime import datetime

def update_database_schema():
    """
    Update the existing database schema to match the new structure.
    This script ensures backward compatibility while adding new features.
    """
    print("Updating database schema...")
    
    conn = sqlite3.connect('startsmart.db')
    c = conn.cursor()
    
    # Check if tables exist and add missing columns
    
    # Users table updates
    try:
        c.execute("ALTER TABLE users ADD COLUMN last_login TIMESTAMP")
    except sqlite3.OperationalError:
        pass  # Column already exists
    
    # Jobs table updates
    try:
        c.execute("ALTER TABLE jobs ADD COLUMN is_active BOOLEAN DEFAULT 1")
    except sqlite3.OperationalError:
        pass  # Column already exists
    
    # Applications table updates
    try:
        c.execute("ALTER TABLE applications ADD COLUMN cover_letter TEXT")
    except sqlite3.OperationalError:
        pass  # Column already exists
    
    try:
        c.execute("ALTER TABLE applications ADD COLUMN updated_at TIMESTAMP")
    except sqlite3.OperationalError:
        pass  # Column already exists
    
    # Startups table updates
    try:
        c.execute("ALTER TABLE startups ADD COLUMN industry TEXT")
    except sqlite3.OperationalError:
        pass  # Column already exists
        
    try:
        c.execute("ALTER TABLE startups ADD COLUMN logo_image TEXT")
    except sqlite3.OperationalError:
        pass  # Column already exists
    
    try:
        c.execute("ALTER TABLE startups ADD COLUMN website_url TEXT")
    except sqlite3.OperationalError:
        pass  # Column already exists
        
    try:
        c.execute("ALTER TABLE startups ADD COLUMN stage TEXT")
    except sqlite3.OperationalError:
        pass  # Column already exists
    
    try:
        c.execute("ALTER TABLE startups ADD COLUMN funding_status TEXT")
    except sqlite3.OperationalError:
        pass  # Column already exists
    
    try:
        c.execute("ALTER TABLE startups ADD COLUMN team_size INTEGER DEFAULT 1")
    except sqlite3.OperationalError:
        pass  # Column already exists
    
    # Mentorship table updates
    try:
        c.execute("ALTER TABLE mentorship ADD COLUMN updated_at TIMESTAMP")
    except sqlite3.OperationalError:
        pass  # Column already exists
    
    # Resources table updates
    try:
        c.execute("ALTER TABLE resources ADD COLUMN external_url TEXT")
    except sqlite3.OperationalError:
        pass  # Column already exists
    
    try:
        c.execute("ALTER TABLE resources ADD COLUMN view_count INTEGER DEFAULT 0")
    except sqlite3.OperationalError:
        pass  # Column already exists
    
    # Create new tables if they don't exist
    
    # Startup Team Members
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
    
    # Mentorship Sessions
    c.execute('''CREATE TABLE IF NOT EXISTS mentorship_sessions (
        id INTEGER PRIMARY KEY,
        mentorship_id INTEGER NOT NULL,
        session_date TIMESTAMP NOT NULL,
        duration INTEGER,
        notes TEXT,
        status TEXT NOT NULL DEFAULT 'scheduled' CHECK(status IN ('scheduled', 'completed', 'cancelled')),
        FOREIGN KEY (mentorship_id) REFERENCES mentorship (id)
    )''')
    
    # Events
    c.execute('''CREATE TABLE IF NOT EXISTS events (
        id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        description TEXT NOT NULL,
        event_type TEXT NOT NULL CHECK(event_type IN ('workshop', 'webinar', 'networking', 'conference', 'other')),
        location TEXT,
        is_virtual BOOLEAN DEFAULT 0,
        event_date TIMESTAMP NOT NULL,
        duration INTEGER,
        organizer_id INTEGER NOT NULL,
        max_participants INTEGER,
        created_at TIMESTAMP NOT NULL,
        FOREIGN KEY (organizer_id) REFERENCES users (id)
    )''')
    
    # Event Registrations
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
    
    # Notifications
    c.execute('''CREATE TABLE IF NOT EXISTS notifications (
        id INTEGER PRIMARY KEY,
        user_id INTEGER NOT NULL,
        message TEXT NOT NULL,
        notification_type TEXT NOT NULL,
        related_id INTEGER,
        is_read BOOLEAN DEFAULT 0,
        created_at TIMESTAMP NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )''')
    
    # Skills
    c.execute('''CREATE TABLE IF NOT EXISTS skills (
        id INTEGER PRIMARY KEY,
        name TEXT UNIQUE NOT NULL,
        category TEXT
    )''')
    
    # User Skills
    c.execute('''CREATE TABLE IF NOT EXISTS user_skills (
        id INTEGER PRIMARY KEY,
        user_id INTEGER NOT NULL,
        skill_id INTEGER NOT NULL,
        proficiency_level TEXT CHECK(proficiency_level IN ('beginner', 'intermediate', 'advanced', 'expert')),
        FOREIGN KEY (user_id) REFERENCES users (id),
        FOREIGN KEY (skill_id) REFERENCES skills (id),
        UNIQUE(user_id, skill_id)
    )''')
    
    # Job Skills
    c.execute('''CREATE TABLE IF NOT EXISTS job_skills (
        id INTEGER PRIMARY KEY,
        job_id INTEGER NOT NULL,
        skill_id INTEGER NOT NULL,
        is_required BOOLEAN DEFAULT 1,
        FOREIGN KEY (job_id) REFERENCES jobs (id),
        FOREIGN KEY (skill_id) REFERENCES skills (id),
        UNIQUE(job_id, skill_id)
    )''')
    
    conn.commit()
    conn.close()
    print("Database schema update complete!")

if __name__ == "__main__":
    update_database_schema()