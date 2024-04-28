#!/usr/bin/python3
"""
Module: api/vi/views/place.py

API endpoints for Place objects.
"""
from flask import abort, jsonify, make_response, request
from werkzeug.exceptions import BadRequest
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.city import City


@app_views.route('/cities/<city_id>/place', methods=['GET'],
                 strict_slashes=False)
def get_places(city_id):
    """Retrieves the list of all place objects of a specific City"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    reviews = [place.to_dict() for place in city.reviews]
    return jsonify(reviews)


@app_views.route('/place/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """Retrieves a specific place based on id"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/place/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """Deletes a place based on id provided"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({})


@app_views.route('/cities/<city_id>/place', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """Creates a Place"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    if not request.is_json:
        return make_response(jsonify({'error': "Not a JSON"}), 400)
    try:
        data = request.get_json()
    except BadRequest:
        return make_response(jsonify({'error': "Not a JSON"}), 400)
    if 'user_id' not in data:
        return make_response(jsonify({'error': "Missing user_id"}), 400)
    if 'name' not in data:
        return make_response(jsonify({'error': "Missing name"}), 400)
    new_place = Place(**data)
    new_place.city_id = city.id
    new_place.save()
    return make_response(jsonify(new_place.to_dict()), 201)


@app_views.route('/place/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """Updates a Place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if not request.is_json:
        return make_response(jsonify({'error': "Not a JSON"}), 400)
    try:
        data = request.get_json()
    except BadRequest:
        return make_response(jsonify({'error': "Not a JSON"}), 400)
    ignored_keys = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignored_keys:
            setattr(place, key, value)
    storage.save()
    return jsonify(place.to_dict())
