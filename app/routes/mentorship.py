from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.services.mentor_service import get_all_mentors, create_mentorship_request  # Example service functions
from app.models.mentorship import Mentor, MentorshipRequest

# Create a Blueprint for mentorship-related routes
mentorship = Blueprint('mentorship', __name__)

@mentorship.route('/mentors')
def mentor_listings():
    """Display a list of all mentors."""
    mentors = get_all_mentors()  # Fetch mentors from the database via the service layer
    return render_template('mentors.html', mentors=mentors)

@mentorship.route('/mentorship/request/<int:mentor_id>', methods=['POST'])
def request_mentorship(mentor_id):
    """Submit a mentorship request."""
    mentee_id = request.form.get('mentee_id')  # Assuming the logged-in user's ID is passed

    try:
        # Call the service function to create the mentorship request
        create_mentorship_request(mentor_id=mentor_id, mentee_id=mentee_id)
        flash('Mentorship request submitted!', 'success')
    except ValueError as e:
        flash(str(e), 'error')

    return redirect(url_for('mentorship.mentor_listings'))