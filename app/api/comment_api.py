from flask import g, request, jsonify, Blueprint

from models.comments import Comment, CommentDB
from models.posts import PostDB

comment_api_blueprint = Blueprint("comment_api_blueprint", __name__)


@comment_api_blueprint.route('/api/v1/comments/', defaults={'comment_id':None}, methods=["GET"])
@comment_api_blueprint.route('/api/v1/comments/<int:comment_id>/', methods=["GET"])
def get_comment(comment_id):
    args = request.args
    commentdb = CommentDB(g.mysql_db, g.mysql_cursor)

    result = None

    if comment_id is None:
        result = commentdb.select_all_comments()

    else:
        result = commentdb.select_post_by_id(comment_id)

    return jsonify({"status": "success", "comments": result}), 200


@comment_api_blueprint.route('/api/v1/comments/', methods=["POST"])
def add_comment(title):
    commentdb = CommentDB(g.mysql_db, g.mysql_cursor)
    postdb = PostDB(g.mysql_db, g.mysql_cursor)

    post = postdb.select_post_by_title(title)
        
    comment = Comment(request.json['text'], post)
    result = commentdb.insert_post(comment)
    
    return jsonify({"status": "success", "id": result['comment_id']}), 200


@comment_api_blueprint.route('/api/v1/comments/<int:comment_id>/', methods=["PUT"])
def update_post(comment_id, title):
    commentdb = CommentDB(g.mysql_db, g.mysql_cursor)
    postdb = PostDB(g.mysql_db, g.mysql_cursor)

    post = postdb.select_post_by_title(title)

    comment = Comment(request.json['text'], post)
    commentdb.update_comment(comment_id, comment)
    
    return jsonify({"status": "success", "id": comment_id}), 200


@comment_api_blueprint.route('/api/v1/comments/<int:comment_id>/', methods=["DELETE"])
def delete_comment(comment_id):
    commentdb = CommentDB(g.mysql_db, g.mysql_cursor)

    commentdb.delete_comment_by_id(comment_id)
        
    return jsonify({"status": "success", "id": comment_id}), 200