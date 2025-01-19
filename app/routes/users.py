"""
This module contains API routes for user management.
"""

from flask import Blueprint, jsonify, request
from app.schemas.user import UserCreate, UserUpdate, UserInDB
from app.services.user import (
    get_user_by_id,
    get_user_by_username,
    create_user,
    update_user,
    delete_user,
    get_users,
)
from app.utils.database import get_db
from sqlalchemy.orm import Session
from app.utils.auth import admin_required
from pydantic import ValidationError

users_bp = Blueprint("users", __name__)


@users_bp.route("/", methods=["POST"])
@admin_required
def create_new_user():
    """
    Creates a new user (admin only).
    """
    db: Session = next(get_db())
    try:
        user_data = UserCreate(**request.json)
        user = create_user(db, user_data)
        return jsonify(UserInDB.model_validate(user).model_dump()), 201
    except ValidationError as e:
        return jsonify(e.errors()), 400


@users_bp.route("/<int:user_id>", methods=["GET"])
@admin_required
def get_existing_user(user_id: int):
    """
    Retrieves a user by ID (admin only).
    """
    db: Session = next(get_db())
    user = get_user_by_id(db, user_id)
    if user:
        return jsonify(UserInDB.model_validate(user).model_dump())
    return jsonify({"message": "User not found"}), 404


@users_bp.route("/username/<string:username>", methods=["GET"])
@admin_required
def get_existing_user_by_username(username: str):
    """
    Retrieves a user by username (admin only).
    """
    db: Session = next(get_db())
    user = get_user_by_username(db, username)
    if user:
        return jsonify(UserInDB.model_validate(user).model_dump())
    return jsonify({"message": "User not found"}), 404


@users_bp.route("/", methods=["GET"])
@admin_required
def get_all_users():
    """
    Retrieves all users (admin only).
    """
    db: Session = next(get_db())
    skip = int(request.args.get("skip", 0))
    limit = int(request.args.get("limit", 100))
    users = get_users(db, skip, limit)
    return jsonify(
        [UserInDB.model_validate(user).model_dump() for user in users]
    )


@users_bp.route("/<int:user_id>", methods=["PUT"])
@admin_required
def update_existing_user(user_id: int):
    """
    Updates an existing user (admin only).
    """
    db: Session = next(get_db())
    user = get_user_by_id(db, user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    update_data = request.get_json()
    try:
        user_data = UserUpdate(**update_data)
    except ValidationError as e:
        return jsonify(e.errors()), 400

    updated_user = update_user(db, user_id, user_data)
    return jsonify(UserInDB.model_validate(updated_user).model_dump())


@users_bp.route("/<int:user_id>", methods=["DELETE"])
@admin_required
def delete_existing_user(user_id: int):
    """
    Deletes a user (admin only).
    """
    db: Session = next(get_db())
    if delete_user(db, user_id):
        return "", 204
    return jsonify({"message": "User not found"}), 404
