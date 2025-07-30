import sqlite3

def update_all_video_links():
    """Update all video resource links with correct YouTube URLs"""
    
    conn = sqlite3.connect('startsmart.db')
    c = conn.cursor()
    
    # Updated video links mapping - using partial title matching
    video_updates = [
        ("How to Start a Business in Africa", "https://youtu.be/l-IuHwgl3kE?si=NVYsDRmxrnDu1-XW"),
        ("Job Interview Skills", "https://youtu.be/uQEuo7woEEk?si=w_ua0cpnP9Sa6w5V"),
        ("Digital Marketing", "https://youtu.be/h95cQkEWBx0?si=iYiiqFRxD5EvI689"),
        ("Resume Writing Workshop", "https://youtu.be/ftJNp7qUps4?si=UKpMFB0cmTliPevR")
    ]
    
    updated_count = 0
    
    for title_part, new_url in video_updates:
        c.execute("UPDATE resources SET external_url = ? WHERE title LIKE ? AND category = 'Videos'", 
                 (new_url, f"%{title_part}%"))
        if c.rowcount > 0:
            updated_count += 1
            print(f"Updated: {title_part}")
        else:
            print(f"Not found: {title_part}")
    
    conn.commit()
    conn.close()
    
    print(f"\nUpdated {updated_count} video links successfully!")

if __name__ == "__main__":
    update_all_video_links()