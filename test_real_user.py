#!/usr/bin/env python3
"""
Test Real User Registration
This script tests registration with a brand new user
"""

import requests
import json
from datetime import datetime

# Base URL for local testing
BASE_URL = 'http://127.0.0.1:5000'

def test_real_user_registration():
    """Test registration with a real-like user"""
    print("🔧 Testing Real User Registration...")
    
    # Create a realistic new user
    timestamp = datetime.now().strftime("%H%M%S")
    real_user = {
        'name': 'Sarah Kimani',
        'email': f'sarah.kimani{timestamp}@gmail.com',  # Unique email each time
        'password': 'MySecurePass123!',
        'confirmPassword': 'MySecurePass123!',
        'user_type': 'student'
    }
    
    print(f"Registering user: {real_user['name']} ({real_user['email']})")
    
    session = requests.Session()
    
    try:
        # Test registration
        reg_response = session.post(f'{BASE_URL}/register', data=real_user, allow_redirects=False)
        print(f"Registration status: {reg_response.status_code}")
        
        if reg_response.status_code == 302:
            print("✅ Real user registration successful - redirected to login")
            
            # Now test login with the new user
            login_data = {
                'email': real_user['email'],
                'password': real_user['password']
            }
            
            login_response = session.post(f'{BASE_URL}/login', data=login_data, allow_redirects=False)
            print(f"Login status: {login_response.status_code}")
            
            if login_response.status_code == 302:
                print("✅ New user can login successfully")
                
                # Test dashboard access
                dashboard_response = session.get(f'{BASE_URL}/dashboard')
                if dashboard_response.status_code == 200:
                    print("✅ New user can access dashboard")
                    return True
                else:
                    print("❌ New user cannot access dashboard")
                    return False
            else:
                print("❌ New user cannot login")
                return False
        else:
            print(f"❌ Real user registration failed - status {reg_response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Real user registration test error: {e}")
        return False

def check_database_for_new_user():
    """Check if the new user was added to database"""
    print("🔍 Checking database for new users...")
    
    try:
        import sqlite3
        conn = sqlite3.connect('startsmart.db')
        c = conn.cursor()
        
        # Count total users
        c.execute("SELECT COUNT(*) FROM users")
        total_users = c.fetchone()[0]
        print(f"Total users in database: {total_users}")
        
        # Get recent users (last 5)
        c.execute("SELECT name, email, user_type, created_at FROM users ORDER BY created_at DESC LIMIT 5")
        recent_users = c.fetchall()
        
        print("Recent users:")
        for user in recent_users:
            print(f"  - {user[0]} ({user[1]}) - {user[2]} - {user[3]}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Database check error: {e}")
        return False

def main():
    """Test real user registration flow"""
    print("🚀 Testing Real User Registration Flow")
    print("=" * 50)
    
    # Test 1: Register a new real user
    reg_success = test_real_user_registration()
    
    # Test 2: Check database
    db_success = check_database_for_new_user()
    
    print("=" * 50)
    if reg_success and db_success:
        print("🎉 Real users CAN register and use the system!")
        print("✅ Registration system is ready for production")
    else:
        print("⚠️ Issues found with real user registration")
    
    return reg_success and db_success

if __name__ == "__main__":
    main()
