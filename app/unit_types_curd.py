import sys
import os
from datetime import datetime

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models import UnitType

app = create_app()

def list_unit_types():
    """List all unit types"""
    with app.app_context():
        units = UnitType.query.all()
        if not units:
            print("\nNo unit types found.")
            return
        print("\nUnit Types:")
        print("=" * 50)
        for u in units:
            print(f"ID: {u.unit_type_id}, Project: {u.project_id}, Type: {u.type_name}, Area: {u.carpet_area} sqft, Price: ₹{u.base_price}")
            print("-" * 50)

def create_unit_type():
    """Create a new unit type"""
    print("\nCreate New Unit Type")
    print("=" * 50)

    data = {}
    data["project_id"] = int(input("Project ID: "))
    data["type_name"] = input("Type Name (e.g. 2BHK): ")
    data["bedrooms"] = int(input("Bedrooms: "))
    data["bathrooms"] = int(input("Bathrooms: "))
    data["carpet_area"] = float(input("Carpet Area (sqft): "))
    data["built_up_area"] = float(input("Built-up Area (sqft): "))
    data["super_area"] = float(input("Super Area (sqft): "))
    data["base_price"] = float(input("Base Price (₹): "))
    data["price_per_sqft"] = float(input("Price per Sqft (₹): "))
    data["floor_plan_url"] = input("Floor Plan URL: ")
    data["is_active"] = bool(int(input("Is Active (1/0): ") or 1))

    try:
        with app.app_context():
            unit = UnitType(**data)
            db.session.add(unit)
            db.session.commit()
            print(f"\n✅ Unit type '{data['type_name']}' created successfully.")
    except Exception as e:
        print(f"\n❌ Error creating unit type: {str(e)}")

def read_unit_type():
    """Read unit type details"""
    unit_type_id = input("\nEnter Unit Type ID to view: ").strip()
    with app.app_context():
        unit = UnitType.query.get(unit_type_id)
        if not unit:
            print("\n❌ Unit type not found!")
            return
        print("\nUnit Type Details:")
        print("=" * 50)
        for column in unit.__table__.columns:
            print(f"{column.name}: {getattr(unit, column.name)}")

def update_unit_type():
    """Update unit type"""
    unit_type_id = input("\nEnter Unit Type ID to update: ").strip()
    with app.app_context():
        unit = UnitType.query.get(unit_type_id)
        if not unit:
            print("\n❌ Unit type not found!")
            return

        print("\nUpdate Unit Type (leave blank to keep existing)")
        unit.type_name = input(f"Type Name [{unit.type_name}]: ") or unit.type_name
        unit.bedrooms = int(input(f"Bedrooms [{unit.bedrooms}]: ") or unit.bedrooms)
        unit.bathrooms = int(input(f"Bathrooms [{unit.bathrooms}]: ") or unit.bathrooms)
        unit.carpet_area = float(input(f"Carpet Area [{unit.carpet_area}]: ") or unit.carpet_area)
        unit.base_price = float(input(f"Base Price (₹) [{unit.base_price}]: ") or unit.base_price)
        unit.is_active = bool(int(input(f"Is Active (1/0) [{int(unit.is_active)}]: ") or int(unit.is_active)))

        db.session.commit()
        print(f"\n✅ Unit Type ID {unit.unit_type_id} updated successfully.")

def delete_unit_type():
    """Delete a unit type"""
    unit_type_id = input("\nEnter Unit Type ID to delete: ").strip()
    with app.app_context():
        unit = UnitType.query.get(unit_type_id)
        if not unit:
            print("\n❌ Unit type not found!")
            return

        confirm = input(f"Are you sure you want to delete unit type '{unit.type_name}'? (yes/no): ").lower()
        if confirm == 'yes':
            db.session.delete(unit)
            db.session.commit()
            print(f"\n✅ Unit type '{unit.type_name}' deleted successfully.")
        else:
            print("\n❌ Deletion cancelled.")

def main_menu():
    while True:
        print("\nUnit Type Management")
        print("=" * 30)
        print("1. List All Unit Types")
        print("2. Create New Unit Type")
        print("3. View Unit Type Details")
        print("4. Update Unit Type")
        print("5. Delete Unit Type")
        print("0. Exit")

        choice = input("Enter your choice (0-5): ")

        if choice == '1':
            list_unit_types()
        elif choice == '2':
            create_unit_type()
        elif choice == '3':
            read_unit_type()
        elif choice == '4':
            update_unit_type()
        elif choice == '5':
            delete_unit_type()
        elif choice == '0':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == '__main__':
    main_menu()
