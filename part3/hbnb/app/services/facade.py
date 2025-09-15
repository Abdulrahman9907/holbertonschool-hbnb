from app.persistence.user_repository import UserRepository
from app.persistence.place_repository import PlaceRepository
from app.persistence.review_repository import ReviewRepository
from app.persistence.amenity_repository import AmenityRepository
from app.models import User, Place, Review, Amenity

class HBnBFacade:
    def __init__(self):
        self.user_repo = UserRepository()
        self.place_repo = PlaceRepository()
        self.review_repo = ReviewRepository()
        self.amenity_repo = AmenityRepository()

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
        return self.user_repo.get_by_email(email)

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
        return user

    # Amenity methods
    def create_amenity(self, amenity_data):
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_amenity_by_name(self, name):
        return self.amenity_repo.get_by_name(name)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            return None
        amenity.update(amenity_data)
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
        # Don't allow owner changes
        if 'owner' in place_data:
            place_data = place_data.copy()
            del place_data['owner']
        place.update(place_data)
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
        # Don't allow user/place changes
        filtered_data = {k: v for k, v in review_data.items() if k not in ['user', 'place']}
        review.update(filtered_data)
        return review

    def delete_review(self, review_id):
        review = self.review_repo.get(review_id)
        if not review:
            return False
        self.review_repo.delete(review_id)
        return True

    def get_reviews_by_place(self, place_id):
        """Get all reviews for a specific place"""
        place = self.get_place(place_id)
        if not place:
            return []
        return place.reviews

    def get_user_reviews(self, user_id):
        """Get all reviews created by a specific user"""
        all_reviews = self.get_all_reviews()
        return [review for review in all_reviews if review.user.id == user_id]

    def delete_place(self, place_id):
        """Delete a place"""
        place = self.place_repo.get(place_id)
        if not place:
            return False
        # SQLAlchemy cascade will handle review deletion
        self.place_repo.delete(place_id)
        return True
