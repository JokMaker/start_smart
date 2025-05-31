from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.services.auth_service import register_user, authenticate_user  # Example service functions
from app.models.user import User

# Create a Blueprint for authentication-related routes
auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    """Register a new user."""
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        try:
            # Call the service function to register the user
            register_user(username=username, email=email, password=password)
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('auth.login'))
        except ValueError as e:
            flash(str(e), 'error')

    return render_template('register.html')  # Template for user registration

@auth.route('/login', methods=['GET', 'POST'])
def login():
    """Log in an existing user."""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Call the service function to authenticate the user
        user = authenticate_user(email=email, password=password)
        if user:
            flash('Login successful!', 'success')
            return redirect(url_for('main.home'))  # Redirect to the homepage after login
        else:
            flash('Invalid email or password.', 'error')

    return render_template('login.html')  # Template for user login