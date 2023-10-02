#!/usr/bin/python3
"""return states(s)"""
from api.v1.views import app_views
from models import storage
from models.state import State
from models.user import User
from models.user import User
import json
import flask
from flask import abort, jsonify


@app_views.route('/users',
                 methods=['GET'],
                 strict_slashes=False)
def users():
    """retrieves a specific state object"""
    users = storage.all(User)
    if users is None:
        abort(404)
    else:
        amens = []
        for user in users:
            amens.append(users[user].to_dict())
        return jsonify(amens), 200


@app_views.route('/users/<user_id>',
                 methods=['GET'],
                 strict_slashes=False)
def get_user(user_id):
    user = storage.get(User, user_id)
    if user:
        return jsonify(user.to_dict()), 200
    else:
        abort(404)


@app_views.route('/users/<user_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    user = storage.get(User, user_id)
    if user:
        storage.delete(user)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/users',
                 methods=['POST'],
                 strict_slashes=False)
def create_user():
    req = flask.request.get_json()
    if req:
        if req.get("email"):
            if req.get('password'):
                r = User()
                r.email = req.get("email")
                r.password = req.get('password')
                if req.get("first_name"):
                    r.first_name = req.get("first_name")
                if req.get("last_name"):
                    r.last_name = req.get("last_name")
                storage.new(r)
                storage.save()
                return jsonify(r.to_dict()), '201'
            else:
                abort(400, {'Missing password'})
        else:
            abort(400, {'Missing email'})
    else:
        abort(400, {"Not a JSON"})


@app_views.route('/users/<user_id>',
                 methods=['PUT'],
                 strict_slashes=False)
def update_user(user_id):
    req = flask.request.get_json()
    user = storage.get(User, user_id)
    if user:
        req = flask.request.get_json()
        if req:
            ignoreKeys = ['id', 'created_at', 'updated_at']
            for key in req.items():
                if key[0] not in ignoreKeys:
                    setattr(user, key[0], key[1])
            storage.save()
        else:
            abort(400, {"Not a JSON"})
    else:
        abort(404)
    return jsonify(user.to_dict()), '200'
