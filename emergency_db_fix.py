"""
EMERGENCY: Fix database and auth for Render deployment
This will ensure database exists and demo users are created
"""
import sqlite3
import os
from datetime import datetime

# Import werkzeug with fallback for Render deployment  
try:
    from werkzeug.security import generate_password_hash
except ImportError:
    print("Werkzeug not available - trying alternative import")
    import hashlib
    def generate_password_hash(password, method='pbkdf2:sha256'):
        # Simple fallback hash if werkzeug fails
        return hashlib.sha256(password.encode()).hexdigest()

def emergency_db_setup():
    """Create database tables and demo users for Render"""
    
    print("🚨 EMERGENCY DATABASE SETUP...")
    
    db_path = 'startsmart.db'
    
    try:
        # Remove existing database to start fresh
        if os.path.exists(db_path):
            os.remove(db_path)
            print("   Removed existing database")
        
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        
        # Create users table
        print("   Creating users table...")
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
        print("   Creating jobs table...")
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
        print("   Creating applications table...")
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
        print("✅ Database tables created successfully")
        
        # Create demo users for video
        print("   Creating demo users...")
        demo_users = [
            ('student@demo.com', 'Demo123!', 'Demo Student', 'student'),
            ('recruiter@demo.com', 'Demo123!', 'Demo Recruiter', 'recruiter'), 
            ('admin@demo.com', 'Demo123!', 'Demo Admin', 'admin'),
            ('videotest@gmail.com', 'VideoTest123!', 'Video Test User', 'student')
        ]
        
        for email, password, name, user_type in demo_users:
            password_hash = generate_password_hash(password, method='pbkdf2:sha256')
            c.execute("""INSERT INTO users (email, password, name, user_type, created_at, is_active) 
                         VALUES (?, ?, ?, ?, ?, ?)""",
                     (email, password_hash, name, user_type, datetime.now(), 1))
            print(f"   ✅ Created: {email}")
        
        conn.commit()
        
        # Verify everything works
        c.execute("SELECT COUNT(*) FROM users")
        user_count = c.fetchone()[0]
        
        print(f"✅ Database ready with {user_count} users")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Emergency setup failed: {e}")
        return False

if __name__ == "__main__":
    if emergency_db_setup():
        print("\n🎉 EMERGENCY SETUP COMPLETE!")
        print("📋 Demo credentials for video:")
        print("   Email: student@demo.com")
        print("   Password: Demo123!")
        print("   OR")
        print("   Email: videotest@gmail.com") 
        print("   Password: VideoTest123!")
    else:
        print("\n❌ Emergency setup failed!")
