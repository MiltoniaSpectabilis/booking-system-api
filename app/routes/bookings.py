from flask import Blueprint, jsonify, request
from app.schemas.booking import BookingCreate, BookingUpdate, BookingInDB
from app.services.booking import (
    get_booking_by_id,
    create_booking,
    update_booking,
    cancel_booking,
    get_bookings_by_user_id,
    get_bookings_by_room_id,
    get_bookings
)
from app.utils.database import get_db
from sqlalchemy.orm import Session

bookings_bp = Blueprint("bookings", __name__)


@bookings_bp.route("/bookings", methods=["POST"])
def create_new_booking():
    db: Session = next(get_db())
    booking_data = BookingCreate(**request.json)
    try:
        booking = create_booking(db, booking_data)
    except ValueError as e:
        return jsonify({"message": str(e)}), 400
    return jsonify(BookingInDB.from_orm(booking).dict()), 201


@bookings_bp.route("/bookings/<int:booking_id>", methods=["GET"])
def get_existing_booking(booking_id: int):
    db: Session = next(get_db())
    booking = get_booking_by_id(db, booking_id)
    if booking:
        return jsonify(BookingInDB.from_orm(booking).dict())
    return jsonify({"message": "Booking not found"}), 404


@bookings_bp.route("/bookings/user/<int:user_id>", methods=["GET"])
def get_bookings_for_user(user_id: int):
    db: Session = next(get_db())
    skip = int(request.args.get("skip", 0))
    limit = int(request.args.get("limit", 100))
    bookings = get_bookings_by_user_id(db, user_id, skip, limit)
    return jsonify(
        [BookingInDB.from_orm(booking).dict() for booking in bookings]
    )


@bookings_bp.route("/bookings/room/<int:room_id>", methods=["GET"])
def get_bookings_for_room(room_id: int):
    db: Session = next(get_db())
    skip = int(request.args.get("skip", 0))
    limit = int(request.args.get("limit", 100))
    bookings = get_bookings_by_room_id(db, room_id, skip, limit)
    return jsonify(
        [BookingInDB.from_orm(booking).dict() for booking in bookings]
    )


@bookings_bp.route("/bookings", methods=["GET"])
def get_all_bookings():
    db: Session = next(get_db())
    skip = int(request.args.get("skip", 0))
    limit = int(request.args.get("limit", 100))
    bookings = get_bookings(db, skip, limit)
    return jsonify(
        [BookingInDB.from_orm(booking).dict() for booking in bookings]
    )


@bookings_bp.route("/bookings/<int:booking_id>", methods=["PUT"])
def update_existing_booking(booking_id: int):
    db: Session = next(get_db())
    booking_data = BookingUpdate(**request.json)
    updated_booking = update_booking(db, booking_id, booking_data)
    if updated_booking:
        return jsonify(BookingInDB.from_orm(updated_booking).dict())
    return jsonify({"message": "Booking not found"}), 404


@bookings_bp.route("/bookings/<int:booking_id>", methods=["DELETE"])
def delete_existing_booking(booking_id: int):
    db: Session = next(get_db())
    if cancel_booking(db, booking_id):
        return jsonify({"message": "Booking deleted"})
    return jsonify({"message": "Booking not found"}), 404
