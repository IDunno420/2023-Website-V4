# Imports section
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
# End imports

db = SQLAlchemy() # Defines the database to use SQL Alchemy
DB_NAME = "database.db" # Defines the databases' name


def create_app():
    app = Flask(__name__) # Defines app
    app.config['SECRET_KEY'] = "kkMSAHg7Y27TbfXkObNVSqPeDNVOA7ym" # Secret key for the website
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}' 
    # Creates and defines the database under DB_NAME
    db.init_app(app) # Initalises the app

    # Imports Section
    from .views import views
    from .auth import auth
    # End imports

    app . register_blueprint(views, url_prefix="/") 
    # Register views python file
    app . register_blueprint(auth, url_prefix="/") 
    # Register auth python file

    from .models import User, Post # Imports models

    with app.app_context():
        db.create_all() # Create a new database file
        print("Created Database") 
        # Message to send if successfully creates a new database

    login_manager = LoginManager() 
    login_manager.login_view = "auth.login" 
    login_manager.init_app(app) 

    @login_manager.user_loader


    def load_user(id):
        return User.query.get(int(id))

    return app # Returns the application


def create_database(app):
    if not path.exists("website/ " + DB_NAME): # The path does not exist
        db.create_all(app = app) # Creates a new database file
        print("Created database!") 
        # Message to send if successfully creates a new database