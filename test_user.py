#!/usr/bin/env python3
"""
Simple script to test user registration and login functionality
"""
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import sys

def create_test_user():
    """Create a test user for login testing"""
    try:
        # Initialize database first
        from db_setup import setup_database
        setup_database()
        print("✅ Database initialized")
        
        # Connect to database
        conn = sqlite3.connect('startsmart.db')
        c = conn.cursor()
        
        # Test user data
        email = 'j.kur@alustudent.com'
        password = 'password123'  # Default test password
        name = 'John Kur'
        user_type = 'student'
        
        # Check if user already exists
        c.execute("SELECT id, email FROM users WHERE email = ?", (email,))
        existing_user = c.fetchone()
        
        if existing_user:
            print(f"✅ User {email} already exists with ID: {existing_user[0]}")
        else:
            # Create new user
            password_hash = generate_password_hash(password)
            c.execute("""INSERT INTO users (email, password, name, user_type, created_at) 
                         VALUES (?, ?, ?, ?, ?)""",
                     (email, password_hash, name, user_type, datetime.now()))
            conn.commit()
            print(f"✅ User {email} created successfully")
        
        # Test login
        c.execute("SELECT id, name, password, email, user_type FROM users WHERE email = ?", (email,))
        user = c.fetchone()
        
        if user:
            print(f"✅ User found: {user[1]} ({user[3]})")
            # Test password verification
            if check_password_hash(user[2], password):
                print(f"✅ Password verification successful for {email}")
            else:
                print(f"❌ Password verification failed for {email}")
                print("Try using password: 'password123'")
        else:
            print(f"❌ User {email} not found in database")
        
        # Show all users for debugging
        c.execute("SELECT id, email, name, user_type FROM users")
        all_users = c.fetchall()
        print(f"\n📊 All users in database ({len(all_users)}):")
        for user in all_users:
            print(f"  ID: {user[0]}, Email: {user[1]}, Name: {user[2]}, Type: {user[3]}")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    create_test_user()
