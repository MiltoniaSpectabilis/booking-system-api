"""
This module defines Pydantic schemas for the User model.
"""

from pydantic import BaseModel, Field, constr
from typing import Optional


class UserBase(BaseModel):
    """
    Base schema for User.
    """
    username: str


class UserCreate(UserBase):
    """
    Schema for creating a new User.
    """
    password: str = Field(..., min_length=6)
    is_admin: bool = False
    username: constr(min_length=3, max_length=50)


class UserUpdate(UserBase):
    """
    Schema for updating a User.
    """
    is_admin: Optional[bool] = None
    username: Optional[constr(min_length=3, max_length=50)] = None


class UserInDB(UserBase):
    """
    Schema for representing a User retrieved from the database.
    """
    id: int
    is_admin: bool
    username: constr(min_length=3, max_length=50)

    class Config:
        from_attributes = True
