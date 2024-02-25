#!/usr/bin/python3
"""RESTful API actions for City"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State
from models.city import City


@app_views.route("/states/<state_id>/cities")
def city_by_state(state_id):
    """
    Retrieve all City of a state
        state_id (str): State identifier
    """
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    cities = []
    for city in state.cities:
        cities.append(city.to_dict())

    return jsonify(cities)


@app_views.route("/cities/<city_id>")
def city_by_id(city_id):
    """
    Retrieve City by ID

    """

    city = storage.get(City, city_id)
    if not city:
        abort(404)

    return jsonify(city.to_dict())


@app_views.route("/cities/<city_id>", methods=["DELETE"])
def city_delete(city_id):
    """
    delete  city
        city_id (str): City identifier
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    city.delete()
    storage.save()

    return jsonify({}), 200


@app_views.route("/states/<state_id>/cities", methods=["POST"])
def city_create(state_id):
    """
    Create  city
        state_id (str): State identifier
    """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    if not request.get_json():
        abort(400, "Not a JSON")
    if "name" not in request.get_json():
        abort(400, "Missing name")

    city = City(state_id=state_id, **request.get_json())
    city.save()

    return jsonify(city.to_dict()), 201


@app_views.route("/cities/<city_id>", methods=["PUT"])
def city_update(city_id):
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    if not request.get_json():
        abort(400, "Not a JSON")

    key = "name"
    setattr(city, key, request.get_json().get(key))
    city.save()

    return jsonify(city.to_dict())
