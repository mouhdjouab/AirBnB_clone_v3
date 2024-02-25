#!/usr/bin/python3
"""
STATES VIEWS

"""
from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.state import State


@app_views.route("/states", strict_slashes=False)
def state_all():
    """Retrieve list of all State object"""
    objects = storage.all(State)
    all_states = []
    for value in objects.values():
        all_states.append(value.to_dict())
    return jsonify(all_states)


@app_views.route("/states/<state_id>", strict_slashes=False)
def state_by_ID(state_id: str):
    """
    Retrive one state object by id
    state_id (string): state identifier
    Returns: `State` object in json

    """
    state_by_id = storage.get(State, state_id)
    if not state_by_id:
        abort(404)
    return jsonify(state_by_id.to_dict())


@app_views.route("/states/<state_id>",
                 strict_slashes=False, methods=["DELETE"])
def del_state(state_id):
    """
    Delete a state
        state_id (str): state identifier
    Return: Empty dictionary - `{}`
    """
    state_by_ID = storage.get(State, state_id)
    if state_by_ID is None:
        abort(404)
    state_by_ID.delete()
    storage.save()
    return jsonify({})


@app_views.route("/states", strict_slashes=False, methods=["POST"])
def state_create():
    """Create  State object"""

    if request.get_json() is None:
        abort(400, "Not a JSON")
    if "name" not in request.get_json().keys():
        abort(400, "Missing name")
    state = State(**request.get_json())
    state.save()
    return jsonify(state.to_dict()), 201


@app_views.route("/states/<state_id>", strict_slashes=False, methods=["PUT"])
def state_update(state_id):
    """
    Update State object
        state_id (str): state identifier
    Return: State object with   200 code
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if not request.get_json():
        abort(400, "Not a JSON")
    key = "name"
    setattr(state, key, request.get_json().get(key))
    state.save()
    return jsonify(state.to_dict())
