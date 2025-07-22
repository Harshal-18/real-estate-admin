import sys
import os
from datetime import datetime

# Add parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models import ProjectMedia

app = create_app()

def list_media():
    """List all project media entries"""
    with app.app_context():
        media = ProjectMedia.query.all()
        if not media:
            print("\nNo project media records found.")
            return
        print("\nProject Media List:")
        print("=" * 50)
        for m in media:
            print(f"Media ID: {m.media_id}, Project ID: {m.project_id}, Type: {m.media_type}, Title: {m.title}, Active: {'Yes' if m.is_active else 'No'}")
            print("-" * 50)

def create_media():
    """Create a new media record"""
    print("\nCreate New Project Media")
    print("=" * 50)

    project_id = input("Project ID: ").strip()
    media_type = input("Media Type (e.g., image, video): ").strip()
    media_url = input("Media URL: ").strip()
    thumbnail_url = input("Thumbnail URL: ").strip()
    title = input("Title: ").strip()
    description = input("Description: ").strip()
    media_category = input("Media Category (e.g., gallery, walkthrough): ").strip()
    is_active = input("Is Active (1/0): ").strip() or "1"

    try:
        with app.app_context():
            record = ProjectMedia(
                project_id=int(project_id),
                media_type=media_type,
                media_url=media_url,
                thumbnail_url=thumbnail_url,
                title=title,
                description=description,
                media_category=media_category,
                is_active=bool(int(is_active)),
                created_at=datetime.utcnow()
            )
            db.session.add(record)
            db.session.commit()
            print(f"\n✅ Media '{title}' added successfully for Project ID {project_id}!")
    except Exception as e:
        print(f"\n❌ Error creating media record: {str(e)}")

def read_media():
    """View specific media details"""
    media_id = input("\nEnter Media ID to view: ").strip()
    with app.app_context():
        media = ProjectMedia.query.get(media_id)
        if not media:
            print("\n❌ Media record not found!")
            return
        print("\nMedia Details:")
        print("=" * 50)
        for column in media.__table__.columns:
            print(f"{column.name}: {getattr(media, column.name)}")

def update_media():
    """Update an existing media record"""
    media_id = input("\nEnter Media ID to update: ").strip()
    with app.app_context():
        media = ProjectMedia.query.get(media_id)
        if not media:
            print("\n❌ Media record not found!")
            return

        print("\nUpdate Media (leave blank to keep current value)")
        media.project_id = int(input(f"Project ID [{media.project_id}]: ") or media.project_id)
        media.media_type = input(f"Media Type [{media.media_type}]: ") or media.media_type
        media.media_url = input(f"Media URL [{media.media_url}]: ") or media.media_url
        media.thumbnail_url = input(f"Thumbnail URL [{media.thumbnail_url}]: ") or media.thumbnail_url
        media.title = input(f"Title [{media.title}]: ") or media.title
        media.description = input(f"Description [{media.description or ''}]: ") or media.description
        media.media_category = input(f"Media Category [{media.media_category}]: ") or media.media_category
        media.is_active = bool(int(input(f"Is Active (1/0) [{int(media.is_active)}]: ") or int(media.is_active)))

        db.session.commit()
        print(f"\n✅ Media ID {media.media_id} updated successfully!")

def delete_media():
    """Delete a media record"""
    media_id = input("\nEnter Media ID to delete: ").strip()
    with app.app_context():
        media = ProjectMedia.query.get(media_id)
        if not media:
            print("\n❌ Media record not found!")
            return

        confirm = input(f"Are you sure you want to delete media titled '{media.title}'? (yes/no): ").lower()
        if confirm == 'yes':
            db.session.delete(media)
            db.session.commit()
            print(f"\n✅ Media ID {media.media_id} deleted successfully!")
        else:
            print("\n❌ Deletion cancelled.")

def main_menu():
    while True:
        print("\nProject Media Management")
        print("=" * 30)
        print("1. List All Media")
        print("2. Create New Media")
        print("3. View Media Details")
        print("4. Update Media")
        print("5. Delete Media")
        print("0. Exit")

        choice = input("Enter your choice (0-5): ")

        if choice == '1':
            list_media()
        elif choice == '2':
            create_media()
        elif choice == '3':
            read_media()
        elif choice == '4':
            update_media()
        elif choice == '5':
            delete_media()
        elif choice == '0':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == '__main__':
    main_menu()
