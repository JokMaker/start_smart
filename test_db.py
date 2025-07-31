import sqlite3
import traceback
from flask import Flask

app = Flask(__name__)

@app.route('/')
def test():
    try:
        print("Testing database...")
        conn = sqlite3.connect('startsmart.db')
        c = conn.cursor()
        
        # List all tables
        c.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = c.fetchall()
        print(f"Tables: {tables}")
        
        # Test users table
        c.execute("SELECT COUNT(*) FROM users")
        user_count = c.fetchone()[0]
        print(f"Users: {user_count}")
        
        # Test a simple select
        c.execute("SELECT * FROM users LIMIT 1")
        sample_user = c.fetchone()
        print(f"Sample user: {sample_user}")
        
        conn.close()
        return f"Database working! {user_count} users, Tables: {[t[0] for t in tables]}"
        
    except Exception as e:
        print(f"ERROR: {e}")
        traceback.print_exc()
        return f"Error: {e}", 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
