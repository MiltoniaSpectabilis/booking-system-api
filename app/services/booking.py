"""
This module contains service functions for booking management.
"""

from sqlalchemy.orm import Session
from app.models.booking import Booking
from app.schemas.booking import BookingCreate, BookingUpdate
from app.services.user import get_user_by_id
from app.services.meeting_room import get_room_by_id
from sqlalchemy import and_, or_
from datetime import datetime, timezone


def get_booking_by_id(db: Session, booking_id: int) -> Booking | None:
    """
    Retrieves a booking by its ID.
    """
    return db.query(Booking).filter(Booking.id == booking_id).first()


def get_bookings_by_user_id(
    db: Session, user_id: int, skip: int = 0, limit: int = 100
) -> list[Booking]:
    """
    Retrieves a list of bookings for a specific user.
    """
    return (
        db.query(Booking)
        .filter(Booking.user_id == user_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_bookings_by_room_id(
    db: Session, room_id: int, skip: int = 0, limit: int = 100
) -> list[Booking]:
    """
    Retrieves a list of bookings for a specific meeting room.
    """
    return (
        db.query(Booking)
        .filter(Booking.room_id == room_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_bookings(
        db: Session, skip: int = 0, limit: int = 100
) -> list[Booking]:
    """
    Retrieves a list of all bookings.
    """
    return db.query(Booking).offset(skip).limit(limit).all()


def create_booking(db: Session, booking: BookingCreate) -> Booking:
    """
    Creates a new booking.
    """
    if get_user_by_id(db, booking.user_id) is None:
        raise ValueError(f"User with id {booking.user_id} does not exist")
    if get_room_by_id(db, booking.room_id) is None:
        raise ValueError(f"Room with id {booking.room_id} does not exist")
    if booking.start_time.tzinfo is None:
        booking.start_time = booking.start_time.replace(tzinfo=timezone.utc)
    if booking.start_time < datetime.now(timezone.utc):
        raise ValueError("Cannot create a booking in the past")
    if not is_room_available(
        db, booking.room_id, booking.start_time, booking.end_time
    ):
        raise ValueError(
            f"Room with id {
                booking.room_id} is not available during the specified time"
        )
    db_booking = Booking(**booking.model_dump())
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    return db_booking


def update_booking(
    db: Session, booking_id: int, booking: BookingUpdate
) -> Booking | None:
    """
    Updates an existing booking.
    """
    db_booking = get_booking_by_id(db, booking_id)
    if not db_booking:
        return None
    update_data = booking.model_dump(exclude_unset=True)
    new_start = update_data.get("start_time", db_booking.start_time)
    new_end = update_data.get("end_time", db_booking.end_time)
    if not is_room_available(
        db,
        db_booking.room_id,
        new_start,
        new_end,
        exclude_booking_id=db_booking.id
    ):
        raise ValueError("Room is not available during the specified time")

    for key, value in update_data.items():
        setattr(db_booking, key, value)
    db.commit()
    db.refresh(db_booking)
    return db_booking


def cancel_booking(db: Session, booking_id: int) -> bool:
    """
    Cancels a booking.
    """
    db_booking = get_booking_by_id(db, booking_id)
    if not db_booking:
        return False
    db.delete(db_booking)
    db.commit()
    return True


def is_room_available(
    db: Session,
    room_id: int,
    start_time: datetime,
    end_time: datetime,
    exclude_booking_id: int = None
) -> bool:
    """
    Checks if a room is available during a given time slot,
    excluding a specific booking.
    """
    query = db.query(Booking).filter(
        and_(
            Booking.room_id == room_id,
            or_(
                and_(Booking.start_time < end_time,
                     Booking.end_time > start_time),
                and_(Booking.start_time >= start_time,
                     Booking.start_time < end_time),
                and_(Booking.end_time > start_time,
                     Booking.end_time <= end_time)
            )
        )
    )
    if exclude_booking_id:
        query = query.filter(Booking.id != exclude_booking_id)
    overlapping_bookings = query.all()
    return not overlapping_bookings
