from app.models.startup import Startup
from app import db

def get_all_startups():
    """Fetch all startups from the database."""
    return Startup.query.all()

def create_startup(name, description, founder_id):
    """Create a new startup."""
    # Check if the founder exists
    founder = db.session.get(User, founder_id)  # Assuming User is the model for founders
    if not founder:
        raise ValueError('Founder not found.')

    # Create the startup
    new_startup = Startup(
        name=name,
        description=description,
        founder_id=founder_id
    )
    db.session.add(new_startup)
    db.session.commit()