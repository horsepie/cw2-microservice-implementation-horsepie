import re
from flask import abort, make_response
from config import db
from models import User, user_schema, users_schema

# READ ALL
def read_all():
    try:
        users = User.query.all()
        return users_schema.dump(users)
    except Exception as e:
        abort(500, f"Database error: {str(e)}")

def read_one(email):
    try:
        user = User.query.get(email)
        if user:
            return user_schema.dump(user)
        else:
            abort(404, f"Profile with email {email} not found")
    except Exception as e:
        abort(500, f"Database error: {str(e)}")

def create(body):
    email = body.get("Email").strip() if body.get("Email") else None
    username = body.get("Username").strip() if body.get("Username") else None
    password = body.get("Password")
    about_me = body.get("AboutMe").strip() if body.get("AboutMe") else None
    location = body.get("Location").strip() if body.get("Location") else None
    dob = body.get("Dob")
    language = body.get("Language").strip() if body.get("Language") else None
    role = body.get("Role", "User").strip()

    if not email or not username or not password:
        abort(400, "Email, Username, and Password are required")

    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        abort(400, "Invalid email format")

    if role not in ["Admin", "User"]:
        abort(400, "Role must be 'Admin' or 'User'")

    try:
        if User.query.get(email):
            abort(409, f"Profile with email {email} already exists")

        user = User(
            email=email,
            username=username,
            about_me=about_me,
            location=location,
            dob=dob,
            language=language,
            password=password,
            role=role
        )
        db.session.add(user)
        db.session.commit()
        return user_schema.dump(user), 201
    except Exception as e:
        db.session.rollback()
        abort(500, f"Database error: {str(e)}")

def update(email, body):
    try:
        user = User.query.get(email)
        if not user:
            abort(404, f"Profile with email {email} not found")

        updated = False
        if "Username" in body:
            username = body["Username"].strip()
            if not username:
                abort(400, "Username cannot be empty")
            user.username = username
            updated = True
        if "AboutMe" in body:
            user.about_me = body["AboutMe"].strip() if body["AboutMe"] else None
            updated = True
        if "Location" in body:
            user.location = body["Location"].strip() if body["Location"] else None
            updated = True
        if "Dob" in body:
            user.dob = body["Dob"]
            updated = True
        if "Language" in body:
            user.language = body["Language"].strip() if body["Language"] else None
            updated = True
        if "Role" in body:
            role = body["Role"].strip()
            if role not in ["Admin", "User"]:
                abort(400, "Role must be 'Admin' or 'User'")
            user.role = role
            updated = True
        if "Password" in body:
            user.password = body["Password"]
            updated = True

        if not updated:
            abort(400, "No fields to update")

        db.session.commit()
        return user_schema.dump(user)
    except Exception as e:
        db.session.rollback()
        abort(500, f"Database error: {str(e)}")

def delete(email):
    try:
        user = User.query.get(email)
        if not user:
            abort(404, f"Profile with email {email} not found")
        db.session.delete(user)
        db.session.commit()
        return make_response("", 204)
    except Exception as e:
        db.session.rollback()
        abort(500, f"Database error: {str(e)}")

def login(body):
    email = body.get("Email").strip() if body.get("Email") else None
    password = body.get("Password")
    if not email or not password:
        abort(400, "Email and Password are required")

    try:
        user = User.query.get(email)
        if user and user.password == password:
            return {"message": "Login successful"}
        else:
            abort(401, "Invalid email or password")
    except Exception as e:
        abort(500, f"Database error: {str(e)}")

def read_one(email):
    # Selects user by email
    try:
        user = User.query.get(email)
        if user:
            return {'email': user.email, 'username': user.username, 'about_me': user.about_me, 'location': user.location, 'dob': str(user.dob) if user.dob else None, 'language': user.language, 'role': user.role}
        else:
            abort(404, f"Profile with email {email} not found")
    except Exception as e:
        abort(500, f"Database error: {str(e)}")

# READ ONE
def read_one(email):
    # Selects user by email
    try:
        user = User.query.get(email)
        if user:
            return {'email': user.email, 'username': user.username, 'about_me': user.about_me, 'location': user.location, 'dob': str(user.dob) if user.dob else None, 'language': user.language, 'role': user.role}
        else:
            abort(404, f"Profile with email {email} not found")
    except Exception as e:
        abort(500, f"Database error: {str(e)}")

# CREATE
def create(body):
    # Creates new user with all fields
    email = body.get("Email").strip() if body.get("Email") else None
    username = body.get("Username").strip() if body.get("Username") else None
    password = body.get("Password")
    about_me = body.get("AboutMe").strip() if body.get("AboutMe") else None
    location = body.get("Location").strip() if body.get("Location") else None
    dob = body.get("Dob")
    language = body.get("Language").strip() if body.get("Language") else None
    role = body.get("Role", "User").strip()

    if not email or not username or not password:
        abort(400, "Email, Username, and Password are required")

    # This uses regex to make sure the email field is a valid email address
    # god I hate regex syntax so much
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        abort(400, "Invalid email format")

    if role not in ["Admin", "User"]:
        abort(400, "Role must be 'Admin' or 'User'")

    try:
        if User.query.get(email):
            abort(409, f"Profile with email {email} already exists")

        user = User(
            email=email,
            username=username,
            about_me=about_me,
            location=location,
            dob=dob,
            language=language,
            password=password,
            role=role
        )
        db.session.add(user)
        db.session.commit()
        return {'email': user.email, 'username': user.username, 'about_me': user.about_me, 'location': user.location, 'dob': str(user.dob) if user.dob else None, 'language': user.language, 'role': user.role}, 201
    except Exception as e:
        db.session.rollback()
        abort(500, f"Database error: {str(e)}")

# UPDATE
def update(email, body):
    # Update user account details
    try:
        user = User.query.get(email)
        if not user:
            abort(404, f"Profile with email {email} not found")

        updated = False
        if "Username" in body:
            username = body["Username"].strip()
            if not username:
                abort(400, "Username cannot be empty")
            user.username = username
            updated = True
        if "AboutMe" in body:
            user.about_me = body["AboutMe"].strip() if body["AboutMe"] else None
            updated = True
        if "Location" in body:
            user.location = body["Location"].strip() if body["Location"] else None
            updated = True
        if "Dob" in body:
            user.dob = body["Dob"]
            updated = True
        if "Language" in body:
            user.language = body["Language"].strip() if body["Language"] else None
            updated = True
        if "Role" in body:
            role = body["Role"].strip()
            if role not in ["Admin", "User"]:
                abort(400, "Role must be 'Admin' or 'User'")
            user.role = role
            updated = True
        if "Password" in body:
            user.password = body["Password"]
            updated = True

        if not updated:
            abort(400, "No fields to update")

        db.session.commit()
        return {'email': user.email, 'username': user.username, 'about_me': user.about_me, 'location': user.location, 'dob': str(user.dob) if user.dob else None, 'language': user.language, 'role': user.role}
    except Exception as e:
        db.session.rollback()
        abort(500, f"Database error: {str(e)}")

# DELETE
def delete(email):
    # Deletes user, selected by email
    try:
        user = User.query.get(email)
        if not user:
            abort(404, f"Profile with email {email} not found")
        db.session.delete(user)
        db.session.commit()
        return make_response("", 204)
    except Exception as e:
        db.session.rollback()
        abort(500, f"Database error: {str(e)}")

# LOGIN
def login(body):
    # Authenticates user by comparing plaintext passwords
    email = body.get("Email").strip() if body.get("Email") else None
    password = body.get("Password")
    if not email or not password:
        abort(400, "Email and Password are required")

    try:
        user = User.query.get(email)
        if user and user.password == password:
            return {"message": "Login successful"}
        else:
            abort(401, "Invalid email or password")
    except Exception as e:
        abort(500, f"Database error: {str(e)}")
