#!/usr/bin/python3
"""
Module: api/vi/views/review.py

API endpoints for Review objects.
"""
from flask import abort, jsonify, make_response, request
from werkzeug.exceptions import BadRequest
from api.v1.views import app_views
from models import storage
from models.review import Review
from models.place import Place


@app_views.route('/places/<place_id>/review', methods=['GET'],
                 strict_slashes=False)
def get_reviews(place_id):
    """Retrieves the list of all review objects of a specific Place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    reviews = [review.to_dict() for review in place.reviews]
    return jsonify(reviews)


@app_views.route('/review/<review_id>', methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """Retrieves a specific review based on id"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/review/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """Deletes a review based on id provided"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({})


@app_views.route('/places/<place_id>/review', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """Creates a Review"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if not request.is_json:
        return make_response(jsonify({'error': "Not a JSON"}), 400)
    try:
        data = request.get_json()
    except BadRequest:
        return make_response(jsonify({'error': "Not a JSON"}), 400)
    if 'user_id' not in data:
        return make_response(jsonify({'error': "Missing user_id"}), 400)
    if 'text' not in data:
        return make_response(jsonify({'error': "Missing text"}), 400)
    new_review = Review(**data)
    new_review.place_id = place.id
    new_review.save()
    return make_response(jsonify(new_review.to_dict()), 201)


@app_views.route('/review/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """Updates a Review"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    if not request.is_json:
        return make_response(jsonify({'error': "Not a JSON"}), 400)
    try:
        data = request.get_json()
    except BadRequest:
        return make_response(jsonify({'error': "Not a JSON"}), 400)
    ignored_keys = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignored_keys:
            setattr(review, key, value)
    storage.save()
    return jsonify(review.to_dict())
