import sys
import os
from datetime import datetime

# Add the parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models import Approval

app = create_app()

def list_approvals():
    """List all approvals"""
    with app.app_context():
        approvals = Approval.query.all()
        if not approvals:
            print("\nNo approvals found.")
            return
        print("\nList of All Approvals:")
        print("=" * 50)
        for ap in approvals:
            print(f"Approval ID: {ap.approval_id}")
            print(f"Name: {ap.name}")
            print(f"Description: {ap.description}")
            print(f"Is Mandatory: {'Yes' if ap.is_mandatory else 'No'}")
            print(f"Category: {ap.category}")
            print(f"Created At: {ap.created_at}")
            print("-" * 50)

def create_approval():
    """Create a new approval"""
    print("\nCreate New Approval")
    print("=" * 50)

    name = input("Approval Name*: ").strip()
    while not name:
        name = input("Approval Name is required*: ").strip()

    description = input("Description: ")
    is_mandatory = input("Is Mandatory (1/0) [0]: ") or "0"
    while is_mandatory not in ['0', '1']:
        is_mandatory = input("Please enter 1 or 0: ")

    category = input("Category: ")

    try:
        with app.app_context():
            approval = Approval(
                name=name,
                description=description or None,
                is_mandatory=bool(int(is_mandatory)),
                category=category or None
            )
            db.session.add(approval)
            db.session.commit()
            print(f"\n✅ Approval '{name}' created successfully!")
    except Exception as e:
        print(f"\n❌ Error creating approval: {e}")

def read_approval():
    """Read approval details"""
    approval_id = input("\nEnter Approval ID: ").strip()
    with app.app_context():
        approval = Approval.query.get(approval_id)
        if not approval:
            print("\n❌ Approval not found!")
            return
        print("\nApproval Details:")
        print("=" * 50)
        print(f"ID: {approval.approval_id}")
        print(f"Name: {approval.name}")
        print(f"Description: {approval.description}")
        print(f"Is Mandatory: {'Yes' if approval.is_mandatory else 'No'}")
        print(f"Category: {approval.category}")
        print(f"Created At: {approval.created_at}")

def update_approval():
    """Update an existing approval"""
    approval_id = input("\nEnter Approval ID to update: ").strip()
    with app.app_context():
        approval = Approval.query.get(approval_id)
        if not approval:
            print("\n❌ Approval not found!")
            return

        print("\nUpdate Approval (Leave blank to keep current value)")
        name = input(f"Name [{approval.name}]: ") or approval.name
        description = input(f"Description [{approval.description}]: ") or approval.description
        is_mandatory = input(f"Is Mandatory (1/0) [{'1' if approval.is_mandatory else '0'}]: ") or str(int(approval.is_mandatory))
        while is_mandatory not in ['0', '1']:
            is_mandatory = input("Please enter 1 or 0: ")

        category = input(f"Category [{approval.category}]: ") or approval.category

        approval.name = name
        approval.description = description
        approval.is_mandatory = bool(int(is_mandatory))
        approval.category = category

        db.session.commit()
        print(f"\n✅ Approval '{approval.name}' updated successfully!")

def delete_approval():
    """Delete an approval"""
    approval_id = input("\nEnter Approval ID to delete: ").strip()
    with app.app_context():
        approval = Approval.query.get(approval_id)
        if not approval:
            print("\n❌ Approval not found!")
            return

        confirm = input(f"Are you sure you want to delete approval '{approval.name}'? (yes/no): ").lower()
        if confirm == 'yes':
            db.session.delete(approval)
            db.session.commit()
            print(f"\n✅ Approval '{approval.name}' deleted successfully!")
        else:
            print("\nDeletion cancelled.")

def main_menu():
    while True:
        print("\nApproval Management System")
        print("=" * 30)
        print("1. List All Approvals")
        print("2. Create New Approval")
        print("3. View Approval Details")
        print("4. Update Approval")
        print("5. Delete Approval")
        print("0. Exit")

        choice = input("Enter your choice (0-5): ")

        if choice == '1':
            list_approvals()
        elif choice == '2':
            create_approval()
        elif choice == '3':
            read_approval()
        elif choice == '4':
            update_approval()
        elif choice == '5':
            delete_approval()
        elif choice == '0':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == '__main__':
    main_menu()
