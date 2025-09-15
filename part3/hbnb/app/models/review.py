# app/models/review.py
from sqlalchemy import Column, String, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship
from . import BaseModel, _require_str, _require_int

class Review(BaseModel):
    """
    Review:
      - text   (required string)
      - rating (int in [1, 5])
      - place  (Place)
      - user   (User)
    """
    __tablename__ = 'reviews'

    text = Column(Text, nullable=False)
    rating = Column(Integer, nullable=False)
    place_id = Column(String(36), ForeignKey('places.id'), nullable=False)
    user_id = Column(String(36), ForeignKey('users.id'), nullable=False)

    # Relationships (will be updated in Task 8)
    place = relationship("Place", back_populates="reviews")
    user = relationship("User", back_populates="reviews")

    def __init__(self, text: str = None, rating: int = None, place=None, user=None, **kwargs):
        super().__init__(**kwargs)
        if text is not None:
            _require_str("text", text, required=True)
            self.text = text
        if rating is not None:
            rating_i = _require_int("rating", rating)
            if not (1 <= rating_i <= 5):
                raise ValueError("rating must be between 1 and 5")
            self.rating = rating_i
        if place is not None:
            from .place import Place
            if not isinstance(place, Place):
                raise TypeError("place must be a Place")
            self.place = place
            self.place_id = place.id
        if user is not None:
            from .user import User
            if not isinstance(user, User):
                raise TypeError("user must be a User")
            self.user = user
            self.user_id = user.id

    def _validate_field(self, key, value):
        if key == "text":
            _require_str("text", value, required=True)
        elif key == "rating":
            v = _require_int("rating", value)
            if not (1 <= v <= 5):
                raise ValueError("rating must be between 1 and 5")
        elif key == "place":
            from .place import Place
            if not isinstance(value, Place):
                raise TypeError("place must be a Place")
        elif key == "user":
            from .user import User
            if not isinstance(value, User):
                raise TypeError("user must be a User")
