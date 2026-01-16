from config import db, ma

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
    password = db.Column(db.String(30), nullable=False)
    role = db.Column(db.String(5), nullable=False, default='User')

# Marshmallow Schemas
class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        exclude = ('password',)  # Exclude password from serialization

user_schema = UserSchema()
users_schema = UserSchema(many=True)
