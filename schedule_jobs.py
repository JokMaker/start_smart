import schedule
import time
from adzuna_integration import import_jobs_from_adzuna

def job_import_task():
    """Run job import daily"""
    print("Starting scheduled job import...")
    import_jobs_from_adzuna()

# Schedule job import every day at 9 AM
schedule.every().day.at("09:00").do(job_import_task)

print("Job scheduler started. Press Ctrl+C to stop.")
while True:
    schedule.run_pending()
    time.sleep(60)  # Check every minute