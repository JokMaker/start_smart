"""
Debug authentication issues - capture exact error messages
"""
import requests
from bs4 import BeautifulSoup

def get_exact_error_messages():
    """Get the exact error messages from registration/login"""
    
    base_url = "https://start-smart.onrender.com"
    session = requests.Session()
    
    print("🔍 DEBUGGING EXACT ERROR MESSAGES...")
    
    # Test registration with detailed error capture
    print("\n1️⃣ Testing registration errors...")
    
    test_data = {
        'name': 'Debug Test',
        'email': 'debugtest@gmail.com',
        'password': 'DebugTest123!',
        'confirmPassword': 'DebugTest123!',
        'user_type': 'student'
    }
    
    try:
        response = session.post(f"{base_url}/register", data=test_data, timeout=30)
        
        if response.status_code == 200:
            # Try to parse HTML and find error messages
            try:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Look for common error message patterns
                error_patterns = [
                    {'class': 'alert-danger'},
                    {'class': 'error'},
                    {'class': 'text-danger'},
                    {'id': 'error'},
                ]
                
                errors_found = []
                for pattern in error_patterns:
                    elements = soup.find_all('div', pattern)
                    for elem in elements:
                        if elem.get_text().strip():
                            errors_found.append(elem.get_text().strip())
                
                if errors_found:
                    print("   Found error messages:")
                    for error in errors_found:
                        print(f"   - {error}")
                else:
                    print("   No visible error messages found in HTML")
                    
                # Check for form validation issues
                form = soup.find('form')
                if form:
                    print("   Form found - checking fields...")
                    inputs = form.find_all('input')
                    for inp in inputs:
                        if inp.get('required') and not inp.get('value'):
                            print(f"   - Required field missing: {inp.get('name', 'unknown')}")
                        
            except Exception as e:
                print(f"   Error parsing HTML: {e}")
                
        print(f"   Raw response length: {len(response.text)} chars")
        
    except Exception as e:
        print(f"   Registration test error: {e}")
    
    # Test login errors
    print("\n2️⃣ Testing login errors...")
    
    login_data = {
        'email': 'student@demo.com',
        'password': 'Demo123!'
    }
    
    try:
        response = session.post(f"{base_url}/login", data=login_data, timeout=30)
        
        if response.status_code == 200:
            try:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Look for error messages
                errors = soup.find_all('div', {'class': ['alert-danger', 'error', 'text-danger']})
                
                if errors:
                    print("   Login error messages found:")
                    for error in errors:
                        if error.get_text().strip():
                            print(f"   - {error.get_text().strip()}")
                else:
                    print("   No login error messages found")
                    
                # Check if we're still on login page
                title = soup.find('title')
                if title and 'login' in title.get_text().lower():
                    print("   Still on login page - login failed")
                elif title and 'dashboard' in title.get_text().lower():
                    print("   Redirected to dashboard - login succeeded!")
                    
            except Exception as e:
                print(f"   Error parsing login response: {e}")
                
    except Exception as e:
        print(f"   Login test error: {e}")

if __name__ == "__main__":
    try:
        from bs4 import BeautifulSoup
    except ImportError:
        print("Installing BeautifulSoup...")
        import subprocess
        subprocess.check_call(['pip', 'install', 'beautifulsoup4'])
        from bs4 import BeautifulSoup
    
    get_exact_error_messages()
