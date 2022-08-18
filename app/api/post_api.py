from flask import g, request, jsonify, Blueprint

from models.posts import Post, PostDB
from models.users import UserDB

post_api_blueprint = Blueprint("post_api_blueprint", __name__)


@post_api_blueprint.route('/api/v1/posts/', defaults={'post_id':None}, methods=["GET"])
@post_api_blueprint.route('/api/v1/posts/<int:post_id>/', methods=["GET"])
def get_post(post_id):
    args = request.args
    postdb = PostDB(g.mysql_db, g.mysql_cursor)

    result = None

    if post_id is None:
        if not 'search' in args:
            result = postdb.select_all_posts()

        else:
            result = postdb.select_post_by_title(args['search'])

    else:
        result = postdb.select_post_by_id(post_id)

    return jsonify({"status": "success", "posts": result}), 200


@post_api_blueprint.route('/api/v1/posts/', methods=["POST"])
def add_post(username):
    postdb = PostDB(g.mysql_db, g.mysql_cursor)
    userdb = UserDB(g.mysql_db, g.mysql_cursor)
    user = userdb.select_user_by_username(username)
        
    post = Post(request.json['title'], request.json['content'], user)
    result = postdb.insert_post(post)
    
    return jsonify({"status": "success", "id": result['post_id']}), 200


@post_api_blueprint.route('/api/v1/posts/<int:post_id>/', methods=["PUT"])
def update_post(post_id, username):
    postdb = PostDB(g.mysql_db, g.mysql_cursor)
    userdb = UserDB(g.mysql_db, g.mysql_cursor)
    user = userdb.select_user_by_username(username)

    post = Post(request.json['title'], request.json['content'], user)
    postdb.update_post(post_id, post)
    
    return jsonify({"status": "success", "id": post_id}), 200


@post_api_blueprint.route('/api/v1/posts/<int:post_id>/', methods=["DELETE"])
def delete_post(post_id):
    postdb = PostDB(g.mysql_db, g.mysql_cursor)

    postdb.delete_post_by_id(post_id)
        
    return jsonify({"status": "success", "id": post_id}), 200