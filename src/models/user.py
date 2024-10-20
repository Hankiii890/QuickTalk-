from database import Base
from sqlalchemy import Column, Integer, String
from database import engine


class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)    # Пользователей с одинаковыми именами быть не может
    password = Column(String)


Base.metadata.create_all(bind=engine)
