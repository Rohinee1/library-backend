
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from datetime import datetime
import uuid

from extensions import mongo, bcrypt

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['POST'])
def register():

    data = request.get_json()

    if not data:
        return jsonify({
            'error': 'No data provided'
        }), 400

    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    if not all([name, email, password]):
        return jsonify({
            'error': 'Name, email and password are required'
        }), 400

    existing_user = mongo.db.users.find_one({
        'email': email
    })

    if existing_user:
        return jsonify({
            'error': 'Email already exists'
        }), 409

    hashed_password = bcrypt.generate_password_hash(
        password
    ).decode('utf-8')

    user = {
        'member_id': str(uuid.uuid4()),
        'name': name,
        'email': email,
        'password': hashed_password,
        'created_at': datetime.utcnow()
    }

    mongo.db.users.insert_one(user)

    return jsonify({
        'message': 'User registered successfully'
    }), 201


@auth_bp.route('/login', methods=['POST'])
def login():

    data = request.get_json()

    if not data:
        return jsonify({
            'error': 'No data provided'
        }), 400

    email = data.get('email')
    password = data.get('password')

    if not all([email, password]):
        return jsonify({
            'error': 'Email and password are required'
        }), 400

    user = mongo.db.users.find_one({
        'email': email
    })

    if not user:
        return jsonify({
            'error': 'Invalid credentials'
        }), 401

    if not bcrypt.check_password_hash(
        user['password'],
        password
    ):
        return jsonify({
            'error': 'Invalid credentials'
        }), 401

    token = create_access_token(
        identity=str(user['_id'])
    )

    return jsonify({
        'message': 'Login successful',
        'token': token
    }), 200
