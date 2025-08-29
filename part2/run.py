#!/usr/bin/env python3
"""
Entry point for the HBnB Flask application.
"""

import sys
import os

# Add the hbnb directory to the path to allow imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'hbnb'))

from hbnb.app import create_app

app = create_app('development')

if __name__ == '__main__':
    print("Starting HBnB API server...")
    print("Access the API documentation at: http://localhost:5000/api/v1/")
    app.run(host='0.0.0.0', port=5000, debug=True)