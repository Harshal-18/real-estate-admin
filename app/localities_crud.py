import sys
import os
from datetime import datetime

# Add the parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models import Locality

app = create_app()

def list_localities():
    """List all localities"""
    with app.app_context():
        localities = Locality.query.all()
        if not localities:
            print("\nNo localities found.")
            return
        print("\nList of All Localities:")
        print("=" * 50)
        for loc in localities:
            print(f"ID: {loc.locality_id}, Name: {loc.name}, City ID: {loc.city_id}, Pincode: {loc.pincode}")
            print("-" * 50)

def create_locality():
    """Create a new locality"""
    print("\nCreate New Locality")
    print("=" * 50)

    city_id = input("City ID: ").strip()
    name = input("Locality Name: ").strip()
    locality_type = input("Locality Type: ").strip()
    pincode = input("Pincode: ").strip()
    latitude = input("Latitude (10,8): ").strip()
    longitude = input("Longitude (11,8): ").strip()
    description = input("Description: ").strip()

    try:
        with app.app_context():
            locality = Locality(
                city_id=int(city_id),
                name=name,
                locality_type=locality_type or None,
                pincode=pincode or None,
                latitude=float(latitude),
                longitude=float(longitude),
                description=description or None
            )
            db.session.add(locality)
            db.session.commit()
            print(f"\n✅ Locality '{name}' created successfully!")
    except Exception as e:
        print(f"\n❌ Error creating locality: {str(e)}")

def read_locality():
    """View a specific locality"""
    locality_id = input("\nEnter Locality ID to view: ").strip()
    with app.app_context():
        locality = Locality.query.get(locality_id)
        if not locality:
            print("\n❌ Locality not found!")
            return
        print("\nLocality Details:")
        print("=" * 50)
        for column in locality.__table__.columns:
            print(f"{column.name}: {getattr(locality, column.name)}")

def update_locality():
    """Update an existing locality"""
    locality_id = input("\nEnter Locality ID to update: ").strip()
    with app.app_context():
        locality = Locality.query.get(locality_id)
        if not locality:
            print("\n❌ Locality not found!")
            return

        print("\nUpdate Locality (leave blank to keep current value)")

        locality.city_id = int(input(f"City ID [{locality.city_id}]: ") or locality.city_id)
        locality.name = input(f"Name [{locality.name}]: ") or locality.name
        locality.locality_type = input(f"Type [{locality.locality_type or ''}]: ") or locality.locality_type
        locality.pincode = input(f"Pincode [{locality.pincode or ''}]: ") or locality.pincode
        locality.latitude = float(input(f"Latitude [{locality.latitude}]: ") or locality.latitude)
        locality.longitude = float(input(f"Longitude [{locality.longitude}]: ") or locality.longitude)
        locality.description = input(f"Description [{locality.description or ''}]: ") or locality.description

        db.session.commit()
        print(f"\n✅ Locality '{locality.name}' updated successfully!")

def delete_locality():
    """Delete a locality"""
    locality_id = input("\nEnter Locality ID to delete: ").strip()
    with app.app_context():
        locality = Locality.query.get(locality_id)
        if not locality:
            print("\n❌ Locality not found!")
            return

        confirm = input(f"Are you sure you want to delete locality '{locality.name}'? (yes/no): ").lower()
        if confirm == 'yes':
            db.session.delete(locality)
            db.session.commit()
            print(f"\n✅ Locality '{locality.name}' deleted successfully!")
        else:
            print("\n❌ Deletion cancelled.")

def main_menu():
    while True:
        print("\nLocality Management System")
        print("=" * 30)
        print("1. List All Localities")
        print("2. Create New Locality")
        print("3. View Locality Details")
        print("4. Update Locality")
        print("5. Delete Locality")
        print("0. Exit")

        choice = input("Enter your choice (0-5): ")

        if choice == '1':
            list_localities()
        elif choice == '2':
            create_locality()
        elif choice == '3':
            read_locality()
        elif choice == '4':
            update_locality()
        elif choice == '5':
            delete_locality()
        elif choice == '0':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == '__main__':
    main_menu()
