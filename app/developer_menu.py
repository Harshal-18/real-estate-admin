import mysql.connector
from mysql.connector import Error
from app.crud.developer_crud import DeveloperCRUD
import os
from datetime import datetime

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_database_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='real_estate_db',
            user='root',
            password='Harshal@18'
        )
        return connection
    except Error as e:
        print(f"Error connecting to database: {e}")
        return None

def display_menu():
    print("\nReal Estate Developer Management System")
    print("======================================")
    print("1. List All Developers")
    print("2. Create New Developer")
    print("3. View Developer Details")
    print("4. Update Developer")
    print("5. Delete Developer")
    print("6. Search Developers")
    print("7. View Developer Statistics")
    print("0. Exit")
    print("\nEnter your choice (0-7): ")

def list_developers(developer_crud):
    clear_screen()
    print("\nList of Developers")
    print("=================")
    
    page = 1
    per_page = 10
    while True:
        success, message, developers, pagination = developer_crud.get_all_developers(page, per_page)
        
        if not success:
            print(f"Error: {message}")
            return
        
        if not developers:
            print("No developers found.")
            return
        
        print("\nID  | Name                 | Contact Email          | Total Projects")
        print("-" * 65)
        
        for dev in developers:
            print(f"{dev['developer_id']:<4} | {dev['name'][:20]:<20} | {dev['contact_email'][:20]:<20} | {dev['total_projects']}")
        
        print(f"\nPage {page} of {pagination['total_pages']}")
        
        if pagination['total_pages'] > 1:
            choice = input("\nEnter 'n' for next page, 'p' for previous page, or any other key to return: ").lower()
            if choice == 'n' and page < pagination['total_pages']:
                page += 1
            elif choice == 'p' and page > 1:
                page -= 1
            else:
                break
        else:
            input("\nPress Enter to continue...")
            break

def create_developer(developer_crud):
    clear_screen()
    print("\nCreate New Developer")
    print("===================")
    
    developer_data = {
        'name': input("Enter developer name: ").strip(),
        'established_year': input("Enter established year (or press Enter to skip): ").strip(),
        'contact_email': input("Enter contact email: ").strip(),
        'contact_phone': input("Enter contact phone: ").strip(),
        'address': input("Enter address: ").strip(),
        'website_url': input("Enter website URL (or press Enter to skip): ").strip(),
        'description': input("Enter description: ").strip()
    }
    
    # Clean up empty values
    developer_data = {k: v for k, v in developer_data.items() if v}
    
    # Convert established_year to int if provided
    if 'established_year' in developer_data:
        try:
            developer_data['established_year'] = int(developer_data['established_year'])
        except ValueError:
            print("Invalid year format. Established year will be skipped.")
            del developer_data['established_year']
    
    success, message, developer_id = developer_crud.create_developer(developer_data)
    
    if success:
        print(f"\nSuccess! Developer created with ID: {developer_id}")
    else:
        print(f"\nError: {message}")
    
    input("\nPress Enter to continue...")

def view_developer_details(developer_crud):
    clear_screen()
    print("\nView Developer Details")
    print("=====================")
    
    developer_id = input("Enter developer ID: ").strip()
    
    try:
        developer_id = int(developer_id)
    except ValueError:
        print("Invalid ID format.")
        input("\nPress Enter to continue...")
        return
    
    success, message, developer = developer_crud.get_developer(developer_id)
    
    if not success:
        print(f"Error: {message}")
        input("\nPress Enter to continue...")
        return
    
    print("\nDeveloper Details:")
    print("=================")
    print(f"ID: {developer['developer_id']}")
    print(f"Name: {developer['name']}")
    print(f"Established Year: {developer['established_year']}")
    print(f"Contact Email: {developer['contact_email']}")
    print(f"Contact Phone: {developer['contact_phone']}")
    print(f"Address: {developer['address']}")
    print(f"Website: {developer['website_url']}")
    print(f"Total Projects: {developer['total_projects']}")
    print(f"Completed Projects: {developer['completed_projects']}")
    print(f"Ongoing Projects: {developer['ongoing_projects']}")
    print(f"Rating: {developer['rating']}")
    print(f"Total Reviews: {developer['total_reviews']}")
    print(f"Verified: {'Yes' if developer['is_verified'] else 'No'}")
    print(f"Created At: {developer['created_at']}")
    
    # Get and display statistics
    success, message, stats = developer_crud.get_developer_statistics(developer_id)
    if success and stats:
        print("\nProject Statistics:")
        print("==================")
        print("Project Types:")
        for ptype, count in stats['project_types'].items():
            print(f"  {ptype}: {count}")
        print(f"\nAverage Minimum Price: {stats['price_statistics']['average_min_price']:,.2f}")
        print(f"Average Maximum Price: {stats['price_statistics']['average_max_price']:,.2f}")
    
    input("\nPress Enter to continue...")

def update_developer(developer_crud):
    clear_screen()
    print("\nUpdate Developer")
    print("===============")
    
    developer_id = input("Enter developer ID: ").strip()
    
    try:
        developer_id = int(developer_id)
    except ValueError:
        print("Invalid ID format.")
        input("\nPress Enter to continue...")
        return
    
    # First, get current developer data
    success, message, developer = developer_crud.get_developer(developer_id)
    
    if not success:
        print(f"Error: {message}")
        input("\nPress Enter to continue...")
        return
    
    print("\nCurrent values (press Enter to keep current value):")
    update_data = {}
    
    name = input(f"Name [{developer['name']}]: ").strip()
    if name:
        update_data['name'] = name
    
    established_year = input(f"Established Year [{developer['established_year']}]: ").strip()
    if established_year:
        try:
            update_data['established_year'] = int(established_year)
        except ValueError:
            print("Invalid year format. This field will not be updated.")
    
    contact_email = input(f"Contact Email [{developer['contact_email']}]: ").strip()
    if contact_email:
        update_data['contact_email'] = contact_email
    
    contact_phone = input(f"Contact Phone [{developer['contact_phone']}]: ").strip()
    if contact_phone:
        update_data['contact_phone'] = contact_phone
    
    address = input(f"Address [{developer['address']}]: ").strip()
    if address:
        update_data['address'] = address
    
    website_url = input(f"Website URL [{developer['website_url']}]: ").strip()
    if website_url:
        update_data['website_url'] = website_url
    
    description = input(f"Description: ").strip()
    if description:
        update_data['description'] = description
    
    if update_data:
        success, message = developer_crud.update_developer(developer_id, update_data)
        if success:
            print("\nDeveloper updated successfully!")
        else:
            print(f"\nError: {message}")
    else:
        print("\nNo changes made.")
    
    input("\nPress Enter to continue...")

def delete_developer(developer_crud):
    clear_screen()
    print("\nDelete Developer")
    print("===============")
    
    developer_id = input("Enter developer ID: ").strip()
    
    try:
        developer_id = int(developer_id)
    except ValueError:
        print("Invalid ID format.")
        input("\nPress Enter to continue...")
        return
    
    # First, get developer details
    success, message, developer = developer_crud.get_developer(developer_id)
    
    if not success:
        print(f"Error: {message}")
        input("\nPress Enter to continue...")
        return
    
    print(f"\nYou are about to delete developer:")
    print(f"ID: {developer['developer_id']}")
    print(f"Name: {developer['name']}")
    print(f"Total Projects: {developer['total_projects']}")
    
    confirm = input("\nAre you sure you want to delete this developer? (yes/no): ").lower()
    
    if confirm == 'yes':
        success, message = developer_crud.delete_developer(developer_id)
        if success:
            print("\nDeveloper deleted successfully!")
        else:
            print(f"\nError: {message}")
    else:
        print("\nDeletion cancelled.")
    
    input("\nPress Enter to continue...")

def search_developers(developer_crud):
    clear_screen()
    print("\nSearch Developers")
    print("================")
    
    search_term = input("Enter search term (name, email, or address): ").strip()
    
    if not search_term:
        print("Search term cannot be empty.")
        input("\nPress Enter to continue...")
        return
    
    page = 1
    per_page = 10
    while True:
        success, message, developers, pagination = developer_crud.search_developers(
            search_term, page, per_page
        )
        
        if not success:
            print(f"Error: {message}")
            break
        
        if not developers:
            print("No developers found matching your search.")
            break
        
        print("\nSearch Results:")
        print("ID  | Name                 | Contact Email          | Total Projects")
        print("-" * 65)
        
        for dev in developers:
            print(f"{dev['developer_id']:<4} | {dev['name'][:20]:<20} | {dev['contact_email'][:20]:<20} | {dev['total_projects']}")
        
        print(f"\nPage {page} of {pagination['total_pages']}")
        
        if pagination['total_pages'] > 1:
            choice = input("\nEnter 'n' for next page, 'p' for previous page, or any other key to return: ").lower()
            if choice == 'n' and page < pagination['total_pages']:
                page += 1
            elif choice == 'p' and page > 1:
                page -= 1
            else:
                break
        else:
            break
    
    input("\nPress Enter to continue...")

def main():
    connection = get_database_connection()
    if not connection:
        print("Could not connect to database. Exiting...")
        return
    
    developer_crud = DeveloperCRUD(connection)
    
    while True:
        clear_screen()
        display_menu()
        
        choice = input().strip()
        
        if choice == '0':
            break
        elif choice == '1':
            list_developers(developer_crud)
        elif choice == '2':
            create_developer(developer_crud)
        elif choice == '3':
            view_developer_details(developer_crud)
        elif choice == '4':
            update_developer(developer_crud)
        elif choice == '5':
            delete_developer(developer_crud)
        elif choice == '6':
            search_developers(developer_crud)
        elif choice == '7':
            view_developer_details(developer_crud)  # This shows statistics too
        else:
            print("\nInvalid choice. Please try again.")
            input("\nPress Enter to continue...")
    
    connection.close()
    print("\nThank you for using the Developer Management System!")

if __name__ == "__main__":
    main() 