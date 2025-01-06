from flask import Blueprint, jsonify, request
from app.schemas.meeting_room import (
    MeetingRoomCreate,
    MeetingRoomUpdate,
    MeetingRoomInDB
)
from app.services.meeting_room import (
    get_room_by_id,
    get_room_by_name,
    create_room,
    update_room,
    delete_room,
    get_rooms
)
from app.utils.database import get_db
from sqlalchemy.orm import Session

rooms_bp = Blueprint("rooms", __name__)


@rooms_bp.route("/rooms", methods=["POST"])
def create_new_room():
    db: Session = next(get_db())
    room_data = MeetingRoomCreate(**request.json)
    room = create_room(db, room_data)
    return jsonify(MeetingRoomInDB.from_orm(room).dict()), 201


@rooms_bp.route("/rooms/<int:room_id>", methods=["GET"])
def get_existing_room(room_id: int):
    db: Session = next(get_db())
    room = get_room_by_id(db, room_id)
    if room:
        return jsonify(MeetingRoomInDB.from_orm(room).dict())
    return jsonify({"message": "Room not found"}), 404


@rooms_bp.route("/rooms/name/<string:name>", methods=["GET"])
def get_existing_room_by_name(name: str):
    db: Session = next(get_db())
    room = get_room_by_name(db, name)
    if room:
        return jsonify(MeetingRoomInDB.from_orm(room).dict())
    return jsonify({"message": "Room not found"}), 404


@rooms_bp.route("/rooms", methods=["GET"])
def get_all_rooms():
    db: Session = next(get_db())
    skip = int(request.args.get("skip", 0))
    limit = int(request.args.get("limit", 100))
    rooms = get_rooms(db, skip, limit)
    return jsonify(
        [MeetingRoomInDB.from_orm(room).dict() for room in rooms]
    )


@rooms_bp.route("/rooms/<int:room_id>", methods=["PUT"])
def update_existing_room(room_id: int):
    db: Session = next(get_db())
    room_data = MeetingRoomUpdate(**request.json)
    updated_room = update_room(db, room_id, room_data)
    if updated_room:
        return jsonify(MeetingRoomInDB.from_orm(updated_room).dict())
    return jsonify({"message": "Room not found"}), 404


@rooms_bp.route("/rooms/<int:room_id>", methods=["DELETE"])
def delete_existing_room(room_id: int):
    db: Session = next(get_db())
    if delete_room(db, room_id):
        return jsonify({"message": "Room deleted"})
    return jsonify({"message": "Room not found"}), 404
