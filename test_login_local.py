"""
Test login functionality locally to ensure it works before deployment
"""
import sqlite3
from werkzeug.security import check_password_hash

def test_login_locally():
    """Test login logic with local database"""
    
    print("🔑 TESTING LOGIN LOGIC LOCALLY...")
    print("=" * 50)
    
    # Test credentials
    test_email = 'student@demo.com'
    test_password = 'Demo123!'
    
    try:
        conn = sqlite3.connect('startsmart.db')
        c = conn.cursor()
        
        # Check if user exists
        print(f"📧 Looking for user: {test_email}")
        c.execute("SELECT id, name, password, email, user_type FROM users WHERE LOWER(email) = ?", (test_email.lower(),))
        user = c.fetchone()
        
        if user:
            print(f"✅ User found: {user[1]} (ID: {user[0]}, Type: {user[4]})")
            
            # Test password verification
            stored_hash = user[2]
            print(f"🔒 Testing password verification...")
            
            if check_password_hash(stored_hash, test_password):
                print("✅ Password verification PASSED!")
                print("🎉 LOGIN LOGIC WORKS LOCALLY!")
                
                # Test session data that would be set
                session_data = {
                    'user_id': user[0],
                    'user_name': user[1], 
                    'user_email': user[3],
                    'user_type': user[4]
                }
                
                print("📋 Session data that would be set:")
                for key, value in session_data.items():
                    print(f"   {key}: {value}")
                
                conn.close()
                return True
            else:
                print("❌ Password verification FAILED!")
                print("   This means either:")
                print("   1. Password hash is corrupted")
                print("   2. Wrong password format")
                print("   3. Hashing method mismatch")
                
        else:
            print(f"❌ User {test_email} not found in database!")
            
            # Show what users exist
            c.execute("SELECT email, name FROM users")
            users = c.fetchall()
            print(f"📋 Available users in database:")
            for email, name in users:
                print(f"   - {email} ({name})")
        
        conn.close()
        return False
        
    except Exception as e:
        print(f"❌ Error testing login: {e}")
        return False

def test_all_demo_users():
    """Test login for all demo users"""
    
    print("\n🔑 TESTING ALL DEMO USERS...")
    print("=" * 50)
    
    demo_users = [
        ('student@demo.com', 'Demo123!'),
        ('recruiter@demo.com', 'Demo123!'),
        ('admin@demo.com', 'Demo123!')
    ]
    
    conn = sqlite3.connect('startsmart.db')
    c = conn.cursor()
    
    for email, password in demo_users:
        print(f"\n📧 Testing: {email}")
        
        c.execute("SELECT id, name, password FROM users WHERE LOWER(email) = ?", (email,))
        user = c.fetchone()
        
        if user:
            if check_password_hash(user[2], password):
                print(f"   ✅ {email} login works!")
            else:
                print(f"   ❌ {email} password verification failed!")
        else:
            print(f"   ❌ {email} not found!")
    
    conn.close()

if __name__ == "__main__":
    success = test_login_locally()
    test_all_demo_users()
    
    if success:
        print("\n🎯 LOGIN FUNCTIONALITY IS WORKING LOCALLY!")
        print("   Issue must be in deployment environment")
    else:
        print("\n🔧 LOGIN ISSUES FOUND LOCALLY - Need to fix")
