from app import db
from .base import BaseModel

class UnitRoomDetail(BaseModel):
    __tablename__ = 'unit_room_details'
    
    room_detail_id = db.Column(db.Integer, primary_key=True)
    unit_type_id = db.Column(db.Integer, db.ForeignKey('unit_types.unit_type_id'), nullable=False)
    room_type = db.Column(db.String(50), nullable=False)
    room_name = db.Column(db.String(100))
    room_sequence = db.Column(db.Integer, default=1)
    
    # Dimensions
    room_length = db.Column(db.Numeric(8, 2), nullable=False)
    room_width = db.Column(db.Numeric(8, 2), nullable=False)
    room_area = db.Column(db.Numeric(8, 2), nullable=False)
    
    # Shape and layout
    room_shape = db.Column(db.String(30), default='rectangular')
    
    # Room specific features
    has_attached_bathroom = db.Column(db.Boolean, default=False)
    has_balcony_access = db.Column(db.Boolean, default=False)
    has_wardrobe = db.Column(db.Boolean, default=False)
    wardrobe_type = db.Column(db.String(50))
    wardrobe_area = db.Column(db.Numeric(6, 2))
    
    # Natural light and ventilation
    has_window = db.Column(db.Boolean, default=True)
    window_count = db.Column(db.Integer, default=1)
    window_total_area = db.Column(db.Numeric(6, 2))
    natural_light_rating = db.Column(db.String(10), default='good')
    ventilation_rating = db.Column(db.String(10), default='good')
    
    # Doors and Windows specifications
    door_count = db.Column(db.Integer, default=1)
    door_type = db.Column(db.String(50))
    door_material = db.Column(db.String(50))
    door_width = db.Column(db.Numeric(5, 2))
    door_height = db.Column(db.Numeric(5, 2))
    
    window_type = db.Column(db.String(50))
    window_material = db.Column(db.String(50))
    window_width = db.Column(db.Numeric(5, 2))
    window_height = db.Column(db.Numeric(5, 2))
    
    # Electrical specifications
    electrical_points = db.Column(db.Integer, default=0)
    fan_points = db.Column(db.Integer, default=0)
    ac_points = db.Column(db.Integer, default=0)
    light_points = db.Column(db.Integer, default=0)
    
    # Flooring and ceiling
    flooring_type = db.Column(db.String(50))
    flooring_brand = db.Column(db.String(100))
    ceiling_type = db.Column(db.String(50))
    ceiling_height = db.Column(db.Numeric(5, 2))
    
    # Fixtures
    has_geyser_provision = db.Column(db.Boolean, default=False)
    has_exhaust_fan = db.Column(db.Boolean, default=False)
    has_chimney_provision = db.Column(db.Boolean, default=False)
    
    # Privacy and position
    privacy_level = db.Column(db.String(20), default='private')
    position_in_unit = db.Column(db.String(30))

    def __repr__(self):
        return f'<RoomDetail {self.room_name} of {self.unit_type.type_name}>'


class BalconyDetail(BaseModel):
    __tablename__ = 'balcony_details'
    
    balcony_id = db.Column(db.Integer, primary_key=True)
    unit_type_id = db.Column(db.Integer, db.ForeignKey('unit_types.unit_type_id'), nullable=False)
    balcony_name = db.Column(db.String(100))
    balcony_sequence = db.Column(db.Integer, default=1)
    
    # Dimensions
    balcony_length = db.Column(db.Numeric(8, 2), nullable=False)
    balcony_width = db.Column(db.Numeric(8, 2), nullable=False)
    balcony_area = db.Column(db.Numeric(8, 2), nullable=False)
    
    # Access and connection
    connected_room = db.Column(db.String(50))
    access_type = db.Column(db.String(30), default='sliding_door')
    
    # Features
    balcony_type = db.Column(db.String(30), default='regular')
    has_provision_for_washing_machine = db.Column(db.Boolean, default=False)
    has_provision_for_drying = db.Column(db.Boolean, default=True)
    has_safety_grill = db.Column(db.Boolean, default=True)
    
    # View and orientation
    facing_direction = db.Column(db.String(20))
    view_description = db.Column(db.Text)
    floor_level = db.Column(db.String(20))

    def __repr__(self):
        return f'<BalconyDetail {self.balcony_name} of {self.unit_type.type_name}>'


class DoorWindowSpec(BaseModel):
    __tablename__ = 'door_window_specs'
    
    spec_id = db.Column(db.Integer, primary_key=True)
    unit_type_id = db.Column(db.Integer, db.ForeignKey('unit_types.unit_type_id'), nullable=False)
    item_type = db.Column(db.String(20), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    
    # Physical specifications
    width = db.Column(db.Numeric(5, 2))
    height = db.Column(db.Numeric(5, 2))
    thickness = db.Column(db.Numeric(5, 2))
    
    # Material and finish
    material = db.Column(db.String(50))
    finish = db.Column(db.String(50))
    brand = db.Column(db.String(100))
    grade = db.Column(db.String(50))
    
    # Features
    is_security_door = db.Column(db.Boolean, default=False)
    has_grill = db.Column(db.Boolean, default=False)
    opening_type = db.Column(db.String(30))
    
    # Hardware
    lock_type = db.Column(db.String(50))
    handle_type = db.Column(db.String(50))
    handle_material = db.Column(db.String(30))
    
    # Glass specifications (for windows)
    glass_type = db.Column(db.String(50))
    glass_thickness = db.Column(db.Numeric(4, 2))

    def __repr__(self):
        return f'<DoorWindowSpec {self.item_type} at {self.location}>' 