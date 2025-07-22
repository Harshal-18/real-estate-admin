from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager
from .base import BaseModel

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin, BaseModel):
    __tablename__ = 'users'
    
    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    phone = db.Column(db.String(20), unique=True)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    user_type = db.Column(db.String(20), default='buyer')
    is_verified = db.Column(db.Boolean, default=False)
    last_login = db.Column(db.DateTime)
    profile_image_url = db.Column(db.String(500))
    is_active = db.Column(db.Boolean, default=True)
    is_admin = db.Column(db.Boolean, default=False)

    # Relationships
    interests = db.relationship('UserInterest', backref='user', lazy=True, 
                              foreign_keys='UserInterest.user_id')
    assigned_interests = db.relationship('UserInterest', backref='assigned_to_user', lazy=True,
                                       foreign_keys='UserInterest.assigned_to')
    reviews = db.relationship('Review', backref='user', lazy=True)
    search_logs = db.relationship('SearchLog', backref='user', lazy=True)
    property_comparisons = db.relationship('PropertyComparison', backref='user', lazy=True)
    notifications = db.relationship('Notification', backref='user', lazy=True)

    def get_id(self):
        return str(self.user_id)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __repr__(self):
        return f'<User {self.email}>' 