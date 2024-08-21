from uuid import UUID

from pydantic import BaseModel


class UserResponse(BaseModel):
    id: UUID
    username: str
    email: str


class User(UserResponse):
    password: str
