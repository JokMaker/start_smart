#!/usr/bin/env python3
"""
Deployment Checklist for StartSmart Application
This script checks if the application is ready for deployment to Render.
"""

import os
import sqlite3
import sys
from datetime import datetime

def check_requirements():
    """Check if requirements.txt exists and has necessary packages"""
    print("📋 Checking requirements.txt...")
    
    if not os.path.exists('requirements.txt'):
        print("❌ requirements.txt not found!")
        return False
    
    with open('requirements.txt', 'r') as f:
        requirements = f.read()
    
    required_packages = ['Flask', 'werkzeug', 'gunicorn']
    missing = []
    
    for package in required_packages:
        if package.lower() not in requirements.lower():
            missing.append(package)
    
    if missing:
        print(f"❌ Missing required packages: {', '.join(missing)}")
        return False
    
    print("✅ requirements.txt looks good")
    return True

def check_database():
    """Check database file and structure"""
    print("\n🗄️ Checking database...")
    
    if not os.path.exists('startsmart.db'):
        print("❌ startsmart.db not found!")
        return False
    
    try:
        conn = sqlite3.connect('startsmart.db')
        c = conn.cursor()
        
        # Check if users table exists
        c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
        if not c.fetchone():
            print("❌ Users table not found!")
            return False
        
        # Check if users exist
        c.execute("SELECT COUNT(*) FROM users")
        user_count = c.fetchone()[0]
        
        print(f"✅ Database exists with {user_count} users")
        
        # Check table structure
        c.execute("PRAGMA table_info(users)")
        columns = [row[1] for row in c.fetchall()]
        
        required_columns = ['id', 'name', 'email', 'password', 'user_type']
        missing_cols = [col for col in required_columns if col not in columns]
        
        if missing_cols:
            print(f"❌ Missing columns in users table: {', '.join(missing_cols)}")
            return False
        
        print("✅ Database structure is correct")
        conn.close()
        return True
        
    except sqlite3.Error as e:
        print(f"❌ Database error: {e}")
        return False

def check_secret_key():
    """Check if SECRET_KEY is properly configured"""
    print("\n🔐 Checking SECRET_KEY configuration...")
    
    # Read app.py to check SECRET_KEY configuration
    try:
        with open('app.py', 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        # Try with different encoding
        with open('app.py', 'r', encoding='latin-1') as f:
            content = f.read()
    
    if ("app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY'" in content or
        "app.secret_key = os.environ.get('SECRET_KEY')" in content):
        print("✅ SECRET_KEY is configured to use environment variable")
        return True
    elif ("app.config['SECRET_KEY'] = 'development-key-change-in-production'" in content or
          "dev-secret-key-change-in-production" in content):
        print("⚠️ Using development SECRET_KEY - should be changed for production")
        return True
    else:
        print("❌ SECRET_KEY configuration not found or incorrect")
        return False

def check_app_structure():
    """Check if all necessary files exist"""
    print("\n📁 Checking application structure...")
    
    required_files = [
        'app.py',
        'requirements.txt',
        'templates/login.html',
        'templates/register.html',
        'templates/dashboard.html',
        'static/css/style.css'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Missing files: {', '.join(missing_files)}")
        return False
    
    print("✅ All required files present")
    return True

def check_gunicorn_config():
    """Check if the app can be run with gunicorn"""
    print("\n🚀 Checking Gunicorn compatibility...")
    
    # Check if app.py has the right structure for gunicorn
    try:
        with open('app.py', 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        with open('app.py', 'r', encoding='latin-1') as f:
            content = f.read()
    
    if "if __name__ == '__main__':" in content and "app.run(" in content:
        print("✅ App has proper structure for both development and production")
        return True
    else:
        print("⚠️ App structure might not be optimal for Gunicorn")
        return False

def generate_render_deployment_guide():
    """Generate deployment guide for Render"""
    print("\n📝 Generating Render deployment guide...")
    
    guide = """
# StartSmart Deployment Guide for Render

## Environment Variables to Set in Render:
1. SECRET_KEY=your-random-secret-key-here
2. FLASK_ENV=production

## Build Command:
pip install -r requirements.txt

## Start Command:
gunicorn app:app

## Important Notes:
- Database will be reset on each deployment (consider using PostgreSQL for persistence)
- Upload files won't persist (consider using cloud storage)
- Sessions are configured for HTTP (change to HTTPS when using custom domain)

## Debugging Routes (remove in production):
- /test-auth - Test authentication system
- /debug-session - Debug session data

## Post-Deployment Testing:
1. Visit /test-auth to verify database connectivity
2. Try registering a new user
3. Test login functionality
4. Check dashboard access

## Common Issues:
- If login fails, check Render logs for database errors
- If sessions don't work, verify SECRET_KEY is set
- If styles don't load, check static file serving

"""
    
    with open('RENDER_DEPLOYMENT_GUIDE.md', 'w') as f:
        f.write(guide)
    
    print("✅ Deployment guide created: RENDER_DEPLOYMENT_GUIDE.md")

def main():
    """Run all checks"""
    print("🔍 StartSmart Deployment Checklist")
    print("=" * 40)
    
    checks = [
        check_requirements,
        check_database,
        check_secret_key,
        check_app_structure,
        check_gunicorn_config
    ]
    
    passed = 0
    total = len(checks)
    
    for check in checks:
        if check():
            passed += 1
    
    print(f"\n📊 Results: {passed}/{total} checks passed")
    
    if passed == total:
        print("🎉 All checks passed! Your app is ready for deployment.")
        generate_render_deployment_guide()
    else:
        print("⚠️ Some issues need to be addressed before deployment.")
    
    print(f"\n⏰ Checklist run at: {datetime.now()}")

if __name__ == '__main__':
    main()
