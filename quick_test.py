#!/usr/bin/env python3
"""
Quick Test Script for StartSmart Application
Tests all critical functionality before deployment
"""

import requests
import sqlite3
import os
import sys
from datetime import datetime

def test_database():
    """Test database connectivity and structure"""
    print("🔍 Testing Database...")
    try:
        conn = sqlite3.connect('startsmart.db')
        c = conn.cursor()
        
        # Check all required tables exist
        required_tables = ['users', 'jobs', 'startups', 'applications', 'mentorship', 'notifications', 'resources']
        c.execute("SELECT name FROM sqlite_master WHERE type='table';")
        existing_tables = [table[0] for table in c.fetchall()]
        
        missing_tables = [table for table in required_tables if table not in existing_tables]
        if missing_tables:
            print(f"❌ Missing tables: {missing_tables}")
            return False
        
        # Check user count
        c.execute("SELECT COUNT(*) FROM users")
        user_count = c.fetchone()[0]
        print(f"✅ Database OK - {user_count} users, {len(existing_tables)} tables")
        
        conn.close()
        return True
    except Exception as e:
        print(f"❌ Database Error: {e}")
        return False

def test_server():
    """Test if the Flask server is responding"""
    print("🔍 Testing Server Response...")
    try:
        response = requests.get('http://127.0.0.1:5000', timeout=5)
        if response.status_code == 200:
            print("✅ Server responding correctly")
            return True
        else:
            print(f"❌ Server returned status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Server not running or not accessible")
        return False
    except Exception as e:
        print(f"❌ Server test error: {e}")
        return False

def test_critical_routes():
    """Test critical application routes"""
    print("🔍 Testing Critical Routes...")
    base_url = 'http://127.0.0.1:5000'
    routes_to_test = [
        '/',           # Home page
        '/login',      # Login page
        '/register',   # Register page
        '/jobs',       # Jobs page
        '/startups',   # Startups page
        '/mentorship', # Mentorship page
        '/resources'   # Resources page
    ]
    
    failed_routes = []
    for route in routes_to_test:
        try:
            response = requests.get(f'{base_url}{route}', timeout=5)
            if response.status_code == 200:
                print(f"✅ {route} - OK")
            else:
                print(f"❌ {route} - Status: {response.status_code}")
                failed_routes.append(route)
        except Exception as e:
            print(f"❌ {route} - Error: {e}")
            failed_routes.append(route)
    
    if failed_routes:
        print(f"❌ Failed routes: {failed_routes}")
        return False
    else:
        print("✅ All routes working correctly")
        return True

def check_static_files():
    """Check if static files exist"""
    print("🔍 Checking Static Files...")
    required_files = [
        'static/css/style.css',
        'static/css/components.css',
        'static/js/animations.js',
        'static/js/search.js',
        'static/js/job-listing.js',
        'static/js/job-posting.js',
        'static/images/hero-illustration.svg'
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
            print(f"❌ Missing: {file_path}")
        else:
            print(f"✅ Found: {file_path}")
    
    if missing_files:
        print(f"❌ Missing {len(missing_files)} static files")
        return False
    else:
        print("✅ All static files present")
        return True

def check_templates():
    """Check if template files exist"""
    print("🔍 Checking Template Files...")
    required_templates = [
        'templates/base.html',
        'templates/index.html',
        'templates/login.html',
        'templates/register.html',
        'templates/dashboard.html',
        'templates/jobs.html',
        'templates/startups.html',
        'templates/mentorship.html',
        'templates/profile.html'
    ]
    
    missing_templates = []
    for template_path in required_templates:
        if not os.path.exists(template_path):
            missing_templates.append(template_path)
            print(f"❌ Missing: {template_path}")
        else:
            # Check if template is not empty
            with open(template_path, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                if len(content) < 50:  # Very basic check
                    print(f"⚠️ Template might be empty: {template_path}")
                    missing_templates.append(template_path)
                else:
                    print(f"✅ Found: {template_path}")
    
    if missing_templates:
        print(f"❌ Missing or empty templates: {missing_templates}")
        return False
    else:
        print("✅ All templates present and not empty")
        return True

def test_registration_form():
    """Test registration functionality"""
    print("🔍 Testing Registration Form...")
    try:
        # Test registration page loads
        response = requests.get('http://127.0.0.1:5000/register', timeout=5)
        if response.status_code != 200:
            print(f"❌ Registration page not loading: {response.status_code}")
            return False
        
        # Check if form fields are present
        if 'name' in response.text and 'email' in response.text and 'password' in response.text:
            print("✅ Registration form fields present")
        else:
            print("❌ Registration form missing required fields")
            return False
        
        print("✅ Registration form working")
        return True
    except Exception as e:
        print(f"❌ Registration test error: {e}")
        return False

def test_login_form():
    """Test login functionality"""
    print("🔍 Testing Login Form...")
    try:
        # Test login page loads
        response = requests.get('http://127.0.0.1:5000/login', timeout=5)
        if response.status_code != 200:
            print(f"❌ Login page not loading: {response.status_code}")
            return False
        
        # Check if form fields are present
        if 'email' in response.text and 'password' in response.text:
            print("✅ Login form fields present")
        else:
            print("❌ Login form missing required fields")
            return False
        
        print("✅ Login form working")
        return True
    except Exception as e:
        print(f"❌ Login test error: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 50)
    print("🚀 STARTSMART APPLICATION QUICK TEST")
    print("=" * 50)
    print(f"Test started at: {datetime.now()}")
    print()
    
    tests = [
        ("Database", test_database),
        ("Server", test_server),
        ("Templates", check_templates),
        ("Static Files", check_static_files),
        ("Critical Routes", test_critical_routes),
        ("Registration Form", test_registration_form),
        ("Login Form", test_login_form),
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        print(f"\n--- {test_name} Test ---")
        try:
            if test_func():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            failed += 1
    
    print("\n" + "=" * 50)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 50)
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"📈 Success Rate: {(passed/(passed+failed)*100):.1f}%")
    
    if failed == 0:
        print("🎉 ALL TESTS PASSED! Your application is ready for deployment!")
    else:
        print("⚠️ SOME TESTS FAILED! Please fix the issues above before deployment.")
        sys.exit(1)
    
    print(f"\nTest completed at: {datetime.now()}")

if __name__ == "__main__":
    main()
