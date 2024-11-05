from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from websocket_manager import manager

routs = APIRouter()


@routs.websocket("/ws/{user_id}")
async def websockets_endpoints(websocket: WebSocket, user_id: id):
    await manager.connect(user_id, websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # логика обработки сообщений
            await manager.send_personal_message(f'You wrote: {data}', f"- {user_id}")
    except WebSocketDisconnect:
        manager.Disconect(user_id)