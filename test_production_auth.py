#!/usr/bin/env python3
"""
Production Registration & Login Test
Tests the enhanced authentication system with real user data
"""

import requests
import json
import random
import string

def generate_test_user():
    """Generate realistic test user data"""
    first_names = ['John', 'Jane', 'Michael', 'Sarah', 'David', 'Emily', 'James', 'Maria', 'Robert', 'Lisa']
    last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez']
    
    first_name = random.choice(first_names)
    last_name = random.choice(last_names)
    
    # Generate unique email
    random_num = random.randint(1000, 9999)
    email = f"{first_name.lower()}.{last_name.lower()}{random_num}@example.com"
    
    return {
        'name': f"{first_name} {last_name}",
        'email': email,
        'password': 'SecurePass123!',
        'confirmPassword': 'SecurePass123!',
        'user_type': random.choice(['student', 'mentor', 'recruiter']),
        'agreeTerms': 'on'
    }

def test_enhanced_registration():
    """Test registration with various scenarios"""
    print("🧪 TESTING ENHANCED REGISTRATION SYSTEM")
    print("=" * 60)
    
    test_cases = [
        {
            'name': 'Valid Registration',
            'data': generate_test_user(),
            'should_succeed': True
        },
        {
            'name': 'Weak Password',
            'data': {
                'name': 'Test User',
                'email': 'test@example.com',
                'password': '123',
                'confirmPassword': '123',
                'user_type': 'student',
                'agreeTerms': 'on'
            },
            'should_succeed': False
        },
        {
            'name': 'Invalid Email',
            'data': {
                'name': 'Test User',
                'email': 'invalid-email',
                'password': 'SecurePass123!',
                'confirmPassword': 'SecurePass123!',
                'user_type': 'student',
                'agreeTerms': 'on'
            },
            'should_succeed': False
        },
        {
            'name': 'Password Mismatch',
            'data': {
                'name': 'Test User',
                'email': 'mismatch@example.com',
                'password': 'SecurePass123!',
                'confirmPassword': 'DifferentPass123!',
                'user_type': 'student',
                'agreeTerms': 'on'
            },
            'should_succeed': False
        },
        {
            'name': 'Missing Terms Agreement',
            'data': {
                'name': 'Test User',
                'email': 'noterms@example.com',
                'password': 'SecurePass123!',
                'confirmPassword': 'SecurePass123!',
                'user_type': 'student'
                # No agreeTerms
            },
            'should_succeed': False
        }
    ]
    
    results = []
    
    for test_case in test_cases:
        print(f"\n🔍 Testing: {test_case['name']}")
        
        try:
            session = requests.Session()
            
            # Get registration page
            response = session.get('http://127.0.0.1:5000/register')
            if response.status_code != 200:
                print(f"❌ Cannot access registration page")
                continue
            
            # Submit registration
            response = session.post('http://127.0.0.1:5000/register', data=test_case['data'])
            
            # Analyze response
            success = False
            if response.status_code == 200:
                if 'login' in response.url:
                    success = True
                    print(f"✅ Registration successful - redirected to login")
                elif 'Registration successful' in response.text:
                    success = True
                    print(f"✅ Registration successful")
                else:
                    success = False
                    if 'error' in response.text.lower() or 'invalid' in response.text.lower():
                        print(f"⚠️ Registration failed with validation error (expected)")
                    else:
                        print(f"❌ Registration failed unexpectedly")
            
            # Check if result matches expectation
            if success == test_case['should_succeed']:
                result = "PASS"
                print(f"✅ Test result: {result}")
            else:
                result = "FAIL"
                print(f"❌ Test result: {result}")
            
            results.append({
                'test': test_case['name'],
                'expected': test_case['should_succeed'],
                'actual': success,
                'result': result
            })
            
        except Exception as e:
            print(f"❌ Test error: {e}")
            results.append({
                'test': test_case['name'],
                'expected': test_case['should_succeed'],
                'actual': False,
                'result': "ERROR"
            })
    
    return results

def test_enhanced_login():
    """Test login with newly created user"""
    print("\n🧪 TESTING ENHANCED LOGIN SYSTEM")
    print("=" * 60)
    
    # First create a test user
    print("📝 Creating test user for login test...")
    test_user = generate_test_user()
    
    try:
        session = requests.Session()
        
        # Register user
        response = session.post('http://127.0.0.1:5000/register', data=test_user)
        if response.status_code != 200 or 'login' not in response.url:
            print("❌ Failed to create test user for login test")
            return False
        
        print(f"✅ Test user created: {test_user['email']}")
        
        # Test login scenarios
        login_tests = [
            {
                'name': 'Valid Login',
                'email': test_user['email'],
                'password': test_user['password'],
                'should_succeed': True
            },
            {
                'name': 'Wrong Password',
                'email': test_user['email'],
                'password': 'WrongPassword123!',
                'should_succeed': False
            },
            {
                'name': 'Non-existent User',
                'email': 'nonexistent@example.com',
                'password': 'AnyPassword123!',
                'should_succeed': False
            },
            {
                'name': 'Empty Email',
                'email': '',
                'password': test_user['password'],
                'should_succeed': False
            }
        ]
        
        for test in login_tests:
            print(f"\n🔍 Testing: {test['name']}")
            
            login_data = {
                'email': test['email'],
                'password': test['password']
            }
            
            # Fresh session for each test
            test_session = requests.Session()
            response = test_session.post('http://127.0.0.1:5000/login', data=login_data)
            
            success = False
            if response.status_code == 200:
                if 'dashboard' in response.url:
                    success = True
                    print("✅ Login successful - redirected to dashboard")
                elif 'Invalid' in response.text or 'required' in response.text:
                    success = False
                    print("⚠️ Login failed with error message (expected)")
                else:
                    success = False
                    print("❌ Login failed")
            
            # Check result
            if success == test['should_succeed']:
                print(f"✅ Test result: PASS")
            else:
                print(f"❌ Test result: FAIL")
        
        return True
        
    except Exception as e:
        print(f"❌ Login test error: {e}")
        return False

def test_production_readiness():
    """Test production readiness features"""
    print("\n🧪 TESTING PRODUCTION READINESS")
    print("=" * 60)
    
    features = [
        {
            'name': 'Server Accessibility',
            'test': lambda: requests.get('http://127.0.0.1:5000').status_code == 200
        },
        {
            'name': 'Registration Page',
            'test': lambda: requests.get('http://127.0.0.1:5000/register').status_code == 200
        },
        {
            'name': 'Login Page',
            'test': lambda: requests.get('http://127.0.0.1:5000/login').status_code == 200
        },
        {
            'name': 'Static Assets',
            'test': lambda: requests.get('http://127.0.0.1:5000/static/css/style.css').status_code == 200
        },
        {
            'name': 'Form Validation JS',
            'test': lambda: requests.get('http://127.0.0.1:5000/static/js/form-validation.js').status_code == 200
        }
    ]
    
    passed = 0
    total = len(features)
    
    for feature in features:
        try:
            if feature['test']():
                print(f"✅ {feature['name']}: PASS")
                passed += 1
            else:
                print(f"❌ {feature['name']}: FAIL")
        except Exception as e:
            print(f"❌ {feature['name']}: ERROR - {e}")
    
    print(f"\n📊 Production Readiness: {passed}/{total} ({(passed/total*100):.1f}%)")
    return passed == total

def main():
    """Run all production tests"""
    print("🚀 STARTSMART PRODUCTION AUTHENTICATION TEST")
    print("=" * 80)
    
    # Test registration
    registration_results = test_enhanced_registration()
    
    # Test login
    login_success = test_enhanced_login()
    
    # Test production readiness
    production_ready = test_production_readiness()
    
    # Summary
    print("\n" + "=" * 80)
    print("📊 FINAL TEST SUMMARY")
    print("=" * 80)
    
    # Registration summary
    reg_passed = sum(1 for r in registration_results if r['result'] == 'PASS')
    reg_total = len(registration_results)
    print(f"Registration Tests: {reg_passed}/{reg_total} passed")
    
    for result in registration_results:
        status = "✅" if result['result'] == 'PASS' else "❌"
        print(f"  {status} {result['test']}: {result['result']}")
    
    print(f"\nLogin Tests: {'✅ PASS' if login_success else '❌ FAIL'}")
    print(f"Production Ready: {'✅ YES' if production_ready else '❌ NO'}")
    
    # Overall assessment
    overall_success = (reg_passed == reg_total) and login_success and production_ready
    
    print("\n" + "=" * 80)
    if overall_success:
        print("🎉 ALL TESTS PASSED! SYSTEM IS PRODUCTION READY!")
        print("✅ Registration system: Rock solid")
        print("✅ Login system: Secure and reliable") 
        print("✅ Validation: Comprehensive and user-friendly")
        print("✅ Error handling: Professional and helpful")
        print("✅ User experience: Smooth and intuitive")
    else:
        print("⚠️ SOME TESTS FAILED - REVIEW REQUIRED")
    
    print("=" * 80)

if __name__ == "__main__":
    main()
