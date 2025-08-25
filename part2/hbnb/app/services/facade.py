from app.persistence.repository import InMemoryRepository

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    # Placeholder: will be implemented in later tasks
    def create_user(self, user_data):
        pass

    # Placeholder: will be implemented in later tasks
    def get_place(self, place_id):
        pass
