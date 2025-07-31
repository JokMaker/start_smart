"""
Email Verification System for StartSmart
Add this to handle real email verification
"""
import secrets
from datetime import datetime, timedelta
from flask_mail import Message

def generate_verification_token():
    """Generate secure verification token"""
    return secrets.token_urlsafe(32)

def send_verification_email(user_email, user_name, token):
    """Send email verification"""
    verification_url = f"https://start-smart.onrender.com/verify-email/{token}"
    
    subject = "Verify Your StartSmart Account"
    body = f"""
Dear {user_name},

Welcome to StartSmart! Please verify your email address by clicking the link below:

{verification_url}

This link will expire in 24 hours.

If you didn't create this account, please ignore this email.

Best regards,
The StartSmart Team
"""
    
    # Send email (when email system is configured)
    try:
        msg = Message(subject, recipients=[user_email], body=body)
        mail.send(msg)
        return True
    except Exception as e:
        print(f"Email verification failed: {e}")
        return False

def add_verification_to_registration():
    """Modified registration with email verification"""
    # In your registration route, add:
    
    # 1. Create user as INACTIVE
    # is_active = 0, email_verified = 0
    
    # 2. Generate verification token
    # token = generate_verification_token()
    
    # 3. Store token in database with expiry
    # verification_tokens table
    
    # 4. Send verification email
    # send_verification_email(email, name, token)
    
    # 5. Show message: "Check your email to verify account"
    pass
