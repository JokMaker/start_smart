import sqlite3

def check_job_application():
    conn = sqlite3.connect('startsmart.db')
    c = conn.cursor()
    
    # Get the application details
    c.execute("""SELECT a.id, a.user_id, a.job_id, u.name, j.title, j.company
                 FROM applications a
                 JOIN users u ON a.user_id = u.id
                 JOIN jobs j ON a.job_id = j.id""")
    
    app = c.fetchone()
    if app:
        print(f"Application found:")
        print(f"  User: {app[3]} (ID: {app[1]})")
        print(f"  Job: {app[4]} at {app[5]} (ID: {app[2]})")
        print(f"  Application ID: {app[0]}")
        
        # Check if this is the job they're trying to view
        job_id = app[2]
        print(f"\nIf you're viewing job ID {job_id}, it will show 'already applied'")
        print(f"Try viewing a different job to see the apply button")
    
    # Show all available jobs
    c.execute("SELECT id, title, company FROM jobs WHERE is_active = 1 ORDER BY id")
    jobs = c.fetchall()
    
    print(f"\nAll available jobs:")
    for job in jobs:
        applied = "✓ APPLIED" if job[0] == app[2] else "○ Available"
        print(f"  Job ID {job[0]}: {job[1]} at {job[2]} - {applied}")
    
    conn.close()

if __name__ == "__main__":
    check_job_application()