import sqlite3
from werkzeug.security import generate_password_hash
from datetime import datetime

def create_fresh_user(email, name, user_type, password="StartSmart2024!"):
    """Create a new user in the clean database"""
    
    conn = sqlite3.connect('startsmart.db')
    c = conn.cursor()
    
    try:
        # Check if user already exists
        c.execute("SELECT id FROM users WHERE LOWER(email) = ?", (email.lower(),))
        if c.fetchone():
            print(f"❌ User with email {email} already exists!")
            return False
        
        # Generate password hash
        password_hash = generate_password_hash(password, method='pbkdf2:sha256')
        
        # Insert new user
        c.execute("""INSERT INTO users (email, password, name, user_type, created_at) 
                     VALUES (?, ?, ?, ?, ?)""",
                 (email, password_hash, name, user_type, datetime.now()))
        
        conn.commit()
        new_user_id = c.lastrowid
        
        print(f"✅ Created user: {name}")
        print(f"   📧 Email: {email}")
        print(f"   🏷️ Type: {user_type}")
        print(f"   🔑 Password: {password}")
        print(f"   🆔 ID: {new_user_id}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating user {email}: {e}")
        return False
    finally:
        conn.close()

def show_all_users():
    """Display all users in the database"""
    conn = sqlite3.connect('startsmart.db')
    c = conn.cursor()
    
    c.execute("SELECT id, email, name, user_type, created_at FROM users ORDER BY id")
    users = c.fetchall()
    
    print(f"\n📋 Current users in database ({len(users)} total):")
    if users:
        for user in users:
            print(f"   ID: {user[0]}, Email: {user[1]}, Name: {user[2]}, Type: {user[3]}")
    else:
        print("   No users found")
    
    conn.close()
    return users

if __name__ == '__main__':
    print("=== Creating Fresh Users ===")
    
    # Example: Create some fresh users
    users_to_create = [
        {
            "email": "j.kur@alustudent.com",
            "name": "JOK JOHN MAKER",
            "user_type": "recruiter",
            "password": "MyPassword123!"
        },
        {
            "email": "student@example.com", 
            "name": "Student User",
            "user_type": "student",
            "password": "StudentPass123!"
        },
        {
            "email": "admin@startsmart.com",
            "name": "System Administrator", 
            "user_type": "admin",
            "password": "AdminPass123!"
        }
    ]
    
    print("Creating users...")
    for user_data in users_to_create:
        create_fresh_user(
            email=user_data["email"],
            name=user_data["name"], 
            user_type=user_data["user_type"],
            password=user_data["password"]
        )
        print()
    
    # Show final result
    show_all_users()
