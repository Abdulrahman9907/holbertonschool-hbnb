from flask import Flask
from flask_restx import Api
from flask_bcrypt import Bcrypt
from app.api.v1.users import api as users_ns
from app.api.v1.amenities import api as amenities_ns
from app.api.v1.places import api as places_ns
from app.api.v1.reviews import api as reviews_ns

# Create bcrypt instance (will be initialized in create_app)
bcrypt = Bcrypt()

def create_app(config_class="config.DevelopmentConfig"):
    """
    Flask Application Factory
    
    Args:
        config_class (str): String reference to configuration class
                           Default: "config.DevelopmentConfig"
    
    Returns:
        Flask: Configured Flask application instance
    """
    app = Flask(__name__)
    
    # Load configuration from the specified class
    # Flask will resolve the string to the actual class
    app.config.from_object(config_class)
    
    # Initialize Flask extensions
    bcrypt.init_app(app)
    
    # Initialize Flask-RESTX API
    api = Api(
        app,
        version='1.0',
        title='HBnB API',
        description='HBnB Application API',
        doc='/api/v1/'
    )
    
    # Register API namespaces
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')
    
    return app
