from app import db
from datetime import datetime

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    company = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)  # Added location field
    description = db.Column(db.Text, nullable=False)      # Added description field
    application_deadline = db.Column(db.DateTime, nullable=True)  # Optional deadline
    posted_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship with JobApplication
    applications = db.relationship('JobApplication', backref='job', lazy=True)

class JobApplication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'), nullable=False)
    applied_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Define uniqueness constraint to prevent duplicate applications
    __table_args__ = (
        db.UniqueConstraint('user_id', 'job_id', name='unique_application'),
    )

    # Relationships
    user = db.relationship('User', backref='applications', lazy=True)