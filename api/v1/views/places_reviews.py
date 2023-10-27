#!/usr/bin/python3
"""A view for Review objects that handles all default RESTFul API actions"""
from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.review import Review
from models.place import Place
from models.user import User


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_reviews(place_id):
    """retrieves the list of all reviews of a place"""
    place = storage.get(Place, place_id)
    if place:
        reviews = place.reviews
        review_list = [review.to_dict() for review in reviews]
        return jsonify(review_list)
    else:
        abort(404)


@app_views.route('/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def get_review(review_id):
    """retrieves a review by id"""
    review = storage.get(Review, review_id)
    if review:
        return jsonify(review.to_dict())
    else:
        abort(404)


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """deletes a Review by id"""
    review = storage.get(Review, review_id)
    if review:
        storage.delete(review)
        storage.save()
        return jsonify({})
    else:
        abort(404)


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """creates a new review"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400
    if "user_id" not in data:
        return jsonify({"error": "Missing user_id"}), 400
    if "text" not in data:
        return jsonify({"error": "Missing text"}), 400

    user = storage.get(User, data["user_id"])
    if not user:
        abort(404)

    new_review = Review(**data)
    new_review.place_id = place_id
    new_review.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def update_review(review_id):
    """updates a review by id"""
    review = storage.get(Review, review_id)
    if review:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Not a JSON"}), 400
        for key, value in data.items():
            if key not in ['id', 'user_id', 'place_id', 'created_at',
                           'updated_at']:
                setattr(review, key, value)
        review.save()
        return jsonify(review.to_dict())
    else:
        abort(404)
