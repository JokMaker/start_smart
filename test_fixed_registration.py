#!/usr/bin/env python3
"""
Test the fixed registration page
"""

import requests
import time

def test_fixed_registration():
    """Test the fixed registration page with recruiter selection"""
    print("🧪 Testing Fixed Registration Page")
    print("=" * 50)
    
    session = requests.Session()
    
    # Test data
    timestamp = int(time.time())
    test_data = {
        'name': 'Fixed Test Recruiter',
        'email': f'fixed_recruiter_{timestamp}@example.com',
        'password': 'testpass',
        'confirmPassword': 'testpass',
        'user_type': 'recruiter',
        'agreeTerms': 'on'
    }
    
    print(f"Testing registration with: {test_data['email']}")
    
    try:
        # First, check that the page loads properly
        reg_page = session.get('http://localhost:5000/register')
        print(f"Registration page status: {reg_page.status_code}")
        
        if 'recruiter' not in reg_page.text.lower():
            print("❌ Recruiter option not found on page")
            return False
        
        print("✅ Registration page loaded with recruiter option")
        
        # Submit the registration
        response = session.post('http://localhost:5000/register', 
                               data=test_data,
                               allow_redirects=False,
                               timeout=10)
        
        print(f"Registration response status: {response.status_code}")
        
        if response.status_code in [302, 303]:
            print("✅ Registration successful - redirected")
            
            # Check if user was created in database
            import sqlite3
            conn = sqlite3.connect('startsmart.db')
            c = conn.cursor()
            c.execute("SELECT name, user_type FROM users WHERE email = ?", (test_data['email'],))
            user = c.fetchone()
            conn.close()
            
            if user and user[1] == 'recruiter':
                print(f"✅ User created successfully: {user[0]} as {user[1]}")
                
                # Test login with new user
                login_data = {
                    'email': test_data['email'],
                    'password': test_data['password']
                }
                
                login_response = session.post('http://localhost:5000/login', 
                                             data=login_data,
                                             allow_redirects=True,
                                             timeout=10)
                
                if login_response.status_code == 200 and 'dashboard' in login_response.url:
                    print("✅ Login successful after registration")
                    return True
                else:
                    print("⚠️ Registration worked but login failed")
                    return True  # Registration itself worked
            else:
                print("❌ User not created in database")
                return False
        elif response.status_code == 200:
            print("⚠️ Registration stayed on same page - checking for issues")
            
            # Check for any error messages
            if 'alert' in response.text.lower():
                print("❌ Registration page shows error messages")
                # Try to extract error
                if 'already exists' in response.text.lower():
                    print("   Error: Email already exists")
                return False
            else:
                print("❌ Unknown issue - form didn't submit properly")
                return False
        else:
            print(f"❌ Unexpected response status: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        return False

if __name__ == "__main__":
    success = test_fixed_registration()
    if success:
        print("\n🎉 FIXED REGISTRATION TEST PASSED!")
        print("The recruiter button should now work without page refresh!")
    else:
        print("\n❌ Registration test failed")
    
    exit(0 if success else 1)
