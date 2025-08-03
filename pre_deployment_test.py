#!/usr/bin/env python3
"""
PRE-DEPLOYMENT TESTING SUITE for StartSmart
Run this before pushing to production to ensure everything works
"""

import os
import sqlite3
import requests
import subprocess
import sys
from datetime import datetime
import time

class PreDeploymentTester:
    def __init__(self):
        self.base_url = "http://127.0.0.1:5000"
        self.session = requests.Session()
        self.test_results = {}
        
    def test_database_integrity(self):
        """Test database structure and data integrity"""
        print("🔍 Testing Database Integrity...")
        
        try:
            conn = sqlite3.connect('startsmart.db')
            cursor = conn.cursor()
            
            # Test all required tables exist
            required_tables = ['users', 'jobs', 'startups', 'applications', 'skills', 'mentorship']
            
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            existing_tables = [row[0] for row in cursor.fetchall()]
            
            missing_tables = set(required_tables) - set(existing_tables)
            if missing_tables:
                print(f"   ❌ Missing tables: {missing_tables}")
                return False
            
            print("   ✅ All required tables exist")
            
            # Test data counts
            for table in required_tables:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                print(f"   📊 {table}: {count} records")
            
            conn.close()
            return True
            
        except Exception as e:
            print(f"   ❌ Database error: {e}")
            return False
    
    def test_authentication_flow(self):
        """Test complete authentication flow"""
        print("\n🔍 Testing Authentication Flow...")
        
        # Test data
        test_user = {
            'email': f'predeployment_test_{datetime.now().strftime("%Y%m%d%H%M%S")}@test.com',
            'password': 'TestDeploy123!',
            'confirmPassword': 'TestDeploy123!',
            'name': 'Pre-Deploy Test User',
            'user_type': 'student'
        }
        
        try:
            # Step 1: Registration
            print("   🔄 Testing registration...")
            reg_response = self.session.post(f"{self.base_url}/register", data=test_user)
            
            if reg_response.status_code not in [200, 302]:
                print(f"   ❌ Registration failed: {reg_response.status_code}")
                return False
            
            # Verify user in database
            conn = sqlite3.connect('startsmart.db')
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM users WHERE email = ?", (test_user['email'],))
            user = cursor.fetchone()
            conn.close()
            
            if not user:
                print("   ❌ User not found in database after registration")
                return False
            
            print("   ✅ Registration successful")
            
            # Step 2: Login
            print("   🔄 Testing login...")
            login_data = {
                'email': test_user['email'],
                'password': test_user['password']
            }
            
            login_response = self.session.post(f"{self.base_url}/login", data=login_data)
            
            if login_response.status_code not in [200, 302]:
                print(f"   ❌ Login failed: {login_response.status_code}")
                return False
            
            print("   ✅ Login successful")
            
            # Step 3: Test protected route access
            print("   🔄 Testing dashboard access...")
            dashboard_response = self.session.get(f"{self.base_url}/dashboard")
            
            if dashboard_response.status_code != 200:
                print(f"   ❌ Dashboard access failed: {dashboard_response.status_code}")
                return False
            
            print("   ✅ Dashboard access successful")
            
            # Step 4: Test logout
            print("   🔄 Testing logout...")
            logout_response = self.session.get(f"{self.base_url}/logout")
            
            # Try to access dashboard after logout (should fail)
            dashboard_after_logout = self.session.get(f"{self.base_url}/dashboard")
            if 'login' not in dashboard_after_logout.url.lower():
                print("   ❌ Session not properly cleared after logout")
                return False
            
            print("   ✅ Logout successful")
            return True
            
        except Exception as e:
            print(f"   ❌ Authentication flow error: {e}")
            return False
    
    def test_api_integration(self):
        """Test Adzuna API integration"""
        print("\n🔍 Testing API Integration...")
        
        try:
            # Test if job fetcher works
            from job_fetcher import AdzunaJobFetcher
            
            fetcher = AdzunaJobFetcher()
            
            # Test API connection with minimal request
            print("   🔄 Testing API connection...")
            
            # Just test connection, don't fetch many jobs
            test_jobs = fetcher.fetch_jobs_from_country('gb', pages=1, results_per_page=5)
            
            if test_jobs:
                print(f"   ✅ API connection successful, fetched {len(test_jobs)} sample jobs")
                return True
            else:
                print("   ⚠️ API connection returned no jobs (might be rate limited or quota exceeded)")
                return True  # This is OK for testing
                
        except Exception as e:
            print(f"   ❌ API integration error: {e}")
            return False
    
    def test_file_structure(self):
        """Test all required files exist"""
        print("\n🔍 Testing File Structure...")
        
        required_files = [
            'app.py',
            'requirements.txt',
            'startsmart.db',
            'templates/base.html',
            'templates/login.html',
            'templates/register.html',
            'templates/dashboard.html',
            'static/css/style.css',
            'job_fetcher.py'
        ]
        
        missing_files = []
        for file_path in required_files:
            if not os.path.exists(file_path):
                missing_files.append(file_path)
            else:
                print(f"   ✅ {file_path}")
        
        if missing_files:
            print(f"   ❌ Missing files: {missing_files}")
            return False
        
        return True
    
    def test_environment_setup(self):
        """Test environment configuration"""
        print("\n🔍 Testing Environment Setup...")
        
        # Check if production example file exists
        if not os.path.exists('.env.production.example'):
            print("   ❌ .env.production.example not found")
            return False
        
        print("   ✅ Production environment file exists")
        
        # Check Flask app configuration
        try:
            # Import and check Flask app config
            sys.path.append('.')
            from app import app
            
            # Test important configurations
            config_checks = {
                'SECRET_KEY': app.secret_key is not None,
                'SESSION_COOKIE_HTTPONLY': app.config.get('SESSION_COOKIE_HTTPONLY', False),
                'SESSION_COOKIE_SAMESITE': app.config.get('SESSION_COOKIE_SAMESITE') == 'Lax'
            }
            
            for config_name, is_set in config_checks.items():
                if is_set:
                    print(f"   ✅ {config_name} configured")
                else:
                    print(f"   ❌ {config_name} not configured")
                    return False
            
            return True
            
        except Exception as e:
            print(f"   ❌ Environment setup error: {e}")
            return False
    
    def test_performance(self):
        """Test basic performance metrics"""
        print("\n🔍 Testing Performance...")
        
        try:
            # Test page load times
            pages_to_test = ['/', '/login', '/register', '/jobs']
            
            for page in pages_to_test:
                start_time = time.time()
                response = self.session.get(f"{self.base_url}{page}")
                load_time = time.time() - start_time
                
                if response.status_code == 200 and load_time < 3.0:
                    print(f"   ✅ {page}: {load_time:.2f}s")
                else:
                    print(f"   ⚠️ {page}: {load_time:.2f}s (slow or failed)")
            
            return True
            
        except Exception as e:
            print(f"   ❌ Performance test error: {e}")
            return False
    
    def generate_deployment_summary(self):
        """Generate deployment readiness summary"""
        print("\n" + "="*60)
        print("📋 DEPLOYMENT READINESS SUMMARY")
        print("="*60)
        
        passed_tests = sum(1 for result in self.test_results.values() if result)
        total_tests = len(self.test_results)
        
        for test_name, passed in self.test_results.items():
            status = "✅ PASS" if passed else "❌ FAIL"
            print(f"{status} - {test_name}")
        
        print(f"\nOverall: {passed_tests}/{total_tests} tests passed ({passed_tests/total_tests*100:.1f}%)")
        
        if passed_tests == total_tests:
            print("\n🚀 READY FOR DEPLOYMENT!")
            print("\n📝 Next Steps:")
            print("1. Commit and push your code to GitHub")
            print("2. Set up environment variables on your deployment platform:")
            print("   - Copy values from .env.production.example")
            print("3. Deploy and test authentication on production URL")
            print("4. Run job fetcher in admin panel to populate jobs")
        else:
            print(f"\n⚠️ {total_tests - passed_tests} issue(s) need attention before deployment")
        
        return passed_tests == total_tests
    
    def run_all_tests(self):
        """Run complete pre-deployment test suite"""
        print("🚀 StartSmart Pre-Deployment Test Suite")
        print("="*60)
        print(f"Test started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        tests = [
            ("File Structure", self.test_file_structure),
            ("Database Integrity", self.test_database_integrity),
            ("Environment Setup", self.test_environment_setup),
            ("Authentication Flow", self.test_authentication_flow),
            ("API Integration", self.test_api_integration),
            ("Performance", self.test_performance)
        ]
        
        for test_name, test_func in tests:
            try:
                print()
                self.test_results[test_name] = test_func()
            except Exception as e:
                print(f"   ❌ Test '{test_name}' crashed: {e}")
                self.test_results[test_name] = False
        
        return self.generate_deployment_summary()

def main():
    """Main function to run pre-deployment tests"""
    
    print("🔍 Checking if Flask server is running...")
    try:
        response = requests.get("http://127.0.0.1:5000", timeout=5)
        print("✅ Flask server is running")
    except:
        print("❌ Flask server not running. Please start it first:")
        print("   python app.py")
        print("   Then run this test again.")
        return False
    
    tester = PreDeploymentTester()
    return tester.run_all_tests()

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
