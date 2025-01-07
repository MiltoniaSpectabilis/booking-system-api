"""
This module defines Pydantic schemas for the MeetingRoom model.
"""

from pydantic import BaseModel, constr, Field
from typing import Optional


class MeetingRoomBase(BaseModel):
    """
    Base schema for MeetingRoom.
    """
    name: constr(min_length=3, max_length=100)
    capacity: int = Field(..., gt=0)
    description: Optional[str] = None


class MeetingRoomCreate(MeetingRoomBase):
    """
    Schema for creating a new MeetingRoom.
    """
    pass


class MeetingRoomUpdate(MeetingRoomBase):
    """
    Schema for updating a MeetingRoom.
    """
    name: Optional[constr(min_length=3, max_length=100)] = None
    capacity: Optional[int] = Field(None, gt=0)
    description: Optional[str] = None


class MeetingRoomInDB(MeetingRoomBase):
    """
    Schema for representing a MeetingRoom retrieved from the database.
    """
    id: int

    class Config:
        from_attributes = True
