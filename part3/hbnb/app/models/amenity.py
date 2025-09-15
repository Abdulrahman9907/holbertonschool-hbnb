# app/models/amenity.py
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from . import BaseModel, _require_str, place_amenity

class Amenity(BaseModel):
    """
    Amenity:
      - name (required, <= 50)
    """
    __tablename__ = 'amenities'

    name = Column(String(50), nullable=False, unique=True)

    # Relationships
    places = relationship("Place", secondary=place_amenity, back_populates="amenities")

    def __init__(self, name: str = None, **kwargs):
        super().__init__(**kwargs)
        if name is not None:
            _require_str("name", name, max_len=50, required=True)
            self.name = name

    def _validate_field(self, key, value):
        if key == "name":
            _require_str("name", value, max_len=50, required=True)
