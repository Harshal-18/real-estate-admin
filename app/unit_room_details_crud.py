import sys
import os
from datetime import datetime

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models import UnitRoomDetail

app = create_app()

def list_rooms():
    """List all room details"""
    with app.app_context():
        rooms = UnitRoomDetail.query.all()
        if not rooms:
            print("\nNo room details found.")
            return
        print("\nRoom Details:")
        print("=" * 50)
        for r in rooms:
            print(f"Room ID: {r.room_detail_id}, Unit Type ID: {r.unit_type_id}, Name: {r.room_name}, Type: {r.room_type}, Area: {r.room_area} sqft")
            print("-" * 50)

def create_room():
    """Create a new room detail record"""
    print("\nCreate New Room Detail")
    print("=" * 50)

    try:
        with app.app_context():
            room = UnitRoomDetail(
                unit_type_id=int(input("Unit Type ID: ").strip()),
                room_type=input("Room Type: ").strip(),
                room_name=input("Room Name: ").strip(),
                room_sequence=int(input("Room Sequence: ").strip()),
                room_length=float(input("Room Length (ft): ").strip()),
                room_width=float(input("Room Width (ft): ").strip()),
                room_area=float(input("Room Area (sqft): ").strip()),
                room_shape=input("Room Shape: ").strip(),
                has_attached_bathroom=bool(int(input("Has Attached Bathroom (1/0): ").strip())),
                has_balcony_access=bool(int(input("Has Balcony Access (1/0): ").strip())),
                has_wardrobe=bool(int(input("Has Wardrobe (1/0): ").strip())),
                wardrobe_type=input("Wardrobe Type: ").strip(),
                wardrobe_area=float(input("Wardrobe Area (sqft): ").strip()),
                has_window=bool(int(input("Has Window (1/0): ").strip())),
                window_count=int(input("Window Count: ").strip()),
                window_total_area=float(input("Window Total Area: ").strip()),
                natural_light_rating=input("Natural Light Rating: ").strip(),
                ventilation_rating=input("Ventilation Rating: ").strip(),
                door_count=int(input("Door Count: ").strip()),
                door_type=input("Door Type: ").strip(),
                door_material=input("Door Material: ").strip(),
                door_width=float(input("Door Width (ft): ").strip()),
                door_height=float(input("Door Height (ft): ").strip()),
                window_type=input("Window Type: ").strip(),
                window_material=input("Window Material: ").strip(),
                window_width=float(input("Window Width (ft): ").strip()),
                window_height=float(input("Window Height (ft): ").strip()),
                electrical_points=int(input("Electrical Points: ").strip()),
                fan_points=int(input("Fan Points: ").strip()),
                ac_points=int(input("AC Points: ").strip()),
                light_points=int(input("Light Points: ").strip()),
                flooring_type=input("Flooring Type: ").strip(),
                flooring_brand=input("Flooring Brand: ").strip(),
                ceiling_type=input("Ceiling Type: ").strip(),
                ceiling_height=float(input("Ceiling Height (ft): ").strip()),
                has_geyser_provision=bool(int(input("Geyser Provision (1/0): ").strip())),
                has_exhaust_fan=bool(int(input("Exhaust Fan (1/0): ").strip())),
                has_chimney_provision=bool(int(input("Chimney Provision (1/0): ").strip())),
                privacy_level=input("Privacy Level: ").strip(),
                position_in_unit=input("Position in Unit: ").strip(),
                created_at=datetime.utcnow()
            )
            db.session.add(room)
            db.session.commit()
            print("\n✅ Room detail created successfully!")
    except Exception as e:
        print(f"\n❌ Error creating room detail: {str(e)}")

def read_room():
    """View a room detail"""
    room_id = input("\nEnter Room Detail ID to view: ").strip()
    with app.app_context():
        room = UnitRoomDetail.query.get(room_id)
        if not room:
            print("\n❌ Room detail not found!")
            return
        print("\nRoom Detail:")
        print("=" * 50)
        for column in room.__table__.columns:
            print(f"{column.name}: {getattr(room, column.name)}")

def update_room():
    """Update an existing room detail"""
    room_id = input("\nEnter Room Detail ID to update: ").strip()
    with app.app_context():
        room = UnitRoomDetail.query.get(room_id)
        if not room:
            print("\n❌ Room detail not found!")
            return

        print("\nUpdate Room Detail (leave blank to keep current value)")
        room.room_name = input(f"Room Name [{room.room_name}]: ") or room.room_name
        room.room_type = input(f"Room Type [{room.room_type}]: ") or room.room_type
        room.room_area = float(input(f"Room Area [{room.room_area}]: ") or room.room_area)
        room.room_shape = input(f"Room Shape [{room.room_shape}]: ") or room.room_shape
        room.has_wardrobe = bool(int(input(f"Has Wardrobe (1/0) [{int(room.has_wardrobe)}]: ") or room.has_wardrobe))
        room.has_window = bool(int(input(f"Has Window (1/0) [{int(room.has_window)}]: ") or room.has_window))

        db.session.commit()
        print(f"\n✅ Room Detail ID {room.room_detail_id} updated successfully!")

def delete_room():
    """Delete a room detail"""
    room_id = input("\nEnter Room Detail ID to delete: ").strip()
    with app.app_context():
        room = UnitRoomDetail.query.get(room_id)
        if not room:
            print("\n❌ Room detail not found!")
            return

        confirm = input(f"Are you sure you want to delete room '{room.room_name}'? (yes/no): ").lower()
        if confirm == 'yes':
            db.session.delete(room)
            db.session.commit()
            print(f"\n✅ Room detail ID {room_id} deleted successfully!")
        else:
            print("\n❌ Deletion cancelled.")

def main_menu():
    while True:
        print("\nUnit Room Details Management")
        print("=" * 30)
        print("1. List All Room Details")
        print("2. Create New Room Detail")
        print("3. View Room Detail")
        print("4. Update Room Detail")
        print("5. Delete Room Detail")
        print("0. Exit")

        choice = input("Enter your choice (0-5): ")

        if choice == '1':
            list_rooms()
        elif choice == '2':
            create_room()
        elif choice == '3':
            read_room()
        elif choice == '4':
            update_room()
        elif choice == '5':
            delete_room()
        elif choice == '0':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == '__main__':
    main_menu()
