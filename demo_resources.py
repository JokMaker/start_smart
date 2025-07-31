#!/usr/bin/env python3
"""
StartSmart Enhanced Resources Demo
This script demonstrates the new dynamic resource system
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from resource_manager import resource_manager
import sqlite3

def demo_banner():
    """Display demo banner"""
    print("\n" + "="*60)
    print("🚀 STARTSMART ENHANCED RESOURCES SYSTEM DEMO")
    print("="*60)
    print("✨ Dynamic content matching for specified categories")
    print("🎯 Real templates, YouTube videos, and case studies")
    print("🌍 Focused on African entrepreneurship and careers")
    print("="*60)

def demo_templates():
    """Demonstrate template functionality"""
    print("\n📄 PROFESSIONAL TEMPLATES")
    print("-" * 40)
    
    categories = ['business', 'career', 'financial']
    
    for category in categories:
        templates = resource_manager.get_templates(category)
        print(f"\n🏷️  {category.title()} Templates ({len(templates)} available):")
        
        for i, template in enumerate(templates[:3], 1):
            print(f"   {i}. {template['title']}")
            print(f"      Type: {template['type']}")
            print(f"      Category: {template['category']}")
            print(f"      URL: {template['url'][:50]}...")
            print(f"      Description: {template['description'][:80]}...")
            print()

def demo_videos():
    """Demonstrate video functionality"""
    print("\n🎥 EDUCATIONAL VIDEOS")
    print("-" * 40)
    
    categories = ['business', 'career', 'tech']
    
    for category in categories:
        videos = resource_manager.get_youtube_videos(category, 3)
        print(f"\n🏷️  {category.title()} Videos ({len(videos)} available):")
        
        for i, video in enumerate(videos[:2], 1):
            print(f"   {i}. {video['title']}")
            print(f"      Channel: {video['channel']}")
            print(f"      Duration: {video['duration']}")
            print(f"      Views: {video['views']}")
            print(f"      Published: {video['published']}")
            print(f"      URL: {video['url'][:50]}...")
            print()

def demo_case_studies():
    """Demonstrate case studies"""
    print("\n📊 SUCCESS CASE STUDIES")
    print("-" * 40)
    
    case_studies = resource_manager.get_case_studies()
    print(f"\n🏷️  African Success Stories ({len(case_studies)} available):")
    
    for i, study in enumerate(case_studies, 1):
        print(f"   {i}. {study['title']}")
        print(f"      Category: {study['category']}")
        print(f"      Type: {study['type']}")
        print(f"      URL: {study['url'][:50]}...")
        print(f"      Description: {study['description'][:80]}...")
        print()

def demo_database_integration():
    """Demonstrate database integration"""
    print("\n💾 DATABASE INTEGRATION")
    print("-" * 40)
    
    conn = sqlite3.connect('startsmart.db')
    c = conn.cursor()
    
    # Show current state
    c.execute("SELECT category, COUNT(*) FROM resources GROUP BY category")
    categories = c.fetchall()
    
    print("\n📊 Current Resources in Database:")
    total = 0
    for category, count in categories:
        print(f"   • {category}: {count} items")
        total += count
    
    print(f"   📈 Total: {total} resources")
    
    # Show recent additions
    c.execute("""SELECT title, category, created_at FROM resources 
                 WHERE uploaded_by IS NULL 
                 ORDER BY created_at DESC LIMIT 5""")
    recent = c.fetchall()
    
    print(f"\n🆕 Recently Added Dynamic Content:")
    for title, category, created_at in recent:
        print(f"   • {title[:40]}... ({category})")
    
    conn.close()

def demo_features():
    """Demonstrate key features"""
    print("\n🎯 KEY FEATURES")
    print("-" * 40)
    
    features = [
        "📄 Real Professional Templates - Business plans, resumes, pitch decks",
        "🎥 YouTube Integration - African content creators and tutorials", 
        "📊 Success Case Studies - M-Pesa, Jumia, Flutterwave examples",
        "🔄 Automatic Refresh - Content updates dynamically",
        "🏷️  Smart Categorization - Templates, Videos, Case Studies, Guides",
        "🌍 African Focus - Content tailored for African professionals",
        "💾 Database Caching - Fast loading with local storage",
        "🔍 Search & Filter - Find exactly what you need",
        "📱 Mobile Responsive - Works on all devices",
        "👥 Community Upload - Users can contribute resources"
    ]
    
    for feature in features:
        print(f"   ✅ {feature}")

def demo_usage_examples():
    """Show practical usage examples"""
    print("\n📝 PRACTICAL USAGE EXAMPLES")
    print("-" * 40)
    
    examples = [
        {
            "scenario": "Student needs job application help",
            "solution": "Navigate to Templates → Career section",
            "result": "Access resume templates, cover letters, interview prep"
        },
        {
            "scenario": "Entrepreneur planning a startup",
            "solution": "Browse Templates → Business + Case Studies",
            "result": "Get business plan templates + learn from M-Pesa success"
        },
        {
            "scenario": "Professional skill development",
            "solution": "Watch Videos → Career or Tech categories", 
            "result": "Learn from African content creators and experts"
        },
        {
            "scenario": "Research successful African companies",
            "solution": "Read Case Studies section",
            "result": "Study Jumia, Flutterwave, Andela business models"
        }
    ]
    
    for i, example in enumerate(examples, 1):
        print(f"\n   🎬 Scenario {i}: {example['scenario']}")
        print(f"      🔧 Solution: {example['solution']}")
        print(f"      🎯 Result: {example['result']}")

def main():
    """Run the complete demo"""
    demo_banner()
    demo_templates()
    demo_videos() 
    demo_case_studies()
    demo_database_integration()
    demo_features()
    demo_usage_examples()
    
    print("\n" + "="*60)
    print("🎉 DEMO COMPLETED SUCCESSFULLY!")
    print("🚀 The enhanced resource system is ready for your assignment!")
    print("✨ Users will now get real, relevant content for each category")
    print("="*60)
    print("\n📌 Next Steps:")
    print("   1. Visit /resources to see the new interface")
    print("   2. Test different categories (Templates, Videos, Case Studies)")
    print("   3. Use the refresh button to update content") 
    print("   4. Upload community resources as a mentor")
    print("\n🌟 Your StartSmart platform now provides professional-grade resources!")

if __name__ == "__main__":
    main()
