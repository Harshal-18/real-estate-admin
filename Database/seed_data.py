#!/usr/bin/env python3
"""
Seed data script for Render deployment
"""
import os
from app import create_app, db
from app.models import *

def seed_data():
    """Insert seed data into the database"""
    app = create_app()
    
    with app.app_context():
        try:
            print("🌱 Starting to seed database...")
            
            # Check if data already exists
            existing_cities = db.session.query(City).count()
            if existing_cities > 0:
                print("✅ Data already exists, skipping seed...")
                return
            
            # Create Cities
            print("🏙️ Creating cities...")
            cities_data = [
                {'name': 'Bengaluru', 'state': 'Karnataka', 'country': 'India', 'latitude': 12.97160000, 'longitude': 77.59460000},
                {'name': 'Ahmedabad', 'state': 'Gujarat', 'country': 'India', 'latitude': 23.02260000, 'longitude': 72.57140000},
                {'name': 'Surat', 'state': 'Gujrat', 'country': 'India', 'latitude': None, 'longitude': None}
            ]
            
            cities = []
            for city_data in cities_data:
                city = City(**city_data)
                cities.append(city)
                db.session.add(city)
            
            db.session.commit()
            print(f"✅ Created {len(cities)} cities")
            
            # Create Developers
            print("🏢 Creating developers...")
            developers_data = [
                {
                    'name': 'Lodha Group',
                    'established_year': 1980,
                    'description': 'Lodha Group is India\'s largest residential real estate developer by sales and construction area.',
                    'website_url': 'https://www.lodhagroup.com',
                    'contact_email': 'sales@lodha.com',
                    'total_projects': 2,
                    'completed_projects': 0,
                    'ongoing_projects': 1,
                    'is_verified': True
                },
                {
                    'name': 'East Park Developers',
                    'established_year': 1995,
                    'description': 'East Park Developers is known for quality construction and timely delivery.',
                    'website_url': 'https://www.eastpark.com',
                    'contact_email': 'info@eastpark.com',
                    'total_projects': 0,
                    'completed_projects': 0,
                    'ongoing_projects': 0,
                    'is_verified': True
                },
                {
                    'name': 'Brigade Group',
                    'established_year': 1986,
                    'description': 'Brigade Group is one of India\'s leading property developers with over three decades of expertise.',
                    'website_url': 'https://www.brigadegroup.com',
                    'contact_email': 'sales@brigadegroup.com',
                    'total_projects': 2,
                    'completed_projects': 0,
                    'ongoing_projects': 0,
                    'is_verified': True
                }
            ]
            
            developers = []
            for dev_data in developers_data:
                developer = Developer(**dev_data)
                developers.append(developer)
                db.session.add(developer)
            
            db.session.commit()
            print(f"✅ Created {len(developers)} developers")
            
            # Create Localities
            print("📍 Creating localities...")
            localities_data = [
                {'city_id': 1, 'name': 'Whitefield', 'locality_type': 'micro_market', 'pincode': '560066', 'latitude': 12.96980000, 'longitude': 77.75000000},
                {'city_id': 1, 'name': 'Hennur', 'locality_type': 'locality', 'pincode': '560043', 'latitude': 13.02730000, 'longitude': 77.63320000},
                {'city_id': 1, 'name': 'Vittal Mallya Road', 'locality_type': 'locality', 'pincode': '560001', 'latitude': 12.97200000, 'longitude': 77.59530000},
                {'city_id': 2, 'name': 'Kankariya_lake', 'locality_type': 'round-about lake', 'pincode': '380008', 'latitude': 23.02260000, 'longitude': 72.57140000, 'description': 'This is the very famous lake of the ahmedabad with high rush on weekends and also on weekdays as well'}
            ]
            
            localities = []
            for loc_data in localities_data:
                locality = Locality(**loc_data)
                localities.append(locality)
                db.session.add(locality)
            
            db.session.commit()
            print(f"✅ Created {len(localities)} localities")
            
            # Create Amenities
            print("🏊 Creating amenities...")
            amenities_data = [
                {'name': 'Swimming Pool', 'category': 'lifestyle'},
                {'name': 'Gymnasium', 'category': 'lifestyle'},
                {'name': 'Club House', 'category': 'lifestyle'},
                {'name': 'Children\'s Play Area', 'category': 'lifestyle'},
                {'name': 'Indoor Games', 'category': 'sports'},
                {'name': 'Landscaped Gardens', 'category': 'natural'},
                {'name': '24/7 Security', 'category': 'security', 'icon_url': '', 'description': ''},
                {'name': 'Tennis Court', 'category': 'sports', 'is_rare': True},
                {'name': 'Yoga Deck', 'category': 'lifestyle'},
                {'name': 'Multipurpose Hall', 'category': 'lifestyle'}
            ]
            
            amenities = []
            for amenity_data in amenities_data:
                amenity = Amenity(**amenity_data)
                amenities.append(amenity)
                db.session.add(amenity)
            
            db.session.commit()
            print(f"✅ Created {len(amenities)} amenities")
            
            # Create Projects
            print("🏗️ Creating projects...")
            projects_data = [
                {
                    'developer_id': 1,
                    'locality_id': 1,
                    'name': 'Lodha Haven',
                    'project_type': 'residential',
                    'property_type': 'apartment',
                    'status': 'under_construction',
                    'total_land_area': 9.10,
                    'total_units': 250,
                    'unit_density': 50.00,
                    'open_area_percentage': 77.00,
                    'park_area': 0.90,
                    'clubhouse_area': 73.00,
                    'min_price': 15000000.00,
                    'max_price': 30000000.00,
                    'price_per_sqft': 8500.00,
                    'currency': 'INR',
                    'launch_date': '2023-01-15',
                    'possession_date': '2026-12-31',
                    'address': 'Choodasandra, Bengaluru',
                    'approach_road_width': 17.00,
                    'nearest_metro_distance': 4.17,
                    'rera_status': 'approved',
                    'description': 'Lodha Haven offers premium 2, 3 & 4 BHK apartments with world-class amenities in Whitefield, Bangalore.',
                    'master_plan_url': 'Master_plan_Lodha_Haven.png',
                    'is_active': True
                },
                {
                    'developer_id': 2,
                    'locality_id': 2,
                    'name': 'East Park Residences',
                    'project_type': 'residential',
                    'property_type': 'apartment',
                    'status': 'under_construction',
                    'total_land_area': 4.20,
                    'total_units': 180,
                    'min_price': 18000000.00,
                    'max_price': 35000000.00,
                    'price_per_sqft': 9200.00,
                    'currency': 'INR',
                    'launch_date': '2023-03-01',
                    'possession_date': '2026-06-30',
                    'rera_status': 'approved',
                    'description': 'East Park Residences presents luxurious 3 & 4 BHK apartments in Hennur, Bangalore with modern amenities.',
                    'is_active': True
                },
                {
                    'developer_id': 3,
                    'locality_id': 3,
                    'name': 'Brigade Insignia',
                    'project_type': 'residential',
                    'property_type': 'apartment',
                    'status': 'ready_to_move',
                    'total_land_area': 3.80,
                    'total_units': 160,
                    'unit_density': 10.00,
                    'open_area_percentage': 70.00,
                    'park_area': 20.00,
                    'clubhouse_area': 19.00,
                    'min_price': 25000000.00,
                    'max_price': 50000000.00,
                    'price_per_sqft': 12500.00,
                    'currency': 'INR',
                    'launch_date': '2020-06-01',
                    'possession_date': '2024-03-31',
                    'rera_status': 'approved',
                    'description': 'Brigade Insignia offers ultra-luxury 3 & 4 BHK apartments in the heart of Bangalore with premium amenities.',
                    'is_active': True
                }
            ]
            
            projects = []
            for project_data in projects_data:
                project = Project(**project_data)
                projects.append(project)
                db.session.add(project)
            
            db.session.commit()
            print(f"✅ Created {len(projects)} projects")
            
            # Create Users
            print("👥 Creating users...")
            users_data = [
                {
                    'email': 'abc.123@gmail.com',
                    'phone': '1234567891',
                    'password_hash': 'Hi@123',
                    'first_name': 'ABC',
                    'last_name': 'ABD',
                    'user_type': 'custoomer',
                    'is_verified': True,
                    'is_active': True
                },
                {
                    'email': 'abc.1234@gmail.com',
                    'password_hash': 'pbkdf2:sha256:600000$VGrpf2ktzzTFQpBm$574423fe46d37db2fdc7335a6c51f9d4134508bd42106eef815399713da8409a',
                    'first_name': 'Priyanshu',
                    'last_name': 'Patel',
                    'user_type': 'buyer',
                    'is_verified': False,
                    'is_active': True
                },
                {
                    'email': 'abc.12345@gmail.com',
                    'password_hash': 'pbkdf2:sha256:600000$LP2lSCA6hcfYXnZS$afb517562c573691cb6d4b74e0d39395873dc9cef9f0458eb621cadcc9285cd8',
                    'first_name': 'Priyanshu',
                    'last_name': 'Patel',
                    'user_type': 'buyer',
                    'is_verified': False,
                    'is_active': True,
                    'is_admin': True
                },
                {
                    'email': 'abd.123@gmail.com',
                    'password_hash': 'pbkdf2:sha256:600000$prVPGhGf5ZTFnr8u$b4080616eeee38652059403ea6d6aa87d91a15bc2a4363ac1af6b4e5f81a7edb',
                    'first_name': 'Harshal',
                    'last_name': 'Joshi',
                    'user_type': 'buyer',
                    'is_verified': False,
                    'is_active': True,
                    'is_admin': True
                },
                {
                    'email': 'admin@test.com',
                    'password_hash': 'admin123',
                    'first_name': 'Test',
                    'last_name': 'Admin',
                    'user_type': 'admin',
                    'is_verified': True,
                    'is_active': True,
                    'is_admin': True
                }
            ]
            
            users = []
            for user_data in users_data:
                user = User(**user_data)
                users.append(user)
                db.session.add(user)
            
            db.session.commit()
            print(f"✅ Created {len(users)} users")
            
            print("🎉 Database seeding completed successfully!")
            
        except Exception as e:
            print(f"❌ Error seeding database: {e}")
            db.session.rollback()

if __name__ == "__main__":
    seed_data() 