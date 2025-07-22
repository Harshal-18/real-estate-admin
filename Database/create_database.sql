-- Enhanced Real Estate Database Schema for PropSoch.com
-- Creation Script

CREATE DATABASE real_estate_db;
USE real_estate_db;

-- Core Tables
CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(20) UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    user_type VARCHAR(20) DEFAULT 'buyer' COMMENT 'buyer, seller, agent, admin',
    is_verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP NULL,
    profile_image_url VARCHAR(500),
    is_active BOOLEAN DEFAULT TRUE
);

CREATE TABLE developers (
    developer_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    established_year INT,
    description TEXT,
    logo_url VARCHAR(500),
    website_url VARCHAR(500),
    contact_email VARCHAR(255),
    contact_phone VARCHAR(20),
    address TEXT,
    total_projects INT DEFAULT 0,
    completed_projects INT DEFAULT 0,
    ongoing_projects INT DEFAULT 0,
    rating DECIMAL(3,2) DEFAULT 0.00,
    total_reviews INT DEFAULT 0,
    is_verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE cities (
    city_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    state VARCHAR(100) NOT NULL,
    country VARCHAR(100) NOT NULL,
    latitude DECIMAL(10,8),
    longitude DECIMAL(11,8)
);

CREATE TABLE localities (
    locality_id INT AUTO_INCREMENT PRIMARY KEY,
    city_id INT NOT NULL,
    name VARCHAR(255) NOT NULL,
    locality_type VARCHAR(20) DEFAULT 'locality' COMMENT 'locality, micro_market, suburb',
    pincode VARCHAR(10),
    latitude DECIMAL(10,8),
    longitude DECIMAL(11,8),
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (city_id) REFERENCES cities(city_id)
);

CREATE TABLE projects (
    project_id INT AUTO_INCREMENT PRIMARY KEY,
    developer_id INT NOT NULL,
    locality_id INT NOT NULL,
    name VARCHAR(255) NOT NULL,
    project_type VARCHAR(20) DEFAULT 'residential' COMMENT 'residential, commercial, mixed',
    property_type VARCHAR(20) NOT NULL COMMENT 'apartment, villa, plot, office, retail',
    status VARCHAR(30) NOT NULL COMMENT 'under_construction, ready_to_move, new_launch, completed',
    
    -- Project Details
    total_land_area DECIMAL(10,2) COMMENT 'in acres',
    total_units INT,
    unit_density DECIMAL(8,2) COMMENT 'units per acre',
    open_area_percentage DECIMAL(5,2),
    park_area DECIMAL(8,2) COMMENT 'in acres',
    clubhouse_area DECIMAL(10,2) COMMENT 'in sq ft',
    
    -- Pricing
    min_price DECIMAL(15,2),
    max_price DECIMAL(15,2),
    price_per_sqft DECIMAL(10,2),
    currency VARCHAR(10) DEFAULT 'INR',
    
    -- Timeline
    launch_date DATE,
    possession_date DATE,
    completion_date DATE,
    
    -- Location specifics
    address TEXT,
    latitude DECIMAL(10,8),
    longitude DECIMAL(11,8),
    approach_road_width DECIMAL(8,2) COMMENT 'in meters',
    nearest_metro_distance DECIMAL(8,2) COMMENT 'in km',
    airport_distance DECIMAL(8,2) COMMENT 'in km',
    
    -- RERA Details
    rera_number VARCHAR(100),
    rera_website VARCHAR(500),
    rera_status VARCHAR(20) DEFAULT 'approved' COMMENT 'approved, pending, expired',
    
    -- Content
    description TEXT,
    highlights TEXT,
    master_plan_url VARCHAR(500),
    brochure_url VARCHAR(500),
    
    -- SEO and Status
    meta_title VARCHAR(255),
    meta_description TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (developer_id) REFERENCES developers(developer_id),
    FOREIGN KEY (locality_id) REFERENCES localities(locality_id)
);

CREATE TABLE towers (
    tower_id INT AUTO_INCREMENT PRIMARY KEY,
    project_id INT NOT NULL,
    tower_name VARCHAR(100) NOT NULL,
    tower_number VARCHAR(50),
    total_floors INT NOT NULL,
    units_per_floor INT DEFAULT 0,
    total_units INT DEFAULT 0,
    tower_type VARCHAR(20) DEFAULT 'residential' COMMENT 'residential, commercial, mixed',
    
    -- Tower specifics
    construction_status VARCHAR(30) DEFAULT 'under_construction' COMMENT 'under_construction, completed, ready_to_move',
    possession_date DATE,
    height_meters DECIMAL(8,2),
    
    -- Facilities
    elevator_count INT DEFAULT 0,
    has_power_backup BOOLEAN DEFAULT TRUE,
    has_water_backup BOOLEAN DEFAULT TRUE,
    has_fire_safety BOOLEAN DEFAULT TRUE,
    
    -- Positioning
    latitude DECIMAL(10,8),
    longitude DECIMAL(11,8),
    facing_direction VARCHAR(20) COMMENT 'north, south, east, west, northeast, northwest, southeast, southwest',
    
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (project_id) REFERENCES projects(project_id)
);

CREATE TABLE unit_types (
    unit_type_id INT AUTO_INCREMENT PRIMARY KEY,
    project_id INT NOT NULL,
    type_name VARCHAR(100) NOT NULL COMMENT 'e.g., 3BHK, 4BHK+Maid, 1BHK+Study',
    bedrooms INT NOT NULL,
    bathrooms INT NOT NULL,
    
    -- Room counts
    master_bedrooms INT DEFAULT 0,
    child_bedrooms INT DEFAULT 0,
    guest_bedrooms INT DEFAULT 0,
    study_rooms INT DEFAULT 0,
    living_rooms INT DEFAULT 1,
    dining_rooms INT DEFAULT 0,
    kitchens INT DEFAULT 1,
    utility_rooms INT DEFAULT 0,
    store_rooms INT DEFAULT 0,
    pooja_rooms INT DEFAULT 0,
    
    -- Maid room details
    has_maid_room BOOLEAN DEFAULT FALSE,
    maid_room_area DECIMAL(8,2) COMMENT 'in sq ft',
    has_maid_bathroom BOOLEAN DEFAULT FALSE,
    
    -- Balcony details
    has_balcony BOOLEAN DEFAULT TRUE,
    balcony_count INT DEFAULT 0,
    total_balcony_area DECIMAL(8,2) COMMENT 'in sq ft',
    
    -- Additional areas
    has_terrace BOOLEAN DEFAULT FALSE,
    terrace_area DECIMAL(8,2) COMMENT 'in sq ft',
    has_private_garden BOOLEAN DEFAULT FALSE,
    private_garden_area DECIMAL(8,2) COMMENT 'in sq ft',
    
    -- Area Details
    carpet_area DECIMAL(10,2) COMMENT 'in sq ft',
    built_up_area DECIMAL(10,2) COMMENT 'in sq ft',
    super_area DECIMAL(10,2) COMMENT 'in sq ft',
    carpet_ratio DECIMAL(5,2) COMMENT 'carpet area percentage',
    
    -- Pricing
    base_price DECIMAL(15,2),
    price_per_sqft DECIMAL(10,2),
    
    -- Layout specifications
    floor_plan_url VARCHAR(500),
    floor_height DECIMAL(5,2) COMMENT 'in meters',
    ceiling_height DECIMAL(5,2) COMMENT 'in meters',
    facing_direction VARCHAR(20) COMMENT 'north, south, east, west, northeast, northwest, southeast, southwest',
    
    -- Door specifications
    main_door_type VARCHAR(50) COMMENT 'wooden, steel, glass, etc.',
    main_door_width DECIMAL(5,2) COMMENT 'in meters',
    main_door_height DECIMAL(5,2) COMMENT 'in meters',
    bedroom_door_type VARCHAR(50),
    bathroom_door_type VARCHAR(50),
    
    -- Window specifications
    window_type VARCHAR(50) COMMENT 'sliding, casement, french, etc.',
    window_material VARCHAR(50) COMMENT 'aluminum, upvc, wooden, etc.',
    
    -- Availability
    total_units INT DEFAULT 0,
    available_units INT DEFAULT 0,
    sold_units INT DEFAULT 0,
    
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (project_id) REFERENCES projects(project_id)
);

-- Enhanced room details table with comprehensive specifications
CREATE TABLE unit_room_details (
    room_detail_id INT AUTO_INCREMENT PRIMARY KEY,
    unit_type_id INT NOT NULL,
    room_type VARCHAR(50) NOT NULL COMMENT 'master_bedroom, child_bedroom, guest_bedroom, living_room, dining_room, kitchen, bathroom, balcony, study_room, utility_room, store_room, pooja_room, foyer, passage',
    room_name VARCHAR(100) COMMENT 'Master Bedroom, Child Bedroom 1, Living Room, etc.',
    room_sequence INT DEFAULT 1 COMMENT 'For multiple rooms of same type',
    
    -- Dimensions
    room_length DECIMAL(8,2) NOT NULL COMMENT 'in meters',
    room_width DECIMAL(8,2) NOT NULL COMMENT 'in meters',
    room_area DECIMAL(8,2) NOT NULL COMMENT 'in sq ft',
    
    -- Shape and layout
    room_shape VARCHAR(30) DEFAULT 'rectangular' COMMENT 'rectangular, square, l_shaped, irregular',
    
    -- Room specific features
    has_attached_bathroom BOOLEAN DEFAULT FALSE,
    has_balcony_access BOOLEAN DEFAULT FALSE,
    has_wardrobe BOOLEAN DEFAULT FALSE,
    wardrobe_type VARCHAR(50) COMMENT 'built-in, walk-in, modular',
    wardrobe_area DECIMAL(6,2) COMMENT 'in sq ft',
    
    -- Natural light and ventilation
    has_window BOOLEAN DEFAULT TRUE,
    window_count INT DEFAULT 1,
    window_total_area DECIMAL(6,2) COMMENT 'in sq ft',
    natural_light_rating VARCHAR(10) DEFAULT 'good' COMMENT 'excellent, good, average, poor',
    ventilation_rating VARCHAR(10) DEFAULT 'good' COMMENT 'excellent, good, average, poor',
    
    -- Doors and Windows specifications
    door_count INT DEFAULT 1,
    door_type VARCHAR(50) COMMENT 'single, double, sliding, folding',
    door_material VARCHAR(50) COMMENT 'wood, steel, glass, composite',
    door_width DECIMAL(5,2) COMMENT 'in meters',
    door_height DECIMAL(5,2) COMMENT 'in meters',
    
    window_type VARCHAR(50) COMMENT 'sliding, casement, french, bay, fixed',
    window_material VARCHAR(50) COMMENT 'aluminum, upvc, wooden, steel',
    window_width DECIMAL(5,2) COMMENT 'in meters',
    window_height DECIMAL(5,2) COMMENT 'in meters',
    
    -- Electrical specifications
    electrical_points INT DEFAULT 0,
    fan_points INT DEFAULT 0,
    ac_points INT DEFAULT 0,
    light_points INT DEFAULT 0,
    
    -- Flooring and ceiling
    flooring_type VARCHAR(50) COMMENT 'marble, vitrified_tiles, ceramic, wooden, granite',
    flooring_brand VARCHAR(100),
    ceiling_type VARCHAR(50) COMMENT 'pop, gypsum, concrete, wooden',
    ceiling_height DECIMAL(5,2) COMMENT 'in meters',
    
    -- Fixtures
    has_geyser_provision BOOLEAN DEFAULT FALSE,
    has_exhaust_fan BOOLEAN DEFAULT FALSE,
    has_chimney_provision BOOLEAN DEFAULT FALSE,
    
    -- Privacy and position
    privacy_level VARCHAR(20) DEFAULT 'private' COMMENT 'private, semi_private, open',
    position_in_unit VARCHAR(30) COMMENT 'front, back, side, central, corner',
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (unit_type_id) REFERENCES unit_types(unit_type_id)
);

-- New table for detailed balcony specifications
CREATE TABLE balcony_details (
    balcony_id INT AUTO_INCREMENT PRIMARY KEY,
    unit_type_id INT NOT NULL,
    balcony_name VARCHAR(100) COMMENT 'Master Bedroom Balcony, Living Room Balcony, etc.',
    balcony_sequence INT DEFAULT 1 COMMENT 'For multiple balconies',
    
    -- Dimensions
    balcony_length DECIMAL(8,2) NOT NULL COMMENT 'in meters',
    balcony_width DECIMAL(8,2) NOT NULL COMMENT 'in meters',
    balcony_area DECIMAL(8,2) NOT NULL COMMENT 'in sq ft',
    
    -- Access and connection
    connected_room VARCHAR(50) COMMENT 'master_bedroom, living_room, dining_room, kitchen',
    access_type VARCHAR(30) DEFAULT 'sliding_door' COMMENT 'sliding_door, french_door, open',
    
    -- Features
    balcony_type VARCHAR(30) DEFAULT 'regular' COMMENT 'regular, utility, sit_out, deck',
    has_provision_for_washing_machine BOOLEAN DEFAULT FALSE,
    has_provision_for_drying BOOLEAN DEFAULT TRUE,
    has_safety_grill BOOLEAN DEFAULT TRUE,
    
    -- View and orientation
    facing_direction VARCHAR(20) COMMENT 'north, south, east, west, northeast, northwest, southeast, southwest',
    view_description TEXT COMMENT 'garden view, road view, park view, etc.',
    floor_level VARCHAR(20) COMMENT 'ground, podium, tower, terrace',
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (unit_type_id) REFERENCES unit_types(unit_type_id)
);

CREATE TABLE property_units (
    unit_id INT AUTO_INCREMENT PRIMARY KEY,
    project_id INT NOT NULL,
    unit_type_id INT NOT NULL,
    tower_id INT NOT NULL,
    unit_number VARCHAR(50) NOT NULL,
    floor_number INT NOT NULL,
    
    unit_position VARCHAR(20) COMMENT 'corner, middle, end',
    wing VARCHAR(10) COMMENT 'A, B, C, etc.',
    
    -- Specific unit details
    carpet_area DECIMAL(10,2),
    built_up_area DECIMAL(10,2),
    super_area DECIMAL(10,2),
    
    has_corner_unit BOOLEAN DEFAULT FALSE,
    has_extra_balcony BOOLEAN DEFAULT FALSE,
    has_servant_quarter BOOLEAN DEFAULT FALSE,
    
    -- Pricing
    unit_price DECIMAL(15,2),
    price_per_sqft DECIMAL(10,2),
    maintenance_charge DECIMAL(10,2),
    
    -- Status
    status VARCHAR(20) DEFAULT 'available' COMMENT 'available, sold, blocked, reserved',
    possession_date DATE,
    
    -- Premium/Discount
    premium_percentage DECIMAL(5,2) DEFAULT 0.00,
    discount_percentage DECIMAL(5,2) DEFAULT 0.00,
    
    -- Specific details
    actual_facing_direction VARCHAR(20),
    view_description TEXT COMMENT 'garden view, road view, etc.',
    
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (project_id) REFERENCES projects(project_id),
    FOREIGN KEY (unit_type_id) REFERENCES unit_types(unit_type_id),
    FOREIGN KEY (tower_id) REFERENCES towers(tower_id)
);

-- Enhanced door and window specifications
CREATE TABLE door_window_specs (
    spec_id INT AUTO_INCREMENT PRIMARY KEY,
    unit_type_id INT NOT NULL,
    item_type VARCHAR(20) NOT NULL COMMENT 'door, window',
    location VARCHAR(100) NOT NULL COMMENT 'main_entrance, master_bedroom, kitchen, etc.',
    
    -- Physical specifications
    width DECIMAL(5,2) COMMENT 'in meters',
    height DECIMAL(5,2) COMMENT 'in meters',
    thickness DECIMAL(5,2) COMMENT 'in mm',
    
    -- Material and finish
    material VARCHAR(50) COMMENT 'wood, steel, aluminum, upvc, glass',
    finish VARCHAR(50) COMMENT 'polished, painted, laminated, etc.',
    brand VARCHAR(100),
    grade VARCHAR(50) COMMENT 'premium, standard, economy',
    
    -- Features
    is_security_door BOOLEAN DEFAULT FALSE,
    has_grill BOOLEAN DEFAULT FALSE,
    opening_type VARCHAR(30) COMMENT 'sliding, hinged, folding, casement',
    
    -- Hardware
    lock_type VARCHAR(50) COMMENT 'mortise, cylindrical, smart_lock',
    handle_type VARCHAR(50),
    handle_material VARCHAR(30),
    
    -- Glass specifications (for windows)
    glass_type VARCHAR(50) COMMENT 'clear, tinted, frosted, laminated',
    glass_thickness DECIMAL(4,2) COMMENT 'in mm',
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (unit_type_id) REFERENCES unit_types(unit_type_id)
);

CREATE TABLE amenities (
    amenity_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    category VARCHAR(20) NOT NULL COMMENT 'lifestyle, sports, natural, security, connectivity, wellness',
    icon_url VARCHAR(500),
    description TEXT,
    is_rare BOOLEAN DEFAULT FALSE COMMENT 'for rare amenities',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE project_amenities (
    project_id INT NOT NULL,
    amenity_id INT NOT NULL,
    is_available BOOLEAN DEFAULT TRUE,
    description TEXT,
    area_size DECIMAL(10,2) COMMENT 'in sq ft',
    capacity INT COMMENT 'number of people/units it can accommodate',
    operating_hours VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    PRIMARY KEY (project_id, amenity_id),
    FOREIGN KEY (project_id) REFERENCES projects(project_id),
    FOREIGN KEY (amenity_id) REFERENCES amenities(amenity_id)
);

CREATE TABLE project_media (
    media_id INT AUTO_INCREMENT PRIMARY KEY,
    project_id INT NOT NULL,
    media_type VARCHAR(20) NOT NULL COMMENT 'image, video, virtual_tour, floor_plan, master_plan',
    media_url VARCHAR(500) NOT NULL,
    thumbnail_url VARCHAR(500),
    title VARCHAR(255),
    description TEXT,
    media_category VARCHAR(20) DEFAULT 'exterior' COMMENT 'exterior, interior, amenities, views, construction, location',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (project_id) REFERENCES projects(project_id)
);

CREATE TABLE approvals (
    approval_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    is_mandatory BOOLEAN DEFAULT TRUE,
    category VARCHAR(20) DEFAULT 'legal' COMMENT 'legal, environmental, fire_safety, structural, other',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE project_approvals (
    project_id INT NOT NULL,
    approval_id INT NOT NULL,
    status VARCHAR(20) DEFAULT 'pending' COMMENT 'pending, approved, rejected, expired',
    approval_number VARCHAR(100),
    approval_date DATE,
    expiry_date DATE,
    issuing_authority VARCHAR(255),
    document_url VARCHAR(500),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    PRIMARY KEY (project_id, approval_id),
    FOREIGN KEY (project_id) REFERENCES projects(project_id),
    FOREIGN KEY (approval_id) REFERENCES approvals(approval_id)
);

CREATE TABLE project_documents (
    document_id INT AUTO_INCREMENT PRIMARY KEY,
    project_id INT NOT NULL,
    document_type VARCHAR(20) NOT NULL COMMENT 'brochure, price_list, floor_plan, master_plan, legal_doc, approval, other',
    title VARCHAR(255) NOT NULL,
    description TEXT,
    file_url VARCHAR(500) NOT NULL,
    file_size BIGINT COMMENT 'in bytes',
    file_type VARCHAR(50),
    is_public BOOLEAN DEFAULT TRUE,
    download_count INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (project_id) REFERENCES projects(project_id)
);

CREATE TABLE user_interests (
    interest_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    project_id INT,
    unit_type_id INT,
    interest_type VARCHAR(20) NOT NULL COMMENT 'enquiry, site_visit, callback, brochure_download, price_quote',
    
    -- Contact preferences
    preferred_contact_method VARCHAR(20) DEFAULT 'phone' COMMENT 'phone, email, whatsapp',
    preferred_contact_time VARCHAR(20) DEFAULT 'anytime' COMMENT 'morning, afternoon, evening, anytime',
    
    -- Requirements
    budget_min DECIMAL(15,2),
    budget_max DECIMAL(15,2),
    preferred_floors TEXT COMMENT 'comma separated',
    specific_requirements TEXT,
    
    -- Status
    status VARCHAR(30) DEFAULT 'new' COMMENT 'new, contacted, site_visit_scheduled, site_visit_done, negotiating, closed_won, closed_lost',
    assigned_to INT COMMENT 'agent user_id',
    
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (project_id) REFERENCES projects(project_id),
    FOREIGN KEY (unit_type_id) REFERENCES unit_types(unit_type_id),
    FOREIGN KEY (assigned_to) REFERENCES users(user_id)
);

CREATE TABLE reviews (
    review_id INT AUTO_INCREMENT PRIMARY KEY,
    project_id INT,
    developer_id INT,
    user_id INT NOT NULL,
    rating INT NOT NULL CHECK (rating >= 1 AND rating <= 5),
    title VARCHAR(255),
    review_text TEXT,
    pros TEXT,
    cons TEXT,
    
    -- Review categories
    construction_quality_rating INT CHECK (construction_quality_rating >= 1 AND construction_quality_rating <= 5),
    amenities_rating INT CHECK (amenities_rating >= 1 AND amenities_rating <= 5),
    location_rating INT CHECK (location_rating >= 1 AND location_rating <= 5),
    value_for_money_rating INT CHECK (value_for_money_rating >= 1 AND value_for_money_rating <= 5),
    
    is_verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (project_id) REFERENCES projects(project_id),
    FOREIGN KEY (developer_id) REFERENCES developers(developer_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE search_logs (
    search_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    search_query VARCHAR(500),
    filters_applied TEXT COMMENT 'JSON format',
    results_count INT,
    clicked_project_id INT,
    search_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    session_id VARCHAR(255),
    ip_address VARCHAR(45),
    
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (clicked_project_id) REFERENCES projects(project_id)
);

CREATE TABLE property_comparisons (
    comparison_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    project_ids TEXT NOT NULL COMMENT 'JSON Array of project IDs',
    comparison_parameters TEXT COMMENT 'JSON - Parameters used for comparison',
    session_id VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE notifications (
    notification_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    type VARCHAR(20) NOT NULL COMMENT 'price_change, new_project, similar_property, reminder, update, promotional',
    title VARCHAR(255) NOT NULL,
    message TEXT NOT NULL,
    related_project_id INT,
    is_read BOOLEAN DEFAULT FALSE,
    is_sent BOOLEAN DEFAULT FALSE,
    delivery_method VARCHAR(20) DEFAULT 'in_app' COMMENT 'email, sms, push, in_app',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    read_at TIMESTAMP NULL,
    
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (related_project_id) REFERENCES projects(project_id)
);

CREATE TABLE price_history (
    price_history_id INT AUTO_INCREMENT PRIMARY KEY,
    project_id INT,
    unit_type_id INT,
    old_price DECIMAL(15,2),
    new_price DECIMAL(15,2),
    old_price_per_sqft DECIMAL(10,2),
    new_price_per_sqft DECIMAL(10,2),
    change_percentage DECIMAL(5,2),
    change_reason VARCHAR(255),
    effective_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (project_id) REFERENCES projects(project_id),
    FOREIGN KEY (unit_type_id) REFERENCES unit_types(unit_type_id)
);
