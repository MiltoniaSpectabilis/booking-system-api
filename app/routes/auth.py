"""
This module contains authentication-related routes.
"""

from app.models.user import User
from flask import Blueprint, jsonify, request
from app.schemas.user import UserCreate, UserInDB
from app.services.user import create_user, get_user_by_username
from app.utils.hashing import Hasher
from app.utils.auth import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from app.utils.database import get_db
from sqlalchemy.orm import Session
from datetime import timedelta
from pydantic import ValidationError

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
def register_user():
    """
    Registers a new user.
    """
    db: Session = next(get_db())
    try:
        user_data = UserCreate(**request.json)
    except ValidationError as e:
        return jsonify(e.errors()), 400
    is_first_user = db.query(User).count() == 0
    user_data.is_admin = is_first_user
    if get_user_by_username(db, user_data.username):
        return jsonify({"message": "Username already exists"}), 409
    user = create_user(db, user_data)
    return jsonify(UserInDB.model_validate(user).model_dump()), 201


@auth_bp.route("/login", methods=["POST"])
def login_user():
    """
    Logs in a user.
    """
    db: Session = next(get_db())
    username = request.json.get("username")
    password = request.json.get("password")
    user = get_user_by_username(db, username)
    if not user or not Hasher.verify_password(password, user.password):
        return jsonify({"message": "Invalid credentials"}), 401
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return jsonify(access_token=access_token), 200
