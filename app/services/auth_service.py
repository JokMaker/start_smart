from app.models.user import User
from werkzeug.security import generate_password_hash, check_password_hash
from app import db

def register_user(username, email, password):
    """Register a new user."""
    # Check if the email is already registered
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        raise ValueError('Email already registered.')

    # Hash the password and create a new user
    password_hash = generate_password_hash(password)
    new_user = User(username=username, email=email, password_hash=password_hash)
    db.session.add(new_user)
    db.session.commit()

def authenticate_user(email, password):
    """Authenticate a user by email and password."""
    user = User.query.filter_by(email=email).first()
    if user and check_password_hash(user.password_hash, password):
        return user
    return None