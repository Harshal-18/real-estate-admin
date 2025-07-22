from app import db
from .base import BaseModel
from sqlalchemy.orm import validates
from decimal import Decimal

class Project(BaseModel):
    __tablename__ = 'projects'
    
    project_id = db.Column(db.Integer, primary_key=True)
    developer_id = db.Column(db.Integer, db.ForeignKey('developers.developer_id'), nullable=False)
    locality_id = db.Column(db.Integer, db.ForeignKey('localities.locality_id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    project_type = db.Column(db.String(20), default='residential')
    property_type = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(30), nullable=False)
    
    # Project Details
    total_land_area = db.Column(db.Numeric(10, 2))  # in acres
    total_units = db.Column(db.Integer)
    unit_density = db.Column(db.Numeric(8, 2))  # units per acre
    open_area_percentage = db.Column(db.Numeric(5, 2))
    park_area = db.Column(db.Numeric(8, 2))  # in acres
    clubhouse_area = db.Column(db.Numeric(10, 2))  # in sq ft
    
    # Pricing
    min_price = db.Column(db.Numeric(15, 2))
    max_price = db.Column(db.Numeric(15, 2))
    price_per_sqft = db.Column(db.Numeric(10, 2))
    currency = db.Column(db.String(10), default='INR')
    
    # Timeline
    launch_date = db.Column(db.Date)
    possession_date = db.Column(db.Date)
    completion_date = db.Column(db.Date)
    
    # Location specifics
    address = db.Column(db.Text)
    latitude = db.Column(db.Numeric(10, 8))
    longitude = db.Column(db.Numeric(11, 8))
    approach_road_width = db.Column(db.Numeric(8, 2))  # in meters
    nearest_metro_distance = db.Column(db.Numeric(8, 2))  # in km
    airport_distance = db.Column(db.Numeric(8, 2))  # in km

    @validates('latitude')
    def validate_latitude(self, key, value):
        if value is None:
            return value
        if isinstance(value, str):
            value = Decimal(value)
        if value < -90 or value > 90:
            raise ValueError("Latitude must be between -90 and +90 degrees")
        return value

    @validates('longitude')
    def validate_longitude(self, key, value):
        if value is None:
            return value
        if isinstance(value, str):
            value = Decimal(value)
        if value < -180 or value > 180:
            raise ValueError("Longitude must be between -180 and +180 degrees")
        return value
    
    # RERA Details
    rera_number = db.Column(db.String(100))
    rera_website = db.Column(db.String(500))
    rera_status = db.Column(db.String(20), default='approved')
    
    # Content
    description = db.Column(db.Text)
    highlights = db.Column(db.Text)
    master_plan_url = db.Column(db.String(500))
    brochure_url = db.Column(db.String(500))
    
    # SEO and Status
    meta_title = db.Column(db.String(255))
    meta_description = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)

    # Relationships
    towers = db.relationship('Tower', back_populates='parent_project', lazy=True)
    unit_types = db.relationship('UnitType', backref='project', lazy=True)
    property_units = db.relationship('PropertyUnit', backref='project', lazy=True)
    amenities = db.relationship('Amenity', secondary='project_amenities', back_populates='projects')
    media = db.relationship('ProjectMedia', back_populates='project', lazy=True)
    documents = db.relationship('ProjectDocument', back_populates='project', lazy=True)
    approvals = db.relationship('Approval', secondary='project_approvals', backref='projects')
    reviews = db.relationship('Review', backref='project', lazy=True)
    user_interests = db.relationship('UserInterest', backref='project', lazy=True)
    price_history = db.relationship('PriceHistory', backref='project', lazy=True)

    def __repr__(self):
        return f'<Project {self.name}>'

    @property
    def average_rating(self):
        if not self.reviews:
            return 0
        return sum(review.rating for review in self.reviews) / len(self.reviews)

    def update_price_range(self):
        """Update min and max price based on unit types"""
        unit_prices = [ut.base_price for ut in self.unit_types if ut.base_price]
        if unit_prices:
            self.min_price = min(unit_prices)
            self.max_price = max(unit_prices)
            db.session.commit()

    def get_available_units(self):
        """Get count of available units"""
        return sum(unit.available_units for unit in self.unit_types) 