from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('amenities', description='Amenity operations')

amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})

@api.route('/')
class AmenityList(Resource):
    @api.expect(amenity_model, validate=True)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(400, 'Amenity name already exists')
    def post(self):
        """Register a new amenity"""
        amenity_data = api.payload
        
        existing_amenity = facade.get_amenity_by_name(amenity_data['name'])
        if existing_amenity:
            return {'error': 'Amenity name already exists'}, 400
        
        new_amenity = facade.create_amenity(amenity_data)
        
        return {
            'id': new_amenity.id,
            'name': new_amenity.name
        }, 201

    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """Retrieve a list of all amenities"""
        amenities = facade.get_all_amenities()
        
        amenities_list = []
        for amenity in amenities:
            amenity_dict = {
                'id': amenity.id,
                'name': amenity.name
            }
            amenities_list.append(amenity_dict)
        
        return amenities_list, 200


@api.route('/<amenity_id>')
class AmenityResource(Resource):
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Get amenity details by ID"""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404
        
        return {
            'id': amenity.id,
            'name': amenity.name
        }, 200

    @api.expect(amenity_model, validate=True)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    @api.response(400, 'Amenity name already exists')
    def put(self, amenity_id):
        """Update an amenity's information"""
        
        amenity_data = api.payload
        existing_amenity = facade.get_amenity(amenity_id)
        if not existing_amenity:
            return {'error': 'Amenity not found'}, 404
        
        if 'name' in amenity_data:
            amenity_with_name = facade.get_amenity_by_name(amenity_data['name'])
            
            if amenity_with_name and amenity_with_name.id != amenity_id:
                return {'error': 'Amenity name already exists'}, 400
        
        updated_amenity = facade.update_amenity(amenity_id, amenity_data)
        
        return {
            'id': updated_amenity.id,
            'name': updated_amenity.name
        }, 200

