# app/models/place.py
from sqlalchemy import Column, String, Float, ForeignKey, Text
from sqlalchemy.orm import relationship
from . import BaseModel, _require_str, _require_float, place_amenity

class Place(BaseModel):
    """
    Place:
      - title       (required, <= 100)
      - description (optional string)
      - price       (float > 0)
      - latitude    (float in [-90, 90])
      - longitude   (float in [-180, 180])
      - owner       (User)
      - reviews     (list of Review, managed via add_review)
      - amenities   (list of Amenity)
    """
    __tablename__ = 'places'

    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Float, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    owner_id = Column(String(36), ForeignKey('users.id'), nullable=False)

    # Relationships
    owner = relationship("User", back_populates="places")
    reviews = relationship("Review", back_populates="place", cascade="all, delete-orphan")
    amenities = relationship("Amenity", secondary=place_amenity, back_populates="places")

    def __init__(self, title: str, description: str = None, price=None, latitude=None, longitude=None, owner=None, **kwargs):
        super().__init__(**kwargs)
        # validate and set basic fields
        if title is not None:
            _require_str("title", title, max_len=100, required=True)
            self.title = title
        if description is not None:
            _require_str("description", description, max_len=None, required=False)
            self.description = description
        if price is not None:
            price_f = _require_float("price", price)
            if price_f <= 0:
                raise ValueError("price must be positive")
            self.price = float(price_f)
        if latitude is not None:
            lat_f = _require_float("latitude", latitude)
            if not (-90.0 <= lat_f <= 90.0):
                raise ValueError("latitude must be within -90.0 to 90.0")
            self.latitude = float(lat_f)
        if longitude is not None:
            lon_f = _require_float("longitude", longitude)
            if not (-180.0 <= lon_f <= 180.0):
                raise ValueError("longitude must be within -180.0 to 180.0")
            self.longitude = float(lon_f)
        if owner is not None:
            from .user import User
            if not isinstance(owner, User):
                raise TypeError("owner must be a User")
            self.owner = owner
            self.owner_id = owner.id

    def _validate_field(self, key, value):
        if key == "title":
            _require_str("title", value, max_len=100, required=True)
        elif key == "description":
            if value is not None:
                _require_str("description", value)
        elif key == "price":
            v = _require_float("price", value)
            if v <= 0:
                raise ValueError("price must be positive")
        elif key == "latitude":
            v = _require_float("latitude", value)
            if not (-90.0 <= float(v) <= 90.0):
                raise ValueError("latitude must be within -90.0 to 90.0")
        elif key == "longitude":
            v = _require_float("longitude", value)
            if not (-180.0 <= float(v) <= 180.0):
                raise ValueError("longitude must be within -180.0 to 180.0")
        elif key == "owner":
            from .user import User
            if not isinstance(value, User):
                raise TypeError("owner must be a User")

    # relationships management
    def add_review(self, review):
        """Add a review to this place"""
        from .review import Review
        if not isinstance(review, Review):
            raise TypeError("review must be a Review")
        if review.place != self:
            raise ValueError("review.place must reference this Place")
        # SQLAlchemy will handle the relationship automatically

    def add_amenity(self, amenity):
        """Add an amenity to this place"""
        from .amenity import Amenity
        if not isinstance(amenity, Amenity):
            raise TypeError("amenity must be an Amenity")
        if amenity not in self.amenities:
            self.amenities.append(amenity)

    def remove_amenity(self, amenity):
        """Remove an amenity from this place"""
        if amenity in self.amenities:
            self.amenities.remove(amenity)
