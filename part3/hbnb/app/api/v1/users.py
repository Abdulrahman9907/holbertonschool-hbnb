from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import facade

api = Namespace('users', description='User operations')

# Define the user model for input validation and documentation
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password of the user')
})

# Define the user model for updates (password optional)
user_update_model = api.model('UserUpdate', {
    'first_name': fields.String(required=False, description='First name of the user'),
    'last_name': fields.String(required=False, description='Last name of the user'),
    'email': fields.String(required=False, description='Email of the user'),
    'password': fields.String(required=False, description='Password of the user')
})

@api.route('/')
class UserList(Resource):
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Admin privileges required')
    @jwt_required()
    def post(self):
        """Register a new user (Admin only)"""
        current_user = get_jwt_identity()
        
        # Check if user is admin
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403
            
        user_data = api.payload
        
        try:
            # Check if email is already registered
            existing_user = facade.get_user_by_email(user_data['email'])
            if existing_user:
                return {'error': 'Email already registered'}, 400

            # Create new user (password will be hashed automatically)
            new_user = facade.create_user(user_data)
            
            # Return user data WITHOUT password
            return {
                'id': new_user.id,
                'first_name': new_user.first_name,
                'last_name': new_user.last_name,
                'email': new_user.email,
                'is_admin': new_user.is_admin,
                'created_at': new_user.created_at.isoformat()
            }, 201
            
        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error': 'Internal server error'}, 500

    @api.response(200, 'List of users retrieved successfully')
    def get(self):
        """Retrieve a list of all users"""
        users = facade.get_all_users()
        
        users_list = []
        for user in users:
            # Explicitly exclude password from response
            user_dict = {
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'is_admin': user.is_admin,
                'created_at': user.created_at.isoformat(),
                'updated_at': user.updated_at.isoformat()
            }
            users_list.append(user_dict)
        
        return users_list, 200

@api.route('/<user_id>')
class UserResource(Resource):
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by ID"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        
        # Return user data WITHOUT password
        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'is_admin': user.is_admin,
            'created_at': user.created_at.isoformat(),
            'updated_at': user.updated_at.isoformat()
        }, 200

    @api.expect(user_update_model, validate=True)
    @api.response(200, 'User updated successfully')
    @api.response(404, 'User not found')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Unauthorized action')
    @jwt_required()
    def put(self, user_id):
        """Update user information"""
        current_user = get_jwt_identity()
        user_data = api.payload
        
        try:
            # Check if user exists
            existing_user = facade.get_user(user_id)
            if not existing_user:
                return {'error': 'User not found'}, 404

            # Check if user is updating their own data or is admin
            is_admin = current_user.get('is_admin', False)
            current_user_id = current_user.get('id')

            if not is_admin and user_id != current_user_id:
                return {'error': 'Unauthorized action'}, 403

            # For regular users (non-admin), prevent email and password changes
            if not is_admin:
                if 'email' in user_data:
                    return {'error': 'You cannot modify email or password'}, 400
                if 'password' in user_data:
                    return {'error': 'You cannot modify email or password'}, 400

            # Check email uniqueness if email is being updated (for admins)
            if 'email' in user_data and user_data['email'] != existing_user.email:
                user_with_email = facade.get_user_by_email(user_data['email'])
                # If email exists and belongs to a different user, return error
                if user_with_email and user_with_email.id != user_id:
                    return {'error': 'Email already registered'}, 400

            # Update the user (password will be hashed automatically if provided)
            updated_user = facade.update_user(user_id, user_data)
            
            # Return updated user data WITHOUT password
            return {
                'id': updated_user.id,
                'first_name': updated_user.first_name,
                'last_name': updated_user.last_name,
                'email': updated_user.email,
                'is_admin': updated_user.is_admin,
                'created_at': updated_user.created_at.isoformat(),
                'updated_at': updated_user.updated_at.isoformat()
            }, 200
            
        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error': 'Internal server error'}, 500
