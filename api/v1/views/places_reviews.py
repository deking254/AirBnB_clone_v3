#!/usr/bin/python3
"""return reviews(s)"""
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.user import User
from models.review import Review
import json
import flask
from flask import abort, jsonify


@app_views.route('/places/<place_id>/reviews',
                 methods=['GET'],
                 strict_slashes=False)
def reviews(place_id):
    """retrieves a specific Review object"""
    places = storage.get(Place, place_id)
    reviews = storage.all(Review)
    if places is None:
        abort(404)
    else:
        plcs = []
        for review in reviews:
            if reviews[review].to_dict().get('place_id') == place_id:
                plcs.append(reviews[review].to_dict())
    if plcs == []:
        abort(404)
    return jsonify(plcs), 200


@app_views.route('/reviews/<review_id>',
                 methods=['GET'],
                 strict_slashes=False)
def get_review(review_id):
    review = storage.get(Review, review_id)
    if review:
        return jsonify(review.to_dict()), 200
    else:
        abort(404)


@app_views.route('/reviews/<review_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    review = storage.get(Review, review_id)
    if review:
        storage.delete(review)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/places/<place_id>/reviews',
                 methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    req = flask.request.get_json()
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if req:
        if req.get("text"):
            if req.get("user_id"):
                user = storage.get(User, req.get("user_id"))
                if user:
                    r = Review()
                    r.place_id = place_id
                    for key in req.items():
                        setattr(r, key[0], key[1])
                    storage.new(r)
                    storage.save()
                else:
                    abort(404)
            else:
                abort(400, {'Missing user_id'})
        else:
            abort(400, {'Missing text'})
    else:
        abort(400, {"Not a JSON"})
    return jsonify(r.to_dict()), '201'


@app_views.route('/reviews/<review_id>',
                 methods=['PUT'],
                 strict_slashes=False)
def update_review(review_id):
    req = flask.request.get_json()
    review = storage.get(Review, review_id)
    if review:
        req = flask.request.get_json()
        if req:
            ignoreKeys = ['id',
                          'created_at',
                          'user_id',
                          'place_id',
                          'updated_at']
            for key in req.items():
                if key[0] not in ignoreKeys:
                    setattr(review, key[0], key[1])
            storage.save()
        else:
            abort(400, {"Not a JSON"})
    else:
        abort(404)
    return jsonify(review.to_dict()), '200'
