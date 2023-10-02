#!/usr/bin/python3
"""return places(s)"""
from api.v1.views import app_views
from models import storage
from models.city import City
from models.place import Place
import json
import flask
from flask import abort, jsonify


@app_views.route('/cities/<city_id>/places',
                 methods=['GET'],
                 strict_slashes=False)
def places(city_id):
    """retrieves a specific city object"""
    cities = storage.all(Place)
    if cities is None:
        abort(404)
    else:
        plcs = []
        for city in cities:
            if cities[city].to_dict().get('city_id') == city_id:
                plcs.append(cities[city].to_dict())
    if plcs == []:
        abort(404)
    return jsonify(plcs), 200


@app_views.route('/places/<place_id>',
                 methods=['GET'],
                 strict_slashes=False)
def get_place(place_id):
    place = storage.get(Place, place_id)
    if place:
        return jsonify(place.to_dict()), 200
    else:
        abort(404)


@app_views.route('/places/<place_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    place = storage.get(Place, place_id)
    if place:
        storage.delete(place)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/cities/<city_id>/places',
                 methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    req = flask.request.get_json()
    city = storage.get(City, city_id)
    if req:
        if req.get("name"):
            if req.get("user_id"):
                if city:
                    r = Place()
                    r.city_id = city_id
                    for key[0] in req.items():
                        setattr(r, key[0], key[1])
                    storage.new(r)
                    storage.save()
                else:
                    abort(404)
            else:
                abort(400, {'Missing user_id'})
        else:
            abort(400, {'Missing name'})
    else:
        abort(400, {"Not a JSON"})
    return jsonify(r.to_dict()), '201'


@app_views.route('/places/<place_id>',
                 methods=['PUT'],
                 strict_slashes=False)
def update_place(place_id):
    req = flask.request.get_json()
    place = storage.get(Place, place_id)
    if place:
        req = flask.request.get_json()
        if req:
            ignoreKeys = ['id', 'created_at', 'user_id', 'city_id', 'updated_at']
            for key in req.items():
                if key[0] not in ignoreKeys:
                    setattr(place, key[0], key[1])
            storage.save()
        else:
            abort(400, {"Not a JSON"})
    else:
        abort(404)
    return jsonify(place.to_dict()), '200'
