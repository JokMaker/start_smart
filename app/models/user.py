from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)  # Hashed password
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True, nullable=False)  # Active status

    # Relationships
    jobs = db.relationship('JobApplication', backref='user', lazy=True)
    mentor_profile = db.relationship('Mentor', backref='user', lazy=True)
    mentorship_requests = db.relationship('MentorshipRequest', backref='mentee', lazy=True)
    startups = db.relationship('StartupMember', backref='user', lazy=True)

    def set_password(self, password):
        """Hash and store the password."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Verify the password against the stored hash."""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'