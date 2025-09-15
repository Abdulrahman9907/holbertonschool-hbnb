# app/models/__init__.py
import re
import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Table, ForeignKey

EMAIL_RE = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")

# Association table for many-to-many relationship between Place and Amenity
# This will be initialized after db is imported

def _require_str(name, value, max_len=None, required=False):
    if required and (value is None or value == ""):
        raise ValueError(f"{name} is required")
    if value is not None and not isinstance(value, str):
        raise TypeError(f"{name} must be a string")
    if max_len is not None and value is not None and len(value) > max_len:
        raise ValueError(f"{name} must be at most {max_len} characters")

def _require_bool(name, value):
    if not isinstance(value, bool):
        raise TypeError(f"{name} must be a boolean")

def _require_float(name, value):
    if not isinstance(value, (float, int)):  # allow ints where float is expected
        raise TypeError(f"{name} must be a number (float)")
    return float(value)

def _require_int(name, value):
    if not isinstance(value, int):
        raise TypeError(f"{name} must be an integer")
    return value

def _require_email(name, value):
    _require_str(name, value, required=True, max_len=255)
    if not EMAIL_RE.match(value):
        raise ValueError(f"{name} must be a valid email")

from database import db

# Association table for many-to-many relationship between Place and Amenity
place_amenity = Table('place_amenity', db.Model.metadata,
    Column('place_id', String(36), ForeignKey('places.id'), primary_key=True),
    Column('amenity_id', String(36), ForeignKey('amenities.id'), primary_key=True)
)

class BaseModel(db.Model):
    """
    Common base with id (UUID string), created_at, updated_at.
    Provides save() and update() with per-field validation hook.
    """
    __abstract__ = True

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    def save(self):
        """Update the updated_at timestamp whenever the object is modified."""
        self.updated_at = datetime.now()
        db.session.commit()

    def _validate_field(self, key, value):
        """Override in subclasses to validate per-field updates."""
        return

    def update(self, data: dict):
        """
        Update attributes from a dict with validation via _validate_field.
        Only updates existing attributes.
        """
        if not isinstance(data, dict):
            raise TypeError("update() expects a dict")
        # validate first
        for k, v in data.items():
            if hasattr(self, k):
                self._validate_field(k, v)
        # apply
        for k, v in data.items():
            if hasattr(self, k):
                setattr(self, k, v)
        self.save()

# Import models after BaseModel definition to avoid circular imports
from .user import User
from .place import Place
from .review import Review
from .amenity import Amenity
