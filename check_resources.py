import sqlite3

def check_resources():
    conn = sqlite3.connect('startsmart.db')
    c = conn.cursor()
    
    # Check if resources table exists
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='resources'")
    table_exists = c.fetchone()
    
    if not table_exists:
        print("❌ Resources table doesn't exist!")
        print("Creating resources table...")
        
        c.execute("""CREATE TABLE IF NOT EXISTS resources (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            category TEXT,
            file_url TEXT,
            external_url TEXT,
            uploaded_by INTEGER,
            created_at TIMESTAMP,
            view_count INTEGER DEFAULT 0,
            FOREIGN KEY (uploaded_by) REFERENCES users (id)
        )""")
        conn.commit()
        print("✅ Resources table created!")
    else:
        print("✅ Resources table exists")
    
    # Check resources count
    c.execute("SELECT COUNT(*) FROM resources")
    count = c.fetchone()[0]
    print(f"Resources in database: {count}")
    
    if count > 0:
        # Show sample resources
        c.execute("SELECT title, category FROM resources LIMIT 5")
        resources = c.fetchall()
        print("\nSample resources:")
        for resource in resources:
            print(f"  - {resource[0]} ({resource[1]})")
    
    # Check categories
    c.execute("SELECT DISTINCT category FROM resources WHERE category IS NOT NULL")
    categories = c.fetchall()
    print(f"\nCategories: {[cat[0] for cat in categories]}")
    
    conn.close()

if __name__ == "__main__":
    check_resources()