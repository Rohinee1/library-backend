"""
LibraryHub - Flask Backend Application
Main application file with database configuration and route setup
"""
from bson.objectid import ObjectId
from flask import Flask, request, jsonify
from flask_cors import CORS
from extensions import mongo, bcrypt, jwt
from datetime import datetime, timedelta
from functools import wraps
import os
from dotenv import load_dotenv


# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Configuration
app.config['MONGO_URI'] = os.getenv('MONGO_URI', 'mongodb://localhost:27017/library_db')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'your-secret-key-change-in-production')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=30)

# Initialize extensions
mongo.init_app(app)
jwt.init_app(app)
bcrypt.init_app(app)

CORS(app)

# =====================================================
# DATABASE INITIALIZATION & INDEXES
# =====================================================

def init_db():
    """Initialize database collections and indexes"""
    try:
        # Create collections if they don't exist
        db = mongo.db
        
        # Collections
        if 'books' not in db.list_collection_names():
            db.create_collection('books')
        if 'users' not in db.list_collection_names():
            db.create_collection('users')
        if 'transactions' not in db.list_collection_names():
            db.create_collection('transactions')
        if 'reservations' not in db.list_collection_names():
            db.create_collection('reservations')
        
        # Create indexes for faster queries
        db.books.create_index('isbn', unique=True)
        db.books.create_index('title')
        db.books.create_index('author')
        db.books.create_index('category')
        
        db.users.create_index('email', unique=True)
        db.users.create_index('member_id', unique=True)
        
        db.transactions.create_index('member_id')
        db.transactions.create_index('book_id')
        db.transactions.create_index('created_at')
        
        db.reservations.create_index('member_id')
        db.reservations.create_index('book_id')
        
        print("✅ Database initialized successfully")
    except Exception as e:
        print(f"❌ Database initialization error: {e}")

# =====================================================
# IMPORT ROUTES
# =====================================================

from routes.auth_routes import auth_bp
from routes.book_routes import book_bp
from routes.user_routes import user_bp
from routes.transaction_routes import transaction_bp
from routes.admin_routes import admin_bp

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(book_bp, url_prefix='/api/books')
app.register_blueprint(user_bp, url_prefix='/api/users')
app.register_blueprint(transaction_bp, url_prefix='/api/transactions')
app.register_blueprint(admin_bp, url_prefix='/api/admin')

# =====================================================
# ERROR HANDLERS
# =====================================================

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Resource not found'}), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({'error': 'Internal server error'}), 500

@app.errorhandler(401)
def unauthorized(error):
    return jsonify({'error': 'Unauthorized'}), 401

@app.errorhandler(403)
def forbidden(error):
    return jsonify({'error': 'Forbidden'}), 403

# =====================================================
# HEALTH CHECK
# =====================================================

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'success',
        'message': 'LibraryHub API is running',
        'timestamp': datetime.now().isoformat()
    }), 200

# =====================================================
# APP CONTEXT & INITIALIZATION
# =====================================================

if __name__ == '__main__':
    with app.app_context():
        init_db()
    
    app.run(
    debug=True,
    host='0.0.0.0',
    port=5000
)