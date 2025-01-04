from sqlalchemy.orm import Session
from app.models.booking import Booking
from app.schemas.booking import BookingCreate, BookingUpdate
from app.services.user import get_user_by_id
from app.services.meeting_room import get_room_by_id
from sqlalchemy import and_, or_
from datetime import datetime


def get_booking_by_id(db: Session, booking_id: int):
    return db.query(Booking).filter(Booking.id == booking_id).first()


def get_bookings_by_user_id(
        db: Session, user_id: int, skip: int = 0, limit: int = 100
):
    return db.query(Booking).filter(Booking.user_id == user_id).offset(skip)\
        .limit(limit).all()


def get_bookings_by_room_id(
        db: Session, room_id: int, skip: int = 0, limit: int = 100
):
    return db.query(Booking).filter(Booking.room_id == room_id).offset(skip)\
        .limit(limit).all()


def get_bookings(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Booking).offset(skip).limit(limit).all()


def create_booking(db: Session, booking: BookingCreate):
    if get_user_by_id(db, booking.user_id) is None:
        raise ValueError(f"User with id {booking.user_id} does not exist")
    if get_room_by_id(db, booking.room_id) is None:
        raise ValueError(f"Room with id {booking.room_id} does not exist")
    if not is_room_available(
        db, booking.room_id, booking.start_time, booking.end_time
    ):
        raise ValueError(
            f"Room with id {booking.room_id} is not available during the\
            specified time"
        )
    db_booking = Booking(**booking.dict())
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    return db_booking


def update_booking(db: Session, booking_id: int, booking: BookingUpdate):
    db_booking = get_booking_by_id(db, booking_id)
    if not db_booking:
        return None
    update_data = booking.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_booking, key, value)
    db.commit()
    db.refresh(db_booking)
    return db_booking


def cancel_booking(db: Session, booking_id: int):
    db_booking = get_booking_by_id(db, booking_id)
    if not db_booking:
        return False
    db.delete(db_booking)
    db.commit()
    return True


def is_room_available(
        db: Session, room_id: int, start_time: datetime, end_time: datetime
):
    overlapping_bookings = db.query(Booking).filter(
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
    ).all()
    return not overlapping_bookings
