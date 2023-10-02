#!/usr/bin/python3
"""return states(s)"""
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
import json
import flask
from flask import abort, jsonify


@app_views.route('/amenities',
                 methods=['GET'],
                 strict_slashes=False)
def amenities():
    """retrieves a specific state object"""
    amenities = storage.all(Amenity)
    if amenities is None:
        abort(404)
    else:
        amens = []
        for amenity in amenities:
            amens.append(amenities[amenity].to_dict())
        return jsonify(amens), 200


@app_views.route('/amenities/<amenity_id>',
                 methods=['GET'],
                 strict_slashes=False)
def get_amenity(amenity_id):
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        return jsonify(amenity.to_dict()), 200
    else:
        abort(404)


@app_views.route('/amenities/<amenity_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        storage.delete(amenity)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/amenities',
                 methods=['POST'],
                 strict_slashes=False)
def create_amenity():
    req = flask.request.get_json()
    if req:
        if req.get("name"):
            r = Amenity()
            r.name = req.get("name")
            storage.new(r)
            storage.save()
            return jsonify(r.to_dict()), '201'
        else:
            abort(400, {'Missing name'})
    else:
        abort(400, {"Not a JSON"})


@app_views.route('/amenities/<amenity_id>',
                 methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    req = flask.request.get_json()
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        req = flask.request.get_json()
        if req:
            ignoreKeys = ['id', 'created_at', 'updated_at']
            for key in req.items():
                if key[0] not in ignoreKeys:
                    setattr(amenity, key[0], key[1])
            storage.save()
        else:
            abort(400, {"Not a JSON"})
    else:
        abort(404)
    return jsonify(amenity.to_dict()), '200'
