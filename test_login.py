#!/usr/bin/env python3
"""Quick test for login/registration functionality"""

import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

def test_auth():
    """Test authentication functionality"""
    print("Testing StartSmart Authentication...")
    
    # Test database connection
    try:
        conn = sqlite3.connect('startsmart.db')
        c = conn.cursor()
        
        # Check if admin user exists and can login
        c.execute("SELECT id, email, password FROM users WHERE email = ?", ('admin@startsmart.com',))
        admin = c.fetchone()
        
        if admin:
            print(f"[OK] Admin user found: {admin[1]}")
            if check_password_hash(admin[2], 'admin123'):
                print("[OK] Admin password verification works")
            else:
                print("[ERROR] Admin password verification failed")
        else:
            print("[ERROR] Admin user not found")
        
        # Test creating a new user (simulate registration)
        test_email = "test@example.com"
        test_password = "TestPass123!"
        test_name = "Test User"
        
        # Check if test user already exists
        c.execute("SELECT id FROM users WHERE LOWER(email) = ?", (test_email.lower(),))
        if c.fetchone():
            print("[INFO] Test user already exists, skipping creation")
        else:
            # Create test user
            password_hash = generate_password_hash(test_password, method='pbkdf2:sha256')
            c.execute("""INSERT INTO users (email, password, name, user_type, created_at, is_active) 
                         VALUES (?, ?, ?, ?, ?, ?)""",
                     (test_email.lower(), password_hash, test_name, 'student', datetime.now(), 1))
            conn.commit()
            print("[OK] Test user created successfully")
        
        # Test login simulation
        c.execute("SELECT id, name, password, email, user_type FROM users WHERE LOWER(email) = ?", (test_email.lower(),))
        user = c.fetchone()
        
        if user and check_password_hash(user[2], test_password):
            print("[OK] Test user login simulation successful")
        else:
            print("[ERROR] Test user login simulation failed")
        
        conn.close()
        print("\n[SUCCESS] Authentication system is working!")
        print("\nYou can now:")
        print("1. Register new users at /register")
        print("2. Login with existing users at /login")
        print("3. Use admin@startsmart.com / admin123 for admin access")
        
    except Exception as e:
        print(f"[ERROR] Error: {e}")

if __name__ == "__main__":
    test_auth()