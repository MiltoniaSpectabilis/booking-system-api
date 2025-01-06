from flask import Blueprint, jsonify, request
from app.schemas.user import UserCreate, UserInDB
from app.services.user import create_user, get_user_by_username
from app.utils.hashing import Hasher
from app.utils.auth import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from app.utils.database import get_db
from sqlalchemy.orm import Session
from datetime import timedelta
import os

auth_bp = Blueprint("auth", __name__)

SECRET_KEY = os.environ.get("SECRET_KEY")


@auth_bp.route("/register", methods=["POST"])
def register_user():
    db: Session = next(get_db())
    user_data = UserCreate(**request.json)
    if get_user_by_username(db, user_data.username):
        return jsonify({"message": "Username already exists"}), 400
    user = create_user(db, user_data)
    return jsonify(UserInDB.from_orm(user).dict()), 201


@auth_bp.route("/login", methods=["POST"])
def login_user():
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
    return jsonify(dict(access_token=access_token)), 200
