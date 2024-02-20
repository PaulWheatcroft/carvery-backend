from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)


# Define the API endpoint to add a restaurant
@app.route('/add-restaurant', methods=['POST'])
def add_restaurant():
    data = request.json  # Assuming the data is sent in JSON format
    name = data.get('name')
    line1_address = data.get('line1_address', '')
    line2_address = data.get('line2_address', '')
    city = data.get('city')
    county = data.get('county')
    post_code = data.get('post_code')
    country = data.get('country')

    if not name or not city or not county or not post_code or not country:
        return jsonify({'error': 'Missing required fieldz'}), 400

    # Connect to the SQLite database
    conn = sqlite3.connect('./carvery.db')
    cursor = conn.cursor()

    # Insert the new restaurant into the database
    cursor.execute(
        """INSERT INTO restaurants
        (name, line1_address, line2_address, city, county, post_code, country)
        VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (name, line1_address, line2_address, city, county, post_code, country),
    )
    conn.commit()

    conn.close()

    return jsonify({'message': 'Restaurant added successfully'}), 201


@app.route('/restaurants', methods=['GET'])
def get_restaurants():
    conn = sqlite3.connect('./carvery.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM restaurants")
    restaurants = cursor.fetchall()
    conn.close()

    restaurant_list = []
    for restaurant in restaurants:
        restaurant_item = {
            'id': restaurant[0],
            'name': restaurant[1],
            'line1_address': restaurant[2],
            'line2_address': restaurant[3],
            'city': restaurant[4],
            'county': restaurant[5],
            'post_code': restaurant[6],
            'country': restaurant[7],
        }
        restaurant_list.append(restaurant_item)

    return jsonify({'restaurants': restaurant_list}), 200


if __name__ == '__main__':
    app.run()
