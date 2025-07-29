from app import db
from .base import BaseModel
from datetime import datetime

class ProjectMedia(BaseModel):
    __tablename__ = 'project_media'
    
    media_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.project_id'), nullable=False)
    media_type = db.Column(db.String(20), nullable=False)  # image, video, virtual_tour, floor_plan, master_plan
    media_url = db.Column(db.String(500), nullable=False)
    thumbnail_url = db.Column(db.String(500))
    title = db.Column(db.String(255))
    description = db.Column(db.Text)
    media_category = db.Column(db.String(20), default='exterior')  # exterior, interior, amenities, views, construction, location
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship
    project = db.relationship('Project', back_populates='media')

    def __repr__(self):
        return f'<ProjectMedia {self.title} of {self.project.name}>'

    @property
    def media_info(self):
        """Return formatted media information"""
        return {
            'id': self.media_id,
            'type': self.media_type,
            'url': self.media_url,
            'thumbnail': self.thumbnail_url,
            'title': self.title,
            'category': self.media_category,
            'description': self.description,
            'is_active': self.is_active
        }

    @property
    def image_path(self):
        from flask import url_for
        return url_for('static', filename='uploads/' + self.media_url)

    def update_status(self, status: bool):
        """Update the active status of the media"""
        self.is_active = status
        db.session.commit()

    @classmethod
    def get_project_media(cls, project_id: int, media_type: str = None, category: str = None):
        """Get all media for a project with optional filters"""
        query = cls.query.filter_by(project_id=project_id)
        
        if media_type:
            query = query.filter_by(media_type=media_type)
        
        if category:
            query = query.filter_by(media_category=category)
            
        return query.filter_by(is_active=True).all() 