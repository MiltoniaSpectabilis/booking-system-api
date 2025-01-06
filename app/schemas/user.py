from pydantic import BaseModel, Field, constr
from typing import Optional


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str = Field(..., min_length=6)
    is_admin: bool = False
    username: constr(min_length=3, max_length=50)


class UserUpdate(UserBase):
    is_admin: Optional[bool] = None
    username: Optional[constr(min_length=3, max_length=50)
                       ] = None


class UserInDB(UserBase):
    id: int
    is_admin: bool
    username: constr(min_length=3, max_length=50)

    class Config:
        from_attributes = True
