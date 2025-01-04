from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from app.utils.database import Base


class MeetingRoom(Base):
    __tablename__ = "meeting_rooms"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    capacity = Column(Integer, nullable=False)
    description = Column(Text)

    bookings = relationship("Booking", back_populates="room")
