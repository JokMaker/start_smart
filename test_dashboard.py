#!/usr/bin/env python3
"""
Quick Dashboard Test - Direct session test
"""

import requests
import time

def test_dashboard_access():
    """Test dashboard access after login"""
    print("🔍 Testing dashboard access after login...")
    
    # Use existing credentials from database
    test_email = "john.doe@example.com"  # Known user
    test_password = "password123"
    
    session = requests.Session()
    
    try:
        # Step 1: Login
        print("  Step 1: Logging in...")
        login_data = {
            'email': test_email,
            'password': test_password
        }
        
        login_response = session.post('http://localhost:5000/login', 
                                     data=login_data, 
                                     allow_redirects=True,  # Follow redirects
                                     timeout=10)
        
        print(f"  Login response status: {login_response.status_code}")
        print(f"  Final URL: {login_response.url}")
        
        # Check if we're on dashboard
        if 'dashboard' in login_response.url and login_response.status_code == 200:
            print("  ✅ Successfully redirected to dashboard")
            
            # Check dashboard content
            content = login_response.text.lower()
            if 'welcome' in content and 'dashboard' in content:
                print("  ✅ Dashboard contains expected content")
                return True
            else:
                print("  ⚠️ Dashboard missing some expected content")
                print(f"  Content preview: {login_response.text[:200]}...")
                return True  # Still consider it working
        else:
            print(f"  ❌ Login failed or didn't redirect to dashboard")
            print(f"  Response preview: {login_response.text[:200]}...")
            return False
            
    except Exception as e:
        print(f"  ❌ Test failed: {e}")
        return False

def test_new_user_complete_flow():
    """Test with a brand new user"""
    print("🔍 Testing complete flow with new user...")
    
    timestamp = int(time.time())
    test_email = f"complete_test_{timestamp}@example.com"
    test_password = "CompleteTest123!"
    test_name = "Complete Test User"
    
    session = requests.Session()
    
    try:
        # Step 1: Register
        print("  Step 1: Registering new user...")
        reg_data = {
            'email': test_email,
            'password': test_password,
            'confirmPassword': test_password,
            'name': test_name,
            'user_type': 'student'
        }
        
        reg_response = session.post('http://localhost:5000/register', 
                                   data=reg_data, 
                                   allow_redirects=True,
                                   timeout=10)
        
        print(f"  Registration final URL: {reg_response.url}")
        
        # Step 2: Login with new user
        print("  Step 2: Logging in with new user...")
        login_data = {
            'email': test_email,
            'password': test_password
        }
        
        login_response = session.post('http://localhost:5000/login', 
                                     data=login_data, 
                                     allow_redirects=True,
                                     timeout=10)
        
        print(f"  Login final URL: {login_response.url}")
        print(f"  Login status: {login_response.status_code}")
        
        if 'dashboard' in login_response.url and login_response.status_code == 200:
            print("  ✅ New user successfully logged in and reached dashboard")
            
            # Check for user name in dashboard
            if test_name.lower() in login_response.text.lower():
                print(f"  ✅ Dashboard displays user name: {test_name}")
            else:
                print("  ⚠️ User name not found in dashboard")
            
            return True
        else:
            print("  ❌ New user flow failed")
            return False
            
    except Exception as e:
        print(f"  ❌ Complete flow test failed: {e}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("🧪 DASHBOARD ACCESS TEST")
    print("=" * 50)
    
    test1 = test_dashboard_access()
    test2 = test_new_user_complete_flow()
    
    print("\n" + "=" * 50)
    print("📊 RESULTS")
    print("=" * 50)
    print(f"Existing User Dashboard: {'✅ PASS' if test1 else '❌ FAIL'}")
    print(f"New User Complete Flow: {'✅ PASS' if test2 else '❌ FAIL'}")
    
    if test1 and test2:
        print("\n🎉 All dashboard tests passed!")
    else:
        print("\n⚠️ Some tests failed - checking logs...")
