#!/usr/bin/env python3
"""
Manual Registration Test
Tests the actual registration functionality
"""

import requests
import json

def test_registration():
    """Test user registration with valid data"""
    print("🧪 Testing User Registration...")
    
    # Test data
    registration_data = {
        'name': 'Test User',
        'email': 'testuser123@example.com',
        'password': 'TestPass123!',
        'confirmPassword': 'TestPass123!',
        'user_type': 'student',
        'agreeTerms': 'on'
    }
    
    try:
        # First, get the registration page to establish session
        session = requests.Session()
        response = session.get('http://127.0.0.1:5000/register')
        print(f"📄 Registration page status: {response.status_code}")
        
        if response.status_code != 200:
            print("❌ Cannot access registration page")
            return False
        
        # Submit registration form
        response = session.post('http://127.0.0.1:5000/register', data=registration_data)
        print(f"📤 Registration submission status: {response.status_code}")
        
        # Check response
        if response.status_code == 200:
            # Check if we got redirected or stayed on the page
            if 'login' in response.url or 'dashboard' in response.url:
                print("✅ Registration successful - redirected to login/dashboard")
                return True
            elif 'register' in response.url:
                # Check for success/error messages
                if 'Registration successful' in response.text:
                    print("✅ Registration successful")
                    return True
                elif 'Email already exists' in response.text:
                    print("⚠️ Email already exists - this is expected behavior")
                    return True
                else:
                    print("❌ Registration failed - stayed on register page")
                    print("Response content preview:", response.text[:500])
                    return False
            else:
                print("🤔 Unexpected response URL:", response.url)
                return False
        else:
            print(f"❌ Registration failed with status: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Registration test error: {e}")
        return False

def test_login():
    """Test user login with existing credentials"""
    print("\n🧪 Testing User Login...")
    
    # Test with existing user (from the database)
    login_data = {
        'email': 'testuser123@example.com',
        'password': 'TestPass123!'
    }
    
    try:
        session = requests.Session()
        
        # Get login page
        response = session.get('http://127.0.0.1:5000/login')
        print(f"📄 Login page status: {response.status_code}")
        
        if response.status_code != 200:
            print("❌ Cannot access login page")
            return False
        
        # Submit login form
        response = session.post('http://127.0.0.1:5000/login', data=login_data)
        print(f"📤 Login submission status: {response.status_code}")
        
        # Check response
        if response.status_code == 200:
            if 'dashboard' in response.url:
                print("✅ Login successful - redirected to dashboard")
                return True
            elif 'login' in response.url:
                if 'Invalid email or password' in response.text:
                    print("❌ Login failed - invalid credentials")
                    return False
                else:
                    print("❌ Login failed - stayed on login page")
                    return False
            else:
                print("🤔 Unexpected login response URL:", response.url)
                return False
        else:
            print(f"❌ Login failed with status: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Login test error: {e}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("🔍 MANUAL FUNCTIONALITY TEST")
    print("=" * 50)
    
    # Test registration
    reg_success = test_registration()
    
    # Test login
    login_success = test_login()
    
    print("\n" + "=" * 50)
    print("📊 MANUAL TEST RESULTS")
    print("=" * 50)
    print(f"Registration: {'✅ PASS' if reg_success else '❌ FAIL'}")
    print(f"Login: {'✅ PASS' if login_success else '❌ FAIL'}")
    
    if reg_success and login_success:
        print("\n🎉 All manual tests passed!")
    else:
        print("\n⚠️ Some manual tests failed - investigation needed")
