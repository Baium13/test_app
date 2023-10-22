import json

from flask import Flask, request, jsonify

log = Flask(__name__)

with open('login.jason') as f:
    users = json.load(f)


@log.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    if not data or 'username' not in data or 'password' not in data:
        return jsonify({'error': 'Login failed'}), 400

    username = data['username']
    password = data['password']

    for user in users:
        if user['username'] == username and user['password'] == password:
            return jsonify({'message': 'Login successful OK'})

    return jsonify({'error': 'Login failed'}), 401


if __name__ == '__main__':
    log.run()
