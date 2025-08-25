# app/models/amenity.py
from . import BaseModel, _require_str

class Amenity(BaseModel):
    """
    Amenity:
      - name (required, <= 50)
    """
    def __init__(self, name: str):
        super().__init__()
        _require_str("name", name, max_len=50, required=True)
        self.name = name

    def _validate_field(self, key, value):
        if key == "name":
            _require_str("name", value, max_len=50, required=True)
