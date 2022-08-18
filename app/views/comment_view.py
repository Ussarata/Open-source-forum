from flask import Blueprint, request, redirect
from flask import render_template, g, Blueprint
from api.comment_api import Comment, CommentDB
from api.post_api import PostDB

comment_list_blueprint = Blueprint("comment_list_blueprint", __name__)

@comment_list_blueprint.route('/comment-entry')
def comment_entry():
   return render_template("comment-entry.html")


@comment_list_blueprint.route('/add-comment', methods = ["POST"])
def add_comment():
    """Gets the title of a post and the text for a comment to add a comment under the post with the given title."""
    text = request.form.get("comment_text")
    title = request.form.get("comment_title")
    
    postdb = PostDB(g.mysql_db, g.mysql_cursor)
    post_id = postdb.select_post_by_title(title)
    
    new_comment = Comment(text, post_id)
    database = CommentDB(g.mysql_db, g.mysql_cursor)

    database.insert_comment(new_comment)

    return redirect('/post')


@comment_list_blueprint.route('/post', methods = ["GET", "POST"])
def post_index():
    """Receives all of the comments associated with a post to display."""
    postdb = PostDB(g.mysql_db, g.mysql_cursor)
    database = CommentDB(g.mysql_db, g.mysql_cursor)

    title = request.form.get("comment_title")
    post_id = postdb.select_post_by_title(title)

    if request.method == "POST":
        comment_ids = request.form.getlist("comment_item")
        for id in comment_ids:
            database.delete_comment_by_id(id)

    return render_template('post-index.html', post_index = database.select_comments_by_post_id(post_id))