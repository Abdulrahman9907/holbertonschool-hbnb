-- Insert initial data for HBnB Database
-- Creates an administrator user and initial amenities

-- Insert Administrator User
-- Note: The password hash below is for 'admin1234' generated using bcrypt
-- In a real deployment, you should generate a new hash for security
INSERT INTO users (id, email, first_name, last_name, password, is_admin, created_at, updated_at) VALUES
(
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
    'admin@hbnb.io',
    'Admin',
    'HBnB',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LeVMpYtA8XDbIeYqe',
    TRUE,
    NOW(),
    NOW()
);

-- Insert Initial Amenities
INSERT INTO amenities (id, name, created_at, updated_at) VALUES
(
    'a1b2c3d4-e5f6-7890-1234-567890abcdef',
    'WiFi',
    NOW(),
    NOW()
),
(
    'b2c3d4e5-f6g7-8901-2345-678901bcdefg',
    'Swimming Pool',
    NOW(),
    NOW()
),
(
    'c3d4e5f6-g7h8-9012-3456-789012cdefgh',
    'Air Conditioning',
    NOW(),
    NOW()
);