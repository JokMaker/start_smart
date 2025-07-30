import sqlite3

# Connect to database and show all users
conn = sqlite3.connect('startsmart.db')
c = conn.cursor()

# Get all users
c.execute('SELECT id, name, email, user_type, created_at FROM users')
users = c.fetchall()

print('🔍 CURRENT USERS IN DATABASE')
print('=' * 60)
if users:
    for user in users:
        print(f'ID: {user[0]:2} | Name: {user[1]:20} | Email: {user[2]:30} | Type: {user[3]:10} | Created: {user[4]}')
else:
    print('No users found in database')

print(f'\nTotal Users: {len(users)}')
conn.close()
