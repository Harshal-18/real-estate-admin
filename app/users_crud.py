import sys
import os
from datetime import datetime

# Add parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models import User

app = create_app()

def list_users():
    """List all users"""
    with app.app_context():
        users = User.query.all()
        if not users:
            print("\nNo users found.")
            return
        print("\nUser List:")
        print("=" * 50)
        for u in users:
            print(f"ID: {u.user_id}, Email: {u.email}, Name: {u.first_name} {u.last_name}, Verified: {u.is_verified}")
            print("-" * 50)

def create_user():
    """Create a new user"""
    print("\nCreate New User")
    print("=" * 50)

    email = input("Email: ").strip()
    phone = input("Phone: ").strip()
    password_hash = input("Password Hash: ").strip()
    first_name = input("First Name: ").strip()
    last_name = input("Last Name: ").strip()
    user_type = input("User Type (admin/customer/etc): ").strip()
    is_verified = input("Is Verified (1/0): ").strip() or "0"
    profile_image_url = input("Profile Image URL: ").strip()
    is_active = input("Is Active (1/0): ").strip() or "1"

    try:
        with app.app_context():
            user = User(
                email=email,
                phone=phone,
                password_hash=password_hash,
                first_name=first_name,
                last_name=last_name,
                user_type=user_type,
                is_verified=bool(int(is_verified)),
                profile_image_url=profile_image_url,
                is_active=bool(int(is_active)),
                created_at=datetime.utcnow(),
                last_login=None
            )
            db.session.add(user)
            db.session.commit()
            print(f"\n✅ User '{email}' created successfully!")
    except Exception as e:
        print(f"\n❌ Error creating user: {str(e)}")

def read_user():
    """View user details"""
    user_id = input("\nEnter User ID to view: ").strip()
    with app.app_context():
        user = User.query.get(user_id)
        if not user:
            print("\n❌ User not found!")
            return
        print("\nUser Details:")
        print("=" * 50)
        for column in user.__table__.columns:
            print(f"{column.name}: {getattr(user, column.name)}")

def update_user():
    """Update an existing user"""
    user_id = input("\nEnter User ID to update: ").strip()
    with app.app_context():
        user = User.query.get(user_id)
        if not user:
            print("\n❌ User not found!")
            return

        print("\nUpdate User (leave blank to keep current value)")
        user.email = input(f"Email [{user.email}]: ") or user.email
        user.phone = input(f"Phone [{user.phone}]: ") or user.phone
        user.password_hash = input(f"Password Hash [{user.password_hash[:8]}...]: ") or user.password_hash
        user.first_name = input(f"First Name [{user.first_name}]: ") or user.first_name
        user.last_name = input(f"Last Name [{user.last_name}]: ") or user.last_name
        user.user_type = input(f"User Type [{user.user_type}]: ") or user.user_type
        user.is_verified = bool(int(input(f"Is Verified (1/0) [{int(user.is_verified)}]: ") or int(user.is_verified)))
        user.profile_image_url = input(f"Profile Image URL [{user.profile_image_url}]: ") or user.profile_image_url
        user.is_active = bool(int(input(f"Is Active (1/0) [{int(user.is_active)}]: ") or int(user.is_active)))

        db.session.commit()
        print(f"\n✅ User ID {user.user_id} updated successfully!")

def delete_user():
    """Delete a user"""
    user_id = input("\nEnter User ID to delete: ").strip()
    with app.app_context():
        user = User.query.get(user_id)
        if not user:
            print("\n❌ User not found!")
            return

        confirm = input(f"Are you sure you want to delete user '{user.email}'? (yes/no): ").lower()
        if confirm == 'yes':
            db.session.delete(user)
            db.session.commit()
            print(f"\n✅ User ID {user.user_id} deleted successfully!")
        else:
            print("\n❌ Deletion cancelled.")

def main_menu():
    while True:
        print("\nUser Management")
        print("=" * 30)
        print("1. List All Users")
        print("2. Create New User")
        print("3. View User Details")
        print("4. Update User")
        print("5. Delete User")
        print("0. Exit")

        choice = input("Enter your choice (0-5): ")

        if choice == '1':
            list_users()
        elif choice == '2':
            create_user()
        elif choice == '3':
            read_user()
        elif choice == '4':
            update_user()
        elif choice == '5':
            delete_user()
        elif choice == '0':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == '__main__':
    main_menu()
