"""
This module contains service functions for user management.
"""

from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.utils.hashing import Hasher
from sqlalchemy.exc import IntegrityError


def get_user_by_id(db: Session, user_id: int) -> User | None:
    """
    Retrieves a user by their ID.
    """
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_username(db: Session, username: str) -> User | None:
    """
    Retrieves a user by their username.
    """
    return db.query(User).filter(User.username == username).first()


def get_users(db: Session, skip: int = 0, limit: int = 100) -> list[User]:
    """
    Retrieves a list of users with pagination.
    """
    return db.query(User).offset(skip).limit(limit).all()


def create_user(db: Session, user: UserCreate) -> User:
    """
    Creates a new user.
    """
    hashed_password = Hasher.get_password_hash(user.password)
    is_admin = user.is_admin if user.is_admin else (
        user.username == "admin"
    )
    db_user = User(
        username=user.username,
        password=hashed_password,
        is_admin=is_admin
    )
    db.add(db_user)
    try:
        db.commit()
        db.refresh(db_user)
        return db_user
    except IntegrityError:
        db.rollback()
        raise ValueError("Username already exists.")


def update_user(db: Session, user_id: int, user: UserUpdate) -> User | None:
    """
    Updates an existing user.
    """
    db_user = get_user_by_id(db, user_id)
    if not db_user:
        return None

    update_data = user.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_user, key, value)

    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int) -> bool:
    """
    Deletes a user.
    """
    db_user = get_user_by_id(db, user_id)
    if not db_user:
        return False
    db.delete(db_user)
    db.commit()
    return True
