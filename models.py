from config import db, ma
from werkzeug.security import generate_password_hash, check_password_hash

# User Model
class User(db.Model):
    __tablename__ = 'Users'
    __table_args__ = {'schema': 'CW2'}

    email = db.Column(db.String(30), primary_key=True)
    username = db.Column(db.String(30), nullable=False)
    about_me = db.Column(db.Text, nullable=True)
    location = db.Column(db.String(50), nullable=True)
    dob = db.Column(db.Date, nullable=True)
    language = db.Column(db.String(30), nullable=True)
    password = db.Column(db.String(30), nullable=False)  # Hashed password
    role = db.Column(db.String(5), nullable=False, default='User')

    # Relationship to FavouriteActivity
    favourites = db.relationship('FavouriteActivity', backref='user', lazy=True)



# Activity Model
class Activity(db.Model):
    __tablename__ = 'Activity'
    __table_args__ = {'schema': 'CW2'}

    activity_id = db.Column(db.SmallInteger, primary_key=True, autoincrement=False)
    activity = db.Column(db.String(30), nullable=False, unique=True)

    # Relationship to FavouriteActivity
    favourited_by = db.relationship('FavouriteActivity', backref='activity', lazy=True)

# FavouriteActivity Model (junction table)
class FavouriteActivity(db.Model):
    __tablename__ = 'FavouriteActivity'
    __table_args__ = {'schema': 'CW2'}

    email = db.Column(db.String(30), db.ForeignKey('CW2.Users.email', ondelete='CASCADE'), primary_key=True)
    activity_id = db.Column(db.SmallInteger, db.ForeignKey('CW2.Activity.activity_id'), primary_key=True)

# Marshmallow Schemas
class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        exclude = ('password',)  # Exclude password from serialization

class ActivitySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Activity
        load_instance = True

class FavouriteActivitySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = FavouriteActivity
        load_instance = True
        include_fk = True  # Include foreign keys for nested data

user_schema = UserSchema()
users_schema = UserSchema(many=True)
activity_schema = ActivitySchema()
activities_schema = ActivitySchema(many=True)
favourite_schema = FavouriteActivitySchema()
favourites_schema = FavouriteActivitySchema(many=True)
