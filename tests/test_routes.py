import unittest
from app import app, db
from app.models import User, Book, BorrowedBook
from app.controllers import *
from flask_jwt_extended import create_access_token
import json


class TestRoutes(unittest.TestCase):
    def setUp(self):
        # Set up Flask app for testing
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()

        # Create tables in the in-memory database
        with app.app_context():
            db.create_all()

    def tearDown(self):
        # Clean up database after each test
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_user(self):
        # Prepare test data
        data = {'username': 'test_user', 'password_hash': 'password', 'role': 'user'}

        # Send POST request to create user
        response = self.app.post('/api/users', json=data)

        # Check response status code
        self.assertEqual(response.status_code, 201)

        # Check if user was created in the database
        with app.app_context():
            user = User.query.filter_by(username='test_user').first()
            self.assertIsNotNone(user)

    # def test_login_valid_credentials(self):
    #     # Assuming there's a user with username 'test_user' and password 'password_hash'
    #     data = {'username': 'test_user', 'password_hash': 'password'}
    #     response = self.app.post('/api/login', json=data)
    #     print(response)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTrue('access_token' in response.json)

    def test_login_invalid_credentials(self):
        data = {'username': 'nonexistent_user', 'password_hash': 'wrong_password'}
        response = self.app.post('/api/login', json=data)
        self.assertEqual(response.status_code, 401)

    def test_protected_route_without_token(self):
        response = self.app.get('/api/protected')
        self.assertEqual(response.status_code, 401)

    def test_protected_route_with_valid_token(self):
        # Assuming there's a valid JWT token for a user
        token = create_access_token(identity='test_user')
        headers = {'Authorization': 'Bearer ' + token}
        response = self.app.get('/api/protected', headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['logged_in_as'], 'test_user')

    # def test_get_user(self):
    #     # Assuming there's a user with id=1 in the database
    #     token = create_access_token(identity='test_user')
    #     headers = {'Authorization': 'Bearer ' + token}
    #     response = self.app.get('/api/users/1', headers=headers)
    #     self.assertEqual(response.status_code, 200)

    # def test_create_book(self):
    #     token = create_access_token(identity='test_user')
    #     headers = {'Authorization': 'Bearer ' + token}
    #     data = {'title': 'Test Book', 'genre': 'Fiction', 'copies_available': 10, 'total_copies': 10}
    #     response = self.client.post('/api/books', headers=headers, json=data)
    #     self.assertEqual(response.status_code, 201)

    # def test_get_book(self):
    #     # Assuming there's a book with id=1 in the database
    #     token = create_access_token(identity='test_user')
    #     headers = {'Authorization': 'Bearer ' + token}
    #     response = self.app.get('/api/books/1', headers=headers)
    #     self.assertEqual(response.status_code, 200)

    # def test_borrow_book(self):
    #     # Assuming there's a user with id=1 and a book with id=1 in the database
    #     token = create_access_token(identity='test_user')
    #     headers = {'Authorization': 'Bearer ' + token}
    #     data = {'user_id': 1, 'book_id': 1}
    #     response = self.app.post('/api/borrow', headers=headers, json=data)
    #     self.assertEqual(response.status_code, 201)


if __name__ == '__main__':
    unittest.main()
