import sqlite3
from flask import jsonify


def add_scores(
    locations,
    parking,
    meat,
    roast_potatoes,
    cauliflower_cheese,
    veg,
    ambience,
    customer_service,
    overall_value,
    user_id,
    restaurant_id,
    date,
    price,
):
    conn = sqlite3.connect('./carvery.db')
    cursor = conn.cursor()

    try:
        cursor.execute(
            """INSERT INTO scores (locations, parking, meat, roast_potatoes,
            cauliflower_cheese, veg, ambience, customer_service, overall_value,
            user_id, restaurant_id, date, price)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                locations,
                parking,
                meat,
                roast_potatoes,
                cauliflower_cheese,
                veg,
                ambience,
                customer_service,
                overall_value,
                user_id,
                restaurant_id,
                date,
                price,
            ),
        )
        conn.commit()
        conn.close()
        return jsonify({'message': 'Scores added successfully'}), 200
    except Exception as e:
        conn.rollback()
        conn.close()
        return (
            jsonify({'error': 'Failed to add scores', 'details': str(e)}),
            500,
        )


def get_scores_for_user(user_id):
    conn = sqlite3.connect('./carvery.db')
    cursor = conn.cursor()

    print(user_id)

    # Get scores for the resolved user ID
    cursor.execute("SELECT * FROM scores WHERE user_id = ?", (user_id,))
    scores = cursor.fetchall()
    conn.close()

    # Convert scores to JSON format
    score_list = []
    for score in scores:
        score_item = {
            'id': score[0],
            'locations': score[1],
            'parking': score[2],
            'meat': score[3],
            'roast_potatoes': score[4],
            'cauliflower_cheese': score[5],
            'veg': score[6],
            'ambience': score[7],
            'customer_service': score[8],
            'overall_value': score[9],
            'user_id': score[10],
            'restaurant_id': score[11],
            'date': score[12],
            'price': score[13],
        }
        score_list.append(score_item)

    return jsonify({'scores': score_list}), 200


def get_scores_for_restaurant(restaurant_id):
    conn = sqlite3.connect('./carvery.db')
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM scores WHERE restaurant_id = ?", (restaurant_id,)
    )
    scores = cursor.fetchall()
    conn.close()

    score_list = []
    for score in scores:
        score_item = {
            'id': score[0],
            'locations': score[1],
            'parking': score[2],
            'meat': score[3],
            'roast_potatoes': score[4],
            'cauliflower_cheese': score[5],
            'veg': score[6],
            'ambience': score[7],
            'customer_service': score[8],
            'overall_value': score[9],
            'user_id': score[10],
            'restaurant_id': score[11],
            'date': score[12],
            'price': score[13],
        }
        score_list.append(score_item)

    return jsonify({'scores': score_list}), 200


def delete_score(score_id, user_id):
    conn = sqlite3.connect('./carvery.db')
    cursor = conn.cursor()

    # Check if the user's ID matches the user_id in the scores entry
    cursor.execute("SELECT user_id FROM scores WHERE id = ?", (score_id,))
    existing_user_id = cursor.fetchone()
    if existing_user_id and existing_user_id[0] == user_id:
        # If the user's ID matches, delete the score
        cursor.execute("DELETE FROM scores WHERE id = ?", (score_id,))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Score deleted successfully'}), 200
    else:
        conn.close()
        return (
            jsonify(
                {
                    'error': 'Score with the specified ID does not exist or does not belong to the user'
                }
            ),
            404,
        )


def get_all_scores():
    conn = sqlite3.connect('./carvery.db')
    cursor = conn.cursor()

    cursor.execute(
        """SELECT scores.*, restaurants.name FROM scores JOIN restaurants ON
        scores.restaurant_id = restaurants.id ORDER BY scores.date DESC"""
    )
    scores = cursor.fetchall()
    conn.close()

    score_list = []
    for score in scores:
        score_item = {
            'id': score[0],
            'locations': score[1],
            'parking': score[2],
            'meat': score[3],
            'roast_potatoes': score[4],
            'cauliflower_cheese': score[5],
            'veg': score[6],
            'ambience': score[7],
            'customer_service': score[8],
            'overall_value': score[9],
            'user_id': score[10],
            'restaurant_id': score[11],
            'restaurant_name': score[14],
            'date': score[12],
            'price': score[13],
        }
        score_list.append(score_item)

    return jsonify({'results': len(score_list)}, {'scores': score_list}), 200


def get_score_averages_for_restaurant(restaurant_id):
    conn = sqlite3.connect('./carvery.db')
    cursor = conn.cursor()

    print(restaurant_id)

    cursor.execute(
        """SELECT
        AVG(locations) AS average_location,
        AVG(parking) AS average_parking,
        AVG(meat) AS average_meat,
        AVG(roast_potatoes) AS average_roast_potatoes,
        AVG(cauliflower_cheese) AS average_cauliflower_cheese,
        AVG(veg) AS average_veg,
        AVG(ambience) AS average_ambience,
        AVG(customer_service) AS average_customer_service,
        AVG(overall_value) AS average_overall_value
    FROM scores
    WHERE restaurant_id = ?""",
        (restaurant_id,),
    )

    averages = cursor.fetchone()
    conn.close()

    if averages:
        total_average = sum(averages)
        averages_dict = {
            'averages': {
                'locations': averages[0],
                'parking': averages[1],
                'meat': averages[2],
                'roast_potatoes': averages[3],
                'cauliflower_cheese': averages[4],
                'veg': averages[5],
                'ambience': averages[6],
                'customer_service': averages[7],
                'overall_value': averages[8],
                'total_average': total_average,
            }
        }
        return jsonify(averages_dict), 200
    else:
        return jsonify({'error': 'No scores found for this restaurant'}), 404


def get_score_averages_for_each_restaurant():
    conn = sqlite3.connect('./carvery.db')
    cursor = conn.cursor()

    cursor.execute(
        """SELECT r.id, r.name, r.line1_address, r.line2_address, r.city,
        r.county, r.post_code, r.country,
        AVG(s.locations) AS average_location,
        AVG(s.parking) AS average_parking,
        AVG(s.meat) AS average_meat,
        AVG(s.roast_potatoes) AS average_roast_potatoes,
        AVG(s.cauliflower_cheese) AS average_cauliflower_cheese,
        AVG(s.veg) AS average_veg,
        AVG(s.ambience) AS average_ambience,
        AVG(s.customer_service) AS average_customer_service,
        AVG(s.overall_value) AS average_overall_value,
        AVG(s.overall_food) AS average_overall_food
    FROM scores s
    JOIN restaurants r ON s.restaurant_id = r.id
    GROUP BY s.restaurant_id"""
    )

    averages = cursor.fetchall()
    conn.close()

    if averages:
        averages_list = []
        for average in averages:
            restaurant_details = {
                'id': average[0],
                'name': average[1],
                'address1': average[2],
                'address2': average[3],
                'city': average[4],
                'county': average[5],
                'postcode': average[6],
                'country': average[7],
            }
            total_average = sum(average[8:18])
            average_item = {
                'restaurant_details': restaurant_details,
                'average_location': average[8],
                'average_parking': average[9],
                'average_meat': average[10],
                'average_roast_potatoes': average[11],
                'average_cauliflower_cheese': average[12],
                'average_veg': average[13],
                'average_ambience': average[14],
                'average_customer_service': average[15],
                'average_overall_value': average[16],
                'average_overall_food': average[17],
                'total_average': total_average,
            }
            averages_list.append(average_item)

        return (
            jsonify(
                {'results': len(averages_list)}, {'averages': averages_list}
            ),
            200,
        )
    else:
        return jsonify({'error': 'No scores found in the database'}), 404
