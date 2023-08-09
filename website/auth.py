# Imports Section
from flask import Blueprint, render_template, redirect, url_for, request, flash
from . import db
from .models import User
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from .forms import RegistrationForm
# End section

auth = Blueprint("auth", __name__) # Defines auth

@auth.route("/login", methods=['GET', 'POST']) 
# Routes the login function with the get and post methods
def login():
    if request.method == 'POST': # Posting information
        email = request.form.get("email") # Defines email through the form
        password = request.form.get("password") 
        # Defines the password through the from

        user = User.query.filter_by(email = email).first() # Defines the user
        if user:
            if check_password_hash(user.password, password): 
            # If the password is valid
                flash("Logged in!" , category = 'success') 
                # Flash success message
                login_user(user , remember = True) # Log in the user
                return redirect(url_for('views.home')) 
                # Redirect the user to the home page
            else: # If the password is incorrect
                flash('Password is incorrect.' , category = 'error') 
                # Return error message
        else: # If the email does not exist
            flash('Email does not exist.' , category = 'error') 
            # Return error message

    return render_template("login.html" , user = current_user) 
    # Render the login page

@auth.route("/sign-up" , methods = ['GET' , 'POST']) 
# Routes the signup with the get and post methods
def sign_up():
    if current_user.is_authenticated: # If the user is authenticated
        return redirect(url_for('home')) # Redirect the user to the home page

    form = RegistrationForm() # Defines the form

    if form.validate_on_submit(): # Validation for the submission to sign-up
        hashed_password = generate_password_hash((form.password.data),
        method = 'sha256') 
        # Generates a value for the password under the method of sha256
        user = User(username=form.username.data, email = form.email.data,
        password = hashed_password) 
        # Defines the user
        db.session.add(user) # Adds the user
        db.session.commit() 
        # Commits the user (and information) to the database
        flash ('Your account has been created') # Flash a success message
        return redirect(url_for('auth.login')) 
        # Redirect the user to the login page

    return render_template('signup.html' , form = form, user = current_user) 
    # Render the signup page


@auth.route('/help') # Sets a route to send the user to the help page
def help():
    return render_template("help.html" , user = current_user) 
    # Takes the user to the help page

@auth.route('/about') # Sets a route to send the user to the about page\
def files():
    return render_template("about.html" , user = current_user) 
    # Takes the user to the file page 

@auth.route("/logout") # Sets a route to logout 
@login_required # Requires the user to be logged in
def logout():
    logout_user() # Logs out the users from their account
    return redirect(url_for("views.home")) 
    # Redirects the user to the home page