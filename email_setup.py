import sqlite3
from datetime import datetime

def add_password_reset_table():
    """Add password reset tokens table"""
    conn = sqlite3.connect('startsmart.db')
    c = conn.cursor()
    
    c.execute('''CREATE TABLE IF NOT EXISTS password_reset_tokens (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        token TEXT UNIQUE NOT NULL,
        expires_at TIMESTAMP NOT NULL,
        used INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )''')
    
    conn.commit()
    conn.close()
    print("Password reset table created successfully!")

if __name__ == "__main__":
    add_password_reset_table()