#!/usr/bin/env python3
"""
StartSmart Job Management CLI
Command line interface for managing jobs from Adzuna API
"""

import argparse
import sys
from job_fetcher import AdzunaJobFetcher
import sqlite3
from datetime import datetime

def fetch_jobs(countries=['gb', 'us'], pages=2):
    """Fetch jobs from Adzuna API"""
    print(f"🔄 Fetching jobs from {countries} ({pages} pages each)...")
    
    fetcher = AdzunaJobFetcher()
    try:
        saved, duplicates = fetcher.fetch_and_save_jobs(
            countries=countries,
            pages_per_country=pages
        )
        print(f"✅ Success! Added {saved} new jobs, skipped {duplicates} duplicates")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def count_jobs():
    """Count total jobs in database"""
    try:
        conn = sqlite3.connect('startsmart.db')
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM jobs")
        total = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM jobs WHERE is_active = 1")
        active = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM jobs WHERE created_at >= date('now', '-7 days')")
        recent = cursor.fetchone()[0]
        
        conn.close()
        
        print(f"📊 Job Statistics:")
        print(f"   Total jobs: {total}")
        print(f"   Active jobs: {active}")
        print(f"   Added in last 7 days: {recent}")
        
    except Exception as e:
        print(f"❌ Error counting jobs: {e}")

def clean_jobs():
    """Clean up old or duplicate jobs"""
    try:
        conn = sqlite3.connect('startsmart.db')
        cursor = conn.cursor()
        
        # Remove jobs older than 60 days
        cursor.execute("DELETE FROM jobs WHERE created_at < date('now', '-60 days')")
        old_deleted = cursor.rowcount
        
        # Remove exact duplicates (same title, company, location)
        cursor.execute("""
            DELETE FROM jobs WHERE id NOT IN (
                SELECT MIN(id) FROM jobs 
                GROUP BY title, company, location
            )
        """)
        duplicates_deleted = cursor.rowcount
        
        conn.commit()
        conn.close()
        
        print(f"🧹 Cleanup completed:")
        print(f"   Removed {old_deleted} old jobs (>60 days)")
        print(f"   Removed {duplicates_deleted} duplicate jobs")
        
    except Exception as e:
        print(f"❌ Error during cleanup: {e}")

def list_recent_jobs(limit=10):
    """List most recent jobs"""
    try:
        conn = sqlite3.connect('startsmart.db')
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT title, company, location, salary, created_at 
            FROM jobs 
            ORDER BY created_at DESC 
            LIMIT ?
        """, (limit,))
        
        jobs = cursor.fetchall()
        conn.close()
        
        if jobs:
            print(f"📋 {len(jobs)} Most Recent Jobs:")
            print("-" * 80)
            for job in jobs:
                title, company, location, salary, created_at = job
                print(f"• {title}")
                print(f"  Company: {company}")
                print(f"  Location: {location}")
                print(f"  Salary: {salary}")
                print(f"  Added: {created_at}")
                print()
        else:
            print("No jobs found in database")
            
    except Exception as e:
        print(f"❌ Error listing jobs: {e}")

def main():
    parser = argparse.ArgumentParser(description='StartSmart Job Management CLI')
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Fetch command
    fetch_parser = subparsers.add_parser('fetch', help='Fetch jobs from Adzuna API')
    fetch_parser.add_argument('--countries', nargs='+', default=['gb', 'us'],
                             help='Country codes to fetch from (default: gb us)')
    fetch_parser.add_argument('--pages', type=int, default=2,
                             help='Pages per country (default: 2)')
    
    # Count command
    subparsers.add_parser('count', help='Count jobs in database')
    
    # Clean command
    subparsers.add_parser('clean', help='Clean up old and duplicate jobs')
    
    # List command
    list_parser = subparsers.add_parser('list', help='List recent jobs')
    list_parser.add_argument('--limit', type=int, default=10,
                            help='Number of jobs to show (default: 10)')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    print(f"🚀 StartSmart Job Manager - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    if args.command == 'fetch':
        fetch_jobs(args.countries, args.pages)
    elif args.command == 'count':
        count_jobs()
    elif args.command == 'clean':
        clean_jobs()
    elif args.command == 'list':
        list_recent_jobs(args.limit)

if __name__ == '__main__':
    main()
