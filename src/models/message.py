from database import Base
from database import engine
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey


class Messages(Base):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True)
    text = Column(String)
    create_at = Column(DateTime)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', backref='messages')


Base.metadata.create_all(engine)


