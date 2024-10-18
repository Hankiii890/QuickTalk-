from src.main import Base
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey


class Messages(Base):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True)
    text = Column(String)
    create_at = Column(DateTime)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', backref='messages')
