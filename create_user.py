import sqlite3
from werkzeug.security import generate_password_hash
from datetime import datetime

def create_user():
    """Create the user j.kur@alustudent.com with the same information from backup"""
    
    # User information from backup
    email = "j.kur@alustudent.com"
    name = "JOK JOHN MAKER"
    user_type = "recruiter"
    password = "StartSmart2024!"  # You'll need to set a new password
    
    print(f"Creating user: {name} ({email}) as {user_type}")
    
    # Connect to current database
    conn = sqlite3.connect('startsmart.db')
    c = conn.cursor()
    
    try:
        # Check if user already exists
        c.execute("SELECT id FROM users WHERE LOWER(email) = ?", (email.lower(),))
        existing_user = c.fetchone()
        
        if existing_user:
            print(f"❌ User with email {email} already exists!")
            return False
        
        # Generate password hash
        password_hash = generate_password_hash(password, method='pbkdf2:sha256')
        
        # Get the table structure first
        c.execute("PRAGMA table_info(users)")
        columns = c.fetchall()
        print("Available columns:")
        for col in columns:
            print(f"  - {col[1]} ({col[2]})")
        
        # Insert new user (using the actual table structure)
        c.execute("""INSERT INTO users (email, password, name, user_type, created_at) 
                     VALUES (?, ?, ?, ?, ?)""",
                 (email, password_hash, name, user_type, datetime.now()))
        
        conn.commit()
        new_user_id = c.lastrowid
        
        print(f"✅ User created successfully!")
        print(f"   ID: {new_user_id}")
        print(f"   Email: {email}")
        print(f"   Name: {name}")
        print(f"   User Type: {user_type}")
        print(f"   Password: {password}")
        print(f"   Created: {datetime.now()}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating user: {e}")
        return False
    finally:
        conn.close()

def verify_user():
    """Verify the user was created successfully"""
    conn = sqlite3.connect('startsmart.db')
    c = conn.cursor()
    
    c.execute("SELECT id, email, name, user_type, created_at FROM users WHERE email = ?", 
              ("j.kur@alustudent.com",))
    user = c.fetchone()
    
    if user:
        print(f"\n✅ User verification successful:")
        print(f"   ID: {user[0]}")
        print(f"   Email: {user[1]}")
        print(f"   Name: {user[2]}")
        print(f"   Type: {user[3]}")
        print(f"   Created: {user[4]}")
    else:
        print(f"\n❌ User verification failed - user not found")
    
    conn.close()

if __name__ == '__main__':
    print("=== Creating User j.kur@alustudent.com ===")
    success = create_user()
    
    if success:
        verify_user()
        print(f"\n🎉 User creation completed successfully!")
        print(f"📧 Email: j.kur@alustudent.com")
        print(f"🔑 Password: StartSmart2024!")
        print(f"🏷️ Role: Recruiter")
    else:
        print(f"\n❌ User creation failed!")
