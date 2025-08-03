"""
Automated Job Scheduler for StartSmart Platform
Run this script to automatically fetch jobs from Adzuna API at regular intervals
"""

from apscheduler.schedulers.blocking import BlockingScheduler
from job_fetcher import AdzunaJobFetcher
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('job_scheduler.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def scheduled_job_fetch():
    """
    Function to be called by the scheduler
    """
    logger.info("🔄 Starting scheduled job fetch...")
    
    try:
        fetcher = AdzunaJobFetcher()
        
        # Fetch jobs from supported countries
        countries = ['gb', 'us']  # Can add more supported countries
        pages = 1  # Fewer pages for automated runs to respect rate limits
        
        saved, duplicates = fetcher.fetch_and_save_jobs(
            countries=countries,
            pages_per_country=pages
        )
        
        logger.info(f"✅ Scheduled job fetch completed: {saved} new jobs, {duplicates} duplicates")
        
    except Exception as e:
        logger.error(f"❌ Scheduled job fetch failed: {e}")

def main():
    """
    Main scheduler function
    """
    scheduler = BlockingScheduler()
    
    # Schedule job fetching every 6 hours
    scheduler.add_job(
        scheduled_job_fetch,
        'interval',
        hours=6,
        id='job_fetch',
        name='Fetch jobs from Adzuna API'
    )
    
    # Also schedule a daily job fetch at 9 AM
    scheduler.add_job(
        scheduled_job_fetch,
        'cron',
        hour=9,
        minute=0,
        id='daily_job_fetch',
        name='Daily job fetch at 9 AM'
    )
    
    logger.info("🚀 Job scheduler started!")
    logger.info("📅 Jobs will be fetched every 6 hours and daily at 9 AM")
    logger.info("🛑 Press Ctrl+C to stop the scheduler")
    
    try:
        scheduler.start()
    except KeyboardInterrupt:
        logger.info("🛑 Scheduler stopped by user")
        scheduler.shutdown()

if __name__ == "__main__":
    # Run one job fetch immediately
    logger.info("🏃‍♂️ Running initial job fetch...")
    scheduled_job_fetch()
    
    # Start the scheduler
    main()
