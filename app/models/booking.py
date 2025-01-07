"""
This module defines the Booking model for the database.
"""

from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.utils.database import Base


class Booking(Base):
    """
    Represents a booking for a meeting room made by a user.
    """
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    room_id = Column(Integer, ForeignKey("meeting_rooms.id"), nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)

    user = relationship("User", back_populates="bookings")
    room = relationship("MeetingRoom", back_populates="bookings")

    def __repr__(self):
        return (f"<Booking(id={self.id}, user_id={self.user_id}, "
                f"room_id={self.room_id}, start_time={self.start_time}, "
                f"end_time={self.end_time})>")
