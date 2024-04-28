#!/usr/bin/python3
"""
Module: api/vi/views/users.py

API endpoints for User objects.
"""
from flask import abort, jsonify, make_response, request
from werkzeug.exceptions import BadRequest
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """Retrieve all User objects."""
    users = storage.all(User).values()
    user_list = [user.to_dict() for user in users]
    return jsonify(user_list)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """Retrieve a specific User object by ID."""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route(
        '/users/<user_id>',
        methods=['DELETE'],
        strict_slashes=False
        )
def delete_user(user_id):
    """Delete a specific User object by ID."""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({})


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """Create a new User."""
    if not request.is_json:
        return make_response(jsonify({'error': "Not a JSON"}), 400)
    try:
        data = request.get_json()
    except BadRequest:
        return make_response(jsonify({'error': "Not a JSON"}), 400)
    if 'email' not in data:
        return make_response(jsonify({'error': "Missing email"}), 400)
    if 'password' not in data:
        return make_response(jsonify({'error': "Missing password"}), 400)
    user = User(**data)
    user.save()
    return make_response(jsonify(user.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """Update a specific User object by ID."""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    if not request.is_json:
        return make_response(jsonify({'error': "Not a JSON"}), 400)
    try:
        data = request.get_json()
    except BadRequest:
        return make_response(jsonify({'error': "Not a JSON"}), 400)
    ignored_keys = ['id', 'email', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignored_keys:
            setattr(user, key, value)
    storage.save()
    return jsonify(user.to_dict())
