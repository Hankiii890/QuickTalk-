from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from .websocket_manager import manager


routs = APIRouter()


@routs.websocket("/ws/{user_id}")
async def websockets_endpoints(websocket: WebSocket, user_id: id):
    await manager.connect(user_id, websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # логика обработки сообщений
            await manager.send_personal_message(f"You wrote: {data}", websocket)
            await manager.broadcast(f"Client #{user_id} say: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f'Client #{user_id} left this chat')
