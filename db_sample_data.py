import sqlite3
import os
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash
import random

def populate_sample_data():
    """
    Populate the StartSmart database with sample data for testing.
    """
    print("Populating database with sample data...")
    
    # Create database connection
    conn = sqlite3.connect('startsmart.db')
    c = conn.cursor()
    
    # Sample users
    sample_users = [
        # Students
        ('student1@example.com', 'password123', 'John Smith', 'student', 'Computer Science student with interest in web development', 
         'Python, JavaScript, HTML/CSS', 'Kigali, Rwanda'),
        ('student2@example.com', 'password123', 'Mary Johnson', 'student', 'Business administration student looking for marketing opportunities', 
         'Marketing, Social Media, Content Creation', 'Nairobi, Kenya'),
        ('student3@example.com', 'password123', 'David Okafor', 'student', 'Engineering student specializing in renewable energy', 
         'CAD, Project Management, Renewable Energy', 'Lagos, Nigeria'),
        
        # Mentors
        ('mentor1@example.com', 'password123', 'Dr. Sarah Kimani', 'mentor', 'Software Engineer with 10 years of experience in tech startups', 
         'Software Development, Entrepreneurship, Career Guidance', 'Nairobi, Kenya'),
        ('mentor2@example.com', 'password123', 'Prof. James Mwangi', 'mentor', 'Business professor and startup consultant', 
         'Business Strategy, Finance, Marketing', 'Kigali, Rwanda'),
        
        # Recruiters
        ('recruiter1@example.com', 'password123', 'Tech Innovations Ltd', 'recruiter', 'Leading tech company in East Africa', 
         'Software Development, AI, Data Science', 'Kigali, Rwanda'),
        ('recruiter2@example.com', 'password123', 'Global Consulting Group', 'recruiter', 'International consulting firm with African operations', 
         'Consulting, Business Analysis, Project Management', 'Nairobi, Kenya')
    ]
    
    user_ids = {}
    for user in sample_users:
        email, password, name, user_type, bio, skills, location = user
        try:
            c.execute("INSERT INTO users (email, password, name, user_type, bio, skills, location, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                     (email, generate_password_hash(password), name, user_type, bio, skills, location, datetime.now()))
            user_ids[email] = c.lastrowid
        except sqlite3.IntegrityError:
            # User already exists, get their ID
            c.execute("SELECT id FROM users WHERE email = ?", (email,))
            user_ids[email] = c.fetchone()[0]
    
    # Sample jobs
    sample_jobs = [
        ('Junior Web Developer', 'Tech Innovations Ltd', 'We are looking for a talented Junior Web Developer to join our team.',
         'Kigali, Rwanda', '$800-$1200/month', 'full-time', user_ids['recruiter1@example.com'],
         'Strong knowledge of HTML, CSS, and JavaScript. Experience with React is a plus.',
         'Health insurance, flexible working hours, professional development opportunities',
         'https://apply.techinnovations.com/junior-web-dev'),
        
        ('Marketing Intern', 'Global Consulting Group', 'Join our marketing team as an intern and gain valuable experience.',
         'Nairobi, Kenya', '$400-$600/month', 'internship', user_ids['recruiter2@example.com'],
         'Currently pursuing a degree in Marketing or related field. Strong communication skills.',
         'Lunch allowance, transportation, potential for full-time employment',
         'https://careers.globalconsulting.com/intern'),
        
        ('Data Analyst', 'Tech Innovations Ltd', 'Seeking a data analyst to help derive insights from our customer data.',
         'Remote', '$1200-$1800/month', 'full-time', user_ids['recruiter1@example.com'],
         'Experience with SQL, Python, and data visualization tools. Statistics background preferred.',
         'Remote work, flexible hours, health insurance, annual bonus',
         'https://apply.techinnovations.com/data-analyst'),
        
        ('Business Development Associate', 'Global Consulting Group', 'Help us expand our business across Africa.',
         'Lagos, Nigeria', '$1000-$1500/month', 'full-time', user_ids['recruiter2@example.com'],
         'Degree in Business Administration or related field. Excellent networking skills.',
         'Commission structure, health benefits, travel opportunities',
         'https://careers.globalconsulting.com/biz-dev')
    ]
    
    job_ids = {}
    for job in sample_jobs:
        title, company, description, location, salary, job_type, posted_by, requirements, benefits, application_url = job
        deadline = datetime.now() + timedelta(days=30)  # 30 days from now
        
        try:
            c.execute("""INSERT INTO jobs 
                      (title, company, description, location, salary, job_type, posted_by, created_at, 
                       requirements, benefits, deadline, application_url) 
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                     (title, company, description, location, salary, job_type, posted_by, 
                      datetime.now(), requirements, benefits, deadline, application_url))
            job_ids[title] = c.lastrowid
        except sqlite3.IntegrityError:
            # Job might already exist
            c.execute("SELECT id FROM jobs WHERE title = ? AND company = ?", (title, company))
            result = c.fetchone()
            if result:
                job_ids[title] = result[0]
    
    # Sample applications
    sample_applications = [
        (job_ids['Junior Web Developer'], user_ids['student1@example.com'], 'pending'),
        (job_ids['Marketing Intern'], user_ids['student2@example.com'], 'shortlisted'),
        (job_ids['Data Analyst'], user_ids['student1@example.com'], 'pending'),
        (job_ids['Business Development Associate'], user_ids['student3@example.com'], 'reviewed')
    ]
    
    for application in sample_applications:
        job_id, user_id, status = application
        try:
            c.execute("INSERT INTO applications (job_id, user_id, status, applied_at) VALUES (?, ?, ?, ?)",
                     (job_id, user_id, status, datetime.now() - timedelta(days=random.randint(1, 10))))
        except sqlite3.IntegrityError:
            # Application might already exist
            pass
    
    # Sample startups
    sample_startups = [
        ('EcoSolutions', 'Developing sustainable energy solutions for rural communities', 
         'Energy', 'prototype', user_ids['student3@example.com']),
        ('LearnConnect', 'Online platform connecting students with local tutors', 
         'Education', 'early-stage', user_ids['student1@example.com'])
    ]
    
    startup_ids = {}
    for startup in sample_startups:
        name, description, industry, stage, founder_id = startup
        try:
            c.execute("INSERT INTO startups (name, description, industry, stage, founder_id, created_at) VALUES (?, ?, ?, ?, ?, ?)",
                     (name, description, industry, stage, founder_id, datetime.now()))
            startup_ids[name] = c.lastrowid
        except sqlite3.IntegrityError:
            # Startup might already exist
            c.execute("SELECT id FROM startups WHERE name = ?", (name,))
            result = c.fetchone()
            if result:
                startup_ids[name] = result[0]
    
    # Sample mentorship requests
    sample_mentorships = [
        (user_ids['mentor1@example.com'], user_ids['student1@example.com'], 'Web Development Career Advice',
         'I would like guidance on becoming a full-stack developer.', 'pending'),
        (user_ids['mentor2@example.com'], user_ids['student2@example.com'], 'Marketing Strategy Help',
         'I need advice on digital marketing strategies for my startup idea.', 'accepted')
    ]
    
    for mentorship in sample_mentorships:
        mentor_id, mentee_id, topic, message, status = mentorship
        try:
            c.execute("INSERT INTO mentorship (mentor_id, mentee_id, topic, message, status, created_at) VALUES (?, ?, ?, ?, ?, ?)",
                     (mentor_id, mentee_id, topic, message, status, datetime.now() - timedelta(days=random.randint(1, 15))))
        except sqlite3.IntegrityError:
            # Mentorship might already exist
            pass
    
    # Sample resources
    sample_resources = [
        ('Resume Writing Guide', 'Comprehensive guide to creating an effective resume', 'Guides', 
         None, user_ids['mentor1@example.com']),
        ('Business Plan Template', 'Template for creating a professional business plan', 'Templates', 
         None, user_ids['mentor2@example.com']),
        ('Interview Preparation Tips', 'Essential tips for acing job interviews', 'Guides', 
         None, user_ids['mentor1@example.com'])
    ]
    
    for resource in sample_resources:
        title, description, category, file_url, uploaded_by = resource
        try:
            c.execute("INSERT INTO resources (title, description, category, file_url, uploaded_by, created_at) VALUES (?, ?, ?, ?, ?, ?)",
                     (title, description, category, file_url, uploaded_by, datetime.now() - timedelta(days=random.randint(1, 30))))
        except sqlite3.IntegrityError:
            # Resource might already exist
            pass
    
    # Sample events
    sample_events = [
        ('Tech Career Workshop', 'Workshop on navigating tech careers in Africa', 'workshop',
         'Kigali Innovation Center', 0, datetime.now() + timedelta(days=14), 120, user_ids['mentor1@example.com'], 50),
        ('Entrepreneurship Webinar', 'Online session about starting a business with minimal capital', 'webinar',
         None, 1, datetime.now() + timedelta(days=7), 90, user_ids['mentor2@example.com'], 100)
    ]
    
    event_ids = {}
    for event in sample_events:
        title, description, event_type, location, is_virtual, event_date, duration, organizer_id, max_participants = event
        try:
            c.execute("""INSERT INTO events 
                      (title, description, event_type, location, is_virtual, event_date, duration, organizer_id, max_participants, created_at) 
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                     (title, description, event_type, location, is_virtual, event_date, duration, organizer_id, max_participants, datetime.now()))
            event_ids[title] = c.lastrowid
        except sqlite3.IntegrityError:
            # Event might already exist
            c.execute("SELECT id FROM events WHERE title = ? AND event_date = ?", (title, event_date))
            result = c.fetchone()
            if result:
                event_ids[title] = result[0]
    
    # Sample event registrations
    if event_ids:
        sample_registrations = [
            (event_ids['Tech Career Workshop'], user_ids['student1@example.com']),
            (event_ids['Tech Career Workshop'], user_ids['student3@example.com']),
            (event_ids['Entrepreneurship Webinar'], user_ids['student1@example.com']),
            (event_ids['Entrepreneurship Webinar'], user_ids['student2@example.com'])
        ]
        
        for registration in sample_registrations:
            event_id, user_id = registration
            try:
                c.execute("INSERT INTO event_registrations (event_id, user_id, registration_date) VALUES (?, ?, ?)",
                         (event_id, user_id, datetime.now()))
            except sqlite3.IntegrityError:
                # Registration might already exist
                pass
    
    # Link users with skills
    c.execute("SELECT id, name FROM skills")
    all_skills = c.fetchall()
    
    if all_skills:
        # For each student, assign 3-5 random skills
        for email in ['student1@example.com', 'student2@example.com', 'student3@example.com']:
            user_id = user_ids[email]
            num_skills = random.randint(3, 5)
            selected_skills = random.sample(all_skills, num_skills)
            
            for skill in selected_skills:
                skill_id, skill_name = skill
                proficiency = random.choice(['beginner', 'intermediate', 'advanced'])
                try:
                    c.execute("INSERT INTO user_skills (user_id, skill_id, proficiency_level) VALUES (?, ?, ?)",
                             (user_id, skill_id, proficiency))
                except sqlite3.IntegrityError:
                    # User skill might already exist
                    pass
        
        # For each job, assign 2-4 required skills
        for job_title, job_id in job_ids.items():
            num_skills = random.randint(2, 4)
            selected_skills = random.sample(all_skills, num_skills)
            
            for skill in selected_skills:
                skill_id, skill_name = skill
                try:
                    c.execute("INSERT INTO job_skills (job_id, skill_id, is_required) VALUES (?, ?, ?)",
                             (job_id, skill_id, 1))
                except sqlite3.IntegrityError:
                    # Job skill might already exist
                    pass
    
    conn.commit()
    conn.close()
    print("Sample data population complete!")

if __name__ == "__main__":
    populate_sample_data()