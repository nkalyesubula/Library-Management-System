from flask import jsonify, request
from app import app, db
from app.models import User, Book, BorrowedBook
from app.controllers import *
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash  # For password hashing

# Define API endpoints for managing users
@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password_hash')

    # Query the database to find the user with the provided username
    user = User.query.filter_by(username=username).first()

    # If user not found or password incorrect, return error message
    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({"msg": "Invalid username or password"}), 401

    # If username and password are correct, create and return JWT token
    access_token = create_access_token(identity=user.username)
    return jsonify(access_token=access_token), 200

@app.route('/api/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

@app.route('/api/users', methods=['POST'])
# @jwt_required()
def create_user():
    return create_user_controller(request)

@app.route('/api/users/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    print(get_jwt_identity())
    return get_user_controller(user_id)

@app.route('/api/users/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    return update_user_controller(user_id, request)

@app.route('/api/users/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    return delete_user_controller(user_id)

# Define API endpoints for managing books
@app.route('/api/books', methods=['POST'])
@jwt_required()
def create_book():
    return create_book_controller(request)

@app.route('/api/books/<int:book_id>', methods=['GET'])
@jwt_required()
def get_book(book_id):
    return get_book_controller(book_id)

@app.route('/api/books/<int:book_id>', methods=['PUT'])
@jwt_required()
def update_book(book_id):
    return update_book_controller(book_id, request)

@app.route('/api/books/<int:book_id>', methods=['DELETE'])
@jwt_required()
def delete_book(book_id):
    return delete_book_controller(book_id)

# Define API endpoints for borrowing and returning books
@app.route('/api/borrow', methods=['POST'])
@jwt_required()
def borrow_book():
    return borrow_book_controller(request)

@app.route('/api/return', methods=['POST'])
@jwt_required()
def return_book():
    return return_book_controller(request)

# Define API endpoints for tracking inventory
@app.route('/api/inventory', methods=['GET'])
@jwt_required()
def get_inventory():
    return get_inventory_controller()

@app.route('/api/overdue_books', methods=['GET'])
@jwt_required()
def get_overdue_books():
    return get_overdue_books_controller()

@app.route('/api/popular_books', methods=['GET'])
@jwt_required()
def get_popular_books():
    return get_popular_books_controller()

@app.route('/api/popular_genres', methods=['GET'])
@jwt_required()
def get_popular_genres():
    return get_popular_genres_controller()
