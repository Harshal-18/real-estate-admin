drop database real_estate_db;

use real_estate_db;

select * from reviews;
select * from projects;
select * from property_units;

ALTER TABLE towers ADD COLUMN created_at DATETIME DEFAULT CURRENT_TIMESTAMP;
ALTER TABLE property_units ADD COLUMN block_number VARCHAR(50);
ALTER TABLE property_units ADD COLUMN booking_status VARCHAR(50);
ALTER TABLE search_logs ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;


ALTER TABLE cities ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;

ALTER TABLE property_units 
#ADD COLUMN block_number VARCHAR(50),
#ADD COLUMN booking_status VARCHAR(50),
ADD COLUMN possession_status VARCHAR(50),
ADD COLUMN base_price DECIMAL(15,2),
ADD COLUMN premium_charges DECIMAL(15,2),
ADD COLUMN other_charges DECIMAL(15,2),
ADD COLUMN total_price DECIMAL(15,2),
ADD COLUMN facing_direction VARCHAR(50),
ADD COLUMN view_type VARCHAR(50),
ADD COLUMN corner_unit BOOLEAN DEFAULT FALSE,
ADD COLUMN has_private_terrace BOOLEAN DEFAULT FALSE,
ADD COLUMN has_private_garden BOOLEAN DEFAULT FALSE,
ADD COLUMN is_modified BOOLEAN DEFAULT FALSE,
ADD COLUMN modifications TEXT;