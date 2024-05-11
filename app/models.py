from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'owner' or 'user'

    def __init__(self, username, password_hash, role):
        self.username = username
        self.password_hash = password_hash
        self.role = role

    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'role': self.role
        }

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    genre = db.Column(db.String(50), nullable=False)
    availability = db.Column(db.Boolean, nullable=False, default=True)
    copies_available = db.Column(db.Integer, nullable=False)
    total_copies = db.Column(db.Integer, nullable=False)

    # def __init__(self, id, title, genre, availability, copies_available, total_copies):
    #     self.id = id
    #     self.title = title
    #     self.genre = genre
    #     self.availability = availability
    #     self.copies_available = copies_available
    #     self.total_copies = total_copies

    # def serialize(self):
    #     return {
    #         self.id = id
    #         self.title = title
    #         self.genre = genre
    #         self.availability = availability
    #         self.copies_available = copies_available
    #         self.total_copies = total_copies
    #     }

class BorrowedBook(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    borrow_date = db.Column(db.DateTime, nullable=False)
    return_date = db.Column(db.DateTime)
    overdue = db.Column(db.Boolean, nullable=False, default=False)
    fine_amount = db.Column(db.Float, default=0.0)
