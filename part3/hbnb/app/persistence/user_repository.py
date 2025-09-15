from .repository import SQLAlchemyRepository
from app.models.user import User

class UserRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(User)

    def get_by_email(self, email):
        """Get user by email address"""
        return self.get_by_attribute('email', email)