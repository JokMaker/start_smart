import sqlite3

def update_additional_links():
    conn = sqlite3.connect('startsmart.db')
    c = conn.cursor()
    
    updates = [
        ("Startup Funding Guide", "https://carta.com/learn/startups/fundraising/series-a/"),
        ("Remote Work Setup Guide", "https://remote4africa.com/blog/how-african-professionals-can-build-a-thriving-remote-career/")
    ]
    
    for title_part, new_url in updates:
        c.execute("UPDATE resources SET external_url = ? WHERE title LIKE ?", 
                 (new_url, f"%{title_part}%"))
        if c.rowcount > 0:
            print(f"Updated: {title_part}")
        else:
            print(f"Not found: {title_part}")
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    update_additional_links()