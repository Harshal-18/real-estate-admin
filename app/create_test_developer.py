import sys
import os

# Add the parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models import Developer

app = create_app()

def create_test_developer():
    """Create a test developer"""
    with app.app_context():
        # Check if test developer already exists
        test_dev = Developer.query.filter_by(name="Test Developer").first()
        if test_dev:
            print("\n✅ Test developer already exists!")
            print(f"ID: {test_dev.developer_id}")
            print(f"Name: {test_dev.name}")
            return
        
        # Create new developer
        developer = Developer(
            name="Test Developer",
            contact_email="test@developer.com",
            contact_phone="1234567890",
            established_year=2020,
            description="A test developer for testing purposes"
        )
        
        db.session.add(developer)
        db.session.commit()
        
        print("\n✅ Test developer created successfully!")
        print(f"ID: {developer.developer_id}")
        print(f"Name: {developer.name}")

if __name__ == '__main__':
    create_test_developer() 