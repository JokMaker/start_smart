import sqlite3
from datetime import datetime

def populate_resources():
    conn = sqlite3.connect('startsmart.db')
    c = conn.cursor()
    
    # Sample resources data
    resources = [
        {
            'title': 'Complete Guide to Resume Writing for African Students',
            'description': 'Learn how to create a compelling resume that stands out to employers across Africa. Includes templates and examples.',
            'category': 'Career Development',
            'external_url': 'https://www.indeed.com/career-advice/resumes-cover-letters/how-to-make-a-resume',
            'uploaded_by': 1
        },
        {
            'title': 'Interview Skills Masterclass',
            'description': 'Master the art of job interviews with tips from HR professionals. Covers common questions and best practices.',
            'category': 'Interview Preparation',
            'external_url': 'https://www.linkedin.com/learning/topics/interview-skills',
            'uploaded_by': 1
        },
        {
            'title': 'Entrepreneurship in Africa: Success Stories',
            'description': 'Inspiring stories of successful African entrepreneurs and the lessons they learned on their journey.',
            'category': 'Entrepreneurship',
            'external_url': 'https://www.entrepreneur.com/topic/africa',
            'uploaded_by': 1
        },
        {
            'title': 'Digital Skills for the Modern Workplace',
            'description': 'Essential digital skills every professional needs in 2024. Covers Microsoft Office, Google Workspace, and more.',
            'category': 'Technical Skills',
            'external_url': 'https://www.coursera.org/browse/information-technology',
            'uploaded_by': 1
        },
        {
            'title': 'Networking Guide for Young Professionals',
            'description': 'How to build meaningful professional relationships and expand your network in Africa and globally.',
            'category': 'Professional Development',
            'external_url': 'https://www.harvard.edu/networking-guide',
            'uploaded_by': 1
        },
        {
            'title': 'Financial Literacy for Students',
            'description': 'Basic financial concepts every student should know: budgeting, saving, investing, and managing debt.',
            'category': 'Financial Education',
            'external_url': 'https://www.khanacademy.org/economics-finance-domain',
            'uploaded_by': 1
        },
        {
            'title': 'Leadership Skills Development',
            'description': 'Develop essential leadership qualities that will help you succeed in your career and make a positive impact.',
            'category': 'Leadership',
            'external_url': 'https://www.edx.org/learn/leadership',
            'uploaded_by': 1
        },
        {
            'title': 'Tech Career Paths in Africa',
            'description': 'Explore various technology career opportunities available across African countries and required skills.',
            'category': 'Career Development',
            'external_url': 'https://www.freecodecamp.org/news/tech-careers-guide',
            'uploaded_by': 1
        }
    ]
    
    for resource in resources:
        c.execute("""INSERT INTO resources 
                  (title, description, category, external_url, uploaded_by, created_at, view_count)
                  VALUES (?, ?, ?, ?, ?, ?, ?)""",
                 (resource['title'], resource['description'], resource['category'], 
                  resource['external_url'], resource['uploaded_by'], datetime.now(), 0))
    
    conn.commit()
    conn.close()
    print(f"✅ Added {len(resources)} resources!")

if __name__ == "__main__":
    populate_resources()