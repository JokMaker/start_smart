"""
Quick fix: Add sample jobs for video demonstration
Since Adzuna integration was removed, we need jobs in the database
"""
import sqlite3
from datetime import datetime, timedelta
import random

def add_demo_jobs():
    """Add professional demo jobs for video demonstration"""
    
    conn = sqlite3.connect('startsmart.db')
    c = conn.cursor()
    
    # Clear existing jobs first
    c.execute("DELETE FROM jobs")
    
    # Professional African job listings
    demo_jobs = [
        {
            'title': 'Software Developer',
            'company': 'TechHub Africa',
            'description': 'Join our dynamic team building innovative fintech solutions for the African market. You will work with React, Node.js, and Python to create applications that serve millions of users across the continent.',
            'location': 'Lagos, Nigeria',
            'salary': '$40,000 - $60,000',
            'job_type': 'full-time',
            'requirements': 'Bachelor\'s degree in Computer Science, 2+ years experience with JavaScript frameworks, Knowledge of Python, Experience with databases',
            'benefits': 'Health insurance, Remote work flexibility, Professional development budget, Stock options'
        },
        {
            'title': 'Digital Marketing Specialist',
            'company': 'Growth Partners Kenya',
            'description': 'Drive digital marketing campaigns for leading African startups. Manage social media, content creation, SEO, and paid advertising across multiple platforms.',
            'location': 'Nairobi, Kenya',
            'salary': '$25,000 - $35,000',
            'job_type': 'full-time',
            'requirements': 'Marketing degree or equivalent, Google Ads certification, Social media management experience, Content creation skills',
            'benefits': 'Flexible working hours, Training opportunities, Performance bonuses, Modern office space'
        },
        {
            'title': 'Data Analyst',
            'company': 'Financial Services SA',
            'description': 'Analyze financial data to provide insights for business decisions. Work with large datasets, create reports, and present findings to senior management.',
            'location': 'Cape Town, South Africa',
            'salary': '$35,000 - $45,000',
            'job_type': 'full-time',
            'requirements': 'Statistics or Mathematics degree, SQL expertise, Excel advanced skills, Python or R knowledge preferred',
            'benefits': 'Medical aid, Retirement fund, Study assistance, Career progression'
        },
        {
            'title': 'UI/UX Designer',
            'company': 'Creative Studio Ghana',
            'description': 'Design user-friendly interfaces for mobile and web applications. Collaborate with developers and product managers to create exceptional user experiences.',
            'location': 'Accra, Ghana',
            'salary': '$30,000 - $40,000',
            'job_type': 'full-time',
            'requirements': 'Design degree, Figma and Adobe Creative Suite expertise, Portfolio of mobile/web designs, User research experience',
            'benefits': 'Creative environment, Latest design tools, Conference attendance, Flexible schedule'
        },
        {
            'title': 'Sales Representative',
            'company': 'AgriTech Solutions',
            'description': 'Sell innovative agricultural technology to farmers and cooperatives across East Africa. Build relationships and drive revenue growth.',
            'location': 'Kampala, Uganda',
            'salary': '$20,000 - $30,000 + Commission',
            'job_type': 'full-time',
            'requirements': 'Sales experience preferred, Agricultural knowledge a plus, Excellent communication skills, Valid driving license',
            'benefits': 'Commission structure, Travel allowances, Product training, Career advancement'
        },
        {
            'title': 'Content Writer',
            'company': 'Media House Rwanda',
            'description': 'Create engaging content for digital platforms, blogs, and social media. Research and write articles on technology, business, and African development.',
            'location': 'Kigali, Rwanda',
            'salary': '$18,000 - $25,000',
            'job_type': 'part-time',
            'requirements': 'Journalism or Communications degree, Excellent writing skills, Social media knowledge, Research abilities',
            'benefits': 'Byline opportunities, Flexible schedule, Professional network, Skill development'
        },
        {
            'title': 'Business Analyst',
            'company': 'Consulting Group',
            'description': 'Analyze business processes and recommend improvements for clients across various industries. Work on exciting projects with international companies.',
            'location': 'Addis Ababa, Ethiopia',
            'salary': '$32,000 - $42,000',
            'job_type': 'full-time',
            'requirements': 'Business or Economics degree, Analytical thinking, Excel and PowerPoint skills, Client interaction experience',
            'benefits': 'International exposure, Training programs, Healthcare, Performance bonuses'
        },
        {
            'title': 'Mobile App Developer',
            'company': 'Innovation Lab Tanzania',
            'description': 'Develop mobile applications for Android and iOS platforms. Work on cutting-edge projects that impact millions of users across Africa.',
            'location': 'Dar es Salaam, Tanzania',
            'salary': '$38,000 - $50,000',
            'job_type': 'full-time',
            'requirements': 'Computer Science degree, React Native or Flutter experience, Mobile development portfolio, API integration skills',
            'benefits': 'Latest technology stack, Conference attendance, Stock options, Learning budget'
        }
    ]
    
    print(f"Adding {len(demo_jobs)} professional jobs...")
    
    for i, job in enumerate(demo_jobs):
        # Random created date within last 15 days
        days_ago = random.randint(1, 15)
        created_at = datetime.now() - timedelta(days=days_ago)
        
        # Deadline 30 days from creation
        deadline = created_at + timedelta(days=30)
        
        # Application URL
        app_url = f"https://start-smart.onrender.com/apply/{i+1}"
        
        c.execute("""INSERT INTO jobs 
                  (title, company, description, location, salary, job_type, posted_by, 
                   created_at, requirements, benefits, deadline, application_url, is_active) 
                  VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                 (job['title'], job['company'], job['description'], job['location'],
                  job['salary'], job['job_type'], 2,  # posted_by recruiter
                  created_at, job['requirements'], job['benefits'],
                  deadline.strftime('%Y-%m-%d'), app_url, 1))
        
        print(f"✅ Added: {job['title']} at {job['company']}")
    
    conn.commit()
    
    # Verify jobs were added
    c.execute("SELECT COUNT(*) FROM jobs WHERE is_active = 1")
    job_count = c.fetchone()[0]
    
    conn.close()
    
    print(f"\n🎉 Successfully added {job_count} jobs!")
    print("Your jobs page will now show professional listings for the video!")
    
    return job_count

if __name__ == "__main__":
    add_demo_jobs()
