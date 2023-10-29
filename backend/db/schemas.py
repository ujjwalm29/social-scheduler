from pydantic import BaseModel


class UserCreate(BaseModel):
    email: str
    name: str
    password: str
    profile_picture: str | None


class UserLogin(BaseModel):
    email: str
    password: str

