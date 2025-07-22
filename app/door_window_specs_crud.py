import sys
import os
from datetime import datetime

# Add the parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models import DoorWindowSpec

app = create_app()

def list_specs():
    """List all door/window specifications"""
    with app.app_context():
        specs = DoorWindowSpec.query.all()
        if not specs:
            print("\nNo specifications found.")
            return
        print("\nList of All Door/Window Specs:")
        print("=" * 50)
        for s in specs:
            print(f"Spec ID: {s.spec_id}, Item: {s.item_type}, Location: {s.location}, Brand: {s.brand}")
            print("-" * 50)

def create_spec():
    """Create a new door/window spec"""
    print("\nCreate New Door/Window Spec")
    print("=" * 50)

    unit_type_id = input("Unit Type ID: ").strip()
    item_type = input("Item Type (Door/Window): ").strip()
    location = input("Location: ").strip()
    width = input("Width (ft): ").strip()
    height = input("Height (ft): ").strip()
    thickness = input("Thickness (in): ").strip()
    material = input("Material: ").strip()
    finish = input("Finish: ").strip()
    brand = input("Brand: ").strip()
    grade = input("Grade: ").strip()
    is_security_door = input("Is Security Door (1/0): ").strip() or "0"
    has_grill = input("Has Grill (1/0): ").strip() or "0"
    opening_type = input("Opening Type: ").strip()
    lock_type = input("Lock Type: ").strip()
    handle_type = input("Handle Type: ").strip()
    handle_material = input("Handle Material: ").strip()
    glass_type = input("Glass Type: ").strip()
    glass_thickness = input("Glass Thickness: ").strip()

    try:
        with app.app_context():
            spec = DoorWindowSpec(
                unit_type_id=int(unit_type_id),
                item_type=item_type,
                location=location,
                width=float(width),
                height=float(height),
                thickness=float(thickness),
                material=material,
                finish=finish,
                brand=brand,
                grade=grade,
                is_security_door=bool(int(is_security_door)),
                has_grill=bool(int(has_grill)),
                opening_type=opening_type,
                lock_type=lock_type,
                handle_type=handle_type,
                handle_material=handle_material,
                glass_type=glass_type,
                glass_thickness=float(glass_thickness)
            )
            db.session.add(spec)
            db.session.commit()
            print(f"\n✅ Spec for '{item_type}' at '{location}' created successfully!")
    except Exception as e:
        print(f"\n❌ Error creating spec: {str(e)}")

def read_spec():
    """View a specific spec"""
    spec_id = input("\nEnter Spec ID to view: ").strip()
    with app.app_context():
        spec = DoorWindowSpec.query.get(spec_id)
        if not spec:
            print("\n❌ Spec not found!")
            return
        print("\nSpec Details:")
        print("=" * 50)
        for column in spec.__table__.columns:
            print(f"{column.name}: {getattr(spec, column.name)}")

def update_spec():
    """Update existing spec"""
    spec_id = input("\nEnter Spec ID to update: ").strip()
    with app.app_context():
        spec = DoorWindowSpec.query.get(spec_id)
        if not spec:
            print("\n❌ Spec not found!")
            return

        print("\nUpdate Spec (leave blank to keep current value)")
        spec.unit_type_id = int(input(f"Unit Type ID [{spec.unit_type_id}]: ") or spec.unit_type_id)
        spec.item_type = input(f"Item Type [{spec.item_type}]: ") or spec.item_type
        spec.location = input(f"Location [{spec.location}]: ") or spec.location
        spec.width = float(input(f"Width [{spec.width}]: ") or spec.width)
        spec.height = float(input(f"Height [{spec.height}]: ") or spec.height)
        spec.thickness = float(input(f"Thickness [{spec.thickness}]: ") or spec.thickness)
        spec.material = input(f"Material [{spec.material}]: ") or spec.material
        spec.finish = input(f"Finish [{spec.finish}]: ") or spec.finish
        spec.brand = input(f"Brand [{spec.brand}]: ") or spec.brand
        spec.grade = input(f"Grade [{spec.grade}]: ") or spec.grade
        spec.is_security_door = bool(int(input(f"Is Security Door (1/0) [{int(spec.is_security_door)}]: ") or int(spec.is_security_door)))
        spec.has_grill = bool(int(input(f"Has Grill (1/0) [{int(spec.has_grill)}]: ") or int(spec.has_grill)))
        spec.opening_type = input(f"Opening Type [{spec.opening_type}]: ") or spec.opening_type
        spec.lock_type = input(f"Lock Type [{spec.lock_type}]: ") or spec.lock_type
        spec.handle_type = input(f"Handle Type [{spec.handle_type}]: ") or spec.handle_type
        spec.handle_material = input(f"Handle Material [{spec.handle_material}]: ") or spec.handle_material
        spec.glass_type = input(f"Glass Type [{spec.glass_type}]: ") or spec.glass_type
        spec.glass_thickness = float(input(f"Glass Thickness [{spec.glass_thickness}]: ") or spec.glass_thickness)

        db.session.commit()
        print(f"\n✅ Spec ID '{spec.spec_id}' updated successfully!")

def delete_spec():
    """Delete a spec"""
    spec_id = input("\nEnter Spec ID to delete: ").strip()
    with app.app_context():
        spec = DoorWindowSpec.query.get(spec_id)
        if not spec:
            print("\n❌ Spec not found!")
            return

        confirm = input(f"Are you sure you want to delete spec for '{spec.item_type}' at '{spec.location}'? (yes/no): ").lower()
        if confirm == 'yes':
            db.session.delete(spec)
            db.session.commit()
            print(f"\n✅ Spec ID '{spec.spec_id}' deleted successfully!")
        else:
            print("\n❌ Deletion cancelled.")

def main_menu():
    while True:
        print("\nDoor/Window Specification Management")
        print("=" * 30)
        print("1. List All Specs")
        print("2. Create New Spec")
        print("3. View Spec Details")
        print("4. Update Spec")
        print("5. Delete Spec")
        print("0. Exit")

        choice = input("Enter your choice (0-5): ")

        if choice == '1':
            list_specs()
        elif choice == '2':
            create_spec()
        elif choice == '3':
            read_spec()
        elif choice == '4':
            update_spec()
        elif choice == '5':
            delete_spec()
        elif choice == '0':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == '__main__':
    main_menu()
