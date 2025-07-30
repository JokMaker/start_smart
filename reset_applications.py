import sqlite3

def reset_applications():
    conn = sqlite3.connect('startsmart.db')
    c = conn.cursor()
    
    # Show current applications
    c.execute("""SELECT a.id, u.name, j.title, j.company
                 FROM applications a
                 JOIN users u ON a.user_id = u.id
                 JOIN jobs j ON a.job_id = j.id""")
    
    apps = c.fetchall()
    print("Current applications:")
    for app in apps:
        print(f"  {app[1]} applied for {app[2]} at {app[3]}")
    
    # Ask for confirmation
    if apps:
        confirm = input(f"\nDelete all {len(apps)} applications? (y/N): ")
        if confirm.lower() == 'y':
            c.execute("DELETE FROM applications")
            conn.commit()
            print("✅ All applications deleted!")
        else:
            print("❌ No changes made")
    else:
        print("No applications to delete")
    
    conn.close()

if __name__ == "__main__":
    reset_applications()