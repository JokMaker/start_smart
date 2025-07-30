import sqlite3

def fix_existing_users():
    """Fix null values for existing users"""
    conn = sqlite3.connect('startsmart.db')
    c = conn.cursor()
    
    # Update NULL values to empty strings for better template handling
    c.execute("UPDATE users SET bio = '' WHERE bio IS NULL")
    c.execute("UPDATE users SET skills = '' WHERE skills IS NULL") 
    c.execute("UPDATE users SET location = '' WHERE location IS NULL")
    c.execute("UPDATE users SET resume_file = '' WHERE resume_file IS NULL")
    c.execute("UPDATE users SET profile_image = '' WHERE profile_image IS NULL")
    
    conn.commit()
    
    # Check results
    c.execute("SELECT id, name, bio, skills, location FROM users")
    users = c.fetchall()
    
    print("Fixed existing users:")
    for user in users:
        print(f"  {user[1]}: bio='{user[2]}', skills='{user[3]}', location='{user[4]}'")
    
    conn.close()
    print("Existing users fixed!")

if __name__ == "__main__":
    fix_existing_users()