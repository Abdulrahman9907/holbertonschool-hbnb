from app.persistence.repository import InMemoryRepository

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    def create_user(self, user_data):
        user = User(**user_data)
        self.user_repo.add(user)
        return user


    def get_place(self, place_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)

    def get_all_users(self):
        """Retrieve all users from the repository"""
        return self.user_repo.get_all()

    def update_user(self, user_id, user_data):
        """Update a user's information"""
        user = self.user_repo.get(user_id)
        if not user:
            return None

        # Update user attributes
        for key, value in user_data.items():
            if hasattr(user, key):
                setattr(user, key, value)

        self.user_repo.update(user_id, user)
        return user
