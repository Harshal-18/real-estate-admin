-- Drop the existing towers table if it exists
DROP TABLE IF EXISTS towers;

-- Create the towers table with exact schema
CREATE TABLE towers (
    tower_id INT AUTO_INCREMENT PRIMARY KEY,
    project_id INT NOT NULL,
    tower_name VARCHAR(100) NOT NULL,
    tower_number VARCHAR(50),
    total_floors INT NOT NULL,
    units_per_floor INT DEFAULT 0,
    total_units INT DEFAULT 0,
    tower_type VARCHAR(20) DEFAULT 'residential',
    construction_status VARCHAR(30) DEFAULT 'under_construction',
    possession_date DATE,
    height_meters DECIMAL(8,2),
    elevator_count INT DEFAULT 0,
    has_power_backup TINYINT(1) DEFAULT 1,
    has_water_backup TINYINT(1) DEFAULT 1,
    has_fire_safety TINYINT(1) DEFAULT 1,
    latitude DECIMAL(10,8),
    longitude DECIMAL(11,8),
    facing_direction VARCHAR(20),
    is_active TINYINT(1) DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES projects(project_id)
); 