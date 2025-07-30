#!/usr/bin/env python3
"""
Test Real User Login
Tests actual user credentials from the database
"""

import requests
import json

def test_real_user_login():
    """Test login with real user credentials"""
    print("🧪 Testing Real User Login...")
    
    # Test different user types
    test_credentials = [
        {
            'email': 'j.kur@alustudent.com',
            'password': 'password123',
            'type': 'Student'
        },
        {
            'email': 'mentor@example.com',
            'password': 'mentor123',
            'type': 'Mentor'
        },
        {
            'email': 'recruiter@company.com',
            'password': 'recruiter123',
            'type': 'Recruiter'
        },
        {
            'email': 'admin@startsmart.com',
            'password': 'admin123',
            'type': 'Admin'
        }
    ]
    
    print("=" * 60)
    print("🔐 TESTING REAL USER CREDENTIALS")
    print("=" * 60)
    
    for creds in test_credentials:
        print(f"\n🧪 Testing {creds['type']} login...")
        
        try:
            session = requests.Session()
            
            # Get login page
            response = session.get('http://127.0.0.1:5000/login')
            if response.status_code != 200:
                print(f"❌ Cannot access login page")
                continue
            
            # Submit login form
            login_data = {
                'email': creds['email'],
                'password': creds['password']
            }
            
            response = session.post('http://127.0.0.1:5000/login', data=login_data)
            
            # Check response
            if response.status_code == 200:
                if 'dashboard' in response.url:
                    print(f"✅ {creds['type']} login successful!")
                    print(f"   📧 Email: {creds['email']}")
                    print(f"   🔑 Password: {creds['password']}")
                    print(f"   🎯 Redirected to: {response.url}")
                elif 'login' in response.url:
                    if 'Invalid email or password' in response.text:
                        print(f"❌ {creds['type']} login failed - invalid credentials")
                    else:
                        print(f"❌ {creds['type']} login failed - unknown error")
                else:
                    print(f"🤔 {creds['type']} unexpected response: {response.url}")
            else:
                print(f"❌ {creds['type']} login failed with status: {response.status_code}")
                
        except Exception as e:
            print(f"❌ {creds['type']} login test error: {e}")
    
    print("\n" + "=" * 60)
    print("✅ REAL USER LOGIN TESTING COMPLETE")
    print("=" * 60)

if __name__ == "__main__":
    test_real_user_login()
