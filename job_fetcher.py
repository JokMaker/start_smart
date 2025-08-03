import requests
import sqlite3
import json
from datetime import datetime, timedelta
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AdzunaJobFetcher:
    def __init__(self):
        self.app_id = "cdd821aa"
        self.app_key = "5722fc56488bc8a2fda4165d2ee54ad5"
        self.base_url = "https://api.adzuna.com/v1/api/jobs"
        self.countries = {
            'gb': 'United Kingdom',
            'us': 'United States', 
            'ca': 'Canada',
            'au': 'Australia',
            'za': 'South Africa',
            'de': 'Germany',
            'fr': 'France',
            'nl': 'Netherlands'
        }
        
    def fetch_jobs_from_country(self, country_code, pages=3, results_per_page=50):
        """
        Fetch jobs from a specific country using Adzuna API
        """
        all_jobs = []
        
        for page in range(1, pages + 1):
            try:
                url = f"{self.base_url}/{country_code}/search/{page}"
                params = {
                    'app_id': self.app_id,
                    'app_key': self.app_key,
                    'results_per_page': results_per_page,
                    'what': '',  # Broader search - get all types of jobs
                    'content-type': 'application/json'
                }
                
                logger.info(f"Fetching page {page} for {country_code}...")
                response = requests.get(url, params=params, timeout=30)
                
                if response.status_code == 200:
                    data = response.json()
                    jobs = data.get('results', [])
                    all_jobs.extend(jobs)
                    logger.info(f"Fetched {len(jobs)} jobs from page {page}")
                    
                    # Rate limiting - be respectful to API
                    time.sleep(1)
                elif response.status_code == 429:
                    logger.warning("Rate limit hit, waiting...")
                    time.sleep(5)
                    continue
                else:
                    logger.error(f"API error: {response.status_code} - {response.text}")
                    break
                    
            except requests.RequestException as e:
                logger.error(f"Request failed: {e}")
                continue
                
        return all_jobs
    
    def process_job_data(self, job_data, country_name):
        """
        Process and clean job data from Adzuna format to our database format
        """
        try:
            # Extract salary information
            salary_min = job_data.get('salary_min')
            salary_max = job_data.get('salary_max')
            
            if salary_min and salary_max:
                salary = f"${salary_min:,.0f} - ${salary_max:,.0f}/year"
            elif salary_min:
                salary = f"${salary_min:,.0f}+/year"
            elif salary_max:
                salary = f"Up to ${salary_max:,.0f}/year"
            else:
                salary = "Salary not specified"
            
            # Clean and format location
            location = job_data.get('location', {}).get('display_name', '')
            if not location:
                location = country_name
            
            # Determine job type
            title_lower = job_data.get('title', '').lower()
            if any(word in title_lower for word in ['intern', 'graduate', 'junior']):
                job_type = 'internship'
            elif any(word in title_lower for word in ['remote', 'work from home']):
                job_type = 'remote'
            elif any(word in title_lower for word in ['part time', 'part-time']):
                job_type = 'part-time'
            else:
                job_type = 'full-time'
            
            # Clean description
            description = job_data.get('description', '')
            if len(description) > 1000:
                description = description[:997] + "..."
            
            processed_job = {
                'title': job_data.get('title', 'Job Title Not Available'),
                'company': job_data.get('company', {}).get('display_name', 'Company Not Specified'),
                'description': description,
                'location': location,
                'salary': salary,
                'job_type': job_type,
                'application_url': job_data.get('redirect_url', ''),
                'requirements': self.extract_requirements(description),
                'benefits': self.extract_benefits(description),
                'external_id': job_data.get('id', ''),
                'source': 'Adzuna'
            }
            
            return processed_job
            
        except Exception as e:
            logger.error(f"Error processing job data: {e}")
            return None
    
    def extract_requirements(self, description):
        """
        Extract requirements from job description
        """
        requirements_keywords = [
            'requirements', 'required', 'must have', 'essential',
            'qualifications', 'skills needed', 'experience'
        ]
        
        description_lower = description.lower()
        for keyword in requirements_keywords:
            if keyword in description_lower:
                # Try to extract the requirements section
                start_idx = description_lower.find(keyword)
                # Look for the next 200 characters or until next section
                end_idx = min(start_idx + 200, len(description))
                requirements_text = description[start_idx:end_idx]
                return requirements_text[:200] + "..." if len(requirements_text) > 200 else requirements_text
        
        return "See job description for requirements"
    
    def extract_benefits(self, description):
        """
        Extract benefits from job description
        """
        benefits_keywords = [
            'benefits', 'package', 'perks', 'offer',
            'competitive salary', 'health insurance'
        ]
        
        description_lower = description.lower()
        for keyword in benefits_keywords:
            if keyword in description_lower:
                start_idx = description_lower.find(keyword)
                end_idx = min(start_idx + 150, len(description))
                benefits_text = description[start_idx:end_idx]
                return benefits_text[:150] + "..." if len(benefits_text) > 150 else benefits_text
        
        return "Competitive package offered"
    
    def save_jobs_to_database(self, jobs):
        """
        Save processed jobs to the database, avoiding duplicates
        """
        conn = sqlite3.connect('startsmart.db')
        cursor = conn.cursor()
        
        saved_count = 0
        duplicate_count = 0
        
        for job in jobs:
            try:
                # Check if job already exists (by title and company)
                cursor.execute(
                    "SELECT id FROM jobs WHERE title = ? AND company = ? AND location = ?",
                    (job['title'], job['company'], job['location'])
                )
                
                if cursor.fetchone():
                    duplicate_count += 1
                    continue
                
                # Set default values for database requirements
                deadline = datetime.now() + timedelta(days=30)  # 30 days from now
                posted_by = 1  # Default system user, you might want to create a dedicated API user
                
                cursor.execute("""
                    INSERT INTO jobs (
                        title, company, description, location, salary, job_type, 
                        posted_by, created_at, application_url, requirements, 
                        benefits, deadline, is_active
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    job['title'], job['company'], job['description'], job['location'],
                    job['salary'], job['job_type'], posted_by, datetime.now(),
                    job['application_url'], job['requirements'], job['benefits'],
                    deadline, True
                ))
                
                saved_count += 1
                
            except sqlite3.Error as e:
                logger.error(f"Database error saving job {job['title']}: {e}")
                continue
        
        conn.commit()
        conn.close()
        
        logger.info(f"Saved {saved_count} new jobs, skipped {duplicate_count} duplicates")
        return saved_count, duplicate_count
    
    def fetch_and_save_jobs(self, countries=['za', 'ke'], pages_per_country=2):
        """
        Main method to fetch jobs from multiple countries and save to database
        """
        logger.info("Starting job fetch from Adzuna API...")
        total_saved = 0
        total_duplicates = 0
        
        for country_code in countries:
            if country_code not in self.countries:
                logger.warning(f"Country code {country_code} not supported")
                continue
                
            country_name = self.countries[country_code]
            logger.info(f"Fetching jobs from {country_name}...")
            
            # Fetch raw job data
            raw_jobs = self.fetch_jobs_from_country(country_code, pages=pages_per_country)
            
            if not raw_jobs:
                logger.warning(f"No jobs fetched from {country_name}")
                continue
            
            # Process job data
            processed_jobs = []
            for raw_job in raw_jobs:
                processed_job = self.process_job_data(raw_job, country_name)
                if processed_job:
                    processed_jobs.append(processed_job)
            
            # Save to database
            saved, duplicates = self.save_jobs_to_database(processed_jobs)
            total_saved += saved
            total_duplicates += duplicates
            
            logger.info(f"Completed {country_name}: {saved} saved, {duplicates} duplicates")
        
        logger.info(f"Job fetch complete! Total: {total_saved} new jobs, {total_duplicates} duplicates")
        return total_saved, total_duplicates

def main():
    """
    Main function to run the job fetcher
    """
    fetcher = AdzunaJobFetcher()
    
    # Fetch jobs from supported countries (UK and US have most jobs)
    countries_to_fetch = ['gb', 'us']
    pages_per_country = 2  # Adjust based on how many jobs you want
    
    try:
        saved, duplicates = fetcher.fetch_and_save_jobs(
            countries=countries_to_fetch, 
            pages_per_country=pages_per_country
        )
        
        print(f"\n✅ Job fetch completed!")
        print(f"📊 Results: {saved} new jobs added, {duplicates} duplicates skipped")
        
    except Exception as e:
        logger.error(f"Job fetch failed: {e}")
        print(f"\n❌ Job fetch failed: {e}")

if __name__ == "__main__":
    main()
