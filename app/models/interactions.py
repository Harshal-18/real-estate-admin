from app import db
from .base import BaseModel

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from datetime import datetime

class UserInterest(BaseModel):
    __tablename__ = 'user_interests'
    
    interest_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.project_id'))
    unit_type_id = db.Column(db.Integer, db.ForeignKey('unit_types.unit_type_id'))
    interest_type = db.Column(db.String(20), nullable=False)
    
    # Contact preferences
    preferred_contact_method = db.Column(db.String(20), default='phone')
    preferred_contact_time = db.Column(db.String(20), default='anytime')
    
    # Requirements
    budget_min = db.Column(db.Numeric(15, 2))
    budget_max = db.Column(db.Numeric(15, 2))
    preferred_floors = db.Column(db.Text)
    specific_requirements = db.Column(db.Text)
    
    # Status
    status = db.Column(db.String(30), default='new')
    assigned_to = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    notes = db.Column(db.Text)

    def __repr__(self):
        return f'<UserInterest {self.interest_type} by {self.user.full_name}>'


class Review(BaseModel):
    __tablename__ = 'reviews'
    
    review_id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.project_id'))
    developer_id = db.Column(db.Integer, db.ForeignKey('developers.developer_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(255))
    review_text = db.Column(db.Text)
    pros = db.Column(db.Text)
    cons = db.Column(db.Text)
    
    # Review categories
    construction_quality_rating = db.Column(db.Integer)
    amenities_rating = db.Column(db.Integer)
    location_rating = db.Column(db.Integer)
    value_for_money_rating = db.Column(db.Integer)
    
    is_verified = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<Review {self.rating}/5 by {self.user.full_name}>'


class SearchLog(BaseModel):
    __tablename__ = 'search_logs'
    
    search_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    search_query = db.Column(db.String(500))
    filters_applied = db.Column(db.Text)
    results_count = db.Column(db.Integer)
    clicked_project_id = db.Column(db.Integer, db.ForeignKey('projects.project_id'))
    session_id = db.Column(db.String(255))
    ip_address = db.Column(db.String(45))
    search_timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<SearchLog {self.search_query}>'


class PropertyComparison(BaseModel):
    __tablename__ = 'property_comparisons'
    
    comparison_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    project_ids = db.Column(db.Text, nullable=False)
    comparison_parameters = db.Column(db.Text)
    session_id = db.Column(db.String(255))

    def __repr__(self):
        return f'<PropertyComparison by {self.user.full_name if self.user else "Anonymous"}>'


class Notification(BaseModel):
    __tablename__ = 'notifications'
    
    notification_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    type = db.Column(db.String(20), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    message = db.Column(db.Text, nullable=False)
    related_project_id = db.Column(db.Integer, db.ForeignKey('projects.project_id'))
    is_read = db.Column(db.Boolean, default=False)
    is_sent = db.Column(db.Boolean, default=False)
    delivery_method = db.Column(db.String(20), default='in_app')
    read_at = db.Column(db.DateTime)

    def __repr__(self):
        return f'<Notification {self.title} for {self.user.full_name}>'


class PriceHistory(BaseModel):
    __tablename__ = 'price_history'
    
    price_history_id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.project_id'))
    unit_type_id = db.Column(db.Integer, db.ForeignKey('unit_types.unit_type_id'))
    old_price = db.Column(db.Numeric(15, 2))
    new_price = db.Column(db.Numeric(15, 2))
    old_price_per_sqft = db.Column(db.Numeric(10, 2))
    new_price_per_sqft = db.Column(db.Numeric(10, 2))
    change_percentage = db.Column(db.Numeric(5, 2))
    change_reason = db.Column(db.String(255))
    effective_date = db.Column(db.Date)

    def __repr__(self):
        return f'<PriceHistory for {self.project.name} - {self.unit_type.type_name}>' 