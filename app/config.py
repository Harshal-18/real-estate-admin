import os
from dotenv import load_dotenv
import urllib.parse

# Load environment variables from .env file
load_dotenv(override=True)

class Config:
    # Database configuration
    DATABASE_URL = os.getenv('DATABASE_URL')
    print(f"Database URL from environment: {DATABASE_URL}")  # Debug print
    
    if DATABASE_URL:
        # Render provides DATABASE_URL for PostgreSQL
        if DATABASE_URL.startswith('postgres://'):
            DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)
        SQLALCHEMY_DATABASE_URI = DATABASE_URL
        print(f"Using database URI: {SQLALCHEMY_DATABASE_URI}")  # Debug print
    else:
        # Fallback for local development
        SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@localhost/real_estate'
        print("Warning: Using local database fallback")
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Flask configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-here')
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    
    # Upload configuration
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    
    # Mail settings
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'smtp.gmail.com'
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') or True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    
    # Admin account
    ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME') or 'admin'
    ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL') or 'admin@example.com'
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD') or 'admin' 