from pydantic import BaseModel, Field, constr
from typing import Optional


class MeetingRoomBase(BaseModel):
    name: constr(min_length=3, max_length=100)
    capacity: int = Field(..., gt=0)
    description: Optional[str] = None


class MeetingRoomCreate(MeetingRoomBase):
    pass


class MeetingRoomUpdate(MeetingRoomBase):
    name: Optional[constr(min_length=3, max_length=100)] = None
    capacity: Optional[int] = Field(None, gt=0)


class MeetingRoomInDB(MeetingRoomBase):
    id: int

    class Config:
        from_attributes = True
