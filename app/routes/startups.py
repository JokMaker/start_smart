from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.services.startup_service import get_all_startups, create_startup  # Example service functions
from app.models.startup import Startup

# Create a Blueprint for startup-related routes
startups = Blueprint('startups', __name__)

@startups.route('/startups')
def startup_listings():
    """Display a list of all startups."""
    startups = get_all_startups()  # Fetch startups from the database via the service layer
    return render_template('startups.html', startups=startups)

@startups.route('/startups/create', methods=['GET', 'POST'])
def create_startup_route():
    """Create a new startup."""
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        founder_id = request.form.get('founder_id')  # Assuming the logged-in user's ID is passed

        try:
            # Call the service function to create the startup
            create_startup(name=name, description=description, founder_id=founder_id)
            flash('Startup created successfully!', 'success')
            return redirect(url_for('startups.startup_listings'))
        except ValueError as e:
            flash(str(e), 'error')

    return render_template('create_startup.html')  # Template for creating a startup