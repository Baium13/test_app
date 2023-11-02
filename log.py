import json
from datetime import datetime

from flask import Flask, request, jsonify, render_template, make_response, redirect

app = Flask(__name__)
app.secret_key = '1'
all_users = {}
sessions = {}


def read_users():
    with open('users.json') as f:
        users = json.load(f)

        for user in users:
            all_users.update({user['username']: user['password']})


@app.route('/login', methods=['POST'])
def login():
    response_type = "JSON"
    if request.form:
        data = request.form
        response_type = "FORM"
    else:
        data = request.get_json()
    response = None
    if not data or 'username' not in data or 'password' not in data:
        response = jsonify({'error': 'Login failed'}), 400

    username = data['username']
    password = data['password']

    try:
        if all_users[username] == password:
            response = jsonify({'message': 'Login successful OK'}), 200
            sessions.update({str(hash(username)): {"username": username, "login_date": datetime.now()}})
    except KeyError:
        pass
    if response is None:
        response = jsonify({'error': 'Login failed'}), 401
    if response_type == "JSON":
        resp = make_response(response[0], response[1])
        if response[1] == 200:
            resp.set_cookie("session", str(hash(username)), max_age=3600)
        return resp
    if response[1] == 200:
        error_message = "Login succeeded with code 200"
    else:
        error_message = f"Login failed with code {response[1]}"
    if response[1] == 200:
        resp = redirect("/welcome")
        resp.set_cookie("session", str(hash(username)), max_age=3600)
        return resp
    return make_response(render_template("login.html", error=error_message), response[1])


@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    email = request.form['email']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    date_of_birth = request.form['date_of_birth']
    user_data = {
        'username': username,
        'password': password,
        'email': email,
        'first_name': first_name,
        'last_name': last_name,
        'date_of_birth': date_of_birth
    }

    with open("users.json", "r") as file:
        data = json.load(file)
        data.append(user_data)
    with open("users.json", "w") as file:
        json.dump(data, file, indent=2)

    sessions.update({str(hash(username)): {"username": username, "login_date": datetime.now()}})
    resp = redirect("/welcome")
    resp.set_cookie("session", str(hash(username)), max_age=3600)
    read_users()
    return resp


@app.route('/login', methods=['GET'])
def get_login_form():
    if request.cookies.get("session") in sessions:
        return redirect("/welcome")
    return render_template('login.html')


@app.route('/register', methods=['GET'])
def get_register_form():
    if request.cookies.get("session") in sessions:
        return redirect("/welcome")
    return render_template("registration_form.html")


@app.route('/welcome', methods=['GET'])
def welcome():
    if request.cookies.get("session") not in sessions:
        return redirect("/login")
    return render_template("welcome.html", username=sessions[request.cookies["session"]]["username"])


@app.route('/logout', methods=['GET'])
def get_logout():
    resp = make_response(render_template("logout.html"))
    resp.set_cookie("session", "", max_age=0)

    return resp


if __name__ == '__main__':
    read_users()
    app.run()


"""
Implement registration form with following fields:
username:
password:
email:
first name:
last name:
date fo birth:

After registration user must be logged in automatically and his credentials + data are stored in the file

Implement logout button in welcome.html when you click it it will log you out.
"""
