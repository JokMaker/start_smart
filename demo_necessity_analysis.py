#!/usr/bin/env python3
"""
Demo Data Assessment for StartSmart
This script analyzes what demo data is necessary vs optional
"""

import sqlite3

def analyze_demo_necessity():
    """Analyze what demo data is necessary for the platform"""
    print("🔍 Demo Data Necessity Analysis")
    print("=" * 50)
    
    conn = sqlite3.connect('startsmart.db')
    c = conn.cursor()
    
    print("\n📊 CURRENT DEMO DATA:")
    
    # Demo Users
    c.execute("SELECT name, email, user_type FROM users WHERE email LIKE '%@startsmart.com' OR email LIKE '%@techcorp.com' OR email LIKE '%@startup.co' OR email LIKE '%@example.com'")
    demo_users = c.fetchall()
    print(f"\n👥 Demo Users ({len(demo_users)}):")
    for user in demo_users:
        print(f"  - {user[0]} ({user[1]}) - {user[2]}")
    
    # Demo Jobs
    c.execute("SELECT title, company, location FROM jobs")
    demo_jobs = c.fetchall()
    print(f"\n💼 Demo Jobs ({len(demo_jobs)}):")
    for job in demo_jobs:
        print(f"  - {job[0]} at {job[1]} ({job[2]})")
    
    # Demo Startups
    c.execute("SELECT name, founder, industry FROM startups")
    demo_startups = c.fetchall()
    print(f"\n🏢 Demo Startups ({len(demo_startups)}):")
    for startup in demo_startups:
        print(f"  - {startup[0]} by {startup[1]} ({startup[2]})")
    
    # Demo Skills
    c.execute("SELECT COUNT(*) FROM skills")
    skills_count = c.fetchone()[0]
    print(f"\n🛠️ Demo Skills: {skills_count} skills")
    
    conn.close()

def assess_necessity():
    """Assess what's necessary vs optional"""
    print("\n" + "=" * 50)
    print("📋 NECESSITY ASSESSMENT")
    print("=" * 50)
    
    print("\n✅ ABSOLUTELY NECESSARY (Keep):")
    print("  🔐 Authentication System - Required for login/registration")
    print("  📊 Database Schema - Required for app functionality")
    print("  🏗️ Table Structure - Required for data storage")
    print("  🔧 Core Application Logic - Required for features")
    
    print("\n🤔 DEMO DATA (Optional - Can Remove):")
    print("  👤 Demo Users (Admin, Alice, Bob, Sarah) - Only for testing")
    print("  💼 Demo Jobs (4 sample jobs) - Only for display purposes")
    print("  🏢 Demo Startups (3 sample startups) - Only for homepage")
    print("  🛠️ Demo Skills (18 skills) - Useful but not critical")
    
    print("\n⚖️ PROS & CONS OF KEEPING DEMO DATA:")
    
    print("\n✅ PROS of Keeping Demo Data:")
    print("  - Homepage looks populated and professional")
    print("  - Students can see example jobs immediately")
    print("  - Platform doesn't look empty to new visitors")
    print("  - Good for demonstrations and presentations")
    print("  - Shows the platform's capabilities")
    
    print("\n❌ CONS of Keeping Demo Data:")
    print("  - Takes up database space")
    print("  - Might confuse real users")
    print("  - Demo jobs aren't real opportunities")
    print("  - May need maintenance/updates")

def provide_recommendation():
    """Provide recommendation on demo data"""
    print("\n" + "=" * 50)
    print("💡 RECOMMENDATION")
    print("=" * 50)
    
    print("\n🎯 FOR YOUR ASSIGNMENT SUBMISSION:")
    print("  ✅ KEEP demo data - makes platform look professional")
    print("  ✅ Shows functionality without requiring real data")
    print("  ✅ Demonstrates all features working")
    print("  ✅ Good for grading/evaluation purposes")
    
    print("\n🚀 FOR PRODUCTION DEPLOYMENT:")
    print("  ⚠️ CONSIDER removing demo users (keep 1 admin)")
    print("  ⚠️ CONSIDER removing demo jobs (or mark as samples)")
    print("  ✅ KEEP skills - useful for real users")
    print("  ✅ KEEP database structure - essential")
    
    print("\n🔄 EASY TO REMOVE LATER:")
    print("  - Demo data can be removed anytime with simple DELETE queries")
    print("  - Real user functionality won't be affected")
    print("  - Database structure remains intact")

def show_removal_option():
    """Show how to remove demo data if needed"""
    print("\n" + "=" * 50)
    print("🗑️ HOW TO REMOVE DEMO DATA (IF NEEDED)")
    print("=" * 50)
    
    print("\n📝 SQL Commands to Remove Demo Data:")
    print("  -- Remove demo users (keep real registrations)")
    print("  DELETE FROM users WHERE email LIKE '%@startsmart.com';")
    print("  DELETE FROM users WHERE email LIKE '%@techcorp.com';")
    print("  DELETE FROM users WHERE email LIKE '%@startup.co';")
    print("  DELETE FROM users WHERE email LIKE '%example.com';")
    print()
    print("  -- Remove demo jobs")
    print("  DELETE FROM jobs WHERE posted_by IN (SELECT id FROM users WHERE email LIKE '%@techcorp.com');")
    print()
    print("  -- Remove demo startups")
    print("  DELETE FROM startups WHERE founder IN ('John Kemboi', 'Amina Hassan', 'David Ochieng');")
    print()
    print("  ⚠️ Note: Keep skills as they're useful for real users")

def main():
    """Main assessment function"""
    analyze_demo_necessity()
    assess_necessity()
    provide_recommendation()
    show_removal_option()
    
    print("\n" + "=" * 50)
    print("🎯 BOTTOM LINE:")
    print("  For your assignment: KEEP everything - it looks professional")
    print("  For real production: You can remove demo data later easily")
    print("  The authentication system is what really matters!")
    print("=" * 50)

if __name__ == "__main__":
    main()
