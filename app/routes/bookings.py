"""
This module contains API routes for booking management.
"""

from flask import Blueprint, jsonify, request
from app.schemas.booking import BookingCreate, BookingUpdate, BookingInDB
from app.services.booking import (
    get_booking_by_id,
    create_booking,
    update_booking,
    cancel_booking,
    get_bookings_by_user_id,
    get_bookings_by_room_id,
    get_bookings,
)
from app.utils.database import get_db
from sqlalchemy.orm import Session

bookings_bp = Blueprint("bookings", __name__)


@bookings_bp.route("/", methods=["POST"])
def create_new_booking():
    """
    Creates a new booking.
    """
    db: Session = next(get_db())
    try:
        booking_data = BookingCreate(**request.json)
        booking = create_booking(db, booking_data)
        return jsonify(BookingInDB.model_validate(booking).model_dump()), 201
    except ValueError as e:
        return jsonify({"message": str(e)}), 400


@bookings_bp.route("/<int:booking_id>", methods=["GET"])
def get_existing_booking(booking_id: int):
    """
    Retrieves a booking by ID.
    """
    db: Session = next(get_db())
    booking = get_booking_by_id(db, booking_id)
    if booking:
        return jsonify(BookingInDB.model_validate(booking).model_dump())
    return jsonify({"message": "Booking not found"}), 404


@bookings_bp.route("/user/<int:user_id>", methods=["GET"])
def get_bookings_for_user(user_id: int):
    """
    Retrieves all bookings for a specific user.
    """
    db: Session = next(get_db())
    skip = int(request.args.get("skip", 0))
    limit = int(request.args.get("limit", 100))
    bookings = get_bookings_by_user_id(db, user_id, skip, limit)
    return jsonify(
        [BookingInDB.model_validate(booking).model_dump()
         for booking in bookings]
    )


@bookings_bp.route("/room/<int:room_id>", methods=["GET"])
def get_bookings_for_room(room_id: int):
    """
    Retrieves all bookings for a specific room.
    """
    db: Session = next(get_db())
    skip = int(request.args.get("skip", 0))
    limit = int(request.args.get("limit", 100))
    bookings = get_bookings_by_room_id(db, room_id, skip, limit)
    return jsonify(
        [BookingInDB.model_validate(booking).model_dump()
         for booking in bookings]
    )


@bookings_bp.route("/", methods=["GET"])
def get_all_bookings():
    """
    Retrieves all bookings.
    """
    db: Session = next(get_db())
    skip = int(request.args.get("skip", 0))
    limit = int(request.args.get("limit", 100))
    bookings = get_bookings(db, skip, limit)
    return jsonify(
        [BookingInDB.model_validate(booking).model_dump()
         for booking in bookings]
    )


@bookings_bp.route("/<int:booking_id>", methods=["PUT"])
def update_existing_booking(booking_id: int):
    """
    Updates an existing booking.
    """
    db: Session = next(get_db())
    booking_data = BookingUpdate(**request.json)
    updated_booking = update_booking(db, booking_id, booking_data)
    if updated_booking:
        return jsonify(
            BookingInDB.model_validate(updated_booking).model_dump()
        )
    return jsonify({"message": "Booking not found"}), 404


@bookings_bp.route("/<int:booking_id>", methods=["DELETE"])
def delete_existing_booking(booking_id: int):
    """
    Deletes a booking.
    """
    db: Session = next(get_db())
    if cancel_booking(db, booking_id):
        return jsonify({"message": "Booking cancelled successfully"})
    return jsonify({"message": "Booking not found"}), 404
