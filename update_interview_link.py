import sqlite3

def update_interview_link():
    conn = sqlite3.connect('startsmart.db')
    c = conn.cursor()
    
    # Update the interview skills video with the correct link
    c.execute("""UPDATE resources 
                 SET external_url = ? 
                 WHERE title LIKE '%Interview Skills%'""", 
             ('https://youtu.be/uQEuo7woEEk?si=w_ua0cpnP9Sa6w5V',))
    
    conn.commit()
    
    # Verify the update
    c.execute("SELECT title, external_url FROM resources WHERE title LIKE '%Interview Skills%'")
    result = c.fetchone()
    
    if result:
        print(f"✅ Updated: {result[0]}")
        print(f"🔗 New URL: {result[1]}")
    else:
        print("❌ Resource not found")
    
    conn.close()
    print("✅ Interview skills video link updated successfully!")

if __name__ == "__main__":
    update_interview_link()