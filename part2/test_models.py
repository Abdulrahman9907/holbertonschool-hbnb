#!/usr/bin/env python3
"""
Unit tests for HBnB Application Models
Tests validation, relationships, and core functionality
"""
import unittest
import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'hbnb'))

from app.models import User, Place, Review, Amenity

class TestUser(unittest.TestCase):
    """Test cases for User model"""
    
    def test_valid_user_creation(self):
        """Test creating a valid user"""
        user = User("John", "Doe", "john@example.com")
        self.assertEqual(user.first_name, "John")
        self.assertEqual(user.last_name, "Doe")
        self.assertEqual(user.email, "john@example.com")
        self.assertFalse(user.is_admin)
        self.assertIsNotNone(user.id)
        self.assertIsNotNone(user.created_at)
        self.assertIsNotNone(user.updated_at)
    
    def test_user_admin_flag(self):
        """Test user with admin flag"""
        admin = User("Admin", "User", "admin@example.com", is_admin=True)
        self.assertTrue(admin.is_admin)
    
    def test_invalid_email(self):
        """Test user creation with invalid email"""
        with self.assertRaises(ValueError):
            User("John", "Doe", "invalid-email")
    
    def test_empty_name(self):
        """Test user creation with empty name"""
        with self.assertRaises(ValueError):
            User("", "Doe", "john@example.com")
        with self.assertRaises(ValueError):
            User("John", "", "john@example.com")
    
    def test_name_too_long(self):
        """Test user creation with name too long"""
        long_name = "a" * 51
        with self.assertRaises(ValueError):
            User(long_name, "Doe", "john@example.com")
        with self.assertRaises(ValueError):
            User("John", long_name, "john@example.com")
    
    def test_user_update(self):
        """Test updating user information"""
        user = User("John", "Doe", "john@example.com")
        original_updated_at = user.updated_at
        
        user.update({"first_name": "Jane"})
        self.assertEqual(user.first_name, "Jane")
        self.assertNotEqual(user.updated_at, original_updated_at)

class TestAmenity(unittest.TestCase):
    """Test cases for Amenity model"""
    
    def test_valid_amenity_creation(self):
        """Test creating a valid amenity"""
        amenity = Amenity("WiFi")
        self.assertEqual(amenity.name, "WiFi")
        self.assertIsNotNone(amenity.id)
        self.assertIsNotNone(amenity.created_at)
        self.assertIsNotNone(amenity.updated_at)
    
    def test_empty_name(self):
        """Test amenity creation with empty name"""
        with self.assertRaises(ValueError):
            Amenity("")
    
    def test_name_too_long(self):
        """Test amenity creation with name too long"""
        long_name = "a" * 51
        with self.assertRaises(ValueError):
            Amenity(long_name)

class TestPlace(unittest.TestCase):
    """Test cases for Place model"""
    
    def setUp(self):
        """Set up test fixtures"""
        # Clear the email registry for clean tests
        User._emails_registry.clear()
        self.user = User("John", "Doe", "john@example.com")
        self.amenity = Amenity("WiFi")
    
    def test_valid_place_creation(self):
        """Test creating a valid place"""
        place = Place("Cozy Apartment", "A nice place", 100.0, 37.7749, -122.4194, self.user)
        self.assertEqual(place.title, "Cozy Apartment")
        self.assertEqual(place.description, "A nice place")
        self.assertEqual(place.price, 100.0)
        self.assertEqual(place.latitude, 37.7749)
        self.assertEqual(place.longitude, -122.4194)
        self.assertEqual(place.owner, self.user)
        self.assertEqual(len(place.amenities), 0)
        self.assertEqual(len(place.reviews), 0)
    
    def test_invalid_price(self):
        """Test place creation with invalid price"""
        with self.assertRaises(ValueError):
            Place("Title", "Desc", -100.0, 37.7749, -122.4194, self.user)
        with self.assertRaises(ValueError):
            Place("Title", "Desc", 0, 37.7749, -122.4194, self.user)
    
    def test_invalid_coordinates(self):
        """Test place creation with invalid coordinates"""
        # Invalid latitude
        with self.assertRaises(ValueError):
            Place("Title", "Desc", 100.0, 91.0, -122.4194, self.user)
        with self.assertRaises(ValueError):
            Place("Title", "Desc", 100.0, -91.0, -122.4194, self.user)
        
        # Invalid longitude
        with self.assertRaises(ValueError):
            Place("Title", "Desc", 100.0, 37.7749, 181.0, self.user)
        with self.assertRaises(ValueError):
            Place("Title", "Desc", 100.0, 37.7749, -181.0, self.user)
    
    def test_empty_title(self):
        """Test place creation with empty title"""
        with self.assertRaises(ValueError):
            Place("", "Description", 100.0, 37.7749, -122.4194, self.user)
    
    def test_title_too_long(self):
        """Test place creation with title too long"""
        long_title = "a" * 101
        with self.assertRaises(ValueError):
            Place(long_title, "Description", 100.0, 37.7749, -122.4194, self.user)
    
    def test_add_amenity(self):
        """Test adding amenity to place"""
        place = Place("Title", "Desc", 100.0, 37.7749, -122.4194, self.user)
        place.add_amenity(self.amenity)
        self.assertIn(self.amenity, place.amenities)
    
    def test_invalid_owner(self):
        """Test place creation with invalid owner"""
        with self.assertRaises(TypeError):
            Place("Title", "Desc", 100.0, 37.7749, -122.4194, "not a user")

class TestReview(unittest.TestCase):
    """Test cases for Review model"""
    
    def setUp(self):
        """Set up test fixtures"""
        # Clear the email registry for clean tests
        User._emails_registry.clear()
        self.user = User("John", "Doe", "john@example.com")
        self.place = Place("Cozy Apartment", "A nice place", 100.0, 37.7749, -122.4194, self.user)
    
    def test_valid_review_creation(self):
        """Test creating a valid review"""
        review = Review("Great place!", 5, self.place, self.user)
        self.assertEqual(review.text, "Great place!")
        self.assertEqual(review.rating, 5)
        self.assertEqual(review.place, self.place)
        self.assertEqual(review.user, self.user)
    
    def test_invalid_rating(self):
        """Test review creation with invalid rating"""
        with self.assertRaises(ValueError):
            Review("Text", 0, self.place, self.user)
        with self.assertRaises(ValueError):
            Review("Text", 6, self.place, self.user)
        with self.assertRaises(ValueError):
            Review("Text", -1, self.place, self.user)
    
    def test_empty_text(self):
        """Test review creation with empty text"""
        with self.assertRaises(ValueError):
            Review("", 5, self.place, self.user)
    
    def test_invalid_place(self):
        """Test review creation with invalid place"""
        with self.assertRaises(TypeError):
            Review("Text", 5, "not a place", self.user)
    
    def test_invalid_user(self):
        """Test review creation with invalid user"""
        with self.assertRaises(TypeError):
            Review("Text", 5, self.place, "not a user")

class TestRepositoryIntegration(unittest.TestCase):
    """Test model integration with repository pattern"""
    
    def setUp(self):
        """Set up test fixtures"""
        # Clear the email registry for clean tests
        User._emails_registry.clear()
        from app.persistence.repository import InMemoryRepository
        self.repo = InMemoryRepository()
    
    def test_user_repository_operations(self):
        """Test user CRUD operations with repository"""
        user = User("John", "Doe", "john@example.com")
        
        # Test add
        self.repo.add(user)
        retrieved = self.repo.get(user.id)
        self.assertEqual(retrieved, user)
        
        # Test get_all
        users = self.repo.get_all()
        self.assertEqual(len(users), 1)
        self.assertIn(user, users)
        
        # Test get_by_attribute
        found = self.repo.get_by_attribute('email', 'john@example.com')
        self.assertEqual(found, user)
        
        # Test update
        self.repo.update(user.id, {"first_name": "Jane"})
        self.assertEqual(user.first_name, "Jane")
        
        # Test delete
        self.repo.delete(user.id)
        self.assertIsNone(self.repo.get(user.id))

def run_tests():
    """Run all tests"""
    unittest.main(argv=[''], exit=False, verbosity=2)

if __name__ == "__main__":
    print("Running HBnB Model Tests...")
    print("=" * 50)
    run_tests()
    print("=" * 50)
    print("Model Testing Complete!")