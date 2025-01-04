from flask import Blueprint, jsonify, request
from app.schemas.user import UserCreate, UserUpdate, UserInDB
from app.services.user import (
    get_user_by_id,
    get_user_by_username,
    create_user, update_user,
    delete_user,
    get_users
)
from app.utils.database import get_db
from sqlalchemy.orm import Session
from app.utils.auth import admin_required

users_bp = Blueprint("users", __name__)


@users_bp.route("/users", methods=["POST"])
@admin_required
def create_new_user():
    db: Session = next(get_db())
    user_data = UserCreate(**request.json)
    user = create_user(db, user_data)
    return jsonify(UserInDB.from_attributes(user).dict()), 201


@users_bp.route("/users/<int:user_id>", methods=["GET"])
@admin_required
def get_existing_user(user_id: int):
    db: Session = next(get_db())
    user = get_user_by_id(db, user_id)
    if user:
        return jsonify(UserInDB.from_attributes(user).dict())
    return jsonify({"message": "User not found"}), 404


@users_bp.route("/users/username/<string:username>", methods=["GET"])
@admin_required
def get_existing_user_by_username(username: str):
    db: Session = next(get_db())
    user = get_user_by_username(db, username)
    if user:
        return jsonify(UserInDB.from_attributes(user).dict())
    return jsonify({"message": "User not found"}), 404


@users_bp.route("/users", methods=["GET"])
@admin_required
def get_all_users():
    db: Session = next(get_db())
    skip = int(request.args.get("skip", 0))
    limit = int(request.args.get("limit", 100))
    users = get_users(db, skip, limit)
    return jsonify([UserInDB.from_attributes(user).dict() for user in users])


@users_bp.route("/users/<int:user_id>", methods=["PUT"])
@admin_required
def update_existing_user(user_id: int):
    db: Session = next(get_db())
    user_data = UserUpdate(**request.json)
    updated_user = update_user(db, user_id, user_data)
    if updated_user:
        return jsonify(UserInDB.from_attributes(updated_user).dict())
    return jsonify({"message": "User not found"}), 404


@users_bp.route("/users/<int:user_id>", methods=["DELETE"])
@admin_required
def delete_existing_user(user_id: int):
    db: Session = next(get_db())
    if delete_user(db, user_id):
        return jsonify({"message": "User deleted"})
    return jsonify({"message": "User not found"}), 404
