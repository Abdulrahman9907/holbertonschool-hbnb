from .repository import SQLAlchemyRepository
from app.models.amenity import Amenity

class AmenityRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(Amenity)

    def get_by_name(self, name):
        """Get amenity by name"""
        return self.get_by_attribute('name', name)