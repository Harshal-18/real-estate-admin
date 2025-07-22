import sys
import os
from datetime import datetime

# Add parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models import Tower

app = create_app()

def list_towers():
    """List all towers"""
    with app.app_context():
        towers = Tower.query.all()
        if not towers:
            print("\nNo towers found.")
            return
        print("\nTower List:")
        print("=" * 50)
        for t in towers:
            print(f"Tower ID: {t.tower_id}, Name: {t.tower_name}, Floors: {t.total_floors}, Active: {'Yes' if t.is_active else 'No'}")
            print("-" * 50)

def create_tower():
    """Create a new tower record"""
    print("\nCreate New Tower")
    print("=" * 50)

    project_id = input("Project ID: ").strip()
    tower_name = input("Tower Name: ").strip()
    tower_number = input("Tower Number: ").strip()
    total_floors = input("Total Floors: ").strip()
    units_per_floor = input("Units per Floor: ").strip()
    total_units = input("Total Units: ").strip()
    tower_type = input("Tower Type: ").strip()
    construction_status = input("Construction Status: ").strip()
    possession_date = input("Possession Date (YYYY-MM-DD): ").strip()
    height_meters = input("Height (in meters): ").strip()
    elevator_count = input("Elevator Count: ").strip()
    has_power_backup = input("Power Backup? (1/0): ").strip() or "0"
    has_water_backup = input("Water Backup? (1/0): ").strip() or "0"
    has_fire_safety = input("Fire Safety? (1/0): ").strip() or "0"
    latitude = input("Latitude: ").strip()
    longitude = input("Longitude: ").strip()
    facing_direction = input("Facing Direction: ").strip()
    is_active = input("Is Active? (1/0): ").strip() or "1"

    try:
        possession_date_obj = datetime.strptime(possession_date, "%Y-%m-%d").date() if possession_date else None
    except ValueError:
        print("❌ Invalid date format. Use YYYY-MM-DD.")
        return

    try:
        with app.app_context():
            tower = Tower(
                project_id=int(project_id),
                tower_name=tower_name,
                tower_number=tower_number,
                total_floors=int(total_floors),
                units_per_floor=int(units_per_floor),
                total_units=int(total_units),
                tower_type=tower_type,
                construction_status=construction_status,
                possession_date=possession_date_obj,
                height_meters=float(height_meters),
                elevator_count=int(elevator_count),
                has_power_backup=bool(int(has_power_backup)),
                has_water_backup=bool(int(has_water_backup)),
                has_fire_safety=bool(int(has_fire_safety)),
                latitude=float(latitude),
                longitude=float(longitude),
                facing_direction=facing_direction,
                is_active=bool(int(is_active)),
                created_at=datetime.utcnow()
            )
            db.session.add(tower)
            db.session.commit()
            print(f"\n✅ Tower '{tower_name}' created successfully!")
    except Exception as e:
        print(f"\n❌ Error creating tower: {str(e)}")

def read_tower():
    """View tower details"""
    tower_id = input("\nEnter Tower ID to view: ").strip()
    with app.app_context():
        tower = Tower.query.get(tower_id)
        if not tower:
            print("\n❌ Tower not found!")
            return
        print("\nTower Details:")
        print("=" * 50)
        for column in tower.__table__.columns:
            print(f"{column.name}: {getattr(tower, column.name)}")

def update_tower():
    """Update an existing tower"""
    tower_id = input("\nEnter Tower ID to update: ").strip()
    with app.app_context():
        tower = Tower.query.get(tower_id)
        if not tower:
            print("\n❌ Tower not found!")
            return

        print("\nUpdate Tower (leave blank to keep current value)")
        tower.project_id = int(input(f"Project ID [{tower.project_id}]: ") or tower.project_id)
        tower.tower_name = input(f"Name [{tower.tower_name}]: ") or tower.tower_name
        tower.tower_number = input(f"Number [{tower.tower_number}]: ") or tower.tower_number
        tower.total_floors = int(input(f"Total Floors [{tower.total_floors}]: ") or tower.total_floors)
        tower.units_per_floor = int(input(f"Units/Floor [{tower.units_per_floor}]: ") or tower.units_per_floor)
        tower.total_units = int(input(f"Total Units [{tower.total_units}]: ") or tower.total_units)
        tower.tower_type = input(f"Type [{tower.tower_type}]: ") or tower.tower_type
        tower.construction_status = input(f"Construction Status [{tower.construction_status}]: ") or tower.construction_status

        possession_input = input(f"Possession Date [{tower.possession_date}]: ")
        if possession_input:
            try:
                tower.possession_date = datetime.strptime(possession_input, "%Y-%m-%d").date()
            except ValueError:
                print("❌ Invalid date format. Skipping possession date.")

        tower.height_meters = float(input(f"Height (m) [{tower.height_meters}]: ") or tower.height_meters)
        tower.elevator_count = int(input(f"Elevator Count [{tower.elevator_count}]: ") or tower.elevator_count)
        tower.has_power_backup = bool(int(input(f"Power Backup (1/0) [{int(tower.has_power_backup)}]: ") or int(tower.has_power_backup)))
        tower.has_water_backup = bool(int(input(f"Water Backup (1/0) [{int(tower.has_water_backup)}]: ") or int(tower.has_water_backup)))
        tower.has_fire_safety = bool(int(input(f"Fire Safety (1/0) [{int(tower.has_fire_safety)}]: ") or int(tower.has_fire_safety)))
        tower.latitude = float(input(f"Latitude [{tower.latitude}]: ") or tower.latitude)
        tower.longitude = float(input(f"Longitude [{tower.longitude}]: ") or tower.longitude)
        tower.facing_direction = input(f"Facing [{tower.facing_direction}]: ") or tower.facing_direction
        tower.is_active = bool(int(input(f"Is Active (1/0) [{int(tower.is_active)}]: ") or int(tower.is_active)))

        db.session.commit()
        print(f"\n✅ Tower ID {tower.tower_id} updated successfully!")

def delete_tower():
    """Delete a tower"""
    tower_id = input("\nEnter Tower ID to delete: ").strip()
    with app.app_context():
        tower = Tower.query.get(tower_id)
        if not tower:
            print("\n❌ Tower not found!")
            return

        confirm = input(f"Are you sure you want to delete tower '{tower.tower_name}'? (yes/no): ").lower()
        if confirm == 'yes':
            db.session.delete(tower)
            db.session.commit()
            print(f"\n✅ Tower ID {tower_id} deleted successfully!")
        else:
            print("\n❌ Deletion cancelled.")

def main_menu():
    while True:
        print("\nTowers Management System")
        print("=" * 30)
        print("1. List All Towers")
        print("2. Create New Tower")
        print("3. View Tower Details")
        print("4. Update Tower")
        print("5. Delete Tower")
        print("0. Exit")

        choice = input("Enter your choice (0-5): ")

        if choice == '1':
            list_towers()
        elif choice == '2':
            create_tower()
        elif choice == '3':
            read_tower()
        elif choice == '4':
            update_tower()
        elif choice == '5':
            delete_tower()
        elif choice == '0':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == '__main__':
    main_menu()
