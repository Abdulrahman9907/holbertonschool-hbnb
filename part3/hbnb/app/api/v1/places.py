from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import facade

api = Namespace('places', description='Place operations')

# Define the place model for input validation and documentation
place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(required=False, description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude coordinate'),
    'longitude': fields.Float(required=True, description='Longitude coordinate'),
    'owner_id': fields.String(required=True, description='ID of the place owner'),
    'amenities': fields.List(fields.String, required=False, description='List of amenity IDs')
})

@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model, validate=True)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(404, 'Owner not found')
    @jwt_required()
    def post(self):
        """Register a new place"""
        current_user = get_jwt_identity()
        place_data = api.payload.copy()
        
        # Set the owner_id to the authenticated user
        place_data['owner_id'] = current_user['id']
        
        # Check if owner exists
        owner = facade.get_user(place_data['owner_id'])
        if not owner:
            return {'error': 'Owner not found'}, 404
        
        try:
            new_place = facade.create_place(place_data)
            if not new_place:
                return {'error': 'Failed to create place'}, 400
                
            return {
                'id': new_place.id,
                'title': new_place.title,
                'description': new_place.description,
                'price': new_place.price,
                'latitude': new_place.latitude,
                'longitude': new_place.longitude,
                'owner': {
                    'id': new_place.owner.id,
                    'first_name': new_place.owner.first_name,
                    'last_name': new_place.owner.last_name,
                    'email': new_place.owner.email
                },
                'amenities': [{'id': amenity.id, 'name': amenity.name} for amenity in new_place.amenities]
            }, 201
        except Exception as e:
            return {'error': str(e)}, 400

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """Retrieve a list of all places"""
        places = facade.get_all_places()
        
        places_list = []
        for place in places:
            place_dict = {
                'id': place.id,
                'title': place.title,
                'description': place.description,
                'price': place.price,
                'latitude': place.latitude,
                'longitude': place.longitude,
                'owner': {
                    'id': place.owner.id,
                    'first_name': place.owner.first_name,
                    'last_name': place.owner.last_name,
                    'email': place.owner.email
                },
                'amenities': [{'id': amenity.id, 'name': amenity.name} for amenity in place.amenities]
            }
            places_list.append(place_dict)
        
        return places_list, 200

@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID"""
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
            
        return {
            'id': place.id,
            'title': place.title,
            'description': place.description,
            'price': place.price,
            'latitude': place.latitude,
            'longitude': place.longitude,
            'owner': {
                'id': place.owner.id,
                'first_name': place.owner.first_name,
                'last_name': place.owner.last_name,
                'email': place.owner.email
            },
            'amenities': [{'id': amenity.id, 'name': amenity.name} for amenity in place.amenities],
            'reviews': [{'id': review.id, 'text': review.text, 'rating': review.rating, 
                        'user_id': review.user.id} for review in place.reviews]
        }, 200

    @api.expect(place_model, validate=True)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Unauthorized action')
    @jwt_required()
    def put(self, place_id):
        """Update place information"""
        current_user = get_jwt_identity()
        place_data = api.payload.copy()
        
        # Check if place exists
        existing_place = facade.get_place(place_id)
        if not existing_place:
            return {'error': 'Place not found'}, 404

        # Check if user is the owner or admin
        is_admin = current_user.get('is_admin', False)
        user_id = current_user.get('id')

        if not is_admin and existing_place.owner.id != user_id:
            return {'error': 'Unauthorized action'}, 403
        
        # Remove owner_id and amenities from update data (these shouldn't be updated via PUT)
        place_data.pop('owner_id', None)
        place_data.pop('amenities', None)
        
        try:
            updated_place = facade.update_place(place_id, place_data)
            
            return {
                'id': updated_place.id,
                'title': updated_place.title,
                'description': updated_place.description,
                'price': updated_place.price,
                'latitude': updated_place.latitude,
                'longitude': updated_place.longitude,
                'owner': {
                    'id': updated_place.owner.id,
                    'first_name': updated_place.owner.first_name,
                    'last_name': updated_place.owner.last_name,
                    'email': updated_place.owner.email
                },
                'amenities': [{'id': amenity.id, 'name': amenity.name} for amenity in updated_place.amenities]
            }, 200
        except Exception as e:
            return {'error': str(e)}, 400