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


def get_scores_for_user(user_email):
    conn = sqlite3.connect('./carvery.db')
    cursor = conn.cursor()

    # Resolve user ID from the email
    cursor.execute("SELECT id FROM users WHERE email = ?", (user_email,))
    user_id = cursor.fetchone()
    if user_id is None:
        conn.close()
        return jsonify({'error': 'User not found'}), 404

    # Get scores for the resolved user ID
    cursor.execute("SELECT * FROM scores WHERE user_id = ?", (user_id[0],))
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
