# HBnB Application - Part 2: Business Logic and API

A modern REST API application built with Flask and Flask-RESTx, implementing a vacation rental platform similar to Airbnb. This project demonstrates clean architecture with proper separation of concerns, implementing the Business Logic layer and API endpoints.

## Architecture

The application follows a layered architecture:

- **Presentation Layer**: REST API endpoints with Flask-RESTx
- **Business Logic Layer**: Core application logic and validation
- **Persistence Layer**: In-memory data storage (with interface for future database integration)

### Project Structure

```
part2/
├── hbnb/                 # Main application package  
│   ├── app/
│   │   ├── __init__.py   # Flask app factory
│   │   ├── api/          # API endpoints
│   │   │   └── v1/       # API version 1
│   │   │       ├── users.py      # User endpoints
│   │   │       ├── places.py     # Place endpoints
│   │   │       ├── reviews.py    # Review endpoints
│   │   │       └── amenities.py  # Amenity endpoints
│   │   ├── models/       # Business logic models
│   │   │   ├── user.py      # User model with validation
│   │   │   ├── place.py     # Place model with geolocation
│   │   │   ├── review.py    # Review model with ratings
│   │   │   └── amenity.py   # Amenity model
│   │   ├── services/     # Business logic services
│   │   │   └── facade.py    # Facade pattern implementation
│   │   └── persistence/  # Data persistence layer
│   │       └── repository.py  # Repository pattern with in-memory storage
├── config.py             # Application configuration
├── run.py                # Application entry point
├── requirements.txt      # Python dependencies
├── test_models.py        # Unit tests for models
├── test_api.py          # API integration tests
└── API_TESTING.md       # API testing guide
```

## Quick Start

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone and navigate to the project:**
   ```bash
   cd part2
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Start the application:**
   ```bash
   python run.py
   ```

The server will start on `http://localhost:5000`

### API Documentation

Once the server is running, access the interactive API documentation at:
- **Swagger UI**: http://localhost:5000/api/v1/

This provides:
- Complete API specification
- Interactive testing interface  
- Request/response examples
- Model schemas

## API Endpoints

### Users
- `POST /api/v1/users/` - Create a new user
- `GET /api/v1/users/` - Get all users  
- `GET /api/v1/users/{id}` - Get user by ID
- `PUT /api/v1/users/{id}` - Update user

### Places
- `POST /api/v1/places/` - Create a new place
- `GET /api/v1/places/` - Get all places
- `GET /api/v1/places/{id}` - Get place by ID  
- `PUT /api/v1/places/{id}` - Update place

### Reviews
- `POST /api/v1/reviews/` - Create a new review
- `GET /api/v1/reviews/` - Get all reviews
- `GET /api/v1/reviews/{id}` - Get review by ID
- `PUT /api/v1/reviews/{id}` - Update review
- `DELETE /api/v1/reviews/{id}` - Delete review
- `GET /api/v1/reviews/places/{place_id}` - Get reviews for a place

### Amenities
- `POST /api/v1/amenities/` - Create a new amenity
- `GET /api/v1/amenities/` - Get all amenities
- `GET /api/v1/amenities/{id}` - Get amenity by ID
- `PUT /api/v1/amenities/{id}` - Update amenity

## Testing

### Run Unit Tests
```bash
python test_models.py
```

### Run API Integration Tests  
```bash
python test_api.py
```

### Manual Testing
See [API_TESTING.md](API_TESTING.md) for detailed cURL examples and testing procedures.

## Key Features

### Validation & Error Handling
- Comprehensive input validation
- Proper HTTP status codes
- Meaningful error messages
- Email format validation
- Coordinate range validation
- Rating range validation (1-5)

### Relationships
- Users can own multiple places
- Places can have multiple amenities
- Places can have multiple reviews
- Users can create multiple reviews
- Proper relationship integrity maintained

### Business Logic
- Email uniqueness enforcement
- Geographic coordinate validation  
- Price validation (positive values)
- Rating validation (1-5 scale)
- Proper entity relationship management

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

### Review Validation
- `text`: Required, non-empty string
- `rating`: Required, integer between 1 and 5  
- `user_id`: Required, must reference existing user
- `place_id`: Required, must reference existing place

### Amenity Validation
- `name`: Required, non-empty string, max 50 characters

## Configuration

The application supports different configurations:
- **Development**: Debug mode enabled
- **Production**: Optimized for deployment
- **Testing**: Configured for automated testing

Set the environment:
```bash
export FLASK_ENV=development  # or production
```

## Response Formats

### Success Responses
- `200 OK`: Resource retrieved successfully
- `201 Created`: Resource created successfully

### Error Responses  
- `400 Bad Request`: Invalid input data or validation error
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server error

## Contributing

1. Follow the existing code style and patterns
2. Add tests for new features
3. Update documentation as needed  
4. Ensure all validation rules are properly implemented

## Development Notes

This implementation focuses on:
- Clean, maintainable code structure
- Proper separation of concerns
- Comprehensive error handling
- Thorough testing coverage  
- Clear documentation and examples

The application is designed to be extended with a real database in Part 3, while maintaining the same business logic and API interface.