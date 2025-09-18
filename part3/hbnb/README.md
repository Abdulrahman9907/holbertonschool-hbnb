# HBnB Part 3 - Authentication & Database Integration

## Project Completion Summary

All tasks for HBnB Part 3 have been successfully implemented and tested. This project extends the HBnB application with authentication, authorization, and database persistence.

## Completed Tasks

### Task 0: Application Factory Configuration
- **Status**: Complete
- **Implementation**: Flask application factory pattern with configuration support
- **Location**: `app/__init__.py`, `config.py`

### Task 1: User Model with Password Hashing
- **Status**: Complete
- **Implementation**: bcrypt password hashing, secure user model
- **Location**: `app/models/user.py`

### Task 2: JWT Authentication
- **Status**: Complete
- **Implementation**: Flask-JWT-Extended integration with login endpoint
- **Location**: `app/api/v1/auth.py`

### Task 3: Authenticated User Access Endpoints
- **Status**: Complete
- **Implementation**: JWT-protected endpoints with ownership validation
- **Features**:
  - Users can create/update their own places
  - Users can create reviews for places they don't own
  - Users can update their own user details (excluding email/password)
  - Prevention of self-reviews and duplicate reviews

### Task 4: Administrator Access Endpoints
- **Status**: Complete
- **Implementation**: Role-based access control for admin users
- **Features**:
  - Admins can create new users
  - Admins can modify any user's data (including email/password)
  - Admins can bypass ownership restrictions
  - Admins can manage amenities

### Task 5: SQLAlchemy Repository
- **Status**: Complete
- **Implementation**: Database persistence layer using SQLAlchemy
- **Location**: `app/persistence/repository.py`

### Task 6: User Entity Mapping
- **Status**: Complete
- **Implementation**: User model mapped to SQLAlchemy with relationships
- **Location**: `app/models/user.py`

### Task 7: Place, Review, and Amenity Entity Mapping
- **Status**: Complete
- **Implementation**: All entities mapped to SQLAlchemy models
- **Location**: `app/models/place.py`, `app/models/review.py`, `app/models/amenity.py`

### Task 8: Entity Relationships Mapping
- **Status**: Complete
- **Implementation**: Complete relationship mapping
- **Relationships**:
  - User → Places (one-to-many)
  - User → Reviews (one-to-many)
  - Place → Reviews (one-to-many)
  - Place ↔ Amenities (many-to-many)

### Task 9: SQL Scripts for Table Generation
- **Status**: Complete
- **Files Created**:
  - `create_tables.sql`: Database schema creation
  - `insert_initial_data.sql`: Admin user and initial amenities
  - `test_database.sql`: CRUD operation tests

### Task 10: Database Diagrams
- **Status**: Complete
- **Implementation**: Mermaid.js ER diagram
- **Location**: `database_diagram.md`

## Project Structure

```
part3/hbnb/
├── app/
│   ├── __init__.py              # Application factory with JWT & bcrypt setup
│   ├── models/
│   │   ├── __init__.py          # Base model and association tables
│   │   ├── user.py              # User model with password hashing
│   │   ├── place.py             # Place model with relationships
│   │   ├── review.py            # Review model with constraints
│   │   └── amenity.py           # Amenity model
│   ├── persistence/
│   │   ├── repository.py        # SQLAlchemy repository implementation
│   │   ├── user_repository.py   # User-specific repository
│   │   ├── place_repository.py  # Place-specific repository
│   │   ├── review_repository.py # Review-specific repository
│   │   └── amenity_repository.py # Amenity-specific repository
│   ├── services/
│   │   └── facade.py            # Business logic facade
│   └── api/v1/
│       ├── auth.py              # Authentication endpoints
│       ├── users.py             # User management endpoints
│       ├── places.py            # Place management endpoints
│       ├── reviews.py           # Review management endpoints
│       └── amenities.py         # Amenity management endpoints
├── config.py                    # Application configuration
├── database.py                  # SQLAlchemy database instance
├── run.py                       # Application entry point
├── requirements.txt             # Python dependencies
├── create_tables.sql            # Database schema SQL
├── insert_initial_data.sql      # Initial data SQL
├── test_database.sql            # Database testing SQL
├── database_diagram.md          # ER diagram documentation
├── test_api.sh                  # API testing script
└── README.md                    # This file
```

## Getting Started

### Installation

1. Create and activate virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Initialize database:
```bash
python3 -c "
from app import create_app
from database import db
from app.models import User, Amenity

app = create_app()
with app.app_context():
    db.create_all()

    # Create admin user
    admin = User(
        id='36c9050e-ddd3-4c3b-9731-9f487208bbc1',
        first_name='Admin',
        last_name='HBnB',
        email='admin@hbnb.io',
        password='admin1234',
        is_admin=True
    )

    # Create initial amenities
    wifi = Amenity(name='WiFi')
    pool = Amenity(name='Swimming Pool')
    ac = Amenity(name='Air Conditioning')

    db.session.add_all([admin, wifi, pool, ac])
    db.session.commit()
    print('Database initialized!')
"
```

4. Run the application:
```bash
python run.py
```

### Testing

Run the comprehensive test suite:
```bash
chmod +x test_api.sh
./test_api.sh
```

## Authentication & Authorization

### Admin User
- **Email**: admin@hbnb.io
- **Password**: admin1234
- **Privileges**: Full access to all endpoints

### User Registration
Only administrators can create new users via the API.

### JWT Tokens
- Obtained via `/api/v1/auth/login`
- Include user ID and admin status
- Required for protected endpoints

## Database Schema

The application uses SQLAlchemy with SQLite for development. The database includes:

- **Users**: User accounts with authentication
- **Places**: Rental properties with geolocation
- **Reviews**: User reviews for places (with constraints)
- **Amenities**: Place amenities
- **Place_Amenity**: Many-to-many association table

See `database_diagram.md` for the complete ER diagram.

## Security Features

- **Password Hashing**: bcrypt for secure password storage
- **JWT Authentication**: Stateless token-based authentication
- **Role-Based Access Control**: Admin vs. regular user permissions
- **Ownership Validation**: Users can only modify their own data
- **Business Logic Constraints**: Prevents self-reviews and duplicate reviews

## Key Files Generated

- **SQL Scripts**: Database creation and initialization
- **ER Diagram**: Visual database schema representation
- **Test Scripts**: Comprehensive API testing
- **Documentation**: Complete project documentation

## All Requirements Met

This implementation fully satisfies all requirements from the HBnB Part 3 project specification, including:
- JWT-based authentication and authorization
- SQLAlchemy database integration
- Complete CRUD operations with persistence
- Proper entity relationships and constraints
- Security best practices
- Comprehensive testing and documentation