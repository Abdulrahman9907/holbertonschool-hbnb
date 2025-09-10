from app.persistence.repository import InMemoryRepository
from app.models import User, Place, Review, Amenity

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    def create_user(self, user_data):
        """Create a new user with hashed password"""
        user = User(**user_data)  # Password will be hashed automatically in __init__
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_place(self, place_id):
        return self.place_repo.get(place_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)

    def get_all_users(self):
        """Retrieve all users from the repository"""
        return self.user_repo.get_all()

    def update_user(self, user_id, user_data):
        """Update a user's information (including password hashing if needed)"""
        user = self.user_repo.get(user_id)
        if not user:
            return None

        # Use the User model's update method which handles password hashing
        user.update(user_data)
        
        # Update in repository
        self.user_repo.update(user_id, user)
        return user

    # Amenity methods
    def create_amenity(self, amenity_data):
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_amenity_by_name(self, name):
        return self.amenity_repo.get_by_attribute('name', name)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            return None
        for key, value in amenity_data.items():
            if hasattr(amenity, key):
                setattr(amenity, key, value)
        self.amenity_repo.update(amenity_id, amenity)
        return amenity

    # Place methods
    def create_place(self, place_data):
        # Get owner from user_repo
        owner_id = place_data.pop('owner_id')
        owner = self.get_user(owner_id)
        if not owner:
            return None
        place_data['owner'] = owner
        
        # Handle amenities if provided
        if 'amenities' in place_data:
            amenity_ids = place_data.pop('amenities')
            amenities = [self.get_amenity(aid) for aid in amenity_ids if self.get_amenity(aid)]
            place = Place(**place_data)
            for amenity in amenities:
                place.add_amenity(amenity)
        else:
            place = Place(**place_data)
        
        self.place_repo.add(place)
        return place

    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        place = self.place_repo.get(place_id)
        if not place:
            return None
        for key, value in place_data.items():
            if hasattr(place, key) and key != 'owner':  # Don't allow owner changes
                setattr(place, key, value)
        self.place_repo.update(place_id, place)
        return place

    # Review methods
    def create_review(self, review_data):
        # Get user and place from repos
        user_id = review_data.pop('user_id')
        place_id = review_data.pop('place_id')
        user = self.get_user(user_id)
        place = self.get_place(place_id)
        
        if not user or not place:
            return None
            
        review_data['user'] = user
        review_data['place'] = place
        
        review = Review(**review_data)
        self.review_repo.add(review)
        
        # Add review to place
        place.add_review(review)
        
        return review

    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def update_review(self, review_id, review_data):
        review = self.review_repo.get(review_id)
        if not review:
            return None
        for key, value in review_data.items():
            if hasattr(review, key) and key not in ['user', 'place']:  # Don't allow user/place changes
                setattr(review, key, value)
        self.review_repo.update(review_id, review)
        return review

    def delete_review(self, review_id):
        review = self.review_repo.get(review_id)
        if not review:
            return False
        # Remove from place's reviews list
        if review in review.place.reviews:
            review.place.reviews.remove(review)
            review.place.save()
        self.review_repo.delete(review_id)
        return True
