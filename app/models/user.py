from pydantic import BaseModel


class UserRegister(BaseModel):
    username: str
    hashed_password: str


class User(BaseModel):
    id: int
    username: str
    hashed_password: str


class UserDetail(BaseModel):
    id: int
    username: str
