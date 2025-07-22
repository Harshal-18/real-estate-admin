import sys
import os
from datetime import datetime

# Add the parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models import PriceHistory

app = create_app()

def list_price_history():
    """List all price history records"""
    with app.app_context():
        records = PriceHistory.query.all()
        if not records:
            print("\nNo price history records found.")
            return
        print("\nPrice History Records:")
        print("=" * 50)
        for ph in records:
            print(f"ID: {ph.price_history_id}, Project ID: {ph.project_id}, Change: ₹{ph.old_price} → ₹{ph.new_price} ({ph.change_percentage}%)")
            print(f"Effective: {ph.effective_date}")
            print("-" * 50)

def create_price_history():
    """Create a new price history record"""
    print("\nCreate New Price History Record")
    print("=" * 50)

    project_id = input("Project ID: ").strip()
    unit_type_id = input("Unit Type ID: ").strip()
    old_price = input("Old Price (₹): ").strip()
    new_price = input("New Price (₹): ").strip()
    old_price_per_sqft = input("Old Price per Sqft: ").strip()
    new_price_per_sqft = input("New Price per Sqft: ").strip()
    change_percentage = input("Change Percentage (%): ").strip()
    change_reason = input("Reason for Change: ").strip()
    effective_date = input("Effective Date (YYYY-MM-DD): ").strip()

    try:
        effective_date_obj = datetime.strptime(effective_date, "%Y-%m-%d").date()
    except ValueError:
        print("❌ Invalid date format. Use YYYY-MM-DD.")
        return

    try:
        with app.app_context():
            record = PriceHistory(
                project_id=int(project_id),
                unit_type_id=int(unit_type_id),
                old_price=float(old_price),
                new_price=float(new_price),
                old_price_per_sqft=float(old_price_per_sqft),
                new_price_per_sqft=float(new_price_per_sqft),
                change_percentage=float(change_percentage),
                change_reason=change_reason,
                effective_date=effective_date_obj
            )
            db.session.add(record)
            db.session.commit()
            print(f"\n✅ Price history record created for project ID {project_id}!")
    except Exception as e:
        print(f"\n❌ Error creating price history record: {str(e)}")

def read_price_history():
    """Read a specific price history record"""
    record_id = input("\nEnter Price History ID to view: ").strip()
    with app.app_context():
        record = PriceHistory.query.get(record_id)
        if not record:
            print("\n❌ Record not found!")
            return
        print("\nPrice History Record:")
        print("=" * 50)
        for column in record.__table__.columns:
            print(f"{column.name}: {getattr(record, column.name)}")

def update_price_history():
    """Update an existing price history record"""
    record_id = input("\nEnter Price History ID to update: ").strip()
    with app.app_context():
        record = PriceHistory.query.get(record_id)
        if not record:
            print("\n❌ Record not found!")
            return

        print("\nUpdate Record (leave blank to keep current value)")
        record.project_id = int(input(f"Project ID [{record.project_id}]: ") or record.project_id)
        record.unit_type_id = int(input(f"Unit Type ID [{record.unit_type_id}]: ") or record.unit_type_id)
        record.old_price = float(input(f"Old Price [{record.old_price}]: ") or record.old_price)
        record.new_price = float(input(f"New Price [{record.new_price}]: ") or record.new_price)
        record.old_price_per_sqft = float(input(f"Old Price/Sqft [{record.old_price_per_sqft}]: ") or record.old_price_per_sqft)
        record.new_price_per_sqft = float(input(f"New Price/Sqft [{record.new_price_per_sqft}]: ") or record.new_price_per_sqft)
        record.change_percentage = float(input(f"Change % [{record.change_percentage}]: ") or record.change_percentage)
        record.change_reason = input(f"Change Reason [{record.change_reason}]: ") or record.change_reason

        eff_date = input(f"Effective Date (YYYY-MM-DD) [{record.effective_date}]: ")
        if eff_date:
            try:
                record.effective_date = datetime.strptime(eff_date, "%Y-%m-%d").date()
            except ValueError:
                print("❌ Invalid date format. Skipping effective date update.")

        db.session.commit()
        print(f"\n✅ Record ID {record.price_history_id} updated successfully!")

def delete_price_history():
    """Delete a price history record"""
    record_id = input("\nEnter Price History ID to delete: ").strip()
    with app.app_context():
        record = PriceHistory.query.get(record_id)
        if not record:
            print("\n❌ Record not found!")
            return

        confirm = input(f"Are you sure you want to delete this record? (yes/no): ").lower()
        if confirm == 'yes':
            db.session.delete(record)
            db.session.commit()
            print(f"\n✅ Record ID {record.price_history_id} deleted successfully!")
        else:
            print("\n❌ Deletion cancelled.")

def main_menu():
    while True:
        print("\nPrice History Management")
        print("=" * 30)
        print("1. List All Records")
        print("2. Create New Record")
        print("3. View Record Details")
        print("4. Update Record")
        print("5. Delete Record")
        print("0. Exit")

        choice = input("Enter your choice (0-5): ")

        if choice == '1':
            list_price_history()
        elif choice == '2':
            create_price_history()
        elif choice == '3':
            read_price_history()
        elif choice == '4':
            update_price_history()
        elif choice == '5':
            delete_price_history()
        elif choice == '0':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == '__main__':
    main_menu()
