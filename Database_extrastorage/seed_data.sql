-- Seed data for Real Estate Database
CREATE DATABASE IF NOT EXISTS real_estate_db;
USE real_estate_db;

-- Cities
INSERT INTO cities (city_id, name, state, country, latitude, longitude) VALUES
(1, 'Bengaluru', 'Karnataka', 'India', 12.9716, 77.5946);

SELECT * FROM cities;

-- Developers
INSERT INTO developers (developer_id, name, established_year, description, website_url, contact_email, is_verified) VALUES
(1, 'Lodha Group', 1980, 'Lodha Group is India\'s largest residential real estate developer by sales and construction area.', 'https://www.lodhagroup.com', 'sales@lodha.com', true),
(2, 'East Park Developers', 1995, 'East Park Developers is known for quality construction and timely delivery.', 'https://www.eastpark.com', 'info@eastpark.com', true),
(3, 'Brigade Group', 1986, 'Brigade Group is one of India\'s leading property developers with over three decades of expertise.', 'https://www.brigadegroup.com', 'sales@brigadegroup.com', true);

SELECT * FROM developers;

-- Localities
INSERT INTO localities (locality_id, city_id, name, locality_type, pincode, latitude, longitude) VALUES
(1, 1, 'Whitefield', 'micro_market', '560066', 12.9698, 77.7500),
(2, 1, 'Hennur', 'locality', '560043', 13.0273, 77.6332),
(3, 1, 'Vittal Mallya Road', 'locality', '560001', 12.9720, 77.5953);

SELECT * FROM localities;

-- Basic Amenities
INSERT INTO amenities (amenity_id, name, category, is_rare) VALUES
(1, 'Swimming Pool', 'lifestyle', false),
(2, 'Gymnasium', 'lifestyle', false),
(3, 'Club House', 'lifestyle', false),
(4, 'Children\'s Play Area', 'lifestyle', false),
(5, 'Indoor Games', 'sports', false),
(6, 'Landscaped Gardens', 'natural', false),
(7, '24/7 Security', 'security', false),
(8, 'Tennis Court', 'sports', true),
(9, 'Yoga Deck', 'lifestyle', false),
(10, 'Multipurpose Hall', 'lifestyle', false);

SELECT * FROM amenities;

-- Projects
INSERT INTO projects (project_id, developer_id, locality_id, name, project_type, property_type, status,
                     total_land_area, total_units, min_price, max_price, price_per_sqft, currency,
                     launch_date, possession_date, description, is_active) VALUES
-- Lodha Haven
(1, 1, 1, 'Lodha Haven', 'residential', 'apartment', 'under_construction',
 5.5, 250, 15000000, 30000000, 8500, 'INR',
 '2023-01-15', '2026-12-31',
 'Lodha Haven offers premium 2, 3 & 4 BHK apartments with world-class amenities in Whitefield, Bangalore.',
 true),

-- East Park Residences
(2, 2, 2, 'East Park Residences', 'residential', 'apartment', 'under_construction',
 4.2, 180, 18000000, 35000000, 9200, 'INR',
 '2023-03-01', '2026-06-30',
 'East Park Residences presents luxurious 3 & 4 BHK apartments in Hennur, Bangalore with modern amenities.',
 true),

-- Brigade Insignia
(3, 3, 3, 'Brigade Insignia', 'residential', 'apartment', 'ready_to_move',
 3.8, 160, 25000000, 50000000, 12500, 'INR',
 '2020-06-01', '2024-03-31',
 'Brigade Insignia offers ultra-luxury 3 & 4 BHK apartments in the heart of Bangalore with premium amenities.',
 true);

SELECT * FROM projects;

-- Towers
INSERT INTO towers (tower_id, project_id, tower_name, total_floors, units_per_floor, total_units, construction_status) VALUES
-- Lodha Haven Towers
(1, 1, 'Haven A', 20, 4, 80, 'under_construction'),
(2, 1, 'Haven B', 20, 4, 80, 'under_construction'),
(3, 1, 'Haven C', 22, 4, 88, 'under_construction'),

-- East Park Residences Towers
(4, 2, 'East Wing', 15, 4, 60, 'under_construction'),
(5, 2, 'West Wing', 15, 4, 60, 'under_construction'),
(6, 2, 'Central Tower', 15, 4, 60, 'under_construction'),

-- Brigade Insignia Towers
(7, 3, 'Insignia Tower 1', 25, 2, 50, 'ready_to_move'),
(8, 3, 'Insignia Tower 2', 25, 2, 50, 'ready_to_move'),
(9, 3, 'Insignia Tower 3', 20, 3, 60, 'ready_to_move');

SELECT * FROM towers;

-- Unit Types
INSERT INTO unit_types (unit_type_id, project_id, type_name, bedrooms, bathrooms, carpet_area, built_up_area, super_area, base_price) VALUES
-- Lodha Haven Unit Types
(1, 1, '2 BHK Premium', 2, 2, 1050, 1250, 1450, 15000000),
(2, 1, '3 BHK Luxury', 3, 3, 1550, 1850, 2100, 22000000),
(3, 1, '4 BHK Ultra Luxury', 4, 4, 2200, 2600, 2900, 30000000),

-- East Park Residences Unit Types
(4, 2, '3 BHK Classic', 3, 3, 1650, 1950, 2200, 18000000),
(5, 2, '3 BHK Premium', 3, 3, 1800, 2100, 2400, 25000000),
(6, 2, '4 BHK Luxury', 4, 4, 2400, 2800, 3100, 35000000),

-- Brigade Insignia Unit Types
(7, 3, '3 BHK Ultra Luxury', 3, 3, 2100, 2400, 2700, 25000000),
(8, 3, '4 BHK Premium', 4, 4, 2800, 3200, 3600, 35000000),
(9, 3, '4 BHK Penthouse', 4, 5, 3500, 4000, 4500, 50000000);

SELECT * FROM unit_types;

-- Project Amenities
INSERT INTO project_amenities (project_id, amenity_id, is_available) VALUES
-- Lodha Haven Amenities
(1, 1, true), -- Swimming Pool
(1, 2, true), -- Gymnasium
(1, 3, true), -- Club House
(1, 4, true), -- Children's Play Area
(1, 6, true), -- Landscaped Gardens
(1, 7, true), -- 24/7 Security

-- East Park Residences Amenities
(2, 1, true), -- Swimming Pool
(2, 2, true), -- Gymnasium
(2, 3, true), -- Club House
(2, 4, true), -- Children's Play Area
(2, 5, true), -- Indoor Games
(2, 7, true), -- 24/7 Security
(2, 9, true), -- Yoga Deck

-- Brigade Insignia Amenities
(3, 1, true), -- Swimming Pool
(3, 2, true), -- Gymnasium
(3, 3, true), -- Club House
(3, 6, true), -- Landscaped Gardens
(3, 7, true), -- 24/7 Security
(3, 8, true), -- Tennis Court
(3, 10, true); -- Multipurpose Hall

SELECT * FROM project_amenities;

-- Sample Property Units
INSERT INTO property_units (unit_id, project_id, unit_type_id, tower_id, unit_number, floor_number, status, unit_price) VALUES
-- Lodha Haven Units
(1, 1, 1, 1, 'A-1201', 12, 'available', 15500000),
(2, 1, 2, 2, 'B-1502', 15, 'available', 22500000),
(3, 1, 3, 3, 'C-1801', 18, 'available', 31000000),

-- East Park Residences Units
(4, 2, 4, 4, 'EW-1001', 10, 'available', 18500000),
(5, 2, 5, 5, 'WW-1102', 11, 'available', 25500000),
(6, 2, 6, 6, 'CT-1401', 14, 'available', 35500000),

-- Brigade Insignia Units
(7, 3, 7, 7, 'T1-2001', 20, 'available', 26000000),
(8, 3, 8, 8, 'T2-2202', 22, 'available', 36000000),
(9, 3, 9, 9, 'T3-2001', 20, 'available', 51000000);

SELECT * FROM property_units;

-- Sample Project Media
INSERT INTO project_media (media_id, project_id, media_type, media_url, media_category, title) VALUES
(1, 1, 'image', 'https://example.com/lodha-haven-exterior.jpg', 'exterior', 'Lodha Haven Exterior View'),
(2, 1, 'image', 'https://example.com/lodha-haven-amenities.jpg', 'amenities', 'Lodha Haven Club House'),

(3, 2, 'image', 'https://example.com/east-park-exterior.jpg', 'exterior', 'East Park Residences Facade'),
(4, 2, 'image', 'https://example.com/east-park-amenities.jpg', 'amenities', 'East Park Swimming Pool'),

(5, 3, 'image', 'https://example.com/brigade-insignia-exterior.jpg', 'exterior', 'Brigade Insignia Tower View'),
(6, 3, 'image', 'https://example.com/brigade-insignia-amenities.jpg', 'amenities', 'Brigade Insignia Club House');

SELECT * FROM project_media;