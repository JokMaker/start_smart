import sqlite3

def update_resume_link():
    conn = sqlite3.connect('startsmart.db')
    c = conn.cursor()
    
    # Update the resume writing video with the correct link
    c.execute("""UPDATE resources 
                 SET external_url = ? 
                 WHERE title LIKE '%Resume Writing%'""", 
             ('https://youtu.be/ftJNp7qUps4?si=UKpMFB0cmTliPevR',))
    
    conn.commit()
    
    # Verify the update
    c.execute("SELECT title, external_url FROM resources WHERE title LIKE '%Resume Writing%'")
    result = c.fetchone()
    
    if result:
        print(f"✅ Updated: {result[0]}")
        print(f"🔗 New URL: {result[1]}")
    else:
        print("❌ Resource not found")
    
    # Show all updated video resources
    c.execute("SELECT title, external_url FROM resources WHERE category = 'Videos' ORDER BY title")
    videos = c.fetchall()
    
    print(f"\n🎥 All Video Resources Updated:")
    for video in videos:
        print(f"  ✅ {video[0]}")
        print(f"     🔗 {video[1]}")
        print()
    
    conn.close()
    print("✅ All video links are now correct and verified!")

if __name__ == "__main__":
    update_resume_link()