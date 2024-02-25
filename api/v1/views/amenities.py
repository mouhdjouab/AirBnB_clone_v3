#!/usr/bin/python3
"""amenities API"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.amenity import Amenity
from datetime import datetime
import uuid


@app_views.route('/amenities/', strict_slashes=False, methods=['GET'])
def amenities_all():
    '''Retrieve  list of all Amenity'''
    amenities = [obj.to_dict() for obj in storage.all("Amenity").values()]
    return jsonify(amenities)


@app_views.route('/amenities/<amenity_id>', strict_slashes=False, methods=['GET'])
def amenity_by_id(amenity_id):
    '''Retrieves  Amenity by ID
    '''
    amenities = storage.all("Amenity").values()
    amenity_objct = [obj.to_dict() for obj in amenities
                     if obj.id == amenity_id]
    if amenity_objct == []:
        abort(404)
    return jsonify(amenity_objct[0])


@app_views.route('/amenities/<amenity_id>', strict_slashes=False, methods=['DELETE'])
def amenity_delete(amenity_id):
    '''Deletes  Amenity '''
    amenities = storage.all("Amenity").values()
    amenity_objct = [obj.to_dict() for obj in amenities
                     if obj.id == amenity_id]
    if amenity_objct == []:
        abort(404)
    amenity_objct.remove(amenity_objct[0])
    for obj in amenities:
        if obj.id == amenity_id:
            storage.delete(obj)
            storage.save()
    return jsonify({}), 200


@app_views.route('/amenities/', strict_slashes=False, methods=['POST'])
def amenity_create():
    '''Creates  Amenity'''
    if not request.get_json():
        abort(400, 'Not a JSON')
    if 'name' not in request.get_json():
        abort(400, 'Missing name')
    amenities = []
    new_amenity = Amenity(name=request.json['name'])
    storage.new(new_amenity)
    storage.save()
    amenities.append(new_amenity.to_dict())
    return jsonify(amenities[0]), 201


@app_views.route('/amenities/<amenity_id>', strict_slashes=False, methods=['PUT'])
def amenity_updates(amenity_id):
    '''Updates Amenity '''
    amenities = storage.all("Amenity").values()
    amenity_objct = [obj.to_dict() for obj in amenities
                     if obj.id == amenity_id]
    if amenity_objct == []:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    amenity_objct[0]['name'] = request.json['name']
    for obj in amenities:
        if obj.id == amenity_id:
            obj.name = request.json['name']
    storage.save()
    return jsonify(amenity_objct[0]), 200
