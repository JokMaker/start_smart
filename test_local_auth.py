"""
Test authentication locally before deploying
"""
import sqlite3
from werkzeug.security import check_password_hash

def test_local_auth():
    """Test that authentication works locally"""
    
    print("🧪 TESTING LOCAL AUTHENTICATION...")
    
    conn = sqlite3.connect('startsmart.db')
    c = conn.cursor()
    
    # Test 1: Check users exist
    print("\n1️⃣ Checking users in database...")
    c.execute("SELECT email, name, user_type FROM users")
    users = c.fetchall()
    
    if users:
        print(f"   Found {len(users)} users:")
        for user in users:
            print(f"   - {user[0]} ({user[1]}) - {user[2]}")
    else:
        print("   ❌ No users found!")
        return False
    
    # Test 2: Test password verification
    print("\n2️⃣ Testing password verification...")
    test_email = 'student@demo.com'
    test_password = 'Demo123!'
    
    c.execute("SELECT password FROM users WHERE email = ?", (test_email,))
    result = c.fetchone()
    
    if result:
        stored_hash = result[0]
        if check_password_hash(stored_hash, test_password):
            print(f"   ✅ Password verification works for {test_email}")
        else:
            print(f"   ❌ Password verification failed for {test_email}")
            return False
    else:
        print(f"   ❌ User {test_email} not found")
        return False
    
    # Test 3: Check jobs exist
    print("\n3️⃣ Checking jobs in database...")
    c.execute("SELECT COUNT(*) FROM jobs WHERE is_active = 1")
    job_count = c.fetchone()[0]
    print(f"   Found {job_count} active jobs")
    
    conn.close()
    
    if job_count > 0:
        print("\n✅ LOCAL AUTHENTICATION READY!")
        return True
    else:
        print("\n⚠️ No jobs found, but authentication should work")
        return True

if __name__ == "__main__":
    test_local_auth()
