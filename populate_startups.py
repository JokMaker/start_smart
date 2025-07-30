import sqlite3
from datetime import datetime

def populate_startups():
    conn = sqlite3.connect('startsmart.db')
    c = conn.cursor()
    
    # Sample startups data
    startups = [
        {
            'name': 'EcoFarm Solutions',
            'description': 'Revolutionizing agriculture in Africa through smart farming technology and sustainable practices. We help farmers increase yields while protecting the environment.',
            'industry': 'AgriTech',
            'founder_id': 1,
            'stage': 'Seed',
            'location': 'Nairobi, Kenya',
            'website': 'https://ecofarm-solutions.com',
            'team_size': 8
        },
        {
            'name': 'HealthConnect Africa',
            'description': 'Telemedicine platform connecting patients with healthcare professionals across rural and urban Africa. Making healthcare accessible to everyone.',
            'industry': 'HealthTech',
            'founder_id': 1,
            'stage': 'Series A',
            'location': 'Lagos, Nigeria',
            'website': 'https://healthconnect-africa.com',
            'team_size': 15
        },
        {
            'name': 'EduTech Rwanda',
            'description': 'Digital learning platform providing quality education content in local languages. Empowering students across Rwanda with technology.',
            'industry': 'EdTech',
            'founder_id': 1,
            'stage': 'Pre-Seed',
            'location': 'Kigali, Rwanda',
            'website': 'https://edutech-rwanda.com',
            'team_size': 5
        },
        {
            'name': 'FinPay Ghana',
            'description': 'Mobile payment solution for small businesses and individuals. Making financial transactions simple and secure across West Africa.',
            'industry': 'FinTech',
            'founder_id': 1,
            'stage': 'Seed',
            'location': 'Accra, Ghana',
            'website': 'https://finpay-ghana.com',
            'team_size': 12
        },
        {
            'name': 'GreenEnergy SA',
            'description': 'Solar energy solutions for homes and businesses in South Africa. Providing clean, affordable energy to communities.',
            'industry': 'CleanTech',
            'founder_id': 1,
            'stage': 'Series A',
            'location': 'Cape Town, South Africa',
            'website': 'https://greenenergy-sa.com',
            'team_size': 20
        },
        {
            'name': 'LogiTrack East Africa',
            'description': 'Supply chain and logistics optimization platform for businesses across East Africa. Streamlining operations and reducing costs.',
            'industry': 'LogTech',
            'founder_id': 1,
            'stage': 'Seed',
            'location': 'Kampala, Uganda',
            'website': 'https://logitrack-ea.com',
            'team_size': 10
        }
    ]
    
    for startup in startups:
        c.execute("""INSERT INTO startups 
                  (name, description, industry, founder_id, created_at)
                  VALUES (?, ?, ?, ?, ?)""",
                 (startup['name'], startup['description'], startup['industry'], 
                  startup['founder_id'], datetime.now()))
    
    conn.commit()
    conn.close()
    print(f"✅ Added {len(startups)} startups!")

if __name__ == "__main__":
    populate_startups()