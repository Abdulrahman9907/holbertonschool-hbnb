#!/usr/bin/env python3

"""Script to create database tables"""

from app import create_app
from database import db
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity

def create_tables():
    """Create all database tables"""
    app = create_app()

    with app.app_context():
        # Create all tables
        db.create_all()
        print("Database tables created successfully!")

if __name__ == "__main__":
    create_tables()