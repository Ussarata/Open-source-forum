from flask import Blueprint, request, redirect
from flask import render_template, g, Blueprint
from api.user_api import UserDB
from api.post_api import Post, PostDB

post_list_blueprint = Blueprint("post_list_blueprint", __name__)

@post_list_blueprint.route('/', methods = ["GET", "POST"])
def index():
    """Receives all of the posts in the database to display."""
    database = PostDB(g.mysql_db, g.mysql_cursor)

    if request.method == "POST":
        post_ids = request.form.getlist("post_item")
        for id in post_ids:
            database.delete_post_by_id(id)

    return render_template('index.html', timeline = database.select_all_posts())


@post_list_blueprint.route('/post-entry')
def post_entry():
   return render_template("post-entry.html")


@post_list_blueprint.route('/add-post', methods = ["POST"])
def add_post():
    """Gets the username, title, and content of a post to add it to the database."""
    title = request.form.get("post_title")
    content = request.form.get("post_content")
    username = request.form.get("post_username")
    
    userdb = UserDB(g.mysql_db, g.mysql_cursor)
    user_id = userdb.select_user_by_username(username)["user_id"]
    
    new_post = Post(title, content, user_id)
    database = PostDB(g.mysql_db, g.mysql_cursor)

    database.insert_post(new_post)

    return redirect('/')


@post_list_blueprint.route('/post-edit')
def post_edit():
   return render_template("post-edit.html")


@post_list_blueprint.route('/edit-post', methods = ["GET", "POST"])
def edit_post():
    """Gets the title of the post and the new content of said post to replace with the old content."""
    title = request.form.get('post_title')

    new_content = request.form.get("post_new_content")
    username = request.form.get("post_username")

    userdb = UserDB(g.mysql_db, g.mysql_cursor)
    user_id = userdb.select_user_by_username(username)["user_id"]

    database = PostDB(g.mysql_db, g.mysql_cursor)
    post = database.select_post_by_title(title)["post_id"]
    new_post = Post(title, new_content, user_id)

    database.update_post(post, new_post)

    return redirect('/')


@post_list_blueprint.route('/delete-post', methods = ["DELETE"])
def delete_post():
    """Gets the title of a post to find and delete from the database."""
    title = request.form.get('post_title')

    database = PostDB(g.mysql_db, g.mysql_cursor)
    post = database.select_post_by_title(title)

    database.delete_post_by_id(post)

    return redirect('/')

@post_list_blueprint.route('/post-delete')
def post_remove():
   return render_template("post-delete.html")


@post_list_blueprint.route('/user-profile', methods = ["GET", "POST"])
def user_index():
    """Finds all of the posts associated with a certain user to display."""
    userdb = UserDB(g.mysql_db, g.mysql_cursor)
    database = PostDB(g.mysql_db, g.mysql_cursor)

    username = request.form.get("post_username")
    user_id = userdb.select_user_by_username(username)["user_id"]

    if request.method == "POST":
        post_ids = request.form.getlist("post_item")
        for id in post_ids:
            database.delete_post_by_id(id)

    return render_template('user-profile.html', user_profile = database.select_posts_by_user_id(user_id))
