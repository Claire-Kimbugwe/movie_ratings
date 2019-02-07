"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash, session)
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Ratings, Movie,connect_to_db, db


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""
    return render_template("homepage.html")


@app.route("/users")
def user_list():
    """Show list of users."""


    users = User.query.all()
    return render_template("user_list.html", users=users)

@app.route("/register")
def get_user_login_info():
    """Show  user registration  page ."""
    
    return render_template("registration.html")


@app.route("/registered", methods = ["POST"])
def register_user():
    """Show  user registration  page ."""
    user_email = request.form.get('email')
    password = request.form.get('pw')

    user = User.query.filter_by(email = user_email).first()

    if user != None:
        return redirect('user_login.html')

    else:
        user = User(email= user_email,password=password)

        db.session.add(user)
        db.session.commit()
    
    
    return redirect("/")

@app.route("/user_login")
def login_user():
    """Allow existing user to login ."""
    
    return render_template("user_login.html")


@app.route("/user_login", methods = ["POST"])
def verify_user_login():
    """make sure that password is correct."""

    user_email = request.form.get('user_email')
    password = request.form.get('password')


    if user_email != User.query.filter_by(email = user_email).first():
        flash("Email not  please try again")

    if password != User.query.filter_by(password = password).first():
        flash("Wrong password please try again")







if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
