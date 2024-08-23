from pydantic import BaseModel, ConfigDict, EmailStr


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)


class User(BaseModel):
    id: int
    username: str
    email: EmailStr
    password: str
    model_config = ConfigDict(from_attributes=True)


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    model_config = ConfigDict(from_attributes=True)


class Message(BaseModel):
    message: str
