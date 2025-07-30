#!/usr/bin/env python3
"""Test profile route for debugging"""

import sqlite3
from datetime import datetime

def test_profile_route():
    """Test what happens when accessing profile"""
    print("Testing profile route...")
    
    conn = sqlite3.connect('startsmart.db')
    c = conn.cursor()
    
    # Get a student user
    c.execute("SELECT * FROM users WHERE user_type = 'student' LIMIT 1")
    user = c.fetchone()
    
    if not user:
        print("[ERROR] No student user found")
        return
    
    print(f"[INFO] Testing with user: {user[3]} ({user[1]})")
    print(f"[INFO] User data length: {len(user)}")
    
    # Test the applications query
    try:
        c.execute("""SELECT j.title, j.company, a.status, a.applied_at 
                     FROM applications a JOIN jobs j ON a.job_id = j.id 
                     WHERE a.user_id = ? ORDER BY a.applied_at DESC""", (user[0],))
        applications = c.fetchall()
        print(f"[INFO] Applications found: {len(applications)}")
        
        for app in applications:
            print(f"  - {app[0]} at {app[1]} ({app[2]})")
            
    except Exception as e:
        print(f"[ERROR] Applications query failed: {e}")
    
    # Test user data access by index
    try:
        print(f"[INFO] Testing user data access:")
        print(f"  user[0] (id): {user[0]}")
        print(f"  user[1] (email): {user[1]}")
        print(f"  user[3] (name): {user[3]}")
        print(f"  user[4] (user_type): {user[4]}")
        print(f"  user[5] (bio): {user[5]}")
        print(f"  user[6] (skills): {user[6]}")
        print(f"  user[7] (location): {user[7]}")
        print(f"  user[8] (resume_file): {user[8]}")
        print(f"  user[9] (profile_image): {user[9]}")
        
    except IndexError as e:
        print(f"[ERROR] Index error accessing user data: {e}")
        print(f"[INFO] User tuple length: {len(user)}")
        for i, val in enumerate(user):
            print(f"  [{i}]: {val}")
    
    conn.close()
    print("[SUCCESS] Profile test completed")

if __name__ == "__main__":
    test_profile_route()