# app/models/place.py
from . import BaseModel, _require_str, _require_float
from .user import User
from .amenity import Amenity

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
    def __init__(self, title: str, description: str | None, price, latitude, longitude, owner: User):
        super().__init__()
        # validate base fields
        _require_str("title", title, max_len=100, required=True)
        if description is not None:
            _require_str("description", description, max_len=None, required=False)
        price_f = _require_float("price", price)
        if price_f <= 0:
            raise ValueError("price must be positive")
        lat_f = _require_float("latitude", latitude)
        if not (-90.0 <= lat_f <= 90.0):
            raise ValueError("latitude must be within -90.0 to 90.0")
        lon_f = _require_float("longitude", longitude)
        if not (-180.0 <= lon_f <= 180.0):
            raise ValueError("longitude must be within -180.0 to 180.0")
        if not isinstance(owner, User):
            raise TypeError("owner must be a User")

        self.title = title
        self.description = description
        self.price = float(price_f)
        self.latitude = float(lat_f)
        self.longitude = float(lon_f)
        self.owner = owner

        # relationships
        self.reviews = []     # list of Review (added via add_review)
        self.amenities = []   # list of Amenity

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
            if not isinstance(value, User):
                raise TypeError("owner must be a User")
        # reviews/amenities are managed via methods, not direct update

    # relationships management
    def add_review(self, review):
        # imported lazily to avoid circular at import time
        from .review import Review
        if not isinstance(review, Review):
            raise TypeError("review must be a Review")
        if review.place is not self:
            raise ValueError("review.place must reference this Place")
        self.reviews.append(review)
        self.save()

    def add_amenity(self, amenity: Amenity):
        if not isinstance(amenity, Amenity):
            raise TypeError("amenity must be an Amenity")
        if amenity not in self.amenities:
            self.amenities.append(amenity)
            self.save()

    def remove_amenity(self, amenity: Amenity):
        if amenity in self.amenities:
            self.amenities.remove(amenity)
            self.save()
