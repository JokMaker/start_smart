import sqlite3
from datetime import datetime

def fix_database():
    """Fix database schema issues for login/registration"""
    conn = sqlite3.connect('startsmart.db')
    c = conn.cursor()
    
    try:
        # Add missing is_active column
        c.execute("ALTER TABLE users ADD COLUMN is_active BOOLEAN DEFAULT 1")
        print("Added is_active column")
    except sqlite3.OperationalError:
        print("is_active column already exists")
    
    # Update all existing users to be active
    c.execute("UPDATE users SET is_active = 1 WHERE is_active IS NULL")
    
    # Ensure jobs table has is_active column
    try:
        c.execute("ALTER TABLE jobs ADD COLUMN is_active BOOLEAN DEFAULT 1")
        print("Added is_active column to jobs")
    except sqlite3.OperationalError:
        print("jobs.is_active column already exists")
    
    # Update all existing jobs to be active
    c.execute("UPDATE jobs SET is_active = 1 WHERE is_active IS NULL")
    
    conn.commit()
    conn.close()
    print("Database schema fixed!")

if __name__ == "__main__":
    fix_database()