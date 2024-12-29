from pydantic import BaseModel, Field, constr
from typing import Optional


class UserBase(BaseModel):
    username: constr(min_length=3, max_length=50)


class UserCreate(UserBase):
    password: str = Field(..., min_length=6)
    is_admin: bool = False


class UserUpdate(UserBase):
    is_admin: Optional[bool] = None


class UserInDB(UserBase):
    id: int
    is_admin: bool

    class Config:
        from_attributes = True
