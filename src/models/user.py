from database import Base
from database import engine
from sqlalchemy import Column, Integer, String


class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)  # Пользователей с одинаковыми именами быть не может
    email = Column(String, nullable=False, unique=True)
    password = Column(String)


Base.metadata.create_all(bind=engine)
