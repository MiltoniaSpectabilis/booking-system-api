"""
This module defines the MeetingRoom model for the database.
"""

from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from app.utils.database import Base


class MeetingRoom(Base):
    """
    Represents a meeting room in the system.
    """
    __tablename__ = "meeting_rooms"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True, nullable=False)
    capacity = Column(Integer, nullable=False)
    description = Column(Text)

    bookings = relationship("Booking", back_populates="room")

    def __repr__(self):
        return f"<MeetingRoom(id={self.id},\
        name='{self.name}',\
        capacity={self.capacity})>"
