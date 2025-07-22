1
import sys
import os

# Add the parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models import Amenity
from datetime import datetime

app = create_app()

def list_amenities():
    """List all amenities"""
    with app.app_context():
        amenities = Amenity.query.all()
        if not amenities:
            print("\nNo amenities found.")
            return
        
        print("\nList of All Amenities:")
        print("=" * 50)
        for amenity in amenities:
            print(f"Amenity ID: {amenity.amenity_id}")
            print(f"Name: {amenity.name}")
            print(f"Category: {amenity.category}")
            print(f"Description: {amenity.description or 'N/A'}")
            print(f"Rare: {'Yes' if amenity.is_rare else 'No'}")
            print(f"Active: {'Yes' if amenity.is_active else 'No'}")
            print("-" * 50)

def create_amenity():
    """Create a new amenity"""
    print("\nCreate New Amenity")
    print("=" * 50)
    print("(Fields marked with * are required)\n")
    
    # Required fields
    name = input("Amenity Name*: ").strip()
    while not name:
        print("Amenity name is required!")
        name = input("Amenity Name*: ").strip()

    category = input("Category*: ").strip()
    while not category:
        print("Category is required!")
        category = input("Category*: ").strip()
    
    # Optional fields
    description = input("Description: ").strip()
    icon_url = input("Icon URL: ").strip()
    
    # Boolean fields with validation
    is_rare = input("Is Rare (1/0) [0]: ").strip() or "0"
    while is_rare not in ["0", "1"]:
        print("Please enter 0 or 1")
        is_rare = input("Is Rare (1/0) [0]: ").strip() or "0"
    
    is_active = input("Is Active (1/0) [1]: ").strip() or "1"
    while is_active not in ["0", "1"]:
        print("Please enter 0 or 1")
        is_active = input("Is Active (1/0) [1]: ").strip() or "1"

    try:
        with app.app_context():
            # Create new amenity
            amenity = Amenity()
            amenity.name = name
            amenity.category = category
            amenity.description = description or None
            amenity.icon_url = icon_url or None
            amenity.is_rare = bool(int(is_rare))
            amenity.is_active = bool(int(is_active))
            
            # Add to database
            db.session.add(amenity)
            db.session.commit()
            
            print(f"\n✅ Amenity '{name}' created successfully!")
            print("\nAmenity Details:")
            print("=" * 50)
            print(f"Amenity ID: {amenity.amenity_id}")
            print(f"Name: {amenity.name}")
            print(f"Category: {amenity.category}")
            print(f"Description: {amenity.description or 'N/A'}")
            print(f"Icon URL: {amenity.icon_url or 'N/A'}")
            print(f"Rare: {'Yes' if amenity.is_rare else 'No'}")
            print(f"Active: {'Yes' if amenity.is_active else 'No'}")
            print(f"Created At: {amenity.created_at}")
            
    except Exception as e:
        print(f"\n❌ Error creating amenity: {str(e)}")

def read_amenity():
    """Read a specific amenity's details"""
    amenity_id = input("\nEnter Amenity ID to view: ")
    
    try:
        with app.app_context():
            amenity = Amenity.query.get(amenity_id)
            if not amenity:
                print("\n❌ Amenity not found!")
                return
            
            print("\nAmenity Details:")
            print("=" * 50)
            print(f"Amenity ID: {amenity.amenity_id}")
            print(f"Name: {amenity.name}")
            print(f"Category: {amenity.category}")
            print(f"Description: {amenity.description or 'N/A'}")
            print(f"Icon URL: {amenity.icon_url or 'N/A'}")
            print(f"Rare: {'Yes' if amenity.is_rare else 'No'}")
            print(f"Active: {'Yes' if amenity.is_active else 'No'}")
            print(f"Created At: {amenity.created_at}")
            
            # Show projects using this amenity if any
            if amenity.projects:
                print("\nProjects with this amenity:")
                print("-" * 30)
                for project in amenity.projects:
                    print(f"- {project.name} (ID: {project.project_id})")
            
    except Exception as e:
        print(f"\n❌ Error reading amenity: {str(e)}")

def update_amenity():
    """Update an existing amenity"""
    amenity_id = input("\nEnter Amenity ID to update: ")
    
    try:
        with app.app_context():
            amenity = Amenity.query.get(amenity_id)
            if not amenity:
                print("\n❌ Amenity not found!")
                return
            
            print("\nUpdate Amenity")
            print("=" * 50)
            print("(Press Enter to keep current value)\n")
            
            # Basic amenity details
            name = input(f"Name [{amenity.name}]: ").strip() or amenity.name
            category = input(f"Category [{amenity.category}]: ").strip() or amenity.category
            description = input(f"Description [{amenity.description or 'N/A'}]: ").strip() or amenity.description
            icon_url = input(f"Icon URL [{amenity.icon_url or 'N/A'}]: ").strip() or amenity.icon_url
            
            # Boolean fields
            is_rare = input(f"Is Rare (1/0) [{1 if amenity.is_rare else 0}]: ").strip() or ('1' if amenity.is_rare else '0')
            while is_rare not in ["0", "1"]:
                print("Please enter 0 or 1")
                is_rare = input(f"Is Rare (1/0) [{1 if amenity.is_rare else 0}]: ").strip() or ('1' if amenity.is_rare else '0')
            
            is_active = input(f"Is Active (1/0) [{1 if amenity.is_active else 0}]: ").strip() or ('1' if amenity.is_active else '0')
            while is_active not in ["0", "1"]:
                print("Please enter 0 or 1")
                is_active = input(f"Is Active (1/0) [{1 if amenity.is_active else 0}]: ").strip() or ('1' if amenity.is_active else '0')
            
            # Update amenity attributes
            amenity.name = name
            amenity.category = category
            amenity.description = description
            amenity.icon_url = icon_url
            amenity.is_rare = bool(int(is_rare))
            amenity.is_active = bool(int(is_active))
            
            # Save changes
            db.session.commit()
            
            print("\n✅ Amenity updated successfully!")
            print("\nUpdated Amenity Details:")
            print("=" * 50)
            print(f"Amenity ID: {amenity.amenity_id}")
            print(f"Name: {amenity.name}")
            print(f"Category: {amenity.category}")
            print(f"Description: {amenity.description or 'N/A'}")
            print(f"Icon URL: {amenity.icon_url or 'N/A'}")
            print(f"Rare: {'Yes' if amenity.is_rare else 'No'}")
            print(f"Active: {'Yes' if amenity.is_active else 'No'}")
            print(f"Created At: {amenity.created_at}")
            
    except Exception as e:
        print(f"\n❌ Error updating amenity: {str(e)}")

def delete_amenity():
    """Delete an existing amenity"""
    amenity_id = input("\nEnter Amenity ID to delete: ")
    
    try:
        with app.app_context():
            amenity = Amenity.query.get(amenity_id)
            if not amenity:
                print("\n❌ Amenity not found!")
                return
            
            # Check if amenity is used in any projects
            if amenity.projects:
                print("\n❌ Cannot delete amenity that is used in projects!")
                print(f"This amenity is used in {len(amenity.projects)} project(s).")
                print("Please remove it from all projects first.")
                return
            
            confirm = input(f"\n⚠️ Are you sure you want to delete amenity '{amenity.name}'? (yes/no): ")
            if confirm.lower() == 'yes':
                # Get the current max ID before deletion
                max_id = db.session.query(db.func.max(Amenity.amenity_id)).scalar() or 0
                
                # Delete the amenity
                db.session.delete(amenity)
                db.session.commit()
                
                # Reset auto-increment to the current max ID
                db.session.execute(db.text(f"ALTER TABLE amenities AUTO_INCREMENT = {max_id}"))
                db.session.commit()
                
                print(f"\n✅ Amenity '{amenity.name}' deleted successfully!")
            else:
                print("\nDeletion cancelled.")
            
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")

def main_menu():
    """Display the main menu"""
    while True:
        print("\nAmenity Management System")
        print("=" * 30)
        print("1. List All Amenities")
        print("2. Create New Amenity")
        print("3. View Amenity Details")
        print("4. Update Amenity")
        print("5. Delete Amenity")
        print("0. Exit")
        
        choice = input("\nEnter your choice (0-5): ")
        
        if choice == '1':
            list_amenities()
        elif choice == '2':
            create_amenity()
        elif choice == '3':
            read_amenity()
        elif choice == '4':
            update_amenity()
        elif choice == '5':
            delete_amenity()
        elif choice == '0':
            print("\nGoodbye!")
            break
        else:
            print("\n❌ Invalid choice. Please try again.")

if __name__ == '__main__':
    main_menu() 