from datetime import timedelta

import psycopg2
from flask import Flask, render_template, request, redirect, url_for, session, make_response

app = Flask(__name__)
app.secret_key = 'my_key'


def sql_select(sql_query, *args):
    conn = psycopg2.connect(dbname="test", user="postgres", password="postgres", host='localhost')

    # Open a cursor to perform database operations
    cur = conn.cursor()
    cur.execute(sql_query, args)
    result = cur.fetchone()
    cur.close()
    conn.close()
    return result


def sql_update(sql_query, *args):
    conn = psycopg2.connect(dbname="test", user="postgres", password="postgres", host='localhost')
    cur = conn.cursor()
    cur.execute(sql_query, args)
    conn.commit()
    cur.close()
    conn.close()


def created_db():
    sql_update("""CREATE TABLE IF NOT EXISTS user_profile (
        user_id SERIAL PRIMARY KEY,
        username TEXT NOT NULL UNIQUE,
        password TEXT,
        email TEXT NOT NULL UNIQUE,
        first_name TEXT,
        last_name TEXT,
        date_of_birth TEXT
        )""")


def get_user(username, email=None):
    return sql_select('SELECT * FROM user_profile WHERE username = %s OR email = %s', username, email)


@app.route('/', methods=['GET'])
def web():
    return render_template('web.html')


@app.route('/login', methods=['GET', 'POST'])
def login_form():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        data = get_user(username, password)
        if data is not None and data[2] == password:
            session['username'] = username
            return redirect(url_for('welcome'))
        else:
            return render_template('login.html', error='Login failed. Please try again.')
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
    data = get_user(username, email)
    if data:
        return render_template('registration_form.html', error='This username or email already used')
    sql_update("INSERT INTO user_profile (username, password, "
               "email, first_name, last_name, date_of_birth) VALUES (%s, %s, %s, %s, %s, %s)", username, password,
               email, first_name,
               last_name, date_of_birth)

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
