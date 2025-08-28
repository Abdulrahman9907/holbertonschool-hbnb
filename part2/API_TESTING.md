# HBnB API Testing Guide

This document provides instructions for testing the HBnB API endpoints implemented in Tasks 4-6.

## Prerequisites

1. Make sure the Flask application is running:
   ```bash
   cd part2/hbnb
   python run.py
   ```
   The server should start on `http://localhost:5000`

2. Install required testing dependencies:
   ```bash
   pip install requests
   ```

## Testing Methods

### 1. Automated API Testing Script

Run the comprehensive API test script:

```bash
cd part2
python test_api.py
```

This script tests:
- All User endpoints (POST, GET, PUT)
- All Amenity endpoints (POST, GET, PUT)
- All Place endpoints (POST, GET, PUT)
- All Review endpoints (POST, GET, PUT, DELETE)
- Validation and error handling
- Relationship integrity

### 2. Unit Tests

Run the model unit tests:

```bash
cd part2
python test_models.py
```

This tests:
- Model validation
- Attribute constraints
- Relationship handling
- Repository integration

### 3. Manual Testing with cURL

#### User Endpoints

**Create User:**
```bash
curl -X POST http://localhost:5000/api/v1/users/ \
  -H "Content-Type: application/json" \
  -d '{"first_name": "John", "last_name": "Doe", "email": "john@example.com"}'
```

**Get All Users:**
```bash
curl http://localhost:5000/api/v1/users/
```

**Get User by ID:**
```bash
curl http://localhost:5000/api/v1/users/{user_id}
```

**Update User:**
```bash
curl -X PUT http://localhost:5000/api/v1/users/{user_id} \
  -H "Content-Type: application/json" \
  -d '{"first_name": "Jane", "last_name": "Doe", "email": "jane@example.com"}'
```

#### Amenity Endpoints

**Create Amenity:**
```bash
curl -X POST http://localhost:5000/api/v1/amenities/ \
  -H "Content-Type: application/json" \
  -d '{"name": "WiFi"}'
```

**Get All Amenities:**
```bash
curl http://localhost:5000/api/v1/amenities/
```

**Get Amenity by ID:**
```bash
curl http://localhost:5000/api/v1/amenities/{amenity_id}
```

**Update Amenity:**
```bash
curl -X PUT http://localhost:5000/api/v1/amenities/{amenity_id} \
  -H "Content-Type: application/json" \
  -d '{"name": "Free WiFi"}'
```

#### Place Endpoints

**Create Place:**
```bash
curl -X POST http://localhost:5000/api/v1/places/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Cozy Apartment",
    "description": "A nice place to stay",
    "price": 100.0,
    "latitude": 37.7749,
    "longitude": -122.4194,
    "owner_id": "{user_id}",
    "amenities": ["{amenity_id}"]
  }'
```

**Get All Places:**
```bash
curl http://localhost:5000/api/v1/places/
```

**Get Place by ID:**
```bash
curl http://localhost:5000/api/v1/places/{place_id}
```

**Update Place:**
```bash
curl -X PUT http://localhost:5000/api/v1/places/{place_id} \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Updated Cozy Apartment",
    "description": "An even nicer place to stay",
    "price": 120.0,
    "latitude": 37.7749,
    "longitude": -122.4194,
    "owner_id": "{user_id}"
  }'
```

#### Review Endpoints

**Create Review:**
```bash
curl -X POST http://localhost:5000/api/v1/reviews/ \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Great place to stay!",
    "rating": 5,
    "user_id": "{user_id}",
    "place_id": "{place_id}"
  }'
```

**Get All Reviews:**
```bash
curl http://localhost:5000/api/v1/reviews/
```

**Get Review by ID:**
```bash
curl http://localhost:5000/api/v1/reviews/{review_id}
```

**Get Reviews for a Place:**
```bash
curl http://localhost:5000/api/v1/reviews/places/{place_id}
```

**Update Review:**
```bash
curl -X PUT http://localhost:5000/api/v1/reviews/{review_id} \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Excellent place to stay!",
    "rating": 5,
    "user_id": "{user_id}",
    "place_id": "{place_id}"
  }'
```

**Delete Review:**
```bash
curl -X DELETE http://localhost:5000/api/v1/reviews/{review_id}
```

### 4. Swagger Documentation

Access the interactive API documentation at:
```
http://localhost:5000/api/v1/
```

This provides:
- Complete API specification
- Interactive testing interface
- Request/response examples
- Model schemas

## Validation Rules

### User Validation
- `first_name`: Required, max 50 characters
- `last_name`: Required, max 50 characters  
- `email`: Required, valid email format, unique
- `is_admin`: Boolean, defaults to False

### Place Validation
- `title`: Required, max 100 characters
- `description`: Optional string
- `price`: Required, positive float
- `latitude`: Required, float between -90 and 90
- `longitude`: Required, float between -180 and 180
- `owner_id`: Required, must reference existing user
- `amenities`: Optional list of amenity IDs

### Review Validation
- `text`: Required, non-empty string
- `rating`: Required, integer between 1 and 5
- `user_id`: Required, must reference existing user
- `place_id`: Required, must reference existing place

### Amenity Validation
- `name`: Required, non-empty string, max 50 characters

## Expected Response Formats

### Success Responses
- 200: Resource retrieved successfully
- 201: Resource created successfully

### Error Responses
- 400: Invalid input data or validation error
- 404: Resource not found
- 500: Server error

## Testing Checklist

- [ ] All endpoints return correct status codes
- [ ] Data validation works properly
- [ ] Relationships are maintained correctly
- [ ] Error handling provides meaningful messages
- [ ] Extended attributes are returned (owner details, amenities, etc.)
- [ ] DELETE functionality works only for reviews
- [ ] API documentation is accessible and accurate