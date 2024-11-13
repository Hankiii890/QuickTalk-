# Маршруты для отправки и получения сообщений

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from model_db.us_me import Messages
from database import get_db
from routs.models import MessageCreated, MessageResponse
import datetime

router = APIRouter()


@router.post("/send_message", response_model=MessageResponse)
async def send_message(message: MessageCreated, db: Session = Depends(get_db)):
    """Создание сообщения"""
    new_message = Messages(
        sender_id=message.sender_id,
        receiver_id=message.receiver_id,
        content=message.context,
        timestamp=datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)    # Преобразовали в UTC
    )
    db.add(new_message)
    db.commit()
    db.refresh(new_message)    # Обновляем объекты, чтобы получить ID и timestamp

    return new_message


@router.get("/message/{user_id}", response_model=list[MessageResponse])
async def get_message(user_id: int, db: Session = Depends(get_db)):
    message = db.query(Messages).filter(
        (Messages.sender_id == user_id) | (Messages.receiver_id == user_id)
    ).all()
    return message
