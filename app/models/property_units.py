from app import db
from .base import BaseModel
from sqlalchemy.ext.declarative import declared_attr
from datetime import datetime

class Tower(db.Model):
    __tablename__ = 'towers'
    
    tower_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.project_id'), nullable=False)
    tower_name = db.Column(db.String(100), nullable=False)
    tower_number = db.Column(db.String(50))
    total_floors = db.Column(db.Integer, nullable=False)
    units_per_floor = db.Column(db.Integer, default=0)
    total_units = db.Column(db.Integer, default=0)
    tower_type = db.Column(db.String(20), default='residential')
    
    # Tower specifics
    construction_status = db.Column(db.String(30), default='under_construction')
    possession_date = db.Column(db.Date)
    height_meters = db.Column(db.Numeric(8, 2))
    
    # Facilities
    elevator_count = db.Column(db.Integer, default=0)
    has_power_backup = db.Column(db.Boolean, default=True)
    has_water_backup = db.Column(db.Boolean, default=True)
    has_fire_safety = db.Column(db.Boolean, default=True)
    
    # Positioning
    latitude = db.Column(db.Numeric(10, 8))
    longitude = db.Column(db.Numeric(11, 8))
    facing_direction = db.Column(db.String(20))
    
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    property_units = db.relationship('PropertyUnit', backref='tower', lazy=True)
    parent_project = db.relationship('Project', back_populates='towers')

    def __repr__(self):
        return f'<Tower {self.tower_name} of Project {self.project_id}>'


class UnitType(BaseModel):
    __tablename__ = 'unit_types'
    
    unit_type_id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.project_id'), nullable=False)
    type_name = db.Column(db.String(100), nullable=False)
    bedrooms = db.Column(db.Integer, nullable=False)
    bathrooms = db.Column(db.Integer, nullable=False)
    
    # Room counts
    master_bedrooms = db.Column(db.Integer, default=0)
    child_bedrooms = db.Column(db.Integer, default=0)
    guest_bedrooms = db.Column(db.Integer, default=0)
    study_rooms = db.Column(db.Integer, default=0)
    living_rooms = db.Column(db.Integer, default=1)
    dining_rooms = db.Column(db.Integer, default=0)
    kitchens = db.Column(db.Integer, default=1)
    utility_rooms = db.Column(db.Integer, default=0)
    store_rooms = db.Column(db.Integer, default=0)
    pooja_rooms = db.Column(db.Integer, default=0)
    
    # Maid room details
    has_maid_room = db.Column(db.Boolean, default=False)
    maid_room_area = db.Column(db.Numeric(8, 2))
    has_maid_bathroom = db.Column(db.Boolean, default=False)
    
    # Balcony details
    has_balcony = db.Column(db.Boolean, default=True)
    balcony_count = db.Column(db.Integer, default=0)
    total_balcony_area = db.Column(db.Numeric(8, 2))
    
    # Additional areas
    has_terrace = db.Column(db.Boolean, default=False)
    terrace_area = db.Column(db.Numeric(8, 2))
    has_private_garden = db.Column(db.Boolean, default=False)
    private_garden_area = db.Column(db.Numeric(8, 2))
    
    # Area Details
    carpet_area = db.Column(db.Numeric(10, 2))
    built_up_area = db.Column(db.Numeric(10, 2))
    super_area = db.Column(db.Numeric(10, 2))
    carpet_ratio = db.Column(db.Numeric(5, 2))
    
    # Pricing
    base_price = db.Column(db.Numeric(15, 2))
    price_per_sqft = db.Column(db.Numeric(10, 2))
    
    # Layout specifications
    floor_plan_url = db.Column(db.String(500))
    floor_height = db.Column(db.Numeric(5, 2))
    ceiling_height = db.Column(db.Numeric(5, 2))
    facing_direction = db.Column(db.String(20))
    
    # Door specifications
    main_door_type = db.Column(db.String(50))
    main_door_width = db.Column(db.Numeric(5, 2))
    main_door_height = db.Column(db.Numeric(5, 2))
    bedroom_door_type = db.Column(db.String(50))
    bathroom_door_type = db.Column(db.String(50))
    
    # Window specifications
    window_type = db.Column(db.String(50))
    window_material = db.Column(db.String(50))
    
    # Availability
    total_units = db.Column(db.Integer, default=0)
    available_units = db.Column(db.Integer, default=0)
    sold_units = db.Column(db.Integer, default=0)
    
    is_active = db.Column(db.Boolean, default=True)

    # Relationships
    property_units = db.relationship('PropertyUnit', backref='unit_type', lazy=True)
    room_details = db.relationship('UnitRoomDetail', backref='unit_type', lazy=True)
    balcony_details = db.relationship('BalconyDetail', backref='unit_type', lazy=True)
    door_window_specs = db.relationship('DoorWindowSpec', backref='unit_type', lazy=True)
    price_history = db.relationship('PriceHistory', backref='unit_type', lazy=True)

    def __repr__(self):
        return f'<UnitType {self.type_name} of {self.project.name}>'

    @property
    def total_rooms(self):
        return (self.bedrooms + self.living_rooms + self.dining_rooms + 
                self.study_rooms + (1 if self.has_maid_room else 0))

    def update_availability(self):
        """Update unit counts based on property units"""
        self.total_units = len(self.property_units)
        self.available_units = len([pu for pu in self.property_units if pu.status == 'available'])
        self.sold_units = len([pu for pu in self.property_units if pu.status == 'sold'])
        db.session.commit()


class PropertyUnit(BaseModel):
    __tablename__ = 'property_units'
    
    unit_id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.project_id'), nullable=False)
    unit_type_id = db.Column(db.Integer, db.ForeignKey('unit_types.unit_type_id'), nullable=False)
    tower_id = db.Column(db.Integer, db.ForeignKey('towers.tower_id'), nullable=False)
    unit_number = db.Column(db.String(50), nullable=False)
    floor_number = db.Column(db.Integer, nullable=False)
    block_number = db.Column(db.String(50))
    
    unit_position = db.Column(db.String(20))  # corner, middle, end
    wing = db.Column(db.String(10))  # A, B, C, etc.
    
    # Specific unit details
    carpet_area = db.Column(db.Numeric(10, 2))
    built_up_area = db.Column(db.Numeric(10, 2))
    super_area = db.Column(db.Numeric(10, 2))
    
    has_corner_unit = db.Column(db.Boolean, default=False)
    has_extra_balcony = db.Column(db.Boolean, default=False)
    has_servant_quarter = db.Column(db.Boolean, default=False)
    
    # Pricing
    unit_price = db.Column(db.Numeric(15, 2))
    price_per_sqft = db.Column(db.Numeric(10, 2))
    maintenance_charge = db.Column(db.Numeric(10, 2))
    # Add total_price to match DB
    total_price = db.Column(db.Numeric(15, 2))
    # Status
    status = db.Column(db.String(20), default='available')
    possession_date = db.Column(db.Date)
    
    # Premium/Discount
    premium_percentage = db.Column(db.Numeric(5, 2), default=0.00)
    discount_percentage = db.Column(db.Numeric(5, 2), default=0.00)
    
    # Specific details
    actual_facing_direction = db.Column(db.String(20))
    view_description = db.Column(db.Text)
    
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<PropertyUnit {self.unit_number} in Tower {self.tower_id}>'

    def calculate_total_price(self):
        """Calculate total price including all charges"""
        base = self.unit_price or 0
        premium = base * (self.premium_percentage or 0) / 100
        discount = base * (self.discount_percentage or 0) / 100
        maintenance = self.maintenance_charge or 0
        
        self.unit_price = base + premium - discount + maintenance
        db.session.commit() 