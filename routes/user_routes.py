from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from bson.objectid import ObjectId

from extensions import mongo

# Create blueprint FIRST
user_bp = Blueprint('users', __name__)


@user_bp.route('/', methods=['GET'])
def get_users():

    users = []

    for user in mongo.db.users.find({}, {'password': 0}):

        user['_id'] = str(user['_id'])

        users.append(user)

    return jsonify(users), 200


@user_bp.route('/profile', methods=['GET'])
@jwt_required()
def profile():

    user_id = get_jwt_identity()

    user = mongo.db.users.find_one(
        {'_id': ObjectId(user_id)},
        {'password': 0}
    )

    if not user:
        return jsonify({
            'error': 'User not found'
        }), 404

    user['_id'] = str(user['_id'])

    return jsonify(user), 200