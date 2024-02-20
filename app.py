from flask import Flask, request

from restaurants import (
    add_restaurant,
    delete_restaurant,
    get_restaurants,
    update_restaurant,
)

app = Flask(__name__)


@app.route('/add-restaurant', methods=['POST'])
def add_restaurant_endpoint():
    data = request.json
    result = add_restaurant(data)
    return result


@app.route('/update-restaurant/<int:restaurant_id>', methods=['PUT'])
def update_restaurant_endpoint(restaurant_id):
    data = request.json
    result = update_restaurant(restaurant_id, data)
    return result


@app.route('/delete-restaurant/<int:restaurant_id>', methods=['DELETE'])
def delete_restaurant_endpoint(restaurant_id):
    result = delete_restaurant(restaurant_id)
    return result


@app.route('/restaurants', methods=['GET'])
def get_restaurants_endpoint():
    result = get_restaurants()
    return result


if __name__ == '__main__':
    app.run()
