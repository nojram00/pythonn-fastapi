from pydantic import BaseModel
from typing import Optional

class UserQuery(BaseModel):
    id: str
    username: str
    password: Optional[str] = None
    role: str
    email: str

    class Config:
        orm_mode = True

class UserMutation(BaseModel):
    username: str
    password: str
    role: str
    email: str

    class Config:
        orm_mode = True

class UserUpdate(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    email: Optional[str] = None

    class Config:
        orm_mode = True

class UserCredential(BaseModel):
    email : str
    password : str

    class Config:
        orm_mode = True