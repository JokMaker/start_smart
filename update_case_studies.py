import sqlite3

def update_case_studies():
    conn = sqlite3.connect('startsmart.db')
    c = conn.cursor()
    
    updates = [
        ("M-Pesa", "https://news.mit.edu/2016/mobile-money-kenyans-out-poverty-1208"),
        ("Flutterwave", "https://african.business/2021/03/technology-information/flutterwave-becomes-africas-fourth-1bn-unicorn"),
        ("Andela", "https://www.3blmedia.com/news/andela-launching-africas-tech-talent")
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
    update_case_studies()