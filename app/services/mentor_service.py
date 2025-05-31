from app.models.mentorship import Mentor, MentorshipRequest
from app import db

def get_all_mentors():
    """Fetch all mentors from the database."""
    return Mentor.query.all()

def create_mentorship_request(mentor_id, mentee_id):
    """Create a new mentorship request."""
    # Check if the mentor exists
    mentor = Mentor.query.get(mentor_id)
    if not mentor:
        raise ValueError('Mentor not found.')

    # Check if the mentee exists
    mentee = db.session.get(User, mentee_id)  # Assuming User is the model for mentees
    if not mentee:
        raise ValueError('Mentee not found.')

    # Check if a request already exists
    existing_request = MentorshipRequest.query.filter_by(
        mentor_id=mentor_id, mentee_id=mentee_id
    ).first()
    if existing_request:
        raise ValueError('A mentorship request already exists.')

    # Create the mentorship request
    new_request = MentorshipRequest(
        mentor_id=mentor_id,
        mentee_id=mentee_id,
        status='pending'
    )
    db.session.add(new_request)
    db.session.commit()