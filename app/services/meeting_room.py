from sqlalchemy.orm import Session
from app.models.meeting_room import MeetingRoom
from app.schemas.meeting_room import MeetingRoomCreate, MeetingRoomUpdate


def get_room_by_id(db: Session, room_id: int):
    return db.query(MeetingRoom).filter(MeetingRoom.id == room_id).first()


def get_room_by_name(db: Session, name: str):
    return db.query(MeetingRoom).filter(MeetingRoom.name == name).first()


def get_rooms(db: Session, skip: int = 0, limit: int = 100):
    return db.query(MeetingRoom).offset(skip).limit(limit).all()


def create_room(db: Session, room: MeetingRoomCreate):
    db_room = MeetingRoom(**room.dict())
    db.add(db_room)
    db.commit()
    db.refresh(db_room)
    return db_room


def update_room(db: Session, room_id: int, room: MeetingRoomUpdate):
    db_room = get_room_by_id(db, room_id)
    if not db_room:
        return None
    update_data = room.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_room, key, value)
    db.commit()
    db.refresh(db_room)
    return db_room


def delete_room(db: Session, room_id: int):
    db_room = get_room_by_id(db, room_id)
    if not db_room:
        return False
    db.delete(db_room)
    db.commit()
    return True
