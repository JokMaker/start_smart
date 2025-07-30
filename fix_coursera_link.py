import sqlite3

def fix_coursera_link():
    conn = sqlite3.connect('startsmart.db')
    c = conn.cursor()
    
    # Find the resource with Coursera link and update it
    c.execute("""UPDATE resources 
                 SET external_url = 'https://www.youtube.com/watch?v=9No-FiEInLA'
                 WHERE title LIKE '%Interview Skills%' AND external_url LIKE '%coursera%'""")
    
    # Also update any other problematic links to YouTube alternatives
    updates = [
        {
            'search': '%entrepreneur.com%',
            'new_url': 'https://www.youtube.com/watch?v=PMY_tdKJtjw',
            'title': 'startup funding'
        },
        {
            'search': '%zapier.com%',
            'new_url': 'https://www.youtube.com/watch?v=WA2eMbdkQFk',
            'title': 'remote work'
        },
        {
            'search': '%upwork.com%',
            'new_url': 'https://www.youtube.com/watch?v=1Ky_Vw5iQKs',
            'title': 'freelancing'
        }
    ]
    
    for update in updates:
        c.execute(f"""UPDATE resources 
                     SET external_url = ? 
                     WHERE external_url LIKE ?""", 
                 (update['new_url'], update['search']))
        print(f"✅ Updated {update['title']} link to YouTube")
    
    conn.commit()
    
    # Verify the changes
    c.execute("SELECT title, external_url FROM resources WHERE category = 'Videos'")
    videos = c.fetchall()
    
    print("\n📹 Updated Video Links:")
    for video in videos:
        print(f"  - {video[0]}")
        print(f"    🔗 {video[1]}")
    
    conn.close()
    print(f"\n✅ Fixed all problematic links!")

if __name__ == "__main__":
    fix_coursera_link()