from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('reviews', description='Review operations')

# Define the review model for input validation and documentation
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Review text'),
    'rating': fields.Integer(required=True, description='Rating from 1 to 5'),
    'user_id': fields.String(required=True, description='ID of the user making the review'),
    'place_id': fields.String(required=True, description='ID of the place being reviewed')
})

@api.route('/')
class ReviewList(Resource):
    @api.expect(review_model, validate=True)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(404, 'User or Place not found')
    def post(self):
        """Create a new review"""
        review_data = api.payload.copy()
        
        # Check if user and place exist
        user = facade.get_user(review_data['user_id'])
        place = facade.get_place(review_data['place_id'])
        
        if not user:
            return {'error': 'User not found'}, 404
        if not place:
            return {'error': 'Place not found'}, 404
        
        try:
            new_review = facade.create_review(review_data)
            if not new_review:
                return {'error': 'Failed to create review'}, 400
                
            return {
                'id': new_review.id,
                'text': new_review.text,
                'rating': new_review.rating,
                'user': {
                    'id': new_review.user.id,
                    'first_name': new_review.user.first_name,
                    'last_name': new_review.user.last_name,
                    'email': new_review.user.email
                },
                'place': {
                    'id': new_review.place.id,
                    'title': new_review.place.title
                }
            }, 201
        except Exception as e:
            return {'error': str(e)}, 400

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve a list of all reviews"""
        reviews = facade.get_all_reviews()
        
        reviews_list = []
        for review in reviews:
            review_dict = {
                'id': review.id,
                'text': review.text,
                'rating': review.rating,
                'user': {
                    'id': review.user.id,
                    'first_name': review.user.first_name,
                    'last_name': review.user.last_name,
                    'email': review.user.email
                },
                'place': {
                    'id': review.place.id,
                    'title': review.place.title
                }
            }
            reviews_list.append(review_dict)
        
        return reviews_list, 200

@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID"""
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
            
        return {
            'id': review.id,
            'text': review.text,
            'rating': review.rating,
            'user': {
                'id': review.user.id,
                'first_name': review.user.first_name,
                'last_name': review.user.last_name,
                'email': review.user.email
            },
            'place': {
                'id': review.place.id,
                'title': review.place.title
            }
        }, 200

    @api.expect(review_model, validate=True)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    def put(self, review_id):
        """Update review information"""
        review_data = api.payload.copy()
        
        # Check if review exists
        existing_review = facade.get_review(review_id)
        if not existing_review:
            return {'error': 'Review not found'}, 404
        
        # Remove user_id and place_id from update data (these shouldn't be updated via PUT)
        review_data.pop('user_id', None)
        review_data.pop('place_id', None)
        
        try:
            updated_review = facade.update_review(review_id, review_data)
            
            return {
                'id': updated_review.id,
                'text': updated_review.text,
                'rating': updated_review.rating,
                'user': {
                    'id': updated_review.user.id,
                    'first_name': updated_review.user.first_name,
                    'last_name': updated_review.user.last_name,
                    'email': updated_review.user.email
                },
                'place': {
                    'id': updated_review.place.id,
                    'title': updated_review.place.title
                }
            }, 200
        except Exception as e:
            return {'error': str(e)}, 400

    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        """Delete a review"""
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        
        success = facade.delete_review(review_id)
        if success:
            return {'message': 'Review deleted successfully'}, 200
        else:
            return {'error': 'Failed to delete review'}, 500

@api.route('/places/<place_id>')
class PlaceReviewList(Resource):
    @api.response(200, 'Reviews for place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a specific place"""
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
            
        reviews_list = []
        for review in place.reviews:
            review_dict = {
                'id': review.id,
                'text': review.text,
                'rating': review.rating,
                'user': {
                    'id': review.user.id,
                    'first_name': review.user.first_name,
                    'last_name': review.user.last_name,
                    'email': review.user.email
                }
            }
            reviews_list.append(review_dict)
        
        return reviews_list, 200