from fastapi import FastAPI
from routs.routers import router

app = FastAPI()

app.include_router(router)
