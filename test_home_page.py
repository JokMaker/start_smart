#!/usr/bin/env python3
"""
Test script to diagnose home page database issues
"""

import sqlite3
import os
from datetime import datetime

def test_database_schema():
    """Test if all required tables and columns exist"""
    print("🔍 Testing database schema for home page...")
    
    if not os.path.exists('startsmart.db'):
        print("❌ Database file doesn't exist!")
        return False
    
    conn = sqlite3.connect('startsmart.db')
    c = conn.cursor()
    
    try:
        # Test users table
        print("Testing users table...")
        c.execute("SELECT COUNT(*) FROM users")
        user_count = c.fetchone()[0]
        print(f"✅ Users table: {user_count} records")
        
        # Test jobs table with correct column name
        print("Testing jobs table...")
        c.execute("SELECT COUNT(*) FROM jobs")
        job_count = c.fetchone()[0]
        print(f"✅ Jobs table: {job_count} records")
        
        # Test the specific query from home page
        print("Testing home page jobs query...")
        c.execute("""SELECT id, title, company, description, location, job_type, salary, 
                     application_url, created_at FROM jobs 
                     WHERE is_active = 1
                     ORDER BY created_at DESC LIMIT 4""")
        recent_jobs = c.fetchall()
        print(f"✅ Recent jobs query: {len(recent_jobs)} records")
        
        # Test startups table
        print("Testing startups table...")
        c.execute("SELECT COUNT(*) FROM startups")
        startup_count = c.fetchone()[0]
        print(f"✅ Startups table: {startup_count} records")
        
        # Test the specific startups query from home page
        print("Testing home page startups query...")
        c.execute("""SELECT id, name, description, industry, founder_id 
                     FROM startups ORDER BY created_at DESC LIMIT 3""")
        featured_startups = c.fetchall()
        print(f"✅ Featured startups query: {len(featured_startups)} records")
        
        # Test skills table
        print("Testing skills table...")
        c.execute("SELECT COUNT(*) FROM skills")
        skills_count = c.fetchone()[0]
        print(f"✅ Skills table: {skills_count} records")
        
        # Test job_skills table
        print("Testing job_skills table...")
        c.execute("SELECT COUNT(*) FROM job_skills")
        job_skills_count = c.fetchone()[0]
        print(f"✅ Job skills table: {job_skills_count} records")
        
        print("\n✅ All database schema tests passed!")
        return True
        
    except sqlite3.Error as e:
        print(f"❌ Database error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False
    finally:
        conn.close()

def test_home_page_logic():
    """Test the exact logic from the home page route"""
    print("\n🏠 Testing home page logic...")
    
    conn = sqlite3.connect('startsmart.db')
    c = conn.cursor()
    
    try:
        # Get counts (same as home page)
        c.execute("SELECT COUNT(*) FROM users")
        user_count = c.fetchone()[0]
        
        c.execute("SELECT COUNT(*) FROM jobs")
        job_count = c.fetchone()[0]
        
        c.execute("SELECT COUNT(*) FROM startups")
        startup_count = c.fetchone()[0]
        
        c.execute("SELECT COUNT(*) FROM users WHERE user_type = 'mentor'")
        mentor_count = c.fetchone()[0]
        
        print(f"📊 Stats: {user_count} users, {job_count} jobs, {startup_count} startups, {mentor_count} mentors")
        
        # Get recent jobs (same query as home page)
        c.execute("""SELECT id, title, company, description, location, job_type, salary, 
                     application_url, created_at FROM jobs 
                     WHERE is_active = 1
                     ORDER BY created_at DESC LIMIT 4""")
        recent_jobs_raw = c.fetchall()
        print(f"📋 Recent jobs: {len(recent_jobs_raw)} found")
        
        # Process recent jobs (same as home page)
        recent_jobs = []
        for job in recent_jobs_raw:
            job_dict = list(job)
            # job[8] is the created_at field
            if job_dict[8] and isinstance(job_dict[8], str):
                try:
                    job_dict[8] = datetime.strptime(job_dict[8], '%Y-%m-%d %H:%M:%S.%f')
                except ValueError:
                    try:
                        job_dict[8] = datetime.strptime(job_dict[8], '%Y-%m-%d %H:%M:%S')
                    except ValueError:
                        job_dict[8] = None
            recent_jobs.append(tuple(job_dict))
        
        # Get job skills (same as home page)
        job_skills = {}
        for job in recent_jobs:
            c.execute("""SELECT s.name FROM skills s 
                         JOIN job_skills js ON s.id = js.skill_id 
                         WHERE js.job_id = ? LIMIT 3""", (job[0],))
            skills = [skill[0] for skill in c.fetchall()]
            job_skills[job[0]] = skills
        
        print(f"🎯 Job skills processed: {len(job_skills)} jobs")
        
        # Get featured startups (same as home page)
        c.execute("""SELECT id, name, description, industry, founder_id 
                     FROM startups ORDER BY created_at DESC LIMIT 3""")
        featured_startups = c.fetchall()
        print(f"🚀 Featured startups: {len(featured_startups)} found")
        
        # Process founder names (same as home page)
        founder_names = {}
        founder_images = {}
        for startup in featured_startups:
            founder_id = startup[4]  # founder_id is at index 4
            if founder_id:
                c.execute("SELECT name FROM users WHERE id = ?", (founder_id,))
                founder_result = c.fetchone()
                founder_names[startup[0]] = founder_result[0] if founder_result else 'Unknown Founder'
            else:
                founder_names[startup[0]] = 'Unknown Founder'
            founder_images[startup[0]] = 'default-profile.jpg'
        
        print(f"👥 Founder names processed: {len(founder_names)} startups")
        
        print("\n✅ Home page logic test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Home page logic error: {e}")
        return False
    finally:
        conn.close()

if __name__ == "__main__":
    print("🧪 Starting home page diagnostic tests...\n")
    
    schema_ok = test_database_schema()
    if schema_ok:
        logic_ok = test_home_page_logic()
        if logic_ok:
            print("\n🎉 All tests passed! Home page should work correctly.")
        else:
            print("\n❌ Home page logic failed. Check the errors above.")
    else:
        print("\n❌ Database schema issues found. Check the errors above.")
