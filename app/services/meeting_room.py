"""
This module contains service functions for meeting room management.
"""

from sqlalchemy.orm import Session
from app.models.meeting_room import MeetingRoom
from app.schemas.meeting_room import MeetingRoomCreate, MeetingRoomUpdate
from sqlalchemy.exc import IntegrityError


def get_room_by_id(db: Session, room_id: int) -> MeetingRoom | None:
    """
    Retrieves a meeting room by its ID.
    """
    return db.query(MeetingRoom).filter(MeetingRoom.id == room_id).first()


def get_room_by_name(db: Session, name: str) -> MeetingRoom | None:
    """
    Retrieves a meeting room by its name.
    """
    return db.query(MeetingRoom).filter(MeetingRoom.name == name).first()


def get_rooms(
        db: Session, skip: int = 0, limit: int = 100
) -> list[MeetingRoom]:
    """
    Retrieves a list of meeting rooms with pagination.
    """
    return db.query(MeetingRoom).offset(skip).limit(limit).all()


def create_room(db: Session, room: MeetingRoomCreate) -> MeetingRoom:
    """
    Creates a new meeting room.
    """
    db_room = MeetingRoom(**room.model_dump())
    db.add(db_room)
    try:
        db.commit()
        db.refresh(db_room)
        return db_room
    except IntegrityError as e:
        db.rollback()
        if "ix_meeting_rooms_name" in str(e):
            raise ValueError("A room with this name already exists.") from e
        else:
            raise ValueError(
                "An error occurred while creating the room.") from e


def update_room(
        db: Session, room_id: int, room: MeetingRoomUpdate
) -> MeetingRoom | None:
    """
    Updates an existing meeting room.
    """
    db_room = get_room_by_id(db, room_id)
    if not db_room:
        return None
    update_data = room.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_room, key, value)
    db.commit()
    db.refresh(db_room)
    return db_room


def delete_room(db: Session, room_id: int) -> bool:
    """
    Deletes a meeting room.
    """
    db_room = get_room_by_id(db, room_id)
    if not db_room:
        return False
    db.delete(db_room)
    db.commit()
    return True
