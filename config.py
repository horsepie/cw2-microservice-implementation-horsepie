from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize SQLAlchemy and Marshmallow without app
db = SQLAlchemy()
ma = Marshmallow()

def configure_app(app):
    # Database configuration from environment variables
    app.config['SQLALCHEMY_DATABASE_URI'] = (
        f"mssql+pyodbc://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_SERVER')}/{os.getenv('DB_NAME')}"
        "?driver=ODBC+Driver+17+for+SQL+Server&Encrypt=yes&TrustServerCertificate=yes"
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
