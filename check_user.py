import sqlite3
import os

def check_user():
    # Check if database exists
    if not os.path.exists('startsmart.db'):
        print('❌ Database file "startsmart.db" does not exist')
        return
    
    print('✅ Database file exists')
    
    # Connect and query for the specific user
    conn = sqlite3.connect('startsmart.db')
    c = conn.cursor()
    
    # First check table structure
    c.execute("PRAGMA table_info(users)")
    columns = c.fetchall()
    print('📋 Users table structure:')
    for col in columns:
        print(f'   {col[1]} ({col[2]})')
    
    # Search for the user
    email_to_find = 'j.kur@alustudent.com'
    c.execute('SELECT * FROM users WHERE LOWER(email) = ?', (email_to_find.lower(),))
    user = c.fetchone()
    
    if user:
        print(f'✅ User found in database:')
        print(f'   Full record: {user}')
    else:
        print(f'❌ User with email "{email_to_find}" NOT found in database')
    
    # Also show total user count for context
    c.execute('SELECT COUNT(*) FROM users')
    total_users = c.fetchone()[0]
    print(f'📊 Total users in database: {total_users}')
    
    # Show all users for verification
    c.execute('SELECT * FROM users ORDER BY id')
    all_users = c.fetchall()
    print(f'📋 All users in database:')
    for i, user in enumerate(all_users, 1):
        print(f'   User {i}: {user}')
    
    conn.close()

if __name__ == '__main__':
    check_user()
