from flask import jsonify, request
from app import app, db
from app.models import User, Book, BorrowedBook
from app.controllers import *

# Define API endpoints for managing users
@app.route('/api/users', methods=['POST'])
def create_user():
    return create_user_controller(request)

@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    return get_user_controller(user_id)

@app.route('/api/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    return update_user_controller(user_id, request)

@app.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    return delete_user_controller(user_id)

# Define API endpoints for managing books
@app.route('/api/books', methods=['POST'])
def create_book():
    return create_book_controller(request)

@app.route('/api/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    return get_book_controller(book_id)

@app.route('/api/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    return update_book_controller(book_id, request)

@app.route('/api/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    return delete_book_controller(book_id)

# Define API endpoints for borrowing and returning books
@app.route('/api/borrow', methods=['POST'])
def borrow_book():
    return borrow_book_controller(request)

@app.route('/api/return', methods=['POST'])
def return_book():
    return return_book_controller(request)

# Define API endpoints for tracking inventory
@app.route('/api/inventory', methods=['GET'])
def get_inventory():
    return get_inventory_controller()

@app.route('/api/overdue_books', methods=['GET'])
def get_overdue_books():
    return get_overdue_books_controller()

@app.route('/api/popular_books', methods=['GET'])
def get_popular_books():
    return get_popular_books_controller()

@app.route('/api/popular_genres', methods=['GET'])
def get_popular_genres():
    return get_popular_genres_controller()
