from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime, timedelta
from bson.objectid import ObjectId

from extensions import mongo

transaction_bp = Blueprint('transactions', __name__)

@transaction_bp.route('/borrow', methods=['POST'])
@jwt_required()
def borrow_book():

    data = request.get_json()

    user_id = get_jwt_identity()
    book_id = data.get('book_id')

    if not book_id:
        return jsonify({"error": "book_id required"}), 400

    book = mongo.db.books.find_one({"_id": ObjectId(book_id)})

    if not book:
        return jsonify({"error": "Book not found"}), 404

    # check if already borrowed
    existing = mongo.db.transactions.find_one({
        "user_id": user_id,
        "book_id": book_id,
        "status": "borrowed"
    })

    if existing:
        return jsonify({"error": "Book already borrowed"}), 409

    borrow_date = datetime.utcnow()
    due_date = borrow_date + timedelta(days=14)

    transaction = {
        "user_id": user_id,
        "book_id": book_id,
        "borrow_date": borrow_date,
        "due_date": due_date,
        "return_date": None,
        "status": "borrowed"
    }

    mongo.db.transactions.insert_one(transaction)

    return jsonify({
        "message": "Book borrowed successfully",
        "due_date": due_date.isoformat()
    }), 201

@transaction_bp.route('/return', methods=['POST'])
@jwt_required()
def return_book():

    data = request.get_json()
    user_id = get_jwt_identity()
    book_id = data.get('book_id')

    transaction = mongo.db.transactions.find_one({
        "user_id": user_id,
        "book_id": book_id,
        "status": "borrowed"
    })

    if not transaction:
        return jsonify({"error": "No active borrow found"}), 404

    return_date = datetime.utcnow()

    # fine calculation
    due_date = transaction['due_date']
    fine = 0

    if return_date > due_date:
        days_late = (return_date - due_date).days
        fine = days_late * 10   # ₹10 per day fine (simple logic)

    mongo.db.transactions.update_one(
        {"_id": transaction["_id"]},
        {"$set": {
            "return_date": return_date,
            "status": "returned",
            "fine": fine
        }}
    )

    return jsonify({
        "message": "Book returned successfully",
        "fine": fine
    }), 200