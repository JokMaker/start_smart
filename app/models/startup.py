from app import db
from datetime import datetime

class Startup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    founder_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship with User (founder)
    founder = db.relationship('User', backref='founded_startups', lazy=True)

    # Relationship with StartupMember (members)
    members = db.relationship('StartupMember', backref='startup', lazy=True)

    def __repr__(self):
        return f'<Startup {self.name}>'

class StartupMember(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    startup_id = db.Column(db.Integer, db.ForeignKey('startup.id'), nullable=False)
    role = db.Column(db.String(50), nullable=False, default='Member')  # Founder/Member
    joined_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Define uniqueness constraint to prevent duplicate memberships
    __table_args__ = (
        db.UniqueConstraint('user_id', 'startup_id', name='unique_startup_membership'),
    )

    # Relationships
    user = db.relationship('User', backref='startup_memberships', lazy=True)

    def __repr__(self):
        return f'<StartupMember {self.user_id} -> {self.startup_id}>'