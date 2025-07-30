import sqlite3
from datetime import datetime
from werkzeug.security import generate_password_hash

def populate_mentors():
    conn = sqlite3.connect('startsmart.db')
    c = conn.cursor()
    
    # Sample mentors data
    mentors = [
        {
            'name': 'Dr. Amina Hassan',
            'email': 'amina.hassan@mentor.com',
            'bio': 'Senior Software Engineer at Google with 10+ years experience. Passionate about mentoring young African developers and promoting diversity in tech.',
            'skills': 'Python, JavaScript, Machine Learning, Career Development',
            'location': 'Nairobi, Kenya',
            'user_type': 'mentor',
            'experience': 'Senior Software Engineer at Google, Former CTO at Kenyan startup, PhD in Computer Science'
        },
        {
            'name': 'James Okonkwo',
            'email': 'james.okonkwo@mentor.com',
            'bio': 'Successful entrepreneur and business consultant. Founded 3 startups in Nigeria and now helps young entrepreneurs build sustainable businesses.',
            'skills': 'Entrepreneurship, Business Strategy, Marketing, Fundraising',
            'location': 'Lagos, Nigeria',
            'user_type': 'mentor',
            'experience': 'CEO of TechHub Nigeria, Serial Entrepreneur, MBA from INSEAD'
        },
        {
            'name': 'Sarah Mukamana',
            'email': 'sarah.mukamana@mentor.com',
            'bio': 'Finance Director with expertise in banking and investment. Dedicated to empowering young women in finance and business leadership.',
            'skills': 'Finance, Investment Banking, Leadership, Financial Planning',
            'location': 'Kigali, Rwanda',
            'user_type': 'mentor',
            'experience': 'Finance Director at Bank of Kigali, Former Investment Banker at Standard Bank'
        },
        {
            'name': 'Michael Asante',
            'email': 'michael.asante@mentor.com',
            'bio': 'Marketing executive and digital strategist. Helps students and professionals build their personal brand and navigate the digital marketing landscape.',
            'skills': 'Digital Marketing, Brand Strategy, Social Media, Content Creation',
            'location': 'Accra, Ghana',
            'user_type': 'mentor',
            'experience': 'Head of Marketing at MTN Ghana, Digital Marketing Consultant'
        },
        {
            'name': 'Dr. Fatima Al-Rashid',
            'email': 'fatima.alrashid@mentor.com',
            'bio': 'Healthcare innovation expert and medical doctor. Mentors students interested in healthcare technology and medical careers.',
            'skills': 'Healthcare, Medical Technology, Innovation, Research',
            'location': 'Cairo, Egypt',
            'user_type': 'mentor',
            'experience': 'Chief Medical Officer at Cairo Health Tech, Practicing Physician, PhD in Medical Innovation'
        },
        {
            'name': 'David Mthembu',
            'email': 'david.mthembu@mentor.com',
            'bio': 'Renewable energy engineer and sustainability advocate. Guides students in engineering and environmental careers.',
            'skills': 'Renewable Energy, Engineering, Sustainability, Project Management',
            'location': 'Johannesburg, South Africa',
            'user_type': 'mentor',
            'experience': 'Senior Engineer at Eskom, Renewable Energy Consultant, MEng in Electrical Engineering'
        }
    ]
    
    for mentor in mentors:
        password_hash = generate_password_hash('MentorPass123!', method='pbkdf2:sha256')
        
        c.execute("""INSERT INTO users 
                  (name, email, password, user_type, bio, skills, location, created_at, is_active)
                  VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                 (mentor['name'], mentor['email'], password_hash, mentor['user_type'],
                  mentor['bio'], mentor['skills'], mentor['location'], datetime.now(), 1))
    
    conn.commit()
    conn.close()
    print(f"✅ Added {len(mentors)} mentors!")
    print("Mentor login password: MentorPass123!")

if __name__ == "__main__":
    populate_mentors()