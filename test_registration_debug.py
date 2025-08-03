#!/usr/bin/env python3
"""
Simple Registration Test
"""

import sqlite3
from werkzeug.security import generate_password_hash
from datetime import datetime

def test_direct_registration():
    """Test direct database registration"""
    print("🔍 Testing direct database registration...")
    
    test_user = {
        'email': 'direct_test@example.com',
        'password': 'TestPassword123!',
        'name': 'Direct Test User',
        'user_type': 'student'
    }
    
    try:
        conn = sqlite3.connect('startsmart.db')
        cursor = conn.cursor()
        
        # Check if user already exists
        cursor.execute("SELECT id FROM users WHERE email = ?", (test_user['email'],))
        existing = cursor.fetchone()
        
        if existing:
            print(f"   User already exists with ID: {existing[0]}")
            cursor.execute("DELETE FROM users WHERE email = ?", (test_user['email'],))
            print(f"   Deleted existing user")
        
        # Hash password
        password_hash = generate_password_hash(test_user['password'])
        
        # Insert user
        cursor.execute("""
            INSERT INTO users (email, password, name, user_type, created_at) 
            VALUES (?, ?, ?, ?, ?)
        """, (
            test_user['email'],
            password_hash,
            test_user['name'],
            test_user['user_type'],
            datetime.now()
        ))
        
        conn.commit()
        user_id = cursor.lastrowid
        
        print(f"   ✅ User created with ID: {user_id}")
        
        # Verify user was created
        cursor.execute("SELECT id, email, name, user_type FROM users WHERE id = ?", (user_id,))
        user = cursor.fetchone()
        
        if user:
            print(f"   ✅ Verification: {user[2]} ({user[1]}) - {user[3]}")
            conn.close()
            return True
        else:
            print("   ❌ User not found after creation")
            conn.close()
            return False
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
        if conn:
            conn.close()
        return False

def test_web_registration():
    """Test web form registration"""
    print("\n🔍 Testing web form registration...")
    
    import requests
    
    test_user = {
        'email': 'web_test_user@example.com',
        'password': 'TestPassword123!',
        'confirmPassword': 'TestPassword123!',
        'name': 'Web Test User',
        'user_type': 'student'
    }
    
    try:
        session = requests.Session()
        
        # Submit registration
        response = session.post(
            'http://127.0.0.1:5000/register',
            data=test_user
        )
        
        print(f"   Response status: {response.status_code}")
        print(f"   Response URL: {response.url}")
        
        # Check if redirected to login (success)
        if 'login' in response.url:
            print("   ✅ Redirected to login page (likely success)")
            
            # Check database
            conn = sqlite3.connect('startsmart.db')
            cursor = conn.cursor()
            cursor.execute("SELECT id, email, name FROM users WHERE email = ?", (test_user['email'],))
            user = cursor.fetchone()
            conn.close()
            
            if user:
                print(f"   ✅ User found in database: {user[2]} ({user[1]})")
                return True
            else:
                print("   ❌ User not found in database despite redirect")
                return False
        else:
            print("   ❌ Not redirected to login")
            print(f"   Response content (first 300 chars): {response.text[:300]}")
            return False
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def main():
    print("🚀 StartSmart Registration Debug Test")
    print("=" * 50)
    
    # Test 1: Direct database registration
    direct_success = test_direct_registration()
    
    # Test 2: Web form registration
    web_success = test_web_registration()
    
    print("\n" + "=" * 50)
    print("📊 RESULTS:")
    print(f"Direct DB Registration: {'✅ PASS' if direct_success else '❌ FAIL'}")
    print(f"Web Form Registration: {'✅ PASS' if web_success else '❌ FAIL'}")
    
    if direct_success and web_success:
        print("\n🎉 Both registration methods work!")
    elif direct_success:
        print("\n⚠️ Database works, but web form has issues")
    else:
        print("\n❌ Both registration methods have issues")

if __name__ == "__main__":
    main()
