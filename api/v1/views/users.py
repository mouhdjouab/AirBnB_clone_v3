#!/usr/bin/python3
'''
     user API
'''
from flask import jsonify, make_response, abort, request
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'],
                 strict_slashes=False)
def fetch_all_users():
    '''
        fetch all user
    '''
    user_all = []
    users = storage.all(User).values()
    for u in users:
        user_all.append = (u.to_dict())
    return jsonify(user_all)


@app_views.route('/users/<user_id>', methods=['GET'],
                 strict_slashes=False)
def user_by_id(user_id):
    '''
        fetch  one user by id

    '''
    user = storage.get(User, user_id)
    if not user:
        abort(404)

    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_user(user_id):
    '''
        Deleting  User
    '''
    user = storage.get(User, user_id)
    if not user:
        abort(404)

    user.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'],
                 strict_slashes=False)
def user_creat():
    """
    Create user


    """
    if not request.get_json():
        abort(400, "Not a JSON")
    if "email" not in request.get_json():
        abort(400, "Missing email")
    if "password" not in request.get_json():
        abort(400, "Missing password")

    user = User(**request.get_json())
    user.save()

    return jsonify(user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
def updtae_user(user_id=None):
    '''
        Update  user
    '''
    obj_user = storage.get(User, user_id)
    if obj_user is None:
        abort(404)
    if not request.json:
        return jsonify({"error": "Not a JSON"}), 400
    for key, value in request.get_json():
        if key not in ['id', 'created_at', 'email', 'updated_at']:
            setattr(obj_user, key, value)
    obj_user.save()
    return (jsonify(obj_user.to_dict()), 200)
