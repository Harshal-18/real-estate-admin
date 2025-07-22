import sys
import os
from datetime import datetime

# Add the parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models import BalconyDetail

app = create_app()

def list_balconies():
    """List all balcony details"""
    with app.app_context():
        balconies = BalconyDetail.query.all()
        if not balconies:
            print("\nNo balcony records found.")
            return
        print("\nList of All Balcony Details:")
        print("=" * 50)
        for b in balconies:
            print(f"ID: {b.balcony_id}, Name: {b.balcony_name}, Area: {b.balcony_area} sqft, Facing: {b.facing_direction}")
            print("-" * 50)

def create_balcony():
    """Create a new balcony detail"""
    print("\nCreate New Balcony Detail")
    print("=" * 50)

    unit_type_id = input("Unit Type ID: ").strip()
    balcony_name = input("Balcony Name: ").strip()
    balcony_sequence = input("Balcony Sequence: ").strip()
    balcony_length = input("Balcony Length (ft): ").strip()
    balcony_width = input("Balcony Width (ft): ").strip()
    balcony_area = input("Balcony Area (sqft): ").strip()
    connected_room = input("Connected Room: ").strip()
    access_type = input("Access Type: ").strip()
    balcony_type = input("Balcony Type: ").strip()
    washing = input("Provision for Washing Machine (1/0): ").strip() or "0"
    drying = input("Provision for Drying (1/0): ").strip() or "0"
    safety = input("Has Safety Grill (1/0): ").strip() or "0"
    facing_direction = input("Facing Direction: ").strip()
    view_description = input("View Description: ").strip()
    floor_level = input("Floor Level: ").strip()

    try:
        with app.app_context():
            balcony = BalconyDetail(
                unit_type_id=int(unit_type_id),
                balcony_name=balcony_name,
                balcony_sequence=int(balcony_sequence),
                balcony_length=float(balcony_length),
                balcony_width=float(balcony_width),
                balcony_area=float(balcony_area),
                connected_room=connected_room,
                access_type=access_type,
                balcony_type=balcony_type,
                has_provision_for_washing_machine=bool(int(washing)),
                has_provision_for_drying=bool(int(drying)),
                has_safety_grill=bool(int(safety)),
                facing_direction=facing_direction,
                view_description=view_description,
                floor_level=floor_level
            )
            db.session.add(balcony)
            db.session.commit()
            print(f"\n✅ Balcony '{balcony_name}' created successfully!")
    except Exception as e:
        print(f"\n❌ Error creating balcony: {str(e)}")

def read_balcony():
    """View specific balcony details"""
    balcony_id = input("\nEnter Balcony ID: ").strip()
    with app.app_context():
        balcony = BalconyDetail.query.get(balcony_id)
        if not balcony:
            print("\n❌ Balcony not found!")
            return
        print("\nBalcony Details:")
        print("=" * 50)
        for column in balcony.__table__.columns:
            print(f"{column.name}: {getattr(balcony, column.name)}")

def update_balcony():
    """Update existing balcony detail"""
    balcony_id = input("\nEnter Balcony ID to update: ").strip()
    with app.app_context():
        balcony = BalconyDetail.query.get(balcony_id)
        if not balcony:
            print("\n❌ Balcony not found!")
            return

        print("\nUpdate Balcony (leave blank to keep current value)")
        balcony.balcony_name = input(f"Name [{balcony.balcony_name}]: ") or balcony.balcony_name
        balcony.unit_type_id = int(input(f"Unit Type ID [{balcony.unit_type_id}]: ") or balcony.unit_type_id)
        balcony.balcony_sequence = int(input(f"Sequence [{balcony.balcony_sequence}]: ") or balcony.balcony_sequence)
        balcony.balcony_length = float(input(f"Length [{balcony.balcony_length}]: ") or balcony.balcony_length)
        balcony.balcony_width = float(input(f"Width [{balcony.balcony_width}]: ") or balcony.balcony_width)
        balcony.balcony_area = float(input(f"Area [{balcony.balcony_area}]: ") or balcony.balcony_area)
        balcony.connected_room = input(f"Connected Room [{balcony.connected_room}]: ") or balcony.connected_room
        balcony.access_type = input(f"Access Type [{balcony.access_type}]: ") or balcony.access_type
        balcony.balcony_type = input(f"Balcony Type [{balcony.balcony_type}]: ") or balcony.balcony_type
        balcony.has_provision_for_washing_machine = bool(int(input(f"Washing Machine (1/0) [{int(balcony.has_provision_for_washing_machine)}]: ") or int(balcony.has_provision_for_washing_machine)))
        balcony.has_provision_for_drying = bool(int(input(f"Drying (1/0) [{int(balcony.has_provision_for_drying)}]: ") or int(balcony.has_provision_for_drying)))
        balcony.has_safety_grill = bool(int(input(f"Safety Grill (1/0) [{int(balcony.has_safety_grill)}]: ") or int(balcony.has_safety_grill)))
        balcony.facing_direction = input(f"Facing [{balcony.facing_direction}]: ") or balcony.facing_direction
        balcony.view_description = input(f"View Description [{balcony.view_description}]: ") or balcony.view_description
        balcony.floor_level = input(f"Floor Level [{balcony.floor_level}]: ") or balcony.floor_level

        db.session.commit()
        print(f"\n✅ Balcony '{balcony.balcony_name}' updated successfully!")

def delete_balcony():
    """Delete balcony detail"""
    balcony_id = input("\nEnter Balcony ID to delete: ").strip()
    with app.app_context():
        balcony = BalconyDetail.query.get(balcony_id)
        if not balcony:
            print("\n❌ Balcony not found!")
            return

        confirm = input(f"Are you sure you want to delete balcony '{balcony.balcony_name}'? (yes/no): ").lower()
        if confirm == 'yes':
            db.session.delete(balcony)
            db.session.commit()
            print(f"\n✅ Balcony '{balcony.balcony_name}' deleted successfully!")
        else:
            print("\n❌ Deletion cancelled.")

def main_menu():
    while True:
        print("\nBalcony Details Management")
        print("=" * 30)
        print("1. List All Balconies")
        print("2. Create New Balcony")
        print("3. View Balcony Details")
        print("4. Update Balcony")
        print("5. Delete Balcony")
        print("0. Exit")

        choice = input("Enter your choice (0-5): ")

        if choice == '1':
            list_balconies()
        elif choice == '2':
            create_balcony()
        elif choice == '3':
            read_balcony()
        elif choice == '4':
            update_balcony()
        elif choice == '5':
            delete_balcony()
        elif choice == '0':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == '__main__':
    main_menu()
