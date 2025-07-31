#!/usr/bin/env python3
"""
Test Authentication with Fresh Database
This script tests registration and login functionality
"""

import requests
import json

# Base URL for local testing
BASE_URL = 'http://127.0.0.1:5000'

def test_registration():
    """Test user registration"""
    print("🔧 Testing Registration...")
    
    test_user = {
        'name': 'Test User',
        'email': 'testuser@example.com',
        'password': 'TestPass123!',
        'confirmPassword': 'TestPass123!',
        'user_type': 'student'
    }
    
    session = requests.Session()
    
    try:
        # Test registration
        reg_response = session.post(f'{BASE_URL}/register', data=test_user, allow_redirects=False)
        print(f"Registration status: {reg_response.status_code}")
        
        if reg_response.status_code == 302:
            print("✅ Registration successful - redirected to login")
            return True
        elif reg_response.status_code == 200:
            print("⚠️ Registration returned 200 - checking for errors in page content")
            if 'error' in reg_response.text.lower() or 'invalid' in reg_response.text.lower():
                print("❌ Registration failed - validation errors found")
                return False
            else:
                print("✅ Registration successful - form submitted")
                return True
        else:
            print(f"❌ Registration failed - status {reg_response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Registration test error: {e}")
        return False

def test_login():
    """Test user login with demo user"""
    print("🔧 Testing Login...")
    
    login_data = {
        'email': 'student@example.com',
        'password': 'student123'
    }
    
    session = requests.Session()
    
    try:
        # Test login
        login_response = session.post(f'{BASE_URL}/login', data=login_data, allow_redirects=False)
        print(f"Login status: {login_response.status_code}")
        
        if login_response.status_code == 302:
            print("✅ Login successful - redirected to dashboard")
            
            # Test dashboard access
            dashboard_response = session.get(f'{BASE_URL}/dashboard')
            if dashboard_response.status_code == 200:
                print("✅ Dashboard accessible after login")
                return True
            else:
                print("❌ Dashboard not accessible after login")
                return False
        else:
            print(f"❌ Login failed - status {login_response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Login test error: {e}")
        return False

def test_home_page():
    """Test home page loads properly"""
    print("🔧 Testing Home Page...")
    
    try:
        response = requests.get(f'{BASE_URL}/')
        if response.status_code == 200 and 'StartSmart' in response.text:
            print("✅ Home page loads successfully")
            return True
        else:
            print(f"❌ Home page failed - status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Home page test error: {e}")
        return False

def main():
    """Run all authentication tests"""
    print("🚀 Testing StartSmart Authentication System")
    print("=" * 50)
    
    results = []
    
    # Test home page first
    results.append(("Home Page", test_home_page()))
    
    # Test existing demo user login
    results.append(("Demo User Login", test_login()))
    
    # Test new user registration
    results.append(("New User Registration", test_registration()))
    
    print("=" * 50)
    print("📊 Test Results:")
    
    all_passed = True
    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"  {test_name}: {status}")
        if not passed:
            all_passed = False
    
    print("=" * 50)
    if all_passed:
        print("🎉 All tests passed! Authentication system is working!")
    else:
        print("⚠️ Some tests failed. Check the output above.")
    
    return all_passed

if __name__ == "__main__":
    main()
