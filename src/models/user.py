from src.main import Base
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Integer, String


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)    # Пользователей с одинаковыми именами быть не может
    password = Column(String)
