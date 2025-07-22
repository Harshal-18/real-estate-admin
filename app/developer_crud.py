import sys
import os

# Add the parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models import Developer
from datetime import datetime

app = create_app()

def list_developers():
    """List all developers"""
    with app.app_context():
        developers = Developer.query.all()
        if not developers:
            print("\nNo developers found.")
            return
        
        print("\nList of All Developers:")
        print("=" * 50)
        for dev in developers:
            print(f"Developer ID: {dev.developer_id}")
            print(f"Name: {dev.name}")
            print(f"Contact Email: {dev.contact_email}")
            print(f"Total Projects: {dev.total_projects}")
            print(f"Rating: {dev.rating}")
            print("-" * 50)

def create_developer():
    """Create a new developer"""
    print("\nCreate New Developer")
    print("=" * 50)
    print("(Press Enter to skip optional fields)\n")
    
    # Required fields
    name = input("Developer Name*: ")
    while not name:
        print("Developer name is required!")
        name = input("Developer Name*: ")

    # Optional fields with validation
    established_year = input("Established Year: ")
    while established_year:
        try:
            year = int(established_year)
            current_year = datetime.now().year
            if year < 1800 or year > current_year:
                print(f"Year must be between 1800 and {current_year}")
                established_year = input("Established Year: ")
                continue
            break
        except ValueError:
            print("Please enter a valid year")
            established_year = input("Established Year: ")

    description = input("Description: ")
    logo_url = input("Logo URL: ")
    website_url = input("Website URL: ")
    
    contact_email = input("Contact Email: ")
    contact_phone = input("Contact Phone: ")
    address = input("Address: ")
    
    # Project statistics
    print("\nProject Statistics:")
    total_projects = input("Total Projects [0]: ") or "0"
    while not total_projects.isdigit():
        print("Please enter a valid number")
        total_projects = input("Total Projects [0]: ") or "0"
    
    completed_projects = input("Completed Projects [0]: ") or "0"
    while not completed_projects.isdigit():
        print("Please enter a valid number")
        completed_projects = input("Completed Projects [0]: ") or "0"
    
    ongoing_projects = input("Ongoing Projects [0]: ") or "0"
    while not ongoing_projects.isdigit():
        print("Please enter a valid number")
        ongoing_projects = input("Ongoing Projects [0]: ") or "0"
    
    # Rating information
    rating = input("Rating (0.00-5.00) [0.00]: ") or "0.00"
    while True:
        try:
            rating_float = float(rating)
            if 0 <= rating_float <= 5:
                break
            print("Rating must be between 0 and 5")
            rating = input("Rating (0.00-5.00) [0.00]: ") or "0.00"
        except ValueError:
            print("Please enter a valid number")
            rating = input("Rating (0.00-5.00) [0.00]: ") or "0.00"
    
    total_reviews = input("Total Reviews [0]: ") or "0"
    while not total_reviews.isdigit():
        print("Please enter a valid number")
        total_reviews = input("Total Reviews [0]: ") or "0"
    
    is_verified = input("Is Verified (1/0) [0]: ") or "0"
    while is_verified not in ["0", "1"]:
        print("Please enter 0 or 1")
        is_verified = input("Is Verified (1/0) [0]: ") or "0"

    try:
        with app.app_context():
            # Create new developer
            developer = Developer()
            developer.name = name
            developer.established_year = int(established_year) if established_year else None
            developer.description = description or None
            developer.logo_url = logo_url or None
            developer.website_url = website_url or None
            developer.contact_email = contact_email or None
            developer.contact_phone = contact_phone or None
            developer.address = address or None
            developer.total_projects = int(total_projects)
            developer.completed_projects = int(completed_projects)
            developer.ongoing_projects = int(ongoing_projects)
            developer.rating = float(rating)
            developer.total_reviews = int(total_reviews)
            developer.is_verified = bool(int(is_verified))
            
            # Add to database
            db.session.add(developer)
            db.session.commit()
            
            print(f"\n✅ Developer '{name}' created successfully!")
            print("\nDeveloper Details:")
            print("=" * 50)
            print(f"Developer ID: {developer.developer_id}")
            print(f"Name: {developer.name}")
            print(f"Established Year: {developer.established_year or 'N/A'}")
            print(f"Contact Email: {developer.contact_email or 'N/A'}")
            print(f"Contact Phone: {developer.contact_phone or 'N/A'}")
            print(f"Address: {developer.address or 'N/A'}")
            print(f"Website: {developer.website_url or 'N/A'}")
            print(f"Total Projects: {developer.total_projects}")
            print(f"Completed Projects: {developer.completed_projects}")
            print(f"Ongoing Projects: {developer.ongoing_projects}")
            print(f"Rating: {developer.rating}")
            print(f"Total Reviews: {developer.total_reviews}")
            print(f"Verified: {'Yes' if developer.is_verified else 'No'}")
            
    except Exception as e:
        print(f"\n❌ Error creating developer: {str(e)}")

def read_developer():
    """Read a specific developer's details"""
    developer_id = input("\nEnter Developer ID to view: ")
    
    try:
        with app.app_context():
            developer = Developer.query.get(developer_id)
            if not developer:
                print("\n❌ Developer not found!")
                return
            
            print("\nDeveloper Details:")
            print("=" * 50)
            print(f"Developer ID: {developer.developer_id}")
            print(f"Name: {developer.name}")
            print(f"Established Year: {developer.established_year or 'N/A'}")
            print(f"Description: {developer.description or 'N/A'}")
            print(f"Logo URL: {developer.logo_url or 'N/A'}")
            print(f"Website: {developer.website_url or 'N/A'}")
            print(f"Contact Email: {developer.contact_email or 'N/A'}")
            print(f"Contact Phone: {developer.contact_phone or 'N/A'}")
            print(f"Address: {developer.address or 'N/A'}")
            
            print("\nProject Statistics:")
            print("-" * 30)
            print(f"Total Projects: {developer.total_projects}")
            print(f"Completed Projects: {developer.completed_projects}")
            print(f"Ongoing Projects: {developer.ongoing_projects}")
            
            print("\nRatings & Reviews:")
            print("-" * 30)
            print(f"Rating: {developer.rating:.2f}/5.00")
            print(f"Total Reviews: {developer.total_reviews}")
            print(f"Verified: {'Yes' if developer.is_verified else 'No'}")
            
            # Show projects if any
            if developer.projects:
                print("\nProjects:")
                print("-" * 30)
                for project in developer.projects:
                    print(f"- {project.name} (ID: {project.project_id})")
            
    except Exception as e:
        print(f"\n❌ Error reading developer: {str(e)}")

def update_developer():
    """Update an existing developer"""
    developer_id = input("\nEnter Developer ID to update: ")
    
    try:
        with app.app_context():
            developer = Developer.query.get(developer_id)
            if not developer:
                print("\n❌ Developer not found!")
                return
            
            print("\nUpdate Developer")
            print("=" * 50)
            print("(Press Enter to keep current value)\n")
            
            # Basic developer details
            name = input(f"Developer Name [{developer.name}]: ") or developer.name
            
            established_year = input(f"Established Year [{developer.established_year or 'N/A'}]: ")
            while established_year:
                try:
                    year = int(established_year)
                    current_year = datetime.now().year
                    if year < 1800 or year > current_year:
                        print(f"Year must be between 1800 and {current_year}")
                        established_year = input(f"Established Year [{developer.established_year or 'N/A'}]: ")
                        continue
                    break
                except ValueError:
                    print("Please enter a valid year")
                    established_year = input(f"Established Year [{developer.established_year or 'N/A'}]: ")
            
            description = input(f"Description [{developer.description or 'N/A'}]: ") or developer.description
            logo_url = input(f"Logo URL [{developer.logo_url or 'N/A'}]: ") or developer.logo_url
            website_url = input(f"Website URL [{developer.website_url or 'N/A'}]: ") or developer.website_url
            contact_email = input(f"Contact Email [{developer.contact_email or 'N/A'}]: ") or developer.contact_email
            contact_phone = input(f"Contact Phone [{developer.contact_phone or 'N/A'}]: ") or developer.contact_phone
            address = input(f"Address [{developer.address or 'N/A'}]: ") or developer.address
            
            # Project statistics
            print("\nProject Statistics:")
            print("-" * 30)
            
            total_projects = input(f"Total Projects [{developer.total_projects}]: ") or str(developer.total_projects)
            while not total_projects.isdigit():
                print("Please enter a valid number")
                total_projects = input(f"Total Projects [{developer.total_projects}]: ") or str(developer.total_projects)
            
            completed_projects = input(f"Completed Projects [{developer.completed_projects}]: ") or str(developer.completed_projects)
            while not completed_projects.isdigit():
                print("Please enter a valid number")
                completed_projects = input(f"Completed Projects [{developer.completed_projects}]: ") or str(developer.completed_projects)
            
            ongoing_projects = input(f"Ongoing Projects [{developer.ongoing_projects}]: ") or str(developer.ongoing_projects)
            while not ongoing_projects.isdigit():
                print("Please enter a valid number")
                ongoing_projects = input(f"Ongoing Projects [{developer.ongoing_projects}]: ") or str(developer.ongoing_projects)
            
            # Rating information
            print("\nRatings & Reviews:")
            print("-" * 30)
            
            rating = input(f"Rating (0.00-5.00) [{developer.rating:.2f}]: ") or str(developer.rating)
            while True:
                try:
                    rating_float = float(rating)
                    if 0 <= rating_float <= 5:
                        break
                    print("Rating must be between 0 and 5")
                    rating = input(f"Rating (0.00-5.00) [{developer.rating:.2f}]: ") or str(developer.rating)
                except ValueError:
                    print("Please enter a valid number")
                    rating = input(f"Rating (0.00-5.00) [{developer.rating:.2f}]: ") or str(developer.rating)
            
            total_reviews = input(f"Total Reviews [{developer.total_reviews}]: ") or str(developer.total_reviews)
            while not total_reviews.isdigit():
                print("Please enter a valid number")
                total_reviews = input(f"Total Reviews [{developer.total_reviews}]: ") or str(developer.total_reviews)
            
            is_verified = input(f"Is Verified (1/0) [{1 if developer.is_verified else 0}]: ") or ('1' if developer.is_verified else '0')
            while is_verified not in ["0", "1"]:
                print("Please enter 0 or 1")
                is_verified = input(f"Is Verified (1/0) [{1 if developer.is_verified else 0}]: ") or ('1' if developer.is_verified else '0')
            
            # Update developer attributes
            developer.name = name
            if established_year:
                developer.established_year = int(established_year)
            developer.description = description
            developer.logo_url = logo_url
            developer.website_url = website_url
            developer.contact_email = contact_email
            developer.contact_phone = contact_phone
            developer.address = address
            developer.total_projects = int(total_projects)
            developer.completed_projects = int(completed_projects)
            developer.ongoing_projects = int(ongoing_projects)
            developer.rating = float(rating)
            developer.total_reviews = int(total_reviews)
            developer.is_verified = bool(int(is_verified))
            
            # Save changes
            db.session.commit()
            
            print("\n✅ Developer updated successfully!")
            print("\nUpdated Developer Details:")
            print("=" * 50)
            print(f"Developer ID: {developer.developer_id}")
            print(f"Name: {developer.name}")
            print(f"Established Year: {developer.established_year or 'N/A'}")
            print(f"Description: {developer.description or 'N/A'}")
            print(f"Logo URL: {developer.logo_url or 'N/A'}")
            print(f"Website: {developer.website_url or 'N/A'}")
            print(f"Contact Email: {developer.contact_email or 'N/A'}")
            print(f"Contact Phone: {developer.contact_phone or 'N/A'}")
            print(f"Address: {developer.address or 'N/A'}")
            
            print("\nProject Statistics:")
            print("-" * 30)
            print(f"Total Projects: {developer.total_projects}")
            print(f"Completed Projects: {developer.completed_projects}")
            print(f"Ongoing Projects: {developer.ongoing_projects}")
            
            print("\nRatings & Reviews:")
            print("-" * 30)
            print(f"Rating: {developer.rating:.2f}/5.00")
            print(f"Total Reviews: {developer.total_reviews}")
            print(f"Verified: {'Yes' if developer.is_verified else 'No'}")
            
    except Exception as e:
        print(f"\n❌ Error updating developer: {str(e)}")
        return

def delete_developer():
    """Delete an existing developer"""
    developer_id = input("\nEnter Developer ID to delete: ")
    
    try:
        with app.app_context():
            developer = Developer.query.get(developer_id)
            if not developer:
                print("\n❌ Developer not found!")
                return
            
            # Check if developer has projects
            if developer.projects:
                print("\n❌ Cannot delete developer with existing projects!")
                print(f"This developer has {len(developer.projects)} project(s).")
                print("Please delete or reassign all projects first.")
                return
            
            confirm = input(f"\n⚠️ Are you sure you want to delete developer '{developer.name}'? (yes/no): ")
            if confirm.lower() == 'yes':
                # Get the current max ID before deletion
                max_id = db.session.query(db.func.max(Developer.developer_id)).scalar() or 0
                
                # Delete the developer
                db.session.delete(developer)
                db.session.commit()
                
                # Reset auto-increment to the current max ID
                db.session.execute(db.text(f"ALTER TABLE developers AUTO_INCREMENT = {max_id}"))
                db.session.commit()
                
                print(f"\n✅ Developer '{developer.name}' deleted successfully!")
            else:
                print("\nDeletion cancelled.")
            
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        return

def main_menu():
    """Display the main menu"""
    while True:
        print("\nDeveloper Management System")
        print("=" * 30)
        print("1. List All Developers")
        print("2. Create New Developer")
        print("3. View Developer Details")
        print("4. Update Developer")
        print("5. Delete Developer")
        print("0. Exit")
        
        choice = input("\nEnter your choice (0-5): ")
        
        if choice == '1':
            list_developers()
        elif choice == '2':
            create_developer()
        elif choice == '3':
            read_developer()
        elif choice == '4':
            update_developer()
        elif choice == '5':
            delete_developer()
        elif choice == '0':
            print("\nGoodbye!")
            break
        else:
            print("\n❌ Invalid choice. Please try again.")

if __name__ == '__main__':
    main_menu() 