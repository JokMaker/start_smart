import sqlite3

def check_applications():
    conn = sqlite3.connect('startsmart.db')
    c = conn.cursor()
    
    # Check total applications
    c.execute("SELECT COUNT(*) FROM applications")
    total_apps = c.fetchone()[0]
    print(f"Total applications: {total_apps}")
    
    # Check applications by user
    c.execute("""SELECT u.name, u.email, COUNT(a.id) as app_count
                 FROM users u 
                 LEFT JOIN applications a ON u.id = a.user_id 
                 WHERE u.user_type = 'student'
                 GROUP BY u.id, u.name, u.email
                 ORDER BY app_count DESC""")
    
    user_apps = c.fetchall()
    print("\nApplications by user:")
    for user in user_apps:
        print(f"  {user[0]} ({user[1]}): {user[2]} applications")
    
    # Check for duplicate applications
    c.execute("""SELECT user_id, job_id, COUNT(*) as duplicates
                 FROM applications 
                 GROUP BY user_id, job_id 
                 HAVING COUNT(*) > 1""")
    
    duplicates = c.fetchall()
    if duplicates:
        print(f"\nFound {len(duplicates)} duplicate applications:")
        for dup in duplicates:
            print(f"  User {dup[0]}, Job {dup[1]}: {dup[2]} applications")
    else:
        print("\nNo duplicate applications found")
    
    # Show recent applications
    c.execute("""SELECT a.id, u.name, j.title, j.company, a.applied_at
                 FROM applications a
                 JOIN users u ON a.user_id = u.id
                 JOIN jobs j ON a.job_id = j.id
                 ORDER BY a.applied_at DESC
                 LIMIT 10""")
    
    recent_apps = c.fetchall()
    print(f"\nRecent applications:")
    for app in recent_apps:
        print(f"  {app[1]} applied for {app[2]} at {app[3]} on {app[4]}")
    
    conn.close()

if __name__ == "__main__":
    check_applications()