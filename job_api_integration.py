import requests
import sqlite3
from datetime import datetime

def fetch_jobs_from_api():
    """Example: Fetch jobs from external API and save to database"""
    
    # Example APIs you could use:
    # - GitHub Jobs API
    # - Reed API
    # - Adzuna API
    # - RemoteOK API
    
    try:
        # Example API call (replace with real API)
        response = requests.get('https://jobs.github.com/positions.json?location=africa')
        jobs_data = response.json()
        
        conn = sqlite3.connect('startsmart.db')
        c = conn.cursor()
        
        for job in jobs_data:
            # Check if job already exists
            c.execute("SELECT id FROM jobs WHERE title = ? AND company = ?", 
                     (job['title'], job['company']))
            
            if not c.fetchone():  # Job doesn't exist, add it
                c.execute("""INSERT INTO jobs 
                          (title, company, description, location, job_type, 
                           posted_by, created_at, application_url, is_active)
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                         (job['title'], job['company'], job['description'], 
                          job['location'], 'full-time', 1,  # System user ID
                          datetime.now(), job['url'], 1))
        
        conn.commit()
        conn.close()
        print(f"Imported {len(jobs_data)} jobs from API")
        
    except Exception as e:
        print(f"API fetch failed: {e}")

# Run this periodically (cron job, scheduler, etc.)
if __name__ == "__main__":
    fetch_jobs_from_api()