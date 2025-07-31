#!/usr/bin/env python3
"""
Deployment Troubleshooting Script for StartSmart
This script identifies and fixes common deployment issues
"""

import os
import sys
import sqlite3
from datetime import datetime

def check_deployment_issues():
    """Check for common deployment issues"""
    print("🔍 StartSmart Deployment Troubleshooting")
    print("=" * 50)
    
    issues_found = []
    fixes_applied = []
    
    # 1. Check database initialization
    print("\n1. 📊 Database Check:")
    if not os.path.exists('startsmart.db'):
        print("   ❌ Database file missing!")
        issues_found.append("Database not initialized on deployment")
        
        # Initialize database
        try:
            from db_setup import setup_database
            setup_database()
            print("   ✅ Database initialized successfully")
            fixes_applied.append("Database created and populated")
        except Exception as e:
            print(f"   ❌ Database initialization failed: {e}")
            issues_found.append(f"Database initialization error: {e}")
    else:
        print("   ✅ Database file exists")
        
        # Check database contents
        conn = sqlite3.connect('startsmart.db')
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM users")
        user_count = c.fetchone()[0]
        print(f"   📈 Users in database: {user_count}")
        
        if user_count == 0:
            print("   ⚠️ No users in database - this might cause issues")
            issues_found.append("Empty users table")
        
        conn.close()
    
    # 2. Check environment variables
    print("\n2. 🔐 Environment Variables Check:")
    secret_key = os.environ.get('SECRET_KEY')
    if not secret_key or secret_key == 'dev-secret-key-change-in-production-2025':
        print("   ⚠️ Using default SECRET_KEY - should be changed for production")
        issues_found.append("Default SECRET_KEY in production")
    else:
        print("   ✅ Custom SECRET_KEY configured")
    
    flask_env = os.environ.get('FLASK_ENV', 'development')
    print(f"   📝 FLASK_ENV: {flask_env}")
    
    # 3. Check imports and dependencies
    print("\n3. 📦 Dependencies Check:")
    critical_imports = [
        'sqlite3', 'os', 're', 'flask', 'werkzeug.security', 
        'datetime', 'secrets', 'random'
    ]
    
    for module in critical_imports:
        try:
            __import__(module)
            print(f"   ✅ {module}")
        except ImportError as e:
            print(f"   ❌ {module}: {e}")
            issues_found.append(f"Missing dependency: {module}")
    
    # 4. Check session configuration
    print("\n4. 🍪 Session Configuration Check:")
    print("   📝 Session settings for deployment:")
    print("   - SESSION_COOKIE_HTTPONLY: True")
    print("   - SESSION_COOKIE_SAMESITE: 'Lax'")
    print("   - SESSION_COOKIE_SECURE: False (for HTTP deployment)")
    
    # 5. Check file permissions and paths
    print("\n5. 📁 File System Check:")
    upload_dir = 'static/uploads'
    if not os.path.exists(upload_dir):
        print(f"   ❌ Upload directory missing: {upload_dir}")
        os.makedirs(upload_dir, exist_ok=True)
        print(f"   ✅ Created upload directory: {upload_dir}")
        fixes_applied.append(f"Created {upload_dir} directory")
    else:
        print(f"   ✅ Upload directory exists: {upload_dir}")
    
    # 6. Check for common authentication issues
    print("\n6. 🔑 Authentication Issues Check:")
    common_auth_issues = [
        "Database connection failure on Render",
        "Session cookie configuration for HTTPS/HTTP",
        "Path issues with database file",
        "Memory/disk space limitations",
        "Environment variables not set",
        "Import errors for authentication modules"
    ]
    
    print("   📋 Common deployment authentication issues:")
    for issue in common_auth_issues:
        print(f"   • {issue}")
    
    return issues_found, fixes_applied

def create_deployment_database():
    """Create a fresh database specifically for deployment"""
    print("\n🚀 Creating Deployment Database...")
    
    try:
        # Remove existing database
        if os.path.exists('startsmart.db'):
            os.remove('startsmart.db')
            print("   🗑️ Removed existing database")
        
        # Create fresh database
        from db_setup import setup_database
        setup_database()
        print("   ✅ Fresh database created")
        
        # Verify database
        conn = sqlite3.connect('startsmart.db')
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM users")
        user_count = c.fetchone()[0]
        c.execute("SELECT COUNT(*) FROM jobs")
        job_count = c.fetchone()[0]
        c.execute("SELECT COUNT(*) FROM startups")
        startup_count = c.fetchone()[0]
        conn.close()
        
        print(f"   📊 Database populated:")
        print(f"      • Users: {user_count}")
        print(f"      • Jobs: {job_count}")
        print(f"      • Startups: {startup_count}")
        
        return True
    except Exception as e:
        print(f"   ❌ Database creation failed: {e}")
        return False

def test_authentication():
    """Test authentication functionality"""
    print("\n🧪 Testing Authentication...")
    
    try:
        # Test imports
        from werkzeug.security import generate_password_hash, check_password_hash
        print("   ✅ Password hashing imports working")
        
        # Test password hashing
        test_password = "TestPassword123!"
        hashed = generate_password_hash(test_password)
        verified = check_password_hash(hashed, test_password)
        
        if verified:
            print("   ✅ Password hashing/verification working")
        else:
            print("   ❌ Password verification failed")
            return False
        
        # Test database connection for auth
        conn = sqlite3.connect('startsmart.db')
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM users LIMIT 1")
        result = c.fetchone()
        conn.close()
        
        if result:
            print("   ✅ Database authentication queries working")
        else:
            print("   ❌ Database authentication queries failed")
            return False
        
        return True
    except Exception as e:
        print(f"   ❌ Authentication test failed: {e}")
        return False

def create_deployment_fix():
    """Create a deployment-specific version of app.py"""
    print("\n🔧 Creating Deployment Fix...")
    
    deployment_fixes = '''
# Add this to the top of your app.py after the imports for deployment debugging
import sys
print(f"Python version: {sys.version}")
print(f"Working directory: {os.getcwd()}")
print(f"Files in directory: {os.listdir('.')}")

# Add database initialization check in app.py
def ensure_database():
    """Ensure database exists and is properly initialized"""
    if not os.path.exists('startsmart.db'):
        print("Database missing, initializing...")
        try:
            from db_setup import setup_database
            setup_database()
            print("Database initialized successfully")
        except Exception as e:
            print(f"Database initialization failed: {e}")
            # Create minimal database if setup fails
            conn = sqlite3.connect('startsmart.db')
            c = conn.cursor()
            c.execute("""CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                name TEXT NOT NULL,
                user_type TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_active INTEGER DEFAULT 1
            )""")
            conn.commit()
            conn.close()
            print("Minimal database created")

# Call this function before creating the Flask app
ensure_database()
'''
    
    print("   📝 Deployment fixes to add to app.py:")
    print(deployment_fixes)
    
    # Create a simple test route for debugging
    test_route = '''
@app.route('/test-auth')
def test_auth():
    """Test route for debugging authentication"""
    try:
        # Test database connection
        conn = sqlite3.connect('startsmart.db')
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM users")
        user_count = c.fetchone()[0]
        conn.close()
        
        # Test session
        session['test'] = 'working'
        test_session = session.get('test', 'not working')
        
        return {
            'database': 'connected',
            'users': user_count,
            'session': test_session,
            'timestamp': datetime.now().isoformat()
        }
    except Exception as e:
        return {
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }
'''
    
    print("   🧪 Test route to add for debugging:")
    print(test_route)

def main():
    """Run comprehensive deployment troubleshooting"""
    issues, fixes = check_deployment_issues()
    
    print("\n" + "=" * 50)
    print("📋 TROUBLESHOOTING SUMMARY")
    print("=" * 50)
    
    if issues:
        print("\n❌ Issues Found:")
        for i, issue in enumerate(issues, 1):
            print(f"   {i}. {issue}")
    
    if fixes:
        print("\n✅ Fixes Applied:")
        for i, fix in enumerate(fixes, 1):
            print(f"   {i}. {fix}")
    
    # Test critical functionality
    auth_working = test_authentication()
    
    print("\n🎯 RECOMMENDATIONS FOR RENDER DEPLOYMENT:")
    print("1. Ensure database is initialized on first deploy")
    print("2. Check that all Python dependencies are in requirements.txt")
    print("3. Verify SECRET_KEY environment variable is set")
    print("4. Test /test-auth route after deployment")
    print("5. Check Render logs for specific error messages")
    
    print("\n🔧 IMMEDIATE FIXES:")
    print("1. Add database initialization check to app.py")
    print("2. Create test route for debugging")
    print("3. Ensure uploads directory exists")
    
    if not auth_working:
        print("\n⚠️ CRITICAL: Authentication tests failed locally!")
        print("This needs to be fixed before deployment will work.")
    
    # Offer to create fresh database
    create_db = input("\n❓ Create fresh database for deployment? (y/n): ").lower()
    if create_db == 'y':
        success = create_deployment_database()
        if success:
            print("✅ Database ready for deployment!")
    
    create_deployment_fix()

if __name__ == "__main__":
    main()
