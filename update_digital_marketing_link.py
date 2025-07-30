import sqlite3

def update_digital_marketing_link():
    conn = sqlite3.connect('startsmart.db')
    c = conn.cursor()
    
    # Update the digital marketing video with the correct link
    c.execute("""UPDATE resources 
                 SET external_url = ? 
                 WHERE title LIKE '%Digital Marketing%'""", 
             ('https://youtu.be/h95cQkEWBx0?si=iYiiqFRxD5EvI689',))
    
    conn.commit()
    
    # Verify the update
    c.execute("SELECT title, external_url FROM resources WHERE title LIKE '%Digital Marketing%'")
    result = c.fetchone()
    
    if result:
        print(f"✅ Updated: {result[0]}")
        print(f"🔗 New URL: {result[1]}")
    else:
        print("❌ Resource not found")
    
    conn.close()
    print("✅ Digital marketing video link updated successfully!")

if __name__ == "__main__":
    update_digital_marketing_link()