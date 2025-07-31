"""
Debug registration validation issues
"""
import re

def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def sanitize_input(text):
    if text is None:
        return ''
    return str(text).strip()[:500]

def test_registration_validation():
    """Test the exact validation logic from app.py"""
    
    # Test data that's failing
    test_data = {
        'email': 'videotest2025@gmail.com',
        'password': 'VideoTest123!',
        'confirmPassword': 'VideoTest123!',
        'name': 'Video Test User',
        'user_type': 'student'
    }
    
    print("🧪 TESTING REGISTRATION VALIDATION LOGIC...")
    print("=" * 50)
    
    # Replicate exact validation from app.py
    email = sanitize_input(test_data['email']).lower().strip()
    password = test_data['password']
    confirm_password = test_data['confirmPassword']
    name = sanitize_input(test_data['name'])
    user_type = test_data['user_type']
    
    print(f"Email after sanitization: '{email}'")
    print(f"Name after sanitization: '{name}'")
    print(f"User type: '{user_type}'")
    
    errors = []
    
    # Name validation
    print(f"\n📝 Name validation:")
    print(f"   Name: '{name}' (length: {len(name.strip())})")
    if not name or len(name.strip()) < 2:
        errors.append('Please enter a valid full name (at least 2 characters)')
        print("   ❌ Name too short")
    elif len(name) > 100:
        errors.append('Name must be less than 100 characters')
        print("   ❌ Name too long")
    elif not re.match(r'^[a-zA-Z\s\'-\.]+$', name):
        errors.append('Name can only contain letters, spaces, hyphens, apostrophes, and periods')
        print("   ❌ Name contains invalid characters")
    else:
        print("   ✅ Name validation passed")
    
    # Email validation
    print(f"\n📧 Email validation:")
    print(f"   Email: '{email}'")
    if not email:
        errors.append('Email address is required')
        print("   ❌ Email is empty")
    elif not validate_email(email):
        errors.append('Please enter a valid email address')
        print("   ❌ Email format invalid")
    elif len(email) > 254:
        errors.append('Email address is too long')
        print("   ❌ Email too long")
    else:
        print("   ✅ Email validation passed")
    
    # Password validation
    print(f"\n🔒 Password validation:")
    print(f"   Password length: {len(password)}")
    if not password:
        errors.append('Password is required')
        print("   ❌ Password is empty")
    elif len(password) < 8:
        errors.append('Password must be at least 8 characters long')
        print("   ❌ Password too short")
    elif len(password) > 128:
        errors.append('Password must be less than 128 characters')
        print("   ❌ Password too long")
    else:
        # Advanced password strength validation
        password_checks = {
            'lowercase': re.search(r"[a-z]", password),
            'uppercase': re.search(r"[A-Z]", password),
            'digit': re.search(r"\d", password),
            'special': re.search(r"[@$!%*?&#^()_+=\-\[\]{}|\\:;\"'<>,.?/~`]", password)
        }
        
        missing_requirements = []
        if not password_checks['lowercase']:
            missing_requirements.append('lowercase letter')
        if not password_checks['uppercase']:
            missing_requirements.append('uppercase letter')
        if not password_checks['digit']:
            missing_requirements.append('number')
        if not password_checks['special']:
            missing_requirements.append('special character')
        
        if missing_requirements:
            errors.append(f'Password must contain at least one: {", ".join(missing_requirements)}')
            print(f"   ❌ Password missing: {', '.join(missing_requirements)}")
        else:
            print("   ✅ Password strength validation passed")
    
    # Password confirmation
    print(f"\n🔄 Password confirmation:")
    if password != confirm_password:
        errors.append('Passwords do not match')
        print("   ❌ Passwords do not match")
    else:
        print("   ✅ Password confirmation passed")
    
    # User type validation
    print(f"\n👤 User type validation:")
    print(f"   User type: '{user_type}'")
    valid_user_types = ['student', 'mentor', 'recruiter']
    if user_type not in valid_user_types:
        errors.append('Please select a valid user type')
        print(f"   ❌ Invalid user type. Valid types: {valid_user_types}")
    else:
        print("   ✅ User type validation passed")
    
    # Final result
    print(f"\n📊 VALIDATION RESULTS:")
    if errors:
        print("❌ VALIDATION FAILED:")
        for error in errors:
            print(f"   - {error}")
        return False
    else:
        print("✅ ALL VALIDATION PASSED!")
        return True

if __name__ == "__main__":
    test_registration_validation()
