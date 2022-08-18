from flask import g, request, jsonify, Blueprint

from models.users import User, UserDB


user_api_blueprint = Blueprint("user_api_blueprint", __name__)


@user_api_blueprint.route('/api/v1/users/', defaults={'user_id':None}, methods=["GET"])
@user_api_blueprint.route('/api/v1/users/<int:user_id>/', methods=["GET"])
def get_user(user_id):
    args = request.args
    userdb = UserDB(g.mysql_db, g.mysql_cursor)

    result = None

    if user_id is None:
        if not 'search' in args:
            result = userdb.select_all_users()

        else:
            result = userdb.select_user_by_username(args['search'])

    else:
        result = userdb.select_user_by_id(user_id)

    return jsonify({"status": "success", "users": result}), 200


@user_api_blueprint.route('/api/v1/users/', methods=["POST"])
def add_user():
    userdb = UserDB(g.mysql_db, g.mysql_cursor)
        
    user = User(request.json['username'], request.json['password'])
    result = userdb.insert_user(user)
    
    return jsonify({"status": "success", "id": result['user_id']}), 200


@user_api_blueprint.route('/api/v1/users/<int:user_id>/', methods=["PUT"])
def update_user(user_id):
    userdb = UserDB(g.mysql_db, g.mysql_cursor)

    user = User(request.json['username'], request.json['password'])
    userdb.update_user(user_id, user)
    
    return jsonify({"status": "success", "id": user_id}), 200


@user_api_blueprint.route('/api/v1/users/<int:user_id>/', methods=["DELETE"])
def delete_user(user_id):
    userdb = UserDB(g.mysql_db, g.mysql_cursor)

    userdb.delete_user_by_id(user_id)
        
    return jsonify({"status": "success", "id": user_id}), 200
