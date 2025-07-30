import sqlite3

def create_resources_table():
    conn = sqlite3.connect('startsmart.db')
    c = conn.cursor()
    
    # Create resources table
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
    conn.close()
    print("✅ Resources table created successfully!")

if __name__ == "__main__":
    create_resources_table()