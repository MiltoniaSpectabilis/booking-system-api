from pydantic import BaseModel, validator
from datetime import datetime
from typing import Optional


class BookingBase(BaseModel):
    start_time: datetime
    end_time: datetime

    @validator("end_time")
    def validate_end_time(cls, value, values):
        if "start_time" in values and value <= values["start_time"]:
            raise ValueError("end_time must be greater than start_time")
        return value


class BookingCreate(BookingBase):
    user_id: int
    room_id: int


class BookingUpdate(BookingBase):
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None


class BookingInDB(BookingBase):
    id: int
    user_id: int
    room_id: int

    class Config:
        from_attributes = True
