import sys
import os
from datetime import datetime

# Add the parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models import ProjectAmenity

app = create_app()

def list_project_amenities():
    """List all project amenities"""
    with app.app_context():
        records = ProjectAmenity.query.all()
        if not records:
            print("\nNo project amenities found.")
            return
        print("\nProject Amenities List:")
        print("=" * 50)
        for pa in records:
            print(f"Project ID: {pa.project_id}, Amenity ID: {pa.amenity_id}, Available: {'Yes' if pa.is_available else 'No'}")
            print(f"Area: {pa.area_size} sqft, Capacity: {pa.capacity}, Hours: {pa.operating_hours}")
            print("-" * 50)

def create_project_amenity():
    """Create a new project amenity record"""
    print("\nCreate New Project Amenity")
    print("=" * 50)

    project_id = input("Project ID: ").strip()
    amenity_id = input("Amenity ID: ").strip()
    is_available = input("Is Available? (1/0): ").strip() or "0"
    description = input("Description: ").strip()
    area_size = input("Area Size (sqft): ").strip()
    capacity = input("Capacity: ").strip()
    operating_hours = input("Operating Hours: ").strip()

    try:
        with app.app_context():
            record = ProjectAmenity(
                project_id=int(project_id),
                amenity_id=int(amenity_id),
                is_available=bool(int(is_available)),
                description=description,
                area_size=float(area_size),
                capacity=int(capacity),
                operating_hours=operating_hours,
                created_at=datetime.utcnow()
            )
            db.session.add(record)
            db.session.commit()
            print(f"\n✅ Amenity ID {amenity_id} added to Project ID {project_id} successfully!")
    except Exception as e:
        print(f"\n❌ Error creating project amenity: {str(e)}")

def read_project_amenity():
    """Read specific project amenity"""
    project_id = input("\nEnter Project ID: ").strip()
    amenity_id = input("Enter Amenity ID: ").strip()
    with app.app_context():
        record = ProjectAmenity.query.get((project_id, amenity_id))
        if not record:
            print("\n❌ Project Amenity not found!")
            return
        print("\nProject Amenity Details:")
        print("=" * 50)
        for column in record.__table__.columns:
            print(f"{column.name}: {getattr(record, column.name)}")

def update_project_amenity():
    """Update an existing project amenity"""
    project_id = input("\nEnter Project ID to update: ").strip()
    amenity_id = input("Enter Amenity ID to update: ").strip()
    with app.app_context():
        record = ProjectAmenity.query.get((project_id, amenity_id))
        if not record:
            print("\n❌ Project Amenity not found!")
            return

        print("\nUpdate Record (leave blank to keep current value)")
        record.is_available = bool(int(input(f"Is Available (1/0) [{int(record.is_available)}]: ") or int(record.is_available)))
        record.description = input(f"Description [{record.description or ''}]: ") or record.description
        record.area_size = float(input(f"Area Size [{record.area_size}]: ") or record.area_size)
        record.capacity = int(input(f"Capacity [{record.capacity}]: ") or record.capacity)
        record.operating_hours = input(f"Operating Hours [{record.operating_hours}]: ") or record.operating_hours

        db.session.commit()
        print(f"\n✅ Project Amenity updated for Project ID {project_id} and Amenity ID {amenity_id}!")

def delete_project_amenity():
    """Delete a project amenity"""
    project_id = input("\nEnter Project ID to delete: ").strip()
    amenity_id = input("Enter Amenity ID to delete: ").strip()
    with app.app_context():
        record = ProjectAmenity.query.get((project_id, amenity_id))
        if not record:
            print("\n❌ Project Amenity not found!")
            return

        confirm = input(f"Are you sure you want to delete this record? (yes/no): ").lower()
        if confirm == 'yes':
            db.session.delete(record)
            db.session.commit()
            print(f"\n✅ Amenity ID {amenity_id} removed from Project ID {project_id}!")
        else:
            print("\n❌ Deletion cancelled.")

def main_menu():
    while True:
        print("\nProject Amenities Management")
        print("=" * 30)
        print("1. List All Amenities")
        print("2. Create New Amenity Record")
        print("3. View Amenity Details")
        print("4. Update Amenity")
        print("5. Delete Amenity")
        print("0. Exit")

        choice = input("Enter your choice (0-5): ")

        if choice == '1':
            list_project_amenities()
        elif choice == '2':
            create_project_amenity()
        elif choice == '3':
            read_project_amenity()
        elif choice == '4':
            update_project_amenity()
        elif choice == '5':
            delete_project_amenity()
        elif choice == '0':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == '__main__':
    main_menu()
