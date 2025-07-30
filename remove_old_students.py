import sqlite3

def remove_old_students():
    """Remove old student users so they can re-register"""
    conn = sqlite3.connect('startsmart.db')
    c = conn.cursor()
    
    # Show current students
    c.execute("SELECT id, name, email FROM users WHERE user_type = 'student'")
    students = c.fetchall()
    
    print("Current students:")
    for student in students:
        print(f"  {student[1]} ({student[2]})")
    
    # Delete old student users (keep admin, mentors, recruiters)
    c.execute("DELETE FROM users WHERE user_type = 'student'")
    deleted_count = c.rowcount
    
    # Also clean up their applications
    c.execute("DELETE FROM applications WHERE user_id NOT IN (SELECT id FROM users)")
    
    conn.commit()
    conn.close()
    
    print(f"Removed {deleted_count} student users")
    print("Students can now register fresh with proper null handling")

if __name__ == "__main__":
    remove_old_students()