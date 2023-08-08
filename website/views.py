# Import Section #
import os 
from pathlib import Path
from PIL import Image
import secrets
from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from .models import Post, User, Comment, Like
from .forms import RegistrationForm, UpdateAccountForm
from . import db
# End Imports #

views = Blueprint("views", __name__) #Defines views for later use

@views.route("/") # Sets the initial page to load
@views.route("/home") # Home page is the blog
@login_required # User must be logged in
def home(): # Defines home() to be able to render home
    posts = Post.query.all() # queries all available posts
    return render_template("home.html", user=current_user, posts=posts) #

@views.route("/create-post", methods=['GET', 'POST']) # Sets methods and html page to use
@login_required # Login is required for the below to be allowed
def create_post(): 
    if request.method == "POST": # Sets the request method to post
        text = request.form.get('text') # Where the user enters in the post text

        if not text: # Comment must have text else send error
            flash('Post cannot be empty', category='error')
        else: # If the input is valid continue
            post = Post(text=text, author=current_user.id) # Attributes the author of the post
            db.session.add(post) # Adds the post
            db.session.commit() # Commits the text to the database
            flash('Post created!', category='success') # If post is successful flash
            return redirect(url_for('views.home')) # Redirects the user to the views page (home page)

    return render_template('create_post.html', user=current_user) # Renders the create post template

@views.route("/delete-post/<id>") # Sets the route for the deletion of posts under the ID of the post
@login_required # Required the user to be logged in
def delete_post(id): 
    post = Post.query.filter_by(id=id).first()

    if not post: # If the post doesnt exist
        flash("Post does not exist.", category='error') # Sends an error
    elif current_user.id != post.id: # If the user not the author of the post 
        flash('You do not have permission to delete this post.', category='error') # Dont allow to delete
    else:
        db.session.delete(post) # If valid delete the post
        db.session.commit() # Commit the change to the database
        flash('Post deleted.', category='success') # Flash a message to exhibit the deletion is complete

    return redirect(url_for('views.home')) # Redirect user to the home page once complete

@views.route("/posts/<username>") # Sets the route for a users page of posts
@login_required # Requires the user to be logged in
def posts(username):
    user = User.query.filter_by(username=username).first()

    if not user: # If the user is not present in the database
        flash('No user with that username exists.', category='error') # Flash error message to user
        return redirect(url_for('views.home')) # Redirect user to the home page

    posts = user.posts # Define posts
    return render_template("posts.html", user=current_user, posts=posts, username=username) # Renders out the users page if it is valid

@views.route("/create-comment/<post_id>", methods=['POST']) # Sets the route for the creation of a comment under the posts ID
@login_required # Requires the user to be logged in
def create_comment(post_id):
    text = request.form.get('text') # Defines text

    if not text: # If the comment is empty
        flash('Comment cannot be empty.', category='error') # Return an error message
    else: # If valid
        post = Post.query.filter_by(id=post_id) # Define post
        if post: 
            comment = Comment(
                text=text, author=current_user.id, post_id=post_id) # Define comment
            db.session.add(comment) # If valid add the comment
            db.session.commit() # Commit the comment to the database
        else: # If the post doesn't exist
            flash('Post does not exist.', category='error') # Return an error message

    return redirect(url_for('views.home')) # Redirect the user to the home page

@views.route("/delete-comment/<comment_id>") # Sets a route for the deletion of a comment under the comments ID
@login_required # Requires the user to be logged in
def delete_comment(comment_id):
    comment = Comment.query.filter_by(id=comment_id).first() # Defines comment

    if not comment: # If the comment is invalid
        flash('Comment does not exist.', category='error') # Return an error message
    elif current_user.id != comment.author and current_user.id != comment.post.author: # If the user is not the author
        flash('You do not have permission to delete this comment.', category='error') # Return an error message
    else: # If valid 
        db.session.delete(comment) # Delete the comment
        db.session.commit() # Commit the deletion to the database

    return redirect(url_for('views.home')) # Redirect the user to the home page

@views.route("/like-post/<post_id>", methods=['POST']) # Sets a route for the liking of a post under the post ID
@login_required # Requires the user to be logged in
def like(post_id):
    post = Post.query.filter_by(id=post_id).first() # Defines the post
    like = Like.query.filter_by( 
        author=current_user.id, post_id=post_id).first() # Defines the like

    if not post: # If the post doesn't exist
        return jsonify({'error': 'Post does not exist.'}, 400) # Return error message
    elif like: # If the post does exist allow the deletion of the like
        db.session.delete(like) # Deletes the like
        db.session.commit() # Commits the change to the database
    else: 
        like = Like(author=current_user.id, post_id=post_id) # defines like
        db.session.add(like) # Adding a like
        db.session.commit() # Commits the addition to the database

    return jsonify({"likes": len(post.likes), "liked": current_user.id in map(lambda x: x.author, post.likes)}) # Displays the amount of likes

def save_picture(form_picture):
    path = Path("website/static/profile_pics") # Defines path
    random_hex = secrets.token_hex(8) # Defines a random hex that is 8 units long string to save the image under
    _,f_ext = os.path.splitext(form_picture.filename) # Defines f_ext
    picture_fn = random_hex + f_ext # Defines picture_fn under the addition of the random hex value and the f_ext value
    picture_path = os.path.join(path, picture_fn) # Sets the path for the database to find the image
    output_size = (125, 125) # Dimensions of the image being outputed
    i = Image.open(form_picture) # Defines i
    i.thumbnail(output_size)
    i.save(picture_path) # Saves the pathing of the image

    return picture_fn # Return the image to the user (updated)

@views.route("/account", methods=['GET', 'POST']) # Sets a route for the account page
@login_required # Requires the user to be logged in
def account():
    form = UpdateAccountForm() # Defines form
    if form.validate_on_submit(): # Begins validating when submitted
        if form.picture.data:
            picture_file = save_picture(form.picture.data) # Shows the picture that the user has saved
            current_user.image_file = picture_file # Defines picture_file
        current_user.username = form.username.data # Displays the username of the user
        current_user.email = form.email.data # Displays the email of the user
        db.session.commit() # Commits the changes to the database
        flash('Your account has been updated!', 'success') # Flash a success message
        return redirect(url_for('views.account')) # Redirects the user to the account page (shows new changes)
    elif request.method == 'GET': 
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file) # Defines the image_file under a URL
    return render_template('account.html',user=current_user,
                           image_file=image_file, form=form) # Returns the template of account page under the current user