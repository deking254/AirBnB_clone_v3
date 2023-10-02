#!/usr/bin/python3
"""View for linking Place objects and Amenity objects"""
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.amenity import Amenity
from flask import jsonify, abort, request

@app_views.route('/places/<place_id>/amenities', methods=['GET'], strict_slashes=False)
def list_place_amenities(place_id):
    """Lists all amenities of a Place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    
    amenities = [amenity.to_dict() for amenity in place.amenities]
    return jsonify(amenities), 200

@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place_amenity(place_id, amenity_id):
    """Deletes a link between Place and Amenity"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    
    if amenity not in place.amenities:
        abort(404)
    
    place.amenities.remove(amenity)
    storage.save()
    return jsonify({}), 200

@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['POST'],
                 strict_slashes=False)
def link_place_amenity(place_id, amenity_id):
    """Links an Amenity to a Place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    
    if amenity in place.amenities:
        return jsonify(amenity.to_dict()), 200
    
    place.amenities.append(amenity)
    storage.save()
    return jsonify(amenity.to_dict()), 201