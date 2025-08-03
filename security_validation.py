#!/usr/bin/env python3
"""
Security and Edge Case Validation for Authentication System
"""

import sqlite3
import requests
import time

def test_sql_injection_protection():
    """Test SQL injection protection in login/registration"""
    print("🔍 Testing SQL injection protection...")
    
    session = requests.Session()
    
    # Test SQL injection in login
    sql_injection_payloads = [
        "admin@test.com'; DROP TABLE users; --",
        "admin@test.com' OR '1'='1",
        "admin@test.com' UNION SELECT * FROM users --"
    ]
    
    for payload in sql_injection_payloads:
        try:
            response = session.post('http://localhost:5000/login', 
                                  data={'email': payload, 'password': 'test'}, 
                                  timeout=5)
            # Should not crash and should return error
            if response.status_code == 200 and 'invalid' in response.text.lower():
                continue
            elif response.status_code in [302, 303]:
                print(f"⚠️ Potential SQL injection vulnerability with payload: {payload}")
                return False
        except Exception as e:
            print(f"❌ SQL injection test failed: {e}")
            return False
    
    print("✅ SQL injection protection working")
    return True

def test_duplicate_registration():
    """Test duplicate email registration prevention"""
    print("🔍 Testing duplicate registration prevention...")
    
    # Get an existing user email from database
    conn = sqlite3.connect('startsmart.db')
    c = conn.cursor()
    c.execute("SELECT email FROM users LIMIT 1")
    existing_user = c.fetchone()
    conn.close()
    
    if not existing_user:
        print("⚠️ No existing users to test with")
        return True
    
    existing_email = existing_user[0]
    
    session = requests.Session()
    
    # Try to register with existing email
    duplicate_data = {
        'email': existing_email,
        'password': 'NewPassword123!',
        'confirmPassword': 'NewPassword123!',
        'name': 'Duplicate User',
        'user_type': 'student'
    }
    
    try:
        response = session.post('http://localhost:5000/register', 
                              data=duplicate_data, 
                              timeout=5)
        
        # Should stay on registration page with error
        if response.status_code == 200 and 'already exists' in response.text.lower():
            print("✅ Duplicate registration properly prevented")
            return True
        else:
            print("❌ Duplicate registration not properly handled")
            return False
            
    except Exception as e:
        print(f"❌ Duplicate registration test failed: {e}")
        return False

def test_password_validation():
    """Test password validation rules"""
    print("🔍 Testing password validation...")
    
    session = requests.Session()
    
    # Test weak passwords
    weak_passwords = [
        "",  # Empty password
        "12",  # Too short
        "ab"   # Too short
    ]
    
    for weak_pass in weak_passwords:
        test_data = {
            'email': f'test_weak_{int(time.time())}@example.com',
            'password': weak_pass,
            'confirmPassword': weak_pass,
            'name': 'Test User',
            'user_type': 'student'
        }
        
        try:
            response = session.post('http://localhost:5000/register', 
                                  data=test_data, 
                                  timeout=5)
            
            # Should stay on registration page with error for weak passwords
            if response.status_code == 200:
                continue  # Good, registration rejected
            elif response.status_code in [302, 303]:
                print(f"⚠️ Weak password accepted: '{weak_pass}'")
                return False
                
        except Exception as e:
            print(f"❌ Password validation test failed: {e}")
            return False
    
    print("✅ Password validation working")
    return True

def test_session_security():
    """Test session security"""
    print("🔍 Testing session security...")
    
    session = requests.Session()
    
    # Try to access dashboard without login
    try:
        response = session.get('http://localhost:5000/dashboard', 
                             allow_redirects=False, 
                             timeout=5)
        
        # Should redirect to login
        if response.status_code in [302, 303]:
            redirect_location = response.headers.get('Location', '')
            if 'login' in redirect_location:
                print("✅ Dashboard properly protected")
                return True
            else:
                print(f"❌ Unexpected redirect: {redirect_location}")
                return False
        else:
            print("❌ Dashboard not properly protected")
            return False
            
    except Exception as e:
        print(f"❌ Session security test failed: {e}")
        return False

def test_user_input_sanitization():
    """Test user input sanitization"""
    print("🔍 Testing input sanitization...")
    
    session = requests.Session()
    
    # Test XSS in name field
    xss_payload = "<script>alert('xss')</script>"
    
    test_data = {
        'email': f'test_xss_{int(time.time())}@example.com',
        'password': 'TestPass123!',
        'confirmPassword': 'TestPass123!',
        'name': xss_payload,
        'user_type': 'student'
    }
    
    try:
        response = session.post('http://localhost:5000/register', 
                              data=test_data, 
                              timeout=5)
        
        # Check if user was created with sanitized name
        if response.status_code in [302, 303]:
            # Check database
            conn = sqlite3.connect('startsmart.db')
            c = conn.cursor()
            c.execute("SELECT name FROM users WHERE email = ?", (test_data['email'],))
            user = c.fetchone()
            conn.close()
            
            if user and '<script>' not in user[0]:
                print("✅ Input sanitization working")
                return True
            else:
                print("⚠️ Potential XSS vulnerability")
                return False
        else:
            # Registration rejected, which is also acceptable
            print("✅ Input sanitization working (registration rejected)")
            return True
            
    except Exception as e:
        print(f"❌ Input sanitization test failed: {e}")
        return False

def run_security_validation():
    """Run all security validation tests"""
    print("=" * 60)
    print("🔒 SECURITY & EDGE CASE VALIDATION")
    print("=" * 60)
    
    tests = [
        ("SQL Injection Protection", test_sql_injection_protection),
        ("Duplicate Registration Prevention", test_duplicate_registration),
        ("Password Validation", test_password_validation),
        ("Session Security", test_session_security),
        ("Input Sanitization", test_user_input_sanitization)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results.append((test_name, False))
    
    # Print Results
    print("\n" + "=" * 60)
    print("🛡️ SECURITY TEST RESULTS")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:<35} {status}")
        if result:
            passed += 1
    
    print("-" * 60)
    print(f"TOTAL: {passed}/{total} security tests passed ({(passed/total)*100:.1f}%)")
    
    return passed == total

if __name__ == "__main__":
    success = run_security_validation()
    exit(0 if success else 1)
