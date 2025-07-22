import sys
import os

# Add the parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models import City
from decimal import Decimal

app = create_app()

def list_cities():
    """List all cities"""
    with app.app_context():
        cities = City.query.all()
        if not cities:
            print("\nNo cities found.")
            return
        
        print("\nList of All Cities:")
        print("=" * 50)
        for city in cities:
            print(f"City ID: {city.city_id}")
            print(f"Name: {city.name}")
            print(f"State: {city.state}")
            print(f"Country: {city.country}")
            print(f"Coordinates: ({city.latitude}, {city.longitude})")
            print("-" * 50)

def create_city():
    """Create a new city"""
    print("\nCreate New City")
    print("=" * 50)
    print("(Fields marked with * are required)\n")
    
    # Required fields
    name = input("City Name*: ").strip()
    while not name:
        print("City name is required!")
        name = input("City Name*: ").strip()

    state = input("State*: ").strip()
    while not state:
        print("State is required!")
        state = input("State*: ").strip()

    country = input("Country*: ").strip()
    while not country:
        print("Country is required!")
        country = input("Country*: ").strip()
    
    # Optional coordinates with validation
    latitude = input("Latitude (-90 to 90): ").strip()
    while latitude:
        try:
            lat = float(latitude)
            if -90 <= lat <= 90:
                break
            print("Latitude must be between -90 and 90 degrees")
            latitude = input("Latitude (-90 to 90): ").strip()
        except ValueError:
            print("Please enter a valid number")
            latitude = input("Latitude (-90 to 90): ").strip()

    longitude = input("Longitude (-180 to 180): ").strip()
    while longitude:
        try:
            lon = float(longitude)
            if -180 <= lon <= 180:
                break
            print("Longitude must be between -180 and 180 degrees")
            longitude = input("Longitude (-180 to 180): ").strip()
        except ValueError:
            print("Please enter a valid number")
            longitude = input("Longitude (-180 to 180): ").strip()

    try:
        with app.app_context():
            # Create new city
            city = City()
            city.name = name
            city.state = state
            city.country = country
            city.latitude = Decimal(latitude) if latitude else None
            city.longitude = Decimal(longitude) if longitude else None
            
            # Add to database
            db.session.add(city)
            db.session.commit()
            
            print(f"\n✅ City '{name}' created successfully!")
            print("\nCity Details:")
            print("=" * 50)
            print(f"City ID: {city.city_id}")
            print(f"Name: {city.name}")
            print(f"State: {city.state}")
            print(f"Country: {city.country}")
            if city.latitude and city.longitude:
                print(f"Coordinates: ({city.latitude}, {city.longitude})")
            else:
                print("Coordinates: Not specified")
            
    except Exception as e:
        print(f"\n❌ Error creating city: {str(e)}")

def read_city():
    """Read a specific city's details"""
    city_id = input("\nEnter City ID to view: ")
    
    try:
        with app.app_context():
            city = City.query.get(city_id)
            if not city:
                print("\n❌ City not found!")
                return
            
            print("\nCity Details:")
            print("=" * 50)
            print(f"City ID: {city.city_id}")
            print(f"Name: {city.name}")
            print(f"State: {city.state}")
            print(f"Country: {city.country}")
            if city.latitude and city.longitude:
                print(f"Coordinates: ({city.latitude}, {city.longitude})")
            else:
                print("Coordinates: Not specified")
            
            # Show localities if any
            if city.localities:
                print("\nLocalities in this city:")
                print("-" * 30)
                for locality in city.localities:
                    print(f"- {locality.name} (ID: {locality.locality_id})")
            
    except Exception as e:
        print(f"\n❌ Error reading city: {str(e)}")

def update_city():
    """Update an existing city"""
    city_id = input("\nEnter City ID to update: ")
    
    try:
        with app.app_context():
            city = City.query.get(city_id)
            if not city:
                print("\n❌ City not found!")
                return
            
            print("\nUpdate City")
            print("=" * 50)
            print("(Press Enter to keep current value)\n")
            
            # Basic city details
            name = input(f"City Name [{city.name}]: ").strip() or city.name
            state = input(f"State [{city.state}]: ").strip() or city.state
            country = input(f"Country [{city.country}]: ").strip() or city.country
            
            # Coordinates
            current_lat = str(city.latitude) if city.latitude is not None else "Not specified"
            latitude = input(f"Latitude (-90 to 90) [{current_lat}]: ").strip()
            while latitude:
                try:
                    lat = float(latitude)
                    if -90 <= lat <= 90:
                        break
                    print("Latitude must be between -90 and 90 degrees")
                    latitude = input(f"Latitude (-90 to 90) [{current_lat}]: ").strip()
                except ValueError:
                    print("Please enter a valid number")
                    latitude = input(f"Latitude (-90 to 90) [{current_lat}]: ").strip()

            current_lon = str(city.longitude) if city.longitude is not None else "Not specified"
            longitude = input(f"Longitude (-180 to 180) [{current_lon}]: ").strip()
            while longitude:
                try:
                    lon = float(longitude)
                    if -180 <= lon <= 180:
                        break
                    print("Longitude must be between -180 and 180 degrees")
                    longitude = input(f"Longitude (-180 to 180) [{current_lon}]: ").strip()
                except ValueError:
                    print("Please enter a valid number")
                    longitude = input(f"Longitude (-180 to 180) [{current_lon}]: ").strip()
            
            # Update city attributes
            city.name = name
            city.state = state
            city.country = country
            if latitude:
                city.latitude = Decimal(latitude)
            if longitude:
                city.longitude = Decimal(longitude)
            
            # Save changes
            db.session.commit()
            
            print("\n✅ City updated successfully!")
            print("\nUpdated City Details:")
            print("=" * 50)
            print(f"City ID: {city.city_id}")
            print(f"Name: {city.name}")
            print(f"State: {city.state}")
            print(f"Country: {city.country}")
            if city.latitude is not None and city.longitude is not None:
                print(f"Coordinates: ({city.latitude}, {city.longitude})")
            else:
                print("Coordinates: Not specified")
            
    except Exception as e:
        print(f"\n❌ Error updating city: {str(e)}")

def delete_city():
    """Delete an existing city"""
    city_id = input("\nEnter City ID to delete: ")
    
    try:
        with app.app_context():
            city = City.query.get(city_id)
            if not city:
                print("\n❌ City not found!")
                return
            
            # Check if city has localities
            if city.localities:
                print("\n❌ Cannot delete city with existing localities!")
                print(f"This city has {len(city.localities)} locality/localities.")
                print("Please delete or reassign all localities first.")
                return
            
            confirm = input(f"\n⚠️ Are you sure you want to delete city '{city.name}'? (yes/no): ")
            if confirm.lower() == 'yes':
                # Get the current max ID before deletion
                max_id = db.session.query(db.func.max(City.city_id)).scalar() or 0
                
                # Delete the city
                db.session.delete(city)
                db.session.commit()
                
                # Reset auto-increment to the current max ID
                db.session.execute(db.text(f"ALTER TABLE cities AUTO_INCREMENT = {max_id}"))
                db.session.commit()
                
                print(f"\n✅ City '{city.name}' deleted successfully!")
            else:
                print("\nDeletion cancelled.")
            
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")

def main_menu():
    """Display the main menu"""
    while True:
        print("\nCity Management System")
        print("=" * 30)
        print("1. List All Cities")
        print("2. Create New City")
        print("3. View City Details")
        print("4. Update City")
        print("5. Delete City")
        print("0. Exit")
        
        choice = input("\nEnter your choice (0-5): ")
        
        if choice == '1':
            list_cities()
        elif choice == '2':
            create_city()
        elif choice == '3':
            read_city()
        elif choice == '4':
            update_city()
        elif choice == '5':
            delete_city()
        elif choice == '0':
            print("\nGoodbye!")
            break
        else:
            print("\n❌ Invalid choice. Please try again.")

if __name__ == '__main__':
    main_menu() 