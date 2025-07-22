import sys
import os
from datetime import datetime

# Add parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models import ProjectDocument

app = create_app()

def list_documents():
    """List all project documents"""
    with app.app_context():
        docs = ProjectDocument.query.all()
        if not docs:
            print("\nNo project documents found.")
            return
        print("\nProject Documents List:")
        print("=" * 50)
        for doc in docs:
            print(f"Document ID: {doc.document_id}, Project ID: {doc.project_id}, Title: {doc.title}, Public: {'Yes' if doc.is_public else 'No'}")
            print("-" * 50)

def create_document():
    """Create a new project document"""
    print("\nCreate New Project Document")
    print("=" * 50)

    project_id = input("Project ID: ").strip()
    document_type = input("Document Type: ").strip()
    title = input("Title: ").strip()
    description = input("Description: ").strip()
    file_url = input("File URL: ").strip()
    file_size = input("File Size (bytes): ").strip()
    file_type = input("File Type (e.g. PDF, DOCX): ").strip()
    is_public = input("Is Public (1/0): ").strip() or "0"
    download_count = input("Download Count [0]: ").strip() or "0"

    try:
        with app.app_context():
            doc = ProjectDocument(
                project_id=int(project_id),
                document_type=document_type,
                title=title,
                description=description,
                file_url=file_url,
                file_size=int(file_size),
                file_type=file_type,
                is_public=bool(int(is_public)),
                download_count=int(download_count),
                created_at=datetime.utcnow()
            )
            db.session.add(doc)
            db.session.commit()
            print(f"\n✅ Document '{title}' added for Project ID {project_id}!")
    except Exception as e:
        print(f"\n❌ Error creating document: {str(e)}")

def read_document():
    """View a specific project document"""
    document_id = input("\nEnter Document ID to view: ").strip()
    with app.app_context():
        doc = ProjectDocument.query.get(document_id)
        if not doc:
            print("\n❌ Document not found!")
            return
        print("\nDocument Details:")
        print("=" * 50)
        for column in doc.__table__.columns:
            print(f"{column.name}: {getattr(doc, column.name)}")

def update_document():
    """Update an existing project document"""
    document_id = input("\nEnter Document ID to update: ").strip()
    with app.app_context():
        doc = ProjectDocument.query.get(document_id)
        if not doc:
            print("\n❌ Document not found!")
            return

        print("\nUpdate Document (leave blank to keep current value)")
        doc.project_id = int(input(f"Project ID [{doc.project_id}]: ") or doc.project_id)
        doc.document_type = input(f"Document Type [{doc.document_type}]: ") or doc.document_type
        doc.title = input(f"Title [{doc.title}]: ") or doc.title
        doc.description = input(f"Description [{doc.description or ''}]: ") or doc.description
        doc.file_url = input(f"File URL [{doc.file_url}]: ") or doc.file_url
        doc.file_size = int(input(f"File Size [{doc.file_size}]: ") or doc.file_size)
        doc.file_type = input(f"File Type [{doc.file_type}]: ") or doc.file_type
        doc.is_public = bool(int(input(f"Is Public (1/0) [{int(doc.is_public)}]: ") or int(doc.is_public)))
        doc.download_count = int(input(f"Download Count [{doc.download_count}]: ") or doc.download_count)

        db.session.commit()
        print(f"\n✅ Document ID {doc.document_id} updated successfully!")

def delete_document():
    """Delete a project document"""
    document_id = input("\nEnter Document ID to delete: ").strip()
    with app.app_context():
        doc = ProjectDocument.query.get(document_id)
        if not doc:
            print("\n❌ Document not found!")
            return

        confirm = input(f"Are you sure you want to delete document '{doc.title}'? (yes/no): ").lower()
        if confirm == 'yes':
            db.session.delete(doc)
            db.session.commit()
            print(f"\n✅ Document ID {doc.document_id} deleted successfully!")
        else:
            print("\n❌ Deletion cancelled.")

def main_menu():
    while True:
        print("\nProject Document Management")
        print("=" * 30)
        print("1. List All Documents")
        print("2. Create New Document")
        print("3. View Document Details")
        print("4. Update Document")
        print("5. Delete Document")
        print("0. Exit")

        choice = input("Enter your choice (0-5): ")

        if choice == '1':
            list_documents()
        elif choice == '2':
            create_document()
        elif choice == '3':
            read_document()
        elif choice == '4':
            update_document()
        elif choice == '5':
            delete_document()
        elif choice == '0':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == '__main__':
    main_menu()
