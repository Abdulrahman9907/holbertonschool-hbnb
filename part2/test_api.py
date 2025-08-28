#!/usr/bin/env python3
"""
Basic API Testing Script for HBnB Application
Tests all endpoints and validates functionality
"""
import requests
import json
import sys

BASE_URL = "http://localhost:5000/api/v1"

def test_users():
    """Test User endpoints"""
    print("Testing User Endpoints...")
    
    # Test POST /users - Create user
    user_data = {
        "first_name": "John",
        "last_name": "Doe", 
        "email": "john@example.com"
    }
    
    response = requests.post(f"{BASE_URL}/users/", json=user_data)
    print(f"POST /users/: {response.status_code} - {response.json()}")
    
    if response.status_code == 201:
        user_id = response.json()['id']
        
        # Test GET /users/{id} - Get user by ID
        response = requests.get(f"{BASE_URL}/users/{user_id}")
        print(f"GET /users/{user_id}: {response.status_code} - {response.json()}")
        
        # Test GET /users/ - Get all users
        response = requests.get(f"{BASE_URL}/users/")
        print(f"GET /users/: {response.status_code} - Found {len(response.json())} users")
        
        # Test PUT /users/{id} - Update user
        update_data = {
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane@example.com"
        }
        response = requests.put(f"{BASE_URL}/users/{user_id}", json=update_data)
        print(f"PUT /users/{user_id}: {response.status_code} - {response.json()}")
        
        return user_id
    
    return None

def test_amenities():
    """Test Amenity endpoints"""
    print("\nTesting Amenity Endpoints...")
    
    # Test POST /amenities - Create amenity
    amenity_data = {"name": "WiFi"}
    
    response = requests.post(f"{BASE_URL}/amenities/", json=amenity_data)
    print(f"POST /amenities/: {response.status_code} - {response.json()}")
    
    if response.status_code == 201:
        amenity_id = response.json()['id']
        
        # Test GET /amenities/{id} - Get amenity by ID
        response = requests.get(f"{BASE_URL}/amenities/{amenity_id}")
        print(f"GET /amenities/{amenity_id}: {response.status_code} - {response.json()}")
        
        # Test GET /amenities/ - Get all amenities
        response = requests.get(f"{BASE_URL}/amenities/")
        print(f"GET /amenities/: {response.status_code} - Found {len(response.json())} amenities")
        
        # Test PUT /amenities/{id} - Update amenity
        update_data = {"name": "Free WiFi"}
        response = requests.put(f"{BASE_URL}/amenities/{amenity_id}", json=update_data)
        print(f"PUT /amenities/{amenity_id}: {response.status_code} - {response.json()}")
        
        return amenity_id
    
    return None

def test_places(user_id, amenity_id):
    """Test Place endpoints"""
    print("\nTesting Place Endpoints...")
    
    if not user_id:
        print("Cannot test places without valid user_id")
        return None
    
    # Test POST /places - Create place
    place_data = {
        "title": "Cozy Apartment",
        "description": "A nice place to stay",
        "price": 100.0,
        "latitude": 37.7749,
        "longitude": -122.4194,
        "owner_id": user_id,
        "amenities": [amenity_id] if amenity_id else []
    }
    
    response = requests.post(f"{BASE_URL}/places/", json=place_data)
    print(f"POST /places/: {response.status_code} - {response.json()}")
    
    if response.status_code == 201:
        place_id = response.json()['id']
        
        # Test GET /places/{id} - Get place by ID
        response = requests.get(f"{BASE_URL}/places/{place_id}")
        print(f"GET /places/{place_id}: {response.status_code} - {response.json()}")
        
        # Test GET /places/ - Get all places
        response = requests.get(f"{BASE_URL}/places/")
        print(f"GET /places/: {response.status_code} - Found {len(response.json())} places")
        
        # Test PUT /places/{id} - Update place
        update_data = {
            "title": "Updated Cozy Apartment",
            "description": "An even nicer place to stay",
            "price": 120.0,
            "latitude": 37.7749,
            "longitude": -122.4194,
            "owner_id": user_id
        }
        response = requests.put(f"{BASE_URL}/places/{place_id}", json=update_data)
        print(f"PUT /places/{place_id}: {response.status_code} - {response.json()}")
        
        return place_id
    
    return None

def test_reviews(user_id, place_id):
    """Test Review endpoints"""
    print("\nTesting Review Endpoints...")
    
    if not user_id or not place_id:
        print("Cannot test reviews without valid user_id and place_id")
        return None
    
    # Test POST /reviews - Create review
    review_data = {
        "text": "Great place to stay!",
        "rating": 5,
        "user_id": user_id,
        "place_id": place_id
    }
    
    response = requests.post(f"{BASE_URL}/reviews/", json=review_data)
    print(f"POST /reviews/: {response.status_code} - {response.json()}")
    
    if response.status_code == 201:
        review_id = response.json()['id']
        
        # Test GET /reviews/{id} - Get review by ID
        response = requests.get(f"{BASE_URL}/reviews/{review_id}")
        print(f"GET /reviews/{review_id}: {response.status_code} - {response.json()}")
        
        # Test GET /reviews/ - Get all reviews
        response = requests.get(f"{BASE_URL}/reviews/")
        print(f"GET /reviews/: {response.status_code} - Found {len(response.json())} reviews")
        
        # Test GET /reviews/places/{place_id} - Get reviews for place
        response = requests.get(f"{BASE_URL}/reviews/places/{place_id}")
        print(f"GET /reviews/places/{place_id}: {response.status_code} - Found {len(response.json())} reviews for place")
        
        # Test PUT /reviews/{id} - Update review
        update_data = {
            "text": "Updated: Excellent place to stay!",
            "rating": 5,
            "user_id": user_id,
            "place_id": place_id
        }
        response = requests.put(f"{BASE_URL}/reviews/{review_id}", json=update_data)
        print(f"PUT /reviews/{review_id}: {response.status_code} - {response.json()}")
        
        # Test DELETE /reviews/{id} - Delete review
        response = requests.delete(f"{BASE_URL}/reviews/{review_id}")
        print(f"DELETE /reviews/{review_id}: {response.status_code} - {response.json()}")
        
        return review_id
    
    return None

def test_validation():
    """Test validation and error cases"""
    print("\nTesting Validation and Error Cases...")
    
    # Test invalid user data
    invalid_user = {"first_name": "", "email": "invalid-email"}
    response = requests.post(f"{BASE_URL}/users/", json=invalid_user)
    print(f"Invalid user data: {response.status_code} - {response.json()}")
    
    # Test invalid place data
    invalid_place = {
        "title": "",
        "price": -100,
        "latitude": 200,  # Invalid latitude
        "longitude": -200,  # Invalid longitude
        "owner_id": "nonexistent"
    }
    response = requests.post(f"{BASE_URL}/places/", json=invalid_place)
    print(f"Invalid place data: {response.status_code} - {response.json()}")
    
    # Test invalid review data
    invalid_review = {
        "text": "",
        "rating": 10,  # Invalid rating
        "user_id": "nonexistent",
        "place_id": "nonexistent"
    }
    response = requests.post(f"{BASE_URL}/reviews/", json=invalid_review)
    print(f"Invalid review data: {response.status_code} - {response.json()}")
    
    # Test 404 cases
    response = requests.get(f"{BASE_URL}/users/nonexistent")
    print(f"GET nonexistent user: {response.status_code} - {response.json()}")
    
    response = requests.get(f"{BASE_URL}/places/nonexistent")
    print(f"GET nonexistent place: {response.status_code} - {response.json()}")
    
    response = requests.get(f"{BASE_URL}/reviews/nonexistent")
    print(f"GET nonexistent review: {response.status_code} - {response.json()}")

def main():
    """Main testing function"""
    print("Starting HBnB API Tests...")
    print("=" * 50)
    
    try:
        # Test all endpoints
        user_id = test_users()
        amenity_id = test_amenities()
        place_id = test_places(user_id, amenity_id)
        review_id = test_reviews(user_id, place_id)
        test_validation()
        
        print("\n" + "=" * 50)
        print("API Testing Complete!")
        
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the API server.")
        print("Make sure the Flask application is running on http://localhost:5000")
        sys.exit(1)
    except Exception as e:
        print(f"Error during testing: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()