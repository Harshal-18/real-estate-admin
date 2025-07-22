import sys
import os
from datetime import datetime

# Add parent directory to sys path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models import UserInterest

app = create_app()

def list_interests():
    """List all user interests"""
    with app.app_context():
        interests = UserInterest.query.all()
        if not interests:
            print("\nNo user interests found.")
            return
        print("\nUser Interests:")
        print("=" * 50)
        for interest in interests:
            print(f"Interest ID: {interest.interest_id}, User ID: {interest.user_id}, Project ID: {interest.project_id}, Type: {interest.interest_type}")
            print("-" * 50)

def create_interest():
    """Create a new user interest"""
    print("\nCreate New User Interest")
    print("=" * 50)

    try:
        with app.app_context():
            interest = UserInterest(
                user_id=int(input("User ID: ").strip()),
                project_id=int(input("Project ID: ").strip()),
                unit_type_id=int(input("Unit Type ID: ").strip()),
                interest_type=input("Interest Type (e.g. buy, rent): ").strip(),
                preferred_contact_method=input("Preferred Contact Method (e.g. phone, email): ").strip(),
                preferred_contact_time=input("Preferred Contact Time (e.g. morning): ").strip(),
                budget_min=float(input("Budget Min (₹): ").strip()),
                budget_max=float(input("Budget Max (₹): ").strip()),
                preferred_floors=input("Preferred Floors (comma-separated): ").strip(),
                specific_requirements=input("Specific Requirements: ").strip(),
                status=input("Status (e.g. open, closed): ").strip(),
                assigned_to=int(input("Assigned To (User ID): ").strip()),
                notes=input("Additional Notes: ").strip(),
                created_at=datetime.utcnow()
            )
            db.session.add(interest)
            db.session.commit()
            print("\n✅ User interest created successfully!")
    except Exception as e:
        print(f"\n❌ Error creating interest: {str(e)}")

def read_interest():
    """View interest details"""
    interest_id = input("\nEnter Interest ID to view: ").strip()
    with app.app_context():
        interest = UserInterest.query.get(interest_id)
        if not interest:
            print("\n❌ Interest not found!")
            return
        print("\nInterest Details:")
        print("=" * 50)
        for column in interest.__table__.columns:
            print(f"{column.name}: {getattr(interest, column.name)}")

def update_interest():
    """Update an existing interest"""
    interest_id = input("\nEnter Interest ID to update: ").strip()
    with app.app_context():
        interest = UserInterest.query.get(interest_id)
        if not interest:
            print("\n❌ Interest not found!")
            return

        print("\nUpdate Fields (leave blank to keep current value)")
        interest.interest_type = input(f"Interest Type [{interest.interest_type}]: ") or interest.interest_type
        interest.status = input(f"Status [{interest.status}]: ") or interest.status
        interest.notes = input(f"Notes [{interest.notes or ''}]: ") or interest.notes
        interest.budget_min = float(input(f"Budget Min [{interest.budget_min}]: ") or interest.budget_min)
        interest.budget_max = float(input(f"Budget Max [{interest.budget_max}]: ") or interest.budget_max)

        db.session.commit()
        print(f"\n✅ Interest ID {interest.interest_id} updated successfully!")

def delete_interest():
    """Delete a user interest"""
    interest_id = input("\nEnter Interest ID to delete: ").strip()
    with app.app_context():
        interest = UserInterest.query.get(interest_id)
        if not interest:
            print("\n❌ Interest not found!")
            return

        confirm = input(f"Are you sure you want to delete interest ID {interest_id}? (yes/no): ").lower()
        if confirm == 'yes':
            db.session.delete(interest)
            db.session.commit()
            print(f"\n✅ Interest ID {interest_id} deleted successfully!")
        else:
            print("\n❌ Deletion cancelled.")

def main_menu():
    while True:
        print("\nUser Interests Management")
        print("=" * 30)
        print("1. List All Interests")
        print("2. Create New Interest")
        print("3. View Interest Details")
        print("4. Update Interest")
        print("5. Delete Interest")
        print("0. Exit")

        choice = input("Enter your choice (0-5): ")

        if choice == '1':
            list_interests()
        elif choice == '2':
            create_interest()
        elif choice == '3':
            read_interest()
        elif choice == '4':
            update_interest()
        elif choice == '5':
            delete_interest()
        elif choice == '0':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == '__main__':
    main_menu()
