from flask import Blueprint, request, redirect, session
from flask import render_template, g, Blueprint
from api.user_api import User, UserDB

user_list_blueprint = Blueprint('user_list_blueprint', __name__)

@user_list_blueprint.route('/signup', methods = ['GET', 'POST'])
def signup():
    """Gets a username and password to add a user to the database."""
    database = UserDB(g.mysql_db, g.mysql_cursor)

    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')

        if database.select_user_by_username(username):
            msg = 'Username has already been taken'
            return redirect('/fail')
        elif not username or not password:
            msg = 'Please enter a username AND password'
            return redirect('/fail')
        else:
            new_user = User(username, password)
            database.insert_user(new_user)
            msg = 'Account creation successful'
            return redirect("/success")

    return render_template('signup.html')


@user_list_blueprint.route('/login', methods =['GET', 'POST'])
def login():
    """Checkes the database after given a username to see if the given password matches what is in the database."""
    database = UserDB(g.mysql_db, g.mysql_cursor)

    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')

        user = database.select_user_by_username(username)
        if user == database.select_user_by_password(password):
            session['loggedin'] = True
            session['id'] = user['user_id']
            session['username'] = user['username']
            msg = 'Login successful'
            return redirect('/success', msg = msg)
        else:
            msg = 'Wrong username or password'
            return redirect('/fail', msg = msg)

    return render_template('login.html')


@user_list_blueprint.route('/fail', methods =['GET', 'POST'])
def fail():
    return render_template('error.html')

@user_list_blueprint.route('/success', methods =['GET', 'POST'])
def success():
    return render_template('success.html')