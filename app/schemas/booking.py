"""
This module defines Pydantic schemas for the Booking model.
"""

from pydantic import BaseModel, validator
from datetime import datetime
from typing import Optional


class BookingBase(BaseModel):
    """
    Base schema for Booking.
    """
    start_time: datetime
    end_time: datetime

    @validator("end_time")
    def validate_end_time(cls, value, values):
        """Validator to ensure end_time is after start_time."""
        if "start_time" in values and value <= values["start_time"]:
            raise ValueError("end_time must be greater than start_time")
        return value


class BookingCreate(BookingBase):
    """
    Schema for creating a new Booking.
    """
    user_id: int
    room_id: int


class BookingUpdate(BookingBase):
    """
    Schema for updating a Booking.
    """
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None


class BookingInDB(BookingBase):
    """
    Schema for representing a Booking retrieved from the database.
    """
    id: int
    user_id: int
    room_id: int

    class Config:
        from_attributes = True
