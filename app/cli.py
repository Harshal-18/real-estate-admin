import sys
import os

# Add the parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models import Developer, Project
from datetime import datetime

app = create_app()

def list_developers():
    """List all developers"""
    with app.app_context():
        developers = Developer.query.all()
        if not developers:
            print("No developers found.")
            return
        
        print("\nDevelopers:")
        print("-" * 50)
        for dev in developers:
            print(f"ID: {dev.developer_id}")
            print(f"Name: {dev.name}")
            print(f"Email: {dev.contact_email}")
            print(f"Phone: {dev.contact_phone}")
            print(f"Projects: {dev.total_projects}")
            print("-" * 50)

def add_developer():
    """Add a new developer"""
    print("\nAdd New Developer")
    print("-" * 50)
    name = input("Developer Name: ")
    email = input("Contact Email: ")
    phone = input("Contact Phone: ")
    year = input("Established Year (YYYY): ")
    desc = input("Description: ")

    with app.app_context():
        developer = Developer(
            name=name,
            contact_email=email,
            contact_phone=phone,
            established_year=int(year) if year.isdigit() else None,
            description=desc
        )
        db.session.add(developer)
        db.session.commit()
        print(f"\n✅ Developer '{name}' added successfully!")

def update_developer():
    """Update an existing developer"""
    list_developers()
    dev_id = input("\nEnter Developer ID to update: ")
    
    with app.app_context():
        developer = Developer.query.get(dev_id)
        if not developer:
            print("❌ Developer not found!")
            return
        
        print("\nUpdate Developer (press Enter to keep current value)")
        print("-" * 50)
        
        name = input(f"Name [{developer.name}]: ")
        email = input(f"Email [{developer.contact_email}]: ")
        phone = input(f"Phone [{developer.contact_phone}]: ")
        year = input(f"Established Year [{developer.established_year}]: ")
        desc = input(f"Description [{developer.description}]: ")

        if name: developer.name = name
        if email: developer.contact_email = email
        if phone: developer.contact_phone = phone
        if year and year.isdigit(): developer.established_year = int(year)
        if desc: developer.description = desc

        db.session.commit()
        print("\n✅ Developer updated successfully!")

def delete_developer():
    """Delete a developer"""
    list_developers()
    dev_id = input("\nEnter Developer ID to delete: ")
    
    with app.app_context():
        developer = Developer.query.get(dev_id)
        if not developer:
            print("❌ Developer not found!")
            return
        
        confirm = input(f"Are you sure you want to delete '{developer.name}'? (y/n): ")
        if confirm.lower() == 'y':
            db.session.delete(developer)
            db.session.commit()
            print("\n✅ Developer deleted successfully!")
        else:
            print("\nDeletion cancelled.")

def list_projects():
    """List all projects"""
    with app.app_context():
        projects = Project.query.all()
        if not projects:
            print("No projects found.")
            return
        
        print("\nProjects:")
        print("-" * 50)
        for proj in projects:
            print(f"ID: {proj.project_id}")
            print(f"Name: {proj.name}")
            print(f"Developer: {proj.developer.name}")
            print(f"Type: {proj.project_type}")
            print(f"Status: {proj.status}")
            print(f"Units: {proj.total_units}")
            print("-" * 50)

def add_project():
    """Add a new project"""
    list_developers()
    dev_id = input("\nEnter Developer ID for the project: ")
    
    with app.app_context():
        developer = Developer.query.get(dev_id)
        if not developer:
            print("❌ Developer not found!")
            return
        
        print("\nAdd New Project")
        print("-" * 50)
        name = input("Project Name: ")
        type = input("Project Type (residential/commercial): ")
        prop_type = input("Property Type (apartment/villa/plot): ")
        status = input("Status (upcoming/under_construction/completed): ")
        units = input("Total Units: ")
        launch_date = input("Launch Date (YYYY-MM-DD): ")

        project = Project(
            developer_id=developer.developer_id,
            name=name,
            project_type=type or 'residential',
            property_type=prop_type,
            status=status or 'upcoming',
            total_units=int(units) if units.isdigit() else 0,
            launch_date=datetime.strptime(launch_date, '%Y-%m-%d') if launch_date else None
        )
        
        db.session.add(project)
        db.session.commit()
        
        # Update developer's project counts
        developer.update_project_counts()
        print(f"\n✅ Project '{name}' added successfully!")

def update_project():
    """Update an existing project"""
    list_projects()
    proj_id = input("\nEnter Project ID to update: ")
    
    with app.app_context():
        project = Project.query.get(proj_id)
        if not project:
            print("❌ Project not found!")
            return
        
        print("\nUpdate Project (press Enter to keep current value)")
        print("-" * 50)
        
        name = input(f"Name [{project.name}]: ")
        type = input(f"Project Type [{project.project_type}]: ")
        status = input(f"Status [{project.status}]: ")
        units = input(f"Total Units [{project.total_units}]: ")

        if name: project.name = name
        if type: project.project_type = type
        if status: project.status = status
        if units and units.isdigit(): project.total_units = int(units)

        db.session.commit()
        
        # Update developer's project counts
        project.developer.update_project_counts()
        print("\n✅ Project updated successfully!")

def delete_project():
    """Delete a project"""
    list_projects()
    proj_id = input("\nEnter Project ID to delete: ")
    
    with app.app_context():
        project = Project.query.get(proj_id)
        if not project:
            print("❌ Project not found!")
            return
        
        developer = project.developer
        confirm = input(f"Are you sure you want to delete '{project.name}'? (y/n): ")
        if confirm.lower() == 'y':
            db.session.delete(project)
            db.session.commit()
            
            # Update developer's project counts
            developer.update_project_counts()
            print("\n✅ Project deleted successfully!")
        else:
            print("\nDeletion cancelled.")

def main_menu():
    """Display the main menu"""
    while True:
        print("\nReal Estate Management System")
        print("=" * 30)
        print("1. List Developers")
        print("2. Add Developer")
        print("3. Update Developer")
        print("4. Delete Developer")
        print("5. List Projects")
        print("6. Add Project")
        print("7. Update Project")
        print("8. Delete Project")
        print("0. Exit")
        
        choice = input("\nEnter your choice (0-8): ")
        
        if choice == '1':
            list_developers()
        elif choice == '2':
            add_developer()
        elif choice == '3':
            update_developer()
        elif choice == '4':
            delete_developer()
        elif choice == '5':
            list_projects()
        elif choice == '6':
            add_project()
        elif choice == '7':
            update_project()
        elif choice == '8':
            delete_project()
        elif choice == '0':
            print("\nGoodbye!")
            break
        else:
            print("\n❌ Invalid choice. Please try again.")

if __name__ == '__main__':
    main_menu() 