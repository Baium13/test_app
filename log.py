import json

from flask import Flask, render_template, request, redirect, url_for, session, make_response

app = Flask(__name__)
app.secret_key = 'my_key'
all_users = {}


def read_file():
    with open('users.json') as f:
        users = json.load(f)
        for user in users:
            all_users.update({user['username']: user['password']})


def login(username, password):
    if username in all_users and all_users[username] == password:
        return True
    else:
        return False


@app.route('/', methods=['GET'])
def web():
    return render_template('web.html')


@app.route('/login', methods=['GET', 'POST'])
def login_form():
    read_file()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if login(username, password):
            session['username'] = username
            return redirect(url_for('welcome'))
        else:
            return 'Login failed. Please try again.'

    if 'username' in session:
        return f'You are already logged in as {session["username"]}. <a href="/logout">Logout</a>'

    return render_template('login.html')


@app.route('/register', methods=['POST'])
def registration():
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
    session['username'] = username
    response = make_response(redirect(url_for('welcome')))
    response.set_cookie('username', username)
    return response


@app.route('/register', methods=['GET'])
def get_welcome_form_after_registration():
    if 'username' in session:
        return redirect(url_for('welcome'))
    return render_template("registration_form.html")


@app.route('/welcome', methods=['GET'])
def welcome():
    if 'username' in session:
        return render_template('welcome.html', username=session['username'])
    return redirect(url_for('/login'))


@app.route('/logout', methods=['GET'])
def logout():
    session.pop('username', None)
    return render_template('logout.html')


if __name__ == '__main__':
    app.run()
