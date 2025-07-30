import sqlite3

def update_applications_table():
    conn = sqlite3.connect('startsmart.db')
    c = conn.cursor()
    
    # Add new columns to applications table
    try:
        c.execute("ALTER TABLE applications ADD COLUMN cover_letter TEXT")
        print("✅ Added cover_letter column")
    except sqlite3.OperationalError:
        print("cover_letter column already exists")
    
    try:
        c.execute("ALTER TABLE applications ADD COLUMN relevant_experience TEXT")
        print("✅ Added relevant_experience column")
    except sqlite3.OperationalError:
        print("relevant_experience column already exists")
    
    try:
        c.execute("ALTER TABLE applications ADD COLUMN portfolio_url TEXT")
        print("✅ Added portfolio_url column")
    except sqlite3.OperationalError:
        print("portfolio_url column already exists")
    
    conn.commit()
    conn.close()
    print("Database updated successfully!")

if __name__ == "__main__":
    update_applications_table()