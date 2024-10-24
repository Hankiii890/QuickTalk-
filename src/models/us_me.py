import datetime
from database import Base
from database import engine
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey


class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)  # Пользователей с одинаковыми именами быть не может
    email = Column(String, nullable=False, unique=True)
    password = Column(String)


class Messages(Base):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True)
    sender_id = Column(Integer, ForeignKey("users.id"))    # Отправитель
    receiver_id = Column(Integer, ForeignKey("users.id"))    # Получатель
    content = Column(String, index=True)
    timestamp = Column(DateTime, default=datetime.timezone.utc)

    sender = relationship("Users", foreign_keys=[sender_id])
    receiver = relationship("Users", foreign_keys=[receiver_id])


Base.metadata.create_all(bind=engine)
