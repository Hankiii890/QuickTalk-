from pydantic import BaseModel
from datetime import datetime


class UserCreated(BaseModel):
    username: str
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str


class MessageCreated(BaseModel):
    sender_id: int
    receiver_id: int
    context: str


class MessageResponse(BaseModel):
    id: int
    sender_id: int
    receiver_id: int
    content: str
    timestamp: datetime

    class Config:
        """Для модели SQlAlchemy"""
        from_attributes = True
