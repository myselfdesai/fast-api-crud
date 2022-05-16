from datetime import datetime
from pydantic import BaseModel
from pydantic.networks import EmailStr

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    name: str
    password: str

class User(UserBase):
    id: int
    name: str
    last_login: datetime

    class Config:
        orm_mode = True
