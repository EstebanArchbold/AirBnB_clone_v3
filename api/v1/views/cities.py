#!/usr/bin/python3
"""Contains cities module"""
from flask import Flask, Blueprint
from flask import abort, make_response
from flask import jsonify, request
from api.v1.views import app_views
from models import storage, state, city
from models.amenity import Amenity


@app_views.route('/cities',
                 methods=['GET'],
                 strict_slashes=False)
def cities():
    """Cities handles all default RestFul API actions"""
    cities = []
    my_cities = storage.all('City').values()
    for my_city in my_cities:
        cities.append(my_city.to_dict())
    return jsonify(cities)


@app_views.route('/states/<string:state_id>/cities',
                 methods=['GET'],
                 strict_slashes=False)
def cities_state_id(state_id):
    """Retrieve an object into a valid JSON"""
    cities = []
    my_state = storage.get('State', state_id)
    if my_state is None:
        abort(404)
    for my_city in my_state.cities:
        cities.append(my_city.to_dict())
    return jsonify(cities)


@app_views.route('/cities/<string:city_id>',
                 methods=['GET'],
                 strict_slashes=False)
def city_id(city_id):
    """Retrieve an object into a valid JSON"""
    my_city = storage.get('City', city_id)
    if my_city is None:
        abort(404)
    return jsonify(my_city.to_dict())


@app_views.route('/cities/<string:city_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def city_id_delete(city_id):
    """Deletes a City object by id"""
    my_city = storage.get('City', city_id)
    if my_city is None:
        abort(404)
    my_city.delete()
    storage.save()
    return jsonify({})


@app_views.route('states/<state_id>/cities',
                 methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """Returns the new State with the status code 201"""
    my_state = storage.get('State', state_id)
    if my_state is None:
        abort(404)
    if not request.json:
        abort(400, 'Not a JSON')
    if 'name' not in request.json:
        abort(400, 'Missing name')
    my_city = city.City(name=request.json.get('name', ""), state_id=state_id)
    storage.new(my_city)
    my_city.save()
    return make_response(jsonify(my_city.to_dict()), 201)


@app_views.route('/cities/<string:city_id>',
                 methods=['PUT'],
                 strict_slashes=False)
def update_city(city_id):
    """Returns the State object with the status code 200"""
    my_city = storage.get('City', city_id)
    if my_city is None:
        abort(404)
    if not request.json:
        abort(400, 'Not a JSON')
    for req in request.json:
        if req not in ['id', 'created_at', 'updated_at']:
            setattr(my_city, req, request.json[req])
    my_city.save()
    return jsonify(my_city.to_dict())


if __name__ == "__main__":
    pass
