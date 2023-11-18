import sqlite3 as sq
from datetime import timedelta

from flask import Flask, render_template, request, redirect, url_for, session, make_response

app = Flask(__name__)
app.secret_key = 'my_key'


def created_db():
    with sq.connect("myDB.db") as con:
        cur = con.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS user_profile (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        password TEXT,
        email TEXT,
        first_name TEXT,
        last_name TEXT,
        date_of_birth TEXT
        )""")


@app.route('/', methods=['GET'])
def web():
    return render_template('web.html')


@app.route('/login', methods=['GET', 'POST'])
def login_form():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        with sq.connect("myDB.db") as con:
            cur = con.cursor()
            data = cur.execute("SELECT username, password FROM user_profile WHERE username = ? AND password = ?",
                               (username, password)).fetchone()
            if data is not None:
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
    with sq.connect("myDB.db") as con:
        cur = con.cursor()
        cur.execute(
            "INSERT INTO user_profile VALUES(NULL, :username, :password, "
            ":email, :first_name, :last_name, :date_of_birth)",
            (username, password, email, first_name, last_name, date_of_birth))

    session['username'] = username
    response = make_response(redirect(url_for('welcome')))
    response.set_cookie('username', username)
    return response


@app.route('/register', methods=['GET'])
def get_welcome_form_after_registration():
    if 'username' in session:
        return render_template('welcome.html')
    return render_template("registration_form.html")


@app.route('/welcome', methods=['GET'])
def welcome():
    if 'username' in session:
        return render_template('welcome.html', username=session['username'])
    return render_template('/login.html')


@app.route('/logout', methods=['GET'])
def logout():
    session.pop('username', None)
    return render_template('logout.html')


@app.before_request
def session_time():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(hours=1)


if __name__ == '__main__':
    created_db()
    app.run()
