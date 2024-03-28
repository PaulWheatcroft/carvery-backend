from flask import Flask, request
from flask_cors import CORS

from restaurants import (
    add_restaurant,
    delete_restaurant,
    get_restaurants,
    update_restaurant,
)

from users import (
    add_user,
    get_users,
    delete_user,
    update_user,
    get_user_details,
)

from scores import (
    add_scores,
    delete_score,
    get_all_scores,
    get_score_averages_for_each_restaurant,
    get_scores_for_user,
    get_scores_for_restaurant,
    get_score_averages_for_restaurant,
)

app = Flask(__name__)
CORS(app, origins=['http://localhost:3000'])  # Set the allowed origin


@app.route('/add-user', methods=['POST'])
def add_user_endpoint():
    data = request.json
    result = add_user(data)
    return result


@app.route('/users', methods=['GET'])
def get_users_endpoint():
    result = get_users()
    return result


@app.route('/delete-user/<int:user_id>', methods=['DELETE'])
def delete_user_endpoint(user_id):
    result = delete_user(user_id)
    return result


@app.route('/update-user/<int:user_id>', methods=['PUT'])
def update_user_endpoint(user_id):
    data = request.json
    result = update_user(user_id, data)
    return result


@app.route('/users/<string:user_id>', methods=['GET'])
def get_user_details_endpoint(user_id):
    result = get_user_details(user_id)
    return result


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


@app.route('/all-scores', methods=['GET'])
def get_all_scores_endpoint():
    result = get_all_scores()
    return result


@app.route('/add-scores', methods=['POST'])
def add_scores_endpoint():
    data = request.json
    result = add_scores(**data)
    return result


@app.route('/user-scores/<string:user_id>', methods=['GET'])
def get_scores_for_user_endpoint(user_id):
    result = get_scores_for_user(user_id)
    return result


@app.route('/restaurant-scores/<int:restaurant_id>', methods=['GET'])
def get_scores_for_restaurant_endpoint(restaurant_id):
    result = get_scores_for_restaurant(restaurant_id)
    return result


@app.route('/score-averages/<int:restaurant_id>', methods=['GET'])
def get_score_totals_for_restaurant_endpoint(restaurant_id):
    result = get_score_averages_for_restaurant(restaurant_id)
    return result


@app.route('/all-score-averages', methods=['GET'])
def get_score_totals_for_each_restaurant_endpoint():
    result = get_score_averages_for_each_restaurant()
    return result


@app.route('/delete-score/<int:score_id>/<int:user_id>', methods=['DELETE'])
def delete_score_endpoint(score_id, user_id):
    result = delete_score(score_id, user_id)
    return result


if __name__ == '__main__':
    app.run()
