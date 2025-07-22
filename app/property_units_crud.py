import sys
import os
from datetime import datetime, date, timezone

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models import PropertyUnit

app = create_app()

def list_units():
    """List all property units"""
    with app.app_context():
        units = PropertyUnit.query.all()
        if not units:
            print("\nNo property units found.")
            return
        print("\nProperty Units:")
        print("=" * 50)
        for u in units:
            print(f"Unit ID: {u.unit_id}, Project ID: {u.project_id}, Unit No: {u.unit_number}, Price: ₹{u.unit_price}")
            print("-" * 50)

def create_unit():
    """Create a new property unit"""
    print("\nCreate New Property Unit")
    print("=" * 50)

    try:
        with app.app_context():
            unit = PropertyUnit(
                project_id=int(input("Project ID: ").strip()),
                unit_type_id=int(input("Unit Type ID: ").strip()),
                tower_id=int(input("Tower ID: ").strip()),
                unit_number=input("Unit Number: ").strip(),
                floor_number=int(input("Floor Number: ").strip()),
                unit_position=input("Unit Position: ").strip(),
                wing=input("Wing: ").strip(),
                carpet_area=float(input("Carpet Area (sqft): ").strip()),
                built_up_area=float(input("Built-up Area (sqft): ").strip()),
                super_area=float(input("Super Area (sqft): ").strip()),
                has_corner_unit=bool(int(input("Has Corner Unit (1/0): ").strip())),
                has_extra_balcony=bool(int(input("Has Extra Balcony (1/0): ").strip())),
                has_servant_quarter=bool(int(input("Has Servant Quarter (1/0): ").strip())),
                unit_price=float(input("Unit Price (₹): ").strip()),
                price_per_sqft=float(input("Price per Sqft (₹): ").strip()),
                maintenance_charge=float(input("Maintenance Charge (₹): ").strip()),
                status=input("Status (e.g. available, sold): ").strip(),
                possession_date=date.fromisoformat(input("Possession Date (YYYY-MM-DD): ").strip()),
                premium_percentage=float(input("Premium %: ").strip()),
                discount_percentage=float(input("Discount %: ").strip()),
                actual_facing_direction=input("Facing Direction: ").strip(),
                view_description=input("View Description: ").strip(),
                is_active=bool(int(input("Is Active (1/0): ").strip() or 1)),
                created_at=datetime.now(timezone.utc)
            )
            db.session.add(unit)
            db.session.commit()
            print("\n✅ Property unit created successfully!")
    except Exception as e:
        print(f"\n❌ Error creating unit: {str(e)}")

def read_unit():
    """Read unit details"""
    unit_id = input("\nEnter Unit ID to view: ").strip()
    with app.app_context():
        unit = PropertyUnit.query.get(unit_id)
        if not unit:
            print("\n❌ Unit not found!")
            return
        print("\nUnit Details:")
        print("=" * 50)
        for column in unit.__table__.columns:
            print(f"{column.name}: {getattr(unit, column.name)}")

def update_unit():
    """Update a property unit"""
    unit_id = input("\nEnter Unit ID to update: ").strip()
    with app.app_context():
        unit = PropertyUnit.query.get(unit_id)
        if not unit:
            print("\n❌ Unit not found!")
            return

        print("\nUpdate Unit (leave blank to keep current value)")
        unit.unit_number = input(f"Unit Number [{unit.unit_number}]: ") or unit.unit_number
        unit.unit_price = float(input(f"Unit Price (₹) [{unit.unit_price}]: ") or unit.unit_price)
        unit.status = input(f"Status [{unit.status}]: ") or unit.status
        unit.is_active = bool(int(input(f"Is Active (1/0) [{int(unit.is_active)}]: ") or int(unit.is_active)))

        db.session.commit()
        print(f"\n✅ Unit ID {unit.unit_id} updated successfully!")

def delete_unit():
    """Delete a property unit"""
    unit_id = input("\nEnter Unit ID to delete: ").strip()
    with app.app_context():
        unit = PropertyUnit.query.get(unit_id)
        if not unit:
            print("\n❌ Unit not found!")
            return

        confirm = input(f"Are you sure you want to delete unit '{unit.unit_number}'? (yes/no): ").lower()
        if confirm == 'yes':
            db.session.delete(unit)
            db.session.commit()
            print(f"\n✅ Unit ID {unit.unit_id} deleted successfully!")
        else:
            print("\n❌ Deletion cancelled.")

def main_menu():
    while True:
        print("\nProperty Units Management")
        print("=" * 30)
        print("1. List All Units")
        print("2. Create New Unit")
        print("3. View Unit Details")
        print("4. Update Unit")
        print("5. Delete Unit")
        print("0. Exit")

        choice = input("Enter your choice (0-5): ")

        if choice == '1':
            list_units()
        elif choice == '2':
            create_unit()
        elif choice == '3':
            read_unit()
        elif choice == '4':
            update_unit()
        elif choice == '5':
            delete_unit()
        elif choice == '0':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == '__main__':
    main_menu()
