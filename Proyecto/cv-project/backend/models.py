from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Profile(db.Model):
    __tablename__ = 'profiles'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    summary = db.Column(db.Text, nullable=False)
    photo_filename = db.Column(db.String(120), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    experiences = db.relationship('Experience', backref='profile', lazy=True, cascade='all, delete-orphan')
    educations = db.relationship('Education', backref='profile', lazy=True, cascade='all, delete-orphan')
    skills = db.relationship('Skill', backref='profile', lazy=True, cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'title': self.title,
            'email': self.email,
            'phone': self.phone,
            'location': self.location,
            'summary': self.summary,
            'photo_filename': self.photo_filename,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class Experience(db.Model):
    __tablename__ = 'experiences'
    
    id = db.Column(db.Integer, primary_key=True)
    profile_id = db.Column(db.Integer, db.ForeignKey('profiles.id'), nullable=False)
    company = db.Column(db.String(200), nullable=False)
    position = db.Column(db.String(200), nullable=False)
    period = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    responsibilities = db.Column(db.JSON, nullable=False)  # Store as JSON array
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'company': self.company,
            'position': self.position,
            'period': self.period,
            'location': self.location,
            'responsibilities': self.responsibilities,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Education(db.Model):
    __tablename__ = 'educations'
    
    id = db.Column(db.Integer, primary_key=True)
    profile_id = db.Column(db.Integer, db.ForeignKey('profiles.id'), nullable=False)
    institution = db.Column(db.String(200), nullable=False)
    degree = db.Column(db.String(200), nullable=False)
    period = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'institution': self.institution,
            'degree': self.degree,
            'period': self.period,
            'location': self.location,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Skill(db.Model):
    __tablename__ = 'skills'
    
    id = db.Column(db.Integer, primary_key=True)
    profile_id = db.Column(db.Integer, db.ForeignKey('profiles.id'), nullable=False)
    category = db.Column(db.String(100), nullable=False)  # programming_languages, frontend, backend, etc.
    skills_list = db.Column(db.JSON, nullable=False)  # Store as JSON array
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'category': self.category,
            'skills_list': self.skills_list,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class ScanHistory(db.Model):
    __tablename__ = 'scan_history'
    
    id = db.Column(db.Integer, primary_key=True)
    target = db.Column(db.String(50), nullable=False)
    port_range = db.Column(db.String(20), nullable=False)
    scan_results = db.Column(db.JSON, nullable=False)  # Store complete scan results as JSON
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    duration = db.Column(db.Float)  # Scan duration in seconds
    
    def to_dict(self):
        return {
            'id': self.id,
            'target': self.target,
            'port_range': self.port_range,
            'scan_results': self.scan_results,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'duration': self.duration
        }

class DonationHistory(db.Model):
    __tablename__ = 'donation_history'
    
    id = db.Column(db.Integer, primary_key=True)
    stripe_session_id = db.Column(db.String(200), nullable=False, unique=True)
    amount = db.Column(db.Integer, nullable=False)  # Amount in cents
    currency = db.Column(db.String(3), default='usd')
    status = db.Column(db.String(20), nullable=False)  # pending, completed, failed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    
    def to_dict(self):
        return {
            'id': self.id,
            'stripe_session_id': self.stripe_session_id,
            'amount': self.amount,
            'currency': self.currency,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None
        }
