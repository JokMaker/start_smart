"""
Test authentication on deployed Render app
Focus ONLY on registration and login issues
"""
import requests
import time

def test_registration_step_by_step():
    """Test registration process step by step"""
    
    print("🧪 TESTING REGISTRATION ON RENDER...")
    print("=" * 50)
    
    base_url = "https://start-smart.onrender.com"
    
    # Test data for registration
    test_user = {
        'name': 'Video Test User',
        'email': 'videotest2025@gmail.com', 
        'password': 'VideoTest123!',
        'confirmPassword': 'VideoTest123!',
        'user_type': 'student'
    }
    
    session = requests.Session()
    
    try:
        # Step 1: Check if site is accessible
        print("📍 Step 1: Checking site accessibility...")
        response = session.get(base_url, timeout=30)
        print(f"   Status: {response.status_code}")
        if response.status_code != 200:
            print(f"❌ Site not accessible: {response.status_code}")
            return False
        print("✅ Site is accessible")
        
        # Step 2: Get registration page
        print("\n📍 Step 2: Loading registration page...")
        reg_page = session.get(f"{base_url}/register", timeout=30)
        print(f"   Status: {reg_page.status_code}")
        if reg_page.status_code != 200:
            print(f"❌ Registration page failed: {reg_page.status_code}")
            return False
        print("✅ Registration page loaded")
        
        # Step 3: Submit registration
        print("\n📍 Step 3: Submitting registration...")
        print(f"   Email: {test_user['email']}")
        print(f"   Name: {test_user['name']}")
        
        reg_response = session.post(
            f"{base_url}/register",
            data=test_user,
            timeout=30,
            allow_redirects=False
        )
        
        print(f"   Response Status: {reg_response.status_code}")
        print(f"   Response Headers: {dict(reg_response.headers)}")
        
        # Check response
        if reg_response.status_code == 302:
            redirect = reg_response.headers.get('Location', '')
            print(f"✅ Registration redirected to: {redirect}")
            if 'login' in redirect:
                print("✅ SUCCESS: Registration worked, redirected to login!")
                return True
            else:
                print(f"⚠️ Unexpected redirect: {redirect}")
        elif reg_response.status_code == 200:
            # Check response content for errors
            content = reg_response.text.lower()
            if 'error' in content:
                print("❌ Registration returned with errors in response")
                # Try to find specific error
                if 'email already exists' in content:
                    print("   → Email already exists")
                elif 'validation' in content:
                    print("   → Validation error")
                return False
            else:
                print("⚠️ Registration returned 200 but no clear success indicator")
        else:
            print(f"❌ Registration failed: {reg_response.status_code}")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ Request timed out - app may be sleeping")
        return False
    except Exception as e:
        print(f"❌ Error during registration test: {e}")
        return False

def test_login_step_by_step():
    """Test login with existing user"""
    
    print("\n🔑 TESTING LOGIN ON RENDER...")
    print("=" * 50)
    
    base_url = "https://start-smart.onrender.com"
    
    # Try with demo user we created
    login_data = {
        'email': 'student@demo.com',
        'password': 'Demo123!'
    }
    
    session = requests.Session()
    
    try:
        print("📍 Step 1: Getting login page...")
        login_page = session.get(f"{base_url}/login", timeout=30)
        print(f"   Status: {login_page.status_code}")
        
        if login_page.status_code != 200:
            print(f"❌ Login page failed: {login_page.status_code}")
            return False
        print("✅ Login page loaded")
        
        print("\n📍 Step 2: Submitting login...")
        print(f"   Email: {login_data['email']}")
        
        login_response = session.post(
            f"{base_url}/login",
            data=login_data,
            timeout=30,
            allow_redirects=False
        )
        
        print(f"   Response Status: {login_response.status_code}")
        
        if login_response.status_code == 302:
            redirect = login_response.headers.get('Location', '')
            print(f"✅ Login redirected to: {redirect}")
            if 'dashboard' in redirect:
                print("✅ SUCCESS: Login worked!")
                return True
            else:
                print(f"⚠️ Unexpected redirect: {redirect}")
        elif login_response.status_code == 200:
            content = login_response.text.lower()
            if 'error' in content or 'invalid' in content:
                print("❌ Login failed - invalid credentials or error")
                return False
            else:
                print("⚠️ Login returned 200 but no clear result")
        else:
            print(f"❌ Login failed: {login_response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error during login test: {e}")
        return False

if __name__ == "__main__":
    print("🚀 AUTHENTICATION TESTING STARTED")
    print("Testing deployed app at: https://start-smart.onrender.com")
    print("\n")
    
    # Test registration
    reg_success = test_registration_step_by_step()
    
    # Test login
    login_success = test_login_step_by_step()
    
    print("\n" + "=" * 50)
    print("📊 FINAL RESULTS:")
    print(f"Registration: {'✅ WORKING' if reg_success else '❌ FAILED'}")
    print(f"Login: {'✅ WORKING' if login_success else '❌ FAILED'}")
    
    if reg_success and login_success:
        print("\n🎉 AUTH SYSTEM IS WORKING! Ready for video!")
    else:
        print("\n🔧 AUTH ISSUES FOUND - Need to fix before video")
