"""
This module contains API routes for meeting room management.
"""

from flask import Blueprint, jsonify, request
from app.schemas.meeting_room import (
    MeetingRoomCreate,
    MeetingRoomUpdate,
    MeetingRoomInDB,
)
from app.services.meeting_room import (
    get_room_by_id,
    get_room_by_name,
    create_room,
    update_room,
    delete_room,
    get_rooms,
)
from app.utils.database import get_db
from sqlalchemy.orm import Session
from pydantic import ValidationError

rooms_bp = Blueprint("rooms", __name__)


@rooms_bp.route("/", methods=["POST"])
def create_new_room():
    """
    Creates a new meeting room.
    """
    db: Session = next(get_db())
    try:
        room_data = MeetingRoomCreate(**request.json)
    except ValidationError as e:
        return jsonify(e.errors()), 400
    try:
        room = create_room(db, room_data)
    except ValueError as e:
        return jsonify({"message": str(e)}), 400
    return jsonify(MeetingRoomInDB.model_validate(room).model_dump()), 201


@rooms_bp.route("/<int:room_id>", methods=["GET"])
def get_existing_room(room_id: int):
    """
    Retrieves a meeting room by ID.
    """
    db: Session = next(get_db())
    room = get_room_by_id(db, room_id)
    if room:
        return jsonify(MeetingRoomInDB.model_validate(room).model_dump())
    return jsonify({"message": "Room not found"}), 404


@rooms_bp.route("/name/<string:name>", methods=["GET"])
def get_existing_room_by_name(name: str):
    """
    Retrieves a meeting room by name.
    """
    db: Session = next(get_db())
    room = get_room_by_name(db, name)
    if room:
        return jsonify(MeetingRoomInDB.model_validate(room).model_dump())
    return jsonify({"message": "Room not found"}), 404


@rooms_bp.route("/", methods=["GET"])
def get_all_rooms():
    """
    Retrieves all meeting rooms.
    """
    db: Session = next(get_db())
    skip = int(request.args.get("skip", 0))
    limit = int(request.args.get("limit", 100))
    rooms = get_rooms(db, skip, limit)
    return jsonify(
        [MeetingRoomInDB.model_validate(room).model_dump() for room in rooms]
    )


@rooms_bp.route("/<int:room_id>", methods=["PUT"])
def update_existing_room(room_id: int):
    """
    Updates an existing meeting room.
    """
    db: Session = next(get_db())
    try:
        room_data = MeetingRoomUpdate(**request.json)
    except ValidationError as e:
        return jsonify(e.errors()), 400
    updated_room = update_room(db, room_id, room_data)
    if updated_room:
        return jsonify(
            MeetingRoomInDB.model_validate(updated_room).model_dump()
        )
    return jsonify({"message": "Room not found"}), 404


@rooms_bp.route("/<int:room_id>", methods=["DELETE"])
def delete_existing_room(room_id: int):
    """
    Deletes a meeting room.
    """
    db: Session = next(get_db())
    if delete_room(db, room_id):
        return "", 204
    return jsonify({"message": "Room not found"}), 404
