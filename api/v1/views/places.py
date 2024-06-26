#!/usr/bin/python3
"""
Module: api/vi/views/places.py

API endpoints for Place objects.
"""
from flask import abort, jsonify, make_response, request
from werkzeug.exceptions import BadRequest
from api.v1.views import app_views
from models import storage
from models.city import City
from models.user import User
from models.place import Place
from models.state import State
from models.amenity import Amenity


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places(city_id):
    """Retrieves the list of all Place objects of a City"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """Retrieves a Place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """Deletes a Place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({})


@app_views.route('/cities/<city_id>/places', methods=['POST'],
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
    user = storage.get(User, data['user_id'])
    if not user:
        abort(404)

    if 'name' not in data:
        return make_response(jsonify({'error': "Missing name"}), 400)

    new_place = Place(**data)
    new_place.city_id = city.id
    new_place.save()
    return make_response(jsonify(new_place.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """Updates a Place object"""
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


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def search_place():
    """
    Retrieves all Place objects depending of the JSON in the body of the
    request
    """
    if not request.is_json:
        return make_response(jsonify({'error': "Not a JSON"}), 400)
    try:
        data = request.get_json()
    except BadRequest:
        return make_response(jsonify({'error': "Not a JSON"}), 400)

    if len(data):
        states = data.get('states', None)
        cities = data.get('cities', None)
        amenities = data.get('amenities', None)
    else:
        places = storage.all(Place).values()
        list_places = [place.to_dict() for place in places]
        return jsonify(list_places)

    list_places = []
    if states:
        list_states = [storage.get(State, state_id) for state_id in states]
        for state in list_states:
            if state:
                for city in state.cities:
                    for place in city.places:
                        list_places.append(place)

    if cities:
        list_cities = [storage.get(City, city_id) for city_id in cities]
        for city in list_cities:
            if city:
                for place in city.places:
                    if place not in list_places:
                        list_places.append(place)

    if amenities:
        if not list_places:
            list_places = storage.all(Place).values()
        list_amenities = [storage.get(Amenity, a_id) for a_id in amenities]
        list_places = [place for place in list_places
                       if all([am in place.amenities
                               for am in list_amenities])]

    places = []
    for place in list_places:
        place_dict = place.to_dict()
        place_dict.pop('amenities', None)
        places.append(place_dict)

    return jsonify(places)
