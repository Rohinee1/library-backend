from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from bson.objectid import ObjectId

from extensions import mongo

book_bp = Blueprint('books', __name__)

@book_bp.route('/add', methods=['POST'])
@jwt_required()
def add_book():

    data = request.get_json()

    required_fields = [
        'title',
        'author',
        'isbn',
        'category',
        'quantity'
    ]

    for field in required_fields:
        if field not in data:
            return jsonify({
                'error': f'{field} is required'
            }), 400

    existing_book = mongo.db.books.find_one({
        'isbn': data['isbn']
    })

    if existing_book:
        return jsonify({
            'error': 'Book already exists'
        }), 409

    book = {
        'title': data['title'],
        'author': data['author'],
        'isbn': data['isbn'],
        'category': data['category'],
        'quantity': int(data['quantity']),
        'available': int(data['quantity'])
    }

    result = mongo.db.books.insert_one(book)

    return jsonify({
        'message': 'Book added successfully',
        'book_id': str(result.inserted_id)
    }), 201

@book_bp.route('/', methods=['GET'])
def get_books():

    books = []

    for book in mongo.db.books.find():

        book['_id'] = str(book['_id'])
        books.append(book)

    return jsonify(books), 200

@book_bp.route('/<book_id>', methods=['GET'])
def get_book(book_id):

    book = mongo.db.books.find_one({
        '_id': ObjectId(book_id)
    })

    if not book:
        return jsonify({
            'error': 'Book not found'
        }), 404

    book['_id'] = str(book['_id'])

    return jsonify(book), 200

@book_bp.route('/<book_id>', methods=['PUT'])
@jwt_required()
def update_book(book_id):

    data = request.get_json()

    mongo.db.books.update_one(
        {'_id': ObjectId(book_id)},
        {'$set': data}
    )

    return jsonify({
        'message': 'Book updated successfully'
    }), 200

@book_bp.route('/<book_id>', methods=['DELETE'])
@jwt_required()
def delete_book(book_id):

    result = mongo.db.books.delete_one({
        '_id': ObjectId(book_id)
    })

    if result.deleted_count == 0:
        return jsonify({
            'error': 'Book not found'
        }), 404

    return jsonify({
        'message': 'Book deleted successfully'
    }), 200