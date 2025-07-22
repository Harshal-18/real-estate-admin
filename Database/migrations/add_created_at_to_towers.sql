-- Add created_at column to towers table
ALTER TABLE towers
ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;

-- Update existing rows with current timestamp
UPDATE towers SET created_at = CURRENT_TIMESTAMP WHERE created_at IS NULL; 