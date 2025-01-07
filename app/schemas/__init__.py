"""
This package contains Pydantic schemas for data validation and serialization.
"""

from .user import (
    UserBase,
    UserCreate,
    UserInDB,
    UserUpdate
)
from .meeting_room import (
    MeetingRoomBase,
    MeetingRoomCreate,
    MeetingRoomInDB,
    MeetingRoomUpdate
)
from .booking import (
    BookingBase,
    BookingCreate,
    BookingInDB,
    BookingUpdate
)
