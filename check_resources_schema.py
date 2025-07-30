import sqlite3

def check_resources_schema():
    """Check the resources table schema and current video data"""
    
    conn = sqlite3.connect('startsmart.db')
    c = conn.cursor()
    
    # Get table schema
    c.execute("PRAGMA table_info(resources)")
    columns = c.fetchall()
    print("Resources table columns:")
    for col in columns:
        print(f"  {col[1]} ({col[2]})")
    
    print("\nCurrent video resources:")
    c.execute("SELECT id, title, external_url FROM resources WHERE category = 'Videos'")
    videos = c.fetchall()
    for video in videos:
        print(f"  ID: {video[0]} | Title: {video[1]} | URL: {video[2]}")
    
    conn.close()

if __name__ == "__main__":
    check_resources_schema()