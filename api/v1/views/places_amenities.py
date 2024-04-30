#!/usr/bin/python3
"""
Module: api/vi/views/places_amenities.py

API endpoints for place_amenities objects.
"""
from flask import abort, jsonify, make_response
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.place import Place
from models import storage_t


@app_views.route('/places/<place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def get_place_amenities(place_id):
    """Retrieves the list of all Amenity objects of a Place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if storage_t == "db":
        amenities = [amenity.to_dict() for amenity in place.amenities]
    else:
        amenities = []
        for amenity_id in place.amenity_ids:
            amenity = storage.get(Amenity, amenity_id)
            amenities.append(amenity.to_dict())
    return jsonify(amenities)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_place_amenity(place_id, amenity_id):
    """Deletes a Amenity object to a Place"""
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if place is None or amenity is None:
        abort(404)

    for place_amenity in place.amenities:
        if place_amenity.id == amenity.id:
            if storage_t == 'db':
                place.amenities.remove(amenity)
            else:
                place.amenity_ids.remove(amenity)
            storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['POST'],
                 strict_slashes=False)
def link_amenity(place_id, amenity_id):
    """Link a Amenity object to a Place"""
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if place is None or amenity is None:
        abort(404)
    if storage_t == "db":
        if amenity in place.amenities:
            return jsonify(amenity.to_dict())
        place.amenities.append(amenity)
    else:
        if amenity_id in place.amenity_ids:
            return jsonify(amenity.to_dict())
        place.amenity_ids.append(amenity_id)
    storage.save()
    return make_response(jsonify(amenity.to_dict()), 201)
