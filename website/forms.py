# Import Section
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField 
from wtforms import SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired
from wtforms.validators import Length, Email, EqualTo, ValidationError
from .models import User
# End Imports

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators = [DataRequired(),
    Length(min = 2 , max = 20)]) # Defines the 
    # username and validates it to require information
    # and a length minimum and maximum
    email = StringField('Email' , validators = [DataRequired() , Email()]) 
    # Defines the email and validates
        # to require information and be a valid email address
    password = PasswordField('Password' , validators = [DataRequired()]) 
    # Defines the password and validates to require data
    confirm_password = PasswordField('Confirm Password',
    validators = [DataRequired() , EqualTo('password')]) 
    # Defines confirm_password and validates
    # to require data and same as the password
    submit = SubmitField('Sign Up') # Submites the information from the form


    def validate_username(self, username):
        user = User.query.filter_by(username = username.data).first() 
        # Defines user and queries the username data
        if user:
            raise ValidationError('That username is already in use, please choose a different username') 
            # If the username is already in use raise an error message


    def validate_email(self, email):
        user = User.query.filter_by(email = email.data).first() 
        # Defines user and queries the email data
        if user:
            raise ValidationError('That email is already in use, please choose a different email to use')
            # If the email is already in use by another account raise error message


class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
    validators = [DataRequired() , Length(min = 2 , max = 20)]) 
    # When updating username 
    # require data to be present along with a
    # min and max length validator reqirements
    email = StringField('Email',
    validators = [DataRequired() , Email()]) 
    # When updating the email the email
    # must have data and a valid email address to be valid
    picture = FileField('Update Profile Picture',
    validators = [FileAllowed(['jpg' , 'png'])]) # Defines the picture
    # of the users profile where the file types
    # allowed are either JPG or PNG files
    submit = SubmitField('Update') # Submit button value (text)


    def validate_username(self, username): # Validating the username
        if username.data != current_user.username:
            user = User.query.filter_by(username = username.data).first() 
            # Define user under the query of username
            if user:
                raise ValidationError('That username is taken. Please choose a different one.') 
                # If the username is already
                # in user raise an error message


    def validate_email(self, email): # Validating the email
        if email.data != current_user.email: 
            user = User.query.filter_by(email = email.data).first() 
            # Define user under the query of the email
            if user:
                raise ValidationError('That email is taken. Please choose a different one.') 
                # If the email is
                # already in use raise an error message