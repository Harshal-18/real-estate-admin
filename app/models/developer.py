from datetime import datetime
from app import db
from sqlalchemy.orm import relationship

class Developer(db.Model):
    __tablename__ = 'developers'

    developer_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    established_year = db.Column(db.Integer)
    description = db.Column(db.Text)
    logo_url = db.Column(db.String(500))
    website_url = db.Column(db.String(500))
    contact_email = db.Column(db.String(255))
    contact_phone = db.Column(db.String(20))
    address = db.Column(db.Text)
    total_projects = db.Column(db.Integer, default=0)
    completed_projects = db.Column(db.Integer, default=0)
    ongoing_projects = db.Column(db.Integer, default=0)
    rating = db.Column(db.Float, default=0.00)
    total_reviews = db.Column(db.Integer, default=0)
    is_verified = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    projects = db.relationship('Project', backref='developer', lazy=True)

    def __repr__(self):
        return f'<Developer {self.name}>'

    def to_dict(self):
        """Convert the model instance to a dictionary"""
        return {
            'developer_id': self.developer_id,
            'name': self.name,
            'established_year': self.established_year,
            'description': self.description,
            'logo_url': self.logo_url,
            'website_url': self.website_url,
            'contact_email': self.contact_email,
            'contact_phone': self.contact_phone,
            'address': self.address,
            'total_projects': self.total_projects,
            'completed_projects': self.completed_projects,
            'ongoing_projects': self.ongoing_projects,
            'rating': float(self.rating) if self.rating else 0.0,
            'total_reviews': self.total_reviews,
            'is_verified': self.is_verified,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

    def update_from_dict(self, data):
        """Update the model instance from a dictionary"""
        for field in ['name', 'established_year', 'description', 'logo_url', 
                     'website_url', 'contact_email', 'contact_phone', 'address',
                     'total_projects', 'completed_projects', 'ongoing_projects',
                     'rating', 'total_reviews', 'is_verified']:
            if field in data:
                setattr(self, field, data[field])

    def update_project_counts(self):
        """Update project counts based on their status"""
        from .project import Project
        
        self.total_projects = Project.query.filter_by(developer_id=self.developer_id).count()
        self.completed_projects = Project.query.filter_by(
            developer_id=self.developer_id, 
            status='completed'
        ).count()
        self.ongoing_projects = Project.query.filter_by(
            developer_id=self.developer_id, 
            status='under_construction'
        ).count()
        db.session.commit()

    def validate(self):
        """Validate developer data"""
        errors = []
        
        # Validate established_year
        if self.established_year:
            current_year = datetime.now().year
            if self.established_year < 1800 or self.established_year > current_year:
                errors.append(f'Established year must be between 1800 and {current_year}')
        
        # Validate rating
        if self.rating is not None and (self.rating < 0 or self.rating > 5):
            errors.append('Rating must be between 0 and 5')
        
        # Validate email format
        if self.contact_email and '@' not in self.contact_email:
            errors.append('Invalid email format')
        
        # Validate phone format (basic validation)
        if self.contact_phone and not self.contact_phone.replace('+', '').replace('-', '').isdigit():
            errors.append('Invalid phone number format')
        
        return errors 