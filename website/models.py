# Imports Section
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
# End imports

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True) 
    # Sets an ID for the comment that is unqiue in the database for the user
    email = db.Column(db.String(150), unique = True) 
    # The email must be unique with a max length of 150
    username = db.Column(db.String(150), unique = True) 
    # The username must be unqiue and has a max length of 150
    password = db.Column(db.String(150)) 
    # The password must have a maximum length of 150
    image_file = db.Column(db.String(20), nullable = False,
    default = 'default.jpg') 
    # Image file cannot be left empty and defaults to default.jpg
    date_created = db.Column(db.DateTime(timezone = True),
    default = func.now()) 
    # Uses the users timezone to set a date of
    # when the users account was created
    posts = db.relationship('Post', backref = 'user', passive_deletes = True) 
    # The total amount of posts that the user has made and can be deleted
    comments = db.relationship('Comment', backref = 'user',
    passive_deletes = True) 
    # The total amount of comments that the user has made and can be deleted
    likes = db.relationship('Like', backref = 'user', passive_deletes = True) 
    # The total amount of likes that the user has made and can be deleted


class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True) 
    # Sets an ID for the comment that is unqiue in the database for the post
    text = db.Column(db.Text, nullable = False) 
    # Defines that the post must be text and not nullable (empty)
    date_created = db.Column(db.DateTime(timezone = True),
    default = func.now()) 
    # Uses the timezone to create a date of creation
    author = db.Column(db.Integer, db.ForeignKey(
    'user.id', ondelete = "CASCADE"), nullable = False) 
    # Uses the users ID to define them as the author of the post
    comments = db.relationship('Comment', backref = 'post',
    passive_deletes = True) 
    # Allows comments to be made with passive deletions
    likes = db.relationship('Like', backref = 'post', passive_deletes = True) 
    # Allows like to be made with passive deletions


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key = True) 
    # Sets an ID for the comment that is unqiue in the database for the comment
    text = db.Column(db.String(200), nullable = False) 
    # Sets a maximum length of the text in a comment and cannot be left empty
    date_created = db.Column(db.DateTime(timezone = True),
    default = func.now()) 
    # Uses the users timezone to be able to 
    #create a date of when the comment was made
    author = db.Column(db.Integer, db.ForeignKey(
    'user.id', ondelete = "CASCADE"), nullable = False) 
    # Creates a author of the comment using their user ID and allows deletion
    post_id = db.Column(db.Integer, db.ForeignKey(
    'post.id', ondelete = "CASCADE"), nullable = False) 
    # Sets a post ID for the comment and allows for deletion


class Like(db.Model):
    id = db.Column(db.Integer, primary_key = True) 
    # Sets an ID for the comment that is unqiue in the database for the like
    date_created = db.Column(db.DateTime(timezone = True),
    default = func.now()) 
    # Uses the users timezone to set a date of when the post was liked
    author = db.Column(db.Integer, db.ForeignKey(
    'user.id', ondelete = "CASCADE"), nullable = False) 
    # Creates a author of the comment using their user ID and allows deletion
    post_id = db.Column(db.Integer, db.ForeignKey(
    'post.id', ondelete = "CASCADE"), nullable = False) 
    # Sets a post ID for the like and allows for deletion
