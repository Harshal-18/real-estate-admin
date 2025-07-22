import sys
import os
from datetime import datetime

# Add parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models import PropertyComparison

app = create_app()

def list_comparisons():
    """List all property comparisons"""
    with app.app_context():
        comparisons = PropertyComparison.query.all()
        if not comparisons:
            print("\nNo property comparisons found.")
            return
        print("\nProperty Comparisons List:")
        print("=" * 50)
        for comp in comparisons:
            print(f"Comparison ID: {comp.comparison_id}, User ID: {comp.user_id}, Session: {comp.session_id}")
            print("-" * 50)

def create_comparison():
    """Create a new property comparison"""
    print("\nCreate New Property Comparison")
    print("=" * 50)

    user_id = input("User ID: ").strip()
    project_ids = input("Project IDs (comma-separated): ").strip()
    comparison_parameters = input("Comparison Parameters (JSON or text): ").strip()
    session_id = input("Session ID: ").strip()

    try:
        with app.app_context():
            record = PropertyComparison(
                user_id=int(user_id),
                project_ids=project_ids,
                comparison_parameters=comparison_parameters,
                session_id=session_id,
                created_at=datetime.utcnow()
            )
            db.session.add(record)
            db.session.commit()
            print(f"\n✅ Comparison created for User ID {user_id}.")
    except Exception as e:
        print(f"\n❌ Error creating property comparison: {str(e)}")

def read_comparison():
    """View a specific property comparison"""
    comparison_id = input("\nEnter Comparison ID to view: ").strip()
    with app.app_context():
        comp = PropertyComparison.query.get(comparison_id)
        if not comp:
            print("\n❌ Comparison not found!")
            return
        print("\nProperty Comparison Details:")
        print("=" * 50)
        for column in comp.__table__.columns:
            print(f"{column.name}: {getattr(comp, column.name)}")

def update_comparison():
    """Update a property comparison"""
    comparison_id = input("\nEnter Comparison ID to update: ").strip()
    with app.app_context():
        comp = PropertyComparison.query.get(comparison_id)
        if not comp:
            print("\n❌ Comparison not found!")
            return

        print("\nUpdate Comparison (leave blank to keep current value)")
        comp.user_id = int(input(f"User ID [{comp.user_id}]: ") or comp.user_id)
        comp.project_ids = input(f"Project IDs [{comp.project_ids}]: ") or comp.project_ids
        comp.comparison_parameters = input(f"Comparison Parameters [{comp.comparison_parameters[:30]}...]: ") or comp.comparison_parameters
        comp.session_id = input(f"Session ID [{comp.session_id}]: ") or comp.session_id

        db.session.commit()
        print(f"\n✅ Comparison ID {comp.comparison_id} updated successfully!")

def delete_comparison():
    """Delete a property comparison"""
    comparison_id = input("\nEnter Comparison ID to delete: ").strip()
    with app.app_context():
        comp = PropertyComparison.query.get(comparison_id)
        if not comp:
            print("\n❌ Comparison not found!")
            return

        confirm = input(f"Are you sure you want to delete this comparison? (yes/no): ").lower()
        if confirm == 'yes':
            db.session.delete(comp)
            db.session.commit()
            print(f"\n✅ Comparison ID {comparison_id} deleted successfully!")
        else:
            print("\n❌ Deletion cancelled.")

def main_menu():
    while True:
        print("\nProperty Comparisons Management")
        print("=" * 30)
        print("1. List All Comparisons")
        print("2. Create New Comparison")
        print("3. View Comparison Details")
        print("4. Update Comparison")
        print("5. Delete Comparison")
        print("0. Exit")

        choice = input("Enter your choice (0-5): ")

        if choice == '1':
            list_comparisons()
        elif choice == '2':
            create_comparison()
        elif choice == '3':
            read_comparison()
        elif choice == '4':
            update_comparison()
        elif choice == '5':
            delete_comparison()
        elif choice == '0':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == '__main__':
    main_menu()
