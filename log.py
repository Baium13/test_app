from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, redirect, url_for, session, make_response
from sqlalchemy import select

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'my_key'

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80))
    first_name = db.Column(db.String(120))
    last_name = db.Column(db.String(120))
    date_of_birth = db.Column(db.String)


@app.route('/', methods=['GET'])
def web():
    return render_template('web.html')


@app.route('/login', methods=['GET', 'POST'])
def login_form():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users_data = db.session.execute(
            select(User.username, User.password).where(User.username == username, User.password == password))
        users = users_data.fetchone()
        if users is not None:
            session['username'] = username
            return redirect(url_for('welcome'))
        else:
            return render_template('login.html', error='Login failed. Please try again.')
    if 'username' in session:
        return f'You are already logged in as {session["username"]}. <a href="/logout">Logout</a>'
    return render_template('login.html')


@app.route('/register', methods=['POST'])
def registration():
    db.create_all()
    username = request.form['username']
    password = request.form['password']
    email = request.form['email']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    date_of_birth = request.form['date_of_birth']
    try:
        new_user = (
            User(username=username, password=password, email=email, first_name=first_name, last_name=last_name,
                 date_of_birth=date_of_birth))
        db.session.add(new_user)
        db.session.commit()
        session['username'] = username
        response = make_response(redirect(url_for('welcome')))
        response.set_cookie('username', username)
        return response
    except:
        return render_template('registration_form.html', error='This username or email already used')


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
    app.run()