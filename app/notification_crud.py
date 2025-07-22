import sys
import os
from datetime import datetime

# Add the parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models import Notification

app = create_app()

def list_notifications():
    """List all notifications"""
    with app.app_context():
        notifications = Notification.query.all()
        if not notifications:
            print("\nNo notifications found.")
            return
        print("\nList of All Notifications:")
        print("=" * 50)
        for n in notifications:
            print(f"ID: {n.notification_id}, Title: {n.title}, Sent: {n.is_sent}, Read: {n.is_read}")
            print("-" * 50)

def create_notification():
    """Create a new notification"""
    print("\nCreate New Notification")
    print("=" * 50)

    user_id = input("User ID: ").strip()
    type_ = input("Type: ").strip()
    title = input("Title: ").strip()
    message = input("Message: ").strip()
    related_project_id = input("Related Project ID (optional): ").strip()
    is_read = input("Is Read? (1/0): ").strip() or "0"
    is_sent = input("Is Sent? (1/0): ").strip() or "0"
    delivery_method = input("Delivery Method (e.g. Email, SMS): ").strip()

    try:
        with app.app_context():
            notification = Notification(
                user_id=int(user_id),
                type=type_,
                title=title,
                message=message,
                related_project_id=int(related_project_id) if related_project_id else None,
                is_read=bool(int(is_read)),
                is_sent=bool(int(is_sent)),
                delivery_method=delivery_method,
                created_at=datetime.utcnow(),
                read_at=None
            )
            db.session.add(notification)
            db.session.commit()
            print(f"\n✅ Notification '{title}' created successfully!")
    except Exception as e:
        print(f"\n❌ Error creating notification: {str(e)}")

def read_notification():
    """View a specific notification"""
    notification_id = input("\nEnter Notification ID to view: ").strip()
    with app.app_context():
        notification = Notification.query.get(notification_id)
        if not notification:
            print("\n❌ Notification not found!")
            return
        print("\nNotification Details:")
        print("=" * 50)
        for column in notification.__table__.columns:
            print(f"{column.name}: {getattr(notification, column.name)}")

def update_notification():
    """Update an existing notification"""
    notification_id = input("\nEnter Notification ID to update: ").strip()
    with app.app_context():
        notification = Notification.query.get(notification_id)
        if not notification:
            print("\n❌ Notification not found!")
            return

        print("\nUpdate Notification (leave blank to keep current value)")
        notification.user_id = int(input(f"User ID [{notification.user_id}]: ") or notification.user_id)
        notification.type = input(f"Type [{notification.type}]: ") or notification.type
        notification.title = input(f"Title [{notification.title}]: ") or notification.title
        notification.message = input(f"Message [{notification.message}]: ") or notification.message
        notification.related_project_id = int(input(f"Related Project ID [{notification.related_project_id or 'None'}]: ") or notification.related_project_id or 0)
        notification.is_read = bool(int(input(f"Is Read (1/0) [{int(notification.is_read)}]: ") or int(notification.is_read)))
        notification.is_sent = bool(int(input(f"Is Sent (1/0) [{int(notification.is_sent)}]: ") or int(notification.is_sent)))
        notification.delivery_method = input(f"Delivery Method [{notification.delivery_method}]: ") or notification.delivery_method
        read_at_input = input(f"Read At (YYYY-MM-DD HH:MM) or leave blank: ").strip()
        if read_at_input:
            try:
                notification.read_at = datetime.strptime(read_at_input, '%Y-%m-%d %H:%M')
            except ValueError:
                print("❌ Invalid datetime format. Skipping read_at update.")

        db.session.commit()
        print(f"\n✅ Notification ID '{notification.notification_id}' updated successfully!")

def delete_notification():
    """Delete a notification"""
    notification_id = input("\nEnter Notification ID to delete: ").strip()
    with app.app_context():
        notification = Notification.query.get(notification_id)
        if not notification:
            print("\n❌ Notification not found!")
            return

        confirm = input(f"Are you sure you want to delete notification '{notification.title}'? (yes/no): ").lower()
        if confirm == 'yes':
            db.session.delete(notification)
            db.session.commit()
            print(f"\n✅ Notification '{notification.title}' deleted successfully!")
        else:
            print("\n❌ Deletion cancelled.")

def main_menu():
    while True:
        print("\nNotification Management System")
        print("=" * 30)
        print("1. List All Notifications")
        print("2. Create New Notification")
        print("3. View Notification Details")
        print("4. Update Notification")
        print("5. Delete Notification")
        print("0. Exit")

        choice = input("Enter your choice (0-5): ")

        if choice == '1':
            list_notifications()
        elif choice == '2':
            create_notification()
        elif choice == '3':
            read_notification()
        elif choice == '4':
            update_notification()
        elif choice == '5':
            delete_notification()
        elif choice == '0':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == '__main__':
    main_menu()
