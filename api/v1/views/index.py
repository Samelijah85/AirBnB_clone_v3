#!/usr/bin/python3
"""
Module: api/vi/views/index.py

Creates views routes
"""
from flask import jsonify
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

classes = {
    'amenities': Amenity, 'cities': City,
    'places': Place, 'reviews': Review,
    'states': State, 'users': User
    }


@app_views.route('/status', methods=['GET'])
def status():
    """Returns the status of the API"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'])
def stats():
    """Retrieves the number of each object by type"""
    obj_stats = {}
    for key, value in classes.items():
        obj_stats[key] = storage.count(value)
    return jsonify(obj_stats)
