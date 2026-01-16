import re
from flask import abort, make_response
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
from config import db
from models import User, Activity, FavouriteActivity, user_schema, users_schema, activity_schema, activities_schema, favourite_schema, favourites_schema

# READ ALL
def read_all():
    # Retrieves all users from the database
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

def update_profile(email, body):
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

    try:
        db.session.commit()
        return user_schema.dump(user)
    except IntegrityError as e:
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
        if "foreign key" in str(e).lower() or "reference constraint" in str(e).lower():
            abort(409, "Cannot delete profile with associated favourites")
        abort(500, f"Database error: {str(e)}")

def login(body):
    email = body.get("Email").strip() if body.get("Email") else None
    password = body.get("Password")
    if not email or not password:
        abort(400, "Email and Password are required")

    user = User.query.get(email)
    if user and user.password == password:
        return {"message": "Login successful"}
    else:
        abort(401, "Invalid email or password")



# PROCEDURES AND VIEWS

def insert_via_procedure(body):
    email = body.get("email")
    username = body.get("username")
    password = body.get("password")
    about_me = body.get("about_me")
    location = body.get("location")
    dob = body.get("dob")
    language = body.get("language")
    role = body.get("role", "User")
    if not email or not username or not password:
        abort(400, "Email, Username, and Password are required")

    try:
        sql = text("EXEC CW2.usp_InsertUser @Email = :email, @Username = :username, @About_me = :about_me, @Location = :location, @Dob = :dob, @Language = :language, @Password = :password, @Role = :role")
        db.session.execute(sql, {"email": email, "username": username, "about_me": about_me, "location": location, "dob": dob, "language": language, "password": password, "role": role})
        db.session.commit()
        return {"message": "User inserted via procedure"}, 201
    except IntegrityError as e:
        db.session.rollback()
        abort(500, f"Database error: {str(e)}")

def get_via_procedure(email):
    try:
        sql = text("EXEC CW2.usp_GetUser @Email = :email")
        result = db.session.execute(sql, {"email": email}).fetchone()
        if result:
            return dict(result)
        else:
            abort(404, f"User with email {email} not found")
    except IntegrityError as e:
        abort(500, f"Database error: {str(e)}")

def update_via_procedure(body):
    email = body.get("email")
    username = body.get("username")
    about_me = body.get("about_me")
    location = body.get("location")
    dob = body.get("dob")
    language = body.get("language")
    password = body.get("password")
    role = body.get("role")
    if not email:
        abort(400, "Email is required")

    try:
        sql = text("EXEC CW2.usp_UpdateUser @Email = :email, @Username = :username, @About_me = :about_me, @Location = :location, @Dob = :dob, @Language = :language, @Password = :password, @Role = :role")
        db.session.execute(sql, {"email": email, "username": username, "about_me": about_me, "location": location, "dob": dob, "language": language, "password": password, "role": role})
        db.session.commit()
        return {"message": "User updated via procedure"}
    except IntegrityError as e:
        db.session.rollback()
        abort(500, f"Database error: {str(e)}")

def delete_via_procedure(email):
    try:
        sql = text("EXEC CW2.usp_DeleteUser @Email = :email")
        db.session.execute(sql, {"email": email})
        db.session.commit()
        return make_response("", 204)
    except IntegrityError as e:
        db.session.rollback()
        abort(500, f"Database error: {str(e)}")

def get_profile_view():
    try:
        result = db.session.execute(text("SELECT * FROM CW2.vw_UserProfile")).fetchall()
        return [dict(row) for row in result]
    except IntegrityError as e:
        abort(500, f"Database error: {str(e)}")

# ACTIVITIES

# READ ALL ACTIVITIES
def read_all_activities():
    try:
        activities = Activity.query.all()
        return activities_schema.dump(activities)
    except Exception as e:
        abort(500, f"Database error: {str(e)}")

# CREATE ACTIVITY
def create_activity(body):
    activity_name = body.get("Activity").strip() if body.get("Activity") else None
    if not activity_name:
        abort(400, "Activity is required")

    try:
        existing = Activity.query.filter_by(activity=activity_name).first()
        if existing:
            abort(409, f"Activity '{activity_name}' already exists")

        max_id = db.session.query(db.func.max(Activity.activity_id)).scalar()
        next_id = (max_id + 1) if max_id else 1

        activity = Activity(activity_id=next_id, activity=activity_name)
        db.session.add(activity)
        db.session.commit()
        return activity_schema.dump(activity), 201
    except Exception as e:
        db.session.rollback()
        abort(500, f"Database error: {str(e)}")

# FAVOURITES

# READ USER FAVOURITES
def read_user_favourites(email):
    try:
        user = User.query.get(email)
        if not user:
            abort(404, f"User {email} not found")

        favourites = [fav.activity for fav in user.favourites]
        return activities_schema.dump(favourites)
    except Exception as e:
        abort(500, f"Database error: {str(e)}")

# ADD FAVOURITE
def add_favourite(email, body):
    activity_id = body.get("Activity_id")
    if activity_id is None or not isinstance(activity_id, int):
        abort(400, "Valid Activity_id is required")

    try:
        user = User.query.get(email)
        if not user:
            abort(404, f"User {email} not found")

        activity = Activity.query.get(activity_id)
        if not activity:
            abort(404, f"Activity {activity_id} not found")

        existing = FavouriteActivity.query.get((email, activity_id))
        if existing:
            abort(409, "Already a favourite")

        fav = FavouriteActivity(email=email, activity_id=activity_id)
        db.session.add(fav)
        db.session.commit()
        return {"message": "Favourite added"}, 201
    except Exception as e:
        db.session.rollback()
        abort(500, f"Database error: {str(e)}")

# REMOVE FAVOURITE
def remove_favourite(email, activity_id):
    if not isinstance(activity_id, int):
        abort(400, "Valid activity_id required")

    try:
        fav = FavouriteActivity.query.get((email, activity_id))
        if not fav:
            abort(404, "Favourite not found")
        db.session.delete(fav)
        db.session.commit()
        return make_response("", 204)
    except Exception as e:
        db.session.rollback()
        abort(500, f"Database error: {str(e)}")
