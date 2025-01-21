"""
This module provides authentication utilities using JWT.
"""

from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError, JWSError
from app.services.user import get_user_by_username
from app.utils.database import get_db
from sqlalchemy.orm import Session
from functools import wraps
from flask import request, jsonify
import os

SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """
    Creates a JWT access token.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str, credentials_exception):
    """
    Verifies a JWT token.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        return username
    except (JWTError, JWSError):
        raise credentials_exception


def get_current_user(token: str):
    """
    Gets the current user from a JWT token.
    """
    db: Session = next(get_db())
    credentials_exception = Exception("Could not validate credentials")
    username = verify_token(token, credentials_exception)
    user = get_user_by_username(db, username)
    if user is None:
        raise credentials_exception
    return user


def token_required(f):
    """
    Decorator to ensure the request includes a valid JWT token.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({"message": "Token is missing!"}), 401
        try:
            token = token.split(" ")[1]
            current_user = get_current_user(token)
        except Exception:
            return jsonify({"message": "Invalid token!"}), 401
        return f(current_user, *args, **kwargs)
    return decorated_function


def user_required(f):
    """
    Decorator to ensure the current user matches the user ID in the request.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({"message": "Token is missing!"}), 401
        try:
            token = token.split(" ")[1]
            current_user = get_current_user(token)
            user_id = kwargs.get('user_id')
            if current_user.id != int(user_id):
                return jsonify({"message": "Access denied!"}), 403
        except Exception:
            return jsonify({"message": "Invalid token!"}), 401
        return f(current_user, *args, **kwargs)
    return decorated_function


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({"message": "Token is missing!"}), 401
        try:
            token = token.split(" ")[1]
            current_user = get_current_user(token)
            if not current_user.is_admin:
                return jsonify({"message": "Admin access required!"}), 403
        except Exception:
            return jsonify({"message": "Invalid token!"}), 401
        return f(*args, **kwargs)
    return decorated_function
