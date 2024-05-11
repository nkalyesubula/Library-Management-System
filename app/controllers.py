from flask import jsonify, request
from app import db
from app.models import User, Book, BorrowedBook
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash

# User management controllers
# def create_user_controller(request):
#     data = request.json
#     new_user = User(username=data['username'], password_hash=data['password_hash'], role=data['role'])
#     db.session.add(new_user)
#     db.session.commit()
#     return jsonify({"message": "User created successfully"}), 201
def create_user_controller(request):
    data = request.json
    username = data.get('username')
    password = data.get('password_hash')  # Assuming you're passing hashed password from client
    role = data.get('role')

    # Check if username already exists
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({"message": "Username already exists"}), 400

    # Hash the password
    password_hash = generate_password_hash(password)

    # Create and add user to the database
    new_user = User(username=username, password_hash=password_hash, role=role)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User created successfully"}), 201

def get_user_controller(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify(user.serialize())

def update_user_controller(user_id, request):
    user = User.query.get_or_404(user_id)
    data = request.json
    user.username = data.get('username', user.username)
    user.password_hash = data.get('password_hash', user.password_hash)
    user.role = data.get('role', user.role)
    db.session.commit()
    return jsonify({"message": "User updated successfully"})

def delete_user_controller(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted successfully"})

# Book management controllers
def create_book_controller(request):
    data = request.json
    new_book = Book(title=data['title'], genre=data['genre'], availability=True,
                    copies_available=data['copies_available'], total_copies=data['total_copies'])
    db.session.add(new_book)
    db.session.commit()
    return jsonify({"message": "Book created successfully"}), 201

def get_book_controller(book_id):
    book = Book.query.get_or_404(book_id)
    return jsonify(book.serialize())

def update_book_controller(book_id, request):
    book = Book.query.get_or_404(book_id)
    data = request.json
    book.title = data.get('title', book.title)
    book.genre = data.get('genre', book.genre)
    book.copies_available = data.get('copies_available', book.copies_available)
    book.total_copies = data.get('total_copies', book.total_copies)
    db.session.commit()
    return jsonify({"message": "Book updated successfully"})

def delete_book_controller(book_id):
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    return jsonify({"message": "Book deleted successfully"})

# Borrowing and returning controllers
def borrow_book_controller(request):
    data = request.json
    user_id = data['user_id']
    book_id = data['book_id']
    user = User.query.get_or_404(user_id)
    book = Book.query.get_or_404(book_id)

    if not book.availability:
        return jsonify({"message": "Book is not available for borrowing"}), 400

    if book.copies_available <= 0:
        return jsonify({"message": "No copies available for borrowing"}), 400

    borrow_date = datetime.now()
    return_date = borrow_date + timedelta(days=7)  # One week borrowing period
    new_borrowed_book = BorrowedBook(user_id=user_id, book_id=book_id, borrow_date=borrow_date, return_date=return_date)
    db.session.add(new_borrowed_book)

    book.copies_available -= 1
    if book.copies_available == 0:
        book.availability = False

    db.session.commit()
    return jsonify({"message": "Book borrowed successfully"}), 201

def return_book_controller(request):
    data = request.json
    borrowed_book_id = data['borrowed_book_id']
    borrowed_book = BorrowedBook.query.get_or_404(borrowed_book_id)

    if borrowed_book.return_date > datetime.now():
        borrowed_book.overdue = True
        fine_days = (datetime.now() - borrowed_book.return_date).days
        borrowed_book.fine_amount = fine_days * 10  # $10 fine per overdue day

    book = Book.query.get_or_404(borrowed_book.book_id)
    book.copies_available += 1
    book.availability = True

    db.session.commit()
    return jsonify({"message": "Book returned successfully"})

# Inventory tracking controllers
def get_inventory_controller():
    total_books = Book.query.count()
    total_users = User.query.count()
    available_books = Book.query.filter_by(availability=True).count()
    overdue_books = BorrowedBook.query.filter(BorrowedBook.return_date < datetime.now()).all()
    popular_book = Book.query.order_by(Book.copies_available.desc()).first()
    popular_genre = db.session.query(Book.genre).group_by(Book.genre).order_by(db.func.count().desc()).first()[0]

    return jsonify({
        "total_books": total_books,
        "total_users": total_users,
        "available_books": available_books,
        "overdue_books": len(overdue_books),
        "popular_book": popular_book.serialize(),
        "popular_genre": popular_genre
    })

def get_overdue_books_controller():
    overdue_books = BorrowedBook.query.filter(BorrowedBook.return_date < datetime.now()).all()
    return jsonify([book.serialize() for book in overdue_books])

def get_popular_books_controller():
    popular_books = Book.query.order_by(Book.copies_available.desc()).limit(5).all()
    return jsonify([book.serialize() for book in popular_books])

def get_popular_genres_controller():
    popular_genres = db.session.query(Book.genre).group_by(Book.genre).order_by(db.func.count().desc()).limit(5).all()
    return jsonify([genre[0] for genre in popular_genres])
