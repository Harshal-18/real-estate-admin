from app import db
from .base import BaseModel
from datetime import datetime

class Amenity(BaseModel):
    __tablename__ = 'amenities'
    
    amenity_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(20), nullable=False)
    icon_url = db.Column(db.String(500))
    description = db.Column(db.Text)
    is_rare = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    projects = db.relationship('Project', secondary='project_amenities', back_populates='amenities')

    def __repr__(self):
        return f'<Amenity {self.name}>'


class ProjectAmenity(BaseModel):
    __tablename__ = 'project_amenities'
    
    project_id = db.Column(db.Integer, db.ForeignKey('projects.project_id'), primary_key=True)
    amenity_id = db.Column(db.Integer, db.ForeignKey('amenities.amenity_id'), primary_key=True)
    is_available = db.Column(db.Boolean, default=True)
    description = db.Column(db.Text)
    area_size = db.Column(db.Numeric(10, 2))
    capacity = db.Column(db.Integer)
    operating_hours = db.Column(db.String(100))

    # Relationships
    project = db.relationship('Project', backref='project_amenity_assocs')
    amenity = db.relationship('Amenity', backref='project_amenity_assocs')

    def __repr__(self):
        return f'<ProjectAmenity {self.amenity.name} for {self.project.name}>'


class ProjectDocument(BaseModel):
    __tablename__ = 'project_documents'
    
    document_id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.project_id'), nullable=False)
    document_type = db.Column(db.String(20), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    file_url = db.Column(db.String(500), nullable=False)
    file_size = db.Column(db.BigInteger)
    file_type = db.Column(db.String(50))
    is_public = db.Column(db.Boolean, default=True)
    download_count = db.Column(db.Integer, default=0)

    # Relationship
    project = db.relationship('Project', back_populates='documents')

    def __repr__(self):
        return f'<ProjectDocument {self.title} of {self.project.name}>'


class Approval(BaseModel):
    __tablename__ = 'approvals'
    
    approval_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    is_mandatory = db.Column(db.Boolean, default=True)
    category = db.Column(db.String(20), default='legal')

    def __repr__(self):
        return f'<Approval {self.name}>'


class ProjectApproval(BaseModel):
    __tablename__ = 'project_approvals'
    
    project_id = db.Column(db.Integer, db.ForeignKey('projects.project_id'), primary_key=True)
    approval_id = db.Column(db.Integer, db.ForeignKey('approvals.approval_id'), primary_key=True)
    status = db.Column(db.String(20), default='pending')
    approval_number = db.Column(db.String(100))
    approval_date = db.Column(db.Date)
    expiry_date = db.Column(db.Date)
    issuing_authority = db.Column(db.String(255))
    document_url = db.Column(db.String(500))
    notes = db.Column(db.Text)

    # Relationships
    project = db.relationship('Project', backref='approval_assocs')
    approval = db.relationship('Approval', backref='project_approval_assocs')

    def __repr__(self):
        return f'<ProjectApproval {self.approval.name} for {self.project.name}>' 