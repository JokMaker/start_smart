#!/usr/bin/env python3
"""
Comprehensive Authentication Test for StartSmart Platform
Tests registration, login, and session management
"""

import requests
import sqlite3
from datetime import datetime
import json

class AuthenticationTester:
    def __init__(self, base_url="http://127.0.0.1:5000"):
        self.base_url = base_url
        self.session = requests.Session()
        
    def test_database_structure(self):
        """Test if users table has correct structure"""
        print("🔍 Testing database structure...")
        
        try:
            conn = sqlite3.connect('startsmart.db')
            cursor = conn.cursor()
            
            # Check users table structure
            cursor.execute("PRAGMA table_info(users)")
            columns = cursor.fetchall()
            
            expected_columns = ['id', 'email', 'password', 'name', 'user_type', 'bio', 'skills', 'location', 'created_at']
            actual_columns = [col[1] for col in columns]
            
            print(f"   Expected columns: {expected_columns}")
            print(f"   Actual columns: {actual_columns}")
            
            missing_columns = set(expected_columns) - set(actual_columns)
            if missing_columns:
                print(f"   ❌ Missing columns: {missing_columns}")
                return False
            else:
                print("   ✅ All required columns present")
                
            # Check if table has data
            cursor.execute("SELECT COUNT(*) FROM users")
            user_count = cursor.fetchone()[0]
            print(f"   📊 Current users in database: {user_count}")
            
            conn.close()
            return True
            
        except Exception as e:
            print(f"   ❌ Database error: {e}")
            return False
    
    def test_registration_page_load(self):
        """Test if registration page loads properly"""
        print("\n🔍 Testing registration page load...")
        
        try:
            response = self.session.get(f"{self.base_url}/register")
            
            if response.status_code == 200:
                print("   ✅ Registration page loads successfully")
                
                # Check if form elements are present
                required_fields = ['email', 'password', 'name', 'user_type']
                page_content = response.text.lower()
                
                for field in required_fields:
                    if field in page_content:
                        print(f"   ✅ Form field '{field}' found")
                    else:
                        print(f"   ❌ Form field '{field}' missing")
                        return False
                
                return True
            else:
                print(f"   ❌ Registration page failed to load: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"   ❌ Error loading registration page: {e}")
            return False
    
    def test_login_page_load(self):
        """Test if login page loads properly"""
        print("\n🔍 Testing login page load...")
        
        try:
            response = self.session.get(f"{self.base_url}/login")
            
            if response.status_code == 200:
                print("   ✅ Login page loads successfully")
                
                # Check if form elements are present
                required_fields = ['email', 'password']
                page_content = response.text.lower()
                
                for field in required_fields:
                    if field in page_content:
                        print(f"   ✅ Form field '{field}' found")
                    else:
                        print(f"   ❌ Form field '{field}' missing")
                        return False
                
                return True
            else:
                print(f"   ❌ Login page failed to load: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"   ❌ Error loading login page: {e}")
            return False
    
    def test_user_registration(self):
        """Test actual user registration"""
        print("\n🔍 Testing user registration...")
        
        # Test data
        test_user = {
            'email': f'test_user_{datetime.now().strftime("%Y%m%d_%H%M%S")}@test.com',
            'password': 'TestPassword123!',
            'confirmPassword': 'TestPassword123!',  # Add confirm password
            'name': 'Test User',
            'user_type': 'student',
            'bio': 'Test bio for registration',
            'skills': 'Python, Testing',
            'location': 'Test City'
        }
        
        try:
            # First get the registration page to get any CSRF tokens
            reg_page = self.session.get(f"{self.base_url}/register")
            
            # Submit registration
            response = self.session.post(
                f"{self.base_url}/register",
                data=test_user,
                allow_redirects=False
            )
            
            print(f"   Registration response status: {response.status_code}")
            
            if response.status_code in [200, 302]:  # Success or redirect
                print("   ✅ Registration submitted successfully")
                
                # Check if user was actually created in database
                conn = sqlite3.connect('startsmart.db')
                cursor = conn.cursor()
                cursor.execute("SELECT id, email, name FROM users WHERE email = ?", (test_user['email'],))
                user = cursor.fetchone()
                conn.close()
                
                if user:
                    print(f"   ✅ User created in database: ID {user[0]}, Email: {user[1]}, Name: {user[2]}")
                    self.test_user_email = test_user['email']
                    self.test_user_password = test_user['password']
                    return True
                else:
                    print("   ❌ User not found in database after registration")
                    return False
            else:
                print(f"   ❌ Registration failed with status {response.status_code}")
                print(f"   Response content: {response.text[:200]}...")
                return False
                
        except Exception as e:
            print(f"   ❌ Registration error: {e}")
            return False
    
    def test_user_login(self):
        """Test user login with the registered user"""
        print("\n🔍 Testing user login...")
        
        if not hasattr(self, 'test_user_email'):
            print("   ❌ No test user available for login test")
            return False
        
        try:
            login_data = {
                'email': self.test_user_email,
                'password': self.test_user_password
            }
            
            # Get login page first
            login_page = self.session.get(f"{self.base_url}/login")
            
            # Submit login
            response = self.session.post(
                f"{self.base_url}/login",
                data=login_data,
                allow_redirects=False
            )
            
            print(f"   Login response status: {response.status_code}")
            
            if response.status_code in [200, 302]:  # Success or redirect
                print("   ✅ Login submitted successfully")
                
                # Try to access a protected page (dashboard)
                dashboard_response = self.session.get(f"{self.base_url}/dashboard")
                
                if dashboard_response.status_code == 200:
                    print("   ✅ Successfully accessed dashboard after login")
                    return True
                else:
                    print(f"   ❌ Cannot access dashboard after login: {dashboard_response.status_code}")
                    return False
            else:
                print(f"   ❌ Login failed with status {response.status_code}")
                print(f"   Response content: {response.text[:200]}...")
                return False
                
        except Exception as e:
            print(f"   ❌ Login error: {e}")
            return False
    
    def test_existing_user_login(self):
        """Test login with existing users from sample data"""
        print("\n🔍 Testing login with existing users...")
        
        try:
            # Get existing users from database
            conn = sqlite3.connect('startsmart.db')
            cursor = conn.cursor()
            cursor.execute("SELECT email, name FROM users LIMIT 3")
            existing_users = cursor.fetchall()
            conn.close()
            
            if not existing_users:
                print("   ❌ No existing users found in database")
                return False
            
            print(f"   Found {len(existing_users)} existing users:")
            for user in existing_users:
                print(f"     - {user[1]} ({user[0]})")
            
            # Try to login with a known password (from sample data)
            test_email = existing_users[0][0]  # First user's email
            test_passwords = ['password123', 'Password123!', 'demo123']  # Common sample passwords
            
            for password in test_passwords:
                login_data = {
                    'email': test_email,
                    'password': password
                }
                
                response = self.session.post(
                    f"{self.base_url}/login",
                    data=login_data,
                    allow_redirects=False
                )
                
                if response.status_code in [200, 302]:
                    print(f"   ✅ Successfully logged in with {test_email} using password '{password}'")
                    return True
            
            print(f"   ❌ Could not login with any common passwords for {test_email}")
            return False
            
        except Exception as e:
            print(f"   ❌ Existing user login error: {e}")
            return False
    
    def run_comprehensive_test(self):
        """Run all authentication tests"""
        print("🚀 StartSmart Authentication Test Suite")
        print("=" * 60)
        print(f"Testing URL: {self.base_url}")
        print(f"Test started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        tests = [
            ("Database Structure", self.test_database_structure),
            ("Registration Page Load", self.test_registration_page_load),
            ("Login Page Load", self.test_login_page_load),
            ("User Registration", self.test_user_registration),
            ("User Login", self.test_user_login),
            ("Existing User Login", self.test_existing_user_login)
        ]
        
        results = {}
        
        for test_name, test_func in tests:
            try:
                results[test_name] = test_func()
            except Exception as e:
                print(f"   ❌ Test '{test_name}' crashed: {e}")
                results[test_name] = False
        
        print("\n" + "=" * 60)
        print("📊 TEST RESULTS SUMMARY")
        print("=" * 60)
        
        passed = 0
        total = len(tests)
        
        for test_name, result in results.items():
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"{status} - {test_name}")
            if result:
                passed += 1
        
        print(f"\nOverall: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
        
        if passed == total:
            print("\n🎉 ALL TESTS PASSED! Registration and login are working correctly.")
        else:
            print(f"\n⚠️  {total-passed} test(s) failed. Authentication needs attention.")
        
        return passed == total

def main():
    tester = AuthenticationTester()
    success = tester.run_comprehensive_test()
    return 0 if success else 1

if __name__ == "__main__":
    exit(main())
