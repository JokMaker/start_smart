import sqlite3
from datetime import datetime

def add_more_resources():
    conn = sqlite3.connect('startsmart.db')
    c = conn.cursor()
    
    # Additional resources with videos, case studies, and guides
    new_resources = [
        # Videos
        {
            'title': 'How to Start a Business in Africa - Complete Video Course',
            'description': 'Comprehensive video series covering business registration, funding, and growth strategies specifically for African entrepreneurs.',
            'category': 'Videos',
            'external_url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
            'uploaded_by': 1
        },
        {
            'title': 'Job Interview Skills - Video Tutorial Series',
            'description': 'Professional video tutorials on mastering job interviews, body language, and answering difficult questions.',
            'category': 'Videos',
            'external_url': 'https://www.coursera.org/learn/interview-skills',
            'uploaded_by': 1
        },
        {
            'title': 'Digital Marketing for African Businesses',
            'description': 'Video course on leveraging social media and digital platforms to grow your business in African markets.',
            'category': 'Videos',
            'external_url': 'https://www.udemy.com/course/digital-marketing-africa/',
            'uploaded_by': 1
        },
        
        # Case Studies
        {
            'title': 'Jumia Success Story: E-commerce in Africa',
            'description': 'Detailed case study of how Jumia became Africa\'s leading e-commerce platform, including challenges and solutions.',
            'category': 'Case Studies',
            'external_url': 'https://hbr.org/case-study/jumia-africa-ecommerce',
            'uploaded_by': 1
        },
        {
            'title': 'M-Pesa: Mobile Money Revolution Case Study',
            'description': 'Analysis of how M-Pesa transformed financial services in Kenya and lessons for other African countries.',
            'category': 'Case Studies',
            'external_url': 'https://www.gsma.com/mobilefordevelopment/m-pesa-case-study/',
            'uploaded_by': 1
        },
        {
            'title': 'Andela: Building Tech Talent in Africa',
            'description': 'Case study of Andela\'s model for training software developers and connecting African talent with global opportunities.',
            'category': 'Case Studies',
            'external_url': 'https://andela.com/case-studies/',
            'uploaded_by': 1
        },
        
        # Guides
        {
            'title': 'Complete Guide to Freelancing in Africa',
            'description': 'Step-by-step guide to starting a successful freelancing career, finding clients, and managing projects remotely.',
            'category': 'Guides',
            'external_url': 'https://www.upwork.com/resources/freelancing-guide-africa',
            'uploaded_by': 1
        },
        {
            'title': 'Startup Funding Guide for African Entrepreneurs',
            'description': 'Comprehensive guide covering angel investors, VCs, grants, and alternative funding sources available in Africa.',
            'category': 'Guides',
            'external_url': 'https://techcrunch.com/startup-funding-africa-guide/',
            'uploaded_by': 1
        },
        {
            'title': 'Personal Branding Guide for Professionals',
            'description': 'Step-by-step guide to building your personal brand on LinkedIn, Twitter, and other professional platforms.',
            'category': 'Guides',
            'external_url': 'https://blog.linkedin.com/personal-branding-guide',
            'uploaded_by': 1
        },
        
        # Templates
        {
            'title': 'African Business Plan Template',
            'description': 'Customized business plan template designed for African markets, including local regulations and market analysis.',
            'category': 'Templates',
            'external_url': 'https://www.score.org/business-plan-template-africa',
            'uploaded_by': 1
        },
        {
            'title': 'CV Template for African Job Market',
            'description': 'Professional CV template optimized for African employers, with examples and formatting guidelines.',
            'category': 'Templates',
            'external_url': 'https://www.indeed.com/career-advice/resumes-cover-letters/african-cv-template',
            'uploaded_by': 1
        },
        {
            'title': 'Pitch Deck Template for African Startups',
            'description': 'Investor pitch deck template with examples from successful African startups and funding tips.',
            'category': 'Templates',
            'external_url': 'https://slidebean.com/pitch-deck-template-africa',
            'uploaded_by': 1
        }
    ]
    
    for resource in new_resources:
        c.execute("""INSERT INTO resources 
                  (title, description, category, external_url, uploaded_by, created_at, view_count)
                  VALUES (?, ?, ?, ?, ?, ?, ?)""",
                 (resource['title'], resource['description'], resource['category'], 
                  resource['external_url'], resource['uploaded_by'], datetime.now(), 0))
    
    conn.commit()
    conn.close()
    print(f"✅ Added {len(new_resources)} additional resources!")
    print("Categories added:")
    categories = set([r['category'] for r in new_resources])
    for cat in categories:
        count = len([r for r in new_resources if r['category'] == cat])
        print(f"  - {cat}: {count} resources")

if __name__ == "__main__":
    add_more_resources()