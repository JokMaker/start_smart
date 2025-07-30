import sqlite3

def verify_video_links():
    conn = sqlite3.connect('startsmart.db')
    c = conn.cursor()
    
    # Get all video resources
    c.execute("SELECT title, description, external_url FROM resources WHERE category = 'Videos' ORDER BY title")
    videos = c.fetchall()
    
    print("🎥 Current Video Resources and Links:")
    print("=" * 60)
    
    for i, video in enumerate(videos, 1):
        title, description, url = video
        print(f"{i}. {title}")
        print(f"   Description: {description}")
        print(f"   Link: {url}")
        print(f"   Status: {'✅ Updated' if 'youtu.be' in url else '❌ Needs Update'}")
        print()
    
    conn.close()
    
    print("Please verify each link matches its title and description.")
    print("If any don't match, let me know which ones need to be corrected!")

if __name__ == "__main__":
    verify_video_links()