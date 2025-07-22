import sys
import os
from datetime import datetime

# Add parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models import SearchLog

app = create_app()

def list_search_logs():
    """List all search logs"""
    with app.app_context():
        logs = SearchLog.query.all()
        if not logs:
            print("\nNo search logs found.")
            return
        print("\nSearch Logs:")
        print("=" * 50)
        for log in logs:
            print(f"Search ID: {log.search_id}, User ID: {log.user_id}, Query: '{log.search_query}', Results: {log.results_count}")
            print("-" * 50)

def create_search_log():
    """Create a new search log"""
    print("\nCreate New Search Log")
    print("=" * 50)

    try:
        with app.app_context():
            log = SearchLog(
                user_id=int(input("User ID: ").strip()),
                search_query=input("Search Query: ").strip(),
                filters_applied=input("Filters Applied: ").strip(),
                results_count=int(input("Results Count: ").strip()),
                clicked_project_id=int(input("Clicked Project ID: ").strip()),
                search_timestamp=datetime.utcnow(),
                session_id=input("Session ID: ").strip(),
                ip_address=input("IP Address: ").strip()
            )
            db.session.add(log)
            db.session.commit()
            print("\n✅ Search log created successfully!")
    except Exception as e:
        print(f"\n❌ Error creating search log: {str(e)}")

def read_search_log():
    """Read a specific search log"""
    search_id = input("\nEnter Search ID to view: ").strip()
    with app.app_context():
        log = SearchLog.query.get(search_id)
        if not log:
            print("\n❌ Search log not found!")
            return
        print("\nSearch Log Details:")
        print("=" * 50)
        for column in log.__table__.columns:
            print(f"{column.name}: {getattr(log, column.name)}")

def update_search_log():
    """Update a specific search log"""
    search_id = input("\nEnter Search ID to update: ").strip()
    with app.app_context():
        log = SearchLog.query.get(search_id)
        if not log:
            print("\n❌ Search log not found!")
            return

        print("\nUpdate Fields (leave blank to keep current value)")
        log.search_query = input(f"Search Query [{log.search_query}]: ") or log.search_query
        log.filters_applied = input(f"Filters Applied [{log.filters_applied}]: ") or log.filters_applied
        log.results_count = int(input(f"Results Count [{log.results_count}]: ") or log.results_count)
        log.clicked_project_id = int(input(f"Clicked Project ID [{log.clicked_project_id}]: ") or log.clicked_project_id)
        log.session_id = input(f"Session ID [{log.session_id}]: ") or log.session_id
        log.ip_address = input(f"IP Address [{log.ip_address}]: ") or log.ip_address

        db.session.commit()
        print(f"\n✅ Search log ID {log.search_id} updated successfully!")

def delete_search_log():
    """Delete a search log"""
    search_id = input("\nEnter Search ID to delete: ").strip()
    with app.app_context():
        log = SearchLog.query.get(search_id)
        if not log:
            print("\n❌ Search log not found!")
            return

        confirm = input(f"Are you sure you want to delete search log ID {log.search_id}? (yes/no): ").lower()
        if confirm == 'yes':
            db.session.delete(log)
            db.session.commit()
            print(f"\n✅ Search log ID {log.search_id} deleted successfully!")
        else:
            print("\n❌ Deletion cancelled.")

def main_menu():
    while True:
        print("\nSearch Logs Management")
        print("=" * 30)
        print("1. List All Search Logs")
        print("2. Create New Search Log")
        print("3. View Search Log")
        print("4. Update Search Log")
        print("5. Delete Search Log")
        print("0. Exit")

        choice = input("Enter your choice (0-5): ")

        if choice == '1':
            list_search_logs()
        elif choice == '2':
            create_search_log()
        elif choice == '3':
            read_search_log()
        elif choice == '4':
            update_search_log()
        elif choice == '5':
            delete_search_log()
        elif choice == '0':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == '__main__':
    main_menu()
