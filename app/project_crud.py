import sys
import os

# Add the parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models import Project, Developer
from datetime import datetime
from decimal import Decimal

app = create_app()

def list_developers():
    """List all developers for selection"""
    with app.app_context():
        developers = Developer.query.all()
        if not developers:
            print("\nNo developers found in the database.")
            print("Please add a developer first before creating a project.")
            return None
        
        print("\nAvailable Developers:")
        print("=" * 50)
        for dev in developers:
            print(f"ID: {dev.developer_id} - Name: {dev.name}")
        return developers

def list_projects():
    """List all projects"""
    with app.app_context():
        projects = Project.query.all()
        if not projects:
            print("\nNo projects found.")
            return
        
        print("\nList of All Projects:")
        print("=" * 50)
        for proj in projects:
            print(f"Project ID: {proj.project_id}")
            print(f"Name: {proj.name}")
            print(f"Developer: {proj.developer.name}")
            print(f"Type: {proj.project_type}")
            print(f"Property Type: {proj.property_type}")
            print(f"Status: {proj.status}")
            print(f"Total Units: {proj.total_units}")
            print(f"Launch Date: {proj.launch_date}")
            print("-" * 50)

def create_project():
    """Create a new project"""
    # First, check if there are any developers
    developers = list_developers()
    if not developers:
        return
    
    # Get developer ID
    while True:
        dev_id = input("\nEnter Developer ID from the list above: ")
        if not dev_id.isdigit():
            print("Please enter a valid number.")
            continue
        
        with app.app_context():
            developer = Developer.query.get(int(dev_id))
            if not developer:
                print("Developer not found. Please enter a valid ID.")
                continue
            break
    
    print("\nCreate New Project")
    print("=" * 50)
    print("(Press Enter to skip optional fields)\n")
    
    # Required fields
    name = input("Project Name*: ")
    while not name:
        print("Project name is required!")
        name = input("Project Name*: ")

    # Optional fields with validation
    project_type = input("Project Type (residential/commercial) [residential]: ").lower() or "residential"
    while project_type and project_type not in ["residential", "commercial"]:
        print("Invalid project type. Please enter 'residential' or 'commercial'")
        project_type = input("Project Type (residential/commercial) [residential]: ").lower() or "residential"

    property_type = input("Property Type (apartment/villa/plot/office/retail) [apartment]: ").lower() or "apartment"
    while property_type and property_type not in ["apartment", "villa", "plot", "office", "retail"]:
        print("Invalid property type. Please enter 'apartment', 'villa', 'plot', 'office', or 'retail'")
        property_type = input("Property Type (apartment/villa/plot/office/retail) [apartment]: ").lower() or "apartment"

    status = input("Status (upcoming/under_construction/ready_to_move/completed) [upcoming]: ").lower() or "upcoming"
    while status and status not in ["upcoming", "under_construction", "ready_to_move", "completed"]:
        print("Invalid status. Please enter 'upcoming', 'under_construction', 'ready_to_move', or 'completed'")
        status = input("Status (upcoming/under_construction/ready_to_move/completed) [upcoming]: ").lower() or "upcoming"

    # Decimal inputs with validation
    total_land_area = input("Total Land Area (in sq ft): ")
    while total_land_area and not total_land_area.replace('.', '').isdigit():
        print("Please enter a valid number")
        total_land_area = input("Total Land Area (in sq ft): ")

    total_units = input("Total Units: ")
    while total_units and not total_units.isdigit():
        print("Please enter a valid number")
        total_units = input("Total Units: ")

    unit_density = input("Unit Density (units per acre): ")
    while unit_density and not unit_density.replace('.', '').isdigit():
        print("Please enter a valid number")
        unit_density = input("Unit Density (units per acre): ")

    open_area_percentage = input("Open Area Percentage: ")
    while open_area_percentage and not open_area_percentage.replace('.', '').isdigit():
        print("Please enter a valid number")
        open_area_percentage = input("Open Area Percentage: ")

    park_area = input("Park Area (in sq ft): ")
    while park_area and not park_area.replace('.', '').isdigit():
        print("Please enter a valid number")
        park_area = input("Park Area (in sq ft): ")

    clubhouse_area = input("Clubhouse Area (in sq ft): ")
    while clubhouse_area and not clubhouse_area.replace('.', '').isdigit():
        print("Please enter a valid number")
        clubhouse_area = input("Clubhouse Area (in sq ft): ")

    min_price = input("Minimum Price: ")
    while min_price and not min_price.replace('.', '').isdigit():
        print("Please enter a valid number")
        min_price = input("Minimum Price: ")

    max_price = input("Maximum Price: ")
    while max_price and not max_price.replace('.', '').isdigit():
        print("Please enter a valid number")
        max_price = input("Maximum Price: ")

    price_per_sqft = input("Price per sq ft: ")
    while price_per_sqft and not price_per_sqft.replace('.', '').isdigit():
        print("Please enter a valid number")
        price_per_sqft = input("Price per sq ft: ")

    currency = input("Currency [INR]: ") or "INR"

    # Date inputs with validation
    def get_valid_date(prompt):
        date_str = input(prompt)
        while date_str:
            try:
                return datetime.strptime(date_str, '%Y-%m-%d')
            except ValueError:
                print("Invalid date format. Please use YYYY-MM-DD")
                date_str = input(prompt)
        return None

    launch_date = get_valid_date("Launch Date (YYYY-MM-DD): ")
    possession_date = get_valid_date("Possession Date (YYYY-MM-DD): ")
    completion_date = get_valid_date("Completion Date (YYYY-MM-DD): ")

    # Location details
    address = input("Project Address: ")
    
    latitude = input("Latitude: ")
    while latitude and not latitude.replace('.', '').replace('-', '').isdigit():
        print("Please enter a valid latitude")
        latitude = input("Latitude: ")

    longitude = input("Longitude: ")
    while longitude and not longitude.replace('.', '').replace('-', '').isdigit():
        print("Please enter a valid longitude")
        longitude = input("Longitude: ")

    approach_road_width = input("Approach Road Width (in meters): ")
    while approach_road_width and not approach_road_width.replace('.', '').isdigit():
        print("Please enter a valid number")
        approach_road_width = input("Approach Road Width (in meters): ")

    nearest_metro_distance = input("Distance to Nearest Metro (in km): ")
    while nearest_metro_distance and not nearest_metro_distance.replace('.', '').isdigit():
        print("Please enter a valid number")
        nearest_metro_distance = input("Distance to Nearest Metro (in km): ")

    airport_distance = input("Distance to Airport (in km): ")
    while airport_distance and not airport_distance.replace('.', '').isdigit():
        print("Please enter a valid number")
        airport_distance = input("Distance to Airport (in km): ")

    # RERA details
    rera_number = input("RERA Number: ")
    rera_website = input("RERA Website URL: ")
    rera_status = input("RERA Status (approved/pending/na) [na]: ").lower() or "na"
    while rera_status and rera_status not in ["approved", "pending", "na"]:
        print("Invalid RERA status. Please enter 'approved', 'pending', or 'na'")
        rera_status = input("RERA Status (approved/pending/na) [na]: ").lower() or "na"

    # Project details
    description = input("Project Description: ")
    highlights = input("Project Highlights: ")
    master_plan_url = input("Master Plan URL: ")
    brochure_url = input("Brochure URL: ")

    # SEO details
    meta_title = input("Meta Title: ")
    meta_description = input("Meta Description: ")

    # Active status
    is_active = input("Is Active (1/0) [1]: ") or "1"
    while is_active not in ["0", "1"]:
        print("Please enter 0 or 1")
        is_active = input("Is Active (1/0) [1]: ") or "1"

    try:
        with app.app_context():
            # Create new project
            project = Project(
                developer_id=int(dev_id),
                locality_id=1,  # Default locality_id as 1
                name=name,
                project_type=project_type,
                property_type=property_type,
                status=status,
                total_land_area=Decimal(total_land_area) if total_land_area else None,
                total_units=int(total_units) if total_units else None,
                unit_density=Decimal(unit_density) if unit_density else None,
                open_area_percentage=Decimal(open_area_percentage) if open_area_percentage else None,
                park_area=Decimal(park_area) if park_area else None,
                clubhouse_area=Decimal(clubhouse_area) if clubhouse_area else None,
                min_price=Decimal(min_price) if min_price else None,
                max_price=Decimal(max_price) if max_price else None,
                price_per_sqft=Decimal(price_per_sqft) if price_per_sqft else None,
                currency=currency,
                launch_date=launch_date,
                possession_date=possession_date,
                completion_date=completion_date,
                address=address,
                latitude=Decimal(latitude) if latitude else None,
                longitude=Decimal(longitude) if longitude else None,
                approach_road_width=Decimal(approach_road_width) if approach_road_width else None,
                nearest_metro_distance=Decimal(nearest_metro_distance) if nearest_metro_distance else None,
                airport_distance=Decimal(airport_distance) if airport_distance else None,
                rera_number=rera_number or None,
                rera_website=rera_website or None,
                rera_status=rera_status,
                description=description or None,
                highlights=highlights or None,
                master_plan_url=master_plan_url or None,
                brochure_url=brochure_url or None,
                meta_title=meta_title or None,
                meta_description=meta_description or None,
                is_active=bool(int(is_active))
            )
            
            # Add to database
            db.session.add(project)
            db.session.commit()
            
            # Update developer's project counts
            developer = Developer.query.get(int(dev_id))
            if hasattr(developer, 'update_project_counts'):
                developer.update_project_counts()
            
            print(f"\n✅ Project '{name}' created successfully!")
            print("\nProject Details:")
            print("=" * 50)
            print(f"Project ID: {project.project_id}")
            print(f"Name: {project.name}")
            print(f"Developer: {project.developer.name}")
            print(f"Type: {project.project_type}")
            print(f"Property Type: {project.property_type}")
            print(f"Status: {project.status}")
            print(f"Total Land Area: {project.total_land_area or 'N/A'} sq ft")
            print(f"Total Units: {project.total_units or 'N/A'}")
            print(f"Unit Density: {project.unit_density or 'N/A'} units/acre")
            print(f"Open Area: {project.open_area_percentage or 'N/A'}%")
            print(f"Park Area: {project.park_area or 'N/A'} sq ft")
            print(f"Clubhouse Area: {project.clubhouse_area or 'N/A'} sq ft")
            print(f"Price Range: {project.min_price or 'N/A'} - {project.max_price or 'N/A'} {project.currency}")
            print(f"Price per sq ft: {project.price_per_sqft or 'N/A'} {project.currency}")
            print(f"Launch Date: {project.launch_date or 'N/A'}")
            print(f"Possession Date: {project.possession_date or 'N/A'}")
            print(f"Completion Date: {project.completion_date or 'N/A'}")
            print(f"Address: {project.address or 'N/A'}")
            print(f"Location: {project.latitude or 'N/A'}, {project.longitude or 'N/A'}")
            print(f"Approach Road Width: {project.approach_road_width or 'N/A'} meters")
            print(f"Distance to Metro: {project.nearest_metro_distance or 'N/A'} km")
            print(f"Distance to Airport: {project.airport_distance or 'N/A'} km")
            print(f"RERA Number: {project.rera_number or 'N/A'}")
            print(f"RERA Website: {project.rera_website or 'N/A'}")
            print(f"RERA Status: {project.rera_status}")
            print(f"Description: {project.description or 'N/A'}")
            print(f"Highlights: {project.highlights or 'N/A'}")
            print(f"Master Plan URL: {project.master_plan_url or 'N/A'}")
            print(f"Brochure URL: {project.brochure_url or 'N/A'}")
            print(f"Meta Title: {project.meta_title or 'N/A'}")
            print(f"Meta Description: {project.meta_description or 'N/A'}")
            print(f"Is Active: {project.is_active}")
            
    except Exception as e:
        print(f"\n❌ Error creating project: {str(e)}")

def read_project():
    """Read a specific project's details"""
    project_id = input("\nEnter Project ID to view: ")
    
    try:
        with app.app_context():
            project = Project.query.get(project_id)
            if not project:
                print("\n❌ Project not found!")
                return
            
            print("\nProject Details:")
            print("=" * 50)
            print(f"Project ID: {project.project_id}")
            print(f"Name: {project.name}")
            print(f"Developer: {project.developer.name}")
            print(f"Type: {project.project_type}")
            print(f"Property Type: {project.property_type}")
            print(f"Status: {project.status}")
            print(f"Total Units: {project.total_units}")
            print(f"Launch Date: {project.launch_date}")
            print(f"Description: {project.description or 'N/A'}")
            print(f"Address: {project.address or 'N/A'}")
            print(f"RERA Number: {project.rera_number or 'N/A'}")
            
    except Exception as e:
        print(f"\n❌ Error reading project: {str(e)}")

def update_project():
    """Update an existing project"""
    project_id = input("\nEnter Project ID to update: ")
    
    try:
        with app.app_context():
            project = Project.query.get(project_id)
            if not project:
                print("\n❌ Project not found!")
                return
            
            print("\nUpdate Project")
            print("=" * 50)
            print("(Press Enter to keep current value)\n")
            
            # Basic project details
            name = input(f"Project Name [{project.name}]: ") or project.name
            
            project_type = input(f"Project Type (residential/commercial) [{project.project_type}]: ").lower() or project.project_type
            while project_type and project_type not in ["residential", "commercial"]:
                print("Invalid project type. Please enter 'residential' or 'commercial'")
                project_type = input(f"Project Type [{project.project_type}]: ").lower() or project.project_type

            property_type = input(f"Property Type (apartment/villa/plot/office/retail) [{project.property_type}]: ").lower() or project.property_type
            while property_type and property_type not in ["apartment", "villa", "plot", "office", "retail"]:
                print("Invalid property type. Please enter 'apartment', 'villa', 'plot', 'office', or 'retail'")
                property_type = input(f"Property Type [{project.property_type}]: ").lower() or project.property_type

            status = input(f"Status (upcoming/under_construction/ready_to_move/completed) [{project.status}]: ").lower() or project.status
            while status and status not in ["upcoming", "under_construction", "ready_to_move", "completed"]:
                print("Invalid status. Please enter 'upcoming', 'under_construction', 'ready_to_move', or 'completed'")
                status = input(f"Status [{project.status}]: ").lower() or project.status

            # Area and unit details
            total_land_area = input(f"Total Land Area in sq ft [{project.total_land_area or 'N/A'}]: ")
            while total_land_area and not total_land_area.replace('.', '').isdigit():
                print("Please enter a valid number")
                total_land_area = input(f"Total Land Area in sq ft [{project.total_land_area or 'N/A'}]: ")

            total_units = input(f"Total Units [{project.total_units or 'N/A'}]: ")
            while total_units and not total_units.isdigit():
                print("Please enter a valid number")
                total_units = input(f"Total Units [{project.total_units or 'N/A'}]: ")

            unit_density = input(f"Unit Density (units per acre) [{project.unit_density or 'N/A'}]: ")
            while unit_density and not unit_density.replace('.', '').isdigit():
                print("Please enter a valid number")
                unit_density = input(f"Unit Density [{project.unit_density or 'N/A'}]: ")

            open_area_percentage = input(f"Open Area Percentage [{project.open_area_percentage or 'N/A'}]: ")
            while open_area_percentage and not open_area_percentage.replace('.', '').isdigit():
                print("Please enter a valid number")
                open_area_percentage = input(f"Open Area Percentage [{project.open_area_percentage or 'N/A'}]: ")

            park_area = input(f"Park Area in sq ft [{project.park_area or 'N/A'}]: ")
            while park_area and not park_area.replace('.', '').isdigit():
                print("Please enter a valid number")
                park_area = input(f"Park Area [{project.park_area or 'N/A'}]: ")

            clubhouse_area = input(f"Clubhouse Area in sq ft [{project.clubhouse_area or 'N/A'}]: ")
            while clubhouse_area and not clubhouse_area.replace('.', '').isdigit():
                print("Please enter a valid number")
                clubhouse_area = input(f"Clubhouse Area [{project.clubhouse_area or 'N/A'}]: ")

            # Price details
            min_price = input(f"Minimum Price [{project.min_price or 'N/A'}]: ")
            while min_price and not min_price.replace('.', '').isdigit():
                print("Please enter a valid number")
                min_price = input(f"Minimum Price [{project.min_price or 'N/A'}]: ")

            max_price = input(f"Maximum Price [{project.max_price or 'N/A'}]: ")
            while max_price and not max_price.replace('.', '').isdigit():
                print("Please enter a valid number")
                max_price = input(f"Maximum Price [{project.max_price or 'N/A'}]: ")

            price_per_sqft = input(f"Price per sq ft [{project.price_per_sqft or 'N/A'}]: ")
            while price_per_sqft and not price_per_sqft.replace('.', '').isdigit():
                print("Please enter a valid number")
                price_per_sqft = input(f"Price per sq ft [{project.price_per_sqft or 'N/A'}]: ")

            currency = input(f"Currency [{project.currency or 'INR'}]: ") or project.currency or 'INR'

            # Date inputs
            def get_valid_date(prompt, current_date):
                date_str = input(prompt)
                while date_str:
                    try:
                        return datetime.strptime(date_str, '%Y-%m-%d')
                    except ValueError:
                        print("Invalid date format. Please use YYYY-MM-DD")
                        date_str = input(prompt)
                return current_date

            launch_date = get_valid_date(
                f"Launch Date (YYYY-MM-DD) [{project.launch_date or 'N/A'}]: ",
                project.launch_date
            )
            possession_date = get_valid_date(
                f"Possession Date (YYYY-MM-DD) [{project.possession_date or 'N/A'}]: ",
                project.possession_date
            )
            completion_date = get_valid_date(
                f"Completion Date (YYYY-MM-DD) [{project.completion_date or 'N/A'}]: ",
                project.completion_date
            )

            # Location details
            address = input(f"Project Address [{project.address or 'N/A'}]: ") or project.address

            latitude = input(f"Latitude [{project.latitude or 'N/A'}]: ")
            while latitude:
                try:
                    lat_val = float(latitude)
                    if lat_val < -90 or lat_val > 90:
                        print("Latitude must be between -90 and +90 degrees")
                        latitude = input(f"Latitude [{project.latitude or 'N/A'}]: ")
                        continue
                    project.latitude = Decimal(str(lat_val))  # Convert to string first for precise decimal conversion
                    break
                except ValueError:
                    print("Please enter a valid number")
                    latitude = input(f"Latitude [{project.latitude or 'N/A'}]: ")

            longitude = input(f"Longitude [{project.longitude or 'N/A'}]: ")
            while longitude:
                try:
                    lon_val = float(longitude)
                    if lon_val < -180 or lon_val > 180:
                        print("Longitude must be between -180 and +180 degrees")
                        longitude = input(f"Longitude [{project.longitude or 'N/A'}]: ")
                        continue
                    project.longitude = Decimal(str(lon_val))  # Convert to string first for precise decimal conversion
                    break
                except ValueError:
                    print("Please enter a valid number")
                    longitude = input(f"Longitude [{project.longitude or 'N/A'}]: ")

            approach_road_width = input(f"Approach Road Width in meters [{project.approach_road_width or 'N/A'}]: ")
            while approach_road_width and not approach_road_width.replace('.', '').isdigit():
                print("Please enter a valid number")
                approach_road_width = input(f"Approach Road Width [{project.approach_road_width or 'N/A'}]: ")

            nearest_metro_distance = input(f"Distance to Nearest Metro in km [{project.nearest_metro_distance or 'N/A'}]: ")
            while nearest_metro_distance and not nearest_metro_distance.replace('.', '').isdigit():
                print("Please enter a valid number")
                nearest_metro_distance = input(f"Distance to Nearest Metro [{project.nearest_metro_distance or 'N/A'}]: ")

            airport_distance = input(f"Distance to Airport in km [{project.airport_distance or 'N/A'}]: ")
            while airport_distance and not airport_distance.replace('.', '').isdigit():
                print("Please enter a valid number")
                airport_distance = input(f"Distance to Airport [{project.airport_distance or 'N/A'}]: ")

            # RERA details
            rera_number = input(f"RERA Number [{project.rera_number or 'N/A'}]: ") or project.rera_number
            rera_website = input(f"RERA Website URL [{project.rera_website or 'N/A'}]: ") or project.rera_website
            rera_status = input(f"RERA Status (approved/pending/na) [{project.rera_status or 'na'}]: ").lower() or project.rera_status or 'na'
            while rera_status and rera_status not in ["approved", "pending", "na"]:
                print("Invalid RERA status. Please enter 'approved', 'pending', or 'na'")
                rera_status = input(f"RERA Status [{project.rera_status or 'na'}]: ").lower() or project.rera_status or 'na'

            # Project details
            description = input(f"Project Description [{project.description or 'N/A'}]: ") or project.description
            highlights = input(f"Project Highlights [{project.highlights or 'N/A'}]: ") or project.highlights
            master_plan_url = input(f"Master Plan URL [{project.master_plan_url or 'N/A'}]: ") or project.master_plan_url
            brochure_url = input(f"Brochure URL [{project.brochure_url or 'N/A'}]: ") or project.brochure_url

            # SEO details
            meta_title = input(f"Meta Title [{project.meta_title or 'N/A'}]: ") or project.meta_title
            meta_description = input(f"Meta Description [{project.meta_description or 'N/A'}]: ") or project.meta_description

            # Active status
            is_active = input(f"Is Active (1/0) [{1 if project.is_active else 0}]: ") or ('1' if project.is_active else '0')
            while is_active not in ["0", "1"]:
                print("Please enter 0 or 1")
                is_active = input(f"Is Active (1/0) [{1 if project.is_active else 0}]: ") or ('1' if project.is_active else '0')

            # Update project attributes
            project.name = name
            project.project_type = project_type
            project.property_type = property_type
            project.status = status
            project.total_land_area = Decimal(total_land_area) if total_land_area else project.total_land_area
            project.total_units = int(total_units) if total_units else project.total_units
            project.unit_density = Decimal(unit_density) if unit_density else project.unit_density
            project.open_area_percentage = Decimal(open_area_percentage) if open_area_percentage else project.open_area_percentage
            project.park_area = Decimal(park_area) if park_area else project.park_area
            project.clubhouse_area = Decimal(clubhouse_area) if clubhouse_area else project.clubhouse_area
            project.min_price = Decimal(min_price) if min_price else project.min_price
            project.max_price = Decimal(max_price) if max_price else project.max_price
            project.price_per_sqft = Decimal(price_per_sqft) if price_per_sqft else project.price_per_sqft
            project.currency = currency
            project.launch_date = launch_date
            project.possession_date = possession_date
            project.completion_date = completion_date
            project.address = address
            project.latitude = Decimal(latitude) if latitude else project.latitude
            project.longitude = Decimal(longitude) if longitude else project.longitude
            project.approach_road_width = Decimal(approach_road_width) if approach_road_width else project.approach_road_width
            project.nearest_metro_distance = Decimal(nearest_metro_distance) if nearest_metro_distance else project.nearest_metro_distance
            project.airport_distance = Decimal(airport_distance) if airport_distance else project.airport_distance
            project.rera_number = rera_number
            project.rera_website = rera_website
            project.rera_status = rera_status
            project.description = description
            project.highlights = highlights
            project.master_plan_url = master_plan_url
            project.brochure_url = brochure_url
            project.meta_title = meta_title
            project.meta_description = meta_description
            project.is_active = bool(int(is_active))
            
            # Save changes
            db.session.commit()
            
            print("\n✅ Project updated successfully!")
            print("\nUpdated Project Details:")
            print("=" * 50)
            print(f"Project ID: {project.project_id}")
            print(f"Name: {project.name}")
            print(f"Developer: {project.developer.name}")
            print(f"Type: {project.project_type}")
            print(f"Property Type: {project.property_type}")
            print(f"Status: {project.status}")
            print(f"Total Land Area: {project.total_land_area or 'N/A'} sq ft")
            print(f"Total Units: {project.total_units or 'N/A'}")
            print(f"Unit Density: {project.unit_density or 'N/A'} units/acre")
            print(f"Open Area: {project.open_area_percentage or 'N/A'}%")
            print(f"Park Area: {project.park_area or 'N/A'} sq ft")
            print(f"Clubhouse Area: {project.clubhouse_area or 'N/A'} sq ft")
            print(f"Price Range: {project.min_price or 'N/A'} - {project.max_price or 'N/A'} {project.currency}")
            print(f"Price per sq ft: {project.price_per_sqft or 'N/A'} {project.currency}")
            print(f"Launch Date: {project.launch_date or 'N/A'}")
            print(f"Possession Date: {project.possession_date or 'N/A'}")
            print(f"Completion Date: {project.completion_date or 'N/A'}")
            print(f"Address: {project.address or 'N/A'}")
            print(f"Location: {project.latitude or 'N/A'}, {project.longitude or 'N/A'}")
            print(f"Approach Road Width: {project.approach_road_width or 'N/A'} meters")
            print(f"Distance to Metro: {project.nearest_metro_distance or 'N/A'} km")
            print(f"Distance to Airport: {project.airport_distance or 'N/A'} km")
            print(f"RERA Number: {project.rera_number or 'N/A'}")
            print(f"RERA Website: {project.rera_website or 'N/A'}")
            print(f"RERA Status: {project.rera_status}")
            print(f"Description: {project.description or 'N/A'}")
            print(f"Highlights: {project.highlights or 'N/A'}")
            print(f"Master Plan URL: {project.master_plan_url or 'N/A'}")
            print(f"Brochure URL: {project.brochure_url or 'N/A'}")
            print(f"Meta Title: {project.meta_title or 'N/A'}")
            print(f"Meta Description: {project.meta_description or 'N/A'}")
            print(f"Is Active: {project.is_active}")
            print("\n🎉 All changes have been saved successfully!")
            
    except Exception as e:
        print(f"\n❌ Error updating project: {str(e)}")

def delete_project():
    """Delete an existing project"""
    project_id = input("\nEnter Project ID to delete: ")
    
    try:
        with app.app_context():
            project = Project.query.get(project_id)
            if not project:
                print("\n❌ Project not found!")
                return
            
            developer = project.developer
            confirm = input(f"\n⚠️ Are you sure you want to delete project '{project.name}'? (yes/no): ")
            if confirm.lower() == 'yes':
                try:
                    # Delete related records first
                    for tower in project.towers:
                        db.session.delete(tower)
                    
                    for unit_type in project.unit_types:
                        db.session.delete(unit_type)
                    
                    for property_unit in project.property_units:
                        db.session.delete(property_unit)
                    
                    # Delete the project
                    db.session.delete(project)
                    db.session.commit()
                    
                    # Update developer's project counts
                    developer.update_project_counts()
                    
                    print(f"\n✅ Project '{project.name}' deleted successfully!")
                except Exception as e:
                    print(f"\n❌ Error deleting project: {str(e)}")
                    db.session.rollback()
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        return

def main_menu():
    """Display the main menu"""
    while True:
        print("\nProject Management System")
        print("=" * 30)
        print("1. List All Projects")
        print("2. Create New Project")
        print("3. View Project Details")
        print("4. Update Project")
        print("5. Delete Project")
        print("0. Exit")
        
        choice = input("\nEnter your choice (0-5): ")
        
        if choice == '1':
            list_projects()
        elif choice == '2':
            create_project()
        elif choice == '3':
            read_project()
        elif choice == '4':
            update_project()
        elif choice == '5':
            delete_project()
        elif choice == '0':
            print("\nGoodbye!")
            break
        else:
            print("\n❌ Invalid choice. Please try again.")

if __name__ == '__main__':
    main_menu() 