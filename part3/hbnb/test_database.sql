-- Test CRUD operations to verify database schema functionality

-- Test 1: Verify tables exist and have correct structure
SHOW TABLES;

-- Test 2: Verify initial data was inserted correctly
SELECT * FROM users WHERE email = 'admin@hbnb.io';
SELECT * FROM amenities;

-- Test 3: Test INSERT operations
-- Insert a test user
INSERT INTO users (id, email, first_name, last_name, password, is_admin) VALUES
('test-user-id-1234', 'test@example.com', 'Test', 'User', 'hashed_password', FALSE);

-- Insert a test place
INSERT INTO places (id, title, description, price, latitude, longitude, owner_id) VALUES
('test-place-id-1234', 'Test Place', 'A nice test place', 100.50, 37.7749, -122.4194, 'test-user-id-1234');

-- Insert a test review
INSERT INTO reviews (id, text, rating, user_id, place_id) VALUES
('test-review-id-1234', 'Great place!', 5, '36c9050e-ddd3-4c3b-9731-9f487208bbc1', 'test-place-id-1234');

-- Insert place-amenity relationship
INSERT INTO place_amenity (place_id, amenity_id) VALUES
('test-place-id-1234', 'a1b2c3d4-e5f6-7890-1234-567890abcdef');

-- Test 4: Test SELECT operations with relationships
SELECT
    p.title as place_title,
    u.first_name as owner_first_name,
    u.last_name as owner_last_name
FROM places p
JOIN users u ON p.owner_id = u.id;

-- Test 5: Test SELECT with reviews
SELECT
    r.text as review_text,
    r.rating,
    u.first_name as reviewer_name,
    p.title as place_title
FROM reviews r
JOIN users u ON r.user_id = u.id
JOIN places p ON r.place_id = p.id;

-- Test 6: Test many-to-many relationship
SELECT
    p.title as place_title,
    a.name as amenity_name
FROM places p
JOIN place_amenity pa ON p.id = pa.place_id
JOIN amenities a ON pa.amenity_id = a.id;

-- Test 7: Test UPDATE operation
UPDATE users SET first_name = 'Updated Test' WHERE id = 'test-user-id-1234';

-- Test 8: Test DELETE operations (cleanup)
DELETE FROM place_amenity WHERE place_id = 'test-place-id-1234';
DELETE FROM reviews WHERE id = 'test-review-id-1234';
DELETE FROM places WHERE id = 'test-place-id-1234';
DELETE FROM users WHERE id = 'test-user-id-1234';

-- Verify cleanup
SELECT COUNT(*) as remaining_test_users FROM users WHERE email = 'test@example.com';