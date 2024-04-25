#!/usr/bin/python3
"""
Module: api/vi/views/index.py

Creates views routes
"""
from flask import jsonify
from api.v1.views import app_views
from models import *
from models import storage


@app_views.route('/status', methods=['GET'])
def status():
    """Returns the status of the API"""
    return jsonify({'status': 'OK'})


@app_views.route('/stats', methods=['GET'])
def stats():
    """Retrieves the number of each object by type"""
    amenities = storage.count('Amenity')
    cities = storage.count('City')
    places = storage.count('Place')
    reviews = storage.count('Review')
    states = storage.count('State')
    users = storage.count('User')
    return jsonify({
        "amenities": amenities,
        "cities": cities,
        "places": places,
        "reviews": reviews,
        "states": states,
        "users": users
        })
