from flask import request, jsonify
import sqlite3


def add_restaurant(data):
    data = request.json
    name = data.get('name')
    line1_address = data.get('line1_address', None)
    line2_address = data.get('line2_address', None)
    city = data.get('city')
    county = data.get('county')
    post_code = data.get('post_code')
    country = data.get('country')

    if not name or not city or not county or not post_code or not country:
        return jsonify({'error': 'Missing required fieldz'}), 400

    conn = sqlite3.connect('./carvery.db')
    cursor = conn.cursor()

    cursor.execute(
        """INSERT INTO restaurants
        (name, line1_address, line2_address, city, county, post_code, country)
        VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (
            name,
            line1_address or None,
            line2_address or None,
            city,
            county,
            post_code,
            country,
        ),
    )
    conn.commit()

    conn.close()

    return jsonify({'message': 'Restaurant added successfully'}), 201


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


def update_restaurant(restaurant_id, data):
    data = request.json
    name = data.get('name')
    line1_address = data.get('line1_address', None)
    line2_address = data.get('line2_address', None)
    city = data.get('city')
    county = data.get('county')
    post_code = data.get('post_code')
    country = data.get('country')

    if not name or not city or not county or not post_code or not country:
        return jsonify({'error': 'Missing required fieldz'}), 400

    conn = sqlite3.connect('./carvery.db')
    cursor = conn.cursor()

    cursor.execute(
        """UPDATE restaurants
        SET name = ?, line1_address = ?, line2_address = ?, city = ?,
        county = ?, post_code = ?, country = ?
        WHERE id = ?""",
        (
            name,
            line1_address or None,
            line2_address or None,
            city,
            county,
            post_code,
            country,
            restaurant_id,
        ),
    )
    conn.commit()

    conn.close()

    return jsonify({'message': 'Restaurant updated successfully'}), 200


def delete_restaurant(restaurant_id):
    conn = sqlite3.connect('./carvery.db')
    cursor = conn.cursor()

    cursor.execute("DELETE FROM restaurants WHERE id = ?", (restaurant_id,))
    conn.commit()

    conn.close()

    return jsonify({'message': 'Restaurant deleted successfully'}), 200
