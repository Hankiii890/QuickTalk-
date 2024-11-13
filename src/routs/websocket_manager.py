from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[int, WebSocket] = {}  # Используем словарь для хранения соединений по user_id

    async def connect(self, user_id: int, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[user_id] = websocket  # Сохраняем соединение по user_id

    def disconnect(self, user_id: int):
        if user_id in self.active_connections:
            del self.active_connections[user_id]  # Удаляем соединение по user_id

    async def send_personal_message(self, message: str, user_id: int):
        websocket = self.active_connections.get(user_id)
        if websocket:
            await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections.values():
            await connection.send_text(message)


manager = ConnectionManager()