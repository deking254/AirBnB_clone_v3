#!/usr/bin/python3
"""return states(s)"""
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City
import json
import flask
from flask import abort, jsonify


@app_views.route('/states/<state_id>/cities',
                 methods=['GET'],
                 strict_slashes=False)
def cities(state_id):
    """retrieves a specific state object"""
    cities = storage.all(City)
    if cities is None:
        abort(404)
    else:
        ctys = []
        for city in cities:
            if cities[city].to_dict().get('state_id') == state_id:
                ctys.append(cities[city].to_dict())
    if ctys == []:
        abort(404)
    return jsonify(ctys), 200


@app_views.route('/cities/<city_id>',
                 methods=['GET'],
                 strict_slashes=False)
def get_city(city_id):
    city = storage.get(City, city_id)
    if city:
        return jsonify(city.to_dict()), 200
    else:
        abort(404)


@app_views.route('/cities/<city_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    city = storage.get(City, city_id)
    if city:
        storage.delete(city)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/states/<state_id>/cities',
                 methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    req = flask.request.get_json()
    state = storage.get(State, state_id)
    if req:
        if req.get("name"):
            if state:
                r = City()
                r.name = req.get("name")
                setattr(r, "state_id", state_id)
                storage.new(r)
                storage.save()
            else:
                abort(404)
        else:
            abort(400, {'Missing name'})
    else:
        abort(400, {"Not a JSON"})
    return jsonify(r.to_dict()), '201'


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    req = flask.request.get_json()
    city = storage.get(City, city_id)
    if city:
        if req:
            ignore_keys = ['id', 'created_at', 'updated_at']
            for key, value in req.items():
                if key not in ignore_keys:
                    setattr(city, key, value)
            storage.save()
        else:
            abort(400, description='Not a JSON')
    else:
        abort(404)
    return jsonify(city.to_dict()), 200
