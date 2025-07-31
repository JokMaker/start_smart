import sqlite3
from datetime import datetime, timedelta
import random

def populate_production_jobs():
    """Add sample jobs for production deployment"""
    conn = sqlite3.connect('startsmart.db')
    c = conn.cursor()
    
    # Sample jobs data
    jobs_data = [
        ("Software Developer", "TechCorp Africa", "Join our dynamic team building innovative solutions for African markets. Experience with Python, JavaScript required.", "Lagos, Nigeria", "$50,000 - $70,000", "full-time", "Bachelor's degree in Computer Science, 2+ years experience", "Health insurance, Remote work options"),
        ("Digital Marketing Specialist", "StartUp Hub", "Drive growth through digital marketing campaigns. Social media, SEO, content marketing experience needed.", "Nairobi, Kenya", "$30,000 - $45,000", "full-time", "Marketing degree, Google Ads certification preferred", "Flexible hours, Professional development"),
        ("Data Analyst", "FinTech Solutions", "Analyze financial data to drive business decisions. SQL, Python, Excel expertise required.", "Cape Town, South Africa", "$40,000 - $55,000", "full-time", "Statistics/Math degree, 1+ years experience", "Stock options, Learning budget"),
        ("UI/UX Designer", "Creative Agency", "Design user-friendly interfaces for mobile and web applications. Portfolio required.", "Accra, Ghana", "$35,000 - $50,000", "full-time", "Design degree, Figma/Adobe experience", "Creative environment, Design tools provided"),
        ("Sales Representative", "AgriTech Company", "Sell innovative agricultural technology solutions to farmers and cooperatives.", "Kampala, Uganda", "$25,000 - $40,000", "full-time", "Sales experience, Agricultural knowledge preferred", "Commission bonuses, Travel opportunities"),
        ("Content Writer", "Media House", "Create engaging content for various digital platforms. Strong writing skills essential.", "Kigali, Rwanda", "$20,000 - $30,000", "part-time", "Journalism/Communications degree, Writing portfolio", "Flexible schedule, Byline opportunities"),
        ("Mobile App Developer", "Innovation Lab", "Develop mobile applications for Android and iOS platforms. React Native experience preferred.", "Dar es Salaam, Tanzania", "$45,000 - $60,000", "full-time", "Computer Science degree, Mobile development experience", "Latest tech stack, Conference attendance"),
        ("Business Analyst", "Consulting Firm", "Analyze business processes and recommend improvements. Strong analytical skills required.", "Addis Ababa, Ethiopia", "$35,000 - $48,000", "full-time", "Business degree, Analytical experience", "Client exposure, Professional growth"),
        ("Graphic Designer", "Advertising Agency", "Create visual designs for print and digital media. Creative portfolio essential.", "Casablanca, Morocco", "$28,000 - $38,000", "full-time", "Design degree, Adobe Creative Suite mastery", "Creative projects, Design awards"),
        ("Project Manager", "Construction Company", "Manage infrastructure projects across multiple locations. PMP certification preferred.", "Abuja, Nigeria", "$55,000 - $75,000", "full-time", "Engineering degree, 5+ years project management", "Leadership role, International projects")
    ]
    
    # Insert jobs
    for i, (title, company, description, location, salary, job_type, requirements, benefits) in enumerate(jobs_data):
        # Create application URL
        app_url = f"https://start-smart.onrender.com/job/{i+1}"
        
        # Random created date within last 30 days
        days_ago = random.randint(1, 30)
        created_at = datetime.now() - timedelta(days=days_ago)
        
        # Deadline 30 days from creation
        deadline = created_at + timedelta(days=30)
        
        c.execute("""INSERT OR REPLACE INTO jobs 
                  (title, company, description, location, salary, job_type, posted_by, 
                   created_at, requirements, benefits, deadline, application_url, is_active) 
                  VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                 (title, company, description, location, salary, job_type, 2,  # posted_by = 2 (recruiter)
                  created_at, requirements, benefits, deadline.strftime('%Y-%m-%d'), app_url, 1))
    
    conn.commit()
    
    # Verify jobs were added
    c.execute("SELECT COUNT(*) FROM jobs WHERE is_active = 1")
    job_count = c.fetchone()[0]
    
    conn.close()
    print(f"✅ Added {len(jobs_data)} jobs to database. Total active jobs: {job_count}")

def populate_sample_users():
    """Add sample users for demo"""
    from werkzeug.security import generate_password_hash
    
    conn = sqlite3.connect('startsmart.db')
    c = conn.cursor()
    
    # Sample users
    users_data = [
        ("student@demo.com", "Demo123!", "Demo Student", "student"),
        ("recruiter@demo.com", "Demo123!", "Demo Recruiter", "recruiter"),
        ("mentor@demo.com", "Demo123!", "Demo Mentor", "mentor")
    ]
    
    for email, password, name, user_type in users_data:
        # Check if user exists
        c.execute("SELECT id FROM users WHERE email = ?", (email,))
        if not c.fetchone():
            password_hash = generate_password_hash(password, method='pbkdf2:sha256')
            c.execute("""INSERT INTO users (email, password, name, user_type, created_at, is_active) 
                         VALUES (?, ?, ?, ?, ?, ?)""",
                     (email, password_hash, name, user_type, datetime.now(), 1))
            print(f"✅ Created user: {email}")
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    populate_production_jobs()
    populate_sample_users()