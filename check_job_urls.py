import sqlite3

def check_job_urls():
    conn = sqlite3.connect('startsmart.db')
    c = conn.cursor()
    
    c.execute("SELECT id, title, company, application_url FROM jobs LIMIT 10")
    jobs = c.fetchall()
    
    print("Job URLs in database:")
    for job in jobs:
        print(f"Job {job[0]}: {job[1]} at {job[2]}")
        print(f"  URL: {job[3]}")
        print()
    
    conn.close()

if __name__ == "__main__":
    check_job_urls()