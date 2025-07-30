import sqlite3

def update_business_link():
    conn = sqlite3.connect('startsmart.db')
    c = conn.cursor()
    
    # Update the business startup video with the correct link
    c.execute("""UPDATE resources 
                 SET external_url = ? 
                 WHERE title = ?""", 
             ('https://youtu.be/l-IuHwgl3kE?si=NVYsDRmxrnDu1-XW', 
              'How to Start a Business in Africa - Complete Guide'))
    
    conn.commit()
    
    # Verify the update
    c.execute("SELECT title, external_url FROM resources WHERE title LIKE '%Business in Africa%'")
    result = c.fetchone()
    
    if result:
        print(f"✅ Updated: {result[0]}")
        print(f"🔗 New URL: {result[1]}")
    else:
        print("❌ Resource not found")
    
    conn.close()
    print("✅ Business startup video link updated successfully!")

if __name__ == "__main__":
    update_business_link()