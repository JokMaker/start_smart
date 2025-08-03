#!/usr/bin/env python3
"""
Comprehensive Authentication Test for StartSmart Platform
Tests registration and login functionality end-to-end
"""

import sqlite3
import requests
import time
import random
import string
from datetime import datetime

def generate_test_email():
    """Generate a unique test email"""
    timestamp = int(time.time())
    random_str = ''.join(random.choices(string.ascii_lowercase, k=6))
    return f"test_{timestamp}_{random_str}@example.com"

def test_database_connection():
    """Test database connectivity and structure"""
    print("🔍 Testing database connection...")
    try:
        conn = sqlite3.connect('startsmart.db')
        c = conn.cursor()
        
        # Check if users table exists and has correct structure
        c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
        users_table = c.fetchone()
        
        if not users_table:
            print("❌ Users table does not exist!")
            return False
            
        # Check table structure
        c.execute("PRAGMA table_info(users)")
        columns = c.fetchall()
        required_columns = ['id', 'email', 'password', 'name', 'user_type']
        column_names = [col[1] for col in columns]
        
        for req_col in required_columns:
            if req_col not in column_names:
                print(f"❌ Required column '{req_col}' missing from users table!")
                return False
        
        # Check current user count
        c.execute("SELECT COUNT(*) FROM users")
        user_count = c.fetchone()[0]
        print(f"✅ Database connected. Current users: {user_count}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

def test_server_status():
    """Test if the Flask server is running"""
    print("🔍 Testing server status...")
    try:
        response = requests.get('http://localhost:5000/health', timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Server is running. Status: {data.get('status', 'unknown')}")
            return True
        else:
            print(f"❌ Server returned status code: {response.status_code}")
            return False
    except requests.RequestException as e:
        print(f"❌ Server connection failed: {e}")
        return False

def test_registration_page():
    """Test registration page accessibility"""
    print("🔍 Testing registration page...")
    try:
        response = requests.get('http://localhost:5000/register', timeout=5)
        if response.status_code == 200:
            if 'register' in response.text.lower() and 'email' in response.text.lower():
                print("✅ Registration page is accessible and contains expected elements")
                return True
            else:
                print("❌ Registration page missing expected content")
                return False
        else:
            print(f"❌ Registration page returned status: {response.status_code}")
            return False
    except requests.RequestException as e:
        print(f"❌ Registration page test failed: {e}")
        return False

def test_login_page():
    """Test login page accessibility"""
    print("🔍 Testing login page...")
    try:
        response = requests.get('http://localhost:5000/login', timeout=5)
        if response.status_code == 200:
            if 'login' in response.text.lower() and 'email' in response.text.lower():
                print("✅ Login page is accessible and contains expected elements")
                return True
            else:
                print("❌ Login page missing expected content")
                return False
        else:
            print(f"❌ Login page returned status: {response.status_code}")
            return False
    except requests.RequestException as e:
        print(f"❌ Login page test failed: {e}")
        return False

def test_user_registration():
    """Test user registration functionality"""
    print("🔍 Testing user registration...")
    test_email = generate_test_email()
    test_password = "TestPass123!"
    test_name = "Test User"
    test_user_type = "student"
    
    try:
        # First, get the registration page to establish session
        session = requests.Session()
        reg_page = session.get('http://localhost:5000/register')
        
        if reg_page.status_code != 200:
            print(f"❌ Could not access registration page: {reg_page.status_code}")
            return False, None
        
        # Submit registration form
        registration_data = {
            'email': test_email,
            'password': test_password,
            'confirmPassword': test_password,
            'name': test_name,
            'user_type': test_user_type
        }
        
        response = session.post('http://localhost:5000/register', 
                              data=registration_data, 
                              allow_redirects=False,
                              timeout=10)
        
        print(f"Registration response status: {response.status_code}")
        
        # Check if registration was successful (should redirect to login)
        if response.status_code in [302, 303]:  # Redirect to login page
            print(f"✅ Registration successful for {test_email}")
            
            # Verify user was created in database
            conn = sqlite3.connect('startsmart.db')
            c = conn.cursor()
            c.execute("SELECT id, email, name, user_type FROM users WHERE email = ?", (test_email,))
            user = c.fetchone()
            conn.close()
            
            if user:
                print(f"✅ User verified in database: {user[1]} ({user[2]})")
                return True, test_email
            else:
                print("❌ User not found in database after registration")
                return False, None
        else:
            print(f"❌ Registration failed with status: {response.status_code}")
            if response.text:
                print(f"Response content: {response.text[:500]}...")
            return False, None
            
    except Exception as e:
        print(f"❌ Registration test failed: {e}")
        return False, None

def test_user_login(test_email):
    """Test user login functionality"""
    print(f"🔍 Testing login with email: {test_email}")
    test_password = "TestPass123!"
    
    try:
        # Create new session for login test
        session = requests.Session()
        
        # Get login page first
        login_page = session.get('http://localhost:5000/login')
        if login_page.status_code != 200:
            print(f"❌ Could not access login page: {login_page.status_code}")
            return False
        
        # Submit login form
        login_data = {
            'email': test_email,
            'password': test_password
        }
        
        response = session.post('http://localhost:5000/login', 
                              data=login_data, 
                              allow_redirects=False,
                              timeout=10)
        
        print(f"Login response status: {response.status_code}")
        
        # Check if login was successful (should redirect to dashboard)
        if response.status_code in [302, 303]:
            redirect_location = response.headers.get('Location', '')
            if 'dashboard' in redirect_location or redirect_location.endswith('/dashboard'):
                print(f"✅ Login successful for {test_email}")
                
                # Test accessing dashboard
                dashboard_response = session.get('http://localhost:5000/dashboard')
                if dashboard_response.status_code == 200:
                    print("✅ Dashboard accessible after login")
                    return True
                else:
                    print(f"❌ Dashboard not accessible: {dashboard_response.status_code}")
                    return False
            else:
                print(f"❌ Unexpected redirect location: {redirect_location}")
                return False
        else:
            print(f"❌ Login failed with status: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Login test failed: {e}")
        return False

def test_password_hashing():
    """Test password hashing functionality"""
    print("🔍 Testing password hashing...")
    try:
        from werkzeug.security import generate_password_hash, check_password_hash
        
        test_password = "TestPassword123!"
        hashed = generate_password_hash(test_password)
        
        if check_password_hash(hashed, test_password):
            print("✅ Password hashing working correctly")
            return True
        else:
            print("❌ Password hashing verification failed")
            return False
            
    except Exception as e:
        print(f"❌ Password hashing test failed: {e}")
        return False

def run_comprehensive_auth_test():
    """Run all authentication tests"""
    print("=" * 60)
    print("🚀 STARTSMART AUTHENTICATION COMPREHENSIVE TEST")
    print("=" * 60)
    
    test_results = []
    
    # Test 1: Database Connection
    test_results.append(("Database Connection", test_database_connection()))
    
    # Test 2: Server Status
    test_results.append(("Server Status", test_server_status()))
    
    # Test 3: Password Hashing
    test_results.append(("Password Hashing", test_password_hashing()))
    
    # Test 4: Registration Page
    test_results.append(("Registration Page", test_registration_page()))
    
    # Test 5: Login Page
    test_results.append(("Login Page", test_login_page()))
    
    # Test 6: User Registration
    reg_success, test_email = test_user_registration()
    test_results.append(("User Registration", reg_success))
    
    # Test 7: User Login (only if registration succeeded)
    if reg_success and test_email:
        login_success = test_user_login(test_email)
        test_results.append(("User Login", login_success))
    else:
        test_results.append(("User Login", False))
    
    # Print Results Summary
    print("\n" + "=" * 60)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 60)
    
    passed = 0
    total = len(test_results)
    
    for test_name, result in test_results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:<25} {status}")
        if result:
            passed += 1
    
    print("-" * 60)
    print(f"TOTAL: {passed}/{total} tests passed ({(passed/total)*100:.1f}%)")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! Authentication system is working correctly.")
    else:
        print("⚠️  Some tests failed. Please check the issues above.")
        
    return passed == total

if __name__ == "__main__":
    success = run_comprehensive_auth_test()
    exit(0 if success else 1)
