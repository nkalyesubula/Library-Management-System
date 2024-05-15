from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager

# Create Flask application instance
app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

# Initialize SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://koyeb-adm:Ivcu0b8YqiVs@ep-frosty-cherry-a2w8eegd.eu-central-1.pg.koyeb.app/koyebdb'
db = SQLAlchemy(app)

# Initialize JWT
jwt = JWTManager(app)

# Create a Migrate object to handle database migrations.
migrate = Migrate(app, db)

# Import routes and models (to ensure routes and models are registered with the app)
from app import routes, models
