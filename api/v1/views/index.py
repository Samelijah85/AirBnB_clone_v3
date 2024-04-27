#!/usr/bin/python3
"""
Module: api/vi/views/index.py

Creates views routes
"""
from flask import jsonify
from api.v1.views import app_views

@app_views.route('/status', methods=['GET'])
def status():
    return jsonify({'status': 'OK'})
