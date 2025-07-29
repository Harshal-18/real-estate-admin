-- PostgreSQL compatible backup for Render deployment
-- Converted from MySQL backup

-- Create tables and insert data for PostgreSQL

-- Amenities table
CREATE TABLE IF NOT EXISTS amenities (
    amenity_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    category VARCHAR(20) NOT NULL,
    icon_url VARCHAR(500),
    description TEXT,
    is_rare BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert amenities data
INSERT INTO amenities (name, category, icon_url, description, is_rare, is_active, created_at) VALUES
('Swimming Pool', 'lifestyle', NULL, NULL, FALSE, TRUE, '2025-07-16 05:53:07'),
('Gymnasium', 'lifestyle', NULL, NULL, FALSE, TRUE, '2025-07-16 05:53:07'),
('Club House', 'lifestyle', NULL, NULL, FALSE, TRUE, '2025-07-16 05:53:07'),
('Children''s Play Area', 'lifestyle', NULL, NULL, FALSE, TRUE, '2025-07-16 05:53:07'),
('Indoor Games', 'sports', NULL, NULL, FALSE, TRUE, '2025-07-16 05:53:07'),
('Landscaped Gardens', 'natural', NULL, NULL, FALSE, TRUE, '2025-07-16 05:53:07'),
('24/7 Security', 'security', '', '', FALSE, TRUE, '2025-07-16 05:53:07'),
('Tennis Court', 'sports', NULL, NULL, TRUE, TRUE, '2025-07-16 05:53:07'),
('Yoga Deck', 'lifestyle', NULL, NULL, FALSE, TRUE, '2025-07-16 05:53:07'),
('Multipurpose Hall', 'lifestyle', NULL, NULL, FALSE, TRUE, '2025-07-16 05:53:07');

-- Cities table
CREATE TABLE IF NOT EXISTS cities (
    city_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    state VARCHAR(100) NOT NULL,
    country VARCHAR(100) NOT NULL,
    latitude DECIMAL(10,8),
    longitude DECIMAL(11,8),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert cities data
INSERT INTO cities (name, state, country, latitude, longitude, created_at) VALUES
('Bengaluru', 'Karnataka', 'India', 12.97160000, 77.59460000, '2025-07-16 07:32:22'),
('Ahmedabad', 'Gujarat', 'India', 23.02260000, 72.57140000, '2025-07-16 07:33:37'),
('Surat', 'Gujrat', 'India', NULL, NULL, '2025-07-16 07:35:18');

-- Developers table
CREATE TABLE IF NOT EXISTS developers (
    developer_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    established_year INTEGER,
    description TEXT,
    logo_url VARCHAR(500),
    website_url VARCHAR(500),
    contact_email VARCHAR(255),
    contact_phone VARCHAR(20),
    address TEXT,
    total_projects INTEGER DEFAULT 0,
    completed_projects INTEGER DEFAULT 0,
    ongoing_projects INTEGER DEFAULT 0,
    rating DECIMAL(3,2) DEFAULT 0.00,
    total_reviews INTEGER DEFAULT 0,
    is_verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert developers data
INSERT INTO developers (name, established_year, description, logo_url, website_url, contact_email, contact_phone, address, total_projects, completed_projects, ongoing_projects, rating, total_reviews, is_verified, created_at) VALUES
('Lodha Group', 1980, 'Lodha Group is India''s largest residential real estate developer by sales and construction area.', NULL, 'https://www.lodhagroup.com', 'sales@lodha.com', NULL, NULL, 2, 0, 1, 0.00, 0, TRUE, '2025-07-16 05:53:07'),
('East Park Developers', 1995, 'East Park Developers is known for quality construction and timely delivery.', NULL, 'https://www.eastpark.com', 'info@eastpark.com', NULL, NULL, 0, 0, 0, 0.00, 0, TRUE, '2025-07-16 05:53:07'),
('Brigade Group', 1986, 'Brigade Group is one of India''s leading property developers with over three decades of expertise.', NULL, 'https://www.brigadegroup.com', 'sales@brigadegroup.com', NULL, NULL, 2, 0, 0, 0.00, 0, TRUE, '2025-07-16 05:53:07');

-- Localities table
CREATE TABLE IF NOT EXISTS localities (
    locality_id SERIAL PRIMARY KEY,
    city_id INTEGER NOT NULL,
    name VARCHAR(255) NOT NULL,
    locality_type VARCHAR(20) DEFAULT 'locality',
    pincode VARCHAR(10),
    latitude DECIMAL(10,8),
    longitude DECIMAL(11,8),
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert localities data
INSERT INTO localities (city_id, name, locality_type, pincode, latitude, longitude, description, created_at) VALUES
(1, 'Whitefield', 'micro_market', '560066', 12.96980000, 77.75000000, NULL, '2025-07-16 05:53:07'),
(1, 'Hennur', 'locality', '560043', 13.02730000, 77.63320000, NULL, '2025-07-16 05:53:07'),
(1, 'Vittal Mallya Road', 'locality', '560001', 12.97200000, 77.59530000, NULL, '2025-07-16 05:53:07'),
(2, 'Kankariya_lake', 'round-about lake', '380008', 23.02260000, 72.57140000, 'This is the very famous lake of the ahmedabad with high rush on weekends and also on weekdays as well', '2025-07-16 04:15:25');

-- Projects table
CREATE TABLE IF NOT EXISTS projects (
    project_id SERIAL PRIMARY KEY,
    developer_id INTEGER NOT NULL,
    locality_id INTEGER NOT NULL,
    name VARCHAR(255) NOT NULL,
    project_type VARCHAR(20) DEFAULT 'residential',
    property_type VARCHAR(20) NOT NULL,
    status VARCHAR(30) NOT NULL,
    total_land_area DECIMAL(10,2),
    total_units INTEGER,
    unit_density DECIMAL(8,2),
    open_area_percentage DECIMAL(5,2),
    park_area DECIMAL(8,2),
    clubhouse_area DECIMAL(10,2),
    min_price DECIMAL(15,2),
    max_price DECIMAL(15,2),
    price_per_sqft DECIMAL(10,2),
    currency VARCHAR(10) DEFAULT 'INR',
    launch_date DATE,
    possession_date DATE,
    completion_date DATE,
    address TEXT,
    latitude DECIMAL(10,8),
    longitude DECIMAL(11,8),
    approach_road_width DECIMAL(8,2),
    nearest_metro_distance DECIMAL(8,2),
    airport_distance DECIMAL(8,2),
    rera_number VARCHAR(100),
    rera_website VARCHAR(500),
    rera_status VARCHAR(20) DEFAULT 'approved',
    description TEXT,
    highlights TEXT,
    master_plan_url VARCHAR(500),
    brochure_url VARCHAR(500),
    meta_title VARCHAR(255),
    meta_description TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert projects data
INSERT INTO projects (developer_id, locality_id, name, project_type, property_type, status, total_land_area, total_units, unit_density, open_area_percentage, park_area, clubhouse_area, min_price, max_price, price_per_sqft, currency, launch_date, possession_date, completion_date, address, latitude, longitude, approach_road_width, nearest_metro_distance, airport_distance, rera_number, rera_website, rera_status, description, highlights, master_plan_url, brochure_url, meta_title, meta_description, is_active, created_at) VALUES
(1, 1, 'Lodha Haven', 'residential', 'apartment', 'under_construction', 9.10, 250, 50.00, 77.00, 0.90, 73.00, 15000000.00, 30000000.00, 8500.00, 'INR', '2023-01-15', '2026-12-31', NULL, 'Choodasandra, Bengaluru', NULL, NULL, 17.00, 4.17, NULL, '', '', 'approved', 'Lodha Haven offers premium 2, 3 & 4 BHK apartments with world-class amenities in Whitefield, Bangalore.', '', 'Master_plan_Lodha_Haven.png', NULL, '', '', TRUE, '2025-07-16 05:53:07'),
(2, 2, 'East Park Residences', 'residential', 'apartment', 'under_construction', 4.20, 180, NULL, NULL, NULL, NULL, 18000000.00, 35000000.00, 9200.00, 'INR', '2023-03-01', '2026-06-30', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'approved', 'East Park Residences presents luxurious 3 & 4 BHK apartments in Hennur, Bangalore with modern amenities.', NULL, NULL, NULL, NULL, NULL, TRUE, '2025-07-16 05:53:07'),
(3, 3, 'Brigade Insignia', 'residential', 'apartment', 'ready_to_move', 3.80, 160, 10.00, 70.00, 20.00, 19.00, 25000000.00, 50000000.00, 12500.00, 'INR', '2020-06-01', '2024-03-31', NULL, '', NULL, NULL, NULL, NULL, NULL, '', '', 'approved', 'Brigade Insignia offers ultra-luxury 3 & 4 BHK apartments in the heart of Bangalore with premium amenities.', '', NULL, NULL, '', '', TRUE, '2025-07-16 05:53:07');

-- Towers table
CREATE TABLE IF NOT EXISTS towers (
    tower_id SERIAL PRIMARY KEY,
    project_id INTEGER NOT NULL,
    tower_name VARCHAR(100) NOT NULL,
    tower_number VARCHAR(50),
    total_floors INTEGER NOT NULL,
    units_per_floor INTEGER DEFAULT 0,
    total_units INTEGER DEFAULT 0,
    tower_type VARCHAR(20) DEFAULT 'residential',
    construction_status VARCHAR(30) DEFAULT 'under_construction',
    possession_date DATE,
    height_meters DECIMAL(8,2),
    elevator_count INTEGER DEFAULT 0,
    has_power_backup BOOLEAN DEFAULT TRUE,
    has_water_backup BOOLEAN DEFAULT TRUE,
    has_fire_safety BOOLEAN DEFAULT TRUE,
    latitude DECIMAL(10,8),
    longitude DECIMAL(11,8),
    facing_direction VARCHAR(20),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert towers data
INSERT INTO towers (project_id, tower_name, tower_number, total_floors, units_per_floor, total_units, tower_type, construction_status, possession_date, height_meters, elevator_count, has_power_backup, has_water_backup, has_fire_safety, latitude, longitude, facing_direction, is_active, created_at) VALUES
(1, 'Haven A', NULL, 20, 4, 80, 'residential', 'under_construction', NULL, NULL, 0, TRUE, TRUE, TRUE, NULL, NULL, NULL, TRUE, '2025-07-16 12:11:13'),
(1, 'Haven B', NULL, 20, 4, 80, 'residential', 'under_construction', NULL, NULL, 0, TRUE, TRUE, TRUE, NULL, NULL, NULL, TRUE, '2025-07-16 12:11:13'),
(1, 'Haven C', NULL, 22, 4, 88, 'residential', 'under_construction', NULL, NULL, 0, TRUE, TRUE, TRUE, NULL, NULL, NULL, TRUE, '2025-07-16 12:11:13'),
(2, 'East Wing', NULL, 15, 4, 60, 'residential', 'under_construction', NULL, NULL, 0, TRUE, TRUE, TRUE, NULL, NULL, NULL, TRUE, '2025-07-16 12:11:13'),
(2, 'West Wing', NULL, 15, 4, 60, 'residential', 'under_construction', NULL, NULL, 0, TRUE, TRUE, TRUE, NULL, NULL, NULL, TRUE, '2025-07-16 12:11:13'),
(2, 'Central Tower', NULL, 15, 4, 60, 'residential', 'under_construction', NULL, NULL, 0, TRUE, TRUE, TRUE, NULL, NULL, NULL, TRUE, '2025-07-16 12:11:13'),
(3, 'Insignia Tower 1', NULL, 25, 2, 50, 'residential', 'ready_to_move', NULL, NULL, 0, TRUE, TRUE, TRUE, NULL, NULL, NULL, TRUE, '2025-07-16 12:11:13'),
(3, 'Insignia Tower 2', NULL, 25, 2, 50, 'residential', 'ready_to_move', NULL, NULL, 0, TRUE, TRUE, TRUE, NULL, NULL, NULL, TRUE, '2025-07-16 12:11:13'),
(3, 'Insignia Tower 3', NULL, 20, 3, 60, 'residential', 'ready_to_move', NULL, NULL, 0, TRUE, TRUE, TRUE, NULL, NULL, NULL, TRUE, '2025-07-16 12:11:13');

-- Unit types table
CREATE TABLE IF NOT EXISTS unit_types (
    unit_type_id SERIAL PRIMARY KEY,
    project_id INTEGER NOT NULL,
    type_name VARCHAR(100) NOT NULL,
    bedrooms INTEGER NOT NULL,
    bathrooms INTEGER NOT NULL,
    master_bedrooms INTEGER DEFAULT 0,
    child_bedrooms INTEGER DEFAULT 0,
    guest_bedrooms INTEGER DEFAULT 0,
    study_rooms INTEGER DEFAULT 0,
    living_rooms INTEGER DEFAULT 1,
    dining_rooms INTEGER DEFAULT 0,
    kitchens INTEGER DEFAULT 1,
    utility_rooms INTEGER DEFAULT 0,
    store_rooms INTEGER DEFAULT 0,
    pooja_rooms INTEGER DEFAULT 0,
    has_maid_room BOOLEAN DEFAULT FALSE,
    maid_room_area DECIMAL(8,2),
    has_maid_bathroom BOOLEAN DEFAULT FALSE,
    has_balcony BOOLEAN DEFAULT TRUE,
    balcony_count INTEGER DEFAULT 0,
    total_balcony_area DECIMAL(8,2),
    has_terrace BOOLEAN DEFAULT FALSE,
    terrace_area DECIMAL(8,2),
    has_private_garden BOOLEAN DEFAULT FALSE,
    private_garden_area DECIMAL(8,2),
    carpet_area DECIMAL(10,2),
    built_up_area DECIMAL(10,2),
    super_area DECIMAL(10,2),
    carpet_ratio DECIMAL(5,2),
    base_price DECIMAL(15,2),
    price_per_sqft DECIMAL(10,2),
    floor_plan_url VARCHAR(500),
    floor_height DECIMAL(5,2),
    ceiling_height DECIMAL(5,2),
    facing_direction VARCHAR(20),
    main_door_type VARCHAR(50),
    main_door_width DECIMAL(5,2),
    main_door_height DECIMAL(5,2),
    bedroom_door_type VARCHAR(50),
    bathroom_door_type VARCHAR(50),
    window_type VARCHAR(50),
    window_material VARCHAR(50),
    total_units INTEGER DEFAULT 0,
    available_units INTEGER DEFAULT 0,
    sold_units INTEGER DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert unit types data
INSERT INTO unit_types (project_id, type_name, bedrooms, bathrooms, master_bedrooms, child_bedrooms, guest_bedrooms, study_rooms, living_rooms, dining_rooms, kitchens, utility_rooms, store_rooms, pooja_rooms, has_maid_room, maid_room_area, has_maid_bathroom, has_balcony, balcony_count, total_balcony_area, has_terrace, terrace_area, has_private_garden, private_garden_area, carpet_area, built_up_area, super_area, carpet_ratio, base_price, price_per_sqft, floor_plan_url, floor_height, ceiling_height, facing_direction, main_door_type, main_door_width, main_door_height, bedroom_door_type, bathroom_door_type, window_type, window_material, total_units, available_units, sold_units, is_active, created_at) VALUES
(1, '2 BHK Premium', 2, 2, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, FALSE, NULL, FALSE, TRUE, 0, NULL, FALSE, NULL, FALSE, NULL, 1050.00, 1250.00, 1450.00, NULL, 15000000.00, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0, 0, TRUE, '2025-07-16 05:53:07'),
(1, '3 BHK Luxury', 3, 3, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, FALSE, NULL, FALSE, TRUE, 0, NULL, FALSE, NULL, FALSE, NULL, 1550.00, 1850.00, 2100.00, NULL, 22000000.00, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0, 0, TRUE, '2025-07-16 05:53:07'),
(1, '4 BHK Ultra Luxury', 4, 4, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, FALSE, NULL, FALSE, TRUE, 0, NULL, FALSE, NULL, FALSE, NULL, 2200.00, 2600.00, 2900.00, NULL, 30000000.00, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0, 0, TRUE, '2025-07-16 05:53:07'),
(2, '3 BHK Classic', 3, 3, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, FALSE, NULL, FALSE, TRUE, 0, NULL, FALSE, NULL, FALSE, NULL, 1650.00, 1950.00, 2200.00, NULL, 18000000.00, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0, 0, TRUE, '2025-07-16 05:53:07'),
(2, '3 BHK Premium', 3, 3, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, FALSE, NULL, FALSE, TRUE, 0, NULL, FALSE, NULL, FALSE, NULL, 1800.00, 2100.00, 2400.00, NULL, 25000000.00, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0, 0, TRUE, '2025-07-16 05:53:07'),
(2, '4 BHK Luxury', 4, 4, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, FALSE, NULL, FALSE, TRUE, 0, NULL, FALSE, NULL, FALSE, NULL, 2400.00, 2800.00, 3100.00, NULL, 35000000.00, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0, 0, TRUE, '2025-07-16 05:53:07'),
(3, '3 BHK Ultra Luxury', 3, 3, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, FALSE, NULL, FALSE, TRUE, 0, NULL, FALSE, NULL, FALSE, NULL, 2100.00, 2400.00, 2700.00, NULL, 25000000.00, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0, 0, TRUE, '2025-07-16 05:53:07'),
(3, '4 BHK Premium', 4, 4, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, FALSE, NULL, FALSE, TRUE, 0, NULL, FALSE, NULL, FALSE, NULL, 2800.00, 3200.00, 3600.00, NULL, 35000000.00, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0, 0, TRUE, '2025-07-16 05:53:07'),
(3, '4 BHK Penthouse', 4, 5, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, FALSE, NULL, FALSE, TRUE, 0, NULL, FALSE, NULL, FALSE, NULL, 3500.00, 4000.00, 4500.00, NULL, 50000000.00, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0, 0, TRUE, '2025-07-16 05:53:07');

-- Users table
CREATE TABLE IF NOT EXISTS users (
    user_id SERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    phone VARCHAR(20) UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    user_type VARCHAR(20) DEFAULT 'buyer',
    is_verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP,
    profile_image_url VARCHAR(500),
    is_active BOOLEAN DEFAULT TRUE,
    is_admin BOOLEAN DEFAULT FALSE
);

-- Insert users data
INSERT INTO users (email, phone, password_hash, first_name, last_name, user_type, is_verified, created_at, last_login, profile_image_url, is_active, is_admin) VALUES
('abc.123@gmail.com', '1234567891', 'Hi@123', 'ABC', 'ABD', 'custoomer', TRUE, '2025-07-16 05:21:17', NULL, '', TRUE, FALSE),
('abc.1234@gmail.com', NULL, 'pbkdf2:sha256:600000$VGrpf2ktzzTFQpBm$574423fe46d37db2fdc7335a6c51f9d4134508bd42106eef815399713da8409a', 'Priyanshu', 'Patel', 'buyer', FALSE, '2025-07-22 00:26:59', NULL, NULL, TRUE, FALSE),
('abc.12345@gmail.com', NULL, 'pbkdf2:sha256:600000$LP2lSCA6hcfYXnZS$afb517562c573691cb6d4b74e0d39395873dc9cef9f0458eb621cadcc9285cd8', 'Priyanshu', 'Patel', 'buyer', FALSE, '2025-07-22 00:32:57', NULL, NULL, TRUE, TRUE),
('abd.123@gmail.com', NULL, 'pbkdf2:sha256:600000$prVPGhGf5ZTFnr8u$b4080616eeee38652059403ea6d6aa87d91a15bc2a4363ac1af6b4e5f81a7edb', 'Harshal', 'Joshi', 'buyer', FALSE, '2025-07-22 02:39:13', NULL, NULL, TRUE, TRUE);

-- Project amenities table
CREATE TABLE IF NOT EXISTS project_amenities (
    project_id INTEGER NOT NULL,
    amenity_id INTEGER NOT NULL,
    is_available BOOLEAN DEFAULT TRUE,
    description TEXT,
    area_size DECIMAL(10,2),
    capacity INTEGER,
    operating_hours VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (project_id, amenity_id)
);

-- Insert project amenities data
INSERT INTO project_amenities (project_id, amenity_id, is_available, description, area_size, capacity, operating_hours, created_at) VALUES
(1, 1, TRUE, NULL, NULL, NULL, NULL, '2025-07-16 05:53:07'),
(1, 2, TRUE, NULL, NULL, NULL, NULL, '2025-07-16 05:53:07'),
(1, 3, TRUE, NULL, NULL, NULL, NULL, '2025-07-16 05:53:07'),
(1, 4, TRUE, NULL, NULL, NULL, NULL, '2025-07-16 05:53:07'),
(1, 6, TRUE, NULL, NULL, NULL, NULL, '2025-07-16 05:53:07'),
(1, 7, TRUE, NULL, NULL, NULL, NULL, '2025-07-16 05:53:07'),
(2, 1, TRUE, NULL, NULL, NULL, NULL, '2025-07-16 05:53:07'),
(2, 2, TRUE, NULL, NULL, NULL, NULL, '2025-07-16 05:53:07'),
(2, 3, TRUE, NULL, NULL, NULL, NULL, '2025-07-16 05:53:07'),
(2, 4, TRUE, NULL, NULL, NULL, NULL, '2025-07-16 05:53:07'),
(2, 5, TRUE, NULL, NULL, NULL, NULL, '2025-07-16 05:53:07'),
(2, 7, TRUE, NULL, NULL, NULL, NULL, '2025-07-16 05:53:07'),
(2, 9, TRUE, NULL, NULL, NULL, NULL, '2025-07-16 05:53:07'),
(3, 1, TRUE, NULL, NULL, NULL, NULL, '2025-07-16 05:53:07'),
(3, 2, TRUE, NULL, NULL, NULL, NULL, '2025-07-16 05:53:07'),
(3, 3, TRUE, NULL, NULL, NULL, NULL, '2025-07-16 05:53:07'),
(3, 6, TRUE, NULL, NULL, NULL, NULL, '2025-07-16 05:53:07'),
(3, 7, TRUE, NULL, NULL, NULL, NULL, '2025-07-16 05:53:07'),
(3, 8, TRUE, NULL, NULL, NULL, NULL, '2025-07-16 05:53:07'),
(3, 10, TRUE, NULL, NULL, NULL, NULL, '2025-07-16 05:53:07');

-- Property units table
CREATE TABLE IF NOT EXISTS property_units (
    unit_id SERIAL PRIMARY KEY,
    project_id INTEGER NOT NULL,
    unit_type_id INTEGER NOT NULL,
    tower_id INTEGER NOT NULL,
    unit_number VARCHAR(50) NOT NULL,
    floor_number INTEGER NOT NULL,
    unit_position VARCHAR(20),
    wing VARCHAR(10),
    carpet_area DECIMAL(10,2),
    built_up_area DECIMAL(10,2),
    super_area DECIMAL(10,2),
    has_corner_unit BOOLEAN DEFAULT FALSE,
    has_extra_balcony BOOLEAN DEFAULT FALSE,
    has_servant_quarter BOOLEAN DEFAULT FALSE,
    unit_price DECIMAL(15,2),
    price_per_sqft DECIMAL(10,2),
    maintenance_charge DECIMAL(10,2),
    status VARCHAR(20) DEFAULT 'available',
    possession_date DATE,
    premium_percentage DECIMAL(5,2) DEFAULT 0.00,
    discount_percentage DECIMAL(5,2) DEFAULT 0.00,
    actual_facing_direction VARCHAR(20),
    view_description TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    block_number VARCHAR(50),
    booking_status VARCHAR(50),
    possession_status VARCHAR(50),
    base_price DECIMAL(15,2),
    premium_charges DECIMAL(15,2),
    other_charges DECIMAL(15,2),
    total_price DECIMAL(15,2),
    facing_direction VARCHAR(50),
    view_type VARCHAR(50),
    corner_unit BOOLEAN DEFAULT FALSE,
    has_private_terrace BOOLEAN DEFAULT FALSE,
    has_private_garden BOOLEAN DEFAULT FALSE,
    is_modified BOOLEAN DEFAULT FALSE,
    modifications TEXT
);

-- Insert property units data
INSERT INTO property_units (project_id, unit_type_id, tower_id, unit_number, floor_number, unit_position, wing, carpet_area, built_up_area, super_area, has_corner_unit, has_extra_balcony, has_servant_quarter, unit_price, price_per_sqft, maintenance_charge, status, possession_date, premium_percentage, discount_percentage, actual_facing_direction, view_description, is_active, created_at, block_number, booking_status, possession_status, base_price, premium_charges, other_charges, total_price, facing_direction, view_type, corner_unit, has_private_terrace, has_private_garden, is_modified, modifications) VALUES
(1, 1, 1, 'A-1201', 12, NULL, NULL, NULL, NULL, NULL, FALSE, FALSE, FALSE, 15500000.00, NULL, NULL, 'available', NULL, 0.00, 0.00, NULL, NULL, TRUE, '2025-07-16 05:53:07', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, FALSE, FALSE, FALSE, FALSE, NULL),
(1, 2, 2, 'B-1502', 15, NULL, NULL, NULL, NULL, NULL, FALSE, FALSE, FALSE, 22500000.00, NULL, NULL, 'available', NULL, 0.00, 0.00, NULL, NULL, TRUE, '2025-07-16 05:53:07', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, FALSE, FALSE, FALSE, FALSE, NULL),
(1, 3, 3, 'C-1801', 18, NULL, NULL, NULL, NULL, NULL, FALSE, FALSE, FALSE, 31000000.00, NULL, NULL, 'available', NULL, 0.00, 0.00, NULL, NULL, TRUE, '2025-07-16 05:53:07', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, FALSE, FALSE, FALSE, FALSE, NULL),
(2, 4, 4, 'EW-1001', 10, NULL, NULL, NULL, NULL, NULL, FALSE, FALSE, FALSE, 18500000.00, NULL, NULL, 'available', NULL, 0.00, 0.00, NULL, NULL, TRUE, '2025-07-16 05:53:07', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, FALSE, FALSE, FALSE, FALSE, NULL),
(2, 5, 5, 'WW-1102', 11, NULL, NULL, NULL, NULL, NULL, FALSE, FALSE, FALSE, 25500000.00, NULL, NULL, 'available', NULL, 0.00, 0.00, NULL, NULL, TRUE, '2025-07-16 05:53:07', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, FALSE, FALSE, FALSE, FALSE, NULL),
(2, 6, 6, 'CT-1401', 14, NULL, NULL, NULL, NULL, NULL, FALSE, FALSE, FALSE, 35500000.00, NULL, NULL, 'available', NULL, 0.00, 0.00, NULL, NULL, TRUE, '2025-07-16 05:53:07', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, FALSE, FALSE, FALSE, FALSE, NULL),
(3, 7, 7, 'T1-2001', 20, NULL, NULL, NULL, NULL, NULL, FALSE, FALSE, FALSE, 26000000.00, NULL, NULL, 'available', NULL, 0.00, 0.00, NULL, NULL, TRUE, '2025-07-16 05:53:07', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, FALSE, FALSE, FALSE, FALSE, NULL),
(3, 8, 8, 'T2-2202', 22, NULL, NULL, NULL, NULL, NULL, FALSE, FALSE, FALSE, 36000000.00, NULL, NULL, 'available', NULL, 0.00, 0.00, NULL, NULL, TRUE, '2025-07-16 05:53:07', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, FALSE, FALSE, FALSE, FALSE, NULL),
(3, 9, 9, 'T3-2001', 20, NULL, NULL, NULL, NULL, NULL, FALSE, FALSE, FALSE, 51000000.00, NULL, NULL, 'available', NULL, 0.00, 0.00, NULL, NULL, TRUE, '2025-07-16 05:53:07', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, FALSE, FALSE, FALSE, FALSE, NULL);

-- Project media table
CREATE TABLE IF NOT EXISTS project_media (
    media_id SERIAL PRIMARY KEY,
    project_id INTEGER NOT NULL,
    media_type VARCHAR(20) NOT NULL,
    media_url VARCHAR(500) NOT NULL,
    thumbnail_url VARCHAR(500),
    title VARCHAR(255),
    description TEXT,
    media_category VARCHAR(20) DEFAULT 'exterior',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert project media data
INSERT INTO project_media (project_id, media_type, media_url, thumbnail_url, title, description, media_category, is_active, created_at) VALUES
(1, 'image', 'uploads/Lodha_Haven.webp', 'https://www.propsoch.com/_next/image?url=https%3A%2F%2Fd1zk2x7mtoyb2b.cloudfront.net%2FProjectImages%2F571-lodha-haven-choodasandra%2Fviews-3DRender-4.webp&w=3840&q=75', '', '', 'photo', TRUE, '2025-07-23 01:17:42'),
(2, 'image', 'uploads/East_Park_Residences.webp', 'https://www.propsoch.com/_next/image?url=https%3A%2F%2Fd1zk2x7mtoyb2b.cloudfront.net%2FProjectImages%2F335-east-park-residences-sarjapur-road%2Fviews-2.jpg&w=3840&q=75', 'Main photo', '', 'photo', TRUE, '2025-07-23 02:48:54'),
(3, 'image', 'uploads/Brigade_Insignia.webp', 'https://www.propsoch.com/_next/image?url=https%3A%2F%2Fd1zk2x7mtoyb2b.cloudfront.net%2FProjectImages%2F369-brigade-insignia-yelahanka%2Fviews-2.png&w=3840&q=75', 'This is the main photo', '', 'photo', TRUE, '2025-07-23 02:56:28'),
(1, 'image', 'uploads/Master_plan_Lodha_Haven.png', 'https://www.propsoch.com/_next/image?url=https%3A%2F%2Fd1zk2x7mtoyb2b.cloudfront.net%2FProjectImages%2F571-lodha-haven-choodasandra%2FmasterPlan.png&w=2048&q=75', 'Master plan', '', 'master_plan', TRUE, '2025-07-23 04:32:50'),
(2, 'image', 'uploads/Master_plan_East_Park_Residences.png', 'https://www.propsoch.com/_next/image?url=https%3A%2F%2Fd1zk2x7mtoyb2b.cloudfront.net%2FProjectImages%2F335-east-park-residences-sarjapur-road%2FmasterPlan-5.png&w=2048&q=75', 'Master plan', '', 'master_plan', TRUE, '2025-07-23 07:29:01'),
(3, 'image', 'uploads/Master_plan_Brigade_Insignia.png', 'https://www.propsoch.com/_next/image?url=https%3A%2F%2Fd1zk2x7mtoyb2b.cloudfront.net%2FProjectImages%2F369-brigade-insignia-yelahanka%2FmasterPlan-17.png&w=2048&q=75', 'Master plan', '', 'master_plan', TRUE, '2025-07-23 07:37:24');

-- Add foreign key constraints
ALTER TABLE localities ADD CONSTRAINT localities_city_id_fkey FOREIGN KEY (city_id) REFERENCES cities(city_id);
ALTER TABLE projects ADD CONSTRAINT projects_developer_id_fkey FOREIGN KEY (developer_id) REFERENCES developers(developer_id);
ALTER TABLE projects ADD CONSTRAINT projects_locality_id_fkey FOREIGN KEY (locality_id) REFERENCES localities(locality_id);
ALTER TABLE towers ADD CONSTRAINT towers_project_id_fkey FOREIGN KEY (project_id) REFERENCES projects(project_id);
ALTER TABLE unit_types ADD CONSTRAINT unit_types_project_id_fkey FOREIGN KEY (project_id) REFERENCES projects(project_id);
ALTER TABLE property_units ADD CONSTRAINT property_units_project_id_fkey FOREIGN KEY (project_id) REFERENCES projects(project_id);
ALTER TABLE property_units ADD CONSTRAINT property_units_unit_type_id_fkey FOREIGN KEY (unit_type_id) REFERENCES unit_types(unit_type_id);
ALTER TABLE property_units ADD CONSTRAINT property_units_tower_id_fkey FOREIGN KEY (tower_id) REFERENCES towers(tower_id);
ALTER TABLE project_amenities ADD CONSTRAINT project_amenities_project_id_fkey FOREIGN KEY (project_id) REFERENCES projects(project_id);
ALTER TABLE project_amenities ADD CONSTRAINT project_amenities_amenity_id_fkey FOREIGN KEY (amenity_id) REFERENCES amenities(amenity_id);
ALTER TABLE project_media ADD CONSTRAINT project_media_project_id_fkey FOREIGN KEY (project_id) REFERENCES projects(project_id); 