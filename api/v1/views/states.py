#!/usr/bin/python3
"""return states(s)"""
import os
from api.v1.views import app_views
from models import storage
from models.state import State
import json
import flask
from flask import abort, jsonify


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def states():
    """retrieves all states"""
    states_array = []
    states = storage.all(State)
    for sts in states:
        states_array.append(states.get(sts).to_dict())
    return jsonify(states_array), 200


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def state(state_id):
    """retrieves a specific state object"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict()), '200'


@app_views.route('/states/<state_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        state = storage.get(State, state_id)
    else:
        state = storage.get('State', state_id)
    if state:
        storage.delete(state)
        storage.save()
    else:
        abort(404)
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create():
    req = flask.request.get_json()
    if req:
        if req.get("name"):
            r = State()
            r.name = req.get("name")
            storage.new(r)
            storage.save()
        else:
            abort(400, {'Missing name'})
    else:
        abort(400, {"Not a JSON"})
    return jsonify(r.to_dict()), '201'


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update(state_id):
    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        state = storage.get(State, state_id)
    else:
        state = storage.get('State', state_id)
    if state:
        req = flask.request.get_json()
        if req:
            ignoreKeys = ['id', 'created_at', 'updated_at']
            for key in req.items():
                if key[0] not in ignoreKeys:
                    setattr(state, key[0], key[1])
            storage.save()
        else:
            abort(400, {"Not a JSON"})
    else:
        abort(404)
    return jsonify(state.to_dict()), '200'
