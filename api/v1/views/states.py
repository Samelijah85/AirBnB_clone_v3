#!/usr/bin/python3
"""
Module: api/vi/views/states.py

API endpoints for State objects.
"""
from flask import abort, jsonify, make_response, request
from werkzeug.exceptions import BadRequest
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """Retrieve all State objects."""
    states = storage.all(State).values()
    state_list = [state.to_dict() for state in states]
    return jsonify(state_list)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """Retrieve a specific State object by ID."""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route(
        '/states/<state_id>',
        methods=['DELETE'],
        strict_slashes=False
        )
def delete_state(state_id):
    """Delete a specific State object by ID."""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({})


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """Create a new State."""
    if not request.is_json:
        return make_response(jsonify({'error': "Not a JSON"}), 400)
    try:
        data = request.get_json()
    except BadRequest:
        return make_response(jsonify({'error': "Not a JSON"}), 400)
    if 'name' not in data:
        return make_response(jsonify({'error': "Missing name"}), 400)
    state = State(**data)
    state.save()
    return make_response(jsonify(state.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """Update a specific State object by ID."""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    if not request.is_json:
        return make_response(jsonify({'error': "Not a JSON"}), 400)
    try:
        data = request.get_json()
    except BadRequest:
        return make_response(jsonify({'error': "Not a JSON"}), 400)
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)
    storage.save()
    return jsonify(state.to_dict())
