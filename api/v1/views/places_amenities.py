#!/usr/bin/python3
"""
A view for Place - Amenity objects that handles all default RESTFul API actions
"""
from flask import jsonify, abort
from api.v1.views import app_views
import os
from models import storage
from models.place import Place
from models.amenity import Amenity


@app_views.route('places/<place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def get_amenities_by_place(place_id):
    """retrieves the list of all amenities of a place"""
    place = storage.get(Place, place_id)
    if place:
        if os.environ.get('HBNB_TYPE_STORAGE') == "db":
            amenities = [amenity.to_dict() for amenity in place.amenities]
        else:
            amenities = [storage.get(Amenity, amenity_id).to_dict()
                         for amenity_id in place.amenity_ids]
        return jsonify(amenities)
    else:
        abort(404)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_place_amenity(place_id, amenity_id):
    """deletes an amenity of a place"""
    place = storage.get(Place, place_id)
    if place:
        amenity = storage.get(Amenity, amenity_id)
        if amenity:
            if os.environ.get('HBNB_TYPE_STORAGE') == "db":
                if amenity not in place.amenities:
                    abort(404)
                place.amenities.remove(amenity)
            else:
                if amenity_id not in place.amenity_ids:
                    abort(404)
                place.amenity_ids.remove(amenity_id)

            storage.save()
            return jsonify({})
        else:
            abort(404)
    else:
        abort(404)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['POST'], strict_slashes=False)
def link_amenity_place(place_id, amenity_id):
    """link an amenity to a place"""
    place = storage.get(Place, place_id)
    if place:
        amenity = storage.get(Amenity, amenity_id)
        if amenity:
            if os.environ.get('HBNB_TYPE_STORAGE') == "db":
                if amenity in place.amenities:
                    return jsonify(amenity.to_dict()), 200
                else:
                    place.amenities.append(amenity)
            else:
                if amenity_id in place.amenity_ids:
                    return jsonify(amenity.to_dict()), 200
                else:
                    place.amenity_ids.append(amenity_id)

            storage.save()
            return jsonify(amenity.to_dict()), 201
        else:
            abort(404)
    else:
        abort(404)
