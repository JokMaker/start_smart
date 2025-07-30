import requests
import json

# Your Adzuna credentials
APP_ID = "cdd821aa"
APP_KEY = "5722fc56488bc8a2fda4165d2ee54ad5"

def test_adzuna_connection():
    """Test if Adzuna API works"""
    
    # Test URL for South Africa jobs
    url = f"https://api.adzuna.com/v1/api/jobs/za/search/1"
    
    params = {
        'app_id': APP_ID,
        'app_key': APP_KEY,
        'results_per_page': 5,
        'what': 'software',  # Search term
        'content-type': 'application/json'
    }
    
    try:
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API Connection Success!")
            print(f"Found {data['count']} jobs")
            
            # Show first job
            if data['results']:
                job = data['results'][0]
                print(f"\nSample Job:")
                print(f"Title: {job['title']}")
                print(f"Company: {job['company']['display_name']}")
                print(f"Location: {job['location']['display_name']}")
                
        else:
            print(f"❌ API Error: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"❌ Connection Error: {e}")

if __name__ == "__main__":
    if APP_ID == "your_app_id_here":
        print("⚠️ Please update APP_ID and APP_KEY with your actual credentials")
    else:
        test_adzuna_connection()