"""
Simple database verification for Render deployment
"""
import sqlite3
import os

def check_database():
    """Check if database exists and has required tables"""
    try:
        print("🔍 Checking database...")
        
        # Check if database file exists
        if os.path.exists('startsmart.db'):
            print("✅ Database file exists")
        else:
            print("❌ Database file not found")
            return False
        
        # Check database connection
        conn = sqlite3.connect('startsmart.db')
        c = conn.cursor()
        
        # Check for users table
        c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
        if c.fetchone():
            print("✅ Users table exists")
            
            # Check user count
            c.execute("SELECT COUNT(*) FROM users")
            count = c.fetchone()[0]
            print(f"✅ Users in database: {count}")
        else:
            print("❌ Users table missing")
            return False
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Database check failed: {e}")
        return False

def create_minimal_database():
    """Create minimal database structure"""
    try:
        print("🔧 Creating minimal database...")
        
        conn = sqlite3.connect('startsmart.db')
        c = conn.cursor()
        
        # Create users table
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
        
        # Create jobs table
        c.execute('''CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            company TEXT NOT NULL,
            description TEXT NOT NULL,
            location TEXT,
            job_type TEXT,
            salary TEXT,
            application_url TEXT,
            posted_by INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            is_active INTEGER DEFAULT 1
        )''')
        
        conn.commit()
        conn.close()
        
        print("✅ Minimal database created successfully")
        return True
        
    except Exception as e:
        print(f"❌ Database creation failed: {e}")
        return False

if __name__ == "__main__":
    if not check_database():
        create_minimal_database()
        check_database()
