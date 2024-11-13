from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from .websocket_manager import manager
from sqlalchemy.orm import Session
from database import get_db
from model_db.us_me import Messages
import json
from datetime import datetime


routs = APIRouter()


@routs.websocket("/ws/{user_id}")
async def websockets_endpoints(websocket: WebSocket, user_id: int, db: Session = Depends(get_db)):
    print(f'Connect is {user_id}')
    await manager.connect(user_id, websocket)
    try:
        while True:
            data = await websocket.receive_text()
            message_data = json.loads(data)


            # Создаем новое сообщение в БД
            new_message = Messages(
                sender_id=user_id,
                receiver_id=message_data['receiver_id'],
                content=message_data['content'],
                timestamp=datetime.utcnow()
            )
            db.add(new_message)
            db.commit()
            db.refresh(new_message)

            # Отправка сообщений юзерам, которые онлайн
            if manager.active_connections.get(message_data['receiver_id']):
                await manager.send_personal_message(json.dumps({
                    'sender_id': user_id,
                    'content': message_data['content'],
                    'timestamp': new_message.timestamp.isoformat()
                })), message_data['receiver_id']

            # Подтверждение отправки
            await manager.send_personal_message(json.dumps({
                'status': 'sent',
                'message': new_message.id,
            }))

    except WebSocketDisconnect:
        manager.disconnect(user_id)
        await manager.broadcast(f'User {user_id} left the chat')


@routs.get("/active_connection")
async def online_user():
    active_users = list(manager.active_connections.keys())  # Получаем список активных user_id
    return {"Active users": active_users, "Count": len(active_users)}  # Возвращаем список и количество активных пользователей
