import os
import pyodbc
import re
from flask import abort, make_response
from dotenv import load_dotenv

# Load environment variables from .env file for database configuration
load_dotenv()

DB_SERVER = os.getenv("DB_SERVER")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

def get_db_connection():
    # Requires ODBC Driver for MSSQL
    try:
        conn = pyodbc.connect(
            f"DRIVER={{ODBC Driver 17 for SQL Server}};"
            f"SERVER={DB_SERVER};"
            f"DATABASE={DB_NAME};"
            f"UID={DB_USER};"
            f"PWD={DB_PASSWORD};"
            "Encrypt=yes;"
            "TrustServerCertificate=yes;"
        )
        return conn
    except Exception as e:
        abort(500, f"Database connection failed: {str(e)}")

# READ ALL
def read_all():
    # Self explanitory, retrieves all users
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT Email, Username FROM CW2.Users")
        columns = [column[0] for column in cursor.description]
        rows = cursor.fetchall()
        result = [dict(zip(columns, row)) for row in rows]
        return result
    finally:
        cursor.close()
        conn.close()

# READ ONE
def read_one(email):
    # Selects user by email
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT Email, Username FROM CW2.Users WHERE Email = ?", email)
        row = cursor.fetchone()
        if row:
            columns = [column[0] for column in cursor.description]
            return dict(zip(columns, row))
        else:
            abort(404, f"Profile with email {email} not found")
    finally:
        cursor.close()
        conn.close()

# CREATE
def create(body):
    # Creates new user
    email = body.get("Email").strip() if body.get("Email") else None
    username = body.get("Username").strip() if body.get("Username") else None
    password = body.get("Password")

    if not email or not username or not password:
        abort(400, "Email, Username, and Password are required")

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Check if email exists
        cursor.execute("SELECT 1 FROM CW2.Users WHERE Email = ?", email)
        if cursor.fetchone():
            abort(409, f"Profile with email {email} already exists")

        cursor.execute("""
            INSERT INTO CW2.Users (Email, Username, Password)
            VALUES (?, ?, ?)
        """, (email, username, password))
        conn.commit()
        return read_one(email), 201
    except pyodbc.Error as e:
        conn.rollback()
        abort(500, f"Database error: {str(e)}")
    finally:
        cursor.close()
        conn.close()

# UPDATE
def update(email, body):
    # Update user account details
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT 1 FROM CW2.Users WHERE Email = ?", email)
        if not cursor.fetchone():
            abort(404, f"Profile with email {email} not found")

        updates = []
        params = []
        if "Username" in body:
            username = body["Username"].strip()
            if not username:
                abort(400, "Username cannot be empty")
            updates.append("Username = ?")
            params.append(username)
        if "Password" in body:
            password = body["Password"]
            updates.append("Password = ?")
            params.append(password)

        if not updates:
            abort(400, "No fields to update")

        params.append(email)
        sql = f"UPDATE CW2.Users SET {', '.join(updates)} WHERE Email = ?"
        cursor.execute(sql, params)
        conn.commit()
        return read_one(email)
    except pyodbc.Error as e:
        conn.rollback()
        abort(500, f"Database error: {str(e)}")
    finally:
        cursor.close()
        conn.close()

# DELETE
def delete(email):
    # Deletes user, selected by email
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM CW2.Users WHERE Email = ?", email)
        if cursor.rowcount == 0:
            abort(404, f"Profile with email {email} not found")
        conn.commit()
        return make_response("", 204)
    except pyodbc.Error as e:
        conn.rollback()
        abort(500, f"Database error: {str(e)}")
    finally:
        cursor.close()
        conn.close()
