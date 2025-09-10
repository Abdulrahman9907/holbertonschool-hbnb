# app/models/review.py
from . import BaseModel, _require_str, _require_int
from .user import User
from .place import Place

class Review(BaseModel):
    """
    Review:
      - text   (required string)
      - rating (int in [1, 5])
      - place  (Place)
      - user   (User)
    """
    def __init__(self, text: str, rating: int, place: Place, user: User):
        super().__init__()
        _require_str("text", text, required=True)
        rating_i = _require_int("rating", rating)
        if not (1 <= rating_i <= 5):
            raise ValueError("rating must be between 1 and 5")
        if not isinstance(place, Place):
            raise TypeError("place must be a Place")
        if not isinstance(user, User):
            raise TypeError("user must be a User")

        self.text = text
        self.rating = rating_i
        self.place = place
        self.user = user

    def _validate_field(self, key, value):
        if key == "text":
            _require_str("text", value, required=True)
        elif key == "rating":
            v = _require_int("rating", value)
            if not (1 <= v <= 5):
                raise ValueError("rating must be between 1 and 5")
        elif key == "place":
            if not isinstance(value, Place):
                raise TypeError("place must be a Place")
        elif key == "user":
            if not isinstance(value, User):
                raise TypeError("user must be a User")
