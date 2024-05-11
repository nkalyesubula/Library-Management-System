# config.py
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_secret_key_here'
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:admin@localhost/library_management'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
