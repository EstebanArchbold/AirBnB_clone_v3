#!/usr/bin/python3
"""Contains users module"""

from flask import jsonify, abort, request, make_response
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route('/users',
                 methods=['GET'],
                 strict_slashes=False)
@app_views.route('/users/<user_id>',
                 methods=['GET'],
                 strict_slashes=False)
def get_user(user_id=None):
    """Retrieves list all User objs or specific User obj"""
    if user_id is None:
        users = [user.to_dict() for user
                 in storage.all("User").values()]
        return jsonify(users)
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def del_user(user_id=None):
    """Deletes a User object"""
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    user.delete()
    storage.save()

    return jsonify({})


@app_views.route('/users',
                 methods=['POST'],
                 strict_slashes=False)
def post_user():
    """Creates a User object"""
    try:
        req = request.get_json()
    except:
        req = None
    if req is None:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'email' not in req:
        return make_response(jsonify({'error': "Missing email"}), 400)
    if 'password' not in req:
        return make_response(jsonify({'error': "Missing password"}), 400)
    user = User(**req)
    user.save()

    return make_response(jsonify(user.to_dict()), 201)


@app_views.route('/users/<user_id>',
                 methods=['PUT'],
                 strict_slashes=False)
def put_user(user_id=None):
    """Updates a User object"""
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    try:
        req = request.get_json()
    except:
        req = None
    if req is None:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for key, val in req.items():
        if key not in ('id', 'email', 'created_at', 'updates_at'):
            setattr(user, key, val)
    user.save()
    return jsonify(user.to_dict())


if __name__ == "__main__":
    pass
