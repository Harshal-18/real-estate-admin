#!/usr/bin/env python3
"""
Test script to check database data
"""
import os
from app import create_app, db
from app.models import *

def test_data():
    """Test if data exists in database"""
    app = create_app()
    
    with app.app_context():
        try:
            print("🔍 Checking database data...")
            
            # Check cities
            cities = db.session.query(City).all()
            print(f"🏙️ Cities found: {len(cities)}")
            for city in cities:
                print(f"   - {city.name}, {city.state}")
            
            # Check developers
            developers = db.session.query(Developer).all()
            print(f"🏢 Developers found: {len(developers)}")
            for dev in developers:
                print(f"   - {dev.name}")
            
            # Check projects
            projects = db.session.query(Project).all()
            print(f"🏗️ Projects found: {len(projects)}")
            for project in projects:
                print(f"   - {project.name} by {project.developer.name if project.developer else 'Unknown'}")
            
            # Check users
            users = db.session.query(User).all()
            print(f"👥 Users found: {len(users)}")
            for user in users:
                print(f"   - {user.email} (Admin: {user.is_admin})")
            
            # Check amenities
            amenities = db.session.query(Amenity).all()
            print(f"🏊 Amenities found: {len(amenities)}")
            for amenity in amenities:
                print(f"   - {amenity.name} ({amenity.category})")
            
            if len(cities) == 0:
                print("❌ No data found! Database might be empty.")
                print("🔄 Running seed data...")
                from Database.seed_data import seed_data
                seed_data()
                print("✅ Seed data completed!")
            else:
                print("✅ Data exists in database!")
                
        except Exception as e:
            print(f"❌ Error checking data: {e}")

if __name__ == "__main__":
    test_data() 