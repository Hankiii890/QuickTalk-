from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routs.auth import router as auth_router
from routs.message import router as message_router

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(auth_router)
app.include_router(message_router)