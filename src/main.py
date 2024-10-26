from fastapi import FastAPI
from routs.auth import router as auth_router
from routs.message import router as message_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(message_router)

