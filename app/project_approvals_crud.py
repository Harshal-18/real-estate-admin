import sys
import os
from datetime import datetime

# Add parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models import ProjectApproval

app = create_app()

def list_project_approvals():
    """List all project approval records"""
    with app.app_context():
        approvals = ProjectApproval.query.all()
        if not approvals:
            print("\nNo project approvals found.")
            return
        print("\nProject Approvals List:")
        print("=" * 50)
        for pa in approvals:
            print(f"Project ID: {pa.project_id}, Approval ID: {pa.approval_id}, Status: {pa.status}, Authority: {pa.issuing_authority}")
            print("-" * 50)

def create_project_approval():
    """Create a new project approval record"""
    print("\nCreate New Project Approval")
    print("=" * 50)

    project_id = input("Project ID: ").strip()
    approval_id = input("Approval ID: ").strip()
    status = input("Status: ").strip()
    approval_number = input("Approval Number: ").strip()
    approval_date = input("Approval Date (YYYY-MM-DD): ").strip()
    expiry_date = input("Expiry Date (YYYY-MM-DD): ").strip()
    issuing_authority = input("Issuing Authority: ").strip()
    document_url = input("Document URL: ").strip()
    notes = input("Notes: ").strip()

    try:
        approval_date_obj = datetime.strptime(approval_date, "%Y-%m-%d").date() if approval_date else None
        expiry_date_obj = datetime.strptime(expiry_date, "%Y-%m-%d").date() if expiry_date else None
    except ValueError:
        print("❌ Invalid date format. Use YYYY-MM-DD.")
        return

    try:
        with app.app_context():
            record = ProjectApproval(
                project_id=int(project_id),
                approval_id=int(approval_id),
                status=status,
                approval_number=approval_number,
                approval_date=approval_date_obj,
                expiry_date=expiry_date_obj,
                issuing_authority=issuing_authority,
                document_url=document_url,
                notes=notes,
                created_at=datetime.utcnow()
            )
            db.session.add(record)
            db.session.commit()
            print(f"\n✅ Project Approval added for Project ID {project_id} and Approval ID {approval_id}!")
    except Exception as e:
        print(f"\n❌ Error creating project approval: {str(e)}")

def read_project_approval():
    """View specific project approval"""
    project_id = input("\nEnter Project ID: ").strip()
    approval_id = input("Enter Approval ID: ").strip()
    with app.app_context():
        record = ProjectApproval.query.get((project_id, approval_id))
        if not record:
            print("\n❌ Project Approval not found!")
            return
        print("\nProject Approval Details:")
        print("=" * 50)
        for column in record.__table__.columns:
            print(f"{column.name}: {getattr(record, column.name)}")

def update_project_approval():
    """Update an existing project approval"""
    project_id = input("\nEnter Project ID to update: ").strip()
    approval_id = input("Enter Approval ID to update: ").strip()
    with app.app_context():
        record = ProjectApproval.query.get((project_id, approval_id))
        if not record:
            print("\n❌ Project Approval not found!")
            return

        print("\nUpdate Record (leave blank to keep current value)")
        record.status = input(f"Status [{record.status}]: ") or record.status
        record.approval_number = input(f"Approval Number [{record.approval_number}]: ") or record.approval_number

        approval_date = input(f"Approval Date (YYYY-MM-DD) [{record.approval_date}]: ")
        if approval_date:
            try:
                record.approval_date = datetime.strptime(approval_date, "%Y-%m-%d").date()
            except ValueError:
                print("❌ Invalid date format. Skipping approval date.")

        expiry_date = input(f"Expiry Date (YYYY-MM-DD) [{record.expiry_date}]: ")
        if expiry_date:
            try:
                record.expiry_date = datetime.strptime(expiry_date, "%Y-%m-%d").date()
            except ValueError:
                print("❌ Invalid date format. Skipping expiry date.")

        record.issuing_authority = input(f"Issuing Authority [{record.issuing_authority}]: ") or record.issuing_authority
        record.document_url = input(f"Document URL [{record.document_url}]: ") or record.document_url
        record.notes = input(f"Notes [{record.notes or ''}]: ") or record.notes

        db.session.commit()
        print(f"\n✅ Project Approval updated for Project ID {project_id} and Approval ID {approval_id}!")

def delete_project_approval():
    """Delete a project approval"""
    project_id = input("\nEnter Project ID to delete: ").strip()
    approval_id = input("Enter Approval ID to delete: ").strip()
    with app.app_context():
        record = ProjectApproval.query.get((project_id, approval_id))
        if not record:
            print("\n❌ Project Approval not found!")
            return

        confirm = input(f"Are you sure you want to delete this record? (yes/no): ").lower()
        if confirm == 'yes':
            db.session.delete(record)
            db.session.commit()
            print(f"\n✅ Approval ID {approval_id} removed from Project ID {project_id}!")
        else:
            print("\n❌ Deletion cancelled.")

def main_menu():
    while True:
        print("\nProject Approvals Management")
        print("=" * 30)
        print("1. List All Project Approvals")
        print("2. Create New Project Approval")
        print("3. View Approval Details")
        print("4. Update Approval")
        print("5. Delete Approval")
        print("0. Exit")

        choice = input("Enter your choice (0-5): ")

        if choice == '1':
            list_project_approvals()
        elif choice == '2':
            create_project_approval()
        elif choice == '3':
            read_project_approval()
        elif choice == '4':
            update_project_approval()
        elif choice == '5':
            delete_project_approval()
        elif choice == '0':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == '__main__':
    main_menu()
