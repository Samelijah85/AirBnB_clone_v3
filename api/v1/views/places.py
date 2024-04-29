#!/usr/bin/python3
"""
Module: api/vi/views/places.py

API endpoints for Place objects.
"""
from flask import abort, jsonify, make_response, request
from werkzeug.exceptions import BadRequest
from api.v1.views import app_views
from models import storage
from models import storage_t
from models.city import City
from models.user import User
from models.place import Place
from models.state import State


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

    list_states_ids = data.get("states")
    list_cities_ids = data.get('cities')
    list_amenities_ids = data.get('amenities')
    list_places = []

    if not list_states_ids and not list_cities_ids:
        list_places = storage.all(Place).values()

    if list_states_ids:
        for s_id in list_states_ids:
            state = storage.all(State).get("State.{}".format(s_id))
            if state:
                for c in state.cities:
                    list_places.extend(c.places)

    if list_cities_ids:
        for c_id in list_cities_ids:
            city = storage.all(City).get("City.{}".format(c_id))
            if city:
                list_places.extend(city.places)

    list_places = list(set(list_places))
    if list_amenities_ids:
        for place in list_places:
            place_ame = []
            if storage_t == "db":
                place_ame = [ame.id for ame in place.amenities]
            else:
                place_ame = place.amenity_ids

            if not all(ame_id in place_ame for ame_id in list_amenities_ids):
                list_places.remove(place)
    places = []
    for p in list_places:
        p_dict = p.to_dict().copy()

        if "amenities" in p.to_dict():
            del p_dict["amenities"]
        places.append(p_dict)

    return jsonify(places)
