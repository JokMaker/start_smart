import requests
import sqlite3
from datetime import datetime

# Your Adzuna credentials
APP_ID = "cdd821aa"
APP_KEY = "5722fc56488bc8a2fda4165d2ee54ad5"

def import_jobs_from_adzuna():
    """Import jobs from Adzuna API to StartSmart database"""
    
    # Focus on South Africa only
    countries = {
        'za': 'South Africa'
    }
    
    conn = sqlite3.connect('startsmart.db')
    c = conn.cursor()
    
    total_imported = 0
    
    for country_code, country_name in countries.items():
        print(f"Fetching jobs from {country_name}...")
        
        url = f"https://api.adzuna.com/v1/api/jobs/{country_code}/search/1"
        
        # Try different search terms for more variety
        search_terms = ['', 'graduate', 'software', 'marketing', 'finance']
        
        for term in search_terms:
            params = {
                'app_id': APP_ID,
                'app_key': APP_KEY,
                'results_per_page': 10,
                'content-type': 'application/json'
            }
            if term:
                params['what'] = term
                print(f"  Searching for '{term}' jobs...")
        
            try:
                response = requests.get(url, params=params)
            
            if response.status_code == 200:
                data = response.json()
                print(f"  Found {data.get('count', 0)} jobs, importing {len(data['results'])}...")
                
                for job in data['results']:
                    # Check if job already exists
                    c.execute("SELECT id FROM jobs WHERE title = ? AND company = ?", 
                             (job['title'], job['company']['display_name']))
                    
                    if not c.fetchone():
                        # Insert new job
                        c.execute("""INSERT INTO jobs 
                                  (title, company, description, location, salary, job_type,
                                   posted_by, created_at, application_url, is_active, requirements)
                                  VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                                 (
                                     job['title'],
                                     job['company']['display_name'],
                                     job['description'][:1000],  # Limit description
                                     job['location']['display_name'],
                                     f"${job.get('salary_min', 0)}-${job.get('salary_max', 0)}" if job.get('salary_min') else '',
                                     'full-time',  # Default
                                     1,  # System user
                                     datetime.now(),
                                     job['redirect_url'],
                                     1,  # Active
                                     'See job description'  # Default requirements
                                 ))
                        total_imported += 1
                        print(f"  + {job['title']} at {job['company']['display_name']}")
                
            else:
                print(f"Error fetching {country_name}: {response.status_code}")
                
        except Exception as e:
            print(f"Error with {country_name}: {e}")
    
    conn.commit()
    conn.close()
    
    print(f"✅ Imported {total_imported} new jobs!")
    return total_imported

if __name__ == "__main__":
    if APP_ID == "your_app_id_here":
        print("⚠️ Please update APP_ID and APP_KEY first")
    else:
        import_jobs_from_adzuna()