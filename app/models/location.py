from app import db
from .base import BaseModel
from datetime import datetime

class City(BaseModel):
    __tablename__ = 'cities'
    
    city_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(100), nullable=False)
    latitude = db.Column(db.Numeric(10, 8))
    longitude = db.Column(db.Numeric(11, 8))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    localities = db.relationship('Locality', backref='city', lazy=True)

    def __repr__(self):
        return f'<City {self.name}, {self.state}>'


class Locality(BaseModel):
    __tablename__ = 'localities'
    
    locality_id = db.Column(db.Integer, primary_key=True)
    city_id = db.Column(db.Integer, db.ForeignKey('cities.city_id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    locality_type = db.Column(db.String(20), default='locality')
    pincode = db.Column(db.String(10))
    latitude = db.Column(db.Numeric(10, 8))
    longitude = db.Column(db.Numeric(11, 8))
    description = db.Column(db.Text)

    # Relationships
    projects = db.relationship('Project', backref='locality', lazy=True)

    def __repr__(self):
        return f'<Locality {self.name}, {self.city.name}>'

    @property
    def full_address(self):
        return f"{self.name}, {self.city.name}, {self.city.state}, {self.pincode}" 