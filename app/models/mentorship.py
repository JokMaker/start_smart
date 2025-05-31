from app import db
from datetime import datetime

class Mentor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    expertise = db.Column(db.String(100), nullable=False)

    # Relationship with User
    user = db.relationship('User', backref='mentor_profile', lazy=True)

    def __repr__(self):
        return f'<Mentor {self.user_id}>'

class MentorshipRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mentor_id = db.Column(db.Integer, db.ForeignKey('mentor.id'), nullable=False)
    mentee_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending/accepted/rejected
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Define uniqueness constraint to prevent duplicate requests
    __table_args__ = (
        db.UniqueConstraint('mentor_id', 'mentee_id', name='unique_mentorship_request'),
    )

    # Relationships
    mentor = db.relationship('Mentor', backref='requests', lazy=True)
    mentee = db.relationship('User', backref='mentorship_requests', lazy=True)

    def __repr__(self):
        return f'<MentorshipRequest {self.mentor_id} -> {self.mentee_id}>'