from app.models.job import Job
from app import db

def get_all_jobs():
    """Fetch all jobs from the database."""
    return Job.query.all()

def create_job(title, company, location, description):
    """Create a new job listing."""
    new_job = Job(
        title=title,
        company=company,
        location=location,
        description=description
    )
    db.session.add(new_job)
    db.session.commit()