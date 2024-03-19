from flask import request, jsonify
from datetime import datetime
import sqlite3


def add_user(data):
    data = request.json
    id = data.get('id')
    name = data.get('name')
    email = data.get('email')
    created = datetime.now()

    if not name or not email:
        return jsonify({'error': 'Missing required fields'}), 400

    conn = sqlite3.connect('./carvery.db')
    cursor = conn.cursor()

    cursor.execute(
        """INSERT INTO users
        (id, name, email, created)
        VALUES (?, ?, ?, ?)""",
        (
            id,
            name,
            email,
            created,
        ),
    )
    conn.commit()

    conn.close()

    return jsonify({'message': 'User added successfully'}), 201


def get_users():
    conn = sqlite3.connect('./carvery.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    conn.close()

    user_list = []
    for user in users:
        user_item = {
            'id': user[0],
            'name': user[1],
            'email': user[2],
            'created': user[3],
        }
        user_list.append(user_item)

    return jsonify({'users': user_list}), 200


def delete_user(user_id):
    conn = sqlite3.connect('./carvery.db')
    cursor = conn.cursor()

    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    existing_user = cursor.fetchone()

    if existing_user:
        cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
        conn.commit()
        conn.close()
        return jsonify({'message': 'User deleted successfully'}), 200
    else:
        conn.close()
        return (
            jsonify({'error': 'User with the specified ID does not exist'}),
            404,
        )


def update_user(user_id, data):
    data = request.json
    name = data.get('name')
    email = data.get('email')

    if not name or not email:
        return jsonify({'error': 'Missing required fields'}), 400

    conn = sqlite3.connect('./carvery.db')
    cursor = conn.cursor()

    cursor.execute(
        """UPDATE users
        SET name = ?, email = ?
        WHERE id = ?""",
        (
            name,
            email,
            user_id,
        ),
    )
    conn.commit()

    conn.close()

    return jsonify({'message': 'User updated successfully'}), 200


def get_user_details(user_id):
    conn = sqlite3.connect('./carvery.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()

    if not user:
        return jsonify({'error': 'User not found'}), 404

    user_item = {
        'id': user[0],
        'name': user[1],
        'email': user[2],
        'created': user[3],
    }

    return jsonify({'user': user_item}), 200
